from .types.v1 import policy_pb2 as _policy_pb2
from ...validate.v1 import validate_pb2 as _validate_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreatePolicySuggestionRequest(_message.Message):
    __slots__ = ["name", "description"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class CreatePolicySuggestionResponse(_message.Message):
    __slots__ = ["suggestion"]
    SUGGESTION_FIELD_NUMBER: _ClassVar[int]
    suggestion: str
    def __init__(self, suggestion: _Optional[str] = ...) -> None: ...

class DeletePolicyRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeletePolicyResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class EvaluatePolicyValidityRequest(_message.Message):
    __slots__ = ["code"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    code: str
    def __init__(self, code: _Optional[str] = ...) -> None: ...

class EvaluatePolicyValidityResponse(_message.Message):
    __slots__ = ["valid", "ast", "error"]
    VALID_FIELD_NUMBER: _ClassVar[int]
    AST_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    valid: bool
    ast: str
    error: str
    def __init__(self, valid: bool = ..., ast: _Optional[str] = ..., error: _Optional[str] = ...) -> None: ...

class CreatePolicyRequest(_message.Message):
    __slots__ = ["name", "description", "code", "notification", "owners", "source_type", "active"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATION_FIELD_NUMBER: _ClassVar[int]
    OWNERS_FIELD_NUMBER: _ClassVar[int]
    SOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    code: str
    notification: str
    owners: _containers.RepeatedScalarFieldContainer[str]
    source_type: str
    active: bool
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., code: _Optional[str] = ..., notification: _Optional[str] = ..., owners: _Optional[_Iterable[str]] = ..., source_type: _Optional[str] = ..., active: bool = ...) -> None: ...

class CreatePolicyResponse(_message.Message):
    __slots__ = ["policy"]
    POLICY_FIELD_NUMBER: _ClassVar[int]
    policy: _policy_pb2.Policy
    def __init__(self, policy: _Optional[_Union[_policy_pb2.Policy, _Mapping]] = ...) -> None: ...

class UpdatePolicyRequest(_message.Message):
    __slots__ = ["id", "source_type", "name", "description", "code", "notification", "owners", "active"]
    ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATION_FIELD_NUMBER: _ClassVar[int]
    OWNERS_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    id: str
    source_type: str
    name: str
    description: str
    code: str
    notification: str
    owners: _containers.RepeatedScalarFieldContainer[str]
    active: bool
    def __init__(self, id: _Optional[str] = ..., source_type: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., code: _Optional[str] = ..., notification: _Optional[str] = ..., owners: _Optional[_Iterable[str]] = ..., active: bool = ...) -> None: ...

class UpdatePolicyResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetPolicyRequest(_message.Message):
    __slots__ = ["policy_id"]
    POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    policy_id: str
    def __init__(self, policy_id: _Optional[str] = ...) -> None: ...

class GetPolicyResponse(_message.Message):
    __slots__ = ["policy"]
    POLICY_FIELD_NUMBER: _ClassVar[int]
    policy: _policy_pb2.Policy
    def __init__(self, policy: _Optional[_Union[_policy_pb2.Policy, _Mapping]] = ...) -> None: ...

class GetPoliciesRequest(_message.Message):
    __slots__ = ["limit", "cursor", "go_back"]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    GO_BACK_FIELD_NUMBER: _ClassVar[int]
    limit: int
    cursor: str
    go_back: bool
    def __init__(self, limit: _Optional[int] = ..., cursor: _Optional[str] = ..., go_back: bool = ...) -> None: ...

class GetPoliciesResponse(_message.Message):
    __slots__ = ["policies", "last_evaluated_key", "has_more"]
    POLICIES_FIELD_NUMBER: _ClassVar[int]
    LAST_EVALUATED_KEY_FIELD_NUMBER: _ClassVar[int]
    HAS_MORE_FIELD_NUMBER: _ClassVar[int]
    policies: _containers.RepeatedCompositeFieldContainer[_policy_pb2.Policy]
    last_evaluated_key: str
    has_more: bool
    def __init__(self, policies: _Optional[_Iterable[_Union[_policy_pb2.Policy, _Mapping]]] = ..., last_evaluated_key: _Optional[str] = ..., has_more: bool = ...) -> None: ...
