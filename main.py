import typer
from typing import Annotated
from rich import print

# import template_generator as generator
import json_handling

# from datetime import date


def main(
    file_path: Annotated[
        str, typer.Argument(help="Path to the contract file to process for billing")
    ],
    m: Annotated[
        bool, typer.Option(help="Display the contract's payment milestones")
    ] = False,
):
    data = json_handling.load_data(file_path)
    milestone_list = [milestone for milestone in data["paymentSchedule"]]
    print(
        f"[bold]PROFORMA GENERATOR[/bold] - Contract: [yellow] \
        {file_path.removesuffix(".json")}[/yellow]"
    )
    if m:
        print_milestones(milestone_list)


def print_milestones(milestones):
    for i, milestone in enumerate(milestones):
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


if __name__ == "__main__":
    typer.run(main)


# today = date.today()
# today_str = today.strftime("%Y-%m-%d")


# TESTING

# being_billed = 0

# env = generator.create_jinja_environment("templates")

# template = generator.load_template(env, "index.html")

# final_html = generator.render_final_html(
#     template,
#     being_billed,
#     base_templates_url="./templates/",
#     contractNumber=data["contractNumber"],
#     contractTitle=data["contractTitle"],
# )

# pdf_name = generator.define_pdf_name(
#     data["contractNumber"], data["contractTitle"], today_str
# )

# print(pdf_name)

# generator.write_pdf(final_html, pdf_name)
