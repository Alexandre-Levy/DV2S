import cv2
import numpy as np
import os

# create images in images/ folder from lct_1.png to lct_23.png
def create_images_lct():
    for i in range(1, 24):
        img = np.zeros((100, 100, 3), dtype="uint8")
        cv2.putText(img, f"LCT {i}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        # write with two digits
        cv2.imwrite(f"images/lct_{i:02d}.png", img)

# create images in images/ folder from chatscene_1.png to chatscene_23.png
def create_images_chatscene():
    for i in range(1, 24):
        img = np.zeros((100, 100, 3), dtype="uint8")
        cv2.putText(img, f"Cha {i}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        # write with two digits
        cv2.imwrite(f"images/chatscene_{i:02d}.png", img)

# create images in images/ folder from trajectory_1.png to trajectory_23.png
def create_images_trajectory():
    for i in range(1, 24):
        img = np.zeros((100, 100, 3), dtype="uint8")
        cv2.putText(img, f"Tra {i}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        # write with two digits
        cv2.imwrite(f"images/trajectory_{i:02d}.png", img)

create_images_lct()
create_images_chatscene()
create_images_trajectory()


