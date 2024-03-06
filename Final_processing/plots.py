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

# Get unique nodes and assign colors dynamically
unique_nodes = df['Node'].unique()
colors = plt.cm.rainbow(range(len(unique_nodes)))
plt.figure(figsize=(10, 10))

for index, row in df.iterrows():
    node_color = colors[list(unique_nodes).index(row['Node'])]
    plt.bar(index, row['Samples/s'], color=node_color, width=0.8, align='center')

    plt.text(index, row['Samples/s'] + 0.1, f"{row['Input Read Files']}", ha='center', va='bottom', fontsize=8, color='black')

# Customize the plot
plt.ylabel('Samples/s')
plt.title('Samples/s')
plt.xticks(range(len(df)), df.index)
plt.legend(labels=unique_nodes)
plt.savefig('bar_chart.png')
plt.close()

