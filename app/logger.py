import logging
import sys

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,  # Change to DEBUG for more verbosity
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )
