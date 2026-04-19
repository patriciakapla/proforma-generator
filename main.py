import template_generator as generator
import json_handling
from datetime import date

today = date.today()
today_str = today.strftime("%Y-%m-%d")


# TESTING
data = json_handling.load_data("contract_data.json")

being_billed = 0

env = generator.create_jinja_environment("templates")

template = generator.load_template(env, "index.html")

final_html = generator.render_final_html(
    template,
    being_billed,
    "C:/dev/proforma-generator/templates/",
    contractNumber=data["contractNumber"],
    contractTitle=data["contractTitle"],
)

pdf_name = generator.define_pdf_name(
    data["contractNumber"], data["contractTitle"], today_str
)

print(pdf_name)

generator.write_pdf(final_html, pdf_name)
