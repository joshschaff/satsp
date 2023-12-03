"""Utilities to read TSPLIB instance files"""
import os
from pathlib import Path
import gzip

import tarfile
import tsplib95
import requests

# change working directory to be the satsp/ module folder
os.chdir(os.path.dirname(__file__))

ALL_TSP_URL = "http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp/ALL_tsp.tar.gz"

ALL_TSP_TAR_GZ = Path("../") / "ALL_tsp.tar.gz"

INSTANCES = [
    'kroE100',
    'fl1400',
    'rl5934',
    'kroA150',
    'att532',
    'burma14',
    'pr107',
    'si535',
    'vm1084',
    'd1655',
    'fl1577',
    'pr439',
    'eil51',
    'dantzig42',
    'pr76',
    'bays29',
    'd493',
    'lin105',
    'pr264',
    'fl417',
    'hk48',
    'si175',
    'ts225',
    'u1060',
    'brg180',
    'gr17',
    'gr21',
    'usa13509',
    'kroB150',
    'nrw1379',
    'gr120',
    'd2103',
    'u574',
    'ali535',
    'pr152',
    'rl1304',
    'gr96',
    'eil101',
    'a280',
    'pr124',
    'rat99',
    'rl5915',
    'st70',
    'kroB100',
    'u159',
    'pcb442',
    'pcb1173',
    'rat783',
    'rl11849',
    'xray',
    'fl3795',
    'gr202',
    'bier127',
    'vm1748',
    'gr24',
    'swiss42',
    'u2319',
    'pr299',
    'pr226',
    'bayg29',
    'pr2392',
    'd657',
    'kroA200',
    'pr144',
    'pla7397',
    'pa561',
    'pr1002',
    'si1032',
    'att48',
    'lin318',
    'kroD100',
    'ulysses16',
    'kroA100',
    'gr48',
    'rl1889',
    'fri26',
    'pla85900',
    'rd400',
    'ch150',
    'u724',
    'ch130',
    'rl1323',
    'gr229',
    'u1817',
    'rat575',
    'u1432',
    'dsj1000',
    'berlin52',
    'ulysses22',
    'd1291',
    'gr137',
    'd198',
    'pla33810',
    'linhp318',
    'pr136',
    'kroC100',
    'p654',
    'kroB200',
    'gil262',
    'gr666',
    'd18512',
    'brazil58',
    'd15112',
    'rat195',
    'tsp225',
    'u2152',
    'rd100',
    'pcb3038',
    'gr431',
    'brd14051',
    'fnl4461',
    'eil76'
]



def _download_all_tsp_tar():
    # download all TSP isntances
    response = requests.get(ALL_TSP_URL)

    with open(ALL_TSP_TAR_GZ, "wb") as f:
        f.write(response.content)


def _read_all_tsp_tar_subfile(file_name: str) -> str:
    """Read the given file contained inside ALL_TSP_TAR"""
    with tarfile.open(ALL_TSP_TAR_GZ, "r:gz") as file:
        # extract the gzip instance file
        compressed_file_bytes = file.extractfile(file_name).read()
        # decompress the gzip instance file to raw bikes
        decompressed_file_bytes = gzip.decompress(compressed_file_bytes)
        # decode file bytes to string
        file_contents = decompressed_file_bytes.decode()
        return file_contents

def read_instance(instance_name: str) -> tsplib95.models.StandardProblem:
    """Read a TSPlib instance prefixed with the given string"""
    instance_str = _read_all_tsp_tar_subfile(f"{instance_name}.tsp.gz")
    return tsplib95.parse(instance_str)


if __name__ == "__main__":
    #_download_all_tsp_tar()

    inst = read_instance(INSTANCES[1])
    print(type(inst))
