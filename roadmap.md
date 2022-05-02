# Roadmap

## Ver 1 – Simply works

x Can inefficiently create a photo_mosaic (NO PREMATURE OPTIMIZATION!)

## Ver 2 – Plug & Play

x Allow pickle ingress for tiles instead of converting cropped images each time.

x Generalize program so it can be used for non-fruit-related purposes.

x Add sample image folder for plug-and-play Github code.

## Reflection

The purpose of this project was to learn the specific skills outlined in README.md. To make the program production-ready, several more changes are required.

Opportunities for improvement:

- Decrease dependence on global variables. The current implementation works fine for making a single photomosaic. However, it will get into scaling problems when using multiple mosaics with different filepaths, tile sizes, etc.

- Add testing & automated deployment for continuous integration of changes. This is a major focus in my next project.

- Add benchmarking to measure the effectiveness of algorithms.

- Optimize find_tile algorithm. Currently it iterates through every image. For large datasets this will take too much processing time. Instead, the images can be bucketed.