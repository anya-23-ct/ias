import numpy as np
import cv2
import os
from matplotlib import pyplot as plt
import re

threshold_value = 1e-14
min_area_thresh = 300

file_path = 'prior_orange_cone.txt'
with open(file_path,"r") as file:
    priororangecone = float(file.read())
# print("Prior probability of orange cone: {}".format(priororangecone))

# Focal length
focal_length = np.load('estimated_final_focal_length.npy')
# print('Focal length is {}'.format(focal_length))

# Actual cone height
actual_cone_height_given = 17 / 12.0
# print('Actual cone height given: {}'.format(actual_cone_height_given))

lookup_table_rgb = np.load('lookup_table_rgb.npy', allow_pickle=True).item()

def find_nearest_sample(rgb_vector):
    rounded_rgb = [round(component / 5) * 5 for component in rgb_vector]
    return rounded_rgb

def calculate_bayes_probability2(lookup_table,rgb_vector):
    if tuple(rgb_vector) in lookup_table:
        pdf = lookup_table[tuple(rgb_vector)]  
    else:
        closest_rgb_vector = find_nearest_sample(rgb_vector)
        pdf = lookup_table[tuple(closest_rgb_vector)]
    prob_rgb = pdf * priororangecone + (1 - pdf) * (1 - priororangecone)
    prob_bayes = pdf * priororangecone / prob_rgb
    return prob_bayes

def get_bayes_prob(image):
    bayes_prob_per_pixel = np.empty((image.shape[0], image.shape[1]))
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            bayes_prob_per_pixel[i][j] = calculate_bayes_probability2(lookup_table_rgb,image[i,j,:])
    return bayes_prob_per_pixel

def threshold_image(prob_matrix):
    img_threshold_mask = (prob_matrix > threshold_value).astype(np.uint8)
    return img_threshold_mask

def region_processing(curfile, threshold_mask, min_area_threshold, color_image_rgb, figure_save_name, distance, cone_base_coord_x, cone_base_coord_y):
    _, labels = cv2.connectedComponents(threshold_mask)
    # region_count = 0  # Counter to keep track of the number of regions identified
    
    image_with_regions = color_image_rgb.copy()  # Initialize the image with regions
    plt.figure()

    for label in range(1, labels.max() + 1):  # Start from 1 to skip background label 0
        mask = np.uint8(labels == label)
        area = np.sum(mask)

        if area > min_area_threshold:
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                bounding_box = cv2.boundingRect(contour)
                x, y, w, h = bounding_box

                estimated_distance = focal_length * actual_cone_height_given / float(h)
                midpoint_x = x + w // 2
                midpoint_y = y + h

                cv2.rectangle(image_with_regions, (x, y), (x + w, y + h), (0, 255, 0), 2)
                plt.plot(midpoint_x, midpoint_y, 'ro')
                plt.text(midpoint_x, midpoint_y, f'Distance: {estimated_distance:.2f} feet', fontsize=8, color=(0, 1, 0))
                
                image_name.append(curfile)
                distance.append(estimated_distance)
                cone_base_coord_x.append(midpoint_x)
                cone_base_coord_y.append(midpoint_y)

    plt.imshow(image_with_regions)
    plt.title(curfile)
    plt.savefig(figure_save_name)
    # plt.show()
    plt.close()


def generate_results_file(file_path, imagename, distance, cone_base_coord_x, cone_base_coord_y):
    with open(file_path, "w") as file:
        for i in range(len(imagename)):
            formatted_distance = "{:.2f}".format(distance[i])
            result_string = 'ImageName: {} Down: {}, Right: {}, Distance: {}'.format(imagename[i], cone_base_coord_y[i], cone_base_coord_x[i], formatted_distance)
            file.write(result_string + "\n")

# MAIN LOOP
image_name = []
distance = []
cone_base_coord_x = []
cone_base_coord_y = []

def sort_key(filename):
    parts = re.split(r'_(\d+)', filename)  
    num_part = int(parts[1]) if len(parts) > 1 else 0  
    is_test = filename.startswith('test') 
    return (not is_test, num_part)  

folder_path = 'test_images/'
file_names = os.listdir(folder_path)
file_names_sorted = sorted(file_names, key=sort_key)
print('file names sorted:', file_names_sorted)

file_path = "test_file_names_sorted.txt"

with open(file_path, "w") as file:
    for i in range(len(file_names_sorted)):
        file.write(file_names_sorted[i] + "\n")

for i in range(len(file_names_sorted)):
    cur_file = file_names_sorted[i]
    print(cur_file)
    image_path = 'test_images/' + cur_file
    orig_image = cv2.imread(image_path)
    image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB) # default out cv2.imread is BGR, so converting to RGB
    base_name, extension = os.path.splitext(cur_file)
    cur_fig_save_name = 'test_' + base_name + '_final_out.png'
    results_file_path = "results.txt"
    prob_mat = get_bayes_prob(image)
    thresh_img = threshold_image(prob_mat)
    region_processing(cur_file,thresh_img,min_area_thresh,image,cur_fig_save_name,distance,cone_base_coord_x,cone_base_coord_y)

generate_results_file(results_file_path,image_name,distance,cone_base_coord_x,cone_base_coord_y)


