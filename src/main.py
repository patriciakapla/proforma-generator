import typer
from typing import Annotated
import json_handling
import template_generator as generator
from pathlib import Path
from rich import print
from utils import validate_milestone

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
    contract.print_contract()
    contract.print_milestones()


@app.command("gen")
def generate_proforma(
    file_path: Annotated[
        str,
        typer.Argument(
            help="Path to the contract file to process for billing",
        ),
    ],
    milestone: Annotated[
        int,
        typer.Argument(
            help="Selects milestone to be billed",
        ),
    ],
) -> None:
    # TODO: Apply logics to accept more than one milestone argument
    """
    Generates proforma from data in given json.
    Arguments:
    - file_path: required argument - path to json file with contract data
    - milestone_to_bill: required argument - displays payment schedule milestones.
    """
    milestone_index = milestone - 1
    fp = Path(file_path)
    contract = json_handling.load_data(fp)
    validate_milestone(milestone_index, contract)
    json_handling.update_json(fp, contract)
    contract.print_contract(milestone_index)
    generator.generate_pdf(contract, milestone_index)


if __name__ == "__main__":
    app()
