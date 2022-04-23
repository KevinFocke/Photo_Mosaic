# Photo_Mosaic

Converts an image into a beautiful RGB photomosaic.

Example use cases:
- Make a portrait composed of life moments 
- Create a mosaic of your community members 
- Solve the perennial debate: Are tomatoes fruits or vegetables?

![tomatoes_are_fruits](https://user-images.githubusercontent.com/19843342/159955932-ea7d4854-1b9e-4303-a9d8-ae1577fafed3.jpg)

How to install & run:

    git clone https://github.com/KevinFocke/Photo_Mosaic.git
    
    - Navigate to cloned folder

    pip install -r requirements.txt

    - Run Photo_Mosaic/src/photomosaic_generator/photomosaic_generator.py


How to customize? 

Change the global flags within photomosaic_generator.py

Credits:

- Project idea from https://robertheaton.com/2018/11/03/programming-project-4-photomosaics/
- Sun image from https://www.pexels.com/photo/abstract-beach-bright-clouds-301599/ 
- Fruits dataset from https://www.kaggle.com/datasets/kritikseth/fruit-and-vegetable-image-recognition
- Tomatoes picture by Andre Taissin https://unsplash.com/photos/hnyZg63sRCY

Dependencies:
- Dependency licenses extracted using pip-licenses
- Pillow Image Processing Library https://pillow.readthedocs.io/en/stable/
- Progress bar https://github.com/tqdm/tqdm

Testing:
Tested on Python 3.10.2 on Win 11
Planning to add automated CI testing on different OSs

Dependency licenses generated using pip-licenses:

| Name           | Version | License                                            |
|----------------|---------|----------------------------------------------------|
| Pillow         | 9.0.1   | Historical Permission Notice and Disclaimer (HPND) |
| about-time     | 3.1.1   | MIT License                                        |
| alive-progress | 2.4.0   | MIT License                                        |
| grapheme       | 0.6.0   | MIT                                                |
| tqdm           | 4.63.1  | MIT License; Mozilla Public License 2.0 (MPL 2.0)  |




