from satsp.simulated_annealing import NeighborStrategy, SimulatedAnnealing
from satsp.tsplib import read_instance
from tqdm import tqdm


from matplotlib import pyplot as plt

import numpy as np

label_to_strategies = {
    'Swap Stops' : [
        NeighborStrategy.SWAP_STOPS
    ],
    'Swap Stops & Flip Subroute' : [
        NeighborStrategy.SWAP_STOPS,
        NeighborStrategy.FLIP_SUBROUTE
    ],
    'Swap Stops & Move Subroute' : [
        NeighborStrategy.SWAP_STOPS,
        NeighborStrategy.MOVE_SUBROUTE
    ],
    'Swap Stops & Flip Subroute & Move Subroute': [
        NeighborStrategy.SWAP_STOPS,
        NeighborStrategy.FLIP_SUBROUTE,
        NeighborStrategy.MOVE_SUBROUTE
    ]
}


instance = read_instance("pr107")


label_to_hist = {}

N= 10_000
runs_per_label = 10


for label, strategies in label_to_strategies.items():
    print(label)
    hists = []

    for i in range(runs_per_label):
        sa = SimulatedAnnealing(instance, N=N, stale_after=N, strategies=strategies)
        hists.append(sa.hist)
  
    hist = np.array(hists).mean(axis=0)
    label_to_hist[label] = -1*hist
    print(len(hists))


domain = list(range(N))
plt.figure()
for label, hist in label_to_hist.items():
    plt.plot(domain, hist, label=label)

plt.title("Min Cost TSP Trajectories of Simulated Annealing Neighborhood Strategies")
plt.ylabel("Min Cost")
plt.xlabel("Steps")
plt.legend()
plt.savefig("test.png")




