from xmlrpc.client import MAXINT
from PIL import Image, ImageOps, ImageStat, ImageCms
from tqdm import tqdm
import os
import math
import copy
import pickle


#Images kept in memory once ingested for speed

#General preferences
# Note: preferences are global; trading off security for convenience
MOSAIC_TILE_SIZE = 20 #will be cropped to MOSAIC_TILE_SIZE x MOSAIC_TILE_SIZE
# Should filenames be prefixed with the MOSAIC_TILE_SIZE?
MAIN_IMAGE_INPUT_PATH = r"./images/mosaic_image/mosaic_in.jpg" #image to convert into mosaic
MOSAIC_IMAGE_OUTPUT_PATH = r"./images/mosaic_image/mosaic_out.jpg" #where to output the mosaic image
TILE_INPUT_FOLDER_PATH = r"./images/tiles/" #where are the mosaic tiles gathered from?
MOSAIC_TILE_FOLDERS =("mango","orange","pineapple") #looks within these folders of the TILE_INPUT_FOLDER_PATH 
#TODO: Test with empty input to ingress everything from root of TILE_INPUT_FOLDER_PATH

#Intermediate preferences
#Pickles are prioritized over uncropped images; reasoning: takes less processing time. If no pickle is found, the proced
USE_PICKLE = 1 #do you use a python pickle to ingress cropped images?
MOSAIC_PICKLE_FILE_PATH = r"./images/tiles/cropped_tiles.pickle"
SAVE_CROPPED_IMAGES = 0 #should cropped images be saved?
SAVE_PICKLE = 1 #Do cropped images get saved to a pickle?
MOSAIC_CROPPED_TILE_FOLDER = r"./images/tiles/cropped/" #where to save cropped images?


def get_img_filenames(TILE_INPUT_FOLDER_PATH, MOSAIC_TILE_FOLDERS):
    img_dict = {} # keys are fruit, contains a list of paths to img files
    img_suffix = ".jpg"

    for fruit in MOSAIC_TILE_FOLDERS:
        try:
            with os.scandir(TILE_INPUT_FOLDER_PATH + fruit) as folder:
                img_dict[fruit] = []
                for dir_entry in folder:
                    if dir_entry.is_file and dir_entry.path[(-len(img_suffix)):] == img_suffix:
                        img_dict[fruit].append(dir_entry.path)
        except FileNotFoundError:
            print(("Path %s not found"% (TILE_INPUT_FOLDER_PATH + fruit)) + ". Continuing to check other paths.")
    if not img_dict: #if no contents in dict
        quit_error("No images found in folder %s" % TILE_INPUT_FOLDER_PATH, "Double check relative filepath.")
        
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
    
def crop_images(key_values, MOSAIC_TILE_SIZE, save_path, save = 0):
    # converts images to Squares based on smallest dimension + returns list containing all cropped images
    cropped_img_list = []
    print("Cropping images. There are %i source folders. One progress bar per folder:" % len(key_values))
    for key_list in key_values: #key_values contains a list of lists
        for imagepath in tqdm(key_list):
            with Image.open(imagepath) as im:
                if im.mode != "RGB":
                    im = im.convert("RGB")
                resized_image = ImageOps.fit(im, (MOSAIC_TILE_SIZE,MOSAIC_TILE_SIZE))
                resized_image.path = imagepath
                im_tuples = make_im_tuples(resized_image)
                cropped_img_list.append(im_tuples) 
                if save == 1:
                    save_image(resized_image,save_path, imagepath)
    return cropped_img_list

def save_image(im_file, output_filepath, input_imagepath =""):
    #the filename is derived from the input_filepath
    if input_imagepath: #if the object contains something
        filename = input_imagepath.split(r"/")[-2:] #assumption: folder/filename
        try:
            folder_path = output_filepath + filename[-2] #outputted in <fruit> folder
            os.makedirs(folder_path)
        except FileExistsError:
            pass
        output_filepath = output_filepath + filename[-2] + r"/" + filename[-1]
        im_file.save(output_filepath, "JPEG")
        return 0
    else:
        filename = output_filepath.split(r"/")[-1]
        try:
            filename_len = len(filename)
            folder_path = output_filepath[:-filename_len]
            os.makedirs(folder_path)
        except FileExistsError:
            pass
        im_file.save(output_filepath, "JPEG")
    return 0
        
def create_cropped_images():
    """
    create_cropped_images steps:
    1. Get filenames to each image
    2. Crop images and add to cropped_image_tuples
    returns cropped_image_tuples
    """
    img_dict = get_img_filenames(TILE_INPUT_FOLDER_PATH, MOSAIC_TILE_FOLDERS) # keys are fruit, contains a list of paths to img files
    cropped_image_tuples = crop_images(img_dict.values(), MOSAIC_TILE_SIZE, MOSAIC_CROPPED_TILE_FOLDER, save=SAVE_CROPPED_IMAGES)
    cropping_feedback = "Images cropped."
    if SAVE_CROPPED_IMAGES == 1:
        cropping_feedback += " Images saved"
    print(cropping_feedback)
    return cropped_image_tuples

def find_distance(coordinates_object_1,coordinates_object_2):
    if len(coordinates_object_1) != len(coordinates_object_2):
        print("Dimension Mismatch") #the dimensions do not match; eg comparing 2D object to 3D
        #TODO: Raise error
    #take euclidian distance
    coordinates_tuples = zip(coordinates_object_1,coordinates_object_2)
    #red_tuples = coordinates_tuples[0]
    #green_tuples = coordinates_tuples[1]
    #blue_tuples = coordinates_tuples[2]
    sum_sqr_diff = sum([(cor1 - cor2) ** 2 for cor1, cor2 in coordinates_tuples]) # calc list of squared difference
    distance = round(sum_sqr_diff ** (1/2),2)
    return distance

def find_mosaic_tile(mainImage_tuples, cropped_images_list):
    lowest_distance = MAXINT
    lowest_distance_im = None
    for tup in cropped_images_list:
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

def create_mosaic(mainImage_tuples, cropped_images_list, grayscale = 0):
    """
    Steps:
    Per mosaic tile find closest match & insert into mainImage
    Return image
    """
    # FOR EVERY tuple find_distance(mainImage_tuples[1:],cropped_images_list[1:])
    #image tuples consist of (Im, avg_red, avg_green, avg_blue) tuples

    mainImage_length = mainImage_tuples[0].size[0]
    mainImage_width = mainImage_tuples[0].size[1]
    mainImage_tiles_in_length = math.trunc(mainImage_length / MOSAIC_TILE_SIZE)#how many tiles fit in a length?
    mainImage_tiles_in_width = math.trunc(mainImage_width / MOSAIC_TILE_SIZE) # how many tiles fit in width?

    mosaic_im = copy.deepcopy(mainImage_tuples[0]) #make deep copy of mainImage im
    #boxes start from the top-left
    row_pixel_top = 0 #at which pixel do we start row-wise?
    col_pixel_left = 0
    print("Creating mosaic:")
    for row in tqdm(range(mainImage_tiles_in_width)):
        for col in range(mainImage_tiles_in_length):
            left, upper, right, lower = [col_pixel_left, row_pixel_top, col_pixel_left+MOSAIC_TILE_SIZE, row_pixel_top + MOSAIC_TILE_SIZE]
            tile_tuples = make_im_tuples(select_tile(mainImage, left, upper, right, lower))
            mosaic_tile_im = find_mosaic_tile(tile_tuples, cropped_images_list)
            mosaic_im.paste(mosaic_tile_im, (left, upper, right, lower))
            #save_image(mosaic_im, MOSAIC_IMAGE_OUTPUT_PATH)
            col_pixel_left += MOSAIC_TILE_SIZE
        col_pixel_left = 0 # reset col_pixel
        row_pixel_top += MOSAIC_TILE_SIZE
    save_image(mosaic_im,MOSAIC_IMAGE_OUTPUT_PATH)
    return 0
        
def quit_error(error_message = "", suggestion_message =""):
    print("\nProgram will abort because it encountered an error.")
    if error_message: #check if object contains something
        print("Error: " + error_message)
    if suggestion_message:
        print("Suggestion: " + suggestion_message)
    print("Python file ran from: \n%s"% os.getcwd())
    print("Aborting program.")
    quit()
    
def check_tile_size(im, MOSAIC_TILE_SIZE):
    if ((im.size[0] % MOSAIC_TILE_SIZE) != 0) or ((im.size[1] % MOSAIC_TILE_SIZE) != 0):
        print("Image dimensions %i x %i is not cleanly divisible by mosaic tile size %i" % (mainImage.size[0], mainImage.size[1], MOSAIC_TILE_SIZE))

        # calculate smallest image dimension
        if im.size[0] <= im.size[1]:
            smallest_dim = im.size[0]
        else:
            smallest_dim = im.size[1]
        # calculate the amount of cropping options, reduce by factor of 10.
        if (cropping_options := smallest_dim // MOSAIC_TILE_SIZE // 10) > 1: pass 
        else:
            suggested_min_dimension = MOSAIC_TILE_SIZE * 10
            quit_error("Mosaic input image too small", "Use a mosaic input image with a smallest dimension of at least %i px" % suggested_min_dimension)
        # calculate image aspect ratio using greatest common denominator
        im_gcd = math.gcd(im.size[0], im.size[1])
        im_aspect_ratio = [im.size[0]//im_gcd, im.size[1]//im_gcd]
        # suggest image dimensions
        cropping_suggestions = [(list(map((lambda x: x * MOSAIC_TILE_SIZE * i), im_aspect_ratio))) for i in range(1,(cropping_options)+2)]  # maps th

        quit_error("Image dimensions do not match tilesize.", "Crop your image to one of these width x height dimensions:\n" + str(cropping_suggestions))

def check_pickle(cropped_images_list):
    # Is every image the correct type, crop size, mode?
    for im_tuple in cropped_images_list:
        if not (isinstance(im_tuple[0], Image.Image)):
            return 1
        if not (im_tuple[0].mode == "RGB"):
            return 1
        if not (im_tuple[0].size[0] == MOSAIC_TILE_SIZE or im_tuple[0].size[1] == MOSAIC_TILE_SIZE):
            return 1
        # Are the computed avg colour values between 0 and 255?
        for colour in im_tuple[1:]:
            if not (colour >= 0 or colour <= 255):
                return 1


def ingressPickle():
    """
    Returns a 1 if pickle is not valid."""
    cropped_images_list = []
    try:
        with open(MOSAIC_PICKLE_FILE_PATH, "rb") as fp_pickle_path:
            cropped_images_list = pickle.load(fp_pickle_path)
            print("Pickle has been loaded")
    except:
        print("Could not open pickle file. Reverting to fallback.")
    if (check_pickle(cropped_images_list) == 1):
        print("Pickle file showed error during ingestion. Reverting to fallback.")
        return 1

    return cropped_images_list

def egressPickle(cropped_image_list):
        try: 
            with open(MOSAIC_PICKLE_FILE_PATH, "wb") as fp_pickle_path:
                pickle.dump(cropped_image_list, fp_pickle_path)
        except:
            print("Could not write pickle file.")
            return 1



if __name__ == "__main__":
    """
    General program flow:

    Open the main image.
    If USE_PICKLE = 1, ingress the pickle into a cropped_imagelist. Else process each image in the Tile_Input_Folder_Path/{MOSAIC_TILE_FOLDERS}
    Create a mosaic based on the lowest avg distance between a region of the main image, and every cropped_imagelist.
    If SAVE_PICKLE = 1, egress the pickle.

    cropped_image_list is a list of tuples of form:
    (im, avgRed,avgGreen,avgBlue)
    
    """
    mainImage_tuples = ()
    cropped_images_list = ()

    try: 
        with Image.open(MAIN_IMAGE_INPUT_PATH) as mainImage:
            mainImage_tuples = make_im_tuples(mainImage)
            check_tile_size(mainImage, MOSAIC_TILE_SIZE) #Check whether image divisible by tilesize
    except FileNotFoundError:
        quit_error("No image found in %s" % MAIN_IMAGE_INPUT_PATH, "Double check relative filepath.")

    # Ingest tile pickle OR create cropped images.
    pickle_valid = 0
    if USE_PICKLE == 1:
        if (cropped_images_list := ingressPickle()) != 1:
            pickle_valid = 1 # the pickle is valid
    if pickle_valid == 0:
        cropped_images_list = create_cropped_images()
    create_mosaic(mainImage_tuples, cropped_images_list)
    if SAVE_PICKLE == 1:
        egressPickle(cropped_images_list)
    print("Program finished.")
