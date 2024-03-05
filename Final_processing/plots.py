import matplotlib.pyplot as plt
import pandas as pd
import sys


csv_file_path = sys.argv[1]
df = pd.read_csv(csv_file_path)
file_counts = df.groupby('Node')['Input Read Files'].sum()

total_files = file_counts.sum()

plt.figure(figsize=(10, 10))
plt.pie(file_counts, labels=file_counts.index, autopct='%1.0f%%', startangle=140)


plt.title('Number of Files Processed by Each Node')

# Display the total number of files
plt.text(0, -1.2, f'Total Files: {total_files}', ha='center', va='center', fontsize=12, color='darkblue')

plt.savefig('pie_chart.png')
#---------------------------

plt.barh(df["Node"], df["Samples/s"], color='skyblue')
plt.xlabel('Samples/s')
plt.ylabel('Node')

plt.title('Samples/s Performance of Each Node')

plt.savefig('bar_chart.png')


