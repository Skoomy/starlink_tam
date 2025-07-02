"""Country data models for Starlink TAM analysis."""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class CountryData(BaseModel):
    """Core country data for TAM modeling."""

    # Basic identifiers
    country_code: str = Field(..., min_length=2, max_length=3)
    country_name: str = Field(..., min_length=1)
    region: str
    income_group: str

    # Geographic data
    land_area_km2: float = Field(..., gt=0)
    land_area_pct: float = Field(..., ge=0, le=1)

    # Population data
    population_total: int = Field(..., gt=0)
    population_rural: int = Field(..., ge=0)
    population_urban: int = Field(..., ge=0)
    population_density_per_km2: float = Field(..., ge=0)

    # Economic indicators
    gdp_total_usd: Decimal = Field(..., gt=0)
    gdp_per_capita_usd: Decimal = Field(..., gt=0)
    gdp_per_capita_monthly: Decimal = Field(..., gt=0)
    gni_per_capita_atlas_usd: Optional[Decimal] = Field(None, gt=0)

    # Infrastructure metrics
    internet_penetration_pct: float = Field(..., ge=0, le=1)
    mobile_penetration_pct: float = Field(..., ge=0, le=2)  # Can exceed 100%
    fixed_broadband_penetration_pct: float = Field(..., ge=0, le=1)
    avg_broadband_speed_mbps: Optional[float] = Field(None, gt=0)

    # Market readiness indicators
    ease_of_doing_business_rank: Optional[int] = Field(None, ge=1)
    regulatory_quality_score: Optional[float] = Field(None, ge=-2.5, le=2.5)

    # Data quality metadata
    data_vintage: datetime
    data_source: str
    confidence_score: float = Field(default=1.0, ge=0, le=1)

    @field_validator("population_urban", "population_rural")
    def validate_population_consistency(cls, v: int, values: dict) -> int:
        """Ensure urban + rural <= total population."""
        if "population_total" in values:
            total = values["population_total"]
            if "population_urban" in values and "population_rural" in values:
                if (
                    values["population_urban"] + values["population_rural"]
                    > total * 1.05
                ):  # 5% tolerance
                    raise ValueError("Urban + rural population exceeds total")
        return v

    @field_validator("gdp_per_capita_monthly")
    def calculate_monthly_gdp(cls, v: Decimal, values: dict) -> Decimal:
        """Auto-calculate monthly GDP if not provided."""
        if v == 0 and "gdp_per_capita_usd" in values:
            return values["gdp_per_capita_usd"] / 12
        return v


class CountryMetrics(BaseModel):
    """Calculated metrics for country analysis."""

    country_code: str

    # Market size metrics
    addressable_population: int
    rural_underserved_population: int
    urban_underserved_population: int

    # Economic accessibility
    affordability_index: float = Field(..., ge=0, le=1)
    purchasing_power_score: float = Field(..., ge=0)

    # Infrastructure gaps
    broadband_gap_mbps: float = Field(..., ge=0)
    connectivity_gap_pct: float = Field(..., ge=0, le=1)

    # Market attractiveness scores
    market_readiness_score: float = Field(..., ge=0, le=10)
    regulatory_risk_score: float = Field(..., ge=0, le=10)
    competitive_intensity_score: float = Field(..., ge=0, le=10)

    # TAM calculations
    satellite_allocation: float = Field(..., ge=0)
    bandwidth_capacity_mbps: float = Field(..., ge=0)
    max_subscribers: int = Field(..., ge=0)
    optimal_price_usd: Decimal = Field(..., gt=0)
    addressable_revenue_usd: Decimal = Field(..., ge=0)

    # Risk adjustments
    penetration_rate_assumption: float = Field(..., ge=0, le=1)
    risk_adjusted_revenue_usd: Decimal = Field(..., ge=0)
    confidence_interval_lower: Decimal = Field(..., ge=0)
    confidence_interval_upper: Decimal = Field(..., ge=0)
