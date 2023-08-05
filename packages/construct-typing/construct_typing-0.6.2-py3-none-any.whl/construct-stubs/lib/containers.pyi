import re
import typing as t

ContainerType = t.TypeVar("ContainerType")
ListType = t.TypeVar("ListType")

SearchPattern = t.Union[t.AnyStr, re.Pattern[t.AnyStr]]

globalPrintFullStrings: bool
globalPrintFalseFlags: bool
globalPrintPrivateEntries: bool

def setGlobalPrintFullStrings(enabled: bool = ...) -> None: ...
def setGlobalPrintFalseFlags(enabled: bool = ...) -> None: ...
def setGlobalPrintPrivateEntries(enabled: bool = ...) -> None: ...
def recursion_lock(
    retval: str = ..., lock_name: str = ...
) -> t.Callable[[t.Callable[..., str]], t.Callable[..., str]]: ...

class Container(t.Generic[ContainerType], t.Dict[str, ContainerType]):
    def __getattr__(self, name: str) -> ContainerType: ...
    def update(
        self,
        seqordict: t.Union[t.Dict[str, ContainerType], t.Tuple[str, ContainerType]],
    ) -> None: ...
    def search(self, pattern: SearchPattern[t.Any]) -> t.Any: ...
    def search_all(self, pattern: SearchPattern[t.Any]) -> t.Any: ...

class ListContainer(t.List[ListType]):
    def search(self, pattern: SearchPattern[t.Any]) -> t.Any: ...
    def search_all(self, pattern: SearchPattern[t.Any]) -> t.Any: ...
