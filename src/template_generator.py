from jinja2 import Environment, FileSystemLoader, Template
from weasyprint import HTML
from pathlib import Path
import utils
import price_index
from contract import Contract


def create_jinja_environment(templates_path: Path) -> Environment:
    env = Environment(loader=FileSystemLoader(str(templates_path)))
    return env


def load_template(env: Environment, template_path: str) -> Template:
    template = env.get_template(template_path)
    return template


def render_final_html(
    template: Template,
    being_billed: int,
    base_templates_url: Path,
    **contract_data: (
        int | float | str | bool | dict[str, str] | list[dict[str, str | int | bool]]
    )
) -> HTML:
    final_html = HTML(
        string=template.render(beingBilled=being_billed, **contract_data),
        base_url=str(base_templates_url),
    )
    print("final html", final_html)
    return final_html


def define_pdf_name(contract: Contract) -> str:
    pdf_name = (
        str(contract.contract_id)
        + " - "
        + contract.title
        + " - certificación "
        + utils.today("%Y-%m-%d")
        + ".pdf"
    )
    return pdf_name


def write_pdf(final_html: HTML, pdf_name: str) -> None:
    final_html.write_pdf("./pdf/" + pdf_name)


def generate_pdf(contract: Contract, milestone_to_bill: int):
    templates_path = Path(__file__).parent / "templates"
    env = create_jinja_environment(templates_path)
    template = load_template(env, "index.html")
    final_html = render_final_html(
        template,
        milestone_to_bill,
        templates_path,
        # variables to be inserted in HTML
        contractNumber=contract.contract_id,
        contractTitle=contract.title,
        clientName=contract.client,
        clientProjectManager=contract.client_project_manager,
        clientTaxID=contract.client_tax_id,
        proposalID=contract.proposal,
        proposalDate=contract.get_contract_date(),
        dateToday=utils.today("%Y-%m-%d"),
        address=contract.address,
        currency=contract.currency,
        contractAmount=utils.format_num_2dec(contract.amount),
        paymentSchedule=contract.payment_schedule,
        milestoneToBill=milestone_to_bill,
        baseMonth=contract.get_cpi_base_date(),
        currentMonth=utils.today("%Y-%m"),
        cpiVariation=utils.format_num_2dec(price_index.get_cpi_variation(contract)),
        adjustmentAmount=utils.format_num_2dec(
            price_index.calculate_adjustment_amount(contract, milestone_to_bill)
        ),
        adjustedSubtotal=utils.format_num_2dec(
            price_index.calculate_adjusted_subtotal(contract, milestone_to_bill)
        ),
    )

    pdf_name = define_pdf_name(contract)
    write_pdf(final_html, pdf_name)
