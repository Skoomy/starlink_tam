"""Market analysis models for comprehensive TAM calculation."""

from decimal import Decimal
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class MarketSegment(str, Enum):
    """Market segments for Starlink services."""

    RESIDENTIAL_RURAL = "residential_rural"
    RESIDENTIAL_URBAN = "residential_urban"
    ENTERPRISE_SMB = "enterprise_smb"
    ENTERPRISE_LARGE = "enterprise_large"
    MOBILITY_MARITIME = "mobility_maritime"
    MOBILITY_AVIATION = "mobility_aviation"
    MOBILITY_AUTOMOTIVE = "mobility_automotive"
    GOVERNMENT = "government"
    EMERGENCY_SERVICES = "emergency_services"


class CustomerSegment(BaseModel):
    """Detailed customer segment analysis."""

    segment: MarketSegment
    addressable_customers: int = Field(..., ge=0)
    average_arpu_monthly_usd: Decimal = Field(..., gt=0)
    penetration_rate: float = Field(..., ge=0, le=1)
    churn_rate_annual: float = Field(..., ge=0, le=1)
    acquisition_cost_usd: Decimal = Field(..., ge=0)

    # Revenue calculations
    total_addressable_revenue_annual: Decimal = Field(..., ge=0)
    serviceable_addressable_revenue: Decimal = Field(..., ge=0)
    serviceable_obtainable_revenue: Decimal = Field(..., ge=0)

    # Competitive dynamics
    competitive_intensity: float = Field(..., ge=0, le=10)
    price_elasticity: float = Field(..., ge=-10, le=0)
    switching_cost_barrier: float = Field(..., ge=0, le=10)


class MarketAnalysis(BaseModel):
    """Comprehensive market analysis for a country/region."""

    country_code: str
    analysis_date: str
    currency: str = "USD"

    # Segment breakdown
    segments: Dict[MarketSegment, CustomerSegment]

    # Aggregate metrics
    total_addressable_market_usd: Decimal = Field(..., ge=0)
    serviceable_addressable_market_usd: Decimal = Field(..., ge=0)
    serviceable_obtainable_market_usd: Decimal = Field(..., ge=0)

    # Market dynamics
    market_growth_rate_annual: float = Field(..., ge=-1)
    competitive_pressure_score: float = Field(..., ge=0, le=10)
    regulatory_risk_score: float = Field(..., ge=0, le=10)

    # Infrastructure requirements
    required_satellites: int = Field(..., ge=0)
    required_ground_stations: int = Field(..., ge=0)
    infrastructure_capex_usd: Decimal = Field(..., ge=0)

    # Financial projections (5-year)
    revenue_projections: List[Decimal] = Field(..., min_length=5, max_length=5)
    customer_projections: List[int] = Field(..., min_length=5, max_length=5)
    market_share_projections: List[float] = Field(..., min_length=5, max_length=5)


class TAMResults(BaseModel):
    """Comprehensive TAM analysis results."""

    # Model metadata
    model_version: str
    analysis_timestamp: str
    scenario_name: str

    # Global aggregates
    global_tam_usd: Decimal = Field(..., ge=0)
    global_sam_usd: Decimal = Field(..., ge=0)
    global_som_usd: Decimal = Field(..., ge=0)

    # Geographic breakdown
    country_analyses: Dict[str, MarketAnalysis]

    # Segment aggregates
    segment_totals: Dict[MarketSegment, Decimal]

    # Key assumptions
    satellite_constellation_size: int = Field(..., ge=0)
    global_bandwidth_capacity_gbps: float = Field(..., ge=0)
    average_price_per_mbps_usd: Decimal = Field(..., gt=0)

    # Risk factors
    key_risks: List[str]
    sensitivity_factors: Dict[str, float]
    confidence_level: float = Field(..., ge=0, le=1)

    # Investment metrics
    required_capex_usd: Decimal = Field(..., ge=0)
    payback_period_years: Optional[float] = Field(None, gt=0)
    irr_estimate: Optional[float] = Field(None, ge=-1)
    npv_estimate_usd: Optional[Decimal] = None

    def get_top_markets(self, n: int = 10) -> List[tuple[str, Decimal]]:
        """Get top N markets by TAM."""
        return sorted(
            [
                (code, analysis.total_addressable_market_usd)
                for code, analysis in self.country_analyses.items()
            ],
            key=lambda x: x[1],
            reverse=True,
        )[:n]

    def get_segment_breakdown(self) -> Dict[str, float]:
        """Get percentage breakdown by segment."""
        total = sum(self.segment_totals.values())
        return (
            {
                segment.value: float(amount / total * 100)
                for segment, amount in self.segment_totals.items()
            }
            if total > 0
            else {}
        )
