import os

import pytest


class ComplexProject:

    def __init__(self, data_location):
        self.name = "complexproject"
        self.common = "common"
        self.tasks = "tasks"
        self.microservices = "microservices"
        self.first = "first"
        self.second = "second"
        self.pipertask_example = "pipertaskexample"

        self.piper_project = os.path.join(data_location, self.name)


@pytest.fixture
def data_location():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")


@pytest.fixture
def complex_project(data_location):
    return ComplexProject(data_location)

