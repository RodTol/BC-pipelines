import matplotlib.pyplot as plt
import pandas as pd
import sys
import numpy as np

csv_file_path = sys.argv[1]
df = pd.read_csv(csv_file_path)

# Plot pie chart
file_counts = df.groupby('Node')['Input Read Files'].sum()
total_files = file_counts.sum()

plt.figure(figsize=(10, 10))
plt.pie(file_counts, labels=file_counts.index, autopct='%1.0f%%', startangle=140)
plt.title('Number of Files Processed by Each Node')
plt.text(0, -1.2, f'Total Files: {total_files}', ha='center', va='center', fontsize=12, color='darkblue')
plt.savefig('pie_chart.png')
plt.close()

fig, ax = plt.subplots()

plt.bar(df['Node'], df['Samples/s'])

# Set labels and title
ax.set_xlabel('Node')
ax.set_ylabel('Samples/s')
ax.set_title('Run Speed Comparison')

# Display the legend
ax.legend()

plt.savefig('bar_chart.png')
plt.close()

