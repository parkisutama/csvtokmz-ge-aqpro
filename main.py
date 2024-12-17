import typer
from src.kml_operations import generate_kmz_from_csv
from src.config import OUTPUT_FOLDER
from src.data_processing import bulk_gps_extraction

app = typer.Typer(help="KMZ Generator CLI: Convert CSV data into KMZ files.")


@app.command()
def greet(
    name: str = typer.Option(..., help="Tell me your Name, so I can Call You!."),
):
    """
    Send a greeting message to You
    """
    typer.echo(f"Halo, {name}!")


@app.command()
def generate(
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
    except FileNotFoundError:
        typer.secho("Error: The specified CSV file was not found.", fg=typer.colors.RED)
    except Exception as e:
        typer.secho(f"An unexpected error occurred: {e}", fg=typer.colors.RED)


@app.command()
def bulk_gps_extract_images(
    folder: str = typer.Option(..., help="Path to the folder containing the images."),
    output_folder: str = typer.Option(..., help="Path to the output folder."),
    excel_name: str = typer.Option("...", help="Name of the output Excel file."),
):
    """
    Bulk extract GPS data from the images in the given folder.
    """
    typer.echo(f"Processing folder: {folder}")
    typer.echo(f"Output will be saved in: {output_folder}")
    typer.echo(f"Excel file name: {excel_name}")

    try:
        bulk_gps_extraction(folder, output_folder, excel_name)
        typer.secho(
            f"GPS Data Extracted Successfully: ({output_folder}{excel_name})",
            fg=typer.colors.GREEN,
        )
    except FileNotFoundError:
        typer.secho("Error: The specified CSV file was not found.", fg=typer.colors.RED)
    except Exception as e:
        typer.secho(f"An unexpected error occurred: {e}", fg=typer.colors.RED)


if __name__ == "__main__":
    app()
