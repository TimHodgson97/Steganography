import PIL
from PIL import Image

def tups(lst,n):
    for i in range(0, len(lst), n):
        yield tuple(lst[i:i+n])

def decode_binary_string(s):
    return ''.join(chr(int(s[i*8:i*8+8],2)) for i in range(len(s)//8))

def encode_pic(file_name = "sample.txt", image_name = 'bible_small.png', steg_name = 'bible_steg.png'):
    
    # Open File into string
    with open(file_name, "r") as f:
        f_string = f.read()

    # Make File text into binary string and divide it into pairs of bits
    binary_string= ''.join(format(ord(i), '08b') for i in f_string)
    array_oftwobits = [binary_string[i:i+2] for i in range(0, len(binary_string), 2)]

    # Open image to be manipulated and create image that will store steg data
    im = Image.open(image_name)

    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    
    im2 = Image.new(im.mode,im.size)
    # Pull pixel data into list
    pixels = list(im.getdata())

    # Get list of alpha values   
    alpha_values = []
    for p in pixels:
        alpha_values.append(p[3])
    
    # Make pixel data into binary
    binary_pixels = []
    for p in pixels:
        for i in range(0, len(p) - 1):
            binary_pixels.append(("{0:b}".format(p[i])).zfill(8))

    steg_pixels = binary_pixels

    for p in range(len(steg_pixels)):
        if p < len(array_oftwobits):
            steg_pixels[p] = int(str(steg_pixels[p][:-2] + array_oftwobits[p]), 2)
        else:
            steg_pixels[p] = int(steg_pixels[p],2)

    new_image_data = []
    count = 1
    alph = 0
    pix = 0
    while len(new_image_data) < len(pixels) * 4:
        if count%4 == 0:
            new_image_data.append(alpha_values[alph])
            alph += 1
        else:
            new_image_data.append(steg_pixels[pix])
            pix += 1
        count += 1

    new_image_data = list(tups(new_image_data, 4))


    im2.putdata(new_image_data)
    im2.save(steg_name)

    print("Steganographised")


def decode_pic(file_name = 'hidden_message.txt', image_name = 'very_big_steg.png'):
    im = Image.open(image_name)
    
    if im.mode != 'RGBA':
        im = im.convert('RGBA')

    steg_pixels = list(im.getdata())

    binary_pixels = []
    for p in steg_pixels:
        for i in range(0, len(p) - 1):
            binary_pixels.append(("{0:b}".format(p[i])).zfill(8))

    hidden_msg = []

    for p in binary_pixels:
        hidden_msg.append(p[-2:])

    binary_string = ''.join(hidden_msg)

    msg = decode_binary_string(binary_string[:17607535])

    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(msg)
    
    print("Desteganographised")

encode_pic('ACV.txt', 'very_big_bible.png', 'very_big_steg.png')
decode_pic()