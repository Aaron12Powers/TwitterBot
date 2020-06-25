import random
import numpy as np
import math
from PIL import Image
import requests
from io import BytesIO

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id


def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return


def test_function():
    print('Module File: TEST TEST TEST')



class CircleClass:
    def _init_(self, location_x, location_y):
        self.locationX = location_x
        self.locationY = location_y
        self.size = 0

    def set_size(self, size):
        self.size = size

    def max_size(self, max_size):
        self.max_Size = max_size

    def closest(self, closest):
        self.closest = closest

    def new_circle(self, size, color, location, count):
        self.size = size
        self.color = color
        self.location = location
        self.count = count


def circles(api, mention, file_name):
    print('Circles Function Called')



    try:
        response = requests.get(file_name)
        im = Image.open(BytesIO(response.content))
    except IOError:
        print('FAIL')
        return 'FAILED'
        pass
    value = (190, 130, 0)

    width, height = im.size

    print(width)
    print(height)

    background_rgb = (0, 0, 0)
    background_rgba = (0, 0, 0, 0)

    circles = im

    for x in range(0, width):
        for y in range(0, height):
            pix = circles.load()
            pix[x, y] = background_rgba

    try:
        original = Image.open(BytesIO(response.content))
    except IOError:
        print('FAIL')
        return 'FAILED'
        pass

    max_size = int(math.sqrt(height * width) / 90)
    min_size = 1
    num_circles = height * 10

    circle_object = [CircleClass] * num_circles

    for i in range(0, num_circles):
        circle_object[i] = CircleClass()
        pix = circles.load()
        rand_width = random.randrange(0, width, 1)
        rand_height = random.randrange(0, height, 1)

        circle_object[i]._init_(rand_width, rand_height)

        if pix[rand_width, rand_height] != background_rgb and background_rgba:
            continue

        if i > 0:
            closest_point = max_size
            for j in range(0, i - 1):

                if circle_object[j].locationX > circle_object[i].locationX:
                    temp_size_x = int(circle_object[j].locationX - circle_object[i].locationX)
                else:
                    temp_size_x = int(circle_object[i].locationX - circle_object[j].locationX)

                if circle_object[j].locationY > circle_object[i].locationY:
                    temp_size_y = int(circle_object[j].locationY - circle_object[i].locationY)

                else:
                    temp_size_y = int(circle_object[i].locationY - circle_object[j].locationY)

                temp_size = int(math.sqrt(pow(temp_size_x, 2) + pow(temp_size_y, 2)))

                temp_size = temp_size - circle_object[j].size

                if closest_point > temp_size:
                    closest_point = temp_size
                if closest_point > max_size:
                    closest_point = max_size - random.randrange(0, 3)
                if closest_point < min_size:
                    closest_point = min_size + random.randrange(0, 2)

        else:
            closest_point = random.randrange(0, max_size)

        circle_object[i].set_size(closest_point)

        temp = original.load()

        for x in range(-circle_object[i].size, circle_object[i].size):
            for y in range(-circle_object[i].size, circle_object[i].size):
                check = pow(x, 2) + pow(y, 2)
                if int(math.sqrt(check)) <= circle_object[i].size - 1:
                    try:
                        pix[circle_object[i].locationX + x, circle_object[i].locationY + y] = temp[rand_width, rand_height]
                    except:
                        continue
                else:
                    continue

    circles.save('temp_new.png')

    api.update_with_media('temp_new.png', '@' + str(mention.user.screen_name) + " Here you go! - circles - via @AaronPDev", mention.id)

    circles.show()

    im.close()


def compress(api, mention, file_name, extent):
    print('Compress Function Called')

    try:
        response = requests.get(file_name)
        im = Image.open(BytesIO(response.content))
    except IOError:
        return 'FAILED'
        pass

    width, height = im.size

    new_height = height // extent
    new_width = width // extent

    compressed = Image.new(mode="RGB", size=(new_width, new_height))

    for x in range(0, new_width):
        for y in range(0, new_height):
            pix = compressed.load()
            pixim = im.load()
            try:
                pix[x, y] = pixim[x*extent, y*extent]
            except:
                continue

    compressed.save('temp_new.png')

    api.update_with_media('temp_new.png', '@' + str(mention.user.screen_name) + " Here you go! - compressed - via @AaronPDev", mention.id)

    compressed.show()

    im.close()


def maze(api, mention):
    print('maze function called')
    width = 500
    height = 250
    maze_image = Image.new(mode="RGB", size=(width, height), color=(256, 256, 256))
    maze_image.save('temp_new.png')

    pix = maze_image.load()

    for x in range(0, width):
        for y in range(0, height):
            if x < 3 or y < 3 or x > 496 or y > 246:
                pix[x, y] = (250, 100, 25)
            if (x % 25 <= 1 or x % 25 == 24) and (y % 25 <= 1 or y % 25 == 24):
                pix[x, y] = (250, 100, 25)

    api.update_with_media('temp_new.png', '@' + str(mention.user.screen_name) + " Here you go! - maze - via @AaronPDev", mention.id)
    maze_image.show()
