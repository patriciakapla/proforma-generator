import typer
from typing import Annotated
from rich import print
import json_handling
import template_generator as generator
from datetime import date


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
    print_milestones(milestone_list)


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
    today = get_date()
    generate_pdf(data, milestone_to_bill, today)


def print_milestones(milestones_list: list):
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
                    )  # if billed = True
        print()


def load_contract(file_path: str):
    data = json_handling.load_data(file_path)
    print(f"Selected contract: [yellow]{data["contractTitle"]}[/yellow]")
    return data


def get_milestones(data):
    milestone_list = [milestone for milestone in data["paymentSchedule"]]
    return milestone_list


def get_date():
    today = date.today()
    today_str = today.strftime("%Y-%m-%d")
    return today_str


def generate_pdf(data, milestone_to_bill, today):
    env = generator.create_jinja_environment("templates")
    template = generator.load_template(env, "index.html")
    final_html = generator.render_final_html(
        template,
        # variables to be inserted in HTML
        milestone_to_bill,
        base_templates_url="./templates/",
        contractNumber=data["contractNumber"],
        contractTitle=data["contractTitle"],
    )
    pdf_name = generator.define_pdf_name(
        data["contractNumber"], data["contractTitle"], today
    )
    generator.write_pdf(final_html, pdf_name)


if __name__ == "__main__":
    app()
