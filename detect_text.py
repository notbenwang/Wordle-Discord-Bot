import numpy as np
import detect_score
from urllib.request import Request, urlopen
import cv2
from glob import glob
from PIL import Image

import pytesseract

def get_black_white_shape(img):
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(gray_image, 255, 255, cv2.THRESH_BINARY)
    img = cv2.bitwise_not(img)
    return img

if __name__ == "__main__":
    url = "https://cdn.discordapp.com/attachments/801334593340047370/1194452054622601256/image.png?ex=65b06729&is=659df229&hm=bb833883c18ebc7c95df46269119fa3dda74ed04c41dc174f8a48e6160d75015&"
    req = urlopen(Request(url, headers={'User-Agent':'Modzilla/5.0'}))
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    img = cv2.imdecode(arr, -1)
    # img = detect_score.get_black_white_shape(tmp)
    print(pytesseract.image_to_string(img, lang='eng'))
    cv2.imshow("test", img)
    cv2.waitKey(0)
    