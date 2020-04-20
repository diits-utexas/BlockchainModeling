import matplotlib.pyplot as plt
import numpy as np

def main():
    infile = open('output_growth.txt', 'r').read()
    data = eval(infile)

    time_to_consistency_10 = data[10]['busy_period']
    cycle_length_10 = data[10]['cycle_length']
    age_of_information_10 = data[10]['age_of_information']
    consistency_fraction_10 = data[10]['consistency_fraction']
    growth_rate_10 = data[10]['growth_rate']
    time_to_consistency_20 = data[20]['busy_period']
    cycle_length_20 = data[20]['cycle_length']
    age_of_information_20 = data[20]['age_of_information']
    consistency_fraction_20 = data[20]['consistency_fraction']
    growth_rate_20 = data[20]['growth_rate']
    time_to_consistency_30 = data[30]['busy_period']
    cycle_length_30 = data[30]['cycle_length']
    age_of_information_30 = data[30]['age_of_information']
    consistency_fraction_30 = data[30]['consistency_fraction']
    growth_rate_30 = data[30]['growth_rate']

    num_data_10 = len(time_to_consistency_10)
    num_data_20 = len(time_to_consistency_20)
    num_data_30 = len(time_to_consistency_30)

    ind_10 = np.sum([cycle_length_10[i][1] < 150 for i in range(num_data_10)])
    ind_20 = np.sum([cycle_length_20[i][1] < 150 for i in range(num_data_20)])
    ind_30 = np.sum([cycle_length_30[i][1] < 150 for i in range(num_data_30)])

    

    plt.figure(1)
    plt.errorbar([time_to_consistency_10[i][0] for i in range(num_data_10)],
                 [time_to_consistency_10[i][1] for i in range(num_data_10)],
                 [2*time_to_consistency_10[i][2] for i in range(num_data_10)], 
                 fmt='o', label='N = 10')
    plt.errorbar([time_to_consistency_20[i][0] for i in range(num_data_20)],
                 [time_to_consistency_20[i][1] for i in range(num_data_20)],
                 [2*time_to_consistency_20[i][2] for i in range(num_data_20)], 
                 fmt='o', label='N = 20')
    plt.errorbar([time_to_consistency_30[i][0] for i in range(num_data_30)],
                 [time_to_consistency_30[i][1] for i in range(num_data_30)],
                 [2*time_to_consistency_30[i][2] for i in range(num_data_30)], 
                 fmt='o', label='N = 30')
    plt.title('Time to Consistency vs. Block Arrival Rate')
    plt.xlabel('Block Arrival Rate (blocks / s)')
    plt.ylabel('Time to Consistency (s)')
    plt.legend()
    
    plt.figure(2)
    plt.errorbar([cycle_length_10[i][0] for i in range(ind_10)],
                 [cycle_length_10[i][1] for i in range(ind_10)],
                 [2*cycle_length_10[i][2] for i in range(ind_10)], 
                 fmt='o', label='N = 10')
    plt.errorbar([cycle_length_20[i][0] for i in range(ind_20)],
                 [cycle_length_20[i][1] for i in range(ind_20)],
                 [2*cycle_length_20[i][2] for i in range(ind_20)], 
                 fmt='o', label='N = 20')
    plt.errorbar([cycle_length_30[i][0] for i in range(ind_30)],
                 [cycle_length_30[i][1] for i in range(ind_30)],
                 [2*cycle_length_30[i][2] for i in range(ind_30)], 
                 fmt='o', label='N = 30')
    plt.title('Cycle Length vs. Block Arrival Rate')
    plt.xlabel('Block Arrival Rate (blocks / s)')
    plt.ylabel('Cycle Length (s)')
    plt.legend()
    
    plt.figure(3)
    plt.errorbar([age_of_information_10[i][0] for i in range(num_data_10)],
                 [age_of_information_10[i][1] for i in range(num_data_10)],
                 [2*age_of_information_10[i][2] for i in range(num_data_10)], 
                 fmt='o', label='N = 10')
    plt.errorbar([age_of_information_20[i][0] for i in range(num_data_20)],
                 [age_of_information_20[i][1] for i in range(num_data_20)],
                 [2*age_of_information_20[i][2] for i in range(num_data_20)], 
                 fmt='o', label='N = 20')
    plt.errorbar([age_of_information_30[i][0] for i in range(num_data_30)],
                 [age_of_information_30[i][1] for i in range(num_data_30)],
                 [2*age_of_information_30[i][2] for i in range(num_data_30)], 
                 fmt='o', label='N = 30')
    plt.title('Age of Information vs. Block Arrival Rate')
    plt.xlabel('Block Arrival Rate (blocks / s)')
    plt.ylabel('Age of Information (blocks)')
    plt.legend()
    
    plt.figure(4)
    plt.errorbar([consistency_fraction_10[i][0] for i in range(num_data_10)],
                 [consistency_fraction_10[i][1] for i in range(num_data_10)],
                 [2*consistency_fraction_10[i][2] for i in range(num_data_10)], 
                 fmt='o', label='N = 10')
    plt.errorbar([consistency_fraction_20[i][0] for i in range(num_data_20)],
                 [consistency_fraction_20[i][1] for i in range(num_data_20)],
                 [2*consistency_fraction_20[i][2] for i in range(num_data_20)], 
                 fmt='o', label='N = 20')
    plt.errorbar([consistency_fraction_30[i][0] for i in range(num_data_30)],
                 [consistency_fraction_30[i][1] for i in range(num_data_30)],
                 [2*consistency_fraction_30[i][2] for i in range(num_data_30)], 
                 fmt='o', label='N = 30')
    plt.title('Consistency Fraction vs. Block Arrival Rate')
    plt.xlabel('Block Arrival Rate (blocks / s)')
    plt.ylabel('Consistency Fraction')
    plt.legend()

    plt.figure(5)
    plt.errorbar([growth_rate_10[i][0] for i in range(num_data_10)],
                 [growth_rate_10[i][1] for i in range(num_data_10)],
                 [2*growth_rate_10[i][2] for i in range(num_data_10)], 
                 fmt='o', label='N = 10')
    plt.errorbar([growth_rate_20[i][0] for i in range(num_data_20)],
                 [growth_rate_20[i][1] for i in range(num_data_20)],
                 [2*growth_rate_20[i][2] for i in range(num_data_20)], 
                 fmt='o', label='N = 20')
    plt.errorbar([growth_rate_30[i][0] for i in range(num_data_30)],
                 [growth_rate_30[i][1] for i in range(num_data_30)],
                 [2*growth_rate_30[i][2] for i in range(num_data_30)], 
                 fmt='o', label='N = 30')
    plt.title('Distinguished Path Growth Rate vs. Block Arrival Rate')
    plt.xlabel('Block Arrival Rate (blocks / s)')
    plt.ylabel('Distinguished Path Growth Rate (blocks / s)')
    plt.legend()
    
    plt.show()

if __name__=='__main__':
  main()

