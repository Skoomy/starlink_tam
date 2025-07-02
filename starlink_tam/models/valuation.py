"""Valuation models for hedge fund quality financial analysis."""

from decimal import Decimal
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class ValuationMetrics(BaseModel):
    """Comprehensive valuation metrics for Starlink TAM analysis."""

    # Revenue metrics
    total_addressable_revenue: Decimal = Field(..., ge=0)
    serviceable_addressable_revenue: Decimal = Field(..., ge=0)
    serviceable_obtainable_revenue: Decimal = Field(..., ge=0)

    # Growth metrics
    revenue_cagr_5y: float = Field(..., ge=-1)
    revenue_cagr_10y: float = Field(..., ge=-1)
    customer_cagr_5y: float = Field(..., ge=-1)
    arpu_growth_rate: float = Field(..., ge=-1)

    # Profitability metrics
    gross_margin: float = Field(..., ge=0, le=1)
    ebitda_margin: float = Field(..., ge=-1, le=1)
    operating_margin: float = Field(..., ge=-1, le=1)
    net_margin: float = Field(..., ge=-1, le=1)

    # Capital efficiency
    asset_turnover: float = Field(..., ge=0)
    return_on_assets: float = Field(..., ge=-1)
    return_on_equity: float = Field(..., ge=-1)
    return_on_invested_capital: float = Field(..., ge=-1)

    # Cash flow metrics
    free_cash_flow: Decimal
    free_cash_flow_yield: float = Field(..., ge=-1)
    cash_conversion_cycle: float
    capex_intensity: float = Field(..., ge=0, le=1)

    # Valuation multiples
    ev_revenue_multiple: float = Field(..., ge=0)
    ev_ebitda_multiple: float = Field(..., ge=0)
    price_to_earnings_multiple: Optional[float] = Field(None, ge=0)
    price_to_book_multiple: float = Field(..., ge=0)

    # DCF valuation
    terminal_value: Decimal = Field(..., ge=0)
    present_value_operations: Decimal = Field(..., ge=0)
    enterprise_value: Decimal = Field(..., ge=0)
    equity_value: Decimal = Field(..., ge=0)

    # Risk-adjusted metrics
    risk_adjusted_npv: Decimal
    value_at_risk_95: Decimal = Field(..., ge=0)
    expected_shortfall_95: Decimal = Field(..., ge=0)
    sharpe_ratio: Optional[float] = None

    # Market comparison
    peer_valuation_premium_discount: float = Field(..., ge=-1)
    market_cap_percentile: float = Field(..., ge=0, le=1)


class SensitivityAnalysis(BaseModel):
    """Sensitivity analysis for key valuation drivers."""

    # Base case
    base_case_valuation: Decimal = Field(..., ge=0)

    # Single variable sensitivity
    satellite_count_sensitivity: Dict[int, Decimal]  # satellite count -> valuation
    bandwidth_sensitivity: Dict[float, Decimal]  # bandwidth/sat -> valuation
    pricing_sensitivity: Dict[float, Decimal]  # price elasticity -> valuation
    penetration_sensitivity: Dict[float, Decimal]  # penetration rate -> valuation

    # Two-way sensitivity tables
    satellite_bandwidth_matrix: Dict[str, Dict[str, Decimal]]
    pricing_penetration_matrix: Dict[str, Dict[str, Decimal]]

    # Scenario analysis
    scenarios: Dict[str, "ScenarioValuation"]

    # Monte Carlo summary
    valuation_percentiles: Dict[str, Decimal]  # P5, P25, P50, P75, P95
    probability_distributions: Dict[str, List[float]]

    # Key driver analysis
    tornado_chart: List[Dict[str, float]]  # ordered by impact
    correlation_matrix: Dict[str, Dict[str, float]]

    # Risk metrics
    downside_risk_scenarios: List[Dict[str, float]]
    upside_opportunity_scenarios: List[Dict[str, float]]
    break_even_analysis: Dict[str, float]

    def get_impact_ranking(self) -> List[tuple[str, float]]:
        """Get sensitivity variables ranked by impact on valuation."""
        return [
            (str(item["variable"]), float(item["impact"]))
            for item in self.tornado_chart
        ]

    def calculate_value_at_risk(self, confidence_level: float = 0.05) -> Decimal:
        """Calculate Value at Risk at specified confidence level."""
        percentile_key = f"P{int((1-confidence_level)*100)}"
        return self.base_case_valuation - self.valuation_percentiles.get(
            percentile_key, Decimal(0)
        )


class ScenarioValuation(BaseModel):
    """Valuation under specific scenario assumptions."""

    scenario_name: str
    scenario_description: str
    probability_weight: float = Field(..., ge=0, le=1)

    # Key assumptions
    assumptions: Dict[str, float]

    # Valuation results
    tam_estimate: Decimal = Field(..., ge=0)
    sam_estimate: Decimal = Field(..., ge=0)
    som_estimate: Decimal = Field(..., ge=0)

    # Financial projections (10-year)
    revenue_projections: List[Decimal] = Field(..., min_length=10, max_length=10)
    ebitda_projections: List[Decimal] = Field(..., min_length=10, max_length=10)
    capex_projections: List[Decimal] = Field(..., min_length=10, max_length=10)
    free_cash_flow_projections: List[Decimal] = Field(..., min_length=10, max_length=10)

    # Valuation outputs
    discount_rate: float = Field(..., gt=0)
    terminal_growth_rate: float = Field(..., ge=-0.1, le=0.1)
    terminal_value: Decimal = Field(..., ge=0)
    present_value: Decimal = Field(..., ge=0)

    # Risk metrics for scenario
    scenario_risk_score: float = Field(..., ge=0, le=10)
    key_risks: List[str]
    mitigation_factors: List[str]


class MarketComparison(BaseModel):
    """Comparable company and market analysis."""

    # Peer universe
    peer_companies: List[str]
    peer_metrics: Dict[str, Dict[str, float]]  # company -> metric -> value

    # Market benchmarks
    sector_averages: Dict[str, float]
    market_averages: Dict[str, float]

    # Relative valuation
    relative_ev_revenue: float
    relative_ev_ebitda: float
    relative_price_earnings: Optional[float]

    # Quality scores
    business_quality_score: float = Field(..., ge=0, le=10)
    management_quality_score: float = Field(..., ge=0, le=10)
    competitive_position_score: float = Field(..., ge=0, le=10)

    # Strategic value
    strategic_option_value: Decimal = Field(..., ge=0)
    network_effect_value: Decimal = Field(..., ge=0)
    regulatory_moat_value: Decimal = Field(..., ge=0)
