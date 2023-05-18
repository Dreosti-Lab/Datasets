import os
import numpy as np
from PIL import Image, ImageFilter

# Specify mask
#mask_name = 'cH'
#mask_name = 'Habenula'
#mask_name = 'OB'
#mask_name = 'DL'
#mask_name = 'PGZ'
#mask_name = 'PoA'
#mask_name = 'PT'
mask_name = 'vHb'

# Build paths
base_folder =  'S:/WIBR_Dreosti_Lab/Alizee/LSZ1/Registration/Analysis/Website_Stacks/512/'
stack_path = base_folder + 'masks/' + mask_name + '.tif'
output_folder = base_folder + '/processed/masks/' + mask_name

# Create output folder (if it does not exist)
if not os.path.exists(output_folder):
   os.makedirs(output_folder)

# Load mask stack
mask_data = Image.open(stack_path)
height, width = np.shape(mask_data)
num_frames = mask_data.n_frames

# Convert raw TIFF to PNG with alpha layers
container = np.zeros((width,height,4), dtype=np.uint8)
for i in range(num_frames):
    mask_data.seek(i)
    gray = mask_data.convert('L')
    gray = gray.point(lambda i: i * 255) # Convert values from 0-1 to 0-255
    edges = gray.filter(ImageFilter.FIND_EDGES)
    smoothed = edges.filter(ImageFilter.SMOOTH)
    smoothed = smoothed.point(lambda i: i * 2) # Enhance smoothed values
    mask = np.array(smoothed)
    container[:,:,1] = mask
    container[:,:,3] = mask
    output = Image.fromarray(container)
    path = output_folder + '/' + mask_name + str(i).zfill(4) + '.png'
    mask_data.save(path)
    output.save(path)
# FIN