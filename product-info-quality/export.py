import pandas as pd
from database import engine

def main():
    # Load the products table into a Pandas DataFrame
    df = pd.read_sql_table("products", con=engine)

    # Save it to a CSV file named products.csv
    df.to_csv("products.csv", index=False)
    print("Success! 'products.csv' has been created in your folder.")

if __name__ == "__main__":
    main()