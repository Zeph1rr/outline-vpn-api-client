import re
from typing import Optional

from pydantic import BaseModel, field_validator


class AccessKeyDataLimit(BaseModel):
    """Represents a data transfer limit in bytes."""

    bytes: int
    """Data transfer limit in bytes."""


class Server(BaseModel):
    """Represents the Outline VPN server configuration and current state."""

    name: str
    """Human-readable name of the server."""
    serverId: str
    """Unique identifier of the server."""
    metricsEnabled: bool
    """Whether metrics sharing is enabled."""
    createdTimestampMs: int
    """Server creation timestamp in milliseconds since epoch."""
    version: str
    """Outline server version."""
    accessKeyDataLimit: Optional[AccessKeyDataLimit] = None
    """Default data transfer limit applied to all access keys, if set."""
    portForNewAccessKeys: int
    """Default port assigned to newly created access keys."""
    hostnameForAccessKeys: str
    """Hostname or IP address used in access key URLs."""


class AccessKey(BaseModel):
    """Represents an Outline VPN access key."""

    id: str
    """Unique identifier of the access key."""
    name: str
    """Human-readable name of the access key."""
    password: str
    """Password used for the Shadowsocks connection."""
    port: int
    """Port used for the Shadowsocks connection."""
    method: str
    """Encryption method used for the Shadowsocks connection."""
    dataLimit: Optional[AccessKeyDataLimit] = None
    """Data transfer limit for this key, if set."""
    accessUrl: str
    """Shadowsocks URL used to configure VPN clients."""

    @field_validator("accessUrl", mode="before")
    def validate_access_url(cls, value):
        pattern = re.compile(r"^ss://[\w\-:]+@[\w\-\.]+:\d+/.+$")
        if not pattern.match(value):
            raise ValueError("Invalid accessUrl format")
        return value


class Metrics(BaseModel):
    """Represents the metrics sharing status of the server."""

    enabled: bool
    """Whether metrics sharing is currently enabled."""


class AccessKeyList(BaseModel):
    """Represents a list of access keys."""

    accessKeys: list[AccessKey]
    """List of all access keys on the server."""


class BytesTransferredByUserId(BaseModel):
    """Represents data transfer statistics per access key."""

    bytesTransferredByUserId: dict[str, int]
    """Mapping of access key ID to total bytes transferred."""


class Info(BaseModel):
    """Aggregated information about the Outline server, its metrics, and access keys."""

    server: Server
    """Server configuration and state."""
    metrics: Metrics
    """Metrics sharing status."""
    access_keys: AccessKeyList
    """List of all access keys."""


# --- Experimental server metrics models ---

class DataTransferred(BaseModel):
    """Represents an amount of transferred data."""

    bytes: int
    """Total data transferred in bytes."""


class TunnelTime(BaseModel):
    """Represents the total time a tunnel was active."""

    seconds: float
    """Total tunnel time in seconds."""


class BandwidthSnapshot(BaseModel):
    """Represents a bandwidth measurement at a specific point in time."""

    data: DataTransferred
    """Bandwidth data at this snapshot."""
    timestamp: int
    """Unix timestamp of the snapshot."""


class Bandwidth(BaseModel):
    """Represents current and peak bandwidth measurements."""

    current: BandwidthSnapshot
    """Most recent bandwidth measurement."""
    peak: BandwidthSnapshot
    """Peak bandwidth measurement over the observed period."""


class LocationMetrics(BaseModel):
    """Represents metrics aggregated by geographic location."""

    location: Optional[str] = None
    """ISO country code of the location."""
    asn: Optional[int] = None
    """Autonomous System Number of the location."""
    asOrg: Optional[str] = None
    """Name of the autonomous system organization."""
    tunnelTime: Optional[TunnelTime] = None
    """Total tunnel time for this location."""
    dataTransferred: Optional[DataTransferred] = None
    """Total data transferred from this location."""


class PeakDeviceCount(BaseModel):
    """Represents the peak number of connected devices at a point in time."""

    data: int
    """Peak number of connected devices."""
    timestamp: int
    """Unix timestamp when the peak was observed."""


class AccessKeyConnection(BaseModel):
    """Represents connection statistics for a single access key."""

    lastTrafficSeen: Optional[float] = None
    """Unix timestamp of the last observed traffic for this key."""
    peakDeviceCount: Optional[PeakDeviceCount] = None
    """Peak number of devices connected using this key."""


class AccessKeyMetrics(BaseModel):
    """Represents detailed metrics for a single access key."""

    accessKeyId: int
    """Unique identifier of the access key."""
    tunnelTime: Optional[TunnelTime] = None
    """Total tunnel time for this key."""
    dataTransferred: Optional[DataTransferred] = None
    """Total data transferred by this key."""
    connection: Optional[AccessKeyConnection] = None
    """Connection statistics for this key."""


class ServerMetricsData(BaseModel):
    """Represents aggregated metrics for the entire server."""

    tunnelTime: Optional[TunnelTime] = None
    """Total tunnel time across all access keys."""
    dataTransferred: Optional[DataTransferred] = None
    """Total data transferred across all access keys."""
    bandwidth: Optional[Bandwidth] = None
    """Current and peak bandwidth measurements."""
    locations: Optional[list[LocationMetrics]] = None
    """Metrics broken down by geographic location."""


class ServerMetrics(BaseModel):
    """Represents the full response from the experimental server metrics endpoint."""

    server: ServerMetricsData
    """Aggregated server-level metrics."""
    accessKeys: list[AccessKeyMetrics]
    """Per-access-key metrics."""