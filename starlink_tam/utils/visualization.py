"""Visualization utilities for TAM analysis results."""

from pathlib import Path
from typing import List, Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from ..models.market import TAMResults
from ..models.simulation import SimulationResults
from .logger import get_logger

logger = get_logger(__name__)


class TAMVisualizer:
    """Professional visualization for TAM analysis results."""

    def __init__(self, theme: str = "plotly_white"):
        self.theme = theme
        self.color_palette = px.colors.qualitative.Set1

    def create_tam_overview_dashboard(self, results: TAMResults) -> go.Figure:
        """Create comprehensive TAM overview dashboard."""

        # Create subplots
        fig = make_subplots(
            rows=2,
            cols=2,
            subplot_titles=(
                "Global Market Size",
                "Top 10 Markets by TAM",
                "Market Segment Breakdown",
                "Risk Factors",
            ),
            specs=[
                [{"type": "bar"}, {"type": "bar"}],
                [{"type": "pie"}, {"type": "scatter"}],
            ],
        )

        # Global market size
        global_metrics = ["TAM", "SAM", "SOM"]
        global_values = [
            float(results.global_tam_usd),
            float(results.global_sam_usd),
            float(results.global_som_usd),
        ]

        fig.add_trace(
            go.Bar(
                x=global_metrics,
                y=global_values,
                marker_color=self.color_palette[:3],
                name="Global Market",
            ),
            row=1,
            col=1,
        )

        # Top markets
        top_markets = results.get_top_markets(10)
        countries = [market[0] for market in top_markets]
        tam_values = [float(market[1]) for market in top_markets]

        fig.add_trace(
            go.Bar(
                x=countries,
                y=tam_values,
                marker_color=self.color_palette[3],
                name="Country TAM",
            ),
            row=1,
            col=2,
        )

        # Segment breakdown
        segment_breakdown = results.get_segment_breakdown()
        if segment_breakdown:
            fig.add_trace(
                go.Pie(
                    labels=list(segment_breakdown.keys()),
                    values=list(segment_breakdown.values()),
                    name="Segments",
                ),
                row=2,
                col=1,
            )

        # Risk factors (placeholder)
        risk_factors = list(results.sensitivity_factors.keys())
        risk_impacts = list(results.sensitivity_factors.values())

        fig.add_trace(
            go.Scatter(
                x=risk_factors,
                y=risk_impacts,
                mode="markers",
                marker=dict(size=10, color=self.color_palette[4]),
                name="Risk Impact",
            ),
            row=2,
            col=2,
        )

        # Update layout
        fig.update_layout(
            title="Starlink TAM Analysis Dashboard",
            template=self.theme,
            height=800,
            showlegend=False,
        )

        return fig

    def create_country_analysis_chart(
        self, results: TAMResults, top_n: int = 15
    ) -> go.Figure:
        """Create detailed country analysis chart."""

        # Get top countries data
        top_markets = results.get_top_markets(top_n)

        data = []
        for country_code, tam_value in top_markets:
            if country_code in results.country_analyses:
                analysis = results.country_analyses[country_code]
                data.append(
                    {
                        "country": country_code,
                        "tam": float(tam_value),
                        "sam": float(analysis.serviceable_addressable_market_usd),
                        "som": float(analysis.serviceable_obtainable_market_usd),
                        "growth_rate": analysis.market_growth_rate_annual,
                        "regulatory_risk": analysis.regulatory_risk_score,
                    }
                )

        df = pd.DataFrame(data)

        # Create figure with secondary y-axis
        fig = make_subplots(
            rows=1,
            cols=1,
            secondary_y=True,
            subplot_titles=("Market Size and Risk Analysis by Country",),
        )

        # Add market size bars
        fig.add_trace(
            go.Bar(
                x=df["country"],
                y=df["tam"],
                name="TAM",
                marker_color=self.color_palette[0],
                opacity=0.8,
            ),
            secondary_y=False,
        )

        fig.add_trace(
            go.Bar(
                x=df["country"],
                y=df["sam"],
                name="SAM",
                marker_color=self.color_palette[1],
                opacity=0.6,
            ),
            secondary_y=False,
        )

        fig.add_trace(
            go.Bar(
                x=df["country"],
                y=df["som"],
                name="SOM",
                marker_color=self.color_palette[2],
                opacity=0.4,
            ),
            secondary_y=False,
        )

        # Add risk line
        fig.add_trace(
            go.Scatter(
                x=df["country"],
                y=df["regulatory_risk"],
                mode="lines+markers",
                name="Regulatory Risk",
                line=dict(color="red", width=3),
                marker=dict(size=8),
            ),
            secondary_y=True,
        )

        # Update axes
        fig.update_xaxes(title_text="Country")
        fig.update_yaxes(title_text="Market Size (USD)", secondary_y=False)
        fig.update_yaxes(title_text="Risk Score (0-10)", secondary_y=True)

        fig.update_layout(
            title="Country-Level TAM Analysis",
            template=self.theme,
            height=600,
            barmode="group",
        )

        return fig

    def create_simulation_results_chart(
        self, sim_results: SimulationResults
    ) -> go.Figure:
        """Create Monte Carlo simulation results visualization."""

        # Create subplots
        fig = make_subplots(
            rows=2,
            cols=2,
            subplot_titles=(
                "TAM Distribution Histogram",
                "Sensitivity Analysis (Tornado Chart)",
                "Risk Metrics",
                "Scenario Comparison",
            ),
            specs=[
                [{"type": "histogram"}, {"type": "bar"}],
                [{"type": "bar"}, {"type": "bar"}],
            ],
        )

        # TAM distribution (would need raw data for proper histogram)
        tam_stats = sim_results.global_tam_statistics
        percentiles = [float(tam_stats.get(f"p{p}", 0)) for p in [5, 25, 50, 75, 95]]

        fig.add_trace(
            go.Bar(
                x=["P5", "P25", "P50", "P75", "P95"],
                y=percentiles,
                marker_color=self.color_palette[0],
                name="TAM Percentiles",
            ),
            row=1,
            col=1,
        )

        # Sensitivity analysis
        if sim_results.tornado_chart_data:
            tornado_data = sim_results.tornado_chart_data[:10]  # Top 10
            variables = [item["variable"] for item in tornado_data]
            impacts = [item["impact"] for item in tornado_data]

            fig.add_trace(
                go.Bar(
                    x=impacts,
                    y=variables,
                    orientation="h",
                    marker_color=self.color_palette[1],
                    name="Parameter Impact",
                ),
                row=1,
                col=2,
            )

        # Risk metrics
        risk_metrics = ["Probability of Loss", "VaR (95%)", "Expected Shortfall"]
        risk_values = [
            sim_results.probability_of_loss * 100,  # Convert to percentage
            float(sim_results.value_at_risk.get("VaR_95", 0)) / 1e9,  # Billions
            float(sim_results.expected_shortfall.get("ES_95", 0)) / 1e9,  # Billions
        ]

        fig.add_trace(
            go.Bar(
                x=risk_metrics,
                y=risk_values,
                marker_color=["red", "orange", "orange"],
                name="Risk Metrics",
            ),
            row=2,
            col=1,
        )

        # Scenario comparison
        scenarios = ["Worst Case", "Base Case", "Best Case"]
        scenario_values = [
            float(sim_results.worst_case_scenario.get("global_tam", 0)) / 1e9,
            float(sim_results.base_case_scenario.get("global_tam", 0)) / 1e9,
            float(sim_results.best_case_scenario.get("global_tam", 0)) / 1e9,
        ]

        fig.add_trace(
            go.Bar(
                x=scenarios,
                y=scenario_values,
                marker_color=["red", "blue", "green"],
                name="Scenarios",
            ),
            row=2,
            col=2,
        )

        fig.update_layout(
            title="Monte Carlo Simulation Results",
            template=self.theme,
            height=800,
            showlegend=False,
        )

        return fig

    def save_chart(self, fig: go.Figure, filename: str, format: str = "html") -> None:
        """Save chart to file."""
        output_path = Path(filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if format.lower() == "html":
            fig.write_html(str(output_path))
        elif format.lower() == "png":
            fig.write_image(str(output_path))
        elif format.lower() == "pdf":
            fig.write_image(str(output_path))
        else:
            raise ValueError(f"Unsupported format: {format}")

        logger.info(f"Chart saved to {output_path}")


def create_dashboard(
    tam_results: TAMResults,
    sim_results: Optional[SimulationResults] = None,
    output_dir: str = "output",
) -> List[str]:
    """Create comprehensive dashboard with all visualizations."""

    visualizer = TAMVisualizer()
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    saved_files = []

    # TAM overview dashboard
    tam_dashboard = visualizer.create_tam_overview_dashboard(tam_results)
    tam_file = output_path / "tam_overview.html"
    visualizer.save_chart(tam_dashboard, str(tam_file))
    saved_files.append(str(tam_file))

    # Country analysis
    country_chart = visualizer.create_country_analysis_chart(tam_results)
    country_file = output_path / "country_analysis.html"
    visualizer.save_chart(country_chart, str(country_file))
    saved_files.append(str(country_file))

    # Simulation results (if available)
    if sim_results:
        sim_chart = visualizer.create_simulation_results_chart(sim_results)
        sim_file = output_path / "simulation_results.html"
        visualizer.save_chart(sim_chart, str(sim_file))
        saved_files.append(str(sim_file))

    logger.info(f"Dashboard created with {len(saved_files)} charts in {output_dir}")
    return saved_files
