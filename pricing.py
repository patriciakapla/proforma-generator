import json_handling


def format_price(price_pointer):
    return f"{price_pointer:,.2f}"


def calculate_milestone_amount(file_pointer):
    """
    calculates the amount of all contract's milestones
    """
    contract_amount = file_pointer["contractAmount"]

    for milestone in file_pointer["paymentSchedule"]:
        if not milestone["amount"]:
            percentage = milestone["percentage"]
            multiplier = percentage * 0.01
            amount = contract_amount * multiplier
            milestone["amount"] = format_price(amount)
    return file_pointer


def get_ipc_base_month(file_pointer):
    """
    calculates base month for adjustment calculation
    """
    if file_pointer["proposalDate"]["month"] == 1:
        base_year = file_pointer["proposalDate"]["year"] - 1
        base_month = 12
    else:
        base_year = file_pointer["proposalDate"]["year"]
        base_month = file_pointer["proposalDate"]["month"] - 1
    base_date = f"{base_year}-{base_month}"
    return base_date


def get_contract_date(file_pointer):
    return f"{file_pointer['proposalDate']['year']}-{file_pointer['proposalDate']['month']}"


def get_base_ipc_index(contract_pointer, ipc_pointer):
    for k, v in ipc_pointer.items():
        if k == get_ipc_base_month(contract_pointer):
            return v


def format_index(get_index_function):
    index = get_index_function * 100
    return f"{index:,.2f}"
