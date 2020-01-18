import cv2
import numpy as np
 
paths = ["CAT_00/00000442_015.jpg"]
results = {}

if __name__ == '__main__' :
 
    for path in paths:
        # Read image
        im = cv2.imread(path)

        # Select ROI
        r = cv2.selectROI(im)
        top = r[0]
        left = r[1]
        width = r[2]
        height = r[3]

        results.update({path: {"top": top, "left": left, "width": width, "height": height}})

print(results)

    # Crop image
    # imCrop = im[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]

    # Display cropped image
    # cv2.imshow("Image", imCrop)
    # cv2.waitKey(0)
