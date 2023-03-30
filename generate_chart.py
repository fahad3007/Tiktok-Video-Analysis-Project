import pandas as pd
import matplotlib.pyplot as plt

# Define the filename and read in the CSV file as a Pandas DataFrame
filename = 'merged.csv'
df = pd.read_csv(filename)

# Group the DataFrame by category and emotion, and count the number of occurrences
counts = df.groupby(['label', 'emotion']).size()

# Create a dictionary to map category numbers to names
categories = {0: 'Ukraine War', 1: 'Climate Change', 2: '5G'}

# Create a bar chart for each category
for category in categories:
    # Select the counts for the current category
    category_counts = counts[category]
    # Create a bar chart using the category counts
    ax = category_counts.plot(kind='bar', title=f'Category {categories[category]}')
    # Set the axis labels and legend
    ax.set_xlabel('Category')
    ax.set_ylabel('Count')
    ax.legend()
    # Show the plot
    plt.show()