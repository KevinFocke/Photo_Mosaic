Ver 1 – Simply works

x Can inefficiently create a photo_mosaic (NO PREMATURE OPTIMIZATION!)

Ver 2 – Plug & Play

x Allow pickle ingress for tiles instead of converting cropped images each time.

x Generalize program so it can be used for non-fruit-related purposes.

x Add sample image folder for plug-and-play Github code.

Ver 3 – Benchmarking & Testing

Prerequisite for improving efficiency.

- Setup benchmarking (run tests of large + small dataset)
- Setup continuous integration environment
- Setup testing

Ver 4 – More efficient! More accurate!

- Optimize efficiency of find_mosaic_tile algorithm. (Currently loops through EVERY image to find the closest match.)

Dynamically bucketed for large datasets. The boundary which defines a large dataset is based on benchmarks.

- Improve colour representativeness of distance algorithm. Consider using a more accurate perceptual colour profile like LAB.

- Create pipenv https://pipenv.pypa.io/en/latest/ for easy install