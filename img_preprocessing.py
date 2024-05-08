# ----------------------------- Packages ------------------------------------------
import cv2 as cv
import numpy as np
import os
import tifffile as tf
import argparse

#----------------------------- Parser ------------------------------------------
parser = argparse.ArgumentParser(prog = 'Image preprocessing',
                    description = 'Convertion ome.tiff image to visible, black and white image of cell from single cell flow')
parser.add_argument('-t', '--target_folder', help = 'Path to the folder with the files to be processed')
parser.add_argument('-ol', '--output_folder_loc', help = 'Path to the location where the output folder will be placed')
parser.add_argument('-on', '--output_folder_name', help = 'Name of the output folder', default = "converted")
parser.add_argument('-l', '--label', help = 'Label of the cell (can be use further for machine learning processes)')
parser.add_argument('-k', '--kernel', help = 'Kernel size', type=int, default = 11)
parser.add_argument('-cs', '--cut_size', help = 'Value for cropping the image relatively to the object on it', type=int, default = 70)
args = vars(parser.parse_args())

# ----------------------------- FUNCTIONS ------------------------------------------

def image_to_uint8(input_image):
    blurred = cv.GaussianBlur(input_image, (7, 7), 0)
    normalized_image = cv.normalize(blurred, None, alpha = 0, beta = 255, norm_type = cv.NORM_MINMAX) # image normalization (range 0-255)
    uint8_image = cv.convertScaleAbs(normalized_image)
    return uint8_image

def uint8_to_masked(uint8_image, kernel_size):
    ret3,thres_img = cv.threshold(uint8_image, 0, 255, cv.THRESH_BINARY+cv.THRESH_OTSU)
    closed_image = cv.morphologyEx(thres_img, cv.MORPH_CLOSE, kernel_size)
    return closed_image

def get_image_contour(closed_image):
    contour = cv.findContours(closed_image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    return contour

def get_mask(closed_image, contour):
    # First found contour is chosen and changed into an array with point coordination
    boundary = np.array(contour[0][0].reshape(-1, 2), dtype=np.int32)
    # The area is filled with white color (255) and masked with area of interest is created
    mask  = cv.fillPoly(closed_image , [boundary], (255))
    return mask

def central_point(mask):
    M = cv.moments(mask)
    # Calculation of centroid
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    return cx, cy

def image_size(closed_image):
    height, width = closed_image.shape
    return height, width 

def image_convertion_to_masked(input_image, mask):
    # Masked input_image (only area defined in mask function)
    masked = cv.bitwise_and(input_image, input_image, mask=mask)
    return masked

# Checking if object (cell) contour is touching an edge of an image 
def check_touching_boundaries(image, contour, height, width):
    touching_edge = False
    for con in contour:
        x, y, w, h = cv.boundingRect(con[0])
        if x <= 0 or (x + w) >= (width - 1) or y <= 0 or (y + h) >= (height - 1):
           return True
        else:
            return False

def trim_image(masked, cx, cy, cut_size):
    x_top_left = max(0, int(cx - args["cut_size"] //2))
    y_top_left = max(0, int(cy - args["cut_size"] //2))
    x_bottom_right = min(masked.shape[1], int(cx + cut_size //2))
    y_bottom_right = min(masked.shape[0], int(cx + cut_size //2))
    trimmed_image = masked[y_top_left:y_bottom_right, x_top_left:x_bottom_right]
    return trimmed_image

def resize_image(trimmed_image, new_height, new_width):
    dim = (new_width, new_height)
    resized_image = cv.resize(trimmed_image, dim, interpolation=cv.INTER_AREA)
    return resized_image

def save_image(image, new_img):
    file_name = os.path.basename(image)
    index = file_name.find("Ch")
    if index != -1:
        end_index = len(file_name)-8
        ch_fragment = file_name[index:end_index]  
    new_folder = os.path.join(args["output_folder_loc"], args["output_folder_name"], f'{ch_fragment}')
    os.makedirs(new_folder, exist_ok = True)
    if args["label"] != None:
        output_path = os.path.join(new_folder, f"{args["label"]}_{file_name}")
    else:
        output_path = os.path.join(new_folder, f"new_{file_name}")
    tf.imsave(output_path, new_img)
    return file_name

# ----------------------------- TEST -----------------------------
kernel_size = np.ones((args["kernel"],args["kernel"]), np.uint8)
normalized_paths = [os.path.normpath(file) for file in args["target_folder"]]
image_files = [os.path.join(args["target_folder"], file) for file in os.listdir(args["target_folder"]) if file.endswith('.tif')]

for image in image_files:
    errors = 0
    input_image = tf.imread(image)
    uint8_image = image_to_uint8(input_image)
    closed_image = uint8_to_masked(uint8_image, kernel_size)
    contour = get_image_contour(closed_image)
    mask = get_mask(closed_image, contour)
    cx, cy = central_point(mask)
    height, width = image_size(closed_image)
    masked_image = image_convertion_to_masked(input_image, mask) # to visualise photos input_image -> uint8_image
    if check_touching_boundaries(masked_image, contour, height, width): 
        continue
    trimmed_image = trim_image(masked_image, cx, cy, args["cut_size"])
    resized_image = resize_image(trimmed_image, args["cut_size"], args["cut_size"])
    file_name = save_image(image, resized_image)
    print(file_name)

# py .\img_preprocessing.py -t "C:\Users\Lenovo\Desktop\PCvsnonPC\nonPC\sca71" -ol "C:\Users\Lenovo\Desktop\PCvsnonPC" -on "nonpc_sca71" -l "nonpc" 


