from PIL import Image

####################
def negative(image):
    source = image.split()

    R, G, B = 0, 1, 2

    red_reverse = source[R].point(lambda i: 255 - i)
    green_reverse = source[G].point(lambda i: 255 - i)
    blue_reverse = source[B].point(lambda i: 255 - i)

    source[R].paste(red_reverse, None, None)
    source[G].paste(green_reverse, None, None)
    source[B].paste(blue_reverse, None, None)

    image = Image.merge(image.mode, source)
    return image
####################

####################
def high_contrast(image):
    for i in range(0, image.size[0]):
        for j in range(0, image.size[1]):
            if image.getpixel((i, j))[0] + image.getpixel((i, j))[1] + image.getpixel((i, j))[2] > 366:
                image.putpixel([i, j], (image.getpixel((i, j))[0] + 50, image.getpixel((i, j))[1] + 50,
                                        image.getpixel((i, j))[2] + 50))
            else:
                image.putpixel([i, j], (image.getpixel((i, j))[0] - 50, image.getpixel((i, j))[1] - 50,
                                        image.getpixel((i, j))[2] - 50))

    return image
####################

####################
def black_and_white(image):
    R, G, B = 0, 1, 2
    source = image.split()
    source[B].paste(source[R], None, None)
    source[G].paste(source[R], None, None)
    image = Image.merge(image.mode, source)

    return image
####################


image = Image.open("/home/ivar-svart/Pictures/Ibragim.jpg")
negative(image).save("Ibragim_distorted.jpg","JPEG")