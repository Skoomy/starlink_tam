"""Data loading and validation utilities with sample data."""

from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import List, Optional

import pandas as pd
from pydantic import ValidationError

from ..models.country import CountryData
from .logger import get_logger

logger = get_logger(__name__)


class DataLoader:
    """Professional data loader with validation and caching."""

    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = Path(data_dir) if data_dir else Path("data")
        self._cache: dict = {}

    def load_country_data(self, file_path: Optional[str] = None) -> List[CountryData]:
        """Load and validate country data."""

        if file_path and Path(file_path).exists():
            return self._load_from_file(file_path)
        else:
            logger.warning("No country data file found, using sample data")
            return self._get_sample_country_data()

    def _load_from_file(self, file_path: str) -> List[CountryData]:
        """Load country data from CSV/Excel file."""
        try:
            if file_path.endswith(".csv"):
                df = pd.read_csv(file_path)
            elif file_path.endswith((".xlsx", ".xls")):
                df = pd.read_excel(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_path}")

            country_data = []
            for _, row in df.iterrows():
                try:
                    country = CountryData(**row.to_dict())
                    country_data.append(country)
                except ValidationError as e:
                    logger.warning(f"Skipping invalid country data: {e}")
                    continue

            logger.info(f"Loaded {len(country_data)} countries from {file_path}")
            return country_data

        except Exception as e:
            logger.error(f"Failed to load country data from {file_path}: {e}")
            raise

    def _get_sample_country_data(self) -> List[CountryData]:
        """Generate sample country data for demonstration."""

        # Sample data representing major markets
        sample_countries = [
            {
                "country_code": "US",
                "country_name": "United States",
                "region": "North America",
                "income_group": "High income",
                "land_area_km2": 9_833_517,
                "land_area_pct": 0.066,  # ~6.6% of global land
                "population_total": 331_900_000,
                "population_rural": 57_230_000,
                "population_urban": 274_670_000,
                "population_density_per_km2": 33.7,
                "gdp_total_usd": Decimal("21_430_000_000_000"),  # $21.43T
                "gdp_per_capita_usd": Decimal("64_530"),
                "gdp_per_capita_monthly": Decimal("5_377"),
                "internet_penetration_pct": 0.87,
                "mobile_penetration_pct": 1.27,
                "fixed_broadband_penetration_pct": 0.36,
                "avg_broadband_speed_mbps": 42.8,
                "ease_of_doing_business_rank": 6,
                "regulatory_quality_score": 1.21,
                "data_vintage": datetime(2023, 1, 1),
                "data_source": "World Bank, ITU, Speedtest",
            },
            {
                "country_code": "CN",
                "country_name": "China",
                "region": "East Asia & Pacific",
                "income_group": "Upper middle income",
                "land_area_km2": 9_596_960,
                "land_area_pct": 0.064,
                "population_total": 1_439_320_000,
                "population_rural": 564_110_000,
                "population_urban": 875_210_000,
                "population_density_per_km2": 150.0,
                "gdp_total_usd": Decimal("14_723_000_000_000"),  # $14.72T
                "gdp_per_capita_usd": Decimal("10_240"),
                "gdp_per_capita_monthly": Decimal("853"),
                "internet_penetration_pct": 0.73,
                "mobile_penetration_pct": 1.25,
                "fixed_broadband_penetration_pct": 0.24,
                "avg_broadband_speed_mbps": 22.1,
                "ease_of_doing_business_rank": 31,
                "regulatory_quality_score": -0.42,
                "data_vintage": datetime(2023, 1, 1),
                "data_source": "World Bank, ITU, Speedtest",
            },
            {
                "country_code": "IN",
                "country_name": "India",
                "region": "South Asia",
                "income_group": "Lower middle income",
                "land_area_km2": 3_287_263,
                "land_area_pct": 0.022,
                "population_total": 1_380_000_000,
                "population_rural": 896_000_000,
                "population_urban": 484_000_000,
                "population_density_per_km2": 420.0,
                "gdp_total_usd": Decimal("2_875_000_000_000"),  # $2.87T
                "gdp_per_capita_usd": Decimal("2_083"),
                "gdp_per_capita_monthly": Decimal("174"),
                "internet_penetration_pct": 0.45,
                "mobile_penetration_pct": 0.85,
                "fixed_broadband_penetration_pct": 0.015,
                "avg_broadband_speed_mbps": 13.8,
                "ease_of_doing_business_rank": 63,
                "regulatory_quality_score": -0.21,
                "data_vintage": datetime(2023, 1, 1),
                "data_source": "World Bank, ITU, Speedtest",
            },
            {
                "country_code": "BR",
                "country_name": "Brazil",
                "region": "Latin America & Caribbean",
                "income_group": "Upper middle income",
                "land_area_km2": 8_514_877,
                "land_area_pct": 0.057,
                "population_total": 212_600_000,
                "population_rural": 25_000_000,
                "population_urban": 187_600_000,
                "population_density_per_km2": 25.0,
                "gdp_total_usd": Decimal("1_609_000_000_000"),  # $1.61T
                "gdp_per_capita_usd": Decimal("7_570"),
                "gdp_per_capita_monthly": Decimal("631"),
                "internet_penetration_pct": 0.71,
                "mobile_penetration_pct": 1.17,
                "fixed_broadband_penetration_pct": 0.16,
                "avg_broadband_speed_mbps": 26.2,
                "ease_of_doing_business_rank": 124,
                "regulatory_quality_score": -0.08,
                "data_vintage": datetime(2023, 1, 1),
                "data_source": "World Bank, ITU, Speedtest",
            },
            {
                "country_code": "RU",
                "country_name": "Russian Federation",
                "region": "Europe & Central Asia",
                "income_group": "Upper middle income",
                "land_area_km2": 17_098_242,
                "land_area_pct": 0.115,  # Largest country by land area
                "population_total": 145_940_000,
                "population_rural": 37_000_000,
                "population_urban": 108_940_000,
                "population_density_per_km2": 8.5,
                "gdp_total_usd": Decimal("1_483_000_000_000"),  # $1.48T
                "gdp_per_capita_usd": Decimal("10_160"),
                "gdp_per_capita_monthly": Decimal("847"),
                "internet_penetration_pct": 0.85,
                "mobile_penetration_pct": 1.61,
                "fixed_broadband_penetration_pct": 0.22,
                "avg_broadband_speed_mbps": 32.4,
                "ease_of_doing_business_rank": 28,
                "regulatory_quality_score": -0.71,
                "data_vintage": datetime(2023, 1, 1),
                "data_source": "World Bank, ITU, Speedtest",
            },
            {
                "country_code": "AU",
                "country_name": "Australia",
                "region": "East Asia & Pacific",
                "income_group": "High income",
                "land_area_km2": 7_692_024,
                "land_area_pct": 0.052,
                "population_total": 25_500_000,
                "population_rural": 2_800_000,
                "population_urban": 22_700_000,
                "population_density_per_km2": 3.3,
                "gdp_total_usd": Decimal("1_392_000_000_000"),  # $1.39T
                "gdp_per_capita_usd": Decimal("54_600"),
                "gdp_per_capita_monthly": Decimal("4_550"),
                "internet_penetration_pct": 0.88,
                "mobile_penetration_pct": 1.08,
                "fixed_broadband_penetration_pct": 0.35,
                "avg_broadband_speed_mbps": 34.6,
                "ease_of_doing_business_rank": 14,
                "regulatory_quality_score": 1.62,
                "data_vintage": datetime(2023, 1, 1),
                "data_source": "World Bank, ITU, Speedtest",
            },
            {
                "country_code": "CA",
                "country_name": "Canada",
                "region": "North America",
                "income_group": "High income",
                "land_area_km2": 9_984_670,
                "land_area_pct": 0.067,
                "population_total": 38_000_000,
                "population_rural": 6_270_000,
                "population_urban": 31_730_000,
                "population_density_per_km2": 3.8,
                "gdp_total_usd": Decimal("1_736_000_000_000"),  # $1.74T
                "gdp_per_capita_usd": Decimal("45_680"),
                "gdp_per_capita_monthly": Decimal("3_807"),
                "internet_penetration_pct": 0.91,
                "mobile_penetration_pct": 0.84,
                "fixed_broadband_penetration_pct": 0.41,
                "avg_broadband_speed_mbps": 52.6,
                "ease_of_doing_business_rank": 23,
                "regulatory_quality_score": 1.59,
                "data_vintage": datetime(2023, 1, 1),
                "data_source": "World Bank, ITU, Speedtest",
            },
        ]

        country_data = []
        for country_dict in sample_countries:
            try:
                country = CountryData(**country_dict)
                country_data.append(country)
            except ValidationError as e:
                logger.error(f"Invalid sample country data: {e}")
                continue

        logger.info(f"Generated {len(country_data)} sample countries")
        return country_data


class DataValidator:
    """Validate and clean country data."""

    def validate_country_data(self, data: List[CountryData]) -> List[CountryData]:
        """Validate and clean country data."""
        valid_data = []

        for country in data:
            if self._is_valid_country(country):
                valid_data.append(country)
            else:
                logger.warning(f"Excluding invalid country: {country.country_code}")

        logger.info(f"Validated {len(valid_data)} out of {len(data)} countries")
        return valid_data

    def _is_valid_country(self, country: CountryData) -> bool:
        """Check if country data meets minimum quality requirements."""

        # Basic validation rules
        if country.population_total <= 0:
            return False

        if country.gdp_per_capita_usd <= 0:
            return False

        if country.land_area_km2 <= 0:
            return False

        if not (0 <= country.internet_penetration_pct <= 1):
            return False

        return True
