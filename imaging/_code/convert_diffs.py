import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import cv2 

# Specify diff name, basediff, and scale values
diff_name = 'Diff_Stack'
baseline = 0.06
pos_scale = 0.8
neg_scale = 0.8

# Build paths
base_folder = 'S:/WIBR_Dreosti_Lab/Alizee/LSZ1/Registration'
stack_path = base_folder + '/Analysis/SOCIAL/512_2/'+ diff_name + '.tif'
mask_path = base_folder + '/mask/DAPI_512_2_MASK.tif'
pos_output_folder = base_folder + '/Analysis/SOCIAL/512_2/' + diff_name + '_pos'
neg_output_folder = base_folder + '/Analysis/SOCIAL/512_2/' + diff_name + '_neg'

output_folder = base_folder + '/Analysis/SOCIAL/512_2/' + diff_name + '_both'
# Create output folders (if they do not exist)
if not os.path.exists(pos_output_folder):
   os.makedirs(pos_output_folder)
if not os.path.exists(neg_output_folder):
   os.makedirs(neg_output_folder)

# Load diff stack
diff_data = Image.open(stack_path)
height, width = np.shape(diff_data)
num_frames = diff_data.n_frames

# Load mask stack
mask_data = Image.open(mask_path)

# Convert raw TIFF to PNG with alpha layers
container = np.zeros((width,height,4), dtype=np.uint8)
pos_container = np.zeros((width,height,4), dtype=np.uint8)
neg_container = np.zeros((width,height,4), dtype=np.uint8)
for i in range(num_frames):
    diff_data.seek(i)
    mask_data.seek(i)
    data = np.asarray(diff_data) * np.asarray(mask_data)
    pos_rescaled = np.clip(((data - baseline) / pos_scale) * 255.0, 0, 255)
    neg_rescaled = np.clip(((data - baseline) / -neg_scale) * 255.0, 0, 255)
    pos_integer = pos_rescaled.astype(np.uint8)
    neg_integer = neg_rescaled.astype(np.uint8)
    
    pos_container[:,:,2] = pos_integer
    pos_container[:,:,3] = pos_integer
    
    neg_container[:,:,0] = neg_integer
    neg_container[:,:,3] = neg_integer
    
    neg_integer = cv2.blur(neg_integer, (7,7), 0)
    pos_integer = cv2.blur(pos_integer, (7,7), 0)
    
    pos_output = Image.fromarray(pos_container)
    neg_output = Image.fromarray(neg_container)
    
    pos_path = pos_output_folder + '/' + diff_name + str(i).zfill(4) + '.png'
    neg_path = neg_output_folder + '/' + diff_name + str(i).zfill(4) + '.png'

    pos_output.save(pos_path)
    neg_output.save(neg_path)
    
    #------------------------------------------------------------------------------

    # container[:,:,2] = pos_integer
    # #container[:,:,3] = pos_integer
    
    # container[:,:,0] = neg_integer
    # container[:,:,3] = neg_integer
     
    # output = Image.fromarray(container)
    
    # output_path = output_folder + '/' + diff_name + str(i).zfill(4) + '.png'
    # output.save(output_path)

# FIN