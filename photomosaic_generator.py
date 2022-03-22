from PIL import Image, ImageOps
import os

#Dataset from https://www.kaggle.com/datasets/kritikseth/fruit-and-vegetable-image-recognition
#Images kept in memory once ingested for speed

fruits =("apple", "banana", "grapes", "kiwi", "mango", "orange", "pear", "pineapple", "pomegranate", "watermelon")
img_square_size = 20 #will be cropped to img_square_size x img_square_size
main_image_path = "ML_Datasets/Fruits_And_Vegetables/mosaic/input/tomatoes.jpeg"


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

def cropImages(key_values, img_square_size, save_path):
    # converts images to Squares based on smallest dimension + returns list containing all cropped images
    cropped_img_list = []

    for key_list in key_values: #key_values contains a list of lists
        for imagepath in key_list:
            with Image.open(imagepath) as im:
                if im.mode != "RGB":
                    im = im.convert("RGB")
                resized_image = ImageOps.fit(im, (img_square_size,img_square_size))
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
        
def create_cropped_images():
    img_mosaic_folder = r"ML_Datasets/Fruits_And_Vegetables/train/"
    img_mosaic_intermediate_folder = r"ML_Datasets/Fruits_And_Vegetables/cropped/"
    """
    create_cropped_images steps:
    1. Get filenames to each image
    2. Crop images and add to cropped_image_list
    returns cropped_image_list
    """

    img_dict = get_img_filenames(img_mosaic_folder, fruits) # keys are fruit, contains a list of paths to img files
    cropped_image_list = cropImages(img_dict.values(), img_square_size, img_mosaic_intermediate_folder)
    print("images cropped")
    return cropped_image_list

if __name__ == "__main__":
    with Image.open(main_image_path) as mainImage:
        if ((mainImage.size[0] % img_square_size) != 0) or ((mainImage.size[1] % img_square_size) != 0):
            print("Image dimensions %i x %i is not cleanly divisible by mosaic tile size %i" % (mainImage.size[0], mainImage.size[1], img_square_size))
            quit()
        cropped_image_list = create_cropped_images()
    create_mosaic(mainImage, cropped_image_list)

    


print("program finished")