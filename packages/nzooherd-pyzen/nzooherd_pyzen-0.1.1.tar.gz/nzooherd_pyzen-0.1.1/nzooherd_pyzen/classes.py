# -*- coding: utf-8 -*-
# @Time    : 07/08/2023
# @Author  : nzooherd
# @File    : classes.py 
# @Software: PyCharm
# -*- coding: utf-8 -*-

def single_instance(clazz: type) -> type:
    """
    Decorator to make a class a singleton.
    """
    class Singleton:

        delegate_clazz = clazz

        instance = None
        delegate_instance = None

        def __init__(self, *args, **kwargs):
            self.delegate_instance.__init__(*args, **kwargs)

        def __new__(cls, *args, **kwargs):
            if cls.instance is None:
                cls.instance = super().__new__(cls)
                cls.delegate_instance = cls.delegate_clazz.__new__(cls.delegate_clazz, *args, **kwargs)
            return cls.instance

        def __getattr__(self, item):
            return getattr(self.delegate_instance, item)

    return Singleton

