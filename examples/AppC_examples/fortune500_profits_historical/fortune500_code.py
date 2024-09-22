# Jupyter Notebook example from 
# https://www.dataquest.io/blog/jupyter-notebook-tutorial/

# some setup
pd.options.mode.chained_assignment = None
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

# How did GM do?
df.loc[df['company'] == 'General Motors'].head()
df.loc[df['company'] == 'General Motors', 'profit'].head()
df.loc[df['company'] == 'General Motors', 'profit'].sum()
# Oops. Why is sum so strange? Check the datatypes of the columns
df.dtypes
# Ah. There's a problem with the profit column

# Find non-numeric profit values
non_numeric_profits = df.profit.str.contains('[^0-9.-]')
# non_number_profits is an array of boolean of the same length as df.profit: [False, False, ..., True, False...]
df.loc[non_numeric_profits].head()
# df.loc with a boolean array returns only element indexes with True

# How many different non-numberic profits?
set(df.profit[non_numeric_profits])
# Only one non-numeric profit value "N.A."

# What should we do? Depends on how many occurrences
len(df.profit[non_numeric_profits])
# Not too many. If they're evenly distributed, we can just remove them.

# Find distributions of records with non-numeric profit values
bin_sizes, _, _ = plt.hist(df.year[non_numeric_profits], bins=range(1955, 2006))
# Number of invalid values in a single year is fewer than 25 (less than 5%)

# Let’s say this is acceptable and go ahead and remove these rows.
# First, df.loc is used for label-based indexing. We'll use it to 
# select only the rows where the profit column contains numeric values. 
df = df.loc[~non_numeric_profits]
# The profit values are still strings, so convert them to numbers.
df['profit'] = pd.to_numeric(df['profit'])
len(df)

df.dtypes
# Better

df.loc[df['company'] == 'General Motors', 'profit'].sum()
df.loc[df['company'] == 'General Motors', 'profit'].mean()
# Looks good. 

# Time for some visualizations.
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

# What about revenues? (IMPORTANT: Execute the next block of statements in the same cell)
y2 = avgs.revenue
fig, ax = plt.subplots()
plot(x, y2, ax, 'Increase in mean Fortune 500 company revenues from 1955 to 2005', 'Revenue (millions)')
# Revenues weren't hit as badly in the downturns, and still an enormous increase

# Is that the whole picture? Let's superimpose plots with their standard deviations
def plot_with_std(x, y, stds, ax, title, y_label):
    ax.fill_between(x, y - stds, y + stds, alpha=0.2)
    plot(x, y, ax, title, y_label)

# IMPORTANT: Execute the next block of statements in the same cell
fig, (ax1, ax2) = plt.subplots(ncols=2)
title = 'Increase in mean and std Fortune 500 company %s from 1955 to 2005'
stds1 = group_by_year.std().profit.values
stds2 = group_by_year.std().revenue.values
plot_with_std(x, y1.values, stds1, ax1, title % 'profits', 'Profit (millions)')
plot_with_std(x, y2.values, stds2, ax2, title % 'revenues', 'Revenue (millions)')
fig.set_size_inches(14, 4)
fig.tight_layout()

# Wow. Some companies made billions, others lost billions.
