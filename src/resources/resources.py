from abc import ABC, abstractmethod


class Resource(ABC):
    def register(self) -> None:
        resources.add(self)

    @abstractmethod
    def cleanup(self) -> None:
        raise NotImplementedError("Subclasses must implement the cleanup method")


class Resources:
    # manage resources to be cleaned up on quitting the app
    def __init__(self):
        self.resources: list[Resource] = []

    def add(self, resource: Resource) -> None:
        self.resources.append(resource)

    def cleanup(self):
        for resource in self.resources:
            print(f"Cleaning up resource: {resource.__class__.__name__}")
            resource.cleanup()


resources = Resources()
