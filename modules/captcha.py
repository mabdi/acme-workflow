import string, random
from flask import session
from PIL import Image, ImageDraw, ImageFont
# try:
# from cStringIO import StringIO
# except ImportError:
from io import BytesIO as StringIO

def validate(inp):
    captcha = session['captcha']
    session['captcha'] = ''
    return inp.lower() == captcha.lower()

def refresh():
    text = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))
    # I know, It's not secure. flask default session management send all data to user as base64.
    # flask-session is recomended.
    # TODO
    session['captcha'] = text
    out = StringIO()
    img = make_image(text)
    img.save(out, "PNG")
    out.seek(0)
    return out


def hex_to_rgb(value):
    """Return (red, green, blue) for the color given as #rrggbb."""
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

# https://github.com/agoravoting/flask-captcha/blob/master/flask_captcha/views.py 
def getsize(font, text):
    return (150,50)
    '''
    if hasattr(font, 'getoffset'):
        return [x + y for x, y in zip(font.getsize(text), font.getoffset(text))]
    else:
        return font.getsize(text)
    '''
    

def noise_arcs(draw, image, fg_color): 
    size = image.size
    draw.arc([-20, -20, size[0], 20], 0, 295, fill=fg_color)
    draw.line([-20, 20, size[0] + 20, size[1] - 20], fill=fg_color)
    draw.line([-20, 0, size[0] + 20, size[1]], fill=fg_color)
    return draw


def noise_dots(draw, image, fg_color): 
    size = image.size
    for p in range(int(size[0] * size[1] * 0.1)):
        draw.point((random.randint(0, size[0]), random.randint(0, size[1])),
                   fill=fg_color)
    return draw

def make_image(text):
    bgcolor = (255,255,255,255)
    from_top = 8
    foreground_color =  hex_to_rgb('#428bca')
    font = ImageFont.truetype('captcha.ttf', 40)
    size = getsize(font, text)
    image = Image.new('RGB', size, bgcolor )
    xpos = 8    
    for char in text:
        fgimage = Image.new('RGB', size, foreground_color)
        charimage = Image.new('L', getsize(font, ' %s ' % char), '#000000')
        chardraw = ImageDraw.Draw(charimage)
        chardraw.text((0, 0), ' %s ' % char, font=font, fill='#ffffff')
        charimage = charimage.crop(charimage.getbbox())
        maskimage = Image.new('L', size)
        maskimage.paste(charimage, (xpos, from_top, xpos + charimage.size[0], from_top + charimage.size[1]))
        size = maskimage.size
        image = Image.composite(fgimage, image, maskimage)
        xpos = xpos + 2 + charimage.size[0]

    #image = image.crop((0, 0, xpos + 1, size[1]))
    draw = ImageDraw.Draw(image)

    draw = noise_arcs(draw, image, foreground_color)
    draw = noise_dots(draw, image, foreground_color)
    return image