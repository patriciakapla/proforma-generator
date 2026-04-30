import typer
from typing import Annotated
from rich import print
import json_handling
import template_generator as generator
import pricing
import requests
from pathlib import Path
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

    data = load_contract(file_path)
    milestone_list = get_milestones(data)
    print(get_milestones(load_contract("contract_data.json")))
    print()
    print_milestones(data, milestone_list)


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
    data = load_contract(file_path)
    today = utils.get_current_date()
    pricing.calculate_milestone_amount(data)
    generate_pdf(data, milestone_to_bill, today)


def print_milestones(file_pointer, milestones_list):
    pricing.calculate_milestone_amount(file_pointer)
    for i, milestone in enumerate(milestones_list):
        print(f"[bold yellow][{i+1}]: [/bold yellow]", sep="", end=" ")
        for key, value in milestone.items():
            match key:
                case "percentage":
                    print(f"[default]{value}% - [/default]", sep="", end=" ")
                case "description":
                    print(value)
                case "billed":
                    (
                        print("[green]Billed[/green]")
                        if value
                        else print("[red]Not billed[/red]")
                    )
        print()


def load_contract(file_path):
    data = json_handling.load_data(file_path)
    print(f"Selected contract: [yellow]{data["contractTitle"]}[/yellow]")
    return data


def get_milestones(file_pointer):
    milestone_list = [milestone for milestone in file_pointer["paymentSchedule"]]
    return milestone_list


def generate_pdf(contract_pointer, milestone_to_bill, today):
    templates_path = Path(__file__).parent / "templates"
    env = generator.create_jinja_environment(templates_path)
    template = generator.load_template(env, "index.html")
    response = requests.get(pricing.define_request(contract_pointer))
    cpi_data = response.json()
    final_html = generator.render_final_html(
        template,
        milestone_to_bill,
        templates_path,
        # variables to be inserted in HTML
        contractNumber=contract_pointer["contractNumber"],
        contractTitle=contract_pointer["contractTitle"],
        clientName=contract_pointer["clientName"],
        clientProjectManager=contract_pointer["clientProjectManager"],
        clientTaxID=contract_pointer["clientTaxID"],
        proposalNumber=contract_pointer["proposalNumber"],
        proposalDate=pricing.get_contract_date(contract_pointer),
        dateToday=today,
        address=contract_pointer["address"],
        currency=contract_pointer["currency"],
        contractAmount=utils.format_num_2dec(contract_pointer["contractAmount"]),
        paymentSchedule=contract_pointer["paymentSchedule"],
        milestoneToBill=milestone_to_bill,
        baseMonth=pricing.get_cpi_base_date(contract_pointer),
        currentMonth=today[:7],
        cpiVariation=utils.format_num_2dec(pricing.get_cpi_variation(cpi_data)),
        adjustmentAmount=utils.format_num_2dec(
            pricing.calculate_adjustment_amount(
                contract_pointer, milestone_to_bill, cpi_data
            )
        ),
        adjustedSubtotal=utils.format_num_2dec(
            pricing.calculate_adjusted_subtotal(
                contract_pointer, milestone_to_bill, cpi_data
            )
        ),
    )

    pdf_name = generator.define_pdf_name(
        contract_pointer["contractNumber"], contract_pointer["contractTitle"], today
    )
    generator.write_pdf(final_html, pdf_name)


if __name__ == "__main__":
    app()
