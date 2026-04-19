import json


def data_variable_setting():
    with open("data.json", "r", encoding="utf8") as file:
        data = json.load(file)
    return data


def ask_milestone_to_be_billed(data):
    for i, milestone in data["paymentSchedule"].items():
        print("[" + i + "]")
        for key, description in milestone.items():
            print(
                key + ":",
                description,
            )
        print()
    tobe_billed = input("Enter code for the milestone to be billed: ")
    return tobe_billed


data = data_variable_setting()

tobe_billed = ask_milestone_to_be_billed(data)
print(tobe_billed)
