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

# Group by Node and create a bar plot for each run
# Group by Node and plot a bar for each node
fig, ax = plt.subplots()
for name, group in df.groupby('Node'):
    ax.bar(name, group['Samples/s'].values[0], label=name)

# Set labels and title
ax.set_xlabel('Node')
ax.set_ylabel('Samples/s')
ax.set_title('Samples/s for Each Node')
ax.legend(title='Node')

plt.savefig('bar_chart.png')
plt.close()

