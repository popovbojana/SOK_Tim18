from abc import ABC, abstractmethod


class GraphLoadingService(ABC):

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def load_graph(self, path: str):
        pass
