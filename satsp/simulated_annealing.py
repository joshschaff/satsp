from tsplib95.models import StandardProblem

from satsp.tsplib import INSTANCES, read_instance



class SimulatedAnnealing():


    def __init__(self,
                 inst: StandardProblem):
        self.instance = inst

        # the total number of stops
        inst.dimension

        # evaluate weights

        self.start = 1
        
        


    # how to get all stops?



    # how to represent a permutation?


    # how to evaluate weight of a permutation?


    def _v(self, permuation):
        """ Value function """
        dist = 0 
        for i in range(len(permuation)):
            start = permuation[i]
            end = permuation[i % self.instance.dimension]
            dist += self.instance.get_weight(start, end)
        return dist



    # start with a permutation of all stops





if __name__ == '__main__':
    inst = read_instance(INSTANCES[0])
    print(inst)
