"""
SVTRAF: Structured Vulnerability Taxonomy and Risk Assessment Framework
Version 1.0.0

A blockchain-specific scoring framework for smart contract vulnerability assessment.
Validated on 150 stratified smart contracts against real financial-loss ground truth.

Author: Udhaya Kumar Palani
Institution: National College of Ireland
"""

__version__ = "1.0.0"
__author__ = "Udhaya Kumar Palani"

from .scoring import SVTRAFScorer
from .validation import ValidationMetrics

__all__ = [
    "SVTRAFScorer",
    "ValidationMetrics",
    "__version__",
    "__author__",
]
