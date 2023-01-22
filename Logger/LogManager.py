import logging
from enum import Enum
from Helpers import SMTPMailHelper

class LogType(Enum):
    INFO = 1
    ERROR = 2
    WARNING = 3
    EXCEPTION = 4 

class LogManager(object):

    @staticmethod
    def logMessage(message, logType):
        if(logType==LogType.INFO):
            logging.info(message);
        elif (logType==LogType.WARNING):
            logging.warning(message);
        elif(logType==LogType.ERROR):
            logging.error(message);
            SMTPMailHelper.SMTPClient.sendEmail(message);
        elif(logType==LogType.EXCEPTION):
            logging.exception(message);
        else:
            logging.debug(message);





