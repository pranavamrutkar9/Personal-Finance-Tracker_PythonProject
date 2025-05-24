from datetime import datetime

date_format = "%d-%m-%y"
CATEGORIES = {"I":"Inflow", "O":"Outflow"}

def get_date(prompt, allow_default=False):
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)
    
    try:
        valid_date = datetime.strptime(date_str, date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print("Invalid date format. Enter date in dd-mm-yyyy format")
        return get_date(prompt, allow_default)

def get_amount():
    try:
        amount = float(input("Enter Amount: "))
        if amount<=0:
            raise ValueError("Amount must not be negative or zero.")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()

def get_category():
    category = input("Enter Tranasaction Category ('I' for inflow/'O' for Outflow): ").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]
    
    print("Invalid Category. Please enter a valid category.")
    return get_category()

def get_description():
    return input("Enter description: ")