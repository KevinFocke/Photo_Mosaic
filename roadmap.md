Ver 1:

x Can inefficiently create a photo_mosaic (NO PREMATURE OPTIMIZATION!)

Ver 2:

x Allow pickle ingress for tiles instead of converting cropped images each time.

- Upload package to python package library 

https://packaging.python.org/en/latest/tutorials/packaging-projects/

x Generalize program so it can be used for non-fruit-related purposes.

x Add sample image folder for plug-and-play Github code.

Ver 3:

- Optimize efficiency of distance algorithm. (The program currently loops through EVERY image to find the closest match.)

Bucket values per colour. Buckets are a multiple of 2 (RGB values are between 0 and 255)

- Improve colour representativeness of distance algorithm. Consider using a more accurate perceptual colour profile like LAB.

- Setup continuous integration environment + testing.