import logging
import sys


def setup_logging() -> None:    
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s: %(asctime)s - %(name)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logging.getLogger("mcp").setLevel(logging.INFO)
    logging.getLogger("tools").setLevel(logging.INFO)
    logging.getLogger("service").setLevel(logging.INFO)

if __name__ != "__main__":
    setup_logging()