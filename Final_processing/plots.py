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
bar_width = 0.8 / len(grouped_data)  # Adjusted width for thinner bars
for i, (name, group) in enumerate(grouped_data):
    color = next(colors)
    x_values = np.arange(len(group)) + i * bar_width
    ax.bar(x_values, group['Samples/s'], width=bar_width, color=color, label=name)
    
    # Add text label near each column with the number of input files
    for j, value in enumerate(group['Input Read Files']):
        ax.text(x_values[j], group['Samples/s'].iloc[j], str(value),
                ha='center', va='bottom', fontsize=8, color='black')

# Set labels and title
ax.set_xlabel('Node')
ax.set_ylabel('Samples/s')
ax.set_title('Run Speed Comparison')
ax.set_xticks(np.arange(len(df['Node'].unique())) + (bar_width * (len(grouped_data) - 1)) / 2)
ax.set_xticklabels(df['Node'].unique())
plt.legend(title='Node', loc='upper right')
plt.savefig('bar_chart.png')
plt.close()


