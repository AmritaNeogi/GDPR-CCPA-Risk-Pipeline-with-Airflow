"""
gdpr_pipeline package

This package powers the GDPR–CCPA Risk Pipeline and exposes
clean, public functions for use in DAGs, notebooks, and apps.

Public API:
    from gdpr_pipeline import (
        fetch_policy_data,
        process_policy_data,
        forecast_policy_trends,
        validate_policy_data,   # only if the file exists
    )
"""

__version__ = "0.1.0"

from .fetch_policy_data import fetch_policy_data
from .process_policy_data import process_policy_data
from .forecast_policy_trends import forecast_policy_trends

# Optional import if you have validate_policy_data.py
try:
    from .validate_policy_data import validate_policy_data
except ImportError:
    validate_policy_data = None

__all__ = [
    "fetch_policy_data",
    "process_policy_data",
    "forecast_policy_trends",
    "validate_policy_data",
]
