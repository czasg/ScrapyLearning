import base64

from captcha_pool import captcha_engine

ANTI_COOKIE_FIRST = 'anti_spider_first'
ANTI_COOKIE_SECOND = 'anti_spider_second'


def check_anti_spider(anti_cookie): return anti_cookie


def stringToHex(s): return "".join([hex(ord(i))[2:] for i in s])


def next_captcha(byte=True):
    answer, captcha = captcha_handler.next_captcha(byte=byte)
    return answer, base64.b64encode(captcha).decode()


class CaptchaManager:
    def __init__(self, random, image):
        self.random = random  #
        self.image = image
        self.factory = captcha_engine.IMGFactory.from_ir(image, random)

    @classmethod
    def from_config(cls, mode='RGB', size=(240, 60), font_size=36, font_num=4):
        rm = captcha_engine.RandomMan()
        img = captcha_engine.IMG(mode, size, font_size, font_num)
        return cls(rm, img)

    def next_captcha(self, byte=True):
        return self.factory.create_picture(filename='test.jpg', byte=byte)


captcha_handler = CaptchaManager.from_config(font_num=4)

if __name__ == '__main__':
    a, b = next_captcha()
    print(type(b))
    print(type(str(b)))
    print(b.decode())
