from cooptools.sectors.grids import RectGrid
from coopgraph.dataStructs import GridPoint
from coopstructs.geometry import Rectangle
import pygame
from coopgame.colors import Color
from typing import Dict, Callable, Tuple
from coopgame.enums import GridDrawType
import coopgame.pygamehelpers as help
from typing import List
from coopstructs.geometry.vectors.vectorN import Vector2
import numpy as np
from cooptools.decor import timer
from cooptools.decor import timer, try_handler, MonitoredClassTimer

class PyGridHandler:

    def __init__(self):
        super().__init__()
        self.hover_grid_pos = None

    @timer
    def _check_and_handle_hover_grid_change(self, old_hover: Vector2, new_hover: Vector2, handlers: List[Callable[[Vector2, Vector2], None]]):
        if new_hover != self.hover_grid_pos:
            [handler(old_hover, new_hover) for handler in handlers or []]

    @MonitoredClassTimer.timer()
    def handle_hover_over(self,
                          grid: RectGrid,
                          area_rect: Rectangle,
                          on_hover_handlers: List[Callable[[Vector2], None]] = None,
                          on_hover_changed_handlers: List[Callable[[Vector2, Vector2], None]] = None,
                          draw_scale_matrix = None):
        # get hovered grid pos
        mouse_pos = help.mouse_pos_as_vector()
        new_hover = self.get_mouse_grid_pos(area_rect, mouse_pos, grid.grid_from_coord, draw_scale_matrix)

        # check and handle when hover grid pos changed
        self._check_and_handle_hover_grid_change(old_hover=self.hover_grid_pos, new_hover=new_hover, handlers=on_hover_changed_handlers)

        # Update the grid pos
        self.hover_grid_pos = new_hover

        # handle grid hover
        [handler(self.hover_grid_pos) for handler in on_hover_handlers or []]

    @MonitoredClassTimer.timer()
    def grid_box_rectangle(self, width, height, grid:RectGrid, margin: int = 0) -> Rectangle:

        grid_box_height = height / grid.nRows - 2 * margin
        grid_box_width = width / grid.nColumns - 2 * margin

        return Rectangle.from_tuple((0,0, grid_box_width, grid_box_height))

    @MonitoredClassTimer.timer()
    def draw_overlay_to_surface(self
                                , surface:pygame.Surface
                                , grid: RectGrid
                                , margin: int = 0
                                , hover: Tuple[Vector2, Color] = None
                                , toggled: Tuple[str, Color] = None
                                , additional_highlight_grid_cells: Dict[Vector2, Color] = None
                                , outlined_grid_cells: Dict[Vector2, Color] = None
                                , draw_scale_matrix = None
                                ):
        grid_box_rect = self.grid_box_rectangle(width=surface.get_width(), height=surface.get_height(), grid=grid, margin=margin)
        self._draw_highlighted_grids(surface=surface,
                                     grid=grid,
                                     grid_box_rect=grid_box_rect,
                                     hover=hover,
                                     toggled=toggled,
                                     additional_highlight_grid_cells=additional_highlight_grid_cells,
                                     draw_scale_matrix = draw_scale_matrix)
        self._draw_outlined_grids(surface=surface
                                    , grid_box_rect=grid_box_rect
                                    , outlined_grid_cells=outlined_grid_cells
                                    , margin=margin
                                    , draw_scale_matrix = draw_scale_matrix)
    @MonitoredClassTimer.timer()
    def draw_base_to_surface(self
             , surface:pygame.Surface
             , grid: RectGrid
             , grid_draw_type: GridDrawType = None
             , grid_color: Color = None
             , margin:int=0
             , draw_scale_matrix: np.array = None
             , center_guide_color: Color = None):
        if grid_draw_type is None:
            grid_draw_type = GridDrawType.BOXES

        if grid_color is None:
            grid_color = Color.BLACK

        if grid_draw_type == GridDrawType.BOXES:
            self._draw_grid_boxes(surface=surface, grid=grid, margin=margin, grid_color=grid_color, draw_scale_matrix = draw_scale_matrix)
        elif grid_draw_type == GridDrawType.LINES:
            self._draw_grid_lines(surface=surface, grid=grid, margin=margin, grid_color=grid_color, draw_scale_matrix = draw_scale_matrix)

        if center_guide_color is not None:
            rs, cs = self.define_center_grids(grid)
            highlights = {}
            row_highlights = {Vector2(r, c): center_guide_color for r in rs for c in range(0, grid.nColumns) }
            col_highlights = {Vector2(r, c): center_guide_color for r in range(0, grid.nRows) for c in cs}
            grid_box_rect = self.grid_box_rectangle(surface.get_width(), surface.get_height(), grid, margin)
            highlights.update(col_highlights)
            highlights.update(row_highlights)
            self._draw_highlighted_grids(surface,
                                         grid_box_rect=grid_box_rect,
                                         additional_highlight_grid_cells=highlights,
                                         draw_scale_matrix=draw_scale_matrix)

    @MonitoredClassTimer.timer()
    def define_center_grids(self,
                            grid: RectGrid):
        if grid.nRows % 2 == 0:
            center_rows = [grid.nRows / 2 + 1, grid.nRows / 2]
        else:
            center_rows = [(grid.nRows - 1 / 2) + 1]

        if grid.nColumns % 2 == 0:
            center_cols = [grid.nColumns / 2 + 1, grid.nColumns / 2]
        else:
            center_cols = [(grid.nColumns - 1 / 2) + 1]

        return (center_rows, center_cols)

    @MonitoredClassTimer.timer()
    def _draw_outlined_grids(self, surface:pygame.Surface,
                             grid_box_rect: Rectangle,
                             margin=0,
                             outlined_grid_cells: Dict[Vector2, Color] = None,
                             draw_scale_matrix = None):
        if outlined_grid_cells is None or len(outlined_grid_cells) == 0:
            return

        for grid_pos, color in outlined_grid_cells.items():
            if color is None:
                color = Color.YELLOW

            rect = Rectangle.from_tuple(((margin + grid_box_rect.width) * grid_pos.x + margin
                             , (margin + grid_box_rect.height) * grid_pos.y + margin
                             , grid_box_rect.height
                             , grid_box_rect.width))
            my_image = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            pygame.draw.rect(my_image, color.value, my_image.get_rect(), 3)
            surface.blit(my_image, (rect.x, rect.y))


    def hover_highlighted_grid(self,
                               grid: RectGrid,
                               hover: Vector2,
                               color: Color) -> Dict[Vector2, Color]:
        highlights = {}

        if hover is not None and grid.nColumns > hover.x >= 0 and grid.nRows > hover.y >= 0:
            highlights[hover] = color

        return highlights

    def toggled_highlighted_grids(self,
                                grid: RectGrid,
                                toggle_key: str,
                                color: Color) -> Dict[Vector2, Color]:
        highlights = {}

        grid_value_array = grid.state_value_as_array(key=toggle_key)
        for x in range(0, grid.nColumns):
            for y in range(0,  grid.nRows):
                if grid_value_array[y][x].value:
                    highlights[Vector2(y, x)] = color

        return highlights

    @MonitoredClassTimer.timer()
    def _draw_highlighted_grids(self,
                                surface:pygame.Surface,
                                grid: RectGrid,
                                grid_box_rect: Rectangle,
                                hover: Tuple[Vector2, Color] = None,
                                toggled: Tuple[str, Color] = None,
                                additional_highlight_grid_cells: Dict[Vector2, Color] = None,
                                draw_scale_matrix = None):
        highlights = {}

        if hover is not None:
            hover_highlights = self.hover_highlighted_grid(grid=grid,
                                                      hover=hover[0],
                                                      color=hover[1])
            highlights = {**highlights, **hover_highlights}

        if toggled is not None:
            toggled_highlights = self.toggled_highlighted_grids(grid=grid,
                                                                 toggle_key=toggled[0],
                                                                 color=toggled[1])

            highlights = {**highlights, **toggled_highlights}

        if additional_highlight_grid_cells is not None:
            highlights = {**highlights, **additional_highlight_grid_cells}

        if draw_scale_matrix is None:
            draw_scale_matrix = np.identity(4)

        for grid_pos, color in highlights.items():
            if color is None:
                color = Color.YELLOW
            points = help.scaled_points_of_a_rect(grid_box_rect,
                                                  grid_pos,
                                                  draw_scale_matrix)[:, :2]

            help.draw_polygon(surface, list(points), color)

    @MonitoredClassTimer.timer()
    def _draw_grid_boxes(self, surface:pygame.Surface, grid: RectGrid, margin=0, grid_color: Color = None, draw_scale_matrix = None):
        grid_box_rect = self.grid_box_rectangle(surface.get_width(), surface.get_height(), grid, margin)

        if draw_scale_matrix is None:
            draw_scale_matrix = np.identity(4)


        for y in range(0, grid.nRows):
            for x in range(0, grid.nColumns):
                points = help.scaled_points_of_a_rect(grid_box_rect, Vector2(x, y), draw_scale_matrix)[:, :2]
                help.draw_polygon(surface, list(points), grid_color)

    @MonitoredClassTimer.timer()
    def _draw_grid_lines(self, surface:pygame.Surface, grid: RectGrid, margin=0, grid_color: Color = None, draw_scale_matrix = None):
        grid_box_rect = self.grid_box_rectangle(surface.get_width(), surface.get_height(), grid, margin)

        if draw_scale_matrix is None:
            draw_scale_matrix = np.identity(4)

        '''Draw each line'''
        for x in range(0, grid.nColumns + 1):
            point_x1 = x * (grid_box_rect.width + margin)
            point_y1 = 0
            start = draw_scale_matrix.dot(np.array([point_x1, point_y1, 0, 1]))
            point_x2 = x * (grid_box_rect.width + margin)
            point_y2 = (grid_box_rect.height + margin) * grid.nRows
            end = draw_scale_matrix.dot(np.array([point_x2, point_y2, 0, 1]))
            _s = tuple(start[:2].astype(int))
            _e = tuple(end[:2].astype(int))
            pygame.draw.aaline(surface, grid_color.value, _s, _e)
        for y in range(0, grid.nRows + 1):
            start = draw_scale_matrix.dot(np.array([0, y * (grid_box_rect.height + margin), 0, 1]))
            end = draw_scale_matrix.dot(np.array([(grid_box_rect.width + margin) * grid.nColumns, y * (grid_box_rect.height + margin), 0, 1]))
            _s = tuple(start[:2])
            _e = tuple(end[:2])
            pygame.draw.aaline(surface, grid_color.value, _s, _e)

    @MonitoredClassTimer.timer()
    def get_mouse_grid_pos(self, game_area_rect: Rectangle, mouse_pos: Vector2, coord_to_grid_converter: Callable[[Tuple[float, float], Tuple[float, float, float, float]], Tuple[float, float]], draw_scale_matrix = None):
        if draw_scale_matrix is None:
            draw_scale_matrix = np.identity(4)

        draw_scale_matrix_inv = np.linalg.inv(draw_scale_matrix)

        # test = draw_scale_matrix_inv.dot(draw_scale_matrix)
        """Gets the mouse position and converts it to a grid position"""
        mouse_game_area_coord = help.game_area_coords_from_parent_coords(parent_coords=mouse_pos, game_area_surface_rectangle=game_area_rect)
        mouse_over_grid_coords = help.viewport_point_on_plane(mouse_game_area_coord, game_area_rect, draw_scale_matrix, margin=0)
        points = np.array([mouse_over_grid_coords[0], mouse_over_grid_coords[1], mouse_over_grid_coords[2], 1])
        grid_coords = draw_scale_matrix_inv.dot(np.transpose(points))

        # return coord_to_grid_converter(mouse_game_area_coord, game_area_rect)
        return coord_to_grid_converter((grid_coords[0], grid_coords[1]), game_area_rect.Dims)

    @MonitoredClassTimer.timer()
    def grid_point_to_viewport_point(self, surface: pygame.Surface, grid, grid_pos: Vector2, grid_point_type: GridPoint = GridPoint.CENTER, margin: int = 0, draw_scale_matrix = None):
        grid_box_rect = self.grid_box_rectangle(surface.get_width(), surface.get_height(), grid, margin)
        grid_box_scaled_points = help.scaled_points_of_a_rect(grid_box_rect, grid_pos=grid_pos, draw_scale_matrix=draw_scale_matrix)

        if grid_point_type == GridPoint.CENTER:
            x = sum(point[0] for point in grid_box_scaled_points)/len(grid_box_scaled_points)
            y = sum(point[1] for point in grid_box_scaled_points) / len(grid_box_scaled_points)
            return Vector2(x, y)
        elif grid_point_type == GridPoint.ORIGIN:
            return Vector2(grid_box_scaled_points[0][0], grid_box_scaled_points[0][1])
        else:
            raise NotImplementedError(f"Unimplemented grid_point_type {grid_point_type}")

    @MonitoredClassTimer.timer()
    def grid_pos_definition(self,
                            grid: RectGrid,
                            grid_pos: Vector2,
                            game_area_rect: Rectangle) -> Rectangle:
        grid_box_rect = self.grid_box_rectangle(game_area_rect.width, game_area_rect.height, grid)
        origin = Vector2(grid_pos.x * grid_box_rect.width, grid_pos.y * grid_box_rect.height)

        return Rectangle(origin.x, origin.y, grid_box_rect.height, grid_box_rect.width)



if __name__ == "__main__":
    grid = RectGrid(10, 10)
    grid_pos = Vector2(5, 9)
    game_area_rect = Rectangle(0, 0, 1500, 2000)

    grid_handler = PyGridHandler()
    grid_def = grid_handler.grid_pos_definition(grid, grid_pos, game_area_rect)

    print(grid_def)
    print(grid_def.center)

