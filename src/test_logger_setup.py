import sys
import os
import json
import logging.config

#import my_module

def setup_logging(
    default_path=None,
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
        
def main(Mypath):
    
    setup_logging(default_path=MyPath)    
    logger = logging.getLogger(__name__)
    logger.info('Startlogging:')
    
    for k,v in  logging.Logger.manager.loggerDict.items()  :
        print('+ [%s] {%s} ' % (str.ljust( k, 20)  , str(v.__class__)[8:-2]) )
        if not isinstance(v, logging.PlaceHolder):
            for h in v.handlers:
                print('     +++',str(h.__class__)[8:-2] )
                
    #my_module.foo()    
    #b = my_module.Bar()
    #b.bar()
    #logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    logger.info("this is info")
    logger.debug("this is debug")
    
if __name__ == '__main__':
    dir = '/Users/klein/git/speedtest/config/'
    file = 'logger.json'
    MyPath = dir+file
    main(MyPath)