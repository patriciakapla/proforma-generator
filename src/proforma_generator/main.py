import typer
from typing import Annotated
from proforma_generator import json_handling
import proforma_generator.template_generator as generator
from proforma_generator.utils import (
    validate_milestones,
    pretty_msg,
    validate_path,
    validate_env_var,
    complete_target,
    DirectoryTarget,
)
from proforma_generator import data_dict
from pathlib import Path
import subprocess

app = typer.Typer()

ENV_VAR_NAME_CONTRACTS = "CONTRACTS_DIR"
ENV_VAR_NAME_PDF = "PDF_DIR"


@app.callback()
def main():
    pretty_msg("\nPROFORMA GENERATOR\n", "bold medium_purple1")


@app.command("set")
def define_contracts_directory(
    path: Annotated[
        str,
        typer.Argument(
            help="Path to target directory. Path must be inside quotation marks"
        ),
    ],
    d: Annotated[
        DirectoryTarget,
        typer.Option(
            help="Directory target: select whether to configure the [contracts] or [pdf] directory.",
            autocompletion=complete_target,
        ),
    ],
):
    """
    Set the path to the directory containing contract JSON files
    - path: path to the directory
    """
    directory = Path(path)
    validate_path(directory)
    if d == DirectoryTarget.contract:
        subprocess.run(
            [
                "setx",
                ENV_VAR_NAME_CONTRACTS,
                str(directory),
            ],  #                         only works on windows
            check=True,
        )
        target = ENV_VAR_NAME_CONTRACTS
    elif d == DirectoryTarget.pdf:
        subprocess.run(
            [
                "setx",
                ENV_VAR_NAME_PDF,
                str(directory),
            ],
            check=True,
        )
        target = ENV_VAR_NAME_PDF

    pretty_msg(f"\n{target} set to:", "sea_green1", " ")
    pretty_msg(f"{path}\n", "light_goldenrod1")
    print("Close and reopen your terminal before running Proforma Generator again.")


@app.command("mile")
def display_milestones(
    file_name: Annotated[
        str,
        typer.Argument(
            help="Name of the contract file to process for billing (e.g. for file project_name.json, argument = project_name)",
        ),
    ],
) -> None:
    """
    Display contract's detailed payment schedule
    - file: JSON file containing contract data
    """
    validate_env_var(ENV_VAR_NAME_CONTRACTS)
    file_path = json_handling.define_json_path(file_name, ENV_VAR_NAME_CONTRACTS)
    contract = json_handling.load_data(file_path)
    contract.print_contract()
    contract.print_milestones()


@app.command("gen")
def generate_proforma(
    file_name: Annotated[
        str,
        typer.Argument(
            help="Name of the contract file to process for billing (e.g. for file project_name.json, argument = project_name)",
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
    - file: JSON file containing contract data
    - milestones: Milestones to bill
    """
    validate_env_var(ENV_VAR_NAME_CONTRACTS)
    validate_env_var(ENV_VAR_NAME_PDF)
    fp = json_handling.define_json_path(file_name, ENV_VAR_NAME_CONTRACTS)
    contract = json_handling.load_data(fp)
    validate_milestones(milestones, contract)
    calculated_payload = data_dict.generate_calculated_data(contract, milestones)
    normalized_payload = data_dict.normalize_data(calculated_payload)
    contract.print_contract()
    contract.print_selected_milestones(milestones)
    generator.generate_pdf(normalized_payload, milestones, ENV_VAR_NAME_PDF)
    pretty_msg("Proforma generated successfully.", "sea_green1")


@app.command("update")
def update_contract(
    file_name: Annotated[
        str,
        typer.Argument(
            help="Name of the contract file to update (e.g. for file project_name.json, argument = project_name)",
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
    """
    Update billing status in contract's JSON
    - file: JSON file containing contract data
    - milestones: Milestones to update billing status
    - billing_status: Status to be applied
    """
    validate_env_var(ENV_VAR_NAME_CONTRACTS)
    fp = json_handling.define_json_path(file_name, ENV_VAR_NAME_CONTRACTS)
    contract = json_handling.load_data(fp)
    validate_milestones(milestones, contract)
    if billing_status in ["b", "n"]:
        json_handling.update_json(contract, milestones, billing_status, fp)
        pretty_msg("Billing status updated", "sea_green1")
    elif billing_status == "q":
        pretty_msg("Leaving...", "medium_purple1")
    else:
        pretty_msg("Not a valid status", "indian_red")


if __name__ == "__main__":
    app()
