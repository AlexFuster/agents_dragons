import logging

# ANSI color codes
COLORS = [
    '\033[91m',  # Red
    '\033[92m',  # Green
    '\033[93m',  # Yellow
    '\033[94m',  # Blue
    '\033[95m',  # Magenta
    '\033[96m',  # Cyan
    '\033[31m',  # Dark Red
    '\033[32m',  # Dark Green
    '\033[33m',  # Dark Yellow
    '\033[35m',  # Dark Magenta
    '\033[36m',  # Dark Cyan
]
RESET = '\033[0m'


def config_logging(agent_name: str) -> logging.Logger:
    """
    Configures a logger for the given agent name with a unique color.
    """
    logger = logging.getLogger(agent_name)
    color = COLORS[hash(agent_name) % len(COLORS)]
    
    colored_formatter = logging.Formatter(
        f'{color}[%(name)s]{RESET} %(message)s'
    )
    handler = logging.StreamHandler()
    handler.setFormatter(colored_formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    return logger