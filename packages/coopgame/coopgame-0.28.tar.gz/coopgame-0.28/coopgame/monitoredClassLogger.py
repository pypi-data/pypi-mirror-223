from typing import List
from coopgame.logger import logger
from cooptools.decor import TimeableProtocol

class MonitoredClassLogger():

    def __init__(self,
                 log_interval_ms: int = 10000,
                 monitored_classes: List[TimeableProtocol] = None):
        self.time_since_report_stats = 0
        self.log_interval_ms = log_interval_ms
        self.monitored_classes: List[TimeableProtocol] = monitored_classes if monitored_classes else []

    def check_and_log(self,
                      delta_time_ms: int):
        self.time_since_report_stats += delta_time_ms
        if self.time_since_report_stats > self.log_interval_ms:
            for item in self.monitored_classes:
                print_dict = {method: round(time, 3) for method, time in item.internally_tracked_times.items()}
                logger.info(f"{item} -- {print_dict}")

            self.time_since_report_stats = 0

    def register_classes(self, new: List[TimeableProtocol]):
        self.monitored_classes += new