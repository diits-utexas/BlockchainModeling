import sys, os

import numpy as np
import numpy.random as random

import scipy

import multiprocessing as mp

class BlockFlooding:
  def __init__(self, N, block_rate, bandwidth, block_arrival_times):
    # Block Flooding Parameters
    self.N = N
    self.block_rate = block_rate
    self.bandwidth = bandwidth
    self.block_arrival_times = block_arrival_times
    self.transmission_rate = (self.N*self.bandwidth)

    # Temporal Parameters
    self.time = 0
    self.busy_period_lengths = []
    self.cycle_lengths = []
    self.cycle_begin = 0
    self.busy_period_begin = 0

    # Discrete Event Parameters
    self.num_cycles = 0
    self.num_blocks_total = 0
    self.num_events_total = 0
    self.num_blocks_behind_avg = 0
    self.num_consistent_peers_avg = 0

    # State-Based Parameters
    self.block_array = np.zeros((0, self.N))
    self.block_arrival_index = 0
    self.consistent = True

  def clean_block_array(self):
    #  Remove the parts of the block array corresponding to
    #    rumors that have already spread accross the entire
    #    network.
    if not (self.block_array.shape == (0, self.N)):
      #print(self.block_array)
      num_current_blocks = self.block_array.shape[0]
      for index in range(num_current_blocks):
        if(np.all(self.block_array[0, :] == 1.)):
          self.block_array = np.delete(self.block_array, 0, 0)

  def event(self):
    #  Perform a single round of flooding.
    self.num_events_total += 1

    self.clean_block_array()

    #beta = 1./self.event_rate
    #old_time = self.time
    #self.time += random.exponential(beta)

    #action_type_sample = random.random()

    # Arrival
    '''
    if (action_type_sample < (1.0*self.block_rate)/(1.0*self.event_rate)):
      self.consistent = False
      #  Check if it is a time of consistency.
      if (self.block_array.shape == (0, self.N)):
        self.busy_period_begin = self.time
        if (self.busy_period_begin < self.cycle_begin):
          print 'ERROR'
      #print('arrival')
      self.num_blocks_total += 1

      #  Add a new block to the block array.
      new_block_peer = random.randint(self.N)
      self.block_array = np.append(self.block_array, np.zeros((1, self.N)), 0)
      self.block_array[-1, new_block_peer] = 1
    '''

    # New Cycle
    if (self.consistent):
      #print 'New Cycle'
      self.time = self.block_arrival_times[self.block_arrival_index]
      self.busy_period_begin = self.time
      self.block_arrival_index += 1
      self.consistent = False


      #  Add a new block to the block array.
      new_block_peer = random.randint(self.N)
      self.block_array = np.append(self.block_array, np.zeros((1, self.N)), 0)
      self.block_array[-1, new_block_peer] = 1

      self.time += random.exponential(1./self.transmission_rate)


    # Update the system time
    else:
      self.time += random.exponential(1./self.transmission_rate)

      # Arrival
      while (self.time > self.block_arrival_times[self.block_arrival_index]):
        #print 'Block Arrival, not a new cycle'
        #self.time = self.block_arrival_times[self.block_arrival_index]
        self.block_arrival_index += 1
      
        #  Add a new block to the block array.
        new_block_peer = random.randint(self.N)
        self.block_array = np.append(self.block_array, np.zeros((1, self.N)), 0)
        self.block_array[-1, new_block_peer] = 1

      #self.time += random.exponential(1./self.transmission_rate)
     
    # Transmission 
      #  Pick a random peer to do a smart push transmission.
      #    The sending peer sends the oldest block that the
      #    sending peer has that the receiving peer does not
      #    have.
      #print('transmission')

      # for the COMPLETE GRAPH
    if not (self.block_array.shape == (0, self.N)):
      sending_peer = random.randint(self.N)
      receiving_peer = random.randint(self.N-1)
      if (receiving_peer >= sending_peer):
        receiving_peer += 1

      # for the 8-REGULAR GRAPH
        #print('sending peer: ' + str(sending_peer))
        #print('receiving peer: ' + str(receiving_peer))

      sending_peer_blocks = self.block_array[:, sending_peer]
      sendable_blocks = np.where(sending_peer_blocks == 1)
      block_to_send = -1

      send_block = False

      if (len(sendable_blocks[0]) > 0):
        for block in range(len(sendable_blocks[0])):
          if (self.block_array[block, sending_peer] == 1. and 
              self.block_array[block, receiving_peer] == 0.):
            send_block = True
            block_to_send = block
              #print('send block: ' + str(block_to_send))
              #  Break the for loop.
            break

        #  Set the receiving peer's block to 1 (if they already had
        #    it, this is as if nothing happened.
        if (send_block):
          self.block_array[block_to_send, receiving_peer] = 1

          if (np.all(self.block_array == 1) and self.consistent == False):
            # Check if it is a time of consistency
            if (self.busy_period_begin < self.cycle_begin):
              print 'ERROR 2'
              print self.time
              print self.busy_period_begin
              print self.cycle_begin
              raw_input()
            self.busy_period_lengths.append(self.time - self.busy_period_begin)
            self.cycle_lengths.append(self.time - self.cycle_begin)
            self.cycle_begin = self.time
            self.num_cycles += 1
            #print 'setting: '
            #print self.time
            #print self.busy_period_begin
            #print self.cycle_begin
            #print self.block_array
            self.consistent = True

        else:
          pass
    self.compute_running_stats()

  def compute_running_stats(self):
    self.num_blocks_behind_avg += (1.0*(self.block_array.size) - np.sum(self.block_array))
    for peer in range(self.N):
      if np.all(self.block_array[:, peer] == 1):
        self.num_consistent_peers_avg += 1

  def compute_stats(self):
    self.mean_busy_period = np.mean(self.busy_period_lengths)
    self.mean_cycle_length = np.mean(self.cycle_lengths)
    self.num_blocks_behind_avg = (1.0*self.num_blocks_behind_avg)/(self.time*self.N)
    self.frac_consistent_peers_avg = (1.0*self.num_consistent_peers_avg)/(self.time*self.N)


def run_simulate(N, block_rate, bandwidth, block_arrival_times, num_cycles, output):
  BF = BlockFlooding(N, block_rate, bandwidth, block_arrival_times)

  while BF.num_cycles < num_cycles:
    BF.event()
    print BF.num_cycles

  BF.compute_stats()

  output.put([BF.mean_busy_period, BF.mean_cycle_length,
              BF.num_blocks_behind_avg, BF.frac_consistent_peers_avg])
  

def main():
  num_peers = 3500
  block_rate = 1./600.
  bandwidth = 73.1
  beta = 1./block_rate

  num_cycles = 2000

  arrival_times = 0
  block_arrival_times = []
  for i in range (5*num_cycles):
    arrival_times += random.exponential(beta)
    block_arrival_times = np.append(block_arrival_times, arrival_times)

  num_processes = 1

  output = mp.Queue()

  processes = [mp.Process(target=run_simulate, args=(100, block_rate, bandwidth, block_arrival_times, num_cycles, output)) for x in range(num_processes)]

  for p in processes:
    p.start()

  for p in processes:
    p.join()

  results = [output.get() for p in processes]

  mean_busy_period = [results[p][0] for p in range(num_processes)]
  mean_cycle_length = [results[p][1] for p in range(num_processes)]
  mean_blocks_behind = [results[p][2] for p in range(num_processes)]
  mean_frac_consistent = [results[p][3] for p in range(num_processes)]

  mean_busy_period = np.mean(mean_busy_period)
  mean_cycle_length = np.mean(mean_cycle_length)
  mean_blocks_behind = np.mean(mean_blocks_behind)
  mean_frac_consistent = np.mean(mean_frac_consistent)

  print mean_busy_period
  print mean_cycle_length
  print mean_blocks_behind
  print mean_frac_consistent


if __name__=='__main__':
  main()
