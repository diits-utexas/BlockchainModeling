import numpy as np
import numpy.random as random

import scipy

class BlockFlooding:
  def __init__(self, N, block_rate):
    self.N = N
    self.block_rate = block_rate

    self.time = 0
    self.times_of_consistency = [0]

    self.blocks_per_ttc = []
    

    initial_peer = random.randint(self.N)
    self.block_array = np.zeros((1, self.N))
    self.block_array[0, initial_peer] = 1

  def clean_block_array(self):
    #  Remove the parts of the block array corresponding to
    #    rumors that have already spread accross the entire
    #    network.
    if not (self.block_array.shape == (0, self.N)):
      #print(self.block_array)
      if(np.all(self.block_array[0, :] == 1.)):
        self.block_array = np.delete(self.block_array, 0, 0)

  def round(self):
    #  Perform a single round of floodsng.
    self.clean_block_array()

    #  Check if it is a time of consistency.
    if (self.block_array.shape == (0, self.N)):
      self.times_of_consistency.append(self.time)

    beta = 1./(self.N + self.block_rate)
    self.time += random.exponential(beta)

    action_type_sample = random.random()
    if (action_type_sample < (1.0*self.block_rate)/(1.0*self.N + 1.0*self.block_rate)):
      #print('arrival')

      #  Add a new block to the block array.
      new_block_peer = random.randint(self.N)
      self.block_array = np.append(self.block_array, np.zeros((1, self.N)), 0)
      self.block_array[-1, new_block_peer] = 1
      
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
              block = len(sendable_blocks[0]) + 1

          #  Set the receiving peer's block to 1 (if they already had
          #    it, this is as if nothing happened.
          if (send_block):
            self.block_array[block_to_send, receiving_peer] = 1

        else:
          pass
    #raw_input()

def main():
  N = 50
  block_rates = np.linspace(0, 0.5, 51)
  
  for block_rate in block_rates:
    BF = BlockFlooding(N, block_rate)
    while (len(BF.times_of_consistency) < 10001):
      BF.round()
      print('\r' + 'Times of Consistency: ' + str(len(BF.times_of_consistency))),

    times_of_consistency_diff = np.diff(BF.times_of_consistency)
    print ('\rMean time to consistency with block rate ' + str(block_rate) + ': '
            + str(np.mean(times_of_consistency_diff)))

if __name__=='__main__':
  main()