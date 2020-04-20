import multiprocessing as mp

import numpy as np
import numpy.random as random

import scipy
class BlockFlooding:
  def __init__(self, N, block_rate):
    # Block Flooding Parameters
    self.N = N
    self.block_rate = block_rate
    self.event_rate = (self.N + self.block_rate)

    # Temporal Parameters
    self.time = 0
    self.busy_period_lengths = []
    self.cycle_lengths = []
    self.cycle_begin = 0
    self.busy_period_begin = 0

    # Discrete Event Parameters
    self.num_blocks_total = 0
    self.num_events_total = 0
    self.num_blocks_behind_avg = 0
    self.frac_consistent_peers = 0

    # State-Based Parameters
    self.block_array = np.zeros((0, self.N))
    self.block_heights = np.zeros(0)
    self.peer_heights = np.zeros(self.N)
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
          self.block_heights = np.delete(self.block_heights, 0)

  def event(self):
    #  Perform a single round of flooding.
    self.num_events_total += 1

    self.clean_block_array()

    beta = 1./self.event_rate
    self.dt = random.exponential(beta)
    self.time += self.dt
    self.compute_running_stats()

    action_type_sample = random.random()

    # Arrival
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

      #  Set the block heights
      self.peer_heights[new_block_peer] += 1
      self.block_heights = np.append(self.block_heights, self.peer_heights[new_block_peer])

      return
     
    # Transmission 
    else:
      #  Pick a random peer to do a smart push transmission.
      #    The sending peer sends the oldest block that the
      #    sending peer has that the receiving peer does not
      #    have.
      #print('transmission')
      if self.consistent:
        return

      if not (self.block_array.shape == (0, self.N)):
        sending_peer = random.randint(self.N)
        receiving_peer = random.randint(self.N-1)
        if (receiving_peer >= sending_peer):
          receiving_peer += 1

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

            #  Update the block height
            self.peer_heights[receiving_peer] = self.block_heights[block_to_send]

            if (np.all(self.block_array == 1)):
              #print self.peer_heights
              # Check if it is a time of consistency
              if (self.busy_period_begin < self.cycle_begin):
                print 'ERROR 2'
                print self.time
                print self.busy_period_begin
                print self.cycle_begin
                raw_input()
              #if (not np.all(self.peer_heights == self.peer_heights[0])):
                #print 'ERROR 3'
                #print self.peer_heights
                #raw_input()
              self.busy_period_lengths.append(self.time - self.busy_period_begin)
              self.cycle_lengths.append(self.time - self.cycle_begin)
              self.cycle_begin = self.time
              #print 'setting: '
              #print self.time
              #print self.busy_period_begin
              #print self.cycle_begin
              #print self.block_array
              self.consistent = True
          return

        else:
          return

  def compute_running_stats(self):
    time_interval = self.dt/(1.0*self.N)

    num_active_blocks = self.block_array.shape[0]
    num_blocks_per_peer = np.sum(self.block_array, axis = 0)
    if num_active_blocks > 0:
      num_consistent_peers = np.sum(num_blocks_per_peer == num_active_blocks)
      self.frac_consistent_peers += num_consistent_peers * time_interval
      self.num_blocks_behind_avg += (self.block_array.size - np.sum(num_blocks_per_peer)) * time_interval
    else:
      self.frac_consistent_peers += 1.0 * self.N * time_interval
      # in this case nobody is behind so no need to update self.num_blocks_behind_avg

  def compute_stats(self):
    self.mean_busy_period = np.mean(self.busy_period_lengths)
    self.mean_cycle_length = np.mean(self.cycle_lengths)
    self.num_blocks_behind_avg = self.num_blocks_behind_avg / self.time
    self.frac_consistent_peers = self.frac_consistent_peers / self.time


def run_simulate(N, block_rate, num_cycles, seed, output):
  random.seed(seed)
  BF = BlockFlooding(N, block_rate)
  while (len(BF.cycle_lengths) < num_cycles):
    BF.event()
  BF.compute_stats()

  output.put([BF.mean_busy_period, BF.mean_cycle_length,
              BF.num_blocks_behind_avg, BF.frac_consistent_peers,
              (1.0*block_rate*BF.peer_heights[0])/(1.0*BF.num_blocks_total)])

def main():
  num_peers = [10 * (i+1) for i in range(3)]

  busy_period_data = []
  cycle_length_data = []
  age_of_information_data = []
  frac_consistent_data = []

  num_cycles = 500

  output = mp.Queue()
  
  num_processes = 30

  block_rate = 0

  data_store = {10: {'busy_period': [], 'cycle_length': [], 'age_of_information': [], 'consistency_fraction': [], 'growth_rate' : []},
                20: {'busy_period': [], 'cycle_length': [], 'age_of_information': [], 'consistency_fraction': [], 'growth_rate' : []},
                30: {'busy_period': [], 'cycle_length': [], 'age_of_information': [], 'consistency_fraction': [], 'growth_rate' : []}}

  for N in num_peers:
    frac_consistent = 1

    block_rate = 0.01
    while (frac_consistent >= 0.01):
      processes = [mp.Process(target = run_simulate, args = (N, block_rate, num_cycles, x, output))
                    for x in range(num_processes)]

      for p in processes:
        p.start()
      for p in processes:
        p.join()

      data = [output.get() for p in processes]
      data_store[N]['busy_period'].append([block_rate, np.mean([i[0] for i in data]), np.std([i[0] for i in data])])
      data_store[N]['cycle_length'].append([block_rate, np.mean([i[1] for i in data]), np.std([i[1] for i in data])])
      data_store[N]['age_of_information'].append([block_rate, np.mean([i[2] for i in data]), np.std([i[2] for i in data])])
      data_store[N]['consistency_fraction'].append([block_rate, np.mean([i[3] for i in data]), np.std([i[3] for i in data])])
      data_store[N]['growth_rate'].append([block_rate, np.mean([i[4] for i in data]), np.std([i[4] for i in data])])
      
      frac_consistent = np.mean([i[3] for i in data])
      block_rate += 0.01


  print data_store
if __name__=='__main__':
  main()
