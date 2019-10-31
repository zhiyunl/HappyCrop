# HappyCrop
This is a small tool for interactively cropping images and create a series of sub images.

*Developed for DL-HCR project on Machine Learning Course @UF*

Description
---
Crop scanned image interactively, create multiple sub-images,
    and save into folder named after labels

Depend on `python-opencv`:
    if cv2 not found, install using : 
            
    pip install opencv-python

**Need to create handwritten image database more quickly?**

**Getting tired of crop images using MS Paint, GIMP or even PS?**

**Or still taking pictures of 1 character each?**

**A handy tool can be helpful!**

Usage
---
1. Running
    + Command line format: `python imCrop.py $sourceImageDir $outputDir [$outputPrefix]`
        
        For example,   `python imCrop.py myimage.jpg ./output "output_"`

        1. This will take in *myimage.jpg*, open it in a pop-up window.
        2. Crop continuously by draw rectangle with mouse.
        3. Close window when you are done, output image will be in *./output* folder.
        4. Image name will looks like *output_1001.jpg*.

    + if using IDE:
    
        + Change `CMDLINE = False`

        + Or set input parameter in IDE, check *./.idea/runConfiguration/imCrop.xml*, it's for Pycharm

1. Use *left mouse* to crop, *right mouse* to change to dir for the next label

1. Program will automatically exits when labels are all done.
        
   But if you want to stop, press `Escape` or close window
