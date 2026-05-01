from datetime import date
import pricing

# Formatting


def format_num_2dec(number):
    return f"{number:,.2f}"


def format_string_to_float(value):
    new_value = value.replace(",", "")
    return float(new_value)


def get_current_date(date_format):
    """returns a string formatted for the final PDF"""
    today = date.today()
    today_str = today.strftime(date_format)
    return today_str


# Contract related utils


def get_milestones(file_pointer):
    milestone_list = [milestone for milestone in file_pointer["paymentSchedule"]]
    return milestone_list


def print_milestones(file_pointer, milestones_list):
    pricing.calculate_milestone_amount(file_pointer)
    for i, milestone in enumerate(milestones_list):
        print(f"[bold yellow][{i+1}]: [/bold yellow]", sep="", end=" ")
        for key, value in milestone.items():
            match key:
                case "percentage":
                    print(f"[default]{value}% - [/default]", sep="", end=" ")
                case "description":
                    print(value)
                case "billed":
                    (
                        print("[green]Billed[/green]")
                        if value
                        else print("[red]Not billed[/red]")
                    )
        print()
