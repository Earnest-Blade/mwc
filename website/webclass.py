import xml.etree.ElementTree as et
import xml.etree




############# POSTS

POSTS = []
class Post():

    PATH = "website/posts.xml"

    def __init__(self):
        self.title = ""
        self.text = ""
        self.date = ""
        self.tags = []
        self.image = ""
    
    def load(self, index):
        tree = et.parse(self.PATH)
        root = tree.getroot() 

        self.title = root[index].attrib["title"]
        self.image = root[index].attrib["image"]
        self.date = root[index].attrib["date"]
        self.text = root[index][0].text

        self.tags = root[index][1].text

def loadAllPosts():
    tree = et.parse(Post.PATH)
    root = tree.getroot() 

    for i in range(0, len(root)):
        postTemp = Post()
        postTemp.load(i)
        POSTS.append(postTemp)
    


