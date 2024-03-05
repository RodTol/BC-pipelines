import matplotlib.pyplot as plt
import pandas as pd
import sys


csv_file_path = sys.argv[1]
df = pd.read_csv(csv_file_path)

# Group data by Node and sum the number of files processed
file_counts = df.groupby('Node')['Input Read Files'].sum()

# Create a pie chart
plt.figure(figsize=(8, 8))
plt.pie(file_counts, labels=file_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Number of Files Processed by Each Node')
# Save the pie chart to a file
plt.savefig('pie_chart.png')

