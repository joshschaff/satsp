import matplotlib.pyplot as plt
import numpy as np
from tsplib95.models import StandardProblem

from satsp.tsplib import INSTANCES, read_instance
from satsp.simulated_annealing import SimulatedAnnealing


class Visualizer():
    instance: StandardProblem


    def __init__(self, instance: StandardProblem):
        self.instance = instance


    def draw_path(self, permutatation: np.ndarray, title: str, out: str):
        plt.figure()
        X = []
        Y = []
        for i in range(len(permutatation)+1):
            node = permutatation[i % len(permutatation)]
            coords = self.instance.get_display(node+1)
            X.append(coords[0])
            Y.append(coords[1])

        plt.plot(X,Y, 'bo-') # blue with circle marker and line
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.title(title)
        plt.savefig(out)




if __name__ == '__main__':
    #inst = read_instance(INSTANCES[6])
    inst = read_instance("pr136")
    print(f"{inst.name = }")
    sa = SimulatedAnnealing(inst, N=100_000)
    vis = Visualizer(inst)
    vis.draw_path(sa.state_best)