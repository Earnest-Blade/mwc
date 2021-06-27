from dataBase import waifuData, waifuDataOutput, waifuDataUtils

import xml.etree.ElementTree as et
import xml.etree
import random

# Cet objet correspond à la serie à laquel appartient un personnage
class waifuSerie:

    SERIES = []

    XMLPATH = "dataBase/animeData.xml"

    # le constructeur peut prendre en entrée de nom de la série
    def __init__(self, name="", setInList=True):
        self.name = name
        self.charctersIn = []

        self.images = []
        self.tags = []
        self.support = []

        self.description = ""
        self.information = ""
        self.node = None

        if setInList:
            self.setInList()
    
    # Permet d'ajouter à la list des personnages de la série toutes les waifu présentent dans le fichier XML
    # Retourne rien
    def attachWaifuToSerie(self):
        if self.name != "":
            for waifu in waifuData.getAllWaifus(False):
                if waifu.serie == self.name:
                    self.charctersIn.append(waifu)
        else: 
            waifuDataOutput.printError(waifuDataOutput.WaifuDataErrorPosition(3, 17, __file__), self)
            return

        if len(self.charctersIn) == 0: 
            waifuDataOutput.printDebugInfo("no character found for " + self.name + " !")

    # Fonction appelée à la fin du constructeur, il enregistre le personnage dans la list, ou l'actualise
    def setInList(self):
        if self in waifuSerie.SERIES:
            for index, serie in enumerate(waifuSerie.SERIES):
                if serie == self:
                    waifuSerie.SERIES[index] = self
        
        else:
            waifuSerie.SERIES.append(self)
    
    def openWithXml(self, name=""):
        if name == "":
            if self.name != "":
                tree = et.parse(waifuSerie.XMLPATH)
                root = tree.getroot()

                for serie in root:
                    if serie[0].text == self.name:
                        self.description = serie[1].text

                        for image in serie[2]:
                            self.images.append(image.text)
                        
                        for tag in serie[3].text.split(','):
                            self.tags.append(tag)
                        
                        for support in serie[5]:
                            self.support.append(otherSupport(support.tag, support[0].text))

                        self.node = serie
                        self.information = serie[4].text

            else:
                return
    def tagsToString(self):
        result = ""
        for tag in self.tags:
            if result == "":
                result = tag.capitalize()
            else: result = result + ", " + tag.capitalize()
        
        return result
    
    def getRandomImage(self):
        image = random.choice(self.images)
        return image
    
    def getAllCharactersIn(self, lowerName=False):
        result = ""
        for char in self.charctersIn:
            if result == "":
                result = char.name
                if lowerName:
                    result = char.getName()
            else: result = result + ", " + char.name
        
        return result

    def getName(self):
        name = self.name
        name = name.replace('_', ' ')
        name = name.title()
        return name

    def __str__(self):
        return "SerieClass"

# Object des autres supports que l'anime 
class otherSupport:

    SUPPORT_MANGA = (0, "Manga")
    SUPPORT_LN = (1, "Light Novel")
    SUPPORT_VS = (2, "Visual Novel")

    def __init__(self, type, information):
        self.type = self.getType(type)
        self.information = information
    
    def getType(self, type):
        if type == "manga":
            return otherSupport.SUPPORT_MANGA
        elif type == "lightNovel":
            return otherSupport.SUPPORT_LN
        elif type == "visualNovel":
            return otherSupport.SUPPORT_VS

# Permet de trouver la serie à laquelle une waifu appartient et en crée un object "WaifuSerie"
# Retourne un object "WaifuSerie" et prend en entrée un nom ou un object "WaifuData"
def createSerieWithWaifu(name="", waifu=None):
        if(name == "" and waifu == None): return
        if name != "":
            waifu = waifuData.getWaifu(name)
        
        serie = waifuSerie(waifu.serie, False)
        serie.attachWaifuToSerie()

        return serie

# Permet de trouver la serie à laquelle une waifu appartient dans la liste sans ajouter de serie à la liste.
# Retourne un object "WaifuSerie" et prend en entrée un nom ou un object "WaifuData"
def getWaifuSerie(name="", waifu=None, output=True):
    if(name == "" and waifu == None): return
    if name != "":
        waifu = waifuData.getWaifu(name)
    
    if len(waifuSerie.SERIES) == 0:
        if output: waifuDataOutput.printError(waifuDataOutput.WaifuDataErrorPosition(5, 58, __file__))
        return None

    for serie in waifuSerie.SERIES:
        if(serie.name == waifu.serie):
            return serie
    
    if output: waifuDataOutput.printDebugInfo("Can't find a serie for " + waifu.name + "!")
    return None

def getSerie(name):
    if name == "" or len(waifuSerie.SERIES) == 0: return
    for serie in waifuSerie.SERIES:
        if serie.name == name:
            return serie

def getAllSeries():
    return waifuSerie.SERIES

# Permet de créer toutes les series de toutes les waifus enregistrée dans le fichier XML
# Ne retourne rien
def createAllSeriesFromXMLFile():
    for waifu in waifuData.getAllWaifus(False):
        if getWaifuSerie(waifu=waifu, output=False) == None:
            serie = waifuSerie(waifu.serie)
            serie.attachWaifuToSerie()
            
            serie.openWithXml()
