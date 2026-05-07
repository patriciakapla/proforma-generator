from jinja2 import Environment, FileSystemLoader, Template
from weasyprint import HTML  # pyright: ignore[reportMissingTypeStubs]
from pathlib import Path
from data_dict import CalculatedData


def create_jinja_environment(templates_path: Path) -> Environment:
    env = Environment(loader=FileSystemLoader(str(templates_path)))
    return env


def load_template(env: Environment, template_path: str) -> Template:
    template = env.get_template(template_path)
    return template


def render_final_html(
    template: Template,
    # being_billed: list[int],
    base_templates_url: Path,
    **contract_data: object
) -> HTML:
    final_html = HTML(
        string=template.render(**contract_data),
        base_url=str(base_templates_url),
    )
    return final_html


def define_pdf_name(data: CalculatedData) -> str:
    pdf_name = (
        str(data["contract_id"])
        + " - "
        + data["title"]
        + " - certificación "
        + data["date_today"]
        + ".pdf"
    )
    return pdf_name


def write_pdf(final_html: HTML, pdf_name: str) -> None:
    pdf_path = Path("pdf") / pdf_name
    final_html.write_pdf(str(pdf_path))  # pyright: ignore[reportUnknownMemberType]


def generate_pdf(data: CalculatedData, milestones: list[int]) -> None:
    templates_path = Path(__file__).parent / "templates"
    env = create_jinja_environment(templates_path)
    template = load_template(env, "index.html")
    final_html = render_final_html(
        template,
        templates_path,
        # variables to be inserted in HTML
        contract_id=data["contract_id"],
        title=data["title"],
        client=data["client"],
        client_project_manager=data["client_project_manager"],
        client_tax_id=data["client_tax_id"],
        address=data["address"],
        proposal=data["proposal"],
        proposal_date=data["proposal_date"],
        contract_amount=data["contract_amount"],
        currency=data["currency"],
        payment_schedule=data["payment_schedule"],
        milestone_amount_list=data["milestone_amounts"],
        milestone_to_bill=milestones,
        date_today=data["date_today"],
        base_month=data["base_month"],
        current_month=data["current_month"],
        cpi_variation=data["cpi_variation"],
        subtotal_amount=data["subtotal_amount"],
        adjustment_amount=data["adjustment_amount"],
        adjusted_subtotal=data["adjusted_subtotal"],
    )
    pdf_name = define_pdf_name(data)
    write_pdf(final_html, pdf_name)
