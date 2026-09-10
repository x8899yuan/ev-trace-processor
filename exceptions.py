class TraceProcessorError(Exception):
    """Base exception for trace-processing errors."""


class VolumeDiscoveryError(TraceProcessorError):
    """Raised when split volumes cannot be discovered or verified."""


class ArchiveMergeError(TraceProcessorError):
    """Raised when split volumes cannot be merged."""


class ArchiveValidationError(TraceProcessorError):
    """Raised when 7-Zip reports an invalid or incomplete archive."""


class ArchiveExtractionError(TraceProcessorError):
    """Raised when an archive cannot be extracted."""
