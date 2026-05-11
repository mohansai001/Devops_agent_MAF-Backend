import logging

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        # Console handler
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        # File handler
        file_handler = logging.FileHandler(f"{name}.log", encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # WebSocket handler
        try:
            from utils.ws_log_handler import WebSocketLogHandler
            ws_handler = WebSocketLogHandler()
            ws_handler.setFormatter(formatter)
            logger.addHandler(ws_handler)
        except ImportError:
            pass  # Avoid circular import during handler definition

    logger.setLevel(logging.INFO)
    return logger