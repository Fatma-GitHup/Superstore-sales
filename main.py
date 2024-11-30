#import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
superstore = pd.read_csv("Superstore Sales Dataset.csv")


#Data Exploration
print(superstore.shape)
print(superstore.head())

superstore.describe()
superstore.info()

# Data cleaning

(superstore.isnull())
(superstore.isnull().sum())
#Only postal code has 11 missing values

#Remove duplicate
superstore.duplicated().sum()
superstore.drop_duplicates(inplace=True)

#Dropping the Row ID column
superstore.drop('Row ID',axis = 1, inplace = True)

#replace null vaalues with postal code of Burlington
superstore[superstore["Postal Code"].isnull()]
superstore["Postal Code"]= superstore["Postal Code"].fillna(05401.0)

superstore.isnull().sum()

#Change order date data type into date type
superstore['Order Date'] = pd.to_datetime(superstore['Order Date'], format='%d/%m/%Y') # Added format argument to specify day/month/year format
superstore['day'] = superstore['Order Date'].dt.day
superstore['month'] = superstore['Order Date'].dt.month
superstore['year'] = superstore['Order Date'].dt.year

#Change order date data type into date type
superstore['Ship Date'] = pd.to_datetime(superstore['Ship Date'], format='%d/%m/%Y')
superstore['day_ship'] = superstore['Ship Date'].dt.day
superstore['month_ship'] = superstore['Ship Date'].dt.month
superstore['year_ship'] = superstore['Ship Date'].dt.year
nan_superstore = superstore[superstore.isna().any(axis=1)]
superstore["Ship Mode"].value_counts().plot(kind="bar")
superstore["Segment"].value_counts().plot(kind="pie",autopct="%1.1f%%")
plt.show

#sorting data by order date
superstore.sort_values(by=['Order Date'], inplace=True, ascending=True)
superstore.set_index("Order Date", inplace = True)

# Top 10 states with highest sales
top_10_states = superstore.nlargest(10, 'Sales')

# Create bar chart
plt.figure(figsize=(10, 6))
plt.bar(top_10_states['State'], top_10_states['Sales'])
plt.xlabel('State')
plt.ylabel('Sales')
plt.title('Top 10 States with Highest Sales')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.tight_layout()
plt.show()

# Group the data by customer segment and calculate the total profit
profit_by_segment = superstore.groupby("Segment")["Sales"].sum()

# Find the most profitable customer segment
most_profitable_segment = profit_by_segment.idxmax()
most_profitable_profit = profit_by_segment.max()

# Print the result
print("Most profitable customer segment:", most_profitable_segment)
print("Total profit:", most_profitable_profit)

# Create a bar chart to visualize the profit by customer segment
plt.figure(figsize=(10, 6))
plt.bar(profit_by_segment.index, profit_by_segment.values)
plt.xlabel("Customer Segment")
plt.ylabel("Total Profit")
plt.title("Profit by Customer Segment")
plt.show()

shipping_mode_counts = superstore["Ship Mode"].value_counts()

# Find the most preferred shipping mode
most_preferred_mode = shipping_mode_counts.idxmax()

# Print the result
print("Most preferred shipping mode:", most_preferred_mode)

# Create a bar chart to visualize the shipping mode counts
plt.figure(figsize=(10, 6))
plt.bar(shipping_mode_counts.index, shipping_mode_counts.values)
plt.xlabel("Shipping Mode")
plt.ylabel("Count")
plt.title("Shipping Mode Preferences")
plt.show()

sales_by_category = superstore.groupby("Category")["Sales"].sum()
best_category = sales_by_category.idxmax()

print("Best-selling product category:", best_category)

plt.figure(figsize=(6, 4))
plt.pie(sales_by_category, labels=sales_by_category.index, autopct="%1.1f%%")
plt.title("Product Category Sales Distribution")
plt.show()

#Which customer segment is bringing in the highest sales?
sales_by_segment = superstore.groupby("Segment")["Sales"].sum()
best_segment = sales_by_segment.idxmax()

print("Best-performing customer segment:", best_segment)

plt.figure(figsize=(6, 4))
plt.pie(sales_by_segment, labels=sales_by_segment.index, autopct="%1.1f%%")
plt.title("Sales by Customer Segment")
plt.show()

# 4. What is the most preferred shipping mode among customers?
shipping_mode_counts = superstore["Ship Mode"].value_counts()
most_preferred_mode = shipping_mode_counts.idxmax()

print("Most preferred shipping mode:", most_preferred_mode)

plt.figure(figsize=(8, 4))
plt.bar(shipping_mode_counts.index, shipping_mode_counts.values)
plt.xlabel("Shipping Mode")
plt.ylabel("Count")
plt.title("Shipping Mode Preferences")
plt.show()

# 5. How has the company’s performance trended over recent years and months?
superstore["Order Date"] = pd.to_datetime(superstore["Order Date"])
yearly_sales = superstore.resample("Y", on="Order Date")["Sales"].sum()
monthly_sales = superstore.resample("M", on="Order Date")["Sales"].sum()

plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(yearly_sales.index.year, yearly_sales)
plt.xlabel("Year")
plt.ylabel("Total Sales")
plt.title("Yearly Sales Trend")

plt.subplot(1, 2, 2)
plt.plot(monthly_sales.index, monthly_sales)
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.title("Monthly Sales Trend")

plt.tight_layout()
plt.show()

# Find the best-selling product category
sales_by_category = superstore.groupby("Category")["Sales"].sum()
best_category = sales_by_category.idxmax()

print("Best-selling product category:", best_category)

plt.figure(figsize=(6, 4))
plt.pie(sales_by_category, labels=sales_by_category.index, autopct="%1.1f%%")
plt.title("Product Category Sales Distribution")
plt.show()


# Group subcategory by sales, profit, and quantity
subcat_analysis = (
    superstore.groupby("Sub-Category")[["Sales"]].sum()
)

# Create a figure with a 1x3 grid of axes (adjustable based on preference)
figure, axis = plt.subplots(1, 3, figsize=(15, 5))  # Adjust figsize as needed

# Plot bar chart for best-selling sub-categories
subcat1 = sns.barplot(
    data=subcat_analysis,
    x=subcat_analysis.index,
    y=subcat_analysis["Sales"],
    ax=axis[0],
)
subcat1.set(title="Best-Selling Sub-Categories")
subcat1.set_xticklabels(subcat1.get_xticklabels(), rotation="vertical", size=10)

# Plot bar chart for most profitable sub-categories
subcat2 = sns.barplot(
    data=subcat_analysis, x=subcat_analysis.index, y=subcat_analysis["Sales"], ax=axis[1]
)
subcat2.set(title="Most Profitable Sub-Categories")
subcat2.set_xticklabels(subcat2.get_xticklabels(), rotation="vertical", size=10)

# Plot bar chart for most ordered sub-categories
subcat3 = sns.barplot(
    data=subcat_analysis, x=subcat_analysis.index, y=subcat_analysis["Sales"], ax=axis[2]
)
subcat3.set(title="Most Ordered Sub-Categories")
subcat3.set_xticklabels(subcat3.get_xticklabels(), rotation="vertical", size=10)

# Adjust spacing between subplots for better readability
plt.tight_layout()

# Display the plot
plt.show()

main_category = "Office Supplies"

# Filter data for the chosen category
filtered_data = superstore[superstore["Category"] == main_category]

# Group by subcategory and calculate total sales
subcategory_sales = filtered_data.groupby("Sub-Category")["Sales"].sum()

# Plot top-selling subcategories (adjust number of subcategories)
plt.figure(figsize=(10, 6))
top_subcategories = subcategory_sales.nlargest(5)  # Choose number of subcategories
plt.bar(top_subcategories.index, top_subcategories.values)
plt.xlabel("Sub-Category")
plt.ylabel("Total Sales")
plt.title(f"Top-Selling Subcategories in {main_category}")
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.tight_layout()
plt.show()
#

# Choose a specific year
year_to_analyze = 2015

# Filter data for the chosen year
filtered_data = superstore[superstore['Order Date'].dt.year == year_to_analyze]

# Group by subcategory and month, then calculate sales
subcategory_sales_by_month = (
    filtered_data.groupby(["Sub-Category", filtered_data['Order Date'].dt.month])["Sales"].sum()
)

# Unstack the DataFrame to have months as columns
subcategory_sales_by_month = subcategory_sales_by_month.unstack()

# Plot line chart for each subcategory
plt.figure(figsize=(12, 6))
for subcategory in subcategory_sales_by_month.columns:
    plt.plot(subcategory_sales_by_month.index, subcategory_sales_by_month[subcategory], label=subcategory)

plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.title(f"Monthly Sales for Subcategories in {year_to_analyze}")
plt.legend()
plt.show()

# Extract year from 'Order Date'
superstore['Year'] = superstore['Order Date'].dt.year

# Group by year and category, then sum sales
total_sales_by_category_per_year = superstore.groupby(['Year', 'Category'])['Sales'].sum().unstack()

# Plot total sales with main categories per year
total_sales_by_category_per_year.plot(kind='line', stacked=False)
plt.xlabel('Year')
plt.ylabel('Total Sales')
plt.title('Total Sales by Category per Year')
plt.legend(title='Category', loc='upper left', bbox_to_anchor=(1.05, 1))  # Adjust legend position
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.tight_layout()
plt.show()
#
