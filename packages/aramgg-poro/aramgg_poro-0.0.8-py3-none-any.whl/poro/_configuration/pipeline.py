from ..utils import dict_to_str

class PoroPipeline:
    def __init__(self):
        from ..transformers import _transformers
        from ..apis import _apis

        self._apiMap = {}
        self._tfMap = {}

        for api in _apis:
            for m in dir(api.__class__):
                if not m.startswith("_"):
                    self._apiMap[getattr(api, m).__annotations__["return"]] = {"api":api, "func":m}

        for tf in _transformers:
            for m in dir(tf.__class__):
                if not m.startswith("_"):
                    self._tfMap[getattr(tf, m).__annotations__["return"]] = {"tf":tf, "func":m}
    
    def set_riot_api_key(self, key:str):
        for _d in self._apiMap.values():
            _d["api"]._set_api_key(key)

    def construct(self, coreType, **kwargs):
        dto = self._get(coreType._dto_type, **kwargs)
        return self._transform(coreType, dto)

    def _get(self, dtoType, **kwargs):
        api = self._apiMap[dtoType]["api"]
        func = self._apiMap[dtoType]["func"]

        return getattr(api, func)(**kwargs)
    
    def _transform(self, coreType, dto):
        tf = self._tfMap[coreType]["tf"]
        func = self._tfMap[coreType]["func"]

        return getattr(tf, func)(dto)
    
    def __str__(self):
        return dict_to_str({"api":self._apiMap, "tf":self._tfMap})