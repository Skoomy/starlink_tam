#!/usr/bin/env python3
"""Demo script to test the Starlink TAM analysis platform."""

import sys
from pathlib import Path

from starlink_tam import (
    DataLoader,
    StarlinkTAMEngine,
    create_dashboard,
    load_config,
    setup_logging,
)

# Add the package to path


sys.path.insert(0, str(Path(__file__).parent))


def main():
    """Run a basic demo of the TAM analysis platform."""

    # Set up logging
    setup_logging(level="INFO")

    print("🚀 Starlink TAM Analysis Platform Demo")
    print("=" * 50)

    try:
        # Load configuration
        print("📊 Loading configuration...")
        config = load_config("config/default.yaml")

        # Load country data
        print("🌍 Loading country data...")
        data_loader = DataLoader()
        country_data = data_loader.load_country_data()
        print(f"   Loaded {len(country_data)} countries")

        # Run TAM analysis
        print("🔍 Running TAM analysis...")
        engine = StarlinkTAMEngine(config, country_data)
        results = engine.run_comprehensive_analysis()

        # Display key results
        print("\\n📈 KEY RESULTS:")
        print(f"   Global TAM: ${results.global_tam_usd:,.0f}")
        print(f"   Global SAM: ${results.global_sam_usd:,.0f}")
        print(f"   Global SOM: ${results.global_som_usd:,.0f}")
        print(f"   Satellites Required: {results.satellite_constellation_size:,}")
        print(f"   Total CAPEX: ${results.required_capex_usd:,.0f}")

        # Show top markets
        print("\\nTOP 5 MARKETS:")
        top_markets = results.get_top_markets(5)
        for i, (country, tam_value) in enumerate(top_markets, 1):
            print(f"   {i}. {country}: ${tam_value:,.0f}")

        # Show segment breakdown
        print("\\n📊 SEGMENT BREAKDOWN:")
        segment_breakdown = results.get_segment_breakdown()
        for segment, percentage in sorted(
            segment_breakdown.items(), key=lambda x: x[1], reverse=True
        ):
            print(f"   {segment.replace('_', ' ').title()}: {percentage:.1f}%")

        # Create visualizations
        print("\\n📊 Creating dashboard...")
        dashboard_files = create_dashboard(results, output_dir="output/demo")
        print(f"   Dashboard saved to: {dashboard_files}")

        print("\\n✅ Demo completed successfully!")
        print("   Check the 'output/demo' directory for visualizations")

    except Exception as e:
        print(f"\\n❌ Demo failed: {e}")
        import traceback

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
