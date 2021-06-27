from dataBase import waifuDataOutput, waifuData

import discord
from discord import Guild

import xml.etree.ElementTree as et
import xml.etree

# Classe principale d'un utilisateur 
class waifuUser:

    # Chemin vers la base de donnée
    XMLPATH = "dataBase/userData.xml"

    WAIFU_PRICE = 100
    MASTER_PRICE = 200
    REMOVE_PRICE = 100

    PLAY_GAIN = 50
    PLAY_TIME = 900

    # Constructeur, prend en entrée un object "Discord.User"
    def __init__(self, user):
        self.user = user
        self.harem = []
        self.masterWaifu = None
        self.haremPoint = 100

        self.id = self.user.id
    
    # Permet de sauvegarder ou de créer d'utilisateur dans la base de donnée
    # Peut prendre en entrée le paramètre "new" qui définit si c'est nouveau ou pas
    def writeToXML(self, new=False):
        tree = et.parse(waifuUser.XMLPATH)
        root = tree.getroot()

        if not new:
            for user in root:
                if user[0].text == str(self.user.id):
                    for waifu in user[1]:
                        user.remove(waifu)
                    
                    user[1].text = ""
                    for waifu in self.harem:
                        if user[1].text == "":
                            user[1].text = waifu.name
                        else:
                            user[1].text = user[1].text  + "," + waifu.name 
                     
                    user[2].text = self.masterWaifu.name
                    user[3].text = str(self.haremPoint)
                    tree.write(waifuUser.XMLPATH)
                    return
            
            new = True

        if new:
            user = root.makeelement("user", {})
            root.append(user)

            ID = user.makeelement("id", {})
            ID.text = str(self.user.id)
            

            harem = user.makeelement("harem", {})
            for waifu in self.harem:
                if not harem.text == "":
                    harem.text = harem.text + "," + waifu.name 
                else:
                    harem.text = waifu.name
            
            masterWaifu = user.makeelement("masterWaifu", {})
            masterWaifu.text = "-"
            if not self.masterWaifu == None:
                masterWaifu.text = self.masterWaifu.name
            
            haremPoint = user.makeelement("haremPoints", {})
            haremPoint.text = str(self.haremPoint)
            

            user.append(ID)
            user.append(harem)
            user.append(masterWaifu)
            user.append(haremPoint)
        
            tree.write(waifuUser.XMLPATH)
    
    def removeWaifuFromHarem(self, waifu=None, name=""):
        if not name == "":
            tree = et.parse(waifuUser.XMLPATH)
            root = tree.getroot()

            if not name == "None":
                waifu = waifuData.getWaifu
            else:
                for user in root:
                    if user[0].text == str(self.user.id):
                        user[1].text = user[1].text.replace(name, "")

            tree.write(waifuUser.XMLPATH)

        if not waifu == None:
            for hwaifu in self.harem:
                if hwaifu.name == waifu.name:
                    self.harem.remove(hwaifu)
        
            self.writeToXML()
        
        
    
    # Permet d'ajouter une waifu au harem de l'utilisateur
    # Prend en entrée un object "WaifuData"
    def addToHarem(self, waifu):
        tree = et.parse(waifuUser.XMLPATH)
        root = tree.getroot()

        for user in root:
            if user[0].text == str(self.user.id):
                user[1].text = str(user[1].text) + "," + waifu.name
        
        self.harem.append(waifu)
        tree.write(waifuUser.XMLPATH)
    
    # Permet de trouver une waifu dans le harem grâce à son nom
    # Prend en entrée un nom et retourne un object "WaifuData"
    def getWaifu(self, name):
        for waifu in self.harem:
            if waifu.name == name:
                return waifuData.getWaifu(name)
    
    # Permet de vérifier si une waifu est dans le harem de l'utilisateur 
    # Prend en entrée un nom et retourne une valeure booléenne
    def waifuInHarem(self, name):
        result = False
        if not len(self.harem) == 0:
            for waifu in self.harem:
                if not waifu == None:
                    if waifu.name == name:
                        result = True
        
        return result

    def waifuIsMasterWaifu(self, waifu):
        result = False
    
        if not self.masterWaifu == None and waifu.name == self.masterWaifu.name:
            result = True
    
        return result


# Permet de vérifier si un utilisateur existe 
# Prend en entrée un object "WaifuUser" et 
# retourne une valeure booléenne
def userExist(userInput):
    tree = et.parse(waifuUser.XMLPATH)
    root = tree.getroot()

    userExist = False

    for user in root:
        if user[0].text == str(userInput.id):
            userExist = True
    
    return userExist

# Permet de récupérer un utilisateur de la banque de donnée 
# Retourne 
def getUser(userInput):
    tree = et.parse(waifuUser.XMLPATH)
    root = tree.getroot()

    userObject = None

    for user in root:
        if user[0].text == str(userInput.id):
            harem = []
            
            if not (user[1].text == None or user[1].text == ""):
                for waifu in user[1].text.split(','):
                    harem.append(waifuData.getWaifu(waifu))

            userObject = waifuUser(userInput)
            userObject.harem = harem
            userObject.masterWaifu = waifuData.getWaifu(user[2].text)
            userObject.haremPoint = int(user[3].text)

    if userObject == None:
        waifuDataOutput.printError(waifuDataOutput.WaifuDataErrorPosition(6, 81, __file__))

    
    return userObject

# Permet de vérifier la waifu entrée est la maître du harem
# Prend en entrée un object "waifuData" et un object "waifuUser" et retourne un booléen
def waifuIsMasterWaifu(waifu, user):
    result = False
    
    if not user.masterWaifu == None and waifu.name == user.masterWaifu.name:
        result = True
    
    return result


def userWithDiscordUser(user):
    if userExist(user) : waifu_user = getUser(user)
    else : 
        waifu_user = waifuUser(user)
        waifu_user.writeToXML()
    
    waifu_user.removeWaifuFromHarem(None)
    return waifu_user

def canBuyWaifu(user, price):
    if user.haremPoint >= price:
        return True

    return False

def getUserByQuery(id):
    from website.webapp import User, db
    user = User.query.filter_by(id=id).first()
    if user:
        return getUser(user)
    else:
        return None

