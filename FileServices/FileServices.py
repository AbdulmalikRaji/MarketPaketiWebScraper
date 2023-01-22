import os
import glob
import shutil
import pandas as pd
import xlsxwriter
from Logger import LogManager as LM
from Props import StaticProps as Props
class FileServices(object):

    @staticmethod
    def CreateOrCheckAppDirectories():
            isUploadingAvailable = FileServices.CheckDirectory(Props.FilePathProps.processBasePath)
            isOnProcessAvailable = FileServices.CheckDirectory(Props.FilePathProps.uploadBasePath)

            if(isUploadingAvailable==False or isOnProcessAvailable == False):
                return False;
            else:
                return True;

    @staticmethod
    def CheckDirectory(directoryPath):
        try:
            if not os.path.exists(directoryPath):
                os.mkdir(directoryPath)
                LM.LogManager.logMessage("Directory " + directoryPath  +  " Created ", LM.LogType.INFO);
            else:
                LM.LogManager.logMessage("Directory " + directoryPath + " already exists", LM.LogType.INFO);
            return True;

        except Exception as e:
            LM.LogManager.logMessage("FileServices- Error Occured While Checking Directory:" + directoryPath, LM.LogType.ERROR);
            return False;

    @staticmethod
    def MoveUploadingDirectory():
        file_source = Props.FilePathProps.uploadBasePath;
        file_destination = Props.FilePathProps.uploadingDestinationPath;
        get_files = os.listdir(file_source)
        for g in get_files:
            os.replace(file_source + "\\" +  g, file_destination + "\\" + g)

    def CopyFile(srcFilePath, destFilePath):
        try:
            shutil.copy(srcFilePath,destFilePath)
            return True;
        except Exception as e:
            LM.LogManager.logMessage("FileServices- CopyFile -- SRC:" + srcFilePath + " - DEST: " + destFilePath, LM.LogType.ERROR);
            return False;

    @staticmethod
    def DeleteOnProcessFiles():
        files = glob.glob(Props.FilePathProps.processBasePath + '/*')
        for f in files:
            os.remove(f)

    @staticmethod
    def CreateEmptyExcelFile(fileName):
        try:
            workbook = xlsxwriter.Workbook(fileName)
            worksheet = workbook.add_worksheet()
            workbook.close()
            return True;
        except Exception as e:
            return False;



