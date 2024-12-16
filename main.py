import typer
from src.kml_operations import generate_kmz_from_csv
from src.config import OUTPUT_FOLDER

app = typer.Typer(help="KMZ Generator CLI: Convert CSV data into KMZ files.")


@app.command()
def generate(
    generate: str = typer.Argument(help="Generate KMZ from CSV"),
    csv_file: str = typer.Option(..., help="Path to the input CSV file."),
):
    """
    Generate KMZ file(s) from the given CSV file.
    """
    typer.echo(f"Processing file: {csv_file}")
    typer.echo(f"Output will be saved in: {OUTPUT_FOLDER}")

    try:
        output_file = generate_kmz_from_csv(csv_file, OUTPUT_FOLDER)
        typer.secho(
            f"KMZ file generated successfully: {output_file}", fg=typer.colors.GREEN
        )
    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED)


if __name__ == "__main__":
    app()
