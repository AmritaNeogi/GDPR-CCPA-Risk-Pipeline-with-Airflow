"""
gdpr_pipeline package

End-to-end GDPR/CCPA risk analytics pipeline.

This package provides helpers to:
- Fetch raw policy updates from EDPB (and other regulators).
- Process and clean policy text for downstream analytics.
- Validate processed data files before use.
- Forecast policy volume and severity trends over time.

Typical usage:

    from gdpr_pipeline import (
        fetch_policy_data,
        process_policy_data,
        validate_latest_xml,
        forecast_policy_trends,
    )

You can then wire these functions into Airflow, scripts, or notebooks.
"""

from .fetch_policy_data import fetch_policy_data
from .process_policy_data import process_policy_data
from .validate_policy_data import validate_latest_xml
from .forecast_policy_trends import forecast_policy_trends

__all__ = [
    "fetch_policy_data",
    "process_policy_data",
    "validate_latest_xml",
    "forecast_policy_trends",
]

__version__ = "0.1.0"
