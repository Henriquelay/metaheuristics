"""Test the UCTP GLS solution by running every instance in the tests folder with a low number of iterations."""

import os
from pprint import pprint
from local_search.local_search import GuidedLocalSearch

from uctp.instance_parser import parse_file

INSTANCES_FOLDER = "instances/test/"

INSTANCES_PATH = [
    os.path.join(INSTANCES_FOLDER, file) for file in os.listdir(INSTANCES_FOLDER)
]


def test_gls_solution():
    """Test the UCTP GLS solution by running every instance in the tests folder with a low number of iterations."""

    for instance_path in INSTANCES_PATH:
        print(f"Testing instance {instance_path}...")
        instance = parse_file(instance_path)

        local_search = GuidedLocalSearch(
            neighborhood_size=3, llambda=1 / 2, alpha=1 / 4
        )

        weights = ((40, 30, 20, 10), (6, 5, 4, 3))
        solution = local_search.search(
            initial_solution=instance.to_graph(),
            max_iterations=100,
            problem=instance,
            weights=weights,
        )

        pprint(instance.evaluate(solution, weights)[0])
        print()
    assert False
