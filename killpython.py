import os
# import shutil
# os.system("taskkill -f -im python.exe")

def findFiles(dirs):
    for dir in os.listdir(dirs):
        fullDir = dirs + '\\' + dir
        if os.path.isdir(fullDir):
            findFiles(fullDir)
        else:
            for line in open(fullDir, 'r'):
                if line.find('application.controller.grant ') != -1:
                    print fullDir
                    
                    
findFiles(r'G:\WorkSpace\kmvip3\client')