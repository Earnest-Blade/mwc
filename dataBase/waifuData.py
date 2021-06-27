import dataBase.waifuDataUtils as waifuDataUtils
import dataBase.waifuDataOutput as waifuDataOutput
import dataBase.waifuSerie as waifuSerie

import xml.etree.ElementTree as et
import xml.etree
import random

class WaifuData:

    # Chemin d'accès vers le fichier contenant les waifus
    XMLPATH = "dataBase/waifuData.xml"

    # Constructeur, prend en compte le nom et initialise les variables
    def __init__(self, name, birthday="", images=[], serie="", description="", tags=[], submit="Admin"):
        self.name = name
        self.birthday = birthday
        self.serie = serie
        self.images = images
        self.description = description
        self.tags = tags
        self.node = None

        self.submit = submit
    

########### MODE LECTURE 

    # execute les fonction qui permettent de charger les données de la Waifu
    def load(self):
        self.findWaifuInXmlData()
        self.readXmlFile()
    
    # permet de trouver la waifu dans le fichier XML 
    # assigne à la variable "node" l'object XML de la waifu
    def findWaifuInXmlData(self):
        tree = et.parse(WaifuData.XMLPATH)
        root = tree.getroot() 

        for waifu in root:
            if waifu[0].text == self.name:
                self.node = waifu

    # Assigne les variables à leurs valeurs du fichier XML
    def readXmlFile(self):
        if self.node != None:
            self.birthday = self.node[1].text
            self.serie = self.node[3].text
            self.description = self.node[4].text
            self.submit = self.node[6].text

            for image in self.node[2]:
                if not image in self.images:
                    self.images.append(image.text)

            for tag in self.node[5].text.split(','):
                self.tags.append(tag) 
            
        else:
            waifuDataOutput.printError(waifuDataOutput.WaifuDataErrorPosition(4, 59, __file__))
    
########### MODIFICATION DE PARAMETRE

    def setName(self, name):
        tree = et.parse(WaifuData.XMLPATH)
        root = tree.getroot()

        for waifu in root:
            if waifu[0].text == self.name:
                waifu[0].text = name

        self.name = name
        tree.write(WaifuData.XMLPATH)
    
    def setBirthday(self, birthday):
        tree = et.parse(WaifuData.XMLPATH)
        root = tree.getroot()

        for waifu in root:
            if waifu[0].text == self.name:
                waifu[1].text = birthday

        self.birthday = birthday
        tree.write(WaifuData.XMLPATH)
    
    def setDescription(self, description):
        tree = et.parse(WaifuData.XMLPATH)
        root = tree.getroot()

        for waifu in root:
            if waifu[0].text == self.name:
                waifu[4].text = description

        self.description = description
        tree.write(WaifuData.XMLPATH)
    
    def setSubmitter(self, submit):
        tree = et.parse(WaifuData.XMLPATH)
        root = tree.getroot()

        for waifu in root:
            if waifu[0].text == self.name:
                waifu[6].text = submit

        self.submit = submit
        tree.write(WaifuData.XMLPATH)
    
    def addTag(self, tag):
        tree = et.parse(WaifuData.XMLPATH)
        root = tree.getroot()

        for waifu in root:
            if waifu[0].text == self.name:
                waifu[5].text = waifu[5].text + "," + tag

        self.tags.append(tag)
        tree.write(WaifuData.XMLPATH)
    
    def addImage(self, image):
        tree = et.parse(WaifuData.XMLPATH)
        root = tree.getroot()

        for waifu in root:
            if waifu[0].text == self.name:
                imageNode = waifu[2].makeelement("image", {})
                imageNode.text = image
                waifu[2].append(imageNode)

        self.images.append(image)
        tree.write(WaifuData.XMLPATH)
    
    # Permet de transformer les tags de la waifu en chaîne de character
    # Retourne une chaîne de character
    def tagsToString(self):
        result = ""
        for tag in self.tags:
            if result == "":
                result = tag.capitalize()
            else: result = result + ", " + tag.capitalize()
        
        return result
    
    # Permet d'avoir une image aléatoire de la waifu
    # Retourne un lien vers l'image
    def getRandomImage(self):
        image = random.choice(self.images)
        return image
    
    def getLowerName(self):
        return self.name.lower()
    
    def getBirthday(self):
        return self.birthday.replace(',', '/')
    
    def getName(self):
        name = self.name
        name = name.replace('_', ' ')
        name = name.title()
        return name
    
    def getSerie(self):
        serie = self.serie
        serie = serie.replace('_', ' ')
        serie = serie.title()
        return serie
    
    def getSerieObject(self):
        return waifuSerie.getWaifuSerie(self.name)


########### MODE ECRITURE

# Permet d'ajouter une nouvelle waifu dans le fichier XML
# Prend comme entrée un object de type "WaifuData"
def addWaifuToXML(object):
    if waifuDataUtils.isCorrectWaifu(object):
        tree = et.parse(WaifuData.XMLPATH)
        root = tree.getroot()

        waifu = root.makeelement("waifu", {})
        root.append(waifu)

        name = waifu.makeelement("name", {})
        name.text = object.name

        birthday = waifu.makeelement("birthday", {})
        birthday.text = object.birthday

        serie = waifu.makeelement("serie", {})
        serie.text = object.serie

        description = waifu.makeelement("description", {})
        description.text = object.description

        submit = waifu.makeelement("submit", {})
        submit.text = object.submit

        tags = waifu.makeelement("tags", {})
        for tag in object.tags:
            if tags.text != None:
                tags.text = tags.text + "," + tag
            else:
                tags.text = tag

        images = waifu.makeelement("images", {})
        for image in object.images:
            imageNode = images.makeelement("image", {})
            imageNode.text = image

            images.append(imageNode)


        waifu.append(name)
        waifu.append(birthday)
        waifu.append(images)
        waifu.append(serie)
        waifu.append(description)
        waifu.append(tags)
        waifu.append(submit)

        tree.write(WaifuData.XMLPATH)

        waifuDataOutput.printDebugInfo(object.name + " is succedfully added to the list!")

    else:
        waifuDataOutput.printError(waifuDataOutput.WaifuDataErrorPosition(2, 185, __file__), object.name)

# Permet de réécrir tout un fichier Xml 
# Prend en entrée une list de waifu
def setXml(waifuList):
    for w in getAllWaifus():
        pass
        removeWaifu(w)

    for w in waifuList:
        addWaifuToXML(w)
    
# Permet de supprimer une waifu du fichier XML
# Ne retourne rien, n'a pas de sécurité 
def removeWaifu(object):
    tree = et.parse(WaifuData.XMLPATH)
    root = tree.getroot()

    for w in root:
        if w[0].text == object.name:
            root.remove(w)
    
    waifuDataOutput.printDebugInfo(object.name + " is succefully removed from the list!")

    tree.write(WaifuData.XMLPATH)

########### Fonction d'aide

# Permet de trouver une waifu dans le fichier XML avec un string
# retourne un objet "WaifuData"
def getWaifu(name, output=True, lowerText=False):
    tree = et.parse(WaifuData.XMLPATH)
    root = tree.getroot()

    wd = None

    for waifu in root:
        if lowerText:
            if waifu[0].text.lower() == name:
                wd = WaifuData(name.capitalize(), "", [], "", "", [], "")
                wd.load()
        else:
            if waifu[0].text == name:
                wd = WaifuData(name, "", [], "", "", [], "")
                wd.load()
    
    if(output): waifuDataOutput.printDebugInfo(name + " is been found!")

    return wd

# Permet d'avoir toutes les waifus du fichier data 
# retourne une liste d'object "WaifuData"
def getAllWaifus(output=True):
    waifusList = []

    tree = et.parse(WaifuData.XMLPATH)
    root = tree.getroot()

    for waifu in root:
        waifusList.append(getWaifu(waifu[0].text, output))
    
    return waifusList

# Permet d'avoir une waifu aléatoire
# retourne un objet "WaifuData" et prend en entrée une list
def getRandomWaifu(waifuList=getAllWaifus(False)):
    return random.choice(waifuList)