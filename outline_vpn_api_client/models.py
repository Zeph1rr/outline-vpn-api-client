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