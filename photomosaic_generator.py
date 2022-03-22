from PIL import Image, ImageOps, ImageMath
import os

#Dataset from https://www.kaggle.com/datasets/kritikseth/fruit-and-vegetable-image-recognition
#Images kept in memory once ingested for speed

fruits =("apple", "banana", "grapes", "kiwi", "mango", "orange", "pear", "pineapple", "pomegranate", "watermelon")

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
        # get list of images
        #img_list += os.listdir(img_mosaic_folder + fruit)
        except FileNotFoundError:
            print("Path not found")

    return img_dict

def cropImages(key_values, img_crop_size, save_path):
    # converts images to Squares based on smallest dimension + returns list containing all cropped images
    cropped_img_list = []

    for key_list in key_values: #key_values contains a list of lists
        for imagepath in key_list:
            with Image.open(imagepath) as im:
                if im.mode != "RGB":
                    im = im.convert("RGB")
                resized_image = ImageOps.fit(im, (img_crop_size,img_crop_size))
                resized_image.path = imagepath
                cropped_img_list.append(resized_image)
                #saveImage(resized_image,imagepath, save_path)
    return cropped_img_list


def saveImage(im_file, imagepath, output_filepath):
    #the filename is derived from the input_filepath
    filename = imagepath.split(r"/")[-2:]
    try:
        folder_path = output_filepath + filename[-2]
        os.mkdir(folder_path)
    except FileExistsError:
        pass
    output_filepath = output_filepath + filename[-2] + r"/" + filename[-1]
    im_file.save(output_filepath, "JPEG")

    return filename
        
def create_mosaic_crops():
    img_mosaic_folder = r"ML_Datasets/Fruits_And_Vegetables/train/"
    img_mosaic_intermediate_folder = r"ML_Datasets/Fruits_And_Vegetables/cropped/"
    img_crop_size = 50 #will be cropped to img_crop_size x img_crop_size
    """
    create_mosaic_crops steps:
    1. Get filenames to each image
    2. Crop images and save to /intermediate folder
    3. create_mosaic_crops average pixel of cropped images, save in a sorted list
    """

    img_dict = get_img_filenames(img_mosaic_folder, fruits) # keys are fruit, contains a list of paths to img files
    cropped_image_list = cropImages(img_dict.values(), img_crop_size, img_mosaic_intermediate_folder)
    print("images cropped")
    



    return None

create_mosaic_crops()

print("program finished")