from os import listdir
from os.path import isfile, join
import numpy
import cv2
import bm3d
import time
from skimage.util import img_as_float

# read the images from the folder containing
# mypath = "C:\\Users\\asus\\Desktop\\final_res\\work_data"
mypath = "uploads\\"
only_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
images = numpy.empty(len(only_files), dtype=object)
for n in range(0, len(only_files)):
    images[n] = cv2.imread(join(mypath, only_files[n]))

start_time = time.time()


# body of algorithm BM3D
def bm3d_algorithm(filepath, seg):
    read_image = filepath
    if read_image is None:
        print("Error: Failed to load the image")
        return None
    print('Read the image...')
    if read_image.shape[0] > 1000 or read_image.shape[1] > 1500:
        print('Image dimensions exceed 1500x1000. Resizing...')
        read_image = cv2.resize(read_image, (1300, 800))
    img_float = img_as_float(read_image)
    print('Processing image using BM3D...')
    denoised_img = bm3d.bm3d(img_float, sigma_psd=seg, stage_arg=bm3d.BM3DStages.ALL_STAGES)
    end_time = time.time()
    total_time = end_time - start_time
    print("Execution time: {:.5f} seconds".format(total_time))
    return denoised_img * 255


# Tpe of noise
def poisson(img):
    vals = len(numpy.unique(img))
    vals = 4 ** numpy.ceil(numpy.log2(vals))
    return numpy.random.poisson(img * vals) / float(vals)


def spinkls_noise(img):
    gauss = numpy.random.normal(0, 1, img.size)
    gauss = gauss.reshape(img.shape[0], img.shape[1], img.shape[2]).astype('uint8')
    return cv2.add(img, gauss)


def gauss_noise(img):
    gauss = numpy.random.normal(0, 1, img.size)
    gauss = gauss.reshape(img.shape[0], img.shape[1], img.shape[2]).astype('uint8')
    return img + img * gauss


# Write the optimization value as requested by the user
seg = int(input("enter the scale for the enhancement recommended is 200% : ")) / 1000

# Store the image results after performing noise operations and after the algorithm has finished working
for i in range(0, len(images)):
    # cv2.imwrite(f'C:\\Users\\asus\\Desktop\\final_res\\gauss_noise\\img_{i + 1}.jpeg', gauss_noise(images[i]))
    # cv2.imwrite(f'C:\\Users\\asus\\Desktop\\final_res\\res_data\\img_{i + 1}.jpeg',
    #             bm3d_algorithm(gauss_noise(images[i]), seg))
    print(f'Image {i + 1} out of {len(images)}')
    cv2.imwrite(f'static\\results\\guass\\img_{i + 1}.jpeg', gauss_noise(images[i]))
    cv2.imwrite(f'static\\results\\final_res\\img_{i + 1}.jpeg', bm3d_algorithm(gauss_noise(images[i]), seg))
