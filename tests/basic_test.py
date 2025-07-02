"""Basic tests for Starlink TAM platform."""

from datetime import datetime
from decimal import Decimal

import pytest

from starlink_tam.models.config import ModelConfig
from starlink_tam.models.country import CountryData
from starlink_tam.utils.data import DataLoader


def test_country_data_validation():
    """Test CountryData model validation."""
    country = CountryData(
        country_code="US",
        country_name="United States",
        region="North America",
        income_group="High income",
        land_area_km2=9_833_517,
        land_area_pct=0.066,
        population_total=331_900_000,
        population_rural=57_230_000,
        population_urban=274_670_000,
        population_density_per_km2=33.7,
        gdp_total_usd=Decimal("21_430_000_000_000"),
        gdp_per_capita_usd=Decimal("64_530"),
        gdp_per_capita_monthly=Decimal("5_377"),
        internet_penetration_pct=0.87,
        mobile_penetration_pct=1.27,
        fixed_broadband_penetration_pct=0.36,
        avg_broadband_speed_mbps=42.8,
        ease_of_doing_business_rank=6,
        regulatory_quality_score=1.21,
        data_vintage=datetime(2023, 1, 1),
        data_source="World Bank, ITU, Speedtest",
    )

    assert country.country_code == "US"
    assert country.population_total > 0
    assert 0 <= country.internet_penetration_pct <= 1


def test_model_config_validation():
    """Test ModelConfig validation."""
    config = ModelConfig(
        satellites_total=12000,
        bandwidth_per_satellite_mbps=17,
        oversubscription_ratio=20.0,
        minimum_bandwidth_per_user_mbps=20,
        gdp_fraction_willingness_to_pay=0.02,
    )

    assert config.satellites_total == 12000
    assert config.gdp_fraction_willingness_to_pay == 0.02


def test_data_loader():
    """Test DataLoader basic functionality."""
    loader = DataLoader()
    countries = loader.load_country_data()

    assert len(countries) > 0
    assert all(isinstance(country, CountryData) for country in countries)

    # Test US data specifically
    us_data = next((c for c in countries if c.country_code == "US"), None)
    assert us_data is not None
    assert us_data.country_name == "United States"


def test_import_all_modules():
    """Test that all main modules can be imported."""
    from starlink_tam import (  # noqa: F401
        CountryData,
        DataLoader,
        MarketSegment,
        ModelConfig,
        MonteCarloRunner,
        StarlinkTAMEngine,
        TAMResults,
    )

    # If we get here without errors, imports are working
    assert True


if __name__ == "__main__":
    pytest.main([__file__])
