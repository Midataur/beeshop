from PIL import Image, ImageFilter, ImageDraw
import numpy as np

def color_filter(img, target, threshold=35):
    target = np.array(target)

    pixels = np.array(img)

    diffs = pixels-np.full((img.size[1],img.size[0],3),target)
    mags = np.sqrt((diffs*diffs).sum(axis=2))
    #add back the axis we lost then do a conditional replace
    new_pixels = np.where(mags[:,:,np.newaxis] <= threshold, target, (0,0,0))
    new_pixels = new_pixels.astype(np.uint8)

    return Image.fromarray(new_pixels)

def find_boarders(image_array):
    edges = []

    for y in [1,-1]:
        hit = False
        for pos,x in enumerate(image_array[::y]):
            if x.max() > 0:
                hit = True
            elif hit == True:
                edges.append(pos)
                break

    for y in [1,-1]:
        hit = False
        for x in range(image_array.shape[1]):
            if image_array[:,y*x].max() > 0:
                hit = True
            elif hit == True:
                edges.append(x)
                break

    #fix bottom and right
    edges[1] = image_array.shape[0]-edges[1]
    edges[3] = image_array.shape[1]-edges[3]

    return edges

def crop_and_split(image_array, edges):
    #crop
    image_array = image_array[edges[0]:edges[1], edges[2]:edges[3]]

    #make sure array is disvis by 8 so we can split them nicely
    #rows
    new_row = np.zeros((1,image_array.shape[1],3))
    for x in range(8-(image_array.shape[0] % 8)):
        image_array = np.vstack((image_array, new_row))

    #cols
    new_col = np.zeros((image_array.shape[0],1,3))
    for x in range(8-(image_array.shape[1] % 8)):
        image_array = np.hstack((image_array, new_col))

    #combine the pixel colors into one color
    image_array = image_array.max(axis=2)

    #split into 64 squares
    splitten = np.array([np.hsplit(x, 8) for x in np.split(image_array, 8)])

    #max will tell us if any pixels are not black
    converted = splitten.max(axis=(2,3))
    return converted

def to_binmap(converted):
    #convert to board state
    binmap = np.invert(converted.astype(bool)).astype(int)
    binmap = np.rot90(binmap,k=3) #for some reason the image gets out of orientation
    return binmap

def image_to_binmap(img):
    print('Colour filter p1')
    filtered = color_filter(img, (11,179,210), 100)
    print('Colour filter p2')
    filtered = filtered.filter(ImageFilter.MaxFilter(size=5))
    print('Cropping and splitting')
    image_array = np.array(filtered)

    #Image.fromarray(image_array).show()

    edges = find_boarders(image_array)
    splitten = crop_and_split(image_array, edges)
    binmap = to_binmap(splitten)
    return binmap