import requests
import os
def generate(pngPath):
    session = requests.session()
    url = "http://{}/api/avator/add".format(os.getenv("AVATOR_SERVER"))
    file = {"file": ('index.jpeg', open('{}'.format(pngPath),'rb'), 'image/png', {})}
    rsp = session.post(url=url, data={"userId":'1614010432'}, files=file)
    return rsp.json()

if __name__ == '__main__':
    rsp = generate("/home/lei/workspace/python/毕设/lovehome_backend/backend/static/img/1614010411-76357.jpg")
    print(rsp)