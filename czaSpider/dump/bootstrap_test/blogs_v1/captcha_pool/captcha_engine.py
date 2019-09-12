import os

from random import randint
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO

current_path = os.path.dirname(os.path.abspath(__file__))


class RandomMan:
    def __init__(self, upper=True, color1=(64, 255), color2=(32, 127)):
        self.rndCharRange = (65, 90) if upper else (97, 122)
        self.rndColor1Range = color1
        self.rndColor2Range = color2

    def _get_randint(self, num=0, *args): return [randint(*args) for _ in range(num)]

    def rndChar(self, num=1): return [chr(*self._get_randint(1, *self.rndCharRange)) for _ in range(num)]

    def rndInt(self, num=1): return [randint(0, 9) for _ in range(num)]

    def rndColor1(self, num=3): return tuple(self._get_randint(num, *self.rndColor1Range))

    def rndColor2(self, num=3): return tuple(self._get_randint(num, *self.rndColor2Range))


class IMG:
    def __init__(self, mode='RGB', size=(240, 60), font_size=36, font_num=4,
                 fontSyle_path=os.path.join(current_path, 'Arial.ttf')):
        self.img = Image.new(mode, size, (255, 255, 255))
        self.width, self.height = size
        self.mode = mode
        try:
            self.font = ImageFont.truetype('Arial.ttf', font_size)
        except:
            self.font = ImageFont.truetype(fontSyle_path, font_size)
        self.draw = ImageDraw.Draw(self.img)
        self.font_num = font_num


class IMGFactory:
    def __init__(self, IMG, RandomMan, blur):
        self.img = IMG
        self.randomMan = RandomMan
        self.blur = blur
        self.res_img = None

    @classmethod
    def from_ir(cls, image, randomMan, blur=True):
        return cls(image, randomMan, blur)

    def _fill_pixel(self):
        for x in range(self.img.width):
            for y in range(self.img.height):
                self.img.draw.point((x, y), fill=self.randomMan.rndColor1())

    def _fill_font(self):
        lis = []
        _width = self.img.width // self.img.font_num
        for t in range(self.img.font_num):
            font = self.randomMan.rndChar()[0]
            lis.append(font)
            self.img.draw.text((_width * t + _width // 4, self.img.height // 4), font,
                               font=self.img.font, fill=self.randomMan.rndColor2())
        self.res_img = ''.join(lis)

    def _blur(self):
        if self.blur:
            self.img.img = self.img.img.filter(ImageFilter.BLUR)

    def save(self, filename='test.jpg', mode='jpeg', byte=False):
        if byte:
            filename = BytesIO()
        else:
            filename = os.path.join(current_path, filename)
        self.img.img.save(filename, mode)
        if byte:
            filename = filename.getvalue()
        return filename

    def create_picture(self, filename='test.jpg', mode='jpeg', byte=False):
        self._fill_pixel()
        self._fill_font()
        # self._blur()
        return self.res_img, self.save(filename, mode, byte)


def get_random_pic(font_num=4, byte=True):
    rm = RandomMan()
    img = IMG(font_num=font_num)
    handle = IMGFactory.from_ir(img, rm)
    return handle.create_picture(byte=byte)


if __name__ == '__main__':
    rm = RandomMan()
    img = IMG(font_num=4)
    handle = IMGFactory.from_ir(img, rm)
    pic = handle.create_picture(byte=False)
