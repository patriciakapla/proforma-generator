import typer
from typing import Annotated
from rich import print
import json_handling
import template_generator as generator
import pricing
import utils

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
):

    data = json_handling.load_data(file_path)
    milestone_list = utils.get_milestones(data)
    print(utils.get_milestones(data))
    print()
    utils.print_milestones(data, milestone_list)


@app.command("gen")
def generate_proforma(
    file_path: Annotated[
        str,
        typer.Argument(
            help="Path to the contract file to process for billing",
        ),
    ],
    milestone_to_bill: Annotated[
        int,
        typer.Argument(
            help="Selects milestone to be billed",
        ),
    ],
):
    """
    Generates proforma from data in given json.
    Arguments:
    - file_path: required argument - path to json file with contract data
    - milestone_to_bill: optional argument - displays payment schedule milestones.
    """
    data = json_handling.load_data(file_path)
    print(f"Selected contract: [yellow]{data["contractTitle"]}[/yellow]")
    pricing.calculate_milestone_amount(data)
    generator.generate_pdf(data, milestone_to_bill)


if __name__ == "__main__":
    app()
