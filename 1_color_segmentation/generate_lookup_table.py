import numpy as np

mean_oc_rgb = np.load('mean_orange_cone_rgb.npy')
cov_oc_rgb = np.load('cov_orange_cone_rgb.npy')

# Define the step size for sampling the RGB space
STEP_SIZE = 5

def multivariate_gaussian_pdf(x, mean, cov_matrix):
    n = 3
    cov_det = np.linalg.det(cov_matrix)
    cov_inv = np.linalg.inv(cov_matrix)
    constant = np.sqrt(cov_det * (2 * np.pi)**n)
    constant = 1.0 / constant
    x_minus_mean = x - mean
    exponent = -0.5 * x_minus_mean.T @ cov_inv @ x_minus_mean
    return constant * np.exp(exponent)

# Precompute PDF values for sampled RGB vectors and store them in the lookup table
def precompute_lookup_table(step_size, mean_oc_rgb,cov_oc_rgb):
    lookup_table = {}

    for r in range(0, 256, step_size):
        for g in range(0, 256, step_size):
            for b in range(0, 256, step_size):
                rgb_vector = np.array([r, g, b])
                pdf = multivariate_gaussian_pdf(rgb_vector, mean_oc_rgb, cov_oc_rgb)
                lookup_table[tuple(rgb_vector)] = pdf
    return lookup_table

# Call the precompute function
lookup_table_rgb = precompute_lookup_table(STEP_SIZE, mean_oc_rgb, cov_oc_rgb)

np.save('lookup_table_rgb.npy', lookup_table_rgb)

