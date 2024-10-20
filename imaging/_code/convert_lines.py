import os
import numpy as np
from PIL import Image

# # Specify line and scale values
# line_name = 'CRH'
# baseline = -0.42
# scale = 14.32

# line_name = 'DAPI'
# baseline = 0.0
# scale = 12000

# line_name = 'POMCA'
# baseline = -8
# scale = 3

# line_name = 'DAT'
# baseline = -0.10
# scale = 12

# line_name = 'GALN'
# baseline = 0
# scale = 15.2

# line_name = 'DLX5A'
# baseline = 1
# scale = 13

# line_name = 'CB1'
# baseline = 0.8
# scale = 2

# line_name = 'AVP'
# baseline = 1
# scale = 15

# line_name = 'SLC6A4A'
# baseline = 0.8
# scale = 6

# line_name = 'TH1'
# baseline = 1.24
# scale = 15.32

# line_name = 'TH2'
# baseline = 1.11
# scale = 3.5

# line_name = 'VACHTB'
# baseline = -0.59
# scale = 40.26

# line_name = 'CHAT1A'
# baseline = -0.56
# scale = 15.43

# line_name = 'SST1'
# baseline = -0.43
# scale = 49.23

# line_name = 'HDC'
# baseline = 1.2
# scale = 2

# line_name = 'KISS1'
# baseline = 1.2
# scale = 2

# line_name = 'NPY'
# baseline = 0
# scale = 16

# line_name = 'OXT'
# baseline = 0
# scale = 50

# line_name = 'OTPB'
# baseline = 1.5
# scale = 4

line_name = 'ARX'
baseline = 0.5
scale = 8

line_name = 'ISL1'
baseline = 0.5
scale = 15

line_name = 'TAC1'
baseline = 0.5
scale = 15

line_name = 'TAC2A'
baseline = 0.5
scale = 3 


# Build paths
base_folder = '/Volumes/T7/Peptides'
stack_path = base_folder + '/'+ line_name + '/TAC2A_s.tif'
mask_path = base_folder + '/masks/' + 'DAPI_s' + '.tif'
output_folder = '/Users/alizeekastler/Documents/GitHub/Datasets/imaging/lines/' + 'sagittal/' + line_name

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
container = np.zeros((height,width,4), dtype=np.uint8)
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