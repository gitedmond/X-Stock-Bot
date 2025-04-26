"""
Scheduling functionality for the RSI Notifier application.
"""
import logging
import time
import schedule
from rsi_notifier.config import SCHEDULE_TIMES
from datetime import datetime

class Scheduler:
    """Manages the scheduling of RSI checks."""
    
    def __init__(self, rsi_notifier):
        """
        Initialize the scheduler.
        
        Args:
            rsi_notifier (RSINotifier): Instance of the RSI notifier.
        """
        self.rsi_notifier = rsi_notifier
        self.logger = logging.getLogger(__name__)
    
    def start(self):
        """Configure and start the scheduler."""
        self._setup_schedule()
        self._run_scheduler()
    
    def _setup_schedule(self):
        """Set up the schedule for RSI checks."""
        for time_str in SCHEDULE_TIMES:
            schedule.every().day.at(time_str).do(self.rsi_notifier.batch_check_rsi)
            self.logger.info(f"Scheduled RSI check at {time_str}")
    
    def _run_scheduler(self):
        """Run the scheduler continuously."""
        self.logger.info("Scheduler running. Press Ctrl+C to exit.")
        try:
            while True:
                now = datetime.now().strftime("%H:%M:%S")
                self.logger.debug(f"[{now}] Waiting for next scheduled task...")
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            self.logger.info("Scheduler stopped by user")