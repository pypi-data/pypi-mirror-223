import typing as t

PY: t.Tuple[int, int]
PY2: bool
PY3: bool
PYPY: bool
ONWINDOWS: bool

stringtypes: t.Tuple[t.Type[bytes], t.Type[str]]
integertypes: t.Tuple[t.Type[int]]
unicodestringtype: t.Type[str]
bytestringtype: t.Type[bytes]

def int2byte(character: int) -> bytes: ...
def byte2int(character: bytes) -> int: ...
def str2bytes(string: str) -> bytes: ...
def bytes2str(string: bytes) -> str: ...
def reprstring(data: t.Union[bytes, str]) -> str: ...
def trimstring(data: t.Union[bytes, str]) -> str: ...
def integers2bytes(ints: t.Iterable[int]) -> bytes: ...
def bytes2integers(data: bytes) -> list[int]: ...
