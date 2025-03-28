# Alien Film Franchise Financial Data Analysis

This notebook provides a complete workflow to analyze financial data for the Alien film franchise. It:
- Loads CSV files containing film budgets and box office revenues for the Alien film franchise.
- Adjusts monetary values for inflation using historical Consumer Price Index (CPI) data.
- Saves the updated data to new CSV files.
- Creates visualizations (line and bar charts) comparing original vs. adjusted values.

Below you'll find the code divided into logical sections.

## 1. Configuration

We begin by importing necessary libraries and setting up our CPI data. The CPI data is stored as a dictionary with historical values.


```python
import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# CPI_DATA stores historical CPI values for specific years.
CPI_DATA = {
    "1979": 72.6, "1986": 109.6, "1992": 140.3, "1997": 160.5,
    "2004": 188.9, "2007": 207.3, "2012": 229.6, "2017": 245.1,
    "2024": 315.6, "2025": 319.1
}
CPI_2025 = CPI_DATA["2025"]

```

## 2. Helper Functions

This section defines functions for:
- Loading and saving CSV files.
- Adjusting amounts for inflation.
- Preparing and plotting charts.


```python
def load_csv(filepath):
    """
    Load CSV data from a file into a list of dictionaries.
    """
    with open(filepath, mode='r', newline='', encoding='utf-8') as file:
        return list(csv.DictReader(file))

def save_csv(filepath, data, fieldnames):
    """
    Save a list of dictionaries to a CSV file.
    """
    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def adjust_for_inflation(amount, year):
    """
    Adjust an amount from a given year to 2025 dollars using CPI data.
    """
    return round(amount * (CPI_2025 / CPI_DATA[year]))

def prepare_plot(ax, title, xlabel, ylabel):
    """
    Prepare the plot with a consistent style.
    """
    fig = ax.get_figure()
    fig.patch.set_facecolor('#2b2b2b')
    ax.set_facecolor('#2b2b2b')
    ax.set_title(title, fontsize=16, color='white')
    ax.set_xlabel(xlabel, fontsize=14, color='white')
    ax.set_ylabel(ylabel, fontsize=14, color='white')
    ax.tick_params(colors='white')
    # Format y-axis ticks to display as currency.
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'${int(x):,}'))
    plt.grid(axis='y', linestyle='--', alpha=0.4, color='gray')

def plot_bar_comparison(titles, values1, values2, labels, colors, title, filename):
    """
    Plot a bar chart comparing two sets of values.
    """
    x = np.arange(len(titles))
    bar_width = 0.4
    fig, ax = plt.subplots(figsize=(12, 6))
    prepare_plot(ax, title, 'Film Title', 'USD')
    
    # Plot two sets of bars side by side.
    ax.bar(x - bar_width/2, values1, width=bar_width, label=labels[0], color=colors[0], alpha=0.9)
    ax.bar(x + bar_width/2, values2, width=bar_width, label=labels[1], color=colors[1], alpha=0.9)
    
    plt.xticks(x, titles, rotation=30, ha='right', fontsize=10, color='white')
    leg = plt.legend(fontsize=10, facecolor='#2b2b2b', edgecolor='white', loc='center left', bbox_to_anchor=(1.05, 0.5))
    for text in leg.get_texts():
        text.set_color('white')
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()

def plot_line_chart(titles, values, title, filename):
    """
    Plot a line chart of the provided values.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    prepare_plot(ax, title, 'Film Title', 'USD')
    ax.plot(titles, values, marker='o', color='#00FF90', linestyle='-')
    plt.xticks(rotation=45, ha='right', fontsize=10, color='white')
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()

```

## 3. Budget Adjustment

This section:
- Loads film budget CSV data.
- Adjusts the budget values using a multiplier.
- Saves the updated CSV data.
- Plots a line chart of the adjusted budgets.

*Note: Update the file paths as needed.*


```python
def adjust_budgets():
    """
    Adjust film budgets using CSV data and save the adjusted data.
    """
    # Load budget data from CSV.
    budget_data = load_csv('filepathalienfranchise.csv')
    adjusted_budgets = []
    
    # Process each row: clean the budget, adjust it, and store the adjusted value.
    for row in budget_data:
        budget = row['Estimated Budget (in USD)'].replace(",", "")
        if budget.isdigit():
            original = int(budget)
            # Example multiplier for adjustment.
            adjusted = round(original * 1.02598)
            row['Estimated Budget (in USD)'] = f"{original:,}"
            row['Adjusted Budget (2025 USD)'] = adjusted
            adjusted_budgets.append((row['Film Title'], adjusted))
        else:
            row['Adjusted Budget (2025 USD)'] = "Unknown"
    
    # Save the updated budget data to a new CSV file.
    save_csv('filepathalien_franchise_adjusted.csv', budget_data, budget_data[0].keys())
    
    # Plot the adjusted budgets using a line chart.
    plot_line_chart(
        titles=[t for t, _ in adjusted_budgets],
        values=[v for _, v in adjusted_budgets],
        title="Alien Franchise Budgets (Adjusted to 2025 USD)",
        filename="alien_franchise_budget_plot.png"
    )

# Run budget adjustment
adjust_budgets()

```

## 4. Box Office Adjustment

This section:
- Loads box office CSV data.
- Adjusts box office revenue for inflation.
- Saves the updated CSV data.
- Plots a bar chart comparing the original and adjusted revenues.


```python
def adjust_box_office():
    """
    Adjust box office revenues for inflation using CSV data and save the adjusted data.
    """
    # Load box office data from CSV.
    box_office_data = load_csv('filepathAlienBoxOffice.csv')
    adjusted_revenues = []
    
    # Process each row: adjust the box office revenue for inflation.
    for row in box_office_data:
        year = row['Year']
        revenue = int(row['Box Office Revenue (USD)'].replace(",", "").replace("~", ""))
        adjusted = adjust_for_inflation(revenue, year)
        row['Adjusted Box Office Revenue (2025 USD)'] = adjusted
        adjusted_revenues.append((row['Film Title'], adjusted))
    
    # Save the adjusted box office data to a new CSV file.
    save_csv('filepathAlienBoxOfficeCPIAdjusted.csv', box_office_data, box_office_data[0].keys())
    
    # Plot a bar chart to compare original vs. adjusted box office revenue.
    plot_bar_comparison(
        titles=[r['Film Title'] for r in box_office_data],
        values1=[int(r['Box Office Revenue (USD)'].replace(",", "").replace("~", "")) for r in box_office_data],
        values2=[int(r['Adjusted Box Office Revenue (2025 USD)']) for r in box_office_data],
        labels=["Original Revenue", "Adjusted Revenue (2025)"],
        colors=["#FF3B3B", "#D9D1C7"],
        title="Alien Franchise Box Office Revenue: Original vs. Adjusted",
        filename="alien_franchise_box_office_comparison.png"
    )

# Run box office adjustment
adjust_box_office()

```    

## 5. Budget & Profit Comparison

This section processes production budgets and estimated profits (both original and inflation-adjusted) and creates side-by-side bar charts for comparison.



```python
def process_budget_profit_plot(data, adjust=False, filename='', title=''):
    """
    Processes budget and profit data from the provided CSV data and creates a bar comparison plot.
    If adjust is True, adjusts the values for inflation.
    """
    titles = [r['Film Title'] for r in data]
    budgets = []
    profits = []
    
    for r in data:
        year = r['Year']
        budget = int(r['Production Budget (USD)'].replace(",", ""))
        profit = int(r['Estimated Profit (USD)'].replace(",", "").replace("~", ""))
        if adjust:
            budget = adjust_for_inflation(budget, year)
            profit = adjust_for_inflation(profit, year)
        budgets.append(budget)
        profits.append(profit)
    
    plot_bar_comparison(
        titles=titles,
        values1=budgets,
        values2=profits,
        labels=["Adjusted Budget (2025 USD)" if adjust else "Original Budget",
                "Adjusted Profit (2025 USD)" if adjust else "Original Profit"],
        colors=["#6AFF6A" if adjust else "#2A7670", "#5B7C99" if adjust else "#F4B860"],
        title=title,
        filename=filename
    )

def compare_budget_profit():
    """
    Generate plots for original and adjusted budgets and profits using box office data.
    """
    # Load box office data (also used for budget/profit data).
    box_office_data = load_csv('filepathAlienBoxOffice.csv')
    
    # Plot original budgets and profits.
    process_budget_profit_plot(
        data=box_office_data,
        adjust=False,
        filename="alien_franchise_budget_profit_plot.png",
        title="Alien Franchise Budgets and Profits"
    )
    
    # Plot inflation-adjusted budgets and profits.
    process_budget_profit_plot(
        data=box_office_data,
        adjust=True,
        filename="alien_franchise_adjusted_budget_profit_plot.png",
        title="Alien Franchise: Adjusted Budgets and Profits (2025 USD)"
    )

# Run budget & profit comparison
compare_budget_profit()

```

```python
## 6. Conclusion

This notebook provided a complete workflow for analyzing film franchise financial data:
- Loading and saving CSV data.
- Adjusting monetary values for inflation.
- Visualizing comparisons using line and bar charts.

Feel free to modify file paths, adjustment multipliers, or visual settings as needed.
```

### Sources of Film Data

- **Box Office Revenues & Production Budgets:**
  - **Box Office Mojo**  
    [https://www.boxofficemojo.com/](https://www.boxofficemojo.com/)  
    *(Provides detailed domestic and worldwide box office figures and production budgets.)*
  - **The Numbers**  
    [https://www.the-numbers.com/](https://www.the-numbers.com/)  
    *(Offers extensive film financial data, including budgets, revenues, and profit estimates.)*
  - **Wikipedia**  
    *(Often cited for historical context and aggregated data on film productions.)*  
    Examples:  
    - [Alien (1979) - Wikipedia](https://en.wikipedia.org/wiki/Alien_(film))  
    - [Aliens (1986) - Wikipedia](https://en.wikipedia.org/wiki/Aliens)

- **Calculated Profits:**
  - **Profit Estimations:**  
    Calculated as:  
    `Estimated Profit = Box Office Revenue – Production Budget`  
    *(Uses the budget/revenue figures sourced from the above sites.)*

### Sources of CPI Data for Inflation Adjustment

- **U.S. Bureau of Labor Statistics (BLS) – CPI Data:**  
  [https://www.bls.gov/cpi/](https://www.bls.gov/cpi/)  
  *(Provides official Consumer Price Index values for different years.)*

- **Historical CPI/Inflation Calculators:**  
  - **US Inflation Calculator**  
    [https://www.usinflationcalculator.com/](https://www.usinflationcalculator.com/)  
    *(Helps in verifying or calculating specific inflation multipliers based on historical CPI values.)*

### Additional Film Review Sources (for context)

- **Rotten Tomatoes:**  
  [https://www.rottentomatoes.com/](https://www.rottentomatoes.com/)  
  *(Used to source approval ratings and audience scores.)*

- **Metacritic:**  
  [https://www.metacritic.com/](https://www.metacritic.com/)  
  *(Provides normalized critic scores.)*

---

These links cover the main data points used in the examples:
- **Box Office/Revenues, Budgets, and Profits:** Sourced mainly via Box Office Mojo, The Numbers, and Wikipedia.
- **Inflation CPI data:** Obtained from the U.S. Bureau of Labor Statistics and verified with online inflation calculators.

Please reference these sources to gather up-to-date figures or verify the historical data used in the code examples.


```python

```
