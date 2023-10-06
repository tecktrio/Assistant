import pandas as pd

# Example data
data = {'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'City': ['New York', 'San Francisco', 'Los Angeles']}

# Create a DataFrame
df = pd.DataFrame(data)

# Export the DataFrame to an Excel file
excel_file_path = "Assistant.xlsx"  # Specify the file path
df.to_excel(excel_file_path, index=False)  # Set index=False to exclude the index column
