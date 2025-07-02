"""CLI interface for Starlink TAM analysis with rich output."""

import sys
from pathlib import Path

import click
import yaml
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from .model.default_model import StarlinkTAMEngine
from .model.monte_carlo import MonteCarloRunner
from .models.simulation import DistributionParams, MonteCarloConfig
from .utils.config import load_config
from .utils.data import DataLoader
from .utils.logger import get_logger, setup_logging

console = Console()
logger = get_logger(__name__)


@click.group()
@click.option("--log-level", default="INFO", help="Logging level")
@click.option("--log-file", type=click.Path(), help="Log file path")
@click.option("--config", type=click.Path(exists=True), help="Configuration file")
@click.pass_context
def cli(ctx, log_level, log_file, config):
    """Starlink Total Addressable Market (TAM) Analysis Platform.

    A hedge fund quality valuation platform for analyzing Starlink's market opportunity.
    """
    ctx.ensure_object(dict)

    # Set up logging
    setup_logging(
        level=log_level, log_file=Path(log_file) if log_file else None, json_logs=False
    )

    # Load configuration
    config_path = config or "config/default.yaml"
    ctx.obj["config"] = load_config(config_path)

    console.print(
        Panel.fit(
            "[bold blue]Starlink TAM Analysis Platform[/bold blue]\n"
            "[dim]Market sizing and valuation analysis[/dim]",
            border_style="blue",
        )
    )


@cli.command()
@click.option("--output", "-o", type=click.Path(), help="Output file for results")
@click.option(
    "--format",
    default="json",
    type=click.Choice(["json", "yaml", "csv"]),
    help="Output format",
)
@click.option("--countries", help="Comma-separated list of country codes to analyze")
@click.pass_context
def analyze(ctx, output, format, countries):
    """Run comprehensive TAM analysis."""

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        # Load data
        progress.add_task("Loading country data...", total=None)
        data_loader = DataLoader()
        country_data = data_loader.load_country_data()

        if countries:
            country_codes = [c.strip().upper() for c in countries.split(",")]
            country_data = [c for c in country_data if c.country_code in country_codes]
            console.print(
                f"[yellow]Filtering to {len(country_data)} countries: {country_codes}[/yellow]"
            )

        # Run analysis
        progress.add_task("Running TAM analysis...", total=None)
        engine = StarlinkTAMEngine(ctx.obj["config"], country_data)
        results = engine.run_comprehensive_analysis()

        # Display results
        _display_results(results)

        # Save results if requested
        if output:
            progress.add_task(f"Saving results to {output}...", total=None)
            _save_results(results, output, format)
            console.print(f"[green]Results saved to {output}[/green]")


@cli.command()
@click.option(
    "--simulations", "-n", default=1000, help="Number of Monte Carlo simulations"
)
@click.option(
    "--config", type=click.Path(exists=True), help="Monte Carlo configuration file"
)
@click.option("--output", "-o", type=click.Path(), help="Output file for results")
@click.option(
    "--parallel/--sequential", default=True, help="Run simulations in parallel"
)
@click.option("--workers", type=int, help="Number of parallel workers")
@click.pass_context
def monte_carlo(ctx, simulations, config, output, parallel, workers):
    """Run Monte Carlo simulation for uncertainty analysis."""

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        # Load Monte Carlo configuration
        mc_config_path = config or "config/distribution.yaml"
        progress.add_task("Loading simulation configuration...", total=None)

        with open(mc_config_path, "r") as f:
            dist_config = yaml.safe_load(f)

        # Convert to proper format
        parameter_distributions = {}
        for param, dist_def in dist_config.items():
            parameter_distributions[param] = DistributionParams(**dist_def)

        mc_config = MonteCarloConfig(
            n_simulations=simulations,
            parameter_distributions=parameter_distributions,
            random_seed=42,  # For reproducibility
        )

        # Load country data
        progress.add_task("Loading country data...", total=None)
        data_loader = DataLoader()
        country_data = data_loader.load_country_data()

        # Run simulation
        progress.add_task(
            f"Running {simulations} Monte Carlo simulations...", total=None
        )
        runner = MonteCarloRunner(country_data, mc_config, ctx.obj["config"])

        if parallel:
            sim_results = runner.run_parallel(max_workers=workers)
        else:
            sim_results = runner.run_sequential()

        # Display results
        _display_simulation_results(sim_results)

        # Save results if requested
        if output:
            progress.add_task(f"Saving results to {output}...", total=None)
            runner.export_results(output)
            console.print(f"[green]Simulation results saved to {output}[/green]")


@cli.command()
@click.option(
    "--metric",
    default="tam",
    type=click.Choice(["tam", "sam", "som"]),
    help="Metric to analyze",
)
@click.option("--top-n", default=10, help="Number of top countries to show")
@click.pass_context
def top_markets(ctx, metric, top_n):
    """Analyze top markets by TAM/SAM/SOM."""

    # Load data and run quick analysis
    data_loader = DataLoader()
    country_data = data_loader.load_country_data()

    engine = StarlinkTAMEngine(ctx.obj["config"], country_data)
    results = engine.run_comprehensive_analysis()

    # Get top markets
    metric_map = {
        "tam": "total_addressable_market_usd",
        "sam": "serviceable_addressable_market_usd",
        "som": "serviceable_obtainable_market_usd",
    }

    metric_attr = metric_map[metric]
    top_markets = sorted(
        [
            (code, getattr(analysis, metric_attr))
            for code, analysis in results.country_analyses.items()
        ],
        key=lambda x: x[1],
        reverse=True,
    )[:top_n]

    # Display table
    table = Table(title=f"Top {top_n} Markets by {metric.upper()}")
    table.add_column("Rank", style="cyan", no_wrap=True)
    table.add_column("Country", style="magenta")
    table.add_column(f"{metric.upper()} (USD)", style="green", justify="right")
    table.add_column("% of Total", style="yellow", justify="right")

    total_value = sum(x[1] for x in top_markets)

    for i, (country_code, value) in enumerate(top_markets, 1):
        percentage = (float(value) / float(total_value)) * 100 if total_value > 0 else 0
        table.add_row(str(i), country_code, f"${value:,.0f}", f"{percentage:.1f}%")

    console.print(table)


def _display_results(results):
    """Display TAM analysis results in a rich format."""

    # Summary panel
    summary_text = f"""
[bold]Global Market Size[/bold]
• Total Addressable Market: [green]${results.global_tam_usd:,.0f}[/green]
• Serviceable Addressable Market: [blue]${results.global_sam_usd:,.0f}[/blue]
• Serviceable Obtainable Market: [yellow]${results.global_som_usd:,.0f}[/yellow]

[bold]Infrastructure Requirements[/bold]
• Satellites: [cyan]{results.satellite_constellation_size:,}[/cyan]
• Global Bandwidth: [cyan]{results.global_bandwidth_capacity_gbps:,.1f} Gbps[/cyan]
• Required CAPEX: [red]${results.required_capex_usd:,.0f}[/red]

[bold]Confidence Level[/bold]: [green]{results.confidence_level:.0%}[/green]
    """

    console.print(
        Panel(summary_text, title="TAM Analysis Summary", border_style="green")
    )

    # Top markets table
    top_markets = results.get_top_markets(5)

    table = Table(title="Top 5 Markets")
    table.add_column("Country", style="cyan")
    table.add_column("TAM (USD)", style="green", justify="right")
    table.add_column("% of Global", style="yellow", justify="right")

    for country_code, tam_value in top_markets:
        percentage = (float(tam_value) / float(results.global_tam_usd)) * 100
        table.add_row(country_code, f"${tam_value:,.0f}", f"{percentage:.1f}%")

    console.print(table)

    # Segment breakdown
    segment_breakdown = results.get_segment_breakdown()
    if segment_breakdown:
        table = Table(title="Market Segment Breakdown")
        table.add_column("Segment", style="magenta")
        table.add_column("% of SOM", style="green", justify="right")

        for segment, percentage in sorted(
            segment_breakdown.items(), key=lambda x: x[1], reverse=True
        ):
            table.add_row(segment.replace("_", " ").title(), f"{percentage:.1f}%")

        console.print(table)


def _display_simulation_results(sim_results):
    """Display Monte Carlo simulation results."""

    tam_stats = sim_results.global_tam_statistics

    # Summary statistics
    summary_text = f"""
[bold]Monte Carlo Simulation Results[/bold]
• Simulations Completed: [cyan]{sim_results.n_simulations_completed:,}[/cyan]
• Execution Time: [cyan]{sim_results.execution_time_seconds:.1f}s[/cyan]

[bold]Global TAM Statistics (USD)[/bold]
• Mean: [green]${tam_stats.get('mean', 0):,.0f}[/green]
• Median: [blue]${tam_stats.get('median', 0):,.0f}[/blue]
• Std Dev: [yellow]${tam_stats.get('std', 0):,.0f}[/yellow]
• 95% CI: [red]${tam_stats.get('p5', 0):,.0f} - ${tam_stats.get('p95', 0):,.0f}[/red]

[bold]Risk Metrics[/bold]
• Probability of Loss: [red]{sim_results.probability_of_loss:.1%}[/red]
• VaR (95%): [red]${sim_results.value_at_risk.get('VaR_95', 0):,.0f}[/red]
    """

    console.print(Panel(summary_text, title="Simulation Summary", border_style="blue"))

    # Sensitivity analysis
    if sim_results.tornado_chart_data:
        table = Table(title="Parameter Sensitivity (Top 5)")
        table.add_column("Parameter", style="cyan")
        table.add_column("Impact Score", style="green", justify="right")

        for item in sim_results.tornado_chart_data[:5]:
            table.add_row(
                item["variable"].replace("_", " ").title(), f"{item['impact']:.3f}"
            )

        console.print(table)


def _save_results(results, output_path, format):
    """Save results to file in specified format."""
    import json
    from decimal import Decimal

    # Convert Decimal to float for JSON serialization
    def decimal_converter(obj):
        if isinstance(obj, Decimal):
            return float(obj)
        raise TypeError(
            "Object of type '%s' is not JSON serializable" % type(obj).__name__
        )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if format == "json":
        with open(output_path, "w") as f:
            json.dump(results.dict(), f, indent=2, default=decimal_converter)
    elif format == "yaml":
        import yaml

        with open(output_path, "w") as f:
            yaml.dump(results.dict(), f, default_flow_style=False)
    elif format == "csv":
        # Convert to DataFrame for CSV export
        import pandas as pd

        # Create summary data
        summary_data = {
            "metric": ["Global TAM", "Global SAM", "Global SOM", "Required CAPEX"],
            "value_usd": [
                float(results.global_tam_usd),
                float(results.global_sam_usd),
                float(results.global_som_usd),
                float(results.required_capex_usd),
            ],
        }

        df = pd.DataFrame(summary_data)
        df.to_csv(output_path, index=False)


def main():
    """Main entry point for CLI."""
    try:
        cli()
    except KeyboardInterrupt:
        console.print("\n[red]Analysis interrupted by user[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        logger.error("CLI execution failed", error=str(e), exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
