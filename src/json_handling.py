import json
import typer
from pathlib import Path


def load_data(file_path: Path):
    from contract import Contract

    try:
        with open(file_path, "r", encoding="utf8") as file:
            data = json.load(file)
        return Contract(
            contract_id=data["contractID"],
            title=data["contractTitle"],
            client=data["clientName"],
            client_tax_id=data["clientTaxID"],
            client_project_manager=data["clientProjectManager"],
            address=data["address"],
            proposal=data["proposalID"],
            proposal_date=data["proposalDate"],
            amount=data["contractAmount"],
            currency=data["currency"],
            payment_schedule=data["paymentSchedule"],
        )
    except FileNotFoundError:
        raise typer.BadParameter(f'File "{file_path}" not found!')


# def update_billing_status(file_pointer, selected_milestone, billing_status: bool):
#     file_pointer["paymentSchedule"][selected_milestone]["billed"] = billing_status
#     return file_pointer


# def update_json(file_pointer):
#     with open("contract_data.json", "w", encoding="utf8") as file:
#         json.dump(file_pointer, file, indent=2)
