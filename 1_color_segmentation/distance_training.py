import math
import numpy as np
import re

# load coordinates
all_roi_coordinates = np.load('all_roi_coordinates.npy')
# dist_indices = [11,14,18,8]
dist_indices = [1,5,6,8]

# estimate the distance of the cone / learn the focal length

def distance(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def find_cone_height(coords):
    # identify shortest side of the triangle, base side -> identify the 2 points associated with this, and the third point
    side_lengths = [distance(coords[i], coords[(i+1) % 3]) for i in range(3)]
    shortest_index = side_lengths.index(min(side_lengths))
    end1 = coords[shortest_index]
    end2 = coords[(shortest_index + 1) % 3]    
    midpoint = ((end1[0] + end2[0]) / 2, (end1[1] + end2[1]) / 2)     # take midpiont of base
    # estimate height, by taking distance from 3rd point to the midpoint of base
    remaining_index = [i for i in range(3) if i != shortest_index][0]
    remaining_coord = coords[remaining_index]  
    cone_height = distance(midpoint, remaining_coord)
    print('end1: {}, end2: {}, midpoint: {}, apex: {}, height: {}'.format(end1,end2,midpoint,remaining_coord, cone_height))
    return cone_height

# def y_coordinate_difference(point1, point2, point3):
def find_cone_height_2(coords):
    point1 = coords[0]
    point2 = coords[1]
    point3 = coords[2]
    print('point1 {} point2 {}, point3 {}'.format(point1,point2,point3))
    # Calculate the absolute differences in x-coordinates
    delta_x1 = abs(point3[0] - point1[0])
    delta_x2 = abs(point3[0] - point2[0])

    # Determine which point is closer to point3 horizontally
    if delta_x1 < delta_x2:
        # Point1 is closer
        return abs(point3[1] - point1[1])
    else:
        # Point2 is closer
        return abs(point3[1] - point2[1])

def extract_distance_from_filename(filename):
    match = re.search(r'dist(\d+)', filename)
    if match:
        return int(match.group(1))
    else:
        return None

actual_cone_height_given = 17 / 12.0 # define actual height of cone (in feet)


all_focal_lengths = []

# holdoutindices = np.load('holdout_indices_array.npy')

file_path = "file_names_sorted.txt"
filenamessorted = []
with open(file_path, "r") as file:
    for line in file:
        filenamessorted.append(line.strip())

for i in range(len(filenamessorted)):
    if i  in dist_indices:
        # index = holdoutindices[i]
        cur_file = filenamessorted[i]
        print(cur_file)
        image_path = 'training_images/' + cur_file

        roi_coordinates_array = all_roi_coordinates[i]

        actual_distance_of_cone = extract_distance_from_filename(image_path) # define the distance of the cone from camera, file name is image_path here right now
        # print("Given distance of cone: {}".format(actual_distance_of_cone))
        # cone_height_in_pixels = find_cone_height(roi_coordinates_array) # measured / calculated height of cone in pixels in the image
        # print("Cone height in pixels: {}".format(cone_height_in_pixels))
        cone_height_in_pixels = find_cone_height_2(roi_coordinates_array)

        # actual_height / distance = pixel_height / focal length in pixels
        estimated_focal_length_in_pixels = cone_height_in_pixels * actual_distance_of_cone  / actual_cone_height_given
        print("distance: {}, height: {}, estimated focal length: {}".format(actual_distance_of_cone,cone_height_in_pixels,estimated_focal_length_in_pixels))
        all_focal_lengths.append(estimated_focal_length_in_pixels)

all_focal_lengths_array = np.array(all_focal_lengths)
estimated_final_focal_length = np.mean(all_focal_lengths_array)
print('estimated focal lengths {}'.format(all_focal_lengths))
print('mean focal length: {}, stddev {}'.format(estimated_final_focal_length, np.std(all_focal_lengths_array)))

# np.save('estimated_final_focal_length.npy', estimated_final_focal_length)
