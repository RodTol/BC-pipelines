import matplotlib.pyplot as plt
import pandas as pd
import sys

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

# Get unique nodes and assign unique colors
unique_nodes = df['Node'].unique()
colors = plt.cm.viridis(range(len(unique_nodes)))

# Create a color dictionary mapping each node to its color
node_color_dict = dict(zip(unique_nodes, colors))

# Plot bar chart
plt.figure(figsize=(12, 8))

for index, row in df.iterrows():
    node = row['Node']
    color = node_color_dict.get(node, 'gray')  # Use gray if the node is not explicitly defined in node_color_dict
    plt.barh(row['Node'], row['Samples/s'], color=color, label=f'{row["Input Read Files"]}', alpha=0.7)

# Customize plot
plt.xlabel('Samples/s')
plt.ylabel('Node')
plt.title('Samples/s Performance of Each Run')
plt.legend(title='Input Read Files', loc='upper right', bbox_to_anchor=(1.15, 1))
plt.grid(axis='x', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig('bar_chart.png')
plt.close()


