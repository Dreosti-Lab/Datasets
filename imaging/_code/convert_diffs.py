import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# Specify diff name, basediff, and scale values
diff_name = 'DIFF_Noxious'
baseline = 0.06
scale = 1.25

# Build paths
base_folder = '/home/kampff/data/Dropbox/Adam_Ele/Website_Stacks'
stack_path = base_folder + '/unprocessed/diffs/'+ diff_name + '.tif'
mask_path = base_folder + '/unprocessed/masks/DAPI_MASK.tif'
pos_output_folder = base_folder + '/processed/' + diff_name + '_pos'
neg_output_folder = base_folder + '/processed/' + diff_name + '_neg'

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
pos_container = np.zeros((width,height,4), dtype=np.uint8)
neg_container = np.zeros((width,height,4), dtype=np.uint8)
for i in range(num_frames):
    diff_data.seek(i)
    mask_data.seek(i)
    data = np.asarray(diff_data) * np.asarray(mask_data)
    pos_rescaled = np.clip(((data - baseline) / scale) * 255.0, 0, 255)
    neg_rescaled = np.clip(((data + baseline) / -scale) * 255.0, 0, 255)
    pos_integer = pos_rescaled.astype(np.uint8)
    neg_integer = neg_rescaled.astype(np.uint8)
    
    pos_container[:,:,2] = pos_integer
    pos_container[:,:,3] = pos_integer
    
    neg_container[:,:,0] = neg_integer
    neg_container[:,:,3] = neg_integer
    
    pos_output = Image.fromarray(pos_container)
    neg_output = Image.fromarray(neg_container)

    pos_path = pos_output_folder + '/' + diff_name + str(i).zfill(4) + '.png'
    neg_path = neg_output_folder + '/' + diff_name + str(i).zfill(4) + '.png'

    pos_output.save(pos_path)
    neg_output.save(neg_path)

# FIN