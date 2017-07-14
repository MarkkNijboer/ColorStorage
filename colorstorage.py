from PIL import Image
import numpy as np
import math

class ColorStorage():
    image = []
    pixel = []

    def __init__(self):
        pass

    def add_pixel(self):
        """
        Adds the buffered pixel as an array to the image list
        """
        self.image.append([self.pixel[0], self.pixel[1], self.pixel[2]])
        self.pixel = []

    def add_byte(self, byte):
        """
        Adds the byte to the R,G or B value of the buffered pixel
        """
        self.pixel.append(byte)
        if len(self.pixel) > 2:
            self.add_pixel()


    def write_image(self, path):
        """
        Takes the image list and converts it into an actual image
        """
        while len(self.pixel) > 0:
            self.add_byte(0)

        size = int(math.ceil(math.sqrt(len(self.image))))
        data = np.zeros((size, size, 3), dtype=np.uint8)

        count = 0
        try:
            for i in range(size):
                for j in range(size):
                    data[j, i] = self.image[count]
                    count = count + 1
        except IndexError:
            pass


        img = Image.fromarray(data, 'RGB')
        img.save(path)

    def encode(self, content, path):
        """
        Converts text into an image, keeping the data intact
        """
        chars = content.encode('utf-16be')
        for c in chars:
            if ord(c) == 0:
                continue;
            self.add_byte(ord(c))
        self.write_image(path)

    def decode(self, path):
        """
        Converts an image into text, revealing the data inside
        """
        img = Image.open(path)
        pixels = img.load()
        buff = ""

        for i in range(img.size[0]):
            for j in range(img.size[1]):
                if pixels[i,j][0] != 0:
                    buff = buff + (chr(pixels[i,j][0]))

                if pixels[i,j][1] != 0:
                    buff = buff + (chr(pixels[i,j][1]))

                if pixels[i,j][2] != 0:
                    buff = buff + (chr(pixels[i,j][2]))

        print buff
