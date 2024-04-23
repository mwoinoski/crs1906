# Jupyter Notebook example from 
# https://www.dataquest.io/blog/jupyter-notebook-tutorial/

# some setup
%matplotlib inline
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="darkgrid")

# read the dataset
df = pd.read_csv('fortune500.csv')

df.head()

# Let’s rename those columns so we can refer to them later
df.columns = ['year', 'rank', 'company', 'revenue', 'profit']

# Is our dataset complete?
len(df)
# Yes, looks good

# Check the datatypes of the columns
df.dtypes
# Oops. problem with the profit column

# Find non-numeric profit values
non_numeric_profits = df.profit.str.contains('[^0-9.-]')
df.loc[non_numeric_profits].head()

# How many different non-numberic profits?
set(df.profit[non_numeric_profits])
# Only one non-numeric profit

# What should we do? Depends on how many occurrences
len(df.profit[non_numeric_profits])
# Not too many. If they're evenly distributed, we can just remove them.

# Find distributions of records with non-numeric profit values
bin_sizes, _, _ = plt.hist(df.year[non_numeric_profits], bins=range(1955, 2006))
# Number of invalid values in a single year is fewer than 25 (less than 5%)

# Let’s say this is acceptable and go ahead and remove these rows.
df = df.loc[~non_numeric_profits]
df.profit = df.profit.apply(pd.to_numeric)
len(df)

df.dtypes
# Better

# Plot the average profit by year
group_by_year = df.loc[:, ['year', 'revenue', 'profit']].groupby('year')
avgs = group_by_year.mean()
x = avgs.index
y1 = avgs.profit

def plot(x, y, ax, title, y_label):
    ax.set_title(title)
    ax.set_ylabel(y_label)
    ax.plot(x, y)
    ax.margins(x=0, y=0)

fig, ax = plt.subplots()
plot(x, y1, ax, 'Increase in mean Fortune 500 company profits from 1955 to 2005', 'Profit (millions)')
# The increase in profits looks exponential, except for early 1990's recession 
# and 2000's dot-com bubble.

# What about revenues? 
y2 = avgs.revenue
fig, ax = plt.subplots()
plot(x, y2, ax, 'Increase in mean Fortune 500 company revenues from 1955 to 2005', 'Revenue (millions)')
# Revenues weren't hit as badly in the downturns, and still an enormous increase

# Is that the whole picture? Let's superimpose plots with their standard deviations
def plot_with_std(x, y, stds, ax, title, y_label):
    ax.fill_between(x, y - stds, y + stds, alpha=0.2)
    plot(x, y, ax, title, y_label)

fig, (ax1, ax2) = plt.subplots(ncols=2)
title = 'Increase in mean and std Fortune 500 company %s from 1955 to 2005'
stds1 = group_by_year.std().profit.values
stds2 = group_by_year.std().revenue.values
plot_with_std(x, y1.values, stds1, ax1, title % 'profits', 'Profit (millions)')
plot_with_std(x, y2.values, stds2, ax2, title % 'revenues', 'Revenue (millions)')
fig.set_size_inches(14, 4)
fig.tight_layout()

# Wow. Some companies made billions, others lost billions.


