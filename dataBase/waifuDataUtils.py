import dataBase.waifuData as wd
import dataBase.waifuDataOutput as waifuDataOutput

SORT_BY_NAME = 1
SORT_BY_SERIE = 2

# Vérifie si le nom entré est déjà enregistré dans la banque de donnée 
# Retourne une valeure boolénnne
def waifuExist(name, lowerText=False):
    count = 0
    xmlFile = open(wd.WaifuData.XMLPATH, 'r')

    if lowerText:
        name = name.capitalize()

    for l in xmlFile.readlines():
        if ("name" in l) and (name in l) :
            count += 1
    
    if count == 1 : 
        return True
    else : 
        return False

# Vérifie si l'objet "WaifuData" est correct
# Retourne une valeur booléenne
def isCorrectWaifu(object):
    if object != None and object.birthday != "" and object.serie != "":
        if(not waifuExist(object.name)):
            return True
        else:
            waifuDataOutput.printError(waifuDataOutput.WaifuDataErrorPosition(1, 31, __file__))
        
    else:
        waifuDataOutput.printError(waifuDataOutput.WaifuDataErrorPosition(0, 34, __file__))
        return False

# Permet de trier toutes les waifus du fichier XML selon une ordre donnée 
# Il prend en entrée un type de triage et sort un dictionnaire avec comme valeure un object "WaifuData" 
# et comme key une chaîne de character 
def sortWaifu(sortType):
    allWaifu = wd.getAllWaifus();

    if sortType == SORT_BY_NAME:
        result = sorted(allWaifu, key=lambda e:e.name)
    elif sortType == SORT_BY_SERIE:
        result = sorted(allWaifu, key=lambda e:e.serie)

    return result

def capitalizeAllString(string):
    result = ""
    for word in string:
        result = result + " " + word.capitalize()
    
    return result

def showableString(string):
    if "_" in string:
        string = string.replace('_', ' ')
    result = ""

    if " " in string:
        for word in string.split(' '):
            result = result + " " + word.capitalize()
            
    else: result = string
    
    return result



