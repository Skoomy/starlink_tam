# 🚀 Starlink TAM Analysis Platform v2.0

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A  valuation platform for analyzing Starlink's Total Addressable Market (TAM) with comprehensive risk modeling, Monte Carlo simulation.

## Overview

This platform provides sophisticated market sizing and valuation analysis for Starlink's satellite internet opportunity, combining:

- **Supply-side modeling**: Satellite capacity and bandwidth allocation
- **Demand-side analysis**: Customer willingness to pay and market penetration
- **Risk assessment**: Regulatory, competitive, and technological risk factors
- **Monte Carlo simulation**: Uncertainty quantification and scenario analysis

## 🏗️ Architecture

### Core Components

1. **TAM Engine** (`StarlinkTAMEngine`): Advanced market sizing with multi-segment analysis
2. **Monte Carlo Runner**: Risk simulation with parallel processing
3. **Data Models**: Pydantic-based validation and type safety
4. **Visualization**: Interactive Plotly dashboards
5. **CLI Interface**: Rich terminal interface with progress tracking

### Key Features

- 📊 **Comprehensive Market Analysis**: TAM/SAM/SOM calculations with segment breakdown
- 🌍 **Country-level Modeling**: Economic, geographic, and regulatory factors
- 🎲 **Monte Carlo Simulation**: 10,000+ simulations with correlation modeling
- 📈 **Risk Analytics**: VaR, Expected Shortfall, sensitivity analysis
- 🔍 **Scenario Planning**: Best/worst/base case projections
- 📋 **Professional Reporting**: Executive-ready outputs and visualizations

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/team-artometrix/starlink-tam
cd starlink-tam

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Basic Usage

```python
from starlink_tam import StarlinkTAMEngine, DataLoader, load_config

# Load configuration and data
config = load_config("config/default.yaml")
data_loader = DataLoader()
country_data = data_loader.load_country_data()

# Run TAM analysis
engine = StarlinkTAMEngine(config, country_data)
results = engine.run_comprehensive_analysis()

print(f"Global TAM: ${results.global_tam_usd:,.0f}")
print(f"Top Markets: {results.get_top_markets(5)}")
```

### CLI Usage

```bash
# Basic TAM analysis
starlink-tam analyze --output results.json

# Monte Carlo simulation
starlink-tam monte-carlo --simulations 10000 --parallel

# Top markets analysis
starlink-tam top-markets --metric tam --top-n 10

# Help
starlink-tam --help
```

### Demo Script

```bash
# Run the demo
python demo.py
```

## 📊 Model Framework

### Supply-Side Inputs
- **Constellation Size**: 12,000 - 42,000 satellites
- **Bandwidth per Satellite**: 17 Mbps (configurable)
- **Oversubscription Ratio**: Network efficiency factor
- **Geographic Allocation**: Land area and economic weighting

### Demand-Side Inputs
- **Price Sensitivity**: GDP-based willingness to pay (~2% monthly income)
- **Market Penetration**: Rural vs urban adoption rates
- **Competitive Dynamics**: Existing infrastructure quality
- **Regulatory Environment**: Country-specific risk factors

### Market Segmentation
- **Residential Rural**: Primary target market
- **Residential Urban**: Secondary market
- **Enterprise SMB/Large**: High-value segments
- **Mobility**: Maritime, aviation, automotive
- **Government/Emergency**: Specialized applications

## 🔬 Advanced Analytics

### Risk Modeling
- **Regulatory Risk**: Scoring based on governance indicators
- **Market Risk**: Competitive intensity and substitution
- **Technology Risk**: Deployment and performance challenges
- **Economic Risk**: GDP correlation and affordability

### Monte Carlo Features
- **Parameter Distributions**: Normal, lognormal, uniform, beta, gamma
- **Correlation Modeling**: Cholesky decomposition for parameter relationships
- **Parallel Processing**: Multi-core simulation execution
- **Statistical Analysis**: Full distribution characterization

### Valuation Metrics
- **DCF Analysis**: Free cash flow projections and terminal value
- **Multiple-based Valuation**: EV/Revenue, EV/EBITDA comparisons
- **Risk-adjusted Returns**: Sharpe ratios and risk premiums
- **Sensitivity Analysis**: Tornado charts and scenario planning

## 📈 Sample Results

Based on base case assumptions:

```
🚀 STARLINK TAM ANALYSIS RESULTS
================================

Global Market Size:
• Total Addressable Market: $89.2B
• Serviceable Addressable Market: $45.6B
• Serviceable Obtainable Market: $23.1B

Top 5 Markets:
1. United States: $8.9B
2. China: $6.7B
3. Russia: $4.2B
4. Brazil: $3.1B
5. India: $2.8B

Infrastructure Requirements:
• Satellites: 12,000
• Global Bandwidth: 204 Gbps
• Required CAPEX: $6.0B

Risk Factors:
• Regulatory approval probability: 75%
• Competitive response impact: Medium
• Technology deployment risk: Low-Medium
```

## 🛠️ Configuration

### Model Parameters (`config/default.yaml`)

```yaml
satellites_total: 12000
bandwidth_per_satellite_mbps: 17
oversubscription_ratio: 20
minimum_bandwidth_per_user_mbps: 20
gdp_fraction_willingness_to_pay: 0.02
```

### Distribution Parameters (`config/distribution.yaml`)

```yaml
satellites_total:
  distribution: uniform
  min: 8000
  max: 42000

bandwidth_per_satellite_mbps:
  distribution: normal
  mean: 17
  std: 3

gdp_fraction_willingness_to_pay:
  distribution: beta
  alpha: 2
  beta: 10
  scale: 0.05
```

## 📊 Visualizations

The platform generates interactive dashboards including:

1. **TAM Overview Dashboard**: Global metrics and top markets
2. **Country Analysis**: Market size vs risk by geography
3. **Segment Breakdown**: Revenue allocation across customer types
4. **Monte Carlo Results**: Distribution analysis and sensitivity
5. **Risk Assessment**: Tornado charts and scenario comparisons

## 🧪 Testing

```bash
# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=starlink_tam --cov-report=html

# Run specific test category
pytest tests/test_models.py -k "test_country_data"
```

## 📚 Documentation

### Key Classes

- `StarlinkTAMEngine`: Main analysis engine
- `MonteCarloRunner`: Simulation framework
- `CountryData`: Economic and demographic data model
- `TAMResults`: Comprehensive results container
- `TAMVisualizer`: Chart and dashboard generator

### Model Validation

All data models use Pydantic for:
- Type validation and conversion
- Range checking and constraints
- Automatic documentation generation
- JSON serialization/deserialization

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt[dev]

# Install pre-commit hooks
pre-commit install

# Run code formatting
black starlink_tam/
isort starlink_tam/

# Run linting
flake8 starlink_tam/
mypy starlink_tam/
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by ARK Invest's Starlink analysis methodology
- Economic data sourced from World Bank, ITU, and Speedtest
- Built with modern Python data science stack

## Contact

**Team Artometrix**
- Email: contact@artometrix.com
- Website: [artometrix.com](https://artometrix.com)

---
