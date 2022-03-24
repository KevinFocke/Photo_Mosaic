from xmlrpc.client import MAXINT
from PIL import Image, ImageOps, ImageStat
import os
import math
import copy

#Dataset from https://www.kaggle.com/datasets/kritikseth/fruit-and-vegetable-image-recognition
#Images kept in memory once ingested for speed

fruits =("apple", "banana", "grapes", "kiwi", "mango", "orange", "pear", "pineapple", "pomegranate", "watermelon")
mosaic_tile_size = 20 #will be cropped to mosaic_tile_size x mosaic_tile_size
main_image_path = "ML_Datasets/Fruits_And_Vegetables/mosaic/input/tomatoes.jpeg"
mosaic_image_output_path = "ML_Datasets/Fruits_And_Vegetables/mosaic/output/tomatoes_are_fruits.jpeg"

def get_img_filenames(img_mosaic_folder, fruits):
    img_dict = {} # keys are fruit, contains a list of paths to img files
    img_suffix = ".jpg"

    for fruit in fruits:
        try:
            img_dict[fruit] = []
            paths_nested_list = []
            with os.scandir(img_mosaic_folder + fruit) as folder:
                for dir_entry in folder:
                    if dir_entry.is_file and dir_entry.path[(-len(img_suffix)):] == img_suffix:
                        img_dict[fruit].append(dir_entry.path)
        except FileNotFoundError:
            print("Path not found")

    return img_dict

#def calc_average(colour_band_list):
 #   for colour in colour_band_list:

def make_im_tuples(im):
    """"
    converts im to RGB + colour band mean tuples
    """
    if im.mode != "RGB":
        im = im.convert("RGB")
    im_statistics = ImageStat.Stat(im)
    avgs_colour = [math.trunc(colour) for colour in im_statistics.mean] #R G B
    
    return (im, avgs_colour[0], avgs_colour[1], avgs_colour[2])
    
def crop_images(key_values, mosaic_tile_size, save_path, save = 1):
    # converts images to Squares based on smallest dimension + returns list containing all cropped images
    cropped_img_list = []

    for key_list in key_values: #key_values contains a list of lists
        for imagepath in key_list:
            with Image.open(imagepath) as im:
                if im.mode != "RGB":
                    im.convert("RGB")
                resized_image = ImageOps.fit(im, (mosaic_tile_size,mosaic_tile_size))
                resized_image.path = imagepath
                im_tuples = make_im_tuples(resized_image)
                cropped_img_list.append(im_tuples) 
                if save == 1:
                    save_image(resized_image,save_path, imagepath)
    return cropped_img_list

def save_image(im_file, output_filepath, input_imagepath =""):
    #the filename is derived from the input_filepath
    if input_imagepath: #if the object contains something
        filename = input_imagepath.split(r"/")[-2:]
        try:
            folder_path = output_filepath + filename[-2]
            os.mkdir(folder_path)
        except FileExistsError:
            pass
        output_filepath = output_filepath + filename[-2] + r"/" + filename[-1]
        im_file.save(output_filepath, "JPEG")
        return 0
    else:
        try:
            filename_len = len(output_filepath.split(r"/")[-1])
            folder_path = output_filepath[:-filename_len]
            os.mkdir(folder_path)
        except FileExistsError:
            pass
        im_file.save(output_filepath, "JPEG")
    return 0
        
def create_cropped_images():
    img_mosaic_folder = r"ML_Datasets/Fruits_And_Vegetables/test/" #where are the mosaic tiles gathered from?
    img_mosaic_intermediate_folder = r"ML_Datasets/Fruits_And_Vegetables/cropped/" #where are the mosaic tiles saved?
    save_cropped_images = 1 #should cropped_images be saved?
    """
    create_cropped_images steps:
    1. Get filenames to each image
    2. Crop images and add to cropped_image_list
    returns cropped_image_list
    """

    img_dict = get_img_filenames(img_mosaic_folder, fruits) # keys are fruit, contains a list of paths to img files
    cropped_image_list = crop_images(img_dict.values(), mosaic_tile_size, img_mosaic_intermediate_folder, save=save_cropped_images)
    print("images cropped")
    return cropped_image_list

def find_distance(coordinates_object_1,coordinates_object_2):
    if len(coordinates_object_1) != len(coordinates_object_2):
        print("Dimension Mismatch") #the dimensions do not match; eg comparing 2D object to 3D
        #TODO: Raise error
    #take euclidian distance
    obj_dimensions = len(coordinates_object_1)
    sum_sqr_diff = sum([(cor1 - cor2) ** 2 for cor1 in coordinates_object_1 for cor2 in coordinates_object_2]) # calc list of squared difference
    distance = round(sum_sqr_diff ** (1/obj_dimensions),2)
    return distance

def find_mosaic_tile(mainImage_tuples, cropped_images_tuples):
    lowest_distance = MAXINT
    lowest_distance_im = None
    for tup in cropped_images_tuples:
        cur_distance = find_distance(mainImage_tuples[1:],tup[1:])
        if  cur_distance < lowest_distance:
            lowest_distance = cur_distance
            lowest_distance_im = tup[0]
        else: pass
    return lowest_distance_im

def select_tile(im, left, upper, right, lower):
    """
    Takes a rectangular tile from an image
    # crop function works by taking (left, upper, right, lower)
    returns im
    """
    tile = im.crop((left, upper, right, lower))
    return tile


def create_mosaic(mainImage_tuples, cropped_images_tuples):
    """
    Steps:
    Per mosaic tile find closest match & insert into mainImage
    Return image
    """
    # FOR EVERY tuple find_distance(mainImage_tuples[1:],cropped_images_tuples[1:])
    #image tuples consist of (Im, avg_red, avg_green, avg_blue) tuples

    mainImage_length = mainImage_tuples[0].size[0]
    mainImage_width = mainImage_tuples[0].size[1]
    mainImage_tiles_in_length = math.trunc(mainImage_length / mosaic_tile_size)#how many tiles fit in a length?
    mainImage_tiles_in_width = math.trunc(mainImage_width / mosaic_tile_size) # how many tiles fit in width?

    mosaic_im = copy.deepcopy(mainImage_tuples[0]) #make deep copy of mainImage im
    #boxes start from the top-left
    row_pixel_top = 0 #at which pixel do we start row-wise?
    col_pixel_left = 0
    for row in range(mainImage_tiles_in_width):
        for col in range(mainImage_tiles_in_length):
            left, upper, right, lower = [col_pixel_left, row_pixel_top, col_pixel_left+mosaic_tile_size, row_pixel_top + mosaic_tile_size]
            tile_tuples = make_im_tuples(select_tile(mainImage, left, upper, right, lower))
            mosaic_tile_im = find_mosaic_tile(tile_tuples, cropped_images_tuples)
            mosaic_im.paste(mosaic_tile_im, (left, upper, right, lower))
            #save_image(mosaic_im, mosaic_image_output_path)
            col_pixel_left += mosaic_tile_size
        col_pixel_left = 0 # reset col_pixel
        row_pixel_top += mosaic_tile_size
    save_image(mosaic_im,mosaic_image_output_path)
    return 0
        



    



if __name__ == "__main__":
    with Image.open(main_image_path) as mainImage:
        mainImage_tuples = make_im_tuples(mainImage)
        if ((mainImage.size[0] % mosaic_tile_size) != 0) or ((mainImage.size[1] % mosaic_tile_size) != 0):
            print("Image dimensions %i x %i is not cleanly divisible by mosaic tile size %i" % (mainImage.size[0], mainImage.size[1], mosaic_tile_size))
            quit()
        cropped_images_tuples = create_cropped_images()
        create_mosaic(mainImage_tuples, cropped_images_tuples)
        #save image

    


print("program finished")