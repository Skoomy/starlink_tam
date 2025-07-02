"""Config models using Pydantic for Starlink TAM project."""

from typing import Dict, List

from pydantic import BaseModel


class ModelConfig(BaseModel):
    satellites_total: int
    bandwidth_per_satellite_mbps: int
    oversubscription_ratio: float
    minimum_bandwidth_per_user_mbps: int
    gdp_fraction_willingness_to_pay: float


class DistributionConfig(BaseModel):
    satellites_total: Dict[str, float]
    bandwidth_per_satellite_mbps: Dict[str, float]
    oversubscription_ratio: Dict[str, float]
    minimum_bandwidth_per_user_mbps: Dict[str, float]
    gdp_fraction_willingness_to_pay: Dict[str, float]


class ScenarioConfig(BaseModel):
    name: str
    description: str
    config: ModelConfig


class ValidationConfig(BaseModel):
    rules: List[str]
    thresholds: Dict[str, float]
