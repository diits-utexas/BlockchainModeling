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
    self.num_consistent_peers_avg = 0

    # State-Based Parameters
    self.block_array = np.zeros((0, self.N))
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

    beta = 1./self.event_rate
    old_time = self.time
    self.time += random.exponential(beta)

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
     
    # Transmission 
    else:
      #  Pick a random peer to do a smart push transmission.
      #    The sending peer sends the oldest block that the
      #    sending peer has that the receiving peer does not
      #    have.
      #print('transmission')
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
              #print 'setting: '
              #print self.time
              #print self.busy_period_begin
              #print self.cycle_begin
              #print self.block_array
              self.consistent = True

        else:
          pass
    self.num_blocks_behind_avg += (1.0*self.block_array.size) - np.sum(self.block_array)
    for peer in range(self.N):
      if np.all(self.block_array[:, peer] == 1):
        self.num_consistent_peers_avg += 1

  def compute_stats(self):
    self.num_blocks_behind_avg = (1.0*self.num_blocks_behind_avg)/(1.0 * self.N * self.num_events_total)
    self.num_consistent_peers_avg = (1.0*self.num_consistent_peers_avg)/(1.0 * self.N * self.num_events_total)

def main():
  num_peers = [10, 20, 30, 40, 50]
  num_peers = [10]
  block_rates = np.linspace(0, 0.5, 51)
  max_block_rates = []

  data_store = {N : {'block_rate' : [], 'time_to_consistency' : [], 'cycle_length' : [],
                     'num_blocks_behind' : [], 'frac_consistent' : []}
                for N in num_peers}


  for N in num_peers:
    #print ('\rN = ' + str(N))
    fraction_consistent = 1

    block_rate = 0.01
    while (fraction_consistent >= 0.01):
      #print ('\nBLOCK RATE:' + str(block_rate)),
      BF = BlockFlooding(N, block_rate)
      while (len(BF.cycle_lengths) < 11):
        BF.event()

      BF.compute_stats()
      data_store[N]['block_rate'] = np.append(data_store[N]['block_rate'], block_rate)
      data_store[N]['time_to_consistency'] = np.append(data_store[N]['time_to_consistency'], BF.busy_period_lengths)
      data_store[N]['cycle_length'] = np.append(data_store[N]['cycle_length'], BF.cycle_lengths)
      data_store[N]['num_blocks_behind'] = np.append(data_store[N]['num_blocks_behind'], BF.num_blocks_behind_avg)
      data_store[N]['frac_consistent'] = np.append(data_store[N]['frac_consistent'], BF.num_consistent_peers_avg)

      fraction_consistent = BF.num_consistent_peers_avg

      block_rate += 0.01

    max_block_rates = np.append(max_block_rates, block_rate)


  print data_store  

if __name__=='__main__':
  main()
