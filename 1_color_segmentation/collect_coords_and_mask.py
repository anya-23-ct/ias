from roipoly import RoiPoly
from matplotlib import pyplot as plt
import cv2
import numpy as np
import os

folder_path = 'training_images'
file_names = os.listdir(folder_path)
file_names_sorted = sorted(file_names, key=lambda x: int(x.split('_')[1]))

# File path to store the list of file names
file_path = "file_names_sorted.txt"

# Write the list of file names to the text file
with open(file_path, "w") as file:
    for i in range(len(file_names_sorted)):
        file.write(file_names_sorted[i] + "\n")

# master arrays for all roi coordinates and all roi masks
all_roi_coordinates = []
all_roi_masks = []
all_orange_pixels = np.empty((0, 3))
# print('type all_orange_pixels {}'.format(type(all_orange_pixels)))

# holdout_indices = [20,16,9,3]

# for i in range(2):
for i in range(len(file_names_sorted)):
    # if i not in holdout_indices:

    cur_file = file_names_sorted[i]
    print(cur_file)
    image_path = 'training_images/' + cur_file
    orig_image = cv2.imread(image_path)
    image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB) # default out cv2.imread is BGR, so converting to RGB
    plt.imshow(image)

    my_roi = RoiPoly(color=(0, 1, 0))
    plt.figure()
    plt.imshow(image)
    my_roi.display_roi()
    base_name, extension = os.path.splitext(cur_file)
    file_name = base_name + '_with_roi' + extension
    plt.savefig(file_name)
    plt.close()

    roi_coordinates = my_roi.get_roi_coordinates()
    print('roi_coordinates {}'.format(roi_coordinates))
    all_roi_coordinates.append(roi_coordinates)

    roi_mask = my_roi.get_mask(image[:, :, 0]) # extract pixel list in the cone; same pixel list for all channels in RGB
    all_roi_masks.append(roi_mask)

    cur_orange_pixels = image[roi_mask]
    cur_pixels_file_name = base_name + '_orange_pixels' + '.npy'
    np.save(cur_pixels_file_name, cur_orange_pixels)
    # print('type cur_orange_pixels {}'.format(type(cur_orange_pixels)))
    # print(cur_orange_pixels.shape)

    # all_orange_pixels = np.concatenate((all_orange_pixels,cur_orange_pixels),axis=0)

all_roi_coordinates_array = np.array(all_roi_coordinates)
all_roi_masks_array = np.array(all_roi_masks)

print('array dimensions \n all_roi_coordinates_array {} \n all_roi_masks_array {} \n all_orange_pixels {}'.format(all_roi_coordinates_array.shape,all_roi_masks_array.shape,all_orange_pixels.shape ))
# print('all orange pixels samples {}'.format(all_orange_pixels[:5]))

np.save('all_roi_coordinates.npy', all_roi_coordinates_array)
np.save('all_roi_masks.npy', all_roi_masks_array)
# np.save('all_orange_pixels.npy', all_orange_pixels)