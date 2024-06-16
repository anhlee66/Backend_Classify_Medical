
Skin disease - v6 2024-05-20 2:52pm
==============================

This dataset was exported via roboflow.com on May 20, 2024 at 8:00 AM GMT

Roboflow is an end-to-end computer vision platform that helps you
* collaborate with your team on computer vision projects
* collect & organize images
* understand and search unstructured image data
* annotate, and create datasets
* export, train, and deploy computer vision models
* use active learning to improve your dataset over time

For state of the art Computer Vision training notebooks you can use with this dataset,
visit https://github.com/roboflow/notebooks

To find over 100k other datasets and pre-trained models, visit https://universe.roboflow.com

The dataset includes 7236 images.
Skin-cDJA are annotated in folder format.

The following pre-processing was applied to each image:
* Auto-orientation of pixel data (with EXIF-orientation stripping)
* Resize to 480x480 (Fit (white edges))

The following augmentation was applied to create 4 versions of each source image:
* 50% probability of horizontal flip
* 50% probability of vertical flip
* Random brigthness adjustment of between -5 and +5 percent
* Random Gaussian blur of between 0 and 0.6 pixels


