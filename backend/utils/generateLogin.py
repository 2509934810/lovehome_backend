import requests
import os

def generateSite(ip):
    KEY = os.getenv("GAODE_KEY")
    url = "https://restapi.amap.com/v3/ip?ip={}&output=json&key={}".format(ip, KEY)
    req = requests.get(url)
    return req.json()
print(generateSite("117.136.91.236"))