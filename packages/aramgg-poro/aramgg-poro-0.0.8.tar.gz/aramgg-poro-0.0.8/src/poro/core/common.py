from typing import Mapping
from abc import abstractclassmethod

class CoreObject:

    def __init__(self, **kwargs):
        self(**kwargs)
            
    @property
    @abstractclassmethod
    def _renamed(cls) -> Mapping[str, str]:
        pass

    def __call__(self, **kwargs):
        for key, value in kwargs.items():
            new_key = self._renamed.get(key, key)
            setattr(self, new_key, value)
        return self
    
    def to_dict(self):
        d = {}
        attrs = {attrname for attrname in dir(self)} - {
            attrname for attrname in dir(self.__class__)
        }
        for attr in attrs:
            v = getattr(self, attr)
            if isinstance(v, CoreObject):
                v = v.to_dict()
            elif hasattr(v, "__iter__") and not isinstance(v, str):
                if isinstance(v, dict):
                    new_v = {}
                    for k, vi in v.items():
                        if isinstance(vi, CoreObject):
                            new_v[k] = vi.to_dict()
                        else:
                            new_v[k] = vi
                    v = new_v
                else:
                    v = [vi.to_dict() if isinstance(vi, CoreObject) else vi for vi in v]
            d[attr] = v
        return d
        

class CoreObjectList(list, CoreObject):
    def __str__(self):
        return list.__str__(self)
    
    def __init__(self, *args, **kwargs):
        list.__init__(self, *args)
        CoreObject.__init__(self, **kwargs)
        
class PoroGhost:
    def __init__(self, **kwargs):
        from .. import configuration
        self._data = {_type: None for _type in self._core_types}

        for _type in self._core_types:
            if "_dto_type" in dir(_type):
                self._data[_type] = configuration._pipeline.construct(_type, **kwargs)

    def __str__(self) -> str:
        result = {}
        for _type, data in self._data.items():
            result[str(_type)] = str(data)
        return str(result).replace("\\'", "'")
    
    def __call__(self, **kwargs):
        from .. import configuration
        self._data = {_type: None for _type in self._core_types}

        for _type in self._core_types:
            if "_dto_type" in dir(_type):
                self._data[_type] = configuration._pipeline.construct(_type, **kwargs)
        
        return self
    
    @classmethod
    def from_data(cls, data: CoreObject):
        assert data is not None
        self = cls()

        if data.__class__ not in self._core_types:
            raise TypeError(
                f"Wrong data type '{data.__class__.__name__}' passed to '{self.__class__.__name__}.from_data'"
            )
        self._data[data.__class__] = data
        return self
    
    def to_dict(self) -> dict:
        d = {}
        for _type in self._core_types:
            new = self._data[_type].to_dict()
            d.update(new)
        return d