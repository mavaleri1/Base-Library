"""Pydantic models for Artifacts Service."""

from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any

from pydantic import BaseModel, Field


class FileInfo(BaseModel):
    """Information about a file in a session."""

    path: str = Field(description="Relative path to the file")
    size: int = Field(description="File size in bytes")
    modified: datetime = Field(description="Last modification time")
    content_type: str = Field(description="MIME content type")


class FileContent(BaseModel):
    """Request model for file content."""

    content: str = Field(description="File content as string")
    content_type: str = Field(default="text/markdown", description="MIME content type")
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional metadata"
    )


class SessionInfo(BaseModel):
    """Information about a session."""

    session_id: str = Field(description="Unique session identifier")
    input_content: str = Field(description="Exam question text")
    display_name: Optional[str] = Field(
        default=None, description="Short display name (3-5 words) for the session"
    )
    created: datetime = Field(description="Session creation time")
    modified: datetime = Field(description="Last modification time")
    status: str = Field(description="Session status (active, completed, failed)")
    files_count: int = Field(description="Number of files in session")


class SessionMetadata(BaseModel):
    """Complete session metadata."""

    session_id: str = Field(description="Unique session identifier")
    thread_id: str = Field(description="Thread identifier")
    input_content: str = Field(description="Exam question text")
    display_name: Optional[str] = Field(
        default=None, description="Short display name (3-5 words) for the session"
    )
    created: datetime = Field(description="Session creation time")
    modified: datetime = Field(description="Last modification time")
    status: str = Field(
        default="active", description="Session status (active, completed, failed)"
    )
    workflow_data: Optional[Dict[str, Any]] = Field(
        default=None, description="Data from GeneralState workflow"
    )


class ThreadInfo(BaseModel):
    """Information about a thread."""

    thread_id: str = Field(description="Unique thread identifier")
    sessions: List[SessionInfo] = Field(description="List of sessions in thread")
    created: datetime = Field(description="Thread creation time")
    last_activity: datetime = Field(description="Last activity timestamp")
    sessions_count: int = Field(description="Number of sessions in thread")


class ThreadMetadata(BaseModel):
    """Complete thread metadata."""

    thread_id: str = Field(description="Unique thread identifier")
    created: datetime = Field(description="Thread creation time")
    last_activity: datetime = Field(description="Last activity timestamp")
    sessions_count: int = Field(description="Number of sessions in thread")
    user_info: Optional[Dict[str, Any]] = Field(
        default=None, description="Information about the Telegram user"
    )


# Response models
class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field(description="Service status")
    service: str = Field(default="artifacts-service", description="Service name")
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Response timestamp"
    )


class ThreadsListResponse(BaseModel):
    """Response for threads list endpoint."""

    threads: List[ThreadInfo] = Field(description="List of threads")


class ThreadDetailResponse(BaseModel):
    """Response for thread detail endpoint."""

    thread_id: str = Field(description="Thread identifier")
    sessions: List[SessionInfo] = Field(description="List of sessions")
    created: datetime = Field(description="Thread creation time")
    last_activity: datetime = Field(description="Last activity timestamp")
    sessions_count: int = Field(description="Number of sessions")


class SessionFilesResponse(BaseModel):
    """Response for session files endpoint."""

    thread_id: str = Field(description="Thread identifier")
    session_id: str = Field(description="Session identifier")
    files: List[FileInfo] = Field(description="List of files in session")


class FileOperationResponse(BaseModel):
    """Response for file operations."""

    message: str = Field(description="Operation result message")
    path: Optional[str] = Field(default=None, description="File path")
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Operation timestamp"
    )


class ErrorResponse(BaseModel):
    """Error response."""

    error: str = Field(description="Error message")
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Error timestamp"
    )


# Export models
class ExportFormat(str, Enum):
    """Available export formats."""
    MARKDOWN = "markdown"
    PDF = "pdf"


class PackageType(str, Enum):
    """Types of export packages."""
    FINAL = "final"  # Only final documents
    ALL = "all"      # All documents including intermediate


class ExportSettings(BaseModel):
    """User export settings."""
    
    user_id: str = Field(description="User identifier")
    default_format: ExportFormat = Field(
        default=ExportFormat.MARKDOWN,
        description="Default export format"
    )
    default_package_type: PackageType = Field(
        default=PackageType.FINAL,
        description="Default package type"
    )
    created: datetime = Field(default_factory=datetime.now)
    modified: datetime = Field(default_factory=datetime.now)


class SessionSummary(BaseModel):
    """Summary of a session for export."""
    
    thread_id: str = Field(description="Thread identifier")
    session_id: str = Field(description="Session identifier")
    input_content: str = Field(description="Original exam question")
    question_preview: str = Field(description="First 30 characters of question")
    display_name: str = Field(description="Formatted name for display")
    created_at: datetime = Field(description="Session creation time")
    has_synthesized: bool = Field(default=False, description="Has synthesized material")
    has_questions: bool = Field(default=False, description="Has gap questions")
    answers_count: int = Field(default=0, description="Number of answers")


class ExportRequest(BaseModel):
    """Export request parameters."""
    
    document_names: Optional[List[str]] = Field(
        default=None,
        description="Specific documents to export"
    )
    format: ExportFormat = Field(
        default=ExportFormat.MARKDOWN,
        description="Export format"
    )
    package_type: PackageType = Field(
        default=PackageType.FINAL,
        description="Package type for batch export"
    )


# Material update models
class MaterialUpdateRequest(BaseModel):
    """Request model for updating a material."""
    
    title: Optional[str] = Field(default=None, max_length=255, description="Material title")
    content: Optional[str] = Field(default=None, max_length=1000000, description="Material content (markdown)")
    subject: Optional[str] = Field(default=None, max_length=100, description="Subject area")
    grade: Optional[str] = Field(default=None, max_length=50, description="Grade level")
    topic: Optional[str] = Field(default=None, max_length=255, description="Specific topic")
    status: Optional[str] = Field(default=None, description="Material status: draft, published, archived")


class MaterialDeleteResponse(BaseModel):
    """Response model for material deletion."""
    
    success: bool = Field(description="Operation success status")
    message: str = Field(description="Success or error message")


# Leaderboard models
class LeaderboardEntry(BaseModel):
    """Response model for a single leaderboard entry."""
    
    rank: int = Field(description="Position in leaderboard")
    walletAddress: str = Field(description="User wallet address")
    materialsCount: int = Field(description="Number of materials created")
    nftCount: int = Field(description="Number of minted NFTs")
    totalScore: int = Field(description="Total score (materials + NFTs)")


class LeaderboardResponse(BaseModel):
    """Response model for leaderboard endpoint."""
    
    entries: List[LeaderboardEntry] = Field(description="List of leaderboard entries")
    total: int = Field(description="Total number of users with materials")
    page: int = Field(description="Current page number")
    page_size: int = Field(description="Page size")