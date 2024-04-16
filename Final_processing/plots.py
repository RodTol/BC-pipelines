import matplotlib.pyplot as plt
import pandas as pd
import sys

from matplotlib.colors import to_hex

def get_viridis_colors(num_colors):
    viridis_cmap = plt.get_cmap("viridis_r")
    viridis_colors = [to_hex(viridis_cmap(i / num_colors)) for i in range(num_colors)]

    return viridis_colors

def assign_colors_to_elements(elements):
    colors = {}
    viridis_colors = get_viridis_colors(len(elements))
    
    # Assign colors from the palette to each element
    for i, element in enumerate(elements):
        colors[element] = viridis_colors[i]
    
    return colors

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
colors = assign_colors_to_elements(unique_nodes)

# Dictionary to store the unique nodes and their colors
node_colors_dict = {}

plt.figure(figsize=(10, 10))

for index, row in df.iterrows():
    node_color = colors[row['Node']]
    # Check if the node color is already in the dictionary
    if node_color not in node_colors_dict:
        node_colors_dict[node_color] = row['Node']
        # Create a bar with label for the first occurrence of the node
        plt.bar(index, row['Samples/s'], color=node_color, label=row['Node'], width=0.8, align='center')
    else:
        # Create a bar without label for subsequent occurrences of the same node
        plt.bar(index, row['Samples/s'], color=node_color, width=0.8, align='center')


    plt.text(index, row['Samples/s'] + 0.1, f"{row['Input Read Files']}", ha='center', va='bottom', fontsize=8, color='black')
    

# Customize the plot
plt.ylabel('Samples/s')
plt.xlabel('Run')
plt.title('Samples/s')
plt.legend()
plt.xticks(range(len(df)), df.index)
plt.savefig('bar_chart.png')
plt.close()

