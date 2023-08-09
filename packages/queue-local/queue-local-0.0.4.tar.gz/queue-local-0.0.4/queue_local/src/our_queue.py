from abc import ABC, abstractmethod


class OurQueue(ABC):

    @abstractmethod
    def push(self, item):
        """push to the queue"""
        pass

    @abstractmethod
    def get(self):
        """get from the queue (and delete)"""
        pass

    @abstractmethod
    def peek(self):
        """get the head of the queue (without deleting)"""
        pass
