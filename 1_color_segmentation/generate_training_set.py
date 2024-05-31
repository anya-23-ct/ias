from roipoly import RoiPoly
from matplotlib import pyplot as plt
import cv2
import numpy as np
import os

folder_path = 'training_images'
file_names = os.listdir(folder_path)
file_names_sorted = sorted(file_names, key=lambda x: int(x.split('_')[1]))

num_files = len(file_names)
holdout_indices = [20,16,9,3]
holdout_indices_array = np.array(holdout_indices)
np.save('holdout_indices_array.npy', holdout_indices_array)

all_roi_masks = np.load('all_roi_masks.npy')
all_orange_pixels = np.empty((0, 3))

# for i in range(2):
for i in range(len(file_names_sorted)):
    if i not in holdout_indices:
        cur_file = file_names_sorted[i]
        print(cur_file)
        image_path = 'training_images/' + cur_file
        orig_image = cv2.imread(image_path)
        image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB) # default out cv2.imread is BGR, so converting to RGB

        #extract cur_mask
        cur_roi_mask = all_roi_masks[i,:,:]
        cur_orange_pixels = image[cur_roi_mask]

        print('type cur_orange_pixels {}'.format(type(cur_orange_pixels)))
        print(cur_orange_pixels.shape)

        all_orange_pixels = np.concatenate((all_orange_pixels,cur_orange_pixels),axis=0)

print('array dimensions \n all_roi_masks_array {} \n all_orange_pixels {}'.format(all_roi_masks.shape,all_orange_pixels.shape ))
# print('all orange pixels samples {}'.format(all_orange_pixels[:5]))

np.save('all_orange_pixels.npy', all_orange_pixels)

num_train_images = num_files - len(holdout_indices)
total_num_pixels = num_train_images * 800* 600

file_path = 'total_num_pixels.txt'
with open(file_path, "w") as file:
    file.write(str(total_num_pixels))
