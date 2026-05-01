from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from pathlib import Path
import utils
import requests
import pricing


def create_jinja_environment(templates_route):
    env = Environment(loader=FileSystemLoader(str(templates_route)))
    return env


def load_template(env, template_name):
    template = env.get_template(template_name)
    return template


def render_final_html(template, being_billed, base_templates_url, **contract_data):
    final_html = HTML(
        string=template.render(beingBilled=being_billed, **contract_data),
        base_url=str(base_templates_url),
    )
    return final_html


def define_pdf_name(contract_number, contract_title):
    pdf_name = (
        str(contract_number)
        + " - "
        + contract_title
        + " - certificación "
        + utils.get_current_date("%Y-%m-%d")
        + ".pdf"
    )
    return pdf_name


def write_pdf(final_html, pdf_name):
    final_html.write_pdf("./pdf/" + pdf_name)


def generate_pdf(contract_pointer, milestone_to_bill):
    templates_path = Path(__file__).parent / "templates"
    env = create_jinja_environment(templates_path)
    template = load_template(env, "index.html")
    response = requests.get(pricing.define_request(contract_pointer))
    cpi_data = response.json()
    final_html = render_final_html(
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
        dateToday=utils.get_current_date("%Y-%m-%d"),
        address=contract_pointer["address"],
        currency=contract_pointer["currency"],
        contractAmount=utils.format_num_2dec(contract_pointer["contractAmount"]),
        paymentSchedule=contract_pointer["paymentSchedule"],
        milestoneToBill=milestone_to_bill,
        baseMonth=pricing.get_cpi_base_date(contract_pointer),
        currentMonth=utils.get_current_date("%Y-%m"),
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

    pdf_name = define_pdf_name(
        contract_pointer["contractNumber"],
        contract_pointer["contractTitle"],
    )
    write_pdf(final_html, pdf_name)


# # testing
# if __name__ == "__main__":
#     being_billed = 0
#     env = create_jinja_environment("templates")

#     template = load_template(env, "index.html")

#     final_html = render_final_html(
#         template,
#         being_billed,
#         base_templates_url="./templates/",
#         contractNumber=666,
#         contractTitle="Vampire Hunt",
#     )

#     write_pdf(final_html, "test.pdf")
