from dataclasses import dataclass, asdict
from pathlib import Path
from statistics import stdev
import json

from satsp.simulated_annealing import SimulatedAnnealing
from satsp.tsplib import read_instance
from satsp.visualizer import Visualizer


OUTPUT_DIR = Path("../") / "output" 

INSTANCE_NAMES = [
    "eil51",
    "pr107",
    "kroA200"
]

@dataclass
class InstanceResult():
    instance_name: str
    distances: list[float]
    distance_mean: float
    distance_std: float
    best_permutation: list[int]

@dataclass
class Summary():
    instance_results: list[InstanceResult]

    def to_json(self, json_path):
        """Save output to json file"""
        json_str = json.dumps(asdict(self), indent=4)
        with open(json_path, 'w') as file:
            file.write(json_str)


INSTANCE_RUNS = 10
SA_STEPS = 100_000


instance_results: list[InstanceResult] = []
for instance_name in INSTANCE_NAMES:
    
    distances = []
    best_permuation = None


    instance = read_instance(instance_name)
    print(instance.name)
    for i in range(INSTANCE_RUNS):
        sa = SimulatedAnnealing(instance, N=SA_STEPS, stale_after=10_000)
        distances.append(-1*sa.V_best)
        if sa.V_best <= min(distances):
            best_permuation = sa.state_best.tolist()


    instance_result = InstanceResult(
        instance_name=instance_name,
        distances=distances,
        distance_mean=sum(distances) / INSTANCE_RUNS,
        distance_std=stdev(distances),
        best_permutation=best_permuation
    )

    instance_results.append(instance_result)

    vis = Visualizer(instance)
    vis.draw_path(best_permuation, 
                 title = f"The best path of {instance_name} by simulated annealing",
                 out = OUTPUT_DIR / f"sa_{instance_name}.png")

print(instance_results[0])

summary = Summary(instance_results)
summary.to_json(OUTPUT_DIR / "output.json")