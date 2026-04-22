from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML


def create_jinja_environment(templates_route):
    env = Environment(loader=FileSystemLoader(templates_route))
    return env


def load_template(env, template_name):
    template = env.get_template(template_name)
    return template


def render_final_html(template, being_billed, base_templates_url, **contract_data):
    final_html = HTML(
        string=template.render(beingBilled=being_billed, **contract_data),
        base_url=base_templates_url,
    )
    # print(*contract_data)        #     TESTING
    return final_html


def define_pdf_name(contract_number, contract_title, today):
    pdf_name = (
        str(contract_number)
        + " - "
        + contract_title
        + " - certificación "
        + today
        + ".pdf"
    )
    return pdf_name


def write_pdf(final_html, pdf_name):
    final_html.write_pdf("./pdf/" + pdf_name)


# testing
if __name__ == "__main__":
    being_billed = 0
    env = create_jinja_environment("templates")

    template = load_template(env, "index.html")

    final_html = render_final_html(
        template,
        being_billed,
        base_templates_url="./templates/",
        contractNumber=666,
        contractTitle="Vampire Hunt",
    )

    # pdf_name = define_pdf_name("test", "test", "test")

    # print(pdf_name)

    write_pdf(final_html, "test.pdf")
