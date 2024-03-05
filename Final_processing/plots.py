import matplotlib.pyplot as plt
import pandas as pd
import sys


csv_file_path = sys.argv[1]
df = pd.read_csv(csv_file_path)
file_counts = df.groupby('Node')['Input Read Files'].sum()

total_files = file_counts.sum()

plt.figure(figsize=(10, 10))
plt.pie(file_counts, labels=file_counts.index, autopct='%1.0f%%', startangle=140)

# Display the number of files instead of percentages
plt.gca().set_aspect('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title('Number of Files Processed by Each Node')

# Display the total number of files
plt.text(0, -1.2, f'Total Files: {total_files}', ha='center', va='center', fontsize=12, color='darkblue')

plt.savefig('pie_chart.png')


