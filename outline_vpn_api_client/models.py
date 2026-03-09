import re
from typing import Optional

from pydantic import BaseModel, field_validator

class AccessKeyDataLimit(BaseModel):
    bytes: int

class Server(BaseModel):
    name: str
    serverId: str
    metricsEnabled: bool
    createdTimestampMs: int
    version: str
    accessKeyDataLimit: Optional[AccessKeyDataLimit] = None
    portForNewAccessKeys: int
    hostnameForAccessKeys: str

class AccessKey(BaseModel):
    id: str
    name: str
    password: str
    port: int
    method: str
    dataLimit: Optional[AccessKeyDataLimit] = None
    accessUrl: str

    @field_validator("accessUrl", mode="before")
    def validate_access_url(cls, value):
        pattern = re.compile(r"^ss://[\w\-:]+@[\w\-\.]+:\d+/.+$")
        if not pattern.match(value):
            raise ValueError("Invalid accessUrl format")
        return value
    
class Metrics(BaseModel): 
    enabled: bool

class AccessKeyList(BaseModel):
    accessKeys: list[AccessKey]

class BytesTransferredByUserId(BaseModel):
    bytesTransferredByUserId: dict[str, int]

class Info(BaseModel):
    server: Server
    metrics: Metrics
    access_keys: AccessKeyList


# --- Experimental server metrics models ---

class DataTransferred(BaseModel):
    bytes: int

class TunnelTime(BaseModel):
    seconds: float

class BandwidthSnapshot(BaseModel):
    data: DataTransferred
    timestamp: int

class Bandwidth(BaseModel):
    current: BandwidthSnapshot
    peak: BandwidthSnapshot

class LocationMetrics(BaseModel):
    location: Optional[str] = None
    asn: Optional[int] = None
    asOrg: Optional[str] = None
    tunnelTime: Optional[TunnelTime] = None
    dataTransferred: Optional[DataTransferred] = None

class PeakDeviceCount(BaseModel):
    data: int
    timestamp: int

class AccessKeyConnection(BaseModel):
    lastTrafficSeen: Optional[float] = None
    peakDeviceCount: Optional[PeakDeviceCount] = None

class AccessKeyMetrics(BaseModel):
    accessKeyId: int
    tunnelTime: Optional[TunnelTime] = None
    dataTransferred: Optional[DataTransferred] = None
    connection: Optional[AccessKeyConnection] = None

class ServerMetricsData(BaseModel):
    tunnelTime: Optional[TunnelTime] = None
    dataTransferred: Optional[DataTransferred] = None
    bandwidth: Optional[Bandwidth] = None
    locations: Optional[list[LocationMetrics]] = None

class ServerMetrics(BaseModel):
    server: ServerMetricsData
    accessKeys: list[AccessKeyMetrics]