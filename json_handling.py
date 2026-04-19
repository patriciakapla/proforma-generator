import json


def load_data():
    with open("contract_data.json", "r", encoding="utf8") as file:
        billing_data = json.load(file)
    return billing_data


def select_milestone(billing_data):
    for milestone_id, milestone in billing_data["paymentSchedule"].items():
        print("[" + milestone_id + "]")
        for key, value in milestone.items():
            print(
                key + ":",
                value,
            )
        print()
    selected_milestone = input("Enter code for the milestone to be billed: ")
    return selected_milestone


def update_billing_data(billing_data, selected_milestone):
    billing_data["paymentSchedule"][selected_milestone]["billed"] = True
    return billing_data


def update_contract_data(billing_data):
    with open("contract_data.json", "w", encoding="utf8") as file:
        json.dump(billing_data, file, indent=2)


billing_data = load_data()
print(billing_data)

selected_milestone = select_milestone(billing_data)

billing_data = update_billing_data(billing_data, selected_milestone)
print(billing_data)
update_contract_data(billing_data)
