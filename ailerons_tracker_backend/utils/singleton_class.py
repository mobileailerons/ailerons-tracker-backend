"""  Singleton Metaclass """


class Singleton(type):
    """ Create singletons by associating with a Base Class 

    Usage:
        MyClassSingleton(MyClassBase, metaclass=Singleton)

    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
