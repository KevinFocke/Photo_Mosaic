# Photo_Mosaic

## General information

This was a project-based learning experience. Skills I practiced:

- Processing & analyzing image data non-destructively using the Pillow library
- Generalizing the program to expand beyond the original use case
- Improving program speed by caching cropped images & storing them in memory
- Enabling ingress & egress of cropped images from and to bytestreams via Python pickles
- Enabling program customization using preferences

The program converts an image into a beautiful RGB photomosaic.

Example use cases:
- Make a portrait composed of life moments 
- Create a mosaic of your community members 
- Solve the perennial debate: Are tomatoes fruits or vegetables?

![tomatoes_are_fruits](https://user-images.githubusercontent.com/19843342/159955932-ea7d4854-1b9e-4303-a9d8-ae1577fafed3.jpg)

## Usage Information

How to install & run:

    - Run the following command in your terminal

    git clone https://github.com/KevinFocke/Photo_Mosaic.git
    
    - Navigate to cloned folder

    pip install -r requirements.txt

    - Run Photo_Mosaic/src/photomosaic_generator.py

How to customize? 

Change the global flags within photomosaic_generator.py

## Credits

- Project idea from https://robertheaton.com/2018/11/03/programming-project-4-photomosaics/
- Sun image from https://www.pexels.com/photo/abstract-beach-bright-clouds-301599/ 
- Fruits dataset from https://www.kaggle.com/datasets/kritikseth/fruit-and-vegetable-image-recognition
- Tomatoes picture by Andre Taissin https://unsplash.com/photos/hnyZg63sRCY

## Reflection
You can find the reflection & suggested improvements at the bottom of roadmap.md

## Dependencies
- Tested on Python 3.10.2 on VSCode Dev Container

VARIANT": "3.10-bullseye"

NODE_VERSION": "lts/*

- Pillow Image Processing Library https://pillow.readthedocs.io/en/stable/
- Progress bar https://github.com/tqdm/tqdm