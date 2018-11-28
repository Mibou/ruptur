from abc import ABCMeta, abstractmethod


class POI(metaclass=ABCMeta):

    @abstractmethod
    def get_tags(self):
        pass

    @abstractmethod
    def get_title(self):
        pass

    @abstractmethod
    def get_subtitle(self):
        pass

    @abstractmethod
    def get_latitude(self):
        pass

    @abstractmethod
    def get_longitude(self):
        pass

    @abstractmethod
    def get_icon(self):
        pass

    @abstractmethod
    def get_url(self):
        pass
