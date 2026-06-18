import typing
import struct
import uuid

from .rect import Rect


MASKS = [1 << j for j in range(8)]
INT_TO_BITS_CACHE = [tuple(bool(i & m) for m in MASKS) for i in range(256)]


class FileReader:
    """Helper class for deserializing a Terraria world file with context management."""

    __slots__ = (
        "stream",
        "_should_close",
    )

    def __init__(self, file_or_path: typing.Union[typing.BinaryIO, str]) -> None:
        if isinstance(file_or_path, str):
            # If a string is passed, we will open it and mark it for closing
            self.stream: typing.BinaryIO = open(file_or_path, "rb")
            self._should_close = True
        else:
            # If a file object is passed, we use it as is
            self.stream: typing.BinaryIO = file_or_path
            self._should_close = False

    def __enter__(self):
        """Returns the instance itself when entering the 'with' block."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Closes the file automatically when exiting the block."""
        if self._should_close:
            self.stream.close()

    _bool = struct.Struct("<?").unpack
    _int1 = struct.Struct("<b").unpack
    _uint1 = struct.Struct("<B").unpack
    _int2 = struct.Struct("<h").unpack
    _uint2 = struct.Struct("<H").unpack
    _int4 = struct.Struct("<i").unpack
    _uint4 = struct.Struct("<I").unpack
    _int8 = struct.Struct("<q").unpack
    _uint8 = struct.Struct("<Q").unpack
    _single = struct.Struct("<f").unpack
    _double = struct.Struct("<d").unpack
    _rect = struct.Struct("<iiii").unpack

    def bool(self) -> bool:
        return self._bool(self.stream.read(1))[0]

    def int1(self) -> int:
        return self._int1(self.stream.read(1))[0]

    def uint1(self) -> int:
        return self._uint1(self.stream.read(1))[0]

    def int2(self) -> int:
        return self._int2(self.stream.read(2))[0]

    def uint2(self) -> int:
        return self._uint2(self.stream.read(2))[0]

    def int4(self) -> int:
        return self._int4(self.stream.read(4))[0]

    def uint4(self) -> int:
        return self._uint4(self.stream.read(4))[0]

    def int8(self) -> int:
        return self._int8(self.stream.read(8))[0]

    def uint8(self) -> int:
        return self._uint8(self.stream.read(8))[0]

    def single(self) -> float:
        return self._single(self.stream.read(4))[0]

    def double(self) -> float:
        return self._double(self.stream.read(8))[0]

    def bits(self) -> tuple[bool, ...]:
        data = self._int1(self.stream.read(1))[0]
        return INT_TO_BITS_CACHE[data]

    def rect(self) -> Rect:
        left, right, top, bottom = self._rect(self.stream.read(16))
        return Rect(left, right, top, bottom)

    def uleb128(self) -> int:
        value = 0
        shift = 0
        while True:
            byte = self.uint1()
            value |= (byte & 0x7F) << shift
            if not (byte & 0x80):
                break
            shift += 7
        return value

    def string(self, size: int | None = None) -> str:
        if size is None:
            size = self.uleb128()
        return str(self.stream.read(size), encoding="utf-8")

    def peek(self, size: int = 0):
        if not self.seekable():
            return None
        pos: int = self.tell()
        peek = self.stream.read(size)
        self.skip_until(pos)
        return peek

    def uuid(self) -> uuid.UUID:
        uuid_bytes = self.stream.read(16)
        return uuid.UUID(bytes_le=uuid_bytes)

    def read_until(self, address: int) -> bytearray:
        current = self.stream.tell()
        if current > address:
            raise ValueError(
                f"Target address {address} is behind current position {current}"
            )
        return bytearray(self.stream.read(address - current))

    def tell(self) -> int:
        """Return the current stream position."""
        return self.stream.tell()

    def seekable(self) -> bool:
        """Return True if the stream supports random access."""
        return self.stream.seekable()

    def seek(self, target: int, whence: int = 0) -> None:
        self.stream.seek(target, whence)

    def __repr__(self):
        return f"<FileReader at {self.tell():02x}>"
