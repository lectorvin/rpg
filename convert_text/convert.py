import PIL

from PIL import Image

MAX_WIDTH = 500 # of image
LETTER_HEIGTH = 30 # real letter's height + 2
STRING = 0

def glue(image1, image2, width=0):
    if (image1.size[0]+image2.size[0]) > MAX_WIDTH:
        _width = image1.size[0]
        _height = STRING
    else:
        # image should be 500 or less
        _width = image1.size[0] + image2.size[0]
        _height = 0
    im3 = Image.new("RGB",\
                    ( _width, \
                         max(image1.size[1], image2.size[1])+_height ),\
                    "white")
    im3.paste(image1, (0,0))
    if image1.size[0] < MAX_WIDTH:
        im3.paste(image2, (max(width,image1.size[0]), _height))
    else:
        im3.paste(image2, (width, _height))
    return im3

def word_to_text(srr): # srr - string with one (!) word, that should
                       # be converted to image;
    srr = srr.upper()
    im1 = 0
    for s in srr:
        if s==".":
            s="dot"
        if not(im1): # if not exist im1
            im1 = Image.open("Alphabet\\" + str(s) + ".gif")
        else:
            im2 = Image.open("Alphabet\\" + str(s) + ".gif")
            im1 = glue(im1, im2)
    return im1

def string_to_text(srr):
    words = srr.split(" ")
    current_width = 0
    im = 0
    final_im = Image.new("RGB", (0,0))
    tab = Image.open("Alphabet\\tab.gif")
    slice_ = Image.open("Alphabet\\slice.gif")
    for word in words:
        global STRING
        im = word_to_text(word)
        # im.size[0] - width of the word
        if (current_width + im.size[0]) > MAX_WIDTH:
            while final_im.size[0] < MAX_WIDTH:
                final_im = glue(final_im, slice_, current_width)
                current_width += 1
            STRING += LETTER_HEIGTH
            current_width = 0
        # text + space + next word
        final_im = glue(final_im, tab, current_width)
        current_width += 14
        final_im = glue(final_im, im, current_width)
        current_width += im.size[0] 
    final_im = glue(final_im, tab, current_width)
# correcting errors
    if (current_width<MAX_WIDTH) and (STRING==0):
        final_im = final_im.crop((5,0,current_width,LETTER_HEIGTH))
    else:
        final_im = final_im.crop((5,0,MAX_WIDTH,STRING+LETTER_HEIGTH))
# end correcting
    # 0 - black; 255 - white
    # lambda finds black pixels of letters and paints them white;
    # other pixels lambda paints black
    final_im = Image.eval(final_im, lambda x: 255 if x==0 else 0)
    return final_im

if __name__ == "__main__":
    srr = "dangero!u.s to go alone take. sword please hero it is somewhere! here is stone"
    string_to_text(srr).save("test.gif")
    """ # one word
    srr = "dan!ger.ous"             
    word_to_text(srr).save("save.gif") """ 
