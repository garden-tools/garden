import logging
import os
from pathlib import Path
from typing import List, Dict

import yaml
from piper.config.pipe import Pipe

_PIPE_FILE = "pipe.yml"


logger = logging.getLogger(__name__)


def _read_pipe(location: str) -> Pipe:

    # Read the pipe file
    path = os.path.join(location, _PIPE_FILE)
    with open(path) as f:
        yml = yaml.load(f, Loader=yaml.SafeLoader) or {}
        return Pipe(location=location, yml=yml)


def _has_pipe(location: str) -> bool:
    return os.path.isfile(os.path.join(location, _PIPE_FILE))


def get_pipe_name(location: str) -> str:
    return os.path.basename(os.path.normpath(location))


def read_all_pipes(location: str) -> Dict[str, Pipe]:

    # Find the uppermost (parent) pipe file
    uppermost = location
    while _has_pipe(location):
        uppermost = location
        location = str(Path(location).parent)

    # Read main pipe file and nested pipe files
    main = _read_pipe(uppermost)
    pipes = {
        main.name: main,
        **{pipe.name: pipe for pipe in _read_pipes_from(uppermost)}
    }

    # Build dependencies
    for name in pipes:
        for pipe in pipes.values():
            if name in pipe.dependencies:
                pipe.fill_dependency_with_pipe(pipes[name])
    return pipes


def _read_pipes_from(location: str) -> List[Pipe]:

    # Read all pipes recursively
    pipes = []
    for directory in os.listdir(location):
        current = os.path.join(location, directory)
        if _has_pipe(current):
            pipes.append(_read_pipe(current))
            pipes = pipes + _read_pipes_from(current)
    return pipes
