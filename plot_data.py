import matplotlib.pyplot as plt
import numpy as np


def main():
  # get the information as a dictionary
  s = open('data.txt', 'r').read()
  data = eval(s)

  data_keys_sorted = data.keys()
  data_keys_sorted.sort()

  # Plot 1
  plt.figure(1)
  fig_1_x = data_keys_sorted
  fig_1_y = [data[i]['block_rate'][-1] for i in data_keys_sorted]

  plt.plot(fig_1_x, fig_1_y, 'o-')
  #plt.title('Maximum Block Rate vs. Number of Peers')
  plt.xlabel('Number of Peers')
  plt.ylabel('Maximum Block Rate')


  # Plot 2
  plt.figure(2)
  fig_2_x_25 = data[25]['block_rate']
  fig_2_y_25 = data[25]['time_to_consistency']
  fig_2_x_50 = data[50]['block_rate']
  fig_2_y_50 = data[50]['time_to_consistency']
  fig_2_x_75 = data[75]['block_rate']
  fig_2_y_75 = data[75]['time_to_consistency']
  fig_2_x_100 = data[100]['block_rate']
  fig_2_y_100 = data[100]['time_to_consistency']
  fig_2_x_125 = data[125]['block_rate']
  fig_2_y_125 = data[125]['time_to_consistency']
  fig_2_x_150 = data[150]['block_rate']
  fig_2_y_150 = data[150]['time_to_consistency']
  fig_2_x_175 = data[175]['block_rate']
  fig_2_y_175 = data[175]['time_to_consistency']
  fig_2_x_200 = data[200]['block_rate']
  fig_2_y_200 = data[200]['time_to_consistency']

  plt.plot(#fig_2_x_25, fig_2_y_25, 'o-',
           fig_2_x_50, fig_2_y_50, 'o-', label='N = 50')
           #fig_2_x_75, fig_2_y_75, 'o-',
  plt.plot(fig_2_x_100, fig_2_y_100, 'o-', label='N = 100')
           #fig_2_x_125, fig_2_y_125, 'o-',
  plt.plot(fig_2_x_150, fig_2_y_150, 'o-', label='N = 150')
           #fig_2_x_175, fig_2_y_175, 'o-',
  plt.plot(fig_2_x_200, fig_2_y_200, 'o-', label='N = 200')

  plt.xlabel('Block Rate')
  plt.ylabel('Mean Time to Consistency')
  plt.legend()


  # Plot 3
  plt.figure(3)
  fig_3_x_25 = data[25]['block_rate']
  fig_3_y_25 = data[25]['num_blocks_behind']
  fig_3_x_50 = data[50]['block_rate']
  fig_3_y_50 = data[50]['num_blocks_behind']
  fig_3_x_75 = data[75]['block_rate']
  fig_3_y_75 = data[75]['num_blocks_behind']
  fig_3_x_100 = data[100]['block_rate']
  fig_3_y_100 = data[100]['num_blocks_behind']
  fig_3_x_125 = data[125]['block_rate']
  fig_3_y_125 = data[125]['num_blocks_behind']
  fig_3_x_150 = data[150]['block_rate']
  fig_3_y_150 = data[150]['num_blocks_behind']
  fig_3_x_175 = data[175]['block_rate']
  fig_3_y_175 = data[175]['num_blocks_behind']
  fig_3_x_200 = data[200]['block_rate']
  fig_3_y_200 = data[200]['num_blocks_behind']

  plt.plot(#fig_3_x_25, fig_3_y_25, 'o-',
           fig_3_x_50, fig_3_y_50, 'o-', label='N = 50')
           #fig_3_x_75, fig_3_y_75, 'o-',
  plt.plot(fig_3_x_100, fig_3_y_100, 'o-', label='N = 100')
           #fig_3_x_125, fig_3_y_125, 'o-',
  plt.plot(fig_3_x_150, fig_3_y_150, 'o-', label='N = 150')
           #fig_3_x_175, fig_3_y_175, 'o-',
  plt.plot(fig_3_x_200, fig_3_y_200, 'o-', label='N = 200')
 
  plt.xlabel('Block Rate')
  plt.ylabel('Mean Number of Blocks Behind')
  plt.legend()


  # Plot 4
  plt.figure(4)
  fig_4_x_25 = data[25]['block_rate']
  fig_4_y_25 = data[25]['frac_consistent']
  fig_4_x_50 = data[50]['block_rate']
  fig_4_y_50 = data[50]['frac_consistent']
  fig_4_x_75 = data[75]['block_rate']
  fig_4_y_75 = data[75]['frac_consistent']
  fig_4_x_100 = data[100]['block_rate']
  fig_4_y_100 = data[100]['frac_consistent']
  fig_4_x_125 = data[125]['block_rate']
  fig_4_y_125 = data[125]['frac_consistent']
  fig_4_x_150 = data[150]['block_rate']
  fig_4_y_150 = data[150]['frac_consistent']
  fig_4_x_175 = data[175]['block_rate']
  fig_4_y_175 = data[175]['frac_consistent']
  fig_4_x_200 = data[200]['block_rate']
  fig_4_y_200 = data[200]['frac_consistent']

  plt.plot(#fig_4_x_25, fig_4_y_25, 'o-',
           fig_4_x_50, fig_4_y_50, 'o-', label='N = 50')
           #fig_4_x_75, fig_4_y_75, 'o-',
  plt.plot(fig_4_x_100, fig_4_y_100, 'o-', label='N = 100')
           #fig_4_x_125, fig_4_y_125, 'o-',
  plt.plot(fig_4_x_150, fig_4_y_150, 'o-', label='N = 150')
           #fig_4_x_175, fig_4_y_175, 'o-',
  plt.plot(fig_4_x_200, fig_4_y_200, 'o-', label='N = 200')

  plt.xlabel('Block Rate')
  plt.ylabel('Mean Fraction of Peers Consistent')
  plt.legend()

  plt.show()

if __name__=='__main__':
  main()

