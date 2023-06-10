from abc import ABC, abstractmethod


class VisualizationService(ABC):
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def load(self):
        pass
    