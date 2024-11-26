import pandas as pd
import MySQLdb

# Read the Excel file
df = pd.read_excel(r"D:\Harshavardhan M\Coding\BCS403\DBMS_FINAL\students.xlsx", sheet_name="Sheet3")

# Establish a MySQL connection
database = MySQLdb.connect(host="localhost", user="root", passwd="Treo1gpmd$", db="bcs403")

# Get the cursor, which is used to traverse the database, line by line
cursor = database.cursor()

# Create the INSERT INTO SQL query
query = """INSERT INTO final_vtu (USN, NAME, 18CS81, 18CS82, 18CSP83, 18CS84, 18CSI85, SGPA) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

# Iterate through each row in the DataFrame
for index, row in df.iterrows():
    usn = row['USN']
    name = row['NAME']
    cs81 = row['18CS81']
    cs82 = row['18CS82']
    csp83 = row['18CSP83']
    cs84 = row['18CS84']
    csi85 = row['18CSI85']
    sgpa = row['SGPA']

    # Assign values from each row
    values = (usn, name, cs81, cs82, csp83, cs84, csi85, sgpa)

    # Execute SQL Query
    cursor.execute(query, values)


# Close the cursor
cursor.close()

# Commit the transaction
database.commit()

# Close the database connection
database.close()

# Print results
print("")
print("All Done! Bye, for now.")
print("")
rows = str(len(df))
print("I just imported " + rows + " rows to MySQL!")