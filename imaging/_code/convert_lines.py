import os
import numpy as np
from PIL import Image

# Specify line and scale values
#line_name = 'CRH'
#baseline = -0.42
#scale = 14.32

#line_name = 'DAPI'
#baseline = 0.0
#scale = 9553.0

#line_name = 'DLX5A'
#baseline = -0.09
#scale = 8.19

#line_name = 'GALN'
#baseline = 0.25
#scale = 15.00

line_name = 'OXT'
baseline = 0.02
scale = 44.91

#line_name = 'SLC6A4B'
#baseline = 1.00
#scale = 10.05

#line_name = 'TH1'
#baseline = 1.02
#scale = 25.09

#line_name = 'TH2'
#baseline = 0.77
#scale = 3.30

#line_name = 'VACHT'
#baseline = -0.45
#scale = 39.75

# Build paths
base_folder = 'S:/WIBR_Dreosti_Lab/Alizee/LSZ1/Registration/Analysis/Website_Stacks'
stack_path = base_folder + '/'+ line_name + '/Mean_OXT_n3.tif'
mask_path = base_folder + '/masks/' + 'DAPI' + '_MASK.tif'
output_folder = base_folder + '/processed/' + line_name

# Create output folder (if it does not exist)
if not os.path.exists(output_folder):
   os.makedirs(output_folder)

# Load line stack
line_data = Image.open(stack_path)
height, width = np.shape(line_data)
num_frames = line_data.n_frames

# Load mask stack
mask_data = Image.open(mask_path)

# Convert raw TIFF to PNG with alpha layers
container = np.zeros((width,height,4), dtype=np.uint8)
for i in range(num_frames):
    line_data.seek(i)
    mask_data.seek(i)
    data = np.asarray(line_data) * np.asarray(mask_data)
    rescaled = np.clip(((data - baseline) / scale) * 255.0, 0, 255)
    integer = rescaled.astype(np.uint8)
    if line_name == 'DAPI':
        container[:,:,0] = integer
        output = Image.fromarray(container[:,:,0])    
    else:
        container[:,:,0] = integer
        container[:,:,3] = integer
        output = Image.fromarray(container)
    path = output_folder + '/' + line_name + str(i).zfill(4) + '.png'
    output.save(path)

# FIN