This code contains Python scripts for solving the maze navigation problem using two different approaches: Value Iteration and Q-Learning.

Code Overview:
maze.py: Contains the implementation of the maze environment, including classes for creating the maze, defining actions, and computing rewards.
evaluation.py: Includes functions for evaluating the performance of the algorithms.
ad2258_proj4_submission.ipynb: The main script that executes both Value Iteration and Q-Learning approaches for solving the maze navigation problem. 
	It initializes the maze environment, defines hyperparameters, runs experiments, and plots the results.

Data:
optimal_Q_values.npy: optimal Q values found from value iteration on the maze problem, using discount rate of 0.9
optimal_Q_values_99.npy: same as above, but using discount rate of 0.99

Results Interpretation:
The code generates plots showing the performance metrics (steps, rewards, RMSE) for different hyperparameter settings.
Use the plots to analyze the effectiveness of each approach and hyperparameter combination in solving the maze navigation problem.

