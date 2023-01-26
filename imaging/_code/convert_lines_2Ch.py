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

# line_name = 'OXT'
# baselines = 0.02
# scales = 44.91

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
stack_paths = [base_folder + '/OXT/Mean_OXT_n3.tif',base_folder + '/DLX5A/Mean_DLX5A_n3.tif']
mask_path = base_folder + '/masks/DAPI_MASK.tif'
output_folder = base_folder + '/processed'

baselines = [0.02,-0.09]
scales = [44.91,8.19]

# Create output folder (if it does not exist)
if not os.path.exists(output_folder):
   os.makedirs(output_folder)


# Load mask stack
mask_data = Image.open(mask_path)

line_data = Image.open(stack_paths[0]) # N.B. both images should have the same number of frames!!!
height, width = np.shape(line_data)
num_frames = line_data.n_frames
    
container = np.zeros((width,height,4), dtype=np.uint8)
# Convert raw TIFF to PNG with alpha layers
for i in range(num_frames):
    temp=[]
    for ch in range(len(baselines)):

        # Load line stack
        line_data = Image.open(stack_paths[ch])
        height, width = np.shape(line_data)

        baseline=baselines[ch]
        scale=scales[ch]

        line_data.seek(i)
        mask_data.seek(i)
        data = np.asarray(line_data) * np.asarray(mask_data)
        rescaled = np.clip(((data - baseline) / scale) * 255.0, 0, 255)
        integer = rescaled.astype(np.uint8)
        
        temp.append(integer)
        if ch==0:    
            container[:,:,0] = integer
        elif ch==1:
            container[:,:,2] = integer
            
    temp_av=np.mean(temp,axis=0) 
    container[:,:,3] = temp_av       
    output = Image.fromarray(container)
    
    path = output_folder + '/OXT_DLX_av/processed_' + str(i).zfill(4) + '.png'
    output.save(path)
#FIN