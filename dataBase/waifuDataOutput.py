import inspect, os

# waifuDataError.printError(waifuDataError.WaifuDataErrorPosition(0, 1, __file__))

printType = 1

class WaifuDataDebug:

    WAIFU_ERROR = [
        "You most enter an correct object to add in list! Maybe the object, birthday or serie variables are not defined!",
        "The waifu that you want to add is allready in the database!",
        "The waifu \"$\" cannot be added because errors block this function!",
        "You most set a name to the serie ($) before use the attachWaifuToSerie function!",
        "You most find the waifu in data before read Xml File!",
        "The Serie list is not create. So You can't find series from the list!",
        "The user object that you want to create can't be find or create with the xml file!"
    ]

    WAIFU_OUTPUT_NOTHING = 0
    WAIFU_OUTPUT_ONLY_ERROR = 1
    WAIFU_OUTPUT_ONLY_DEBUG = 2
    WAIFU_OUTPUT_ALL = 3


class WaifuDataErrorPosition:

    def __init__(self, errorType, line=0, classCaller=None):
        self.errorType = errorType
        self.line = line
        self.classCaller = classCaller

def setOutputType(outputType):
    printType = outputType

def printError(error, *args):
    if printType == 1 or printType == 3:
        errorReference = WaifuDataDebug.WAIFU_ERROR[error.errorType]
        if '$' in errorReference:
            errorText = WaifuDataDebug.WAIFU_ERROR[error.errorType].split('$')[0] + str(args[0]) + WaifuDataDebug.WAIFU_ERROR[error.errorType].split('$')[1]
        else:
            errorText = errorReference

        print('\033[31m' + "Error: at line " + str(error.line) + " in " + os.path.basename(error.classCaller) + " : " + errorText  + '\033[0m')

def printDebugInfo(info, *args):
    if printType == 2 or printType == 3:
        if args != (): 
            color = args[0]
        else : color = ""
        print(color + "Info : " + info)
    