import numpy as np

# load all orange pixels
allorangepixels = np.load('all_orange_pixels.npy')

file_path = 'total_num_pixels.txt'
with open(file_path,"r") as file:
    totalnumpixels = int(file.read())
print("total number of pixels: {}".format(totalnumpixels))

def calc_single_gauss_params(pixels):
    class_mean = np.mean(pixels, axis=0)
    class_cov = np.cov(pixels, rowvar = False)

    class_cov_det = np.linalg.det(class_cov)
    class_cov_inv = np.linalg.inv(class_cov)

    print('mean \n {}'.format(class_mean))
    print('covariance \n {}'.format(class_cov))
    print('det: \n {}'.format(class_cov_det))
    print('inv \n {}'.format(class_cov_inv))

    return class_mean, class_cov, class_cov_det, class_cov_inv

mean_orange_cone_rgb, cov_orange_cone_rgb, cov_det_orange_cone_rgb, cov_inv_orange_cone_rgb = calc_single_gauss_params(allorangepixels)

prior_orange_cone = len(allorangepixels[0]) / totalnumpixels

file_path = 'prior_orange_cone.txt'
with open(file_path, "w") as file:
    file.write(str(prior_orange_cone))

np.save('mean_orange_cone_rgb.npy', mean_orange_cone_rgb)
np.save('cov_orange_cone_rgb.npy', cov_orange_cone_rgb)

# file_path = 'mean_orange_cone_rgb.txt'
# with open(file_path, "w") as file:
#     file.write(str(mean_orange_cone_rgb))

# file_path = 'cov_orange_cone_rgb.txt'
# with open(file_path, "w") as file:
#     file.write(str(cov_orange_cone_rgb))

# file_path = 'cov_det_orange_cone_rgb.txt'
# with open(file_path, "w") as file:
#     file.write(str(cov_det_orange_cone_rgb))

# file_path = 'cov_inv_orange_cone_rgb.txt'
# with open(file_path, "w") as file:
#     file.write(str(cov_inv_orange_cone_rgb))
