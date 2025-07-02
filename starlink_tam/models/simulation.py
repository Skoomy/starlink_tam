"""Simulation and Monte Carlo models for uncertainty analysis."""

from decimal import Decimal
from typing import Dict, List, Optional, Union

import numpy as np
from pydantic import BaseModel, Field, field_validator


class DistributionParams(BaseModel):
    """Parameters for probability distributions."""

    distribution_type: str = Field(
        ..., pattern="^(normal|lognormal|uniform|triangular|beta|gamma)$"
    )

    # Common parameters
    mean: Optional[float] = None
    std: Optional[float] = None

    # Uniform distribution
    min_val: Optional[float] = Field(None, alias="min")
    max_val: Optional[float] = Field(None, alias="max")

    # Triangular distribution
    mode: Optional[float] = None

    # Beta distribution
    alpha: Optional[float] = None
    beta: Optional[float] = None
    scale: Optional[float] = 1.0

    # Gamma distribution
    shape: Optional[float] = None
    scale_gamma: Optional[float] = Field(None, alias="scale")

    @field_validator("std")
    def validate_std_positive(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v <= 0:
            raise ValueError("Standard deviation must be positive")
        return v

    def sample(self, size: int = 1) -> Union[float, np.ndarray]:
        """Generate random samples from the distribution."""
        if self.distribution_type == "normal":
            return np.random.normal(self.mean, self.std, size)
        elif self.distribution_type == "lognormal":
            return np.random.lognormal(self.mean, self.std, size)
        elif self.distribution_type == "uniform":
            return np.random.uniform(self.min_val, self.max_val, size)
        elif self.distribution_type == "triangular":
            return np.random.triangular(self.min_val, self.mode, self.max_val, size)
        elif self.distribution_type == "beta":
            return np.random.beta(self.alpha, self.beta, size) * self.scale
        elif self.distribution_type == "gamma":
            return np.random.gamma(self.shape, self.scale_gamma, size)
        else:
            raise ValueError(f"Unsupported distribution: {self.distribution_type}")


class MonteCarloConfig(BaseModel):
    """Configuration for Monte Carlo simulation."""

    n_simulations: int = Field(default=10000, ge=100, le=1000000)
    random_seed: Optional[int] = None
    confidence_levels: List[float] = Field(default=[0.05, 0.25, 0.5, 0.75, 0.95])

    # Parameter distributions
    parameter_distributions: Dict[str, DistributionParams]

    # Correlation matrix (parameter names as keys)
    correlations: Optional[Dict[str, Dict[str, float]]] = None

    # Output configuration
    save_detailed_results: bool = True
    output_percentiles: List[float] = Field(default=[1, 5, 10, 25, 50, 75, 90, 95, 99])

    @field_validator("confidence_levels")
    def validate_confidence_levels(cls, v):
        for level in v:
            if not 0 < level < 1:
                raise ValueError("Confidence levels must be between 0 and 1")
        return sorted(v)


class SimulationResults(BaseModel):
    """Results from Monte Carlo simulation."""

    # Simulation metadata
    config: MonteCarloConfig
    n_simulations_completed: int
    execution_time_seconds: float

    # Key metrics statistics
    global_tam_statistics: Dict[str, float]  # mean, std, percentiles
    global_sam_statistics: Dict[str, float]
    global_som_statistics: Dict[str, float]

    # Country-level results (top N countries)
    country_tam_statistics: Dict[str, Dict[str, float]]

    # Segment-level results
    segment_tam_statistics: Dict[str, Dict[str, float]]

    # Risk metrics
    probability_of_loss: float = Field(..., ge=0, le=1)
    value_at_risk: Dict[str, Decimal]  # VaR at different confidence levels
    expected_shortfall: Dict[str, Decimal]  # ES at different confidence levels

    # Sensitivity analysis
    parameter_correlations: Dict[str, float]  # correlation with TAM
    tornado_chart_data: List[Dict[str, Union[str, float]]]

    # Scenario analysis
    best_case_scenario: Dict[str, float]
    worst_case_scenario: Dict[str, float]
    base_case_scenario: Dict[str, float]

    # Distribution characteristics
    tam_distribution_moments: Dict[str, float]  # mean, variance, skewness, kurtosis

    def get_confidence_interval(
        self, metric: str, confidence_level: float
    ) -> tuple[float, float]:
        """Get confidence interval for a specific metric."""
        if metric in self.global_tam_statistics:
            lower_pct = (1 - confidence_level) / 2 * 100
            upper_pct = (1 + confidence_level) / 2 * 100

            stats = self.global_tam_statistics
            return stats[f"p{lower_pct}"], stats[f"p{upper_pct}"]
        else:
            raise ValueError(f"Metric '{metric}' not found in results")

    def get_exceedance_probability(self, metric: str, threshold: float) -> float:
        """Calculate probability that metric exceeds threshold."""
        # This would need access to raw simulation data
        # For now, approximate using percentiles
        stats = getattr(self, f"{metric}_statistics", {})

        # Find closest percentiles
        percentiles = [
            float(k.replace("p", "")) for k in stats.keys() if k.startswith("p")
        ]
        percentiles.sort()

        for pct in percentiles:
            if stats[f"p{pct}"] >= threshold:
                return (100 - pct) / 100

        return 0.0  # All values below threshold
