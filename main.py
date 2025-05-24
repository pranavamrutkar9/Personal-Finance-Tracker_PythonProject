import pandas as pd
import csv
from datetime import datetime
from data_entry import get_date, get_amount, get_category, get_description
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date","amount","category","description"]
    DATE_FORMAT = "%d-%m-%y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)
    
    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date":date,
            "amount":amount,
            "category":category,
            "description":description
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry Added Successfully!!")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=CSV.DATE_FORMAT, errors="coerce")
        df = df.sort_values(by="date")

        start_date = datetime.strptime(start_date, CSV.DATE_FORMAT)
        end_date = datetime.strptime(end_date, CSV.DATE_FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("\nNo transactions found in given date range.")
        else:
            print(f"\nTransactions from {start_date.strftime(CSV.DATE_FORMAT)} to {end_date.strftime(CSV.DATE_FORMAT)}")
            print(filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(CSV.DATE_FORMAT)}))
            
            total_inflow = filtered_df[filtered_df["category"]=="Inflow"]["amount"].sum()
            total_outflow = filtered_df[filtered_df["category"]=="Outflow"]["amount"].sum()
            print("\nSummary")
            print(f"Total Inflow: {total_inflow}")
            print(f"Total Outflow: {total_outflow}")
            print(f"Total Savings: {(total_inflow-total_outflow):.2f}")
        return filtered_df

def add():
    CSV.initialize_csv()
    date = get_date("\nDate for Transaction (dd-mm-yy)/ Enter for today's date: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)

def plot_transactions(df):
    df.set_index('date', inplace=True)

    full_range = pd.date_range(start=df.index.min(), end=df.index.max())

    inflow_df = df[df["category"]=="Inflow"].resample("D").sum().reindex(full_range, fill_value=0)
    outflow_df = df[df["category"]=="Outflow"].resample("D").sum().reindex(full_range, fill_value=0)

    plt.figure(figsize=(10,5))
    plt.plot(inflow_df.index, inflow_df["amount"], label = "Inflow", color = "g")
    plt.plot(outflow_df.index, outflow_df["amount"], label = "Outflow", color = "r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Inflow and Outflow Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()
    
    
def main():
    while True:
        print("1. Add new Transaction")
        print("2. View Transaction Summary")
        print("3. Exit")
        choice = input("Enter Choice (1/2/3): ")
        # print("\n")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter start date: ")
            end_date = get_date("Enter end date: ")
            df = CSV.get_transactions(start_date, end_date)
            if input("Do you want to plot transactions? (y/n): ").lower()=="y":
                plot_transactions(df)
            continue
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid Choice. Enter 1/2/3: ")

if __name__ == "__main__":
    main()