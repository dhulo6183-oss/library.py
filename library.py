import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class LibraryDashboard:

    def __init__(self):
        self.df = None

    def load_data(self, file_path):
        try:
            self.df = pd.read_csv(file_path)

            required_cols = [
                "Transaction ID",
                "Date",
                "User ID",
                "Book Title",
                "Genre",
                "Borrowing Duration (Days)"
            ]

            missing = [col for col in required_cols if col not in self.df.columns]

            if len(missing) > 0:
                print("Missing columns:", missing)
                self.df = None
                return

            self.df.dropna(inplace=True)
            print("Data loaded successfully")

        except Exception as e:
            print("Error:", e)

    def calculate_statistics(self):
        if self.df is None:
            print("Load data first")
            return

        print("\nStatistics:")

        most_borrowed = self.df["Book Title"].value_counts().head(1)
        print("Most Borrowed Book:\n", most_borrowed)

        avg_duration = np.mean(self.df["Borrowing Duration (Days)"])
        print("Average Borrowing Duration:", avg_duration)

        self.df["Date"] = pd.to_datetime(self.df["Date"])
        busiest_day = self.df["Date"].dt.day_name().value_counts().head(1)
        print("Busiest Day:\n", busiest_day)

    def filter_transactions(self):
        if self.df is None:
            print("Load data first")
            return

        print("\n1. Filter by Genre")
        print("2. Filter by Date Range")

        choice = input("Enter choice: ")

        match choice:
            case "1":
                genre = input("Enter genre: ")
                result = self.df[self.df["Genre"] == genre]
                print(result)

            case "2":
                start = input("Start date (YYYY-MM-DD): ")
                end = input("End date (YYYY-MM-DD): ")

                self.df["Date"] = pd.to_datetime(self.df["Date"])
                result = self.df[
                    (self.df["Date"] >= start) &
                    (self.df["Date"] <= end)
                ]
                print(result)

            case _:
                print("Invalid choice")

    def generate_report(self):
        if self.df is None:
            print("Load data first")
            return

        print("\nGenerating Report...")

        print("Total Transactions:", len(self.df))
        print("Unique Users:", self.df["User ID"].nunique())
        print("Unique Books:", self.df["Book Title"].nunique())

    def visualize(self):
        if self.df is None:
            print("Load data first")
            return

        print("\n1. Bar Chart")
        print("2. Line Graph")
        print("3. Pie Chart")
        print("4. Heatmap")

        choice = input("Enter choice: ")

        match choice:

            case "1":
                top_books = self.df["Book Title"].value_counts().head(5)
                top_books.plot(kind="bar")
                plt.title("Top 5 Most Borrowed Books")
                plt.show()

            case "2":
                self.df["Date"] = pd.to_datetime(self.df["Date"])
                monthly = self.df.groupby(self.df["Date"].dt.month).size()
                monthly.plot()
                plt.title("Borrowing Trend")
                plt.show()

            case "3":
                genre = self.df["Genre"].value_counts()
                genre.plot(kind="pie", autopct="%1.1f%%")
                plt.title("Genre Distribution")
                plt.show()

            case "4":
                self.df["Day"] = pd.to_datetime(self.df["Date"]).dt.day_name()
                pivot = pd.crosstab(self.df["Day"], self.df["Genre"])
                sns.heatmap(pivot, annot=True)
                plt.title("Heatmap")
                plt.show()

            case _:
                print("Invalid choice")


def main():
    dashboard = LibraryDashboard()

    while True:

        print("\n===== Library Dashboard =====")
        print("1. Load Data")
        print("2. Calculate Statistics")
        print("3. Filter Transactions")
        print("4. Generate Report")
        print("5. Visualize")
        print("6. Exit")

        choice = input("Enter choice: ")

        match choice:

            case "1":
                path = input("Enter CSV file path: ")
                dashboard.load_data(path)

            case "2":
                dashboard.calculate_statistics()

            case "3":
                dashboard.filter_transactions()

            case "4":
                dashboard.generate_report()

            case "5":
                dashboard.visualize()

            case "6":
                print("Exiting...")
                break

            case _:
                print("Invalid choice")


if __name__ == "__main__":
    main()
