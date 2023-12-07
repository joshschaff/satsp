import random

import numpy as np
from tsplib95.models import StandardProblem
from tqdm import tqdm

from satsp.tsplib import INSTANCES, read_instance

from enum import Enum


class NeighborStrategy(Enum):
    SWAP_STOPS = 1
    FLIP_SUBROUTE = 2
    MOVE_SUBROUTE = 3


class SimulatedAnnealing():

    instance: StandardProblem
    N: int
    strategies: list[NeighborStrategy]

    n: int
    state: np.ndarray
    V_state: float
    state_best: np.ndarray
    V_best: np.ndarray

    hist = list[float]

    stale_after: int
    last_update: int

    def __init__(self,
                 inst: StandardProblem,
                 N: int,
                 stale_after: int,
                 strategies = [strat for strat in NeighborStrategy]):
        self.instance = inst
        self.N = N
        self.strategies = strategies

        self.n = 0
        self.state= np.random.permutation(inst.dimension)
        self.V_state = self._v(self.state)

        self.state_best = self.state
        self.V_best = self.V_state

        self.hist = []

        self.stale_after=stale_after
        self.last_update=0

        self._run()


    def _run(self):
        pbar = tqdm(total=self.N)
        while (self.n < self.N):
            self._step()
            pbar.update(1)
            pbar.set_description(str(self.V_best))
            if self.n - self.last_update > self.stale_after:
                break


    def _v(self, permuation) -> float:
        """ Value function 
        
        Permutation should be of 0 to self.inst.dimension -1
        """
        dist = 0
        for i, start in enumerate(permuation):
            end = permuation[(i + 1)  % self.instance.dimension]
            # instances are indexed starting at 1
            dist += self.instance.get_weight(start+1, end+1)
        return -1*dist


    def _get_neighboring_state(self) -> np.ndarray:
        """
        Returns a copy of self.state with two random indices exchanged
        """
        # copy the existing state permuation
        seq = self.state.copy()

        strat = random.choice(self.strategies)
        match strat:
            case NeighborStrategy.SWAP_STOPS:
                return self._swap_stops(seq)
            case NeighborStrategy.FLIP_SUBROUTE:
                return self._flip_subroute(seq)
            case NeighborStrategy.MOVE_SUBROUTE:
                return self._move_subroute(seq)


    def _swap_stops(self, seq: np.ndarray) -> np.ndarray:
        # swap two random indices
        idx1, idx2 = random.sample(range(len(seq)), 2)
        seq[idx1], seq[idx2] = seq[idx2], seq[idx1]
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
        return seq


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
                self.last_update = self.n

        self.n += 1
        self.hist.append(self.V_state)


if __name__ == '__main__':
    instance = read_instance(INSTANCES[6])
    print(f"{instance.name = }")
    print(f"{instance.dimension = }")

    sa = SimulatedAnnealing(inst=instance, N=10_000, stale_after=100_000)

    print(f"{sa.V_best = }")
