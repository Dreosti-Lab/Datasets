import os
import numpy as np
from PIL import Image

# Specify line and scale values
# line_name = 'CRH'
# baseline = -0.42
# scale = 14.32

# line_name = 'DAPI'
# baseline = 0.0
# scale = 12000

line_name = 'POMCA'
baseline = -8
scale = 3

# line_name = 'DLX5A'
# baseline = -0.05
# scale = 10.89

# line_name = 'GALN'
# baseline = 0.25
# scale = 15.00

# line_name = 'OXT'
# baseline = 0.06
# scale = 43.41

# line_name = 'SLC6A4B'
# baseline = -0.03
# scale = 8.17

# line_name = 'TH1'
# baseline = 1.24
# scale = 15.32

# line_name = 'TH2'
# baseline = 1.11
# scale = 3.5

# line_name = 'VACHT'
# baseline = -0.59
# scale = 40.26

# line_name = 'CHAT1A'
# baseline = -0.56
# scale = 15.43

# line_name = 'SST1'
# baseline = -0.43
# scale = 49.23

# Build paths
base_folder = 'S:/WIBR_Dreosti_Lab/Alizee/LSZ1/Registration/Analysis/Website_Stacks/512'
stack_path = base_folder + '/'+ line_name + '/POMCA.tif'
mask_path = base_folder + '/masks/' + 'DAPI' + '.tif'
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