# coding:utf-8
__author__ = 'john'
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random,os,uuid


class Code:
    # 随机一个字母或者数字
    def random_chr(self):
        num = random.randint(1, 3)
        if num == 1:
            char = random.randint(48, 57)
        elif num == 2:
            char = random.randint(97, 122)
        else:
            char = random.randint(65, 90)
        return chr(char)

    #随机一个干扰字符
    def random_dis(self):
        arr = ['^', '%', '^', '&', '*', '@', '#']
        return arr[random.randint(0, len(arr) - 1)]

    #定义干扰字符的颜色,RGB 0~255
    def random_color(self):
        return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

    def random_color2(self):
        return (random.randint(32, 97), random.randint(32, 97), random.randint(32, 97))

    #生成验证码
    def create_code(self):
        width = 240
        height = 60
        #创建一个图片
        image = Image.new('RGB',(width,height),(192,192,192))
        #创建font对象

        font_file = os.path.join(os.path.dirname(__file__),r'static/fonts/') + '11.ttf'

        #print font_file
        font = ImageFont.truetype(font_file,30)
        #创建一个画布
        draw = ImageDraw.ImageDraw(image)
        for x in range(0,width,5):
            for y in range(0,height,5):
                draw.point((x,y),fill = self.random_color())
        #填充烦扰字符
        for v in range(0,width,30):
            dis = self.random_dis()
            w = 5 + v
            h = random.randint(5,15)
            draw.text((w,h),dis,fill=self.random_color2())
        #填充字符
        chars = ''
        for v in range(4):
            c = self.random_chr()
            chars += str(c)
            w = width/4 *v + 10
            h = random.randint(5,15)
            draw.text((w,h),c,font = font,fill=self.random_color())
        #模糊效果
        image.filter(ImageFilter.BLUR)
        image_name = '%s.jpg'%uuid.uuid4().hex
        save_dir = os.path.join(os.path.dirname(__file__),r'static')
        save_dir += r'/code'
        #print save_dir
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        image.save(save_dir + '/' + image_name,'jpeg')
        #image.show()
        return dict(imge_name = image_name,code = chars)



if __name__ == '__main__':
    c = Code()
    c.create_code()