from urllib.request import Request, urlopen
import cv2
import numpy as np


def get_black_white_shape(img):
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(gray_image, 30, 255, cv2.THRESH_BINARY)
    img = cv2.bitwise_not(img)
    return img


def get_color(img, color):
    if color == 'green':
        lower = np.array([25,25,25])  # 25 110 140 and 75 255 255
        upper = np.array([75,255,255]) # 25 25 25 and 75 255 255  <---Current Iteration
    elif color == 'yellow':
        lower = np.array([25,160,50])  # 25 160 160 and 95 255 255
        upper = np.array([120,255,255])  # 25 160 50 and 120 255 255 <---Current Iteration
    else:
        return
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    color_image = cv2.bitwise_and(img, img, mask=mask)
    return color_image


def identify_shapes(img, normal=False):
    if normal:
        thresh = get_black_white_shape(img)
    else:
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray_image, 0, 255, 0)

    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    error = 30
    coords = {}
    size = 0
    for i, c in enumerate(contours):
        if i == 0 and normal:
            continue
        epsilon = 0.01 * cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)
        x,y,w,h = cv2.boundingRect(approx)
        in_dict = False
        c_x = int(x + w / 2)
        c_y = int(y + h / 2)
        for coord in coords:
            it_x,it_y = coord
            if it_x + -1*error <= x <= it_x + error and it_y + -1*error <= y <= it_y + error:
                in_dict = True
                break
        if not in_dict and w > error:
            coords[(x,y)] = (w,h)
            cv2.circle(img, (c_x, c_y), radius=int(w / 2), color=(0, 0, 255), thickness=2)
        size += 1

    return coords


def coord_in_set_of_boxes(coord, boxes):
    x,y = coord
    for box in boxes:
        it_x, it_y = box
        w,h = boxes[box]
        if it_x - int(w/2) <= x <= it_x + int(w/2) and it_y - int(h/2) <= y <= it_y + int(h/2):
            return True
    return False


def print_matrix(matrix):
    for i in range(6):
        for j in range(5):
            print(matrix[i][j], end=' ')
        print()
    print()


def array_to_2d_matrix(array):
    matrix = [[0]*5 for i in range(6)]
    if len(array) != 30:
        return -1
    else:
        i = 0
        j = 0
        k = 0
        while i < 30:
            matrix[j][k] = array[i]
            i += 1
            k += 1
            if k % 5 == 0:
                k = 0
                j += 1
        return matrix


def get_wordle_score(array):
    score = 0
    for row in array:
        score += 1
        greens = 0
        for letter in row:
            if letter == "G":
                greens += 1
            if greens >= 5:
                return score
    return "0"

def score_from_image(img):
    normal = img
    yellow = get_color(img, "yellow")
    green = get_color(img, "green")

    normal_boxes = identify_shapes(normal, normal=True)
    yellow_boxes = identify_shapes(yellow)
    green_boxes = identify_shapes(green)
    wordle = [0] * 30

    for i, coord in enumerate(normal_boxes):
        x, y = coord
        w, h = normal_boxes[coord]
        if coord_in_set_of_boxes(coord, yellow_boxes):
            color = "Y"
        elif coord_in_set_of_boxes(coord, green_boxes):
            color = "G"
        else:
            color = 'X'
        wordle[29 - i] = color

    matrix = array_to_2d_matrix(wordle)
    return get_wordle_score(matrix), normal

if __name__ == "__main__":
    url = "https://cdn.discordapp.com/attachments/801334593340047370/1194452054622601256/image.png?ex=65b06729&is=659df229&hm=bb833883c18ebc7c95df46269119fa3dda74ed04c41dc174f8a48e6160d75015&"
    req = urlopen(Request(url, headers={'User-Agent':'Modzilla/5.0'}))
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    img = cv2.imdecode(arr, -1)

    score,_ = score_from_image(img)
    print("Score:",score)
    cv2.imshow("test", img)
    cv2.waitKey(0)

# url = # some link
# req = urlopen(Request(url, headers={'User-Agent':'Modzilla/5.0'}))
# arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
# img = cv2.imdecode(arr, -1)

# score,_ = score_from_image(img)
# print("Score:",score)
# cv2.imshow("test", img)
# cv2.waitKey(0)