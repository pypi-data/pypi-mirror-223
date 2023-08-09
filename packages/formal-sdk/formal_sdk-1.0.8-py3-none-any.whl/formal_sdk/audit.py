import grpc


from .gen.admin.v1.audit_pb2 import (
	GetLogsRequest,
	GetLogsResponse,
	GetEventBySessionRequest,
	GetEventBySessionResponse,
	EventData,
	GetDataBySessionRequest,
	SshData,
	GetDataBySessionResponse,
)

from .gen.admin.v1.audit_pb2_grpc import AuditLogsServiceStub
class AuditLogsService:
	def __init__(self, base_url, token):
		self.base_url = base_url
		self.channel = grpc.secure_channel(self.base_url, grpc.ssl_channel_credentials())
		self.stub = AuditLogsServiceStub(self.channel)
		self.headers = [('x-api-key', token)]

	def GetLogs(self, request: GetLogsRequest) -> GetLogsResponse:
		return self.stub.GetLogs(request, metadata=self.headers)

	def GetEventBySession(self, request: GetEventBySessionRequest) -> GetEventBySessionResponse:
		return self.stub.GetEventBySession(request, metadata=self.headers)

	def GetDataBySession(self, request: GetDataBySessionRequest) -> GetDataBySessionResponse:
		return self.stub.GetDataBySession(request, metadata=self.headers)

