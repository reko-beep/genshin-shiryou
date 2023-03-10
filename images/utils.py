
from __future__ import annotations

import typing

from dataclasses import dataclass

from datetime import datetime
import inspect
from PIL import Image, ImageChops, ImageOps, ImageDraw, ImageFont, ImageFilter
import requests
from io import BytesIO
from colorthief import ColorThief



import random
@dataclass
class URL:

    '''
    URL data class
    for easy extending of url and manipulation

    attrs
    --------


    root: base url
    path: pathname
    
    '''

    
    def __init__(self, root: str,
                       path:str= '') -> None:

        self.root = str(root)
        self.path = str(path)        
        self.__fix_url()

    def __fix_url(self):

        self.path = self.path.replace(' ','_',99)
        if self.root.endswith('/'):
            self.root = self.root[:-1]


    def __repr__(self) -> str:
        dict_ = ' '.join([f'{k}={self.__dict__[k]}' for k in self.__dict__])
        return f"<URL {dict_}>"

    def __add__(self, otherURL):

        if isinstance(otherURL, str):

            __url = str(self)
            if __url.endswith('/'):
                return URL(__url[:-1], otherURL)   
        
        else:

            __url = str(self)
            if __url.endswith('/'):
                return URL(__url[:-1], otherURL.path)   
        
    
    def __str__(self) -> str:   
             
        return self.root+"/"+self.path.replace(' ','_',99)


class ImageManipulation:

    @classmethod
    def mask_image(cls, image_original: Image, gradient_levels: int, inverse:bool= False) -> Image:   
        '''
        creates a linear gradient to apply fade

        '''     
        
        from math import pi, sin
        gradient = Image.new('L', (gradient_levels, 1), color=0xFF)
        for x in range(gradient_levels):
            
            gradient.putpixel((x, 0), int(
                255 * (sin(2*pi*(1/4)*x/gradient_levels + pi) + 1)
            ))        
        return gradient.resize(image_original.size)
    
    @classmethod
    def resize_image(cls, image, to_size: tuple) -> Image:
        '''
        resize the [image] keeping the aspect ratio

        --------'

        to_size : [ (width, height)]

        provide either width or height and other should be 0
        '''
        width, height = image.size
        width_to, height_to = to_size
        calculated_size = image.size
        if width_to == 0:
            ratio = height_to/height
            calculated_size = (int(float(width) * float(ratio)),height_to )

        if height_to == 0:
            ratio = width_to/width     
            calculated_size = (width_to, int(float(height) * float(ratio)))

        image_resized = image.resize(calculated_size)

        return image_resized

    @classmethod
    def add_corners(cls,  im: Image, rad: int) -> Image:
        '''
        rounds the corner of image [im] with specified radius [rad]

        returns
        --------

        Image object

        '''
        circle = Image.new('L', (rad * 2, rad * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
        alpha = Image.new('L', im.size, 255)
        w, h = im.size
        alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
        alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
        alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
        alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
        im.putalpha(alpha)
        return im


    @classmethod
    def colorize_image(cls, image: Image, color: tuple):  

        image.load()
        r, g, b, alpha = image.split()
        gray = ImageOps.grayscale(image)
        result = ImageOps.colorize(gray, (0, 0, 0, 0), color) 
        result.putalpha(alpha)
        return result      
      
    @classmethod
    def has_alpha(cls, img: Image):
        
        if img.info.get("transparency", None) is not None:
            return True
        if img.mode == "P":
            transparent = img.info.get("transparency", -1)
            for _, index in img.getcolors():
                if index == transparent:
                    return True
        elif img.mode == "RGBA":
            extrema = img.getextrema()
            if extrema[3][0] < 255:
                return True

        return False

    @classmethod
    def create_image_card(cls,text_field:str, image_link:str, invert:bool = False, heading_text: str= '', image_pos_x: int = 0, image_pos_y: int = 0):
        '''
        
        creates a rounded card [1920x1080] with image [image_link] faded to left added
        '''

        title = ImageFont.truetype('font.ttf', size=75)
        text = ImageFont.truetype('sub.otf', size=25)
        bg_ = Image.open('images/bgs/bg.png','r').convert('RGBA')
        bg = Image.new('RGBA', bg_.size)
        bytes_ = None
        with requests.get(image_link) as r:
            bytes_ = BytesIO(r.content)
        
        if bytes_:
            char_img = Image.open(bytes_, 'r').convert('RGBA')
            if invert:
                char_img = char_img.transpose(Image.FLIP_LEFT_RIGHT)
            char_img = cls.resize_image(char_img, (0, bg.size[1]))


            
            color = cls.get_dominant_color_from_image(bytes_, True, False, False)
            bg_ = cls.colorize_image(bg_, color)

            if cls.has_alpha(char_img):
                width = char_img.size[0]
                height = char_img.size[1]
                if width+image_pos_x > bg.size[0]:
                    width = bg.size[0]
                if height+image_pos_y > bg.size[1]:
                    height = bg.size[0]
                bg_copy = bg_.copy().crop((image_pos_x, image_pos_y, width, height))
                bg_copy.paste(char_img, (0,0), char_img)
                char_img = bg_copy


            grad = cls.mask_image(char_img, 10)    
            char_img.putalpha(grad)      

         
            
         
            bg.paste(char_img, (image_pos_x, image_pos_y), char_img)

        __ = bg_.copy()
        grad =  cls.mask_image(__, 3, True)
        grad = grad.transpose(Image.FLIP_LEFT_RIGHT)

        __.putalpha(grad)
        __.show()

        bg.paste(__, (0,0), __)
        bg.show()
        
        bg = cls.add_corners(bg, 45)
        bg = cls.draw_text_with_halo(bg, (35,40), text_field, title, 'lt', (255,255,255), color )

        if heading_text != '':
            pos = (35, title.getsize(text_field)[1]+25)
            bg = cls.draw_text_with_halo(bg, pos , heading_text, text, 'lt', (255,255,255), color )
        
        return bg

    @classmethod
    def paste_cards(cls, main_image : Image, start_pos : tuple, end_pos: tuple, cards_list : typing.List[dict], subheading_text : str = ''):

        '''
        Pastes a list of cards to main image
        starting from position [start_pos (x,y)]

        subheading_text: text to draw before cards start
        
        '''

        small_font = ImageFont.truetype('sub.otf', size=35)

        start_x = start_pos[0]
        start_y = start_pos[1]
        row = 1
        end_x = end_pos[0]
        end_y = end_pos[1]

        if end_x == 0:
            end_x = main_image.size[0] - 150
        if end_y == 0:
            end_y = main_image.size[1] - 150
        max_item = None

        if subheading_text != '':
            main_image = cls.draw_text_with_halo(main_image, (start_x+105, start_y+20), subheading_text, font=small_font, anchor='rt', col=(255,255,255), halo_col=(54,54,54))
        
        for c, card_ in enumerate(cards_list,1):
            c_copy = card_.copy()
            c_copy['txt'] = c_copy['txt'] 
            c_img = cls.create_card_image(c_copy)

            if max_item is None:
                max_item = (end_x - start_x) // c_img.size[0]

            if c > (max_item * row):
                row += 1
                count_fix = (c - (max_item * (row-1)))
                
            else:
                if row > 1:
                    count_fix = c - ((row-1) * max_item)
                else:
                    count_fix = c 
            

            x = start_x + (count_fix *122) + 30
            y = start_y + ((row - 1) *  152)
            main_image.paste(c_img, (x,y), c_img)
        
        return main_image

    @classmethod
    def create_image_card_wh(cls,text_field:str, image_link:str, width: int, height: int, invert:bool = False, text_lower: bool=False, text_size: int = 25, sub_text: bool = False, sub_text_field: str = '', rounded: bool = True):
        '''
        
        creates a rounded card [1920x1080] with image [image_link] faded to left added
        '''
        title = ImageFont.truetype('font.ttf', size=text_size)
        text = ImageFont.truetype('sub.otf', size=30)
        bg = Image.open('images/bgs/bg.png','r').convert('RGBA')
        if bg.size > (width, height):
            bg = bg.crop((0,0, width, height))
        else:
            bg = bg.resize((width, height), resample=Image.LANCZOS)
        bytes_ = None
        print('img link', image_link)
        with requests.get(image_link, headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'cookie': 'z_theme=11; guest_id=4160438; PHPSESSID=cisf8b989m4h3l52i20lgifkbo'
        }) as r:
            bytes_ = BytesIO(r.content)
        
        if bytes_:
            char_img = Image.open(bytes_, 'r').convert('RGBA')
            if invert:
                char_img = char_img.transpose(Image.FLIP_LEFT_RIGHT)
            char_img = cls.resize_image(char_img, (0, bg.size[1]))
            
            color = cls.get_dominant_color_from_image(bytes_, True, False, False)
            bg = cls.colorize_image(bg, color)

            if cls.has_alpha(char_img):
                bg_copy = bg.copy().crop((0, 0, char_img.size[0], char_img.size[1]))
                bg_copy.paste(char_img, (0,0), char_img)
                char_img = bg_copy
            print(color)

            grad = cls.mask_image(char_img, 15)    
            if invert:
                grad = grad.transpose(Image.FLIP_LEFT_RIGHT)
            char_img.putalpha(grad)       

         
            
            if invert:
                bg.paste(char_img, (bg.size[0]-char_img.size[0],0), char_img)
            else:
                bg.paste(char_img, (0,0), char_img)

        if rounded:
            bg = cls.add_corners(bg, 45)
        if not text_lower:
            bg = cls.draw_text_with_halo(bg, (35,40), text_field, title, 'lt', (255,255,255) , color )
        else:
            bg = cls.draw_text_with_halo(bg, (35,(bg.size[1]-title.getsize(text_field)[1])+10), text_field, title, 'lb', (255,255,255), color )

        if sub_text:
            bg = cls.draw_text_with_halo(bg, (35,(bg.size[1]- title.getsize(text_field)[1])+20), sub_text_field, text, 'lt', (255,255,255), color )
            
        
        return bg

    @classmethod
    def draw_text_with_halo(cls, img, position, text, font, anchor, col, halo_col):
        '''
        draws a halo'd text on img [image] at position (x,y) with font [ImageFont], anchor and color [text color], halo_col [halo color]
        
        '''
        
        halo = Image.new('RGBA', img.size, (0, 0, 0, 0))
        ImageDraw.Draw(halo).text(position, text, font = font, fill = halo_col, anchor = anchor)
        blurred_halo = halo.filter(ImageFilter.GaussianBlur(radius=2))
        ImageDraw.Draw(blurred_halo).text(position, text, font = font, fill = col, anchor = anchor)
        return Image.composite(img, blurred_halo, ImageChops.invert(blurred_halo))



    @classmethod
    def create_card_image(cls, card_dict: dict) -> Image:
        '''
        
        creates a card image for a provided [card_dict]

        required keys of card_dict
        -------------

        card_bg: card background
        title: item name 
        txt: txt shown in card
        img: item image

        -------------

        only img and txt is shown in card
        to show diff txt just modify the txt param of card dict

        '''

        check_args = ['card_bg', 'title', 'txt', 'img']
        check = len(set(check_args).intersection(list(card_dict.keys()))) == 4

        if check:
            with requests.get(card_dict['card_bg']) as r:
                img = Image.open(BytesIO(r.content), 'r').convert('RGBA')
                img_pos = (0, 0)
                center_x = img.size[0] // 2
                center_y = img.size[1] // 2
                font = ImageFont.truetype('numbers.otf', size=25)
                with requests.get(card_dict['img']) as r:
                    itm_img = Image.open(BytesIO(r.content), 'r').convert('RGBA')
                    itm_img = cls.resize_image(itm_img, (0,112))
                img.paste(itm_img, img_pos, itm_img)
                ImageDraw.Draw(img).text((center_x, 122), str(card_dict['txt']), anchor='mm', font=font, fill=(54,54,54))
                return img
        else:
            raise Exception('One of more the required parameters of card is missing in dictionary provided!')

    @classmethod
    def get_dominant_color_from_image(cls, bytes_: typing.Union[str, BytesIO], rgb:bool=False, hex:bool=False, int_color:bool=True):


        if not isinstance(bytes_, BytesIO):
            with requests.get(bytes_) as f:
                bytes_ = BytesIO(f.content)
         
        bytes_ = ColorThief(bytes_)
        
        def clamp(x): 
            return max(0, min(x, 255))
        color = bytes_.get_color(quality=1)
        if rgb:
            return color
        if hex:
            return "{0:02x}{1:02x}{2:02x}".format(clamp(color[0]), clamp(color[1]), clamp(color[2]))            
        return int("{0:02x}{1:02x}{2:02x}".format(clamp(color[0]), clamp(color[1]), clamp(color[2])),16)






def fix_amount(string : str):
    __ = string
    if isinstance(string, str):
        __ = string.replace(',','',99)
        __ = int(__ .replace('N/A','0', 1)) if 'N/A' in __  else __ 
        __ = int(round(float(__),0)) if '.' in __ else int(__)

    return __

def add_cards(*card_dicts_list ):

    cards_sum = []
    cards_ids = []
    for card_list in card_dicts_list:
        for card in card_list:
            if card['title'] not in cards_ids:
                __ = card.copy()
                cards_sum.append(__)
                cards_ids.append(card['title'])
            else:
                __ = cards_ids.index(card['title'])
                cards_sum[__]['txt'] = str(fix_amount(cards_sum[__]['txt']) + fix_amount(card['txt']))


    return cards_sum






def logc(*msg):
    stack = inspect.stack()
    class_name = stack[1][0].f_locals["self"].__class__.__name__
    print(f"[{class_name}] at [{datetime.now().strftime('%c')}] - ", *msg)





                        

