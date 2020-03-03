from abc import abstractmethod, ABCMeta


class BaseModelConfig(metaclass=ABCMeta):

    @abstractmethod
    def name(self):
        raise NotImplementedError
