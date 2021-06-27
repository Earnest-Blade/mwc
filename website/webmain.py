import sys, re
sys.path.append("d:\\Projets\\Code\\Python\\WaifuBot\\")

from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from flask_login import current_user
import website.webclass as webclass
from dataBase import waifuData, waifuSerie

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template("baseUI.html",  current_user=current_user,
    title="| Home",
    pagepath="templates/home.html", 
    webclassref=webclass)

@main.route('/list')
def route_list():
    return redirect(url_for("main.list", type='waifu'))

@main.route('/list/<type>', methods=['POST', 'GET'])
def list(type):
    searchingResult = ""
    if request.method == 'POST':
        search = request.form['waifu_name_input']
        request.args = {'search': search}

        searchingResult = search

    if type == 'waifu':
        return render_template("baseUI.html",  current_user=current_user,
            title="| List",
            pagepath="templates/list.html", 
            data=waifuData,
            showingType=str(type),
            searchres=searchingResult)

    elif type == 'anime':
        return render_template("baseUI.html",  current_user=current_user,
            title="| List",
            pagepath="templates/list.html", 
            data=waifuSerie,
            showingType=str(type),
            searchres=searchingResult)

    else: return cantLoadPage()

@main.route('/discord')
def discord():
    return render_template("baseUI.html",  current_user=current_user,
    title="| Discord",
    pagepath="templates/discord.html")


@main.route('/api')
def api():
    return render_template("baseUI.html",  current_user=current_user,
    title="| API",
    pagepath="templates/api.html")

#"""@main.route('/addwaifu')
# def addWaifu():
#
 #   return render_template("baseUI.html",  current_user=current_user,
#    title="| API",
#    pagepath="templates/addWaifu.html")
#
#@main.route('/addwaifu', methods=['POST'])
# def addWaifu_post():
##
#    return render_template("baseUI.html",  current_user=current_user,
#        title="| API",
#        pagepath="templates/addWaifu.html")

@main.route('/forum/post/<postID>')
def post_page(postID):
    if int(postID) <= len(webclass.POSTS) and int(postID) >= 0:
        return render_template("baseUI.html",  current_user=current_user,
        title="| " + webclass.POSTS[int(postID)].title,
        pagepath="templates/postPage.html", 
        postref=webclass.POSTS[int(postID)], 
        text=webclass.POSTS[int(postID)].text)
    else:
        return cantLoadPage()


@main.route('/waifu/<waifu>')
def waifu_page(waifu):
    waifuObject = waifuData.getWaifu(waifu, lowerText=True)
    if not waifuObject == None:
        return render_template("baseUI.html",  current_user=current_user,
        title="| " + waifuObject.getName(),
        pagepath="templates/waifuPage.html", 
        waifuref=waifuObject)
    else:
        return cantLoadPage()

@main.route('/serie/<serie>')
def serie_page(serie):
    serieObject = waifuSerie.getSerie(serie)
    if not serieObject == None:
        return render_template("baseUI.html",  current_user=current_user,
        title="| " + serieObject.getName(),
        pagepath="templates/seriePage.html", 
        serieref=serieObject)
    else:
        return cantLoadPage()


@main.route('/image/<waifu>/<imageID>')
def waifuImage_path(waifu, imageID):
    item = waifuData.getWaifu(waifu, lowerText=True)
    if not item:
        item = waifuSerie.getSerie(waifu)
    
    if not item:
        return cantLoadPage()

    imgID = int(re.findall("\d+", imageID)[0])

    if imgID <= (len(item.images) - 1) and imgID >= 0:
        imageURL = item.images[imgID]
    else:
        return cantLoadPage()
    
    return render_template("baseUI.html",  current_user=current_user,
        title="| " + item.getName(),
        pagepath="templates/waifuImagePage.html", 
        waifuref=item, 
        imageURL=imageURL)


def cantLoadPage():
    return render_template("baseUI.html",  current_user=current_user,
        title="| Not Found !",
        pagepath="templates/notfound.html")