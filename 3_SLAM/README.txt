Please place the test data in the folder 'ECE5242Proj3-test/', or update the google drive mount folder to the folder containing the data
Please do ensure that the load_data and MapUtils are in the appropriate folder to load from as well

These below are sample commands for new test dataset, using the example of test dataset 4.


Load data:
FL_4, FR_4, RL_4, RR_4, ts_enc_4 = ld.get_encoder(encoder_files[4])
lidar_4 = ld.get_lidar(lidar_files[4])

Processing:
lidar_timestamps_consolidated_4 = np.array([lidar_4[i]['t'] for i in range(len(lidar_4))]),
matched_lidar_indices_4 = match_lidar_indices_to_encoder(ts_enc_4,lidar_timestamps_consolidated_4)

Set odometry parameters dictionary:
(only update the values ending in the number _4)

params_odom_4 = {
    'FL': FL_4,
    'FR': FR_4,
    'RL': RL_4,
    'RR': RR_4,
    'ts_enc': ts_enc_4,
    'encoder_ticks_to_meters': encoder_ticks_to_meters,
    'width_between_wheels': width_between_wheels,
    'tuning_factor': tuning_factor_4,
    'lidar': lidar_4,
    'matched_lidar_indices': matched_lidar_indices_4,
    'adjust_x': adjust_x,
    'adjust_y': adjust_y,
    'map_cell_size': map_cell_size,
    'maxmap': maxmap,
    'init_map_size': init_map_size,
    'log_odds_for_occupied': log_odds_for_occupied,
    'log_odds_for_empty': log_odds_for_empty,
    'occmap_min_value': occmap_minval,
    'occmap_max_value': occmap_maxval,
    'period': period
}

odometry function call:

occupancymapslist_4_odometry_only, final_occupancymap_4_odometry_only = update_occupancy_map(**params_odom_4)
plot_occupancy_map(final_occupancymap_4_odometry_only)


SLAM function call:
occupancymaps_all_4_good_width = lidar_hits_2(FL_4,FR_4,RL_4,RR_4,ts_enc_4,encoder_ticks_to_meters,width_between_wheels,1.7,lidar_4,matched_lidar_indices_4,adjust_x,adjust_y,map_cell_size,maxmap,init_map_size,log_odds_for_occupied,log_odds_for_empty,num_particles,n_eff_min,noise_covariance,occmap_minval,occmap_maxval)
plot_occupancy_map(occupancymaps_all_4_good_width[-1])