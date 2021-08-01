import logging
import os


logger = logging.getLogger(__name__)


class Pipe:

    def __init__(self, location: str, yml: dict):
        self.location = location
        self.name = os.path.basename(os.path.normpath(location))

        # Pop the config entries  # TODO sanity checks! Because we will execute scripts
        config = yml.copy()
        self.python = config.pop("python", None)
        self.dependencies = {dep: None for dep in config.pop("dependencies", [])}
        self.requirements = config.pop("requirements", {})

        # Extra utils
        self.setup_py_folder = os.path.join(self.location, "package")
        self.requirements_file = os.path.join(self.setup_py_folder, "requirements.txt")

        # If there are still configs, they are unknown. Raise an error
        if config:
            raise KeyError(f"Unknown configuration in pipe file: {config}")

    def fill_dependency_with_pipe(self, pipe):
        self.dependencies[pipe.name] = pipe

    def flat_dependencies(self):

        def visit(pipe, visited, level=0):
            for dep in pipe.dependencies.values():
                visited[dep] = max(level, visited.get(dep, level))
                visit(dep, visited, level=level+1)
            return visited

        pipes = visit(self, {})
        dependencies = [pipe for pipe, level in sorted(pipes.items(), key=lambda x: x[1], reverse=True)]
        return dependencies

    def __str__(self):
        return str(vars(self))

    def __repr__(self):
        return str(self)
