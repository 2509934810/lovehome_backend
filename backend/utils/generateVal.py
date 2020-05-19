from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import random
from backend.utils.generatePng import generate as generateURL
def getRandomColor():
    '''获取一个随机颜色(r,g,b)格式的'''
    c1 = random.randint(0,255)
    c2 = random.randint(0,255)
    c3 = random.randint(0,255)
    return (c1,c2,c3)
 
def getRandomStr():
    '''获取一个随机字符串，每个字符的颜色也是随机的'''
    random_num = str(random.randint(0, 9))
    random_low_alpha = chr(random.randint(97, 122))
    random_upper_alpha = chr(random.randint(65, 90))
    random_char = random.choice([random_num, random_low_alpha, random_upper_alpha])
    return random_char

import os, random
def generate():
    image = Image.new('RGB',(150,30),getRandomColor())
    draw = ImageDraw.Draw(image)
    SS = ""
    for i in range(5):
        # 循环5次，获取5个随机字符串
        random_char = getRandomStr()
        SS +=random_char
        # 在图片上一次写入得到的随机字符串,参数是：定位，字符串，颜色，字体
        draw.text((10+i*30, 10),random_char , getRandomColor())
    filepath = "backend/static/img/{}_{}.png".format("tmp", random.randrange(1, 10000))
    basePath = os.path.join(os.path.abspath(os.path.curdir), filepath)
    print(basePath)
    image.save(open(basePath,'wb'),'png')
    PngPath = generateURL(basePath).get("path")
    os.remove(basePath)
    return SS, PngPath
SS, PngPath= generate()
print(SS, PngPath)
