```
You are an expert financial analyst and an Actuary expert. You are familiar with all the
financial and actuary equations and python packages and you know how to write python function
as you are also a highly skilled python developer.

In the .xlsx file "csv_and_xlsx/financial_equations_python_packages_lookup_table.xlsx" in the sheet name "Master_Lookup"
you will find 815 rows of financial/actuary/technical-analysis equations related
to various domains and subdomains in the financial world.
The relevant columns to pat attention to are:
1. equation name
2. math form of the equation
3. python package
4. domain
5. subdomain
```



## Tasks
use only these instructions and nothing else. Not any .py file or .md file found in this folder "instltns"
1. 
```
Create a .py file where you translate each of these equations (each row) to a python function. The objective is that these 
functions will serve as a graph where the name of the function serves as an edge (the y-output parameter) and the parameters serve as
nodes (the X-input parameters). Such that each parameter can be a node (another function). 
For example, if one equation is A=B+C, and another is B=D+E, then B serves as an edge for A and is also a node. 
Accordingly, you must keep the same name for an edge and a node if you identify (and you must do a deep research, 
even going on the web if needed) if it is the same financial entity. Pay attention that some parameters might have the same symbol
but they have the different financial meaning. The meaning must be found accurately to not make mistakes between edges and nodes.
```
2. 
```
For each function create a description of the domain in the function  - simply copy the list from the .xlsx file column domain.
Name it "domain"
```
3. 
```
For each function create a description of the subdomain in the function  - simply copy the list from the .xlsx file column subdomain
Name it "subdomain"
```
4. 
```
For each function create a description of the function - a financial/statistial/etc. description of the function. Notice that this exact description must appear in the parameter description if it is also an edge of another function- an X parameter of another function (another financial parameter))
Name it "function"
In the :return desacriptions of the function output, give a textual description of the function used 
```
5. 
```
For each parameter (a function's argument passed through the function) create a description of the parameter - a financial/statistial/etc. description of the parameter. Notice that this exact description must appear in the function description if it is also a node (an other function)
insert in the :param desacriptions of the function arguments
```
6. 
```
For each function create a description of all the functions in the python file that for which the function name serves as an argument (input X parameter) - this description will be served to create the graph - this would be a list with all the function names for which the function serves as an argument
You will be tested for high accuracy for this list. So pay extra attention. This needs to be created according to the two previous tasks (4 and 5 - the description of the y parameter and the description of the X parameters - function arguments)
Name it "y_as_x"
```
7. 
```
Create the algorithm for each function. Notice that it is preferable to use the python package function over a manual scripting of that function. 
Notice that you need to understand which one is the correct one if not given specifically in the column python package in the .xlsx file of the specific row).
```
8. 
```
name the .py file 'financial_functions_1.py' and save it in the folder 'instltns'
```

## Notes
1.
```
Notice that some of the equations are written as math equations or not complete math equations (for example D&A means Depreciation and Amortization), or with math operators like 
sub_i (which means summing over i) that are not parameters. You need to do a deep research on the web to rederive those equations to understand exactly what is a math operator
and what is an input parameter, and understand exactly what is each parameter so that you will not mistake them for others with the same symbol but with different meaning (
for example the symbol rho could mean density in some equations and could also mean correlation coefficient in some other equations).
```
2. 
```
Notice that it is preferable to use the python package function over a manual scripting of that function. 
Do a deep research, using the web if needed, so that you could understand which exact equation is the correct one if not given specifically in the column python package in the .xlsx file of the specific row).
```

3. 
```
do not return the exact examples given in here [## Examples], these examples are lacking deep research and all functions in y_as_x. Do it better and include all functions required in y_as_x
```

## Examples
1.
```
    def ebit(revenue, operating_expenses):
        '''
        domain: ['Financial Accounting & Corporate Finance']
        subdomain: ['Financial Statement Analysis']
        function: "EBIT - Earnings Before Interest and Taxes, is a financial metric measuring a company's profitability from core operations. It shows profit available to pay lenders, taxes, and shareholders, allowing investors to compare companies without capital structure impacts."
        y_as_x: ['ebitda', 'interest_coverage', 'ev_over_ebitda', ... (there are others to find, not only this sublist as an example, you should return them all according to the Note in [## Notes])]
        :param revenue: "Revenue is the total amount of income a business generates from the sale of goods or services, or any other use of capital or assets, before deducting expenses. Often called "top-line" growth, it represents the foundational inflow of cash or accounts receivable, indicating market demand and sales effectiveness, but it is not profit."
        :param operating_expenses: "Operating Expenses (OpEx) are the essential, ongoing costs a business incurs to maintain daily operations and generate revenue, excluding direct production costs (COGS) and financial interest. Common examples include rent, salaries, marketing, and utilities. These are recorded on the income statement and impact profitability."
        :return: "Computed value of EBIT = Revenue - Operating Expenses"
        '''
        return revenue - operating_expenses
        
    def ebitda(ebit, depreciation, amortization):
        '''
        domain: ['Financial Accounting & Corporate Finance']
        subdomain: ['Financial Statement Analysis']
        function: "EBITDA - Earnings Before Interest, Taxes, Depreciation, and Amortization, is a financial metric used to evaluate a company's core operating profitability by excluding non-operating expenses (interest, taxes) and non-cash accounting items (depreciation, amortization). It acts as a proxy for operating cash flow, showing how much cash a business generates from daily operations before capital investments and debt financing."
        y_as_x: ['cash_interest_coverage', 'ebitda_margin', ... (there are others to find, not only this sublist as an example, you should return them all according to the Note in [## Notes])]
        :param ebit: "EBIT - Earnings Before Interest and Taxes, is a financial metric measuring a company's profitability from core operations. It shows profit available to pay lenders, taxes, and shareholders, allowing investors to compare companies without capital structure impacts."
        :param depreciation: "Depreciation - is an accounting method that spreads the cost of a tangible asset—such as machinery, vehicles, or buildings—over its useful life, reflecting its decline in value due to wear, tear, or obsolescence. It is a non-cash expense that aligns asset costs with the revenue they generate over time."
        :param amortization: "Amortization is the process of spreading out a loan (debt) or the cost of an intangible asset over a specific period. For loans, it means paying down principal and interest via regular installments. For assets, it involves gradually writing off the cost of intangible items (patents, copyrights, software) over their useful life to align costs with revenue generation."
        :return: "Computed value of EBITDA = EBIT + Depreciation + Amortization"
        '''
        return ebit + depreciation + amortization
```
2.
```
    def drawdown(returns:[list,pd.Series, np.ndarray])->[list,pd.Series, np.ndarray]:
        '''
        domain: ['Risk Management & Actuarial Science']
        subdomain: ['Market Risk', 'Volatility Modeling', 'Downside & Tail Risk']
        function: "Drawdown — a drawdown is the peak-to-trough decline of an investment or trading account value, measuring the percentage loss from its highest point to its lowest point before a new peak is reached. It is a critical, often superior, risk metric compared to volatility, representing the worst-case scenario during a specific period."
        y_as_x: ['maximum_drawdown', ... (there are others to find, not only this sublist as an example, you should return them all according to the Note in [## Notes])]
        :param returns: "Returns are the gain or loss generated on an investment over a specific period, calculated as a percentage of the initial cost. They encompass income (dividends/interest) and capital appreciation (price changes). Returns measure performance, enabling investors to compare opportunities and balance risk against potential rewards."
        :return: "Computed DD list"
        '''
        import pandas as pd
        import numpy as np
        # 1. Sample Daily Returns (list, np.array, or a pd.series) - percentage values
        # 2. Compute Wealth Index
        wealth_index = (1 + returns).cumprod()
        # 3. Compute the Running Peak (High Water Mark)
        previous_peaks = wealth_index.cummax()
        # 4. Compute Drawdown as a percentage
        drawdown = (previous_peaks - wealth_index) / previous_peaks
        return drawdown
        
    def maximum_drawdown(drawdown:[list,pd.Series, np.ndarray]):
        '''
        domain: ["Asset Management & Market Microstructure", "Risk Management & Actuarial Science"]
        subdomain: ["Performance Attribution", "Risk-Adjusted Performance", "Downside & Tail Risk"]
        function: "Maximum Drawdown - is the maximum observed loss from a peak to a trough of a portfolio, before a new peak is attained, expressed as a percentage. It measures the largest "pain" or capital reduction an investor could have experienced, acting as a crucial indicator of downside risk and capital preservation."
        y_as_x: ['calmar_ratio', ... (there are others to find, not only this sublist as an example, you should return them all according to the Note in [## Notes])]
        :param drawdown: "Drawdown — a drawdown is the peak-to-trough decline of an investment or trading account value, measuring the percentage loss from its highest point to its lowest point before a new peak is reached. It is a critical, often superior, risk metric compared to volatility, representing the worst-case scenario during a specific period."
        :return: "Computed MDD = max_t[(peak_t-V_t)/peak_t]"
        '''
        return drawdown.max()
```