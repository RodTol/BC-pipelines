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

# Group data by 'Node'
grouped_data = df.groupby('Node')
fig, ax = plt.subplots()

# Assign different colors to each group
colors = iter(plt.cm.rainbow_r(np.linspace(0, 1, len(grouped_data))))

# Plot each group separately
for name, group in grouped_data:
    color = next(colors)
    ax.bar(group.index, group['Samples/s'], color=color, label=f'{name} - {group["Input Read Files"].sum()} files')

# Set labels and title
ax.set_xlabel('Run Index')
ax.set_ylabel('Samples/s')
ax.set_title('Run Speed Comparison')
ax.legend()
plt.savefig('bar_chart.png')
plt.close()


