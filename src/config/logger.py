import logging
import json
from datetime import datetime
from typing import Any, Dict
import uuid

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_record: Dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name
        }
        
        # if hasattr(record, "extra"):
        #     log_record.update(record.extra)
            
        # return json.dumps(log_record)

        # Creating dynamic extra fields safely
        for key, value in record.__dict__.items():
            if key not in (
                "name", "msg", "args", "levelname", "levelno",
                "pathname", "filename", "module", "exc_info",
                "exc_text", "stack_info", "lineno", "funcName",
                "created", "msecs", "relativeCreated",
                "thread", "threadName", "processName", "process"
            ):
                log_record[key] = value
                
        return json.dumps(log_record)
            
            
def setup_logger(name: str = "agent") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    
    if not logger.handlers:
        logger.addHandler(handler)
        
    logger.propagate = False
    return logger

def generate_run_id() -> str:
    return str(uuid.uuid4())