import typer
from typing import Annotated
import json_handling
import template_generator as generator
from pathlib import Path
from rich import print
from utils import validate_milestones
import data_dict

app = typer.Typer()


@app.callback()
def main():
    print("[purple]PROFORMA GENERATOR[/purple]")


@app.command("mile")
def display_milestones(
    file_path: Annotated[
        str,
        typer.Argument(
            help="Path to the contract file to process for billing",
        ),
    ],
) -> None:
    fp = Path(file_path)
    contract = json_handling.load_data(fp)
    contract.print_contract([])
    contract.print_milestones()


@app.command("gen")
def generate_proforma(
    file_path: Annotated[
        str,
        typer.Argument(
            help="Path to the contract file to process for billing",
        ),
    ],
    milestones: Annotated[
        list[int],
        typer.Argument(
            help="Selects milestones to be billed",
        ),
    ],
) -> None:
    """
    Generate a proforma invoice from contract data in a JSON file.
    Arguments:
    - file_path: Path to the JSON file containing contract data.
    - milestones: Milestones to include in the billing.
    """
    fp = Path(file_path)
    contract = json_handling.load_data(fp)
    validate_milestones(milestones, contract)
    calculated_payload = data_dict.generate_calculated_data(contract, milestones)
    normalized_payload = data_dict.normalize_data(calculated_payload)
    contract.print_contract(milestones)
    generator.generate_pdf(normalized_payload, milestones)


@app.command("update")
def update_contract(): ...


if __name__ == "__main__":
    app()
