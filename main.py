import typer
from src.kml_operations import generate_kmz_from_csv
from src.config import OUTPUT_FOLDER

app = typer.Typer(help="KMZ Generator CLI: Convert CSV data into KMZ files.")

@app.command()
def generate(
    csv_file: str = typer.Option(..., help="Path to the input CSV file."),
    output_folder: str = typer.Option(OUTPUT_FOLDER, help="Output folder for KMZ files.")
):
    """
    Generate KMZ file(s) from the given CSV file.
    """
    typer.echo(f"Processing file: {csv_file}")
    typer.echo(f"Output will be saved in: {output_folder}")
    
    try:
        output_file = generate_kmz_from_csv(csv_file, output_folder)
        typer.secho(f"KMZ file generated successfully: {output_file}", fg=typer.colors.GREEN)
    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED)

if __name__ == "__main__":
    app()
