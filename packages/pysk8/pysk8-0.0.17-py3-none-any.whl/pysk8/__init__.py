import sys
import logging

from . import core

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def setLoglevel(lvl=logging.WARN):
    """Shortcut method to set pysk8.core loglevel
    
    Args: 
        lvl (int): a standard level enum from the logging module

    Returns:
        nothing
    """
    core.logger.setLevel(lvl)    
