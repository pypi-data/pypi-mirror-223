from google.protobuf import timestamp_pb2 as _timestamp_pb2
from ...validate.v1 import validate_pb2 as _validate_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetApiKeysRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ApiKey(_message.Message):
    __slots__ = ["id", "name", "created_at"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    created_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class GetApiKeysResponse(_message.Message):
    __slots__ = ["api_keys"]
    API_KEYS_FIELD_NUMBER: _ClassVar[int]
    api_keys: _containers.RepeatedCompositeFieldContainer[ApiKey]
    def __init__(self, api_keys: _Optional[_Iterable[_Union[ApiKey, _Mapping]]] = ...) -> None: ...

class CreateApiKeyRequest(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class CreateApiKeyResponse(_message.Message):
    __slots__ = ["id", "name", "secret", "created_at"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SECRET_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    secret: str
    created_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., secret: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class DeleteApiKeyRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteApiKeyResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
