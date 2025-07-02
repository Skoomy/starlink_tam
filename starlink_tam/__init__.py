"""Starlink Total Addressable Market (TAM) Analysis Platform.

A hedge fund quality valuation platform for analyzing Starlink's market opportunity
with comprehensive risk modeling and professional reporting.
"""

__version__ = "2.0.0"
__author__ = "Team Artometrix"
__email__ = "contact@artometrix.com"

from .model.default_model import StarlinkTAMEngine
from .model.monte_carlo import MonteCarloRunner
from .models import (
    CountryData,
    MarketSegment,
    ModelConfig,
    MonteCarloConfig,
    SimulationResults,
    TAMResults,
)
from .utils import (
    DataLoader,
    TAMVisualizer,
    create_dashboard,
    get_logger,
    load_config,
    setup_logging,
)

__all__ = [
    "__version__",
    "StarlinkTAMEngine",
    "MonteCarloRunner",
    "ModelConfig",
    "CountryData",
    "TAMResults",
    "MarketSegment",
    "SimulationResults",
    "MonteCarloConfig",
    "setup_logging",
    "get_logger",
    "load_config",
    "DataLoader",
    "TAMVisualizer",
    "create_dashboard",
]
