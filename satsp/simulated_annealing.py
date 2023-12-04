import random

import numpy as np
from tsplib95.models import StandardProblem
from tqdm import tqdm

from satsp.tsplib import INSTANCES, read_instance


class SimulatedAnnealing():

    instance: StandardProblem
    state: np.ndarray
    N: int

    def __init__(self,
                 inst: StandardProblem,
                 N: int):
        self.instance = inst
        self.N = N

        # initialize state to be a random permutation
        # this will be from 0 to dimension -1
        self.state= np.random.permutation(inst.dimension)
        self.V_state = self._v(self.state)
        self.n = 0

        self.state_best = self.state
        self.V_best = self.V_state

        self._run()


    def _run(self):
        pbar = tqdm(total=self.N)
        while (self.n < self.N):
            self._step()
            pbar.update(1)
            pbar.set_description(str(self.V_best))

    def _v(self, permuation) -> float:
        """ Value function 
        
        Permutation should be of 0 to self.inst.dimension -1
        """
        dist = 0
        for i, start in enumerate(permuation):
            end = permuation[(i + 1)  % self.instance.dimension]
            # instances are indexed starting at 1
            dist += self.instance.get_weight(start+1, end+1)
        return -1* dist

        
    def _get_neighboring_state(self) -> np.ndarray:
        """
        Returns a copy of self.state with two random indices exchanged
        """
        # copy the existing state permuation
        seq = self.state.copy()

        U = random.random()
        if U < 1/3:
            # swap two random indices
            idx1, idx2 = random.sample(range(len(seq)), 2)
            seq[idx1], seq[idx2] = seq[idx2], seq[idx1]
        elif U < 2/3:
            self._flip_subroute(seq)
        else:
            self._move_subroute(seq)
        return seq

    def _move_subroute(self, seq: np.ndarray) -> np.ndarray:
        idx1, idx2 = random.sample(range(len(seq)), 2)
        start = min(idx1, idx2)
        stop = max(idx1, idx2)
        subseq = seq[start : stop]
        seq = np.delete(seq, np.s_[start:stop])
        insert = random.choice(range(len(seq)))
        return np.insert(seq, insert, subseq)



    def _flip_subroute(self, seq: np.ndarray) -> np.ndarray:
        idx1, idx2 = random.sample(range(len(seq)), 2)
        start = min(idx1, idx2)
        stop = max(idx1, idx2)
        subseq = seq[start : stop]
        seq[start: stop] = np.flip(subseq)


    def _step(self):
        """One step of the simulated annealing algorithm"""
        neighbor = self._get_neighboring_state()

        V_neighbor = self._v(neighbor)

        transtion = (
            # if the neighbor strictly improve objective
            V_neighbor > self.V_state or
            # otherwise with random probability
            random.random() < (1+self.n) ** (V_neighbor-self.V_state)
        )

        if transtion:
            # traverse to neighbor
            self.state = neighbor
            self.V_state = V_neighbor

            # update best
            if self.V_state > self.V_best:
                self.state_best = self.state.copy()
                self.V_best = self.V_state
            
        self.n += 1


if __name__ == '__main__':
    instance = read_instance(INSTANCES[6])
    print(f"{instance.name = }")
    print(f"{instance.dimension = }")

    sa = SimulatedAnnealing(instance, 10_000)

    print(f"{sa.V_best = }")



    



    
