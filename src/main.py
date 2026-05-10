import typer
from typing import Annotated
import json_handling
import template_generator as generator
from utils import validate_milestones, pretty_msg
import data_dict

app = typer.Typer()


@app.callback()
def main():
    pretty_msg("PROFORMA GENERATOR\n", "bold medium_purple1")


@app.command("mile")
def display_milestones(
    file_path: Annotated[
        str,
        typer.Argument(
            help="Path to the contract file to process for billing",
        ),
    ],
) -> None:
    contract = json_handling.load_data(file_path)
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
    contract = json_handling.load_data(file_path)
    validate_milestones(milestones, contract)
    calculated_payload = data_dict.generate_calculated_data(contract, milestones)
    normalized_payload = data_dict.normalize_data(calculated_payload)
    contract.print_contract()
    contract.print_selected_milestones(milestones)
    generator.generate_pdf(normalized_payload, milestones)
    pretty_msg("Proforma generated successfully.", "chartreuse3")


@app.command("update")
def update_contract(
    file_path: Annotated[
        str,
        typer.Argument(
            help="Path to the contract file to update",
        ),
    ],
    milestones: Annotated[
        list[int],
        typer.Argument(
            help="Selects milestones to update",
        ),
    ],
    billing_status: Annotated[
        str,
        typer.Option(
            help="Milestone billing status to set",
            prompt="Billing status [b: billed / n: not billed / q quit]",
        ),
    ],
) -> None:
    contract = json_handling.load_data(file_path)
    validate_milestones(milestones, contract)
    if billing_status in ["b", "n"]:
        json_handling.update_json(file_path, contract, milestones, billing_status)
        pretty_msg("Billing status updated", "chartreuse3")
    elif billing_status == "q":
        pretty_msg("Leaving...", "medium_purple1")
    else:
        pretty_msg("Not a valid status", "red3")


if __name__ == "__main__":
    app()
