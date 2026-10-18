"""
Data models used by the CardioTwin API.

These models define the structure of information
that can be exchanged between CardioTwin components.
"""

from typing import Any

from pydantic import BaseModel, Field


class PatientData(BaseModel):
    """Structured patient information for the prototype."""

    patient_id: str = Field(
        default="demo-patient",
        min_length=1,
    )

    profile: dict[str, Any] = Field(
        default_factory=dict,
    )

    symptoms: list[str] = Field(
        default_factory=list,
    )

    measurements: dict[str, Any] = Field(
        default_factory=dict,
    )

    lifestyle: dict[str, Any] = Field(
        default_factory=dict,
    )

    environment: dict[str, Any] = Field(
        default_factory=dict,
    )

    medical_history: list[dict[str, Any]] = Field(
        default_factory=list,
    )

    is_demo_data: bool = True