import logging

import pygame
from coopstructs.geometry import Rectangle
from coopgame.colors import Color
import functools
from coopgame.pygbutton import PygButton
from cooptools.decor import timer, try_handler, MonitoredClassTimer
from typing import Callable, List, Dict, Optional, Any, Protocol
import coopgame.pygamehelpers as help
from coopgame.logger import logger
from coopgame.spriteHandling.sprites import AnimatedSprite
from coopstructs.geometry import Rectangle as cRect
# from coopgame.monitoredClassLogger import MonitoredClassLogger
from cooptools.coopEnum import CoopEnum
from enum import auto
import inspect
from coopgame.pygame_k_constant_names import pygame_key_mapper, PyKeys, PyMouse
from coopgame.gameTimeTracker import GameTimeTracker
from coopstructs.toggles import BooleanToggleable
from cooptools.dataRefresher import DataRefresher
from cooptools.timedDecay import Timer
from coopgame.pyLabel import TextAlignmentType
from coopgame.handleKeyPressedArgs import InputState, InputStateHandler, InputAction, InputEvent, InputEventType, InputType, CallbackPackage

DEBUG_COLORKEY = Color.DARK_SLATE_GRAY
DEBUGGER_MASK_ALPHA = 65
key_mapper = Callable[[InputState], Any]

class BuiltInSurfaceType(CoopEnum):
    BACKGROUND = auto()
    FOREGROUND = auto()
    HELP = auto()
    DEBUGGER = auto()
    DEBUGGER_MASK = auto()

class GameTemplate:

    def __init__(self,
                 fullscreen: bool = False,
                 screen_width: int = 1000,
                 screen_height: int = 500,
                 max_fps: int = 120,
                 debug_mode=False,
                 input_state_handler: InputStateHandler = None,
                 log_stats_interval_ms: int = 5000):
        self.init_screen_width = screen_width
        self.init_screen_height = screen_height
        self.log_stats_interval_ms = log_stats_interval_ms

        self.fullscreen = fullscreen
        self.screen: pygame.Surface = None
        self._init_screen(self.fullscreen, self.screen_width, self.screen_height)

        self.debug_mode_toggle = BooleanToggleable(default=debug_mode)

        self.input_state_handler = input_state_handler if input_state_handler is not None else \
            InputStateHandler(quit_callback_package=CallbackPackage(down=lambda x: self.quit()),
                              debug_callback_package=CallbackPackage(down=lambda x: self.debug_mode_toggle.toggle()),
                              fullscreen_callback_package=CallbackPackage(down=lambda x: self.toggle_fullscreen()))
        self.game_time_tracker = GameTimeTracker(max_fps=max_fps)

        self.running = False

        self.debug_surface_update_timer = Timer(100, True)

        self.buttons = {}
        self.sprites = {}

        # build in surfaces
        self.built_in_surfaces: Dict[BuiltInSurfaceType, Optional[pygame.Surface]] = {
            BuiltInSurfaceType.BACKGROUND: None,
            BuiltInSurfaceType.FOREGROUND: None,
            BuiltInSurfaceType.HELP: None,
            BuiltInSurfaceType.DEBUGGER: None
        }

        self.game_time_tracker.set_start()
        self.log_stats_refresher = DataRefresher('log_stats',
                                                 refresh_callback=lambda: logger.info(
                                                     f"FPS: {int(self.game_time_tracker.fps) if self.game_time_tracker.fps else None}"),
                                                 refresh_interval_ms=1000)
        pygame.init()

    def quit(self):
        self.running = False

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self._init_screen(self.fullscreen, self.screen_width, self.screen_height)

    def _init_screen(self, fullscreen=None, screen_width=None, screen_height=None):
        if fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        elif screen_width and screen_height:
            self.screen = pygame.display.set_mode((self.init_screen_width, self.init_screen_height))
        else:
            self.screen = pygame.display.set_mode((0, 0))

    def register_button(self, id, text, callback, postion_rect):
        self.buttons[id] = PygButton(postion_rect, caption=text, callback=callback)

    def main(self, debug: bool = False):
        self.debug_mode_toggle.set_value(debug)

        self.init_builtin_surfaces()
        self.initialize_game()

        self.running = True

        while self.running:
            self._update()
            self._draw(frames=self.game_time_tracker.frames)

        pygame.quit()

    def _update(self):
        """:return
            Update environment based on time delta and any input
        """

        ''' Calculate the ticks between update calls so that the update functions can handle correct time deltas '''
        delta_time_ms = self.game_time_tracker.update()

        '''Log Stats'''
        MonitoredClassTimer.check_and_log(logger=logging.getLogger('coopgame_stats'), delta_time_ms=delta_time_ms, log_interval_ms=self.log_stats_interval_ms)
        self.log_stats_refresher.check_and_refresh()

        '''Handle Events'''
        """ Handling events should come before updating the model so that any updates to input, etc
        are appropriately handled in the model prior to drawing. O/w, the draw can be written explicitly
        on the last state (not model) and can cause it to be out of order"""
        self._handle_events(delta_time_ms)

        '''Update Model'''
        self._model_updater(delta_time_ms)

        '''Update Sprites'''
        self.sprite_updater(delta_time_ms)

        '''Animate Sprites'''
        self._sprite_animator(delta_time_ms)

    def _handle_events(self, delta_time_ms: int):
        """:return
            handle all of the registered events that have been captured since last iteration
        """

        '''Mouse Pos'''
        inp_state = InputState(delta_ms=delta_time_ms)
        inp_state.register(mouse_pos=help.mouse_pos_as_vector().as_tuple())

        '''Get next event'''
        for event in pygame.event.get():
            '''Check and handle button press'''
            self.handle_buttons(event)

            '''Debug Printer'''
            if event.type not in (0, 1, 4, 6):
                logger.debug(f"Pygame EventType: {event.type}")

            '''Event Type Switch'''
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                inp_state.register(events=[InputEvent(event_type=InputEventType.DOWN, input_key=PyKeys.by_val(event.key))])
            elif event.type == pygame.MOUSEBUTTONDOWN:
                inp_state.register(events=[InputEvent(event_type=InputEventType.DOWN, input_key=PyMouse.by_val(event.button))])
            elif event.type == pygame.KEYUP:
                inp_state.register(events=[InputEvent(event_type=InputEventType.UP, input_key=PyKeys.by_val(event.key))])
            elif event.type == pygame.MOUSEBUTTONUP:
                inp_state.register(events=[InputEvent(event_type=InputEventType.UP, input_key=PyMouse.by_val(event.button))])
            elif event.type == pygame.WINDOWSIZECHANGED:
                self._on_resize()
            else:
                logger.debug(f"Unhandled event: {event.type}")

        '''Handle Input State'''
        self.input_state_handler.handle_input(inp_state)

    def register_action_to_keys(self, keys_tuple, func: key_mapper, react_while_holding: bool = False):
        """
            Takes a tuple of keys (integers) and maps that key combo to a callable function

            :param keys_tuple a list of keys (integers) that will be mapped to the input callable. Note that a single
            value Tuple is input as ([key],) *note the comma
            :param func a callable that is mapped to the key combo
        """
        self._key_handlers[keys_tuple] = (func, react_while_holding)

    @MonitoredClassTimer.timer()
    @try_handler(logger=logger)
    def handle_buttons(self, event):
        for id, button in self.buttons:
            if 'click' in button.handleEvent(event):
                button.callback()

    @try_handler(logger=logger)
    def _model_updater(self, delta_time_ms: int):
        return self.model_updater(delta_time_ms)

    @try_handler(logger=logger)
    def initialize_game(self):
        raise NotImplementedError()

    @try_handler(logger=logger)
    def handle_hover_over(self, input_state: InputState):
        raise NotImplementedError()

    @MonitoredClassTimer.timer()
    @try_handler(logger=logger)
    def draw(self, frames: int, debug_mode: bool = False):
        raise NotImplementedError()

    @MonitoredClassTimer.timer()
    @try_handler(logger=logger)
    def model_updater(self, delta_time_ms: int):
        raise NotImplementedError()

    @MonitoredClassTimer.timer()
    @try_handler(logger=logger)
    def sprite_updater(self, delta_time_ms: int):
        raise NotImplementedError()

    def _on_resize(self):
        logger.info(f"Window Resized [{self.screen.get_width()}x{self.screen.get_height()}]")
        self.init_builtin_surfaces()
        self.on_resize()

    @try_handler(logger=logger)
    def on_resize(self):
        raise NotImplementedError()

    @MonitoredClassTimer.timer()
    @try_handler(logger=logger)
    def update_built_in_surfaces(self, surface_types: List[BuiltInSurfaceType]):
        raise NotImplementedError()

    def _draw(self, frames: int):
        self.screen.fill(Color.BLACK.value)
        self.draw(frames, self.debug_mode_toggle.value)

        '''Draw Sprites'''
        self.sprite_drawer(self.screen)

        if self.debug_mode_toggle.value:
            self._check_update_debugger_surface()
            self.screen.blit(self.built_in_surfaces[BuiltInSurfaceType.DEBUGGER_MASK], (0, 0))
            self.screen.blit(self.built_in_surfaces[BuiltInSurfaceType.DEBUGGER], (0, 0))

        # Update the display
        pygame.display.flip()

    def _check_update_debugger_surface(self):
        if self.debug_surface_update_timer.finished:
            self._update_debugger_surface()
            self.debug_surface_update_timer.reset()

    def _update_debugger_surface(self):
        deb_surf = self.built_in_surfaces[BuiltInSurfaceType.DEBUGGER]
        if deb_surf is None:
            return

        deb_surf.fill(DEBUG_COLORKEY.value)
        help.draw_text(f"Sprite Count: {len(self.sprites)}", deb_surf,
                       offset_rect=cRect.from_tuple((self.screen.get_width() - 400, self.screen.get_height() - 100, 400, 20)),
                       alignment=TextAlignmentType.TOPRIGHT,
                       color=Color.WHITE)
        help.draw_fps(deb_surf,
                      fps=self.game_time_tracker.fps,
                      offset_rect=cRect.from_tuple((self.screen.get_width() - 400, self.screen.get_height() - 80, 400, 20)),
                      alignment=TextAlignmentType.TOPRIGHT,
                      color=Color.WHITE
                      )
        help.draw_mouse_coord(deb_surf,
                              offset_rect=cRect.from_tuple((self.screen.get_width() - 400, self.screen.get_height() - 40, 400, 20)),
                              alignment=TextAlignmentType.TOPRIGHT,
                              color=Color.WHITE)
        help.draw_game_time(deb_surf,
                            game_time_s=self.game_time_tracker.ticks / 1000,
                            offset_rect=cRect.from_tuple((self.screen.get_width() - 400, self.screen.get_height() - 60, 400, 20)),
                            alignment=TextAlignmentType.TOPRIGHT,
                            color=Color.WHITE)

        self.draw_monitoredclass_stats(surface=deb_surf)

    def draw_monitoredclass_stats(self,
                                  surface: pygame.Surface):
        offset = 0
        offset = help.draw_dict(dict_to_draw=MonitoredClassTimer.internally_tracked_times,
                                surface=surface,
                                g_offset=offset,
                                total_game_time_sec=self.game_time_tracker.ticks / 1000,
                                title=f"RunTime Stats")

    def _sprite_animator(self,
                         delta_time_ms: int):

        for name, sprite in self.sprites.items():
            if type(sprite) == AnimatedSprite:
                sprite.animate(delta_time_ms)

    def sprite_drawer(self,
                      surface: pygame.surface):

        sprites = list(self.sprites.values())
        sprites.sort(key=lambda x: x.bottom_center_pos.y)
        for sprite in sprites:
            sprite.blit(surface, display_handle=self.debug_mode_toggle.value, display_rect=self.debug_mode_toggle.value)

    # def register_monitored_classes(self, new_classes: List[TimeableProtocol]):
    #     self._monitored_class_logger.register_classes(new_classes)

    def init_builtin_surfaces(self, types: List[BuiltInSurfaceType] = None, colorkey: Color = None):
        if colorkey is None: colorkey = DEBUG_COLORKEY
        if types is None: types = [e for e in BuiltInSurfaceType]

        for type in types:
            self.built_in_surfaces[type] = pygame.Surface(self.screen.get_size()).convert()
            self.built_in_surfaces[type].set_colorkey(colorkey.value)
            if type == BuiltInSurfaceType.DEBUGGER_MASK:
                self.built_in_surfaces[type].set_alpha(DEBUGGER_MASK_ALPHA)


    def _update_help_surface(self):
        text = self._help_txt()

        self.built_in_surfaces[BuiltInSurfaceType.HELP].fill(Color.WHEAT.value)

        font = pygame.font.Font(None, 20)
        fontsize = font.get_height()
        offSet = 0

        for idx, line in enumerate(text):
            help.draw_text(line,
                           self.built_in_surfaces[BuiltInSurfaceType.HELP],
                           font=font,
                           offset_rect=Rectangle.from_tuple((0,
                                                 idx * fontsize + offSet,
                                                 fontsize + 3,
                                                 self.built_in_surfaces[BuiltInSurfaceType.HELP].get_width())))

    def _help_txt(self):

        txt = []
        txt.append("HELP")
        txt.append("\n--------")
        txt.append("\n")
        for k, v in self._key_handlers.items():
            if len(v) > 2:
                callback_txt = v[2]
            elif v[0].__name__ == "<lambda>":
                callback_txt = inspect.getsource(v[0])
                callback_txt = callback_txt.split("lambda:", 1)[1].split('(', 1)[0].replace("self.", "")
            else:
                callback_txt = v[0].__name__
            k_tup = [pygame_key_mapper(x) for x in k]
            txt.append(f"{k_tup} -- {callback_txt}")

        return txt

    @property
    def screen_width(self):
        return self.screen.get_width() if self.screen else self.init_screen_width

    @property
    def screen_height(self):
        return self.screen.get_height() if self.screen else self.init_screen_height

    @property
    def game_area_rectangle(self):
        return Rectangle.from_tuple((0, 0, self.screen.get_width(), self.screen.get_height()))

if __name__ == "__main__":
    gt = GameTemplate()
    gt.main(debug=True)