import sys
sys.path.insert(0, '/opt/')

from main import app as application
#from main import debugLog

if __name__ == '__main__':
    #debugLog("run1")
    application.run(port=1111)
    #debugLog("run2")
