import logging
import os
from pathlib import Path
from typing import List, Dict

import yaml
from travel.config.bags.bag import Bag
from travel.config.bags.base_bag import BaseBag
from travel.config.bags.root_bag import RootBag

BAG_FILE = "bag.yml"


logger = logging.getLogger(__name__)


def read_bag(location: str, is_root: bool = False) -> BaseBag:

    # Read the bag file
    path = os.path.join(location, BAG_FILE)
    with open(path) as f:
        yml = yaml.load(f, Loader=yaml.SafeLoader) or {}
        bag_builder = RootBag if is_root else Bag
        return bag_builder(location=location, yml=yml)


def has_bag(location: str) -> bool:
    return os.path.isfile(os.path.join(location, BAG_FILE))


def get_bag_name(location: str) -> str:
    return os.path.basename(os.path.normpath(location))


def read_all_bags(location: str) -> Dict[str, BaseBag]:

    # Find the uppermost (parent) bag file
    uppermost = location
    while has_bag(location):
        uppermost = location
        location = str(Path(location).parent)

    # Read main bag file and bagged bag files
    bags = {bag.name: bag for bag in read_bags_from(uppermost)}
    # Set the root context
    for b in bags.values():
        b.root_context = uppermost

    # Build dependencies
    for name in bags:
        for bag in bags.values():
            if name in bag.dependencies:
                bag.fill_dependency_with_bag(bags[name])
    return bags


def parse_bags(location: str, target: str = None) -> (BaseBag, BaseBag):

    # Read the target bag and all the bags
    target = target or get_bag_name(location)
    bags = read_all_bags(location)

    # Manage this target bag
    if target not in bags:
        raise ValueError(f"The specified bag \"{target}\" does not exist in {location}")
    bag = bags[target]
    return bag, bags


def read_bags_from(uppermost: str) -> List[BaseBag]:
    return read_bags_from_recursive(uppermost, is_root=True)


def read_bags_from_recursive(location: str, is_root: bool = True) -> List[BaseBag]:

    # Read the local bag
    group = []
    bag = read_bag(location, is_root=is_root)

    # Read all bags recursively
    bags = [bag]
    for directory in os.listdir(location):
        current = os.path.join(location, directory)
        if has_bag(current):
            children = read_bags_from_recursive(current, is_root=False)
            group = group + children
            bags = bags + children

    # Set the bagged group
    bag.group = group
    return bags
