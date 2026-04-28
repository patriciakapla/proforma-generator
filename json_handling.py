import json


def load_data(file_route: str):
    with open(file_route, "r", encoding="utf8") as file:
        data = json.load(file)
    return data


def update_billing_status(file_pointer, selected_milestone):
    file_pointer["paymentSchedule"][selected_milestone][
        "billed"
    ] = True  # REVIEW: hardcoded True
    return file_pointer


def update_json(file_pointer):
    with open("contract_data.json", "w", encoding="utf8") as file:
        json.dump(file_pointer, file, indent=2)
