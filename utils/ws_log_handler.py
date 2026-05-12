import logging
import asyncio
from apis.routes.log_manager import manager

class WebSocketLogHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        try:
            asyncio.create_task(manager.send_log(log_entry))
        except RuntimeError:
            # Not in event loop, fallback (optional: queue for later)
            pass