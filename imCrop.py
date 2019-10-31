# -- coding: utf-8 --
"""
Description:
    Crop scanned image interactively, create multiple sub-images,
    and save into folder named after labels

    using python-opencv:
        if cv2 not found, install using : "pip install opencv-python"

    Developed for DL-HCR project on Machine Learning Course @UF

    Need to create handwritten image database more quickly?
    Getting tired of crop images using MS Paint, GIMP or even PS?
    Or still taking pictures of 1 character each?
    A handy tool can be helpful!

Usage:
    1. cmd line: python imCrop.py <sourceImageDir> <outputDir> <outputPrefix>
        e.g. python imCrop.py myimage.jpg ./output "output_"

        This will take in myimage.jpg, open it in a pop-up window.
        Crop continuously by draw rectangle with mouse
        Close window when you are done, output image will be in ./output folder
        image name will looks like output_1001.jpg

    2. if using IDE, a) change CMDLINE = False
                     b) or set input parameter in IDE, check ./.idea/runConfiguration/imCrop.xml for Pycharm

    3. use left mouse to crop, right mouse to change to next output dir

    4. program will automatically exits when labels are all done.
        if you want to stop, press Escape or close window


"""
import os
import sys

import cv2

# TODO change to False if IDE
CMDLINE = True


class DataGenerate:
    label_dict = []
    cnt = 0
    p1 = None
    p2 = None
    img = None
    mask = None
    out_dir = ""
    prefix = ""
    cur = 0
    title = ""

    def nextDir(self):
        if self.cur < len(self.label_dict) - 1:
            self.cur += 1
            self.cnt = 0
            print("current output directory is : %s" % self.out_dir + "/" + str(self.label_dict[self.cur]))
        else:
            print("reached final output dir!")
            sys.exit(0)

    def mouseInterrupt(self, event, x, y, flags, param):
        mask = self.img.copy()
        if event == cv2.EVENT_LBUTTONDOWN:  # left click
            self.p1 = (x, y)
            cv2.circle(mask, self.p1, 10, (0, 255, 0), 5)
            cv2.imshow(self.title, mask)
        elif event == cv2.EVENT_MOUSEMOVE and (flags and cv2.EVENT_FLAG_LBUTTON):  # drag with left key
            cv2.rectangle(mask, self.p1, (x, y), (255, 0, 0), 5)
            cv2.imshow(self.title, mask)
        elif event == cv2.EVENT_LBUTTONUP:  # left key release
            self.p2 = (x, y)
            cv2.rectangle(mask, self.p1, self.p2, (0, 0, 255), 5)
            cv2.imshow(self.title, mask)
            hor = (self.p1[0], self.p2[0]) if self.p1[0] < self.p2[0] else (self.p2[0], self.p1[0])
            ver = (self.p1[1], self.p2[1]) if self.p1[1] < self.p2[1] else (self.p2[1], self.p1[1])
            roi = self.img[ver[0]:ver[1], hor[0]:hor[1]]
            cv2.imwrite("%s/%s/%s%04d.jpg" % (self.out_dir, self.label_dict[self.cur], self.prefix, self.cnt), roi)
            self.cnt = self.cnt + 1
            print(self.cnt)
        elif event == cv2.EVENT_FLAG_RBUTTON:  # right click
            self.nextDir()

    def crop(self):
        cv2.namedWindow(self.title)
        cv2.setMouseCallback(self.title, self.mouseInterrupt)
        while True:
            cv2.imshow(self.title, self.img)
            if cv2.waitKey(0) == 27:  # 27 is Escape Key value
                break
        cv2.destroyAllWindows()

    def __init__(self, src, out, prefix):
        self.out_dir = out
        self.prefix = prefix
        self.img = cv2.imread(src)
        self.cur = 0
        self.cnt = 0
        self.title = "image: %s , output:%s" % (src, out)
        if not os.path.isdir(self.out_dir):
            os.mkdir(self.out_dir, 0o755)

    def setLabels(self, labels):
        self.label_dict = labels
        for d in labels:
            # check if dir exists, mkdir if not
            if not os.path.isdir(self.out_dir + "/%s" % d):
                # permission denied error, use mode 0755 or 0770
                # newer python will need 0oxxx notation mode
                os.mkdir(os.path.join(self.out_dir, str(d)), 0o755)


if __name__ == '__main__':
    if CMDLINE:
        if len(sys.argv) < 3:
            print('usage: {} <sourceImageDir> <outputDir> [<outputPrefix>]'.format(sys.argv[0]))
            print("e.g. : python imCrop.py myimage.jpg ./output 'image_'".format(sys.argv[0]))
            sys.exit(0)

        src = sys.argv[1]
        out_dir = sys.argv[2]
        out_prefix = sys.argv[3] if len(sys.argv) == 4 else "image_"
    else:
        # TODO change parameters here if using IDE
        src = "./src/zhiyun-hw.jpg"
        out_dir = "./sub"
        out_prefix = "image_"

    labels = ['a', 'b', 'c', 'd', 'h', 'i', 'j', 'k']
    gen = DataGenerate(src, out_dir, out_prefix)
    gen.setLabels(labels)
    gen.crop()
