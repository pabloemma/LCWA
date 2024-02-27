import sys
import os
import json
import logging.config

import my_module

def setup_logging(
    default_path='logging.json',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """
    Setup logging configuration
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def main():
    
    setup_logging()    
    logger = logging.getLogger(__name__)
    logger.info('Startlogging:')
                
    my_module.foo()    
    b = my_module.Bar()
    b.bar()
    
    print logger.handlers
    
if __name__ == '__main__':
    main()