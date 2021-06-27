import website.webauth as webauth
import requests

from flask_discord import configs

def getToken(code: str, uri):
    data = {
    'client_id': webauth.CLIENT_ID,
    'client_secret': webauth.CLIENT_SECRET,
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': uri
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    resp = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
    resp.raise_for_status()
    return resp.json()['access_token']

def getUserInfo(token, url):
    resp = requests.get("https://discord.com/api/" + url, headers={'Authorization': f'Bearer {token}'})
    resp.raise_for_status()
    return resp.json()

def avatar_url(avatar_hash, id, is_avatar_animated=False):
    if not avatar_hash: return
    
    image_format = configs.DISCORD_ANIMATED_IMAGE_FORMAT \
        if is_avatar_animated else configs.DISCORD_IMAGE_FORMAT

    return configs.DISCORD_USER_AVATAR_BASE_URL.format(
        user_id=id, avatar_hash=avatar_hash, format=image_format)