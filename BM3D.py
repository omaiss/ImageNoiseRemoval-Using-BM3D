# import needed libraries
import bm3d
import time
from skimage.util import img_as_float
import cv2
import numpy


# implementation of bm3d_algorithm
def bm3d_algorithm(filepath, filename):
    start_time = time.time()
    # read the image using cv2.imread
    read_image = cv2.imread(filepath)
    # if the image file is not found then print an error message to the console
    if read_image is None:
        print("Error: Failed to load the image")
        # Return nothing so that the server will also display the error
        return None
    print('Read the image...')
    # if the image size if greater than 1500*1000 pixels reformat it so that
    # it's visible on the screen
    if read_image.shape[0] > 1000 or read_image.shape[1] > 1500:
        print('Image dimensions exceed 1280*720. Resizing...')
        # resize the image to 1300*800
        read_image = cv2.resize(read_image, (1280, 720))
    # convert the read image to img float which means a float range between 0 and 1
    img_float = img_as_float(read_image)
    print('Processing image using BM3D...')
    # using the bm3d algorithm to denoise the image
    denoised_img = bm3d.bm3d(img_float, sigma_psd=0.2, stage_arg=bm3d.BM3DStages.ALL_STAGES)

    final_img_path = 'static/results/' + filename
    # save the image to the path after converting it back to the range of 0~255
    # so that it is coloured
    if not cv2.imwrite(final_img_path, denoised_img * 255):
        print("Error: Failed to save the denoised image")
        return None
    print('Saved the denoised image:', final_img_path)
    print('saved all images...ending algorithm run....execution time will now be shown')
    # get the current time as end time
    end_time = time.time()
    total_time = end_time - start_time
    # total time taken by the algorithm to execute
    print("Execution time: {:.5f} seconds".format(total_time))
    return final_img_path
