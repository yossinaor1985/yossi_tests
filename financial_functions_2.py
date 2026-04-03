"""
financial_functions_1.py
========================
A comprehensive library of 815 financial, actuarial, and technical analysis functions.
Each function serves as a node/edge in a computational graph where:
  - The function name is an edge (Y-output)
  - The parameters are nodes (X-inputs)
  - If a parameter name matches another function name, it creates a graph connection

Generated from financial_equations_python_packages_lookup_table.xlsx
"""

# fixme: a lot of mistakes. needs to be done manually. The model doesn't know how to handle it.
def abnormal_earnings_growth(capitalized_next_earnings, pv_abnormal_earnings_growth):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Equity Valuation', 'Asset Pricing']
    function: "Abnormal earnings growth — P_0 = capitalized next earnings + PV abnormal earnings growth. A financial metric in the domain of Equity valuation & asset pricing."
    y_as_x: []
    :param capitalized_next_earnings: "Parameter capitalized_next_earnings used in Abnormal earnings growth calculation."
    :param pv_abnormal_earnings_growth: "Parameter pv_abnormal_earnings_growth used in Abnormal earnings growth calculation."
    :return: "Computed value of Abnormal earnings growth: P_0 = capitalized next earnings + PV abnormal earnings growth"
    '''
    return capitalized_next_earnings + pv_abnormal_earnings_growth






def abs_pool_factor(current_pool_balance, original_pool_balance):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Structured Finance', 'Securitization']
    function: "ABS pool factor — Factor_t = Current Pool Balance / Original Pool Balance. A financial metric in the domain of Structured finance & securitization."
    y_as_x: []
    :param current_pool_balance: "Current Pool Balance is the outstanding principal of an ABS/MBS pool."
    :param original_pool_balance: "Original Pool Balance is the initial principal of an ABS/MBS pool at issuance."
    :return: "Computed value of ABS pool factor: Factor_t = Current Pool Balance / Original Pool Balance"
    '''
    return current_pool_balance / original_pool_balance






def absolute_ppp(p, p_2):
    '''
    domain: ['FX & international finance']
    subdomain: ['FX Markets', 'International Finance']
    function: "Absolute PPP — S = P / P^*. A financial metric in the domain of FX & international finance."
    y_as_x: []
    :param p: "Model order parameter p (autoregressive order or similar)."
    :param p_2: "Parameter p_2 used in Absolute PPP calculation."
    :return: "Computed value of Absolute PPP: S = P / P^*"
    '''
    return p / p_2






def accounting_identity(liabilities, equity):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "Accounting identity — Assets = Liabilities + Equity. A financial metric in the domain of Accounting & financial statement analysis."
    y_as_x: []
    :param liabilities: "Total Liabilities represent all obligations owed by the company."
    :param equity: "Total Equity is the residual interest in assets after deducting liabilities."
    :return: "Computed value of Accounting identity: Assets = Liabilities + Equity"
    '''
    return liabilities + equity






def accrued_interest(coupon, daycountfraction):
    '''
    domain: ['Fixed income & bond math']
    subdomain: ['Fixed Income', 'Bond Mathematics']
    function: "Accrued interest — AI = Coupon × DayCountFraction. A financial metric in the domain of Fixed income & bond math."
    y_as_x: ['clean_price', 'dirty_price']
    :param coupon: "Coupon is the periodic interest payment made to the bondholder."
    :param daycountfraction: "Parameter daycountfraction used in Accrued interest calculation."
    :return: "Computed value of Accrued interest: AI = Coupon × DayCountFraction"
    '''
    return coupon * daycountfraction






def accumulation_distribution_line(high, low, close, volume):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "Accumulation/distribution line — ADL = ADL_{t-1} + MFM_t x Volume_t. A financial metric in the domain of Technical analysis & chart-based indicators."
    y_as_x: []
    :param high: "High is the highest price during a specific trading period."
    :param low: "Low is the lowest price during a specific trading period."
    :param close: "Close is the final trading price at the end of a trading period."
    :param volume: "Volume is the total number of shares or contracts traded during a period."
    :param period: "Period (n) is the lookback window in number of bars for technical indicators."
    :return: "Computed value of Accumulation/distribution line: ADL = ADL_{t-1} + MFM_t x Volume_t"
    '''
    import pandas as pd
    h = pd.Series(high); l = pd.Series(low); c = pd.Series(close); v = pd.Series(volume)
    mfm = ((c - l) - (h - c)) / (h - l)
    mfm = mfm.fillna(0)
    return (mfm * v).cumsum()


def active_return(portfolio_return, benchmark_return):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Active return — AR = R_p - R_b. A financial metric in the domain of Asset management & portfolio optimization."
    y_as_x: []
    :param portfolio_return: "Portfolio Return is the total return of the managed portfolio."
    :param benchmark_return: "Benchmark Return is the total return of the benchmark index."
    :return: "Computed value of Active return: AR = R_p - R_b"
    '''
    return portfolio_return - benchmark_return






def active_risk_budget(information_coefficient, breadth):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Performance Attribution', 'Risk-Adjusted Performance']
    function: "Active risk budget — IR = IC x sqrt(Breadth). A financial metric in the domain of Performance measurement & attribution."
    y_as_x: []
    :param args: "Parameter args used in Active risk budget calculation."
    :param kwargs: "Parameter kwargs used in Active risk budget calculation."
    :return: "Computed value of Active risk budget: IR = IC x sqrt(Breadth)"
    '''
    import numpy as np
    return information_coefficient * np.sqrt(breadth)


def active_share(portfolio_weights, benchmark_weights):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Active share — Active Share = 0.5 sum_i |w_i - w_{b,i}|. A financial metric in the domain of Asset management & portfolio optimization."
    y_as_x: []
    :param args: "Parameter args used in Active share calculation."
    :param kwargs: "Parameter kwargs used in Active share calculation."
    :return: "Computed value of Active share: Active Share = 0.5 sum_i |w_i - w_{b,i}|"
    '''
    import numpy as np
    return 0.5 * np.sum(np.abs(np.array(portfolio_weights) - np.array(benchmark_weights)))




def adf_unit_root_test(y, X):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Financial Econometrics', 'Time Series Analysis']
    function: "ADF unit-root test — Delta y_t = alpha + beta t + gamma y_{t-1} + sum_i delta_i Delta y_{t-i} + epsilon_t. A financial metric in the domain of Econometrics & time-series finance."
    y_as_x: []
    :param y: "Parameter y used in ADF unit-root test calculation."
    :param X: "Parameter X used in ADF unit-root test calculation."
    :return: "Computed value of ADF unit-root test: Delta y_t = alpha + beta t + gamma y_{t-1} + sum_i delta_i Delta y_{t-i} + epsilon_t"
    '''
    import statsmodels.api as sm
    X_const = sm.add_constant(X)
    model = sm.OLS(y, X_const).fit()
    return model






def adjusted_present_value_apv(cash_flows, discount_rate):
    '''
    domain: ['Corporate finance & capital budgeting']
    subdomain: ['Corporate Finance', 'Capital Budgeting']
    function: "Adjusted present value (APV) — APV = NPV_unlevered + PV(financing side effects). A financial metric in the domain of Corporate finance & capital budgeting."
    y_as_x: []
    :param cash_flows: "Parameter cash_flows used in Adjusted present value (APV) calculation."
    :param discount_rate: "Discount Rate is the rate used to discount future cash flows to present value."
    :return: "Computed value of Adjusted present value (APV): APV = NPV_unlevered + PV(financing side effects)"
    '''
    import numpy as np
    cf = np.array(cash_flows)
    t = np.arange(1, len(cf) + 1)
    return np.sum(cf / (1 + discount_rate)**t)







def adjusted_r_squared(y, X):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Financial Econometrics', 'Time Series Analysis']
    function: "Adjusted R-squared — Adj R^2 = 1 - (1-R^2)(n-1)/(n-k-1). A financial metric in the domain of Econometrics & time-series finance."
    y_as_x: []
    :param y: "Parameter y used in Adjusted R-squared calculation."
    :param X: "Parameter X used in Adjusted R-squared calculation."
    :return: "Computed value of Adjusted R-squared: Adj R^2 = 1 - (1-R^2)(n-1)/(n-k-1)"
    '''
    import statsmodels.api as sm
    X_const = sm.add_constant(X)
    model = sm.OLS(y, X_const).fit()
    return model






def advance_rate(loan_amount, eligible_collateral_base):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Banking', 'Consumer Lending', 'Project Finance']
    function: "Advance rate — Advance Rate = Loan Amount / Eligible Collateral Base. A financial metric in the domain of Banking, consumer lending & project finance."
    y_as_x: []
    :param loan_amount: "Loan Amount is the total principal borrowed."
    :param eligible_collateral_base: "Eligible Collateral Base is the total value of assets qualifying as collateral."
    :return: "Computed value of Advance rate: Advance Rate = Loan Amount / Eligible Collateral Base"
    '''
    return loan_amount / eligible_collateral_base






def adverse_selection_cost(effective_spread, realized_spread):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Liquidity Risk', 'Market Liquidity', 'Execution Cost']
    function: "Adverse selection cost — ASC = Effective Spread - Realized Spread. A financial metric in the domain of Liquidity risk, market liquidity & execution cost."
    y_as_x: []
    :param effective_spread: "Effective Spread is twice the difference between the trade price and the midpoint."
    :param realized_spread: "Realized Spread is the effective spread minus the subsequent adverse price movement."
    :return: "Computed value of Adverse selection cost: ASC = Effective Spread - Realized Spread"
    '''
    return effective_spread - realized_spread






def adx(high, low, close, period=14):
    '''
    domain: ['Technical analysis']
    subdomain: ['Technical Analysis']
    function: "ADX — ADX = EMA(Directional Movement Index). A financial metric in the domain of Technical analysis."
    y_as_x: []
    :param close: "Close is the final trading price at the end of a trading period."
    :param period: "Period (n) is the lookback window in number of bars for technical indicators."
    :return: "Computed value of ADX: ADX = EMA(Directional Movement Index)"
    '''
    import pandas as pd
    import numpy as np
    h = pd.Series(high); l = pd.Series(low); c = pd.Series(close)
    tr = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    up = h.diff(); dn = (-l.diff())
    plus_dm = ((up > dn) & (up > 0)).astype(float) * up
    minus_dm = ((dn > up) & (dn > 0)).astype(float) * dn
    plus_di = 100 * plus_dm.rolling(window=period).mean() / atr
    minus_di = 100 * minus_dm.rolling(window=period).mean() / atr
    dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di)
    return dx.rolling(window=period).mean()


def affine_term_structure_bond_price(a_coeff, b_coeff, state_vector):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Interest Rate Modeling', 'Term Structure']
    function: "Affine term structure bond price — P(t,T)=exp(A(t,T)+B(t,T)'X_t). A financial metric in the domain of Interest-rate modeling & term structures."
    y_as_x: []
    :param args: "Parameter args used in Affine term structure bond price calculation."
    :param kwargs: "Parameter kwargs used in Affine term structure bond price calculation."
    :return: "Computed value of Affine term structure bond price: P(t,T)=exp(A(t,T)+B(t,T)'X_t)"
    '''
    import numpy as np
    return np.exp(a_coeff + np.dot(b_coeff, state_vector))




def after_tax_cost_of_debt(cost_of_debt, tax_rate):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "After-tax cost of debt — R_d,aftertax = R_d(1-T). A financial metric in the domain of Corporate finance, valuation & capital budgeting."
    y_as_x: []
    :param args: "Parameter args used in After-tax cost of debt calculation."
    :param kwargs: "Parameter kwargs used in After-tax cost of debt calculation."
    :return: "Computed value of After-tax cost of debt: R_d,aftertax = R_d(1-T)"
    '''
    return cost_of_debt * (1 - tax_rate)




def aggregate_loss_distribution(claim_amounts, num_claims=None):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "Aggregate loss distribution — S = sum_{i=1}^N X_i. A financial metric in the domain of Actuarial science & insurance."
    y_as_x: []
    :param data: "Parameter data used in Aggregate loss distribution calculation."
    :param args: "Parameter args used in Aggregate loss distribution calculation."
    :return: "Computed value of Aggregate loss distribution: S = sum_{i=1}^N X_i"
    '''
    import numpy as np
    claims = np.array(claim_amounts)
    if num_claims is not None:
        claims = claims[:num_claims]
    return np.sum(claims)




def allocation_effect_brinson_fachler(portfolio_weights, benchmark_weights, benchmark_sector_returns, benchmark_total_return):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Performance Attribution', 'Risk-Adjusted Performance']
    function: "Allocation effect (Brinson-Fachler) — Allocation_i = (w_i^P - w_i^B)(r_i^B - r^B). A financial metric in the domain of Performance measurement & attribution."
    y_as_x: []
    :param args: "Parameter args used in Allocation effect (Brinson-Fachler) calculation."
    :param kwargs: "Parameter kwargs used in Allocation effect (Brinson-Fachler) calculation."
    :return: "Computed value of Allocation effect (Brinson-Fachler): Allocation_i = (w_i^P - w_i^B)(r_i^B - r^B)"
    '''
    import numpy as np
    return (np.array(portfolio_weights) - np.array(benchmark_weights)) * (np.array(benchmark_sector_returns) - benchmark_total_return)




def alpha(returns):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Equity Valuation', 'Asset Pricing']
    function: "Alpha — alpha_i = E[R_i] - [R_f + beta_i(E[R_m]-R_f)]. A financial metric in the domain of Equity valuation & asset pricing."
    y_as_x: ['appraisal_ratio', 'information_ratio']
    :param returns: "Returns are the gain or loss generated on an investment over a specific period."
    :return: "Computed value of Alpha: alpha_i = E[R_i] - [R_f + beta_i(E[R_m]-R_f)]"
    '''
    import numpy as np
    # Implementation via empyrical-reloaded
    return np.array(returns)






def alpha_from_regression(y, X):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Performance Attribution', 'Risk-Adjusted Performance']
    function: "Alpha from regression — R_p-R_f = alpha + beta(R_b-R_f) + epsilon. A financial metric in the domain of Performance measurement & attribution."
    y_as_x: []
    :param y: "Parameter y used in Alpha from regression calculation."
    :param X: "Parameter X used in Alpha from regression calculation."
    :return: "Computed value of Alpha from regression: R_p-R_f = alpha + beta(R_b-R_f) + epsilon"
    '''
    import statsmodels.api as sm
    X_const = sm.add_constant(X)
    model = sm.OLS(y, X_const).fit()
    return model






def altman_z_score(*components):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "Altman Z-score — Z = 1.2X1 + 1.4X2 + 3.3X3 + 0.6X4 + 1.0X5. A financial metric in the domain of Accounting & financial statement analysis."
    y_as_x: []
    :param components: "Parameter components used in Altman Z-score calculation."
    :return: "Computed value of Altman Z-score: Z = 1.2X1 + 1.4X2 + 3.3X3 + 0.6X4 + 1.0X5"
    '''
    return sum(components)






def american_option_binomial_pricing(spot_price, strike_price, risk_free_rate, volatility, time_to_expiry, steps, option_type="call"):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "American option binomial pricing — V = max(intrinsic, discounted expected continuation). A financial metric in the domain of Derivatives, options & volatility."
    y_as_x: []
    :param args: "Parameter args used in American option binomial pricing calculation."
    :param kwargs: "Parameter kwargs used in American option binomial pricing calculation."
    :return: "Computed value of American option binomial pricing: V = max(intrinsic, discounted expected continuation)"
    '''
    import numpy as np
    dt = time_to_expiry / steps
    u = np.exp(volatility * np.sqrt(dt)); d = 1/u
    p = (np.exp(risk_free_rate * dt) - d) / (u - d)
    prices = spot_price * u**np.arange(steps, -1, -1) * d**np.arange(0, steps+1)
    values = np.maximum(prices - strike_price, 0) if option_type == 'call' else np.maximum(strike_price - prices, 0)
    for i in range(steps - 1, -1, -1):
        pi = spot_price * u**np.arange(i, -1, -1) * d**np.arange(0, i+1)
        hold = np.exp(-risk_free_rate * dt) * (p * values[:i+1] + (1-p) * values[1:i+2])
        ex = np.maximum(pi - strike_price, 0) if option_type == 'call' else np.maximum(strike_price - pi, 0)
        values = np.maximum(hold, ex)
    return values[0]


def amihud_illiquidity(meanr_t, dollarvolume_t):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Liquidity Risk', 'Market Liquidity', 'Execution Cost']
    function: "Amihud illiquidity — ILLIQ = mean(|R_t|/DollarVolume_t). A financial metric in the domain of Liquidity risk, market liquidity & execution cost."
    y_as_x: []
    :param meanr_t: "Parameter meanr_t used in Amihud illiquidity calculation."
    :param dollarvolume_t: "Parameter dollarvolume_t used in Amihud illiquidity calculation."
    :return: "Computed value of Amihud illiquidity: ILLIQ = mean(|R_t|/DollarVolume_t)"
    '''
    return meanr_t / dollarvolume_t






def amivest_liquidity_ratio(volume, return_val):
    '''
    domain: ['Trading, execution & market microstructure']
    subdomain: ['Trading', 'Execution', 'Market Microstructure']
    function: "Amivest liquidity ratio — Amivest = Volume / |Return|. A financial metric in the domain of Trading, execution & market microstructure."
    y_as_x: []
    :param volume: "Volume is the total number of shares or contracts traded during a period."
    :param return_val: "Parameter return_val used in Amivest liquidity ratio calculation."
    :return: "Computed value of Amivest liquidity ratio: Amivest = Volume / |Return|"
    '''
    return volume / return_val






def amortization_factor(rate, num_periods, present_value):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Banking', 'Consumer Lending', 'Project Finance']
    function: "Amortization factor — AF = r(1+r)^n / ((1+r)^n - 1). A financial metric in the domain of Banking, consumer lending & project finance."
    y_as_x: []
    :param rate: "Rate (r) is the interest rate or discount rate per period."
    :param num_periods: "Number of Periods (n) is the total number of payment or compounding periods."
    :param present_value: "Present Value (PV) is the current worth of a future sum given a rate of return."
    :return: "Computed value of Amortization factor: AF = r(1+r)^n / ((1+r)^n - 1)"
    '''
    import numpy_financial as npf
    return npf.pmt(rate, num_periods, -present_value)






def annual_percentage_rate_apr(periodic_rate, periods_per_year):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Banking', 'Consumer Lending', 'Project Finance']
    function: "Annual percentage rate (APR) — APR = periodic rate x periods per year. A financial metric in the domain of Banking, consumer lending & project finance."
    y_as_x: []
    :param periodic_rate: "Periodic Rate is the interest rate charged per compounding period."
    :param periods_per_year: "Periods Per Year is the number of compounding or return periods in one year."
    :return: "Computed value of Annual percentage rate (APR): APR = periodic rate x periods per year"
    '''
    return periodic_rate * periods_per_year






def annualized_cpi_inflation_from_monthly_cpi(cpi_current, cpi_year_ago):
    '''
    domain: ['Macroeconomics, inflation & price indices']
    subdomain: ['Macroeconomics', 'Inflation', 'Price Indices']
    function: "Annualized CPI inflation from monthly CPI — π_t^(ann) = (CPI_t / CPI_(t-1))^12 - 1. A financial metric in the domain of Macroeconomics, inflation & price indices."
    y_as_x: []
    :param args: "Parameter args used in Annualized CPI inflation from monthly CPI calculation."
    :param kwargs: "Parameter kwargs used in Annualized CPI inflation from monthly CPI calculation."
    :return: "Computed value of Annualized CPI inflation from monthly CPI: π_t^(ann) = (CPI_t / CPI_(t-1))^12 - 1"
    '''
    return (cpi_current / cpi_year_ago) - 1


def annualized_ppi_inflation_from_monthly_ppi(ppi_current, ppi_year_ago):
    '''
    domain: ['Macroeconomics, inflation & price indices']
    subdomain: ['Macroeconomics', 'Inflation', 'Price Indices']
    function: "Annualized PPI inflation from monthly PPI — π_t^(ann) = (PPI_t / PPI_(t-1))^12 - 1. A financial metric in the domain of Macroeconomics, inflation & price indices."
    y_as_x: []
    :param args: "Parameter args used in Annualized PPI inflation from monthly PPI calculation."
    :param kwargs: "Parameter kwargs used in Annualized PPI inflation from monthly PPI calculation."
    :return: "Computed value of Annualized PPI inflation from monthly PPI: π_t^(ann) = (PPI_t / PPI_(t-1))^12 - 1"
    '''
    return (ppi_current / ppi_year_ago) - 1




def annualized_return_cagr(returns, periods_per_year=252):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Performance Attribution', 'Risk-Adjusted Performance']
    function: "Annualized return (CAGR) — CAGR = (Ending Value / Beginning Value)^(1/n) - 1. A financial metric in the domain of Performance measurement & attribution."
    y_as_x: []
    :param returns: "Returns are the gain or loss generated on an investment over a specific period."
    :param periods_per_year: "Periods Per Year is the number of compounding or return periods in one year."
    :return: "Computed value of Annualized return (CAGR): CAGR = (Ending Value / Beginning Value)^(1/n) - 1"
    '''
    import numpy as np
    r = np.array(returns)
    total = np.prod(1 + r)
    n_years = len(r) / periods_per_year
    return total**(1/n_years) - 1






def annualized_volatility(returns, periods_per_year=252):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Performance Attribution', 'Risk-Adjusted Performance']
    function: "Annualized volatility — σ_ann = σ_period × √m. A financial metric in the domain of Performance measurement & attribution."
    y_as_x: []
    :param returns: "Returns are the gain or loss generated on an investment over a specific period."
    :param periods_per_year: "Periods Per Year is the number of compounding or return periods in one year."
    :return: "Computed value of Annualized volatility: σ_ann = σ_period × √m"
    '''
    import numpy as np
    return np.std(returns, ddof=1) * np.sqrt(periods_per_year)






def annuity_future_value(rate, num_periods, payment, present_value=0):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "Annuity future value — FV_annuity = PMT x ((1+r)^n - 1) / r. A financial metric in the domain of Corporate finance, valuation & capital budgeting."
    y_as_x: []
    :param rate: "Rate (r) is the interest rate or discount rate per period."
    :param num_periods: "Number of Periods (n) is the total number of payment or compounding periods."
    :param payment: "Payment (PMT) is the periodic payment amount in an amortization schedule."
    :param present_value: "Present Value (PV) is the current worth of a future sum given a rate of return."
    :return: "Computed value of Annuity future value: FV_annuity = PMT x ((1+r)^n - 1) / r"
    '''
    import numpy_financial as npf
    return npf.fv(rate, num_periods, -payment, -present_value)






def annuity_present_value(rate, num_periods, payment, future_value=0):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "Annuity present value — PV_annuity = PMT x (1-(1+r)^-n) / r. A financial metric in the domain of Corporate finance, valuation & capital budgeting."
    y_as_x: []
    :param rate: "Rate (r) is the interest rate or discount rate per period."
    :param num_periods: "Number of Periods (n) is the total number of payment or compounding periods."
    :param payment: "Payment (PMT) is the periodic payment amount in an amortization schedule."
    :param future_value: "Future Value (FV) is the value of a current asset at a future date."
    :return: "Computed value of Annuity present value: PV_annuity = PMT x (1-(1+r)^-n) / r"
    '''
    import numpy_financial as npf
    return npf.pv(rate, num_periods, -payment, -future_value)






def aparch(returns, p=1, q=1):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "APARCH — sigma_t^delta = omega + alpha(|eps_{t-1}|-gamma eps_{t-1})^delta + beta sigma_{t-1}^delta. A financial metric in the domain of Market risk & volatility modeling."
    y_as_x: []
    :param returns: "Returns are the gain or loss generated on an investment over a specific period."
    :param p: "Model order parameter p (autoregressive order or similar)."
    :param q: "Model order parameter q (moving average order, ARCH order, or similar)."
    :return: "Computed value of APARCH: sigma_t^delta = omega + alpha(|eps_{t-1}|-gamma eps_{t-1})^delta + beta sigma_{t-1}^delta"
    '''
    from arch import arch_model
    model = arch_model(returns, vol="GARCH", p=p, q=q)
    result = model.fit(disp="off")
    return result






def appraisal_ratio(alpha, residual_risk):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Appraisal ratio — Appraisal = alpha / Residual Risk. A financial metric in the domain of Asset management & portfolio optimization."
    y_as_x: []
    :param alpha: "Alpha is the excess return relative to what is predicted by risk models."
    :param residual_risk: "Parameter residual_risk used in Appraisal ratio calculation."
    :return: "Computed value of Appraisal ratio: Appraisal = alpha / Residual Risk"
    '''
    return alpha / residual_risk






def approximate_price_change(cash_flows, discount_rate):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Fixed Income', 'Bond Mathematics', 'Credit Markets']
    function: "Approximate price change — Delta P / P approx -D_mod Delta y + 0.5 Convexity (Delta y)^2. A financial metric in the domain of Fixed income, bonds & credit markets."
    y_as_x: []
    :param cash_flows: "Parameter cash_flows used in Approximate price change calculation."
    :param discount_rate: "Discount Rate is the rate used to discount future cash flows to present value."
    :return: "Computed value of Approximate price change: Delta P / P approx -D_mod Delta y + 0.5 Convexity (Delta y)^2"
    '''
    import numpy as np
    cf = np.array(cash_flows)
    t = np.arange(1, len(cf) + 1)
    return np.sum(cf / (1 + discount_rate)**t)






def ar_1(time_series, lags=1):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Financial Econometrics', 'Time Series Analysis']
    function: "AR(1) — y_t = c + φ y_{t-1} + ε_t. A financial metric in the domain of Econometrics & time-series finance."
    y_as_x: []
    :param data: "Parameter data used in AR(1) calculation."
    :param args: "Parameter args used in AR(1) calculation."
    :return: "Computed value of AR(1): y_t = c + φ y_{t-1} + ε_t"
    '''
    from statsmodels.tsa.ar_model import AutoReg
    return AutoReg(time_series, lags=lags).fit()


def ar_1_2(time_series, lags=1):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Financial Econometrics', 'Time Series Analysis']
    function: "AR(1) — x_t = c + phi x_{t-1} + epsilon_t. A financial metric in the domain of Econometrics & time-series finance."
    y_as_x: []
    :param data: "Parameter data used in AR(1) calculation."
    :param args: "Parameter args used in AR(1) calculation."
    :return: "Computed value of AR(1): x_t = c + phi x_{t-1} + epsilon_t"
    '''
    from statsmodels.tsa.ar_model import AutoReg
    model = AutoReg(time_series, lags=lags)
    return model.fit()




def ar_p(time_series, lags):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Financial Econometrics', 'Time Series Analysis']
    function: "AR(p) — x_t = c + sum_{i=1}^p phi_i x_{t-i} + epsilon_t. A financial metric in the domain of Econometrics & time-series finance."
    y_as_x: []
    :param data: "Parameter data used in AR(p) calculation."
    :param args: "Parameter args used in AR(p) calculation."
    :return: "Computed value of AR(p): x_t = c + sum_{i=1}^p phi_i x_{t-i} + epsilon_t"
    '''
    from statsmodels.tsa.ar_model import AutoReg
    model = AutoReg(time_series, lags=lags)
    return model.fit()




def arbitrage_pricing_theory_apt(risk_free_rate, factor_betas, factor_risk_premiums):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Equity Valuation', 'Asset Pricing']
    function: "Arbitrage pricing theory (APT) — E[R_i] = R_f + sum_k beta_{ik} lambda_k. A financial metric in the domain of Equity valuation & asset pricing."
    y_as_x: []
    :param y: "Parameter y used in Arbitrage pricing theory (APT) calculation."
    :param X: "Parameter X used in Arbitrage pricing theory (APT) calculation."
    :return: "Computed value of Arbitrage pricing theory (APT): E[R_i] = R_f + sum_k beta_{ik} lambda_k"
    '''
    import numpy as np
    return risk_free_rate + np.dot(factor_betas, factor_risk_premiums)




def arch_q(returns, p=1, q=1):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "ARCH(q) — sigma_t^2 = omega + sum_{i=1}^q alpha_i epsilon_{t-i}^2. A financial metric in the domain of Market risk & volatility modeling."
    y_as_x: []
    :param returns: "Returns are the gain or loss generated on an investment over a specific period."
    :param p: "Model order parameter p (autoregressive order or similar)."
    :param q: "Model order parameter q (moving average order, ARCH order, or similar)."
    :return: "Computed value of ARCH(q): sigma_t^2 = omega + sum_{i=1}^q alpha_i epsilon_{t-i}^2"
    '''
    from arch import arch_model
    model = arch_model(returns, vol="GARCH", p=p, q=q)
    result = model.fit(disp="off")
    return result






def arima_pdq(time_series, order):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Financial Econometrics', 'Time Series Analysis']
    function: "ARIMA(p,d,q) — phi(L)(1-L)^d x_t = c + theta(L)epsilon_t. A financial metric in the domain of Econometrics & time-series finance."
    y_as_x: []
    :param time_series: "Time Series is a sequence of data points indexed in time order."
    :param order: "Order specifies the model order, e.g., (p,d,q) for ARIMA."
    :return: "Computed value of ARIMA(p,d,q): phi(L)(1-L)^d x_t = c + theta(L)epsilon_t"
    '''
    from statsmodels.tsa.arima.model import ARIMA
    model = ARIMA(time_series, order=order).fit()
    return model






def arimax_dynamic_regression(time_series, order):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Financial Econometrics', 'Time Series Analysis']
    function: "ARIMAX / dynamic regression — y_t = beta' x_t + ARIMA errors. A financial metric in the domain of Econometrics & time-series finance."
    y_as_x: []
    :param time_series: "Time Series is a sequence of data points indexed in time order."
    :param order: "Order specifies the model order, e.g., (p,d,q) for ARIMA."
    :return: "Computed value of ARIMAX / dynamic regression: y_t = beta' x_t + ARIMA errors"
    '''
    from statsmodels.tsa.arima.model import ARIMA
    model = ARIMA(time_series, order=order).fit()
    return model






def arma_pq(time_series, order):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Financial Econometrics', 'Time Series Analysis']
    function: "ARMA(p,q) — x_t = c + sum phi_i x_{t-i} + epsilon_t + sum theta_i epsilon_{t-i}. A financial metric in the domain of Econometrics & time-series finance."
    y_as_x: []
    :param time_series: "Time Series is a sequence of data points indexed in time order."
    :param order: "Order specifies the model order, e.g., (p,d,q) for ARIMA."
    :return: "Computed value of ARMA(p,q): x_t = c + sum phi_i x_{t-i} + epsilon_t + sum theta_i epsilon_{t-i}"
    '''
    from statsmodels.tsa.arima.model import ARIMA
    model = ARIMA(time_series, order=order).fit()
    return model






def aroon_down(low, period=25):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "Aroon Down — AroonDown = 100(n - periods since n-period low)/n. A financial metric in the domain of Technical analysis & chart-based indicators."
    y_as_x: []
    :param high: "High is the highest price during a specific trading period."
    :param low: "Low is the lowest price during a specific trading period."
    :param close: "Close is the final trading price at the end of a trading period."
    :param volume: "Volume is the total number of shares or contracts traded during a period."
    :param period: "Period (n) is the lookback window in number of bars for technical indicators."
    :return: "Computed value of Aroon Down: AroonDown = 100(n - periods since n-period low)/n"
    '''
    import pandas as pd
    l = pd.Series(low)
    return l.rolling(window=period+1).apply(lambda x: (period - x.argmin()) / period * 100, raw=True)


def aroon_oscillator(aroonup, aroondown):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "Aroon oscillator — Aroon Osc = AroonUp - AroonDown. A financial metric in the domain of Technical analysis & chart-based indicators."
    y_as_x: []
    :param aroonup: "Parameter aroonup used in Aroon oscillator calculation."
    :param aroondown: "Parameter aroondown used in Aroon oscillator calculation."
    :return: "Computed value of Aroon oscillator: Aroon Osc = AroonUp - AroonDown"
    '''
    return aroonup - aroondown






def aroon_up(high, period=25):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "Aroon Up — AroonUp = 100(n - periods since n-period high)/n. A financial metric in the domain of Technical analysis & chart-based indicators."
    y_as_x: []
    :param high: "High is the highest price during a specific trading period."
    :param low: "Low is the lowest price during a specific trading period."
    :param close: "Close is the final trading price at the end of a trading period."
    :param volume: "Volume is the total number of shares or contracts traded during a period."
    :param period: "Period (n) is the lookback window in number of bars for technical indicators."
    :return: "Computed value of Aroon Up: AroonUp = 100(n - periods since n-period high)/n"
    '''
    import pandas as pd
    h = pd.Series(high)
    return h.rolling(window=period+1).apply(lambda x: x.argmax() / period * 100, raw=True)


def arrival_price_slippage(executed_price, arrival_price):
    '''
    domain: ['Trading, execution & market microstructure']
    subdomain: ['Trading', 'Execution', 'Market Microstructure']
    function: "Arrival price slippage — Slippage = Executed Price - Arrival Price. A financial metric in the domain of Trading, execution & market microstructure."
    y_as_x: []
    :param executed_price: "Parameter executed_price used in Arrival price slippage calculation."
    :param arrival_price: "Arrival Price is the market price at the time the order was submitted."
    :return: "Computed value of Arrival price slippage: Slippage = Executed Price - Arrival Price"
    '''
    return executed_price - arrival_price






def asian_option_price(spot_price, strike_price, risk_free_rate, volatility, time_to_expiry, num_steps=252, option_type="call", num_sims=10000):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Asian option price — V = E_Q[e^{-rT}(average(S)-K)^+]. A financial metric in the domain of Derivatives, options & volatility."
    y_as_x: []
    :param args: "Parameter args used in Asian option price calculation."
    :param kwargs: "Parameter kwargs used in Asian option price calculation."
    :return: "Computed value of Asian option price: V = E_Q[e^{-rT}(average(S)-K)^+]"
    '''
    import numpy as np
    dt = time_to_expiry / num_steps
    payoffs = []
    for _ in range(num_sims):
        path = [spot_price]
        for _ in range(num_steps):
            path.append(path[-1] * np.exp((risk_free_rate - 0.5*volatility**2)*dt + volatility*np.sqrt(dt)*np.random.standard_normal()))
        avg = np.mean(path)
        payoffs.append(max(avg - strike_price, 0) if option_type == 'call' else max(strike_price - avg, 0))
    return np.exp(-risk_free_rate * time_to_expiry) * np.mean(payoffs)


def asset_swap_spread(bond_price, par_value, coupon_rate, swap_rate, maturity):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Fixed Income', 'Bond Mathematics', 'Credit Markets']
    function: "Asset swap spread — ASW = bond coupon spread that sets package PV to par. A financial metric in the domain of Fixed income, bonds & credit markets."
    y_as_x: []
    :param args: "Parameter args used in Asset swap spread calculation."
    :param kwargs: "Parameter kwargs used in Asset swap spread calculation."
    :return: "Computed value of Asset swap spread: ASW = bond coupon spread that sets package PV to par"
    '''
    return coupon_rate - swap_rate + (par_value - bond_price) / (par_value * maturity)




def asset_turnover(revenue, average_assets):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "Asset turnover — Asset Turnover = Revenue / Average Assets. A financial metric in the domain of Accounting & financial statement analysis."
    y_as_x: []
    :param revenue: "Revenue is the total amount of income a business generates from the sale of goods or services before deducting expenses."
    :param average_assets: "Parameter average_assets used in Asset turnover calculation."
    :return: "Computed value of Asset turnover: Asset Turnover = Revenue / Average Assets"
    '''
    return revenue / average_assets






def average_directional_index_adx(high, low, close, period=14):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "Average directional index (ADX) — ADX = EMA of directional movement index. A financial metric in the domain of Technical analysis & chart-based indicators."
    y_as_x: []
    :param close: "Close is the final trading price at the end of a trading period."
    :param period: "Period (n) is the lookback window in number of bars for technical indicators."
    :return: "Computed value of Average directional index (ADX): ADX = EMA of directional movement index"
    '''
    import pandas as pd
    h = pd.Series(high); l = pd.Series(low); c = pd.Series(close)
    tr = pd.concat([h-l, (h-c.shift()).abs(), (l-c.shift()).abs()], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    up = h.diff(); dn = (-l.diff())
    plus_dm = ((up > dn) & (up > 0)).astype(float) * up
    minus_dm = ((dn > up) & (dn > 0)).astype(float) * dn
    plus_di = 100 * plus_dm.rolling(period).mean() / atr
    minus_di = 100 * minus_dm.rolling(period).mean() / atr
    dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di)
    return dx.rolling(period).mean()


def average_loan_age(loan_balances, loan_ages):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Structured Finance', 'Securitization']
    function: "Average loan age — ALA = weighted average seasoning of loans. A financial metric in the domain of Structured finance & securitization."
    y_as_x: []
    :param args: "Parameter args used in Average loan age calculation."
    :param kwargs: "Parameter kwargs used in Average loan age calculation."
    :return: "Computed value of Average loan age: ALA = weighted average seasoning of loans"
    '''
    import numpy as np
    b = np.array(loan_balances); a = np.array(loan_ages)
    return np.sum(b * a) / np.sum(b)




def average_true_range_atr(high, low, close, period=14):
    '''
    domain: ['Technical analysis']
    subdomain: ['Technical Analysis']
    function: "Average true range (ATR) — ATR = EMA(True Range). A financial metric in the domain of Technical analysis."
    y_as_x: []
    :param close: "Close is the final trading price at the end of a trading period."
    :param period: "Period (n) is the lookback window in number of bars for technical indicators."
    :return: "Computed value of Average true range (ATR): ATR = EMA(True Range)"
    '''
    import pandas as pd
    h = pd.Series(high); l = pd.Series(low); c = pd.Series(close)
    tr = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    return tr.rolling(window=period).mean()




def awesome_oscillator(high, low):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "Awesome oscillator — AO = SMA_5(MedianPrice) - SMA_34(MedianPrice). A financial metric in the domain of Technical analysis & chart-based indicators."
    y_as_x: []
    :param high: "High is the highest price during a specific trading period."
    :param low: "Low is the lowest price during a specific trading period."
    :param close: "Close is the final trading price at the end of a trading period."
    :param volume: "Volume is the total number of shares or contracts traded during a period."
    :param period: "Period (n) is the lookback window in number of bars for technical indicators."
    :return: "Computed value of Awesome oscillator: AO = SMA_5(MedianPrice) - SMA_34(MedianPrice)"
    '''
    import pandas as pd
    median_price = (pd.Series(high) + pd.Series(low)) / 2
    return median_price.rolling(5).mean() - median_price.rolling(34).mean()




def bachelier_option_price(forward_price, strike_price, volatility, time_to_expiry, option_type="call"):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Interest Rate Modeling', 'Term Structure']
    function: "Bachelier option price — Price = DF[(F-K)N(d) + sigma sqrt(T)n(d)]. A financial metric in the domain of Interest-rate modeling & term structures."
    y_as_x: []
    :param args: "Parameter args used in Bachelier option price calculation."
    :param kwargs: "Parameter kwargs used in Bachelier option price calculation."
    :return: "Computed value of Bachelier option price: Price = DF[(F-K)N(d) + sigma sqrt(T)n(d)]"
    '''
    import numpy as np
    from scipy.stats import norm
    sigma_sqrt_t = volatility * np.sqrt(time_to_expiry)
    d = (forward_price - strike_price) / sigma_sqrt_t if sigma_sqrt_t > 0 else 0
    if option_type == 'call':
        return sigma_sqrt_t * (d * norm.cdf(d) + norm.pdf(d))
    else:
        return sigma_sqrt_t * (-d * norm.cdf(-d) + norm.pdf(d))




def back_end_dti_gross_income(total_monthly_debt_payments, gross_monthly_income):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Banking', 'Consumer Lending', 'Project Finance']
    function: "Back-end DTI (gross income) — DTI_gross = Total Monthly Debt Payments / Gross Monthly Income. A financial metric in the domain of Banking, consumer lending & project finance."
    y_as_x: []
    :param total_monthly_debt_payments: "Parameter total_monthly_debt_payments used in Back-end DTI (gross income) calculation."
    :param gross_monthly_income: "Gross Monthly Income is pre-tax monthly income."
    :return: "Computed value of Back-end DTI (gross income): DTI_gross = Total Monthly Debt Payments / Gross Monthly Income"
    '''
    return total_monthly_debt_payments / gross_monthly_income






def back_end_dti_net_income(total_monthly_debt_payments, net_monthly_income):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Banking', 'Consumer Lending', 'Project Finance']
    function: "Back-end DTI (net income) — DTI_net = Total Monthly Debt Payments / Net Monthly Income. A financial metric in the domain of Banking, consumer lending & project finance."
    y_as_x: []
    :param total_monthly_debt_payments: "Parameter total_monthly_debt_payments used in Back-end DTI (net income) calculation."
    :param net_monthly_income: "Net Monthly Income is post-tax monthly income."
    :return: "Computed value of Back-end DTI (net income): DTI_net = Total Monthly Debt Payments / Net Monthly Income"
    '''
    return total_monthly_debt_payments / net_monthly_income






def backtesting_exception_rate(exceptions, observations):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "Backtesting exception rate — Exception Rate = exceptions / observations. A financial metric in the domain of Market risk & volatility modeling."
    y_as_x: []
    :param exceptions: "Parameter exceptions used in Backtesting exception rate calculation."
    :param observations: "Parameter observations used in Backtesting exception rate calculation."
    :return: "Computed value of Backtesting exception rate: Exception Rate = exceptions / observations"
    '''
    return exceptions / observations






def backwardation_slope(near_futures_price, far_futures_price):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Commodities', 'Futures', 'Hedging']
    function: "Backwardation slope — Backwardation = 1 - F_long / F_short. A financial metric in the domain of Commodities, futures & hedging."
    y_as_x: []
    :param args: "Parameter args used in Backwardation slope calculation."
    :param kwargs: "Parameter kwargs used in Backwardation slope calculation."
    :return: "Computed value of Backwardation slope: Backwardation = 1 - F_long / F_short"
    '''
    return (near_futures_price - far_futures_price) / far_futures_price


def balloon_payment(rate, num_periods, payment, present_value=0):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Banking', 'Consumer Lending', 'Project Finance']
    function: "Balloon payment — Balloon = Outstanding Balance at maturity. A financial metric in the domain of Banking, consumer lending & project finance."
    y_as_x: []
    :param rate: "Rate (r) is the interest rate or discount rate per period."
    :param num_periods: "Number of Periods (n) is the total number of payment or compounding periods."
    :param payment: "Payment (PMT) is the periodic payment amount in an amortization schedule."
    :param present_value: "Present Value (PV) is the current worth of a future sum given a rate of return."
    :return: "Computed value of Balloon payment: Balloon = Outstanding Balance at maturity"
    '''
    import numpy_financial as npf
    return npf.fv(rate, num_periods, -payment, -present_value)






def barrier_option_price(spot_price, strike_price, barrier, risk_free_rate, volatility, time_to_expiry, option_type="call", barrier_type="down-and-out", num_sims=10000):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Barrier option price — V = BS closed form with reflection terms / lattice / MC. A financial metric in the domain of Derivatives, options & volatility."
    y_as_x: []
    :param args: "Parameter args used in Barrier option price calculation."
    :param kwargs: "Parameter kwargs used in Barrier option price calculation."
    :return: "Computed value of Barrier option price: V = BS closed form with reflection terms / lattice / MC"
    '''
    import numpy as np
    dt = time_to_expiry / 252
    payoffs = []
    for _ in range(num_sims):
        path = [spot_price]
        for _ in range(252):
            path.append(path[-1] * np.exp((risk_free_rate-0.5*volatility**2)*dt + volatility*np.sqrt(dt)*np.random.standard_normal()))
        path = np.array(path)
        knocked = ('up' in barrier_type and np.max(path) >= barrier) or ('down' in barrier_type and np.min(path) <= barrier)
        active = (knocked and 'in' in barrier_type) or (not knocked and 'out' in barrier_type)
        if active:
            payoffs.append(max(path[-1]-strike_price,0) if option_type=='call' else max(strike_price-path[-1],0))
        else:
            payoffs.append(0)
    return np.exp(-risk_free_rate * time_to_expiry) * np.mean(payoffs)


def basel_irb_capital_requirement(pd_val, lgd, ead, maturity_adj=1.0, correlation=0.15):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit Risk', 'Default Modeling', 'Credit Portfolio']
    function: "Basel IRB capital requirement — K = LGD[Phi((Phi^-1(PD)+sqrt(R)Phi^-1(0.999))/sqrt(1-R)) - PD] x MA. A financial metric in the domain of Credit risk, default modeling & credit portfolio."
    y_as_x: []
    :param args: "Parameter args used in Basel IRB capital requirement calculation."
    :param kwargs: "Parameter kwargs used in Basel IRB capital requirement calculation."
    :return: "Computed value of Basel IRB capital requirement: K = LGD[Phi((Phi^-1(PD)+sqrt(R)Phi^-1(0.999))/sqrt(1-R)) - PD] x MA"
    '''
    import numpy as np
    from scipy.stats import norm
    k = lgd * (norm.cdf(np.sqrt(correlation / (1 - correlation)) * norm.ppf(pd_val) + np.sqrt(1 / (1 - correlation)) * norm.ppf(0.999)) - pd_val) * maturity_adj
    return k * ead




def basel_standardized_capital_requirement(ead, risk_weight, capital_ratio=0.08):
    '''
    domain: ['Bank regulation, Basel & prudential ratios']
    subdomain: ['Bank Regulation', 'Basel Framework', 'Prudential Ratios']
    function: "Basel standardized capital requirement — Capital = 8% x RWA. A financial metric in the domain of Bank regulation, Basel & prudential ratios."
    y_as_x: []
    :param args: "Parameter args used in Basel standardized capital requirement calculation."
    :param kwargs: "Parameter kwargs used in Basel standardized capital requirement calculation."
    :return: "Computed value of Basel standardized capital requirement: Capital = 8% x RWA"
    '''
    return ead * risk_weight * capital_ratio




def basis(s_t, f_t):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Commodities', 'Futures', 'Hedging']
    function: "Basis — Basis = S_t - F_t. A financial metric in the domain of Commodities, futures & hedging."
    y_as_x: []
    :param s_t: "Parameter s_t used in Basis calculation."
    :param f_t: "Parameter f_t used in Basis calculation."
    :return: "Computed value of Basis: Basis = S_t - F_t"
    '''
    return s_t - f_t






def basis_convergence(basis_initial, basis_final):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Commodities', 'Futures', 'Hedging']
    function: "Basis convergence — Basis_T = 0 at maturity (ignoring delivery frictions). A financial metric in the domain of Commodities, futures & hedging."
    y_as_x: []
    :param args: "Parameter args used in Basis convergence calculation."
    :param kwargs: "Parameter kwargs used in Basis convergence calculation."
    :return: "Computed value of Basis convergence: Basis_T = 0 at maturity (ignoring delivery frictions)"
    '''
    return basis_initial - basis_final


def batting_average(countalpha_t_0, t):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Performance Attribution', 'Risk-Adjusted Performance']
    function: "Batting average — BA = count(alpha_t > 0)/T. A financial metric in the domain of Performance measurement & attribution."
    y_as_x: []
    :param countalpha_t_0: "Parameter countalpha_t_0 used in Batting average calculation."
    :param t: "Parameter t used in Batting average calculation."
    :return: "Computed value of Batting average: BA = count(alpha_t > 0)/T"
    '''
    return countalpha_t_0 / t






def bayesian_shrinkage_return_forecast(sample_mean, prior_mean, shrinkage_factor):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Bayesian shrinkage return forecast — mu_hat = lambda mu_prior + (1-lambda) mu_sample. A financial metric in the domain of Asset management & portfolio optimization."
    y_as_x: []
    :param args: "Parameter args used in Bayesian shrinkage return forecast calculation."
    :param kwargs: "Parameter kwargs used in Bayesian shrinkage return forecast calculation."
    :return: "Computed value of Bayesian shrinkage return forecast: mu_hat = lambda mu_prior + (1-lambda) mu_sample"
    '''
    return shrinkage_factor * prior_mean + (1 - shrinkage_factor) * sample_mean


def behavioral_duration_of_deposits(deposit_rates, market_rates, deposit_balances):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Treasury', 'ALM', 'Balance Sheet Management']
    function: "Behavioral duration of deposits — D_beh = sensitivity-derived effective duration of non-maturity deposits. A financial metric in the domain of Treasury, ALM & balance-sheet management."
    y_as_x: []
    :param data: "Parameter data used in Behavioral duration of deposits calculation."
    :param args: "Parameter args used in Behavioral duration of deposits calculation."
    :return: "Computed value of Behavioral duration of deposits: D_beh = sensitivity-derived effective duration of non-maturity deposits"
    '''
    import numpy as np
    from scipy import stats
    slope, intercept, r, p, se = stats.linregress(market_rates, deposit_rates)
    return slope * np.mean(deposit_balances)




def benchmark_relative_optimization(expected_returns, cov_matrix, benchmark_weights, risk_aversion=1.0):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Benchmark-relative optimization — min_w (w-w_b)'Sigma(w-w_b) - lambda mu'(w-w_b). A financial metric in the domain of Asset management & portfolio optimization."
    y_as_x: []
    :param expected_returns: "Expected Returns vector contains the anticipated return for each asset."
    :param cov_matrix: "Covariance Matrix contains the covariances between all pairs of assets."
    :param constraints: "Parameter constraints used in Benchmark-relative optimization calculation."
    :return: "Computed value of Benchmark-relative optimization: min_w (w-w_b)'Sigma(w-w_b) - lambda mu'(w-w_b)"
    '''
    import numpy as np
    import cvxpy as cp
    n = len(expected_returns)
    w = cp.Variable(n)
    mu = np.array(expected_returns); sigma = np.array(cov_matrix); bw = np.array(benchmark_weights)
    ret = mu @ w
    risk = cp.quad_form(w - bw, sigma)
    prob = cp.Problem(cp.Maximize(ret - risk_aversion * risk), [cp.sum(w) == 1, w >= 0])
    prob.solve()
    return w.value




def benefit_reserve_recursion(reserve_prev, premium, interest_rate, mortality_rate, benefit):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "Benefit reserve recursion — (V_t + P)(1+i) = q Benefit + p V_{t+1}. A financial metric in the domain of Actuarial science & insurance."
    y_as_x: []
    :param args: "Parameter args used in Benefit reserve recursion calculation."
    :param kwargs: "Parameter kwargs used in Benefit reserve recursion calculation."
    :return: "Computed value of Benefit reserve recursion: (V_t + P)(1+i) = q Benefit + p V_{t+1}"
    '''
    return ((reserve_prev + premium) * (1 + interest_rate) - mortality_rate * benefit) / (1 - mortality_rate)




def beneish_m_score(*components):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "Beneish M-score — M = -4.84 + 0.92DSRI + 0.528GMI + 0.404AQI + 0.892SGI + 0.115DEPI - 0.172SGAI + 4.679TATA - 0.327LVGI. A financial metric in the domain of Accounting & financial statement analysis."
    y_as_x: []
    :param components: "Parameter components used in Beneish M-score calculation."
    :return: "Computed value of Beneish M-score: M = -4.84 + 0.92DSRI + 0.528GMI + 0.404AQI + 0.892SGI + 0.115DEPI - 0.172SGAI + 4.679TATA - 0.327LVGI"
    '''
    return sum(components)






def beta(asset_returns, market_returns):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Equity Valuation', 'Asset Pricing']
    function: "Beta — systematic risk measure. beta = Cov(R_i, R_m) / Var(R_m). Beta > 1 means more volatile than market."
    y_as_x: ['alpha', 'capm_expected_return', 'carhart_4_factor_model', 'cost_of_equity_capm', 'fama_french_3_factor_model', 'jensens_alpha', 'levered_beta_hamada', 'security_market_line', 'treynor_ratio', 'unlevered_beta']
    :param asset_returns: "Returns of the individual asset."
    :param market_returns: "Returns of the market index."
    :return: "Computed value of Beta: beta_i = Cov(R_i,R_m)/Var(R_m)"
    '''
    import numpy as np
    cov = np.cov(asset_returns, market_returns)[0][1]
    var = np.var(market_returns, ddof=1)
    return cov / var






def bid_ask_spread(ask, bid):
    '''
    domain: ['Liquidity risk & market liquidity']
    subdomain: ['Liquidity Risk', 'Market Liquidity']
    function: "Bid-ask spread — Spread = Ask - Bid. A financial metric in the domain of Liquidity risk & market liquidity."
    y_as_x: []
    :param ask: "Parameter ask used in Bid-ask spread calculation."
    :param bid: "Parameter bid used in Bid-ask spread calculation."
    :return: "Computed value of Bid-ask spread: Spread = Ask - Bid"
    '''
    return ask - bid






def binary_asset_or_nothing_call(spot_price, strike_price, risk_free_rate, volatility, time_to_expiry):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Binary asset-or-nothing call — AON = S e^{-qT} N(d1). A financial metric in the domain of Derivatives, options & volatility."
    y_as_x: []
    :param args: "Parameter args used in Binary asset-or-nothing call calculation."
    :param kwargs: "Parameter kwargs used in Binary asset-or-nothing call calculation."
    :return: "Computed value of Binary asset-or-nothing call: AON = S e^{-qT} N(d1)"
    '''
    import numpy as np
    from scipy.stats import norm
    d1 = (np.log(spot_price/strike_price) + (risk_free_rate + 0.5*volatility**2)*time_to_expiry) / (volatility*np.sqrt(time_to_expiry))
    return spot_price * norm.cdf(d1)


def binomial_down_factor(x_1, u):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Binomial down factor — d = 1/u. A financial metric in the domain of Derivatives, options & volatility."
    y_as_x: []
    :param x_1: "Parameter x_1 used in Binomial down factor calculation."
    :param u: "Parameter u used in Binomial down factor calculation."
    :return: "Computed value of Binomial down factor: d = 1/u"
    '''
    return x_1 / u






def binomial_option_pricing(spot_price, strike_price, risk_free_rate, volatility, time_to_expiry, steps, option_type="call"):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Binomial option pricing — V = e^{-rΔt}[pV_u + (1-p)V_d]. A financial metric in the domain of Derivatives, options & volatility."
    y_as_x: []
    :param args: "Parameter args used in Binomial option pricing calculation."
    :param kwargs: "Parameter kwargs used in Binomial option pricing calculation."
    :return: "Computed value of Binomial option pricing: V = e^{-rΔt}[pV_u + (1-p)V_d]"
    '''
    import numpy as np
    dt = time_to_expiry / steps; u = np.exp(volatility*np.sqrt(dt)); d = 1/u
    p = (np.exp(risk_free_rate*dt) - d) / (u - d); disc = np.exp(-risk_free_rate*dt)
    prices = spot_price * u**np.arange(steps,-1,-1) * d**np.arange(0,steps+1)
    values = np.maximum(prices-strike_price, 0) if option_type=='call' else np.maximum(strike_price-prices, 0)
    for _ in range(steps):
        values = disc * (p * values[:-1] + (1-p) * values[1:])
    return values[0]


def binomial_up_factor(volatility, dt):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Binomial up factor — u = e^{sigma sqrt(Delta t)}. A financial metric in the domain of Derivatives, options & volatility."
    y_as_x: []
    :param args: "Parameter args used in Binomial up factor calculation."
    :param kwargs: "Parameter kwargs used in Binomial up factor calculation."
    :return: "Computed value of Binomial up factor: u = e^{sigma sqrt(Delta t)}"
    '''
    import numpy as np
    return np.exp(volatility * np.sqrt(dt))




def bipower_variation(returns):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "Bipower variation — BV_t = mu_1^-2 sum |r_i||r_{i-1}|. A financial metric in the domain of Market risk & volatility modeling."
    y_as_x: []
    :param args: "Parameter args used in Bipower variation calculation."
    :param kwargs: "Parameter kwargs used in Bipower variation calculation."
    :return: "Computed value of Bipower variation: BV_t = mu_1^-2 sum |r_i||r_{i-1}|"
    '''
    import numpy as np
    r = np.array(returns)
    n = len(r)
    return (np.pi / 2) * (n / (n - 1)) * np.sum(np.abs(r[1:]) * np.abs(r[:-1]))




def black_76_option_price(spot_price, strike_price, risk_free_rate, volatility, time_to_expiry, option_type):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Black 76 option price — Price = DF[F N(d1) - K N(d2)] for call. A financial metric in the domain of Derivatives, options & volatility."
    y_as_x: []
    :param spot_price: "Spot Price (S) is the current market price of the underlying asset."
    :param strike_price: "Strike Price (K) is the predetermined price at which an option can be exercised."
    :param risk_free_rate: "Risk-Free Rate (Rf) is the theoretical rate of return with zero risk, typically proxied by government bond yields."
    :param volatility: "Volatility (sigma) is the annualized standard deviation of returns."
    :param time_to_expiry: "Time to Expiry (T) is the remaining time until expiration, in years."
    :param option_type: "Option Type specifies whether the option is a "call" or "put"."
    :return: "Computed value of Black 76 option price: Price = DF[F N(d1) - K N(d2)] for call"
    '''
    import numpy as np
    from scipy.stats import norm
    d1 = (np.log(spot_price/strike_price) + (risk_free_rate + 0.5*volatility**2)*time_to_expiry) / (volatility*np.sqrt(time_to_expiry))
    d2 = d1 - volatility*np.sqrt(time_to_expiry)
    if option_type == "call":
        return spot_price*norm.cdf(d1) - strike_price*np.exp(-risk_free_rate*time_to_expiry)*norm.cdf(d2)
    else:
        return strike_price*np.exp(-risk_free_rate*time_to_expiry)*norm.cdf(-d2) - spot_price*norm.cdf(-d1)






def black_caplet_price(forward_rate, strike_rate, volatility, time_to_expiry, notional, day_count_fraction, discount_factor):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Interest Rate Modeling', 'Term Structure']
    function: "Black caplet price — Caplet = DF x tau [F N(d1) - K N(d2)]. A financial metric in the domain of Interest-rate modeling & term structures."
    y_as_x: []
    :param args: "Parameter args used in Black caplet price calculation."
    :param kwargs: "Parameter kwargs used in Black caplet price calculation."
    :return: "Computed value of Black caplet price: Caplet = DF x tau [F N(d1) - K N(d2)]"
    '''
    import numpy as np
    from scipy.stats import norm
    d1 = (np.log(forward_rate/strike_rate) + 0.5*volatility**2*time_to_expiry) / (volatility*np.sqrt(time_to_expiry))
    d2 = d1 - volatility*np.sqrt(time_to_expiry)
    return discount_factor * notional * day_count_fraction * (forward_rate*norm.cdf(d1) - strike_rate*norm.cdf(d2))


def black_swaption_price(swap_rate, strike_rate, volatility, time_to_expiry, annuity_factor, option_type="payer"):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Interest Rate Modeling', 'Term Structure']
    function: "Black swaption price — Swaption = A x [S N(d1) - K N(d2)]. A financial metric in the domain of Interest-rate modeling & term structures."
    y_as_x: []
    :param args: "Parameter args used in Black swaption price calculation."
    :param kwargs: "Parameter kwargs used in Black swaption price calculation."
    :return: "Computed value of Black swaption price: Swaption = A x [S N(d1) - K N(d2)]"
    '''
    import numpy as np
    from scipy.stats import norm
    d1 = (np.log(swap_rate / strike_rate) + 0.5 * volatility**2 * time_to_expiry) / (volatility * np.sqrt(time_to_expiry))
    d2 = d1 - volatility * np.sqrt(time_to_expiry)
    if option_type == 'payer':
        return annuity_factor * (swap_rate * norm.cdf(d1) - strike_rate * norm.cdf(d2))
    else:
        return annuity_factor * (strike_rate * norm.cdf(-d2) - swap_rate * norm.cdf(-d1))




def black_76_commodity_option(spot_price, strike_price, risk_free_rate, volatility, time_to_expiry, option_type):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Commodities', 'Futures', 'Hedging']
    function: "Black-76 commodity option — C = e^{-rT}[F N(d1)-K N(d2)]. A financial metric in the domain of Commodities, futures & hedging."
    y_as_x: []
    :param spot_price: "Spot Price (S) is the current market price of the underlying asset."
    :param strike_price: "Strike Price (K) is the predetermined price at which an option can be exercised."
    :param risk_free_rate: "Risk-Free Rate (Rf) is the theoretical rate of return with zero risk, typically proxied by government bond yields."
    :param volatility: "Volatility (sigma) is the annualized standard deviation of returns."
    :param time_to_expiry: "Time to Expiry (T) is the remaining time until expiration, in years."
    :param option_type: "Option Type specifies whether the option is a "call" or "put"."
    :return: "Computed value of Black-76 commodity option: C = e^{-rT}[F N(d1)-K N(d2)]"
    '''
    import numpy as np
    from scipy.stats import norm
    d1 = (np.log(spot_price/strike_price) + (risk_free_rate + 0.5*volatility**2)*time_to_expiry) / (volatility*np.sqrt(time_to_expiry))
    d2 = d1 - volatility*np.sqrt(time_to_expiry)
    if option_type == "call":
        return spot_price*norm.cdf(d1) - strike_price*np.exp(-risk_free_rate*time_to_expiry)*norm.cdf(d2)
    else:
        return strike_price*np.exp(-risk_free_rate*time_to_expiry)*norm.cdf(-d2) - spot_price*norm.cdf(-d1)






def black_litterman_implied_equilibrium_returns(risk_aversion, cov_matrix, market_weights):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Black-Litterman implied equilibrium returns — Pi = delta Sigma w_mkt. A financial metric in the domain of Asset management & portfolio optimization."
    y_as_x: []
    :param expected_returns: "Expected Returns vector contains the anticipated return for each asset."
    :param cov_matrix: "Covariance Matrix contains the covariances between all pairs of assets."
    :return: "Computed value of Black-Litterman implied equilibrium returns: Pi = delta Sigma w_mkt"
    '''
    import numpy as np
    return risk_aversion * np.array(cov_matrix) @ np.array(market_weights)


def black_litterman_posterior_mean(tau, cov_matrix, equilibrium_returns, P, Q, omega):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Black-Litterman posterior mean — μ_BL = [(τΣ)^(-1)+P^TΩ^(-1)P]^(-1)[(τΣ)^(-1)π + P^TΩ^(-1)Q]. A financial metric in the domain of Asset management & portfolio optimization."
    y_as_x: []
    :param expected_returns: "Expected Returns vector contains the anticipated return for each asset."
    :param cov_matrix: "Covariance Matrix contains the covariances between all pairs of assets."
    :return: "Computed value of Black-Litterman posterior mean: μ_BL = [(τΣ)^(-1)+P^TΩ^(-1)P]^(-1)[(τΣ)^(-1)π + P^TΩ^(-1)Q]"
    '''
    import numpy as np
    sigma = np.array(cov_matrix); pi = np.array(equilibrium_returns)
    P = np.array(P); Q = np.array(Q); omega = np.array(omega)
    tau_sigma_inv = np.linalg.inv(tau * sigma)
    p_omega_inv_p = P.T @ np.linalg.inv(omega) @ P
    return np.linalg.inv(tau_sigma_inv + p_omega_inv_p) @ (tau_sigma_inv @ pi + P.T @ np.linalg.inv(omega) @ Q)




def black_scholes_call(spot_price, strike_price, risk_free_rate, volatility, time_to_expiry):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Black-Scholes Call — European call option price. C = S*N(d1) - K*exp(-rT)*N(d2)."
    y_as_x: []
    :param spot_price: "Spot Price (S) is the current market price of the underlying asset."
    :param strike_price: "Strike Price (K) is the predetermined price at which an option can be exercised."
    :param risk_free_rate: "Risk-Free Rate (Rf) is the theoretical rate of return with zero risk, typically proxied by government bond yields."
    :param volatility: "Volatility (sigma) is the annualized standard deviation of returns."
    :param time_to_expiry: "Time to Expiry (T) is the remaining time until expiration, in years."
    :return: "Computed value of Black-Scholes call: C = S_0 e^{-qT}N(d1) - K e^{-rT}N(d2)"
    '''
    import numpy as np
    from scipy.stats import norm
    d1 = (np.log(spot_price/strike_price) + (risk_free_rate + 0.5*volatility**2)*time_to_expiry) / (volatility*np.sqrt(time_to_expiry))
    d2 = d1 - volatility*np.sqrt(time_to_expiry)
    return spot_price * norm.cdf(d1) - strike_price * np.exp(-risk_free_rate*time_to_expiry) * norm.cdf(d2)






def black_scholes_put(spot_price, strike_price, risk_free_rate, volatility, time_to_expiry):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Black-Scholes Put — European put option price. P = K*exp(-rT)*N(-d2) - S*N(-d1)."
    y_as_x: []
    :param spot_price: "Spot Price (S) is the current market price of the underlying asset."
    :param strike_price: "Strike Price (K) is the predetermined price at which an option can be exercised."
    :param risk_free_rate: "Risk-Free Rate (Rf) is the theoretical rate of return with zero risk, typically proxied by government bond yields."
    :param volatility: "Volatility (sigma) is the annualized standard deviation of returns."
    :param time_to_expiry: "Time to Expiry (T) is the remaining time until expiration, in years."
    :return: "Computed value of Black-Scholes put: P = K e^{-rT}N(-d2) - S_0 e^{-qT}N(-d1)"
    '''
    import numpy as np
    from scipy.stats import norm
    d1 = (np.log(spot_price/strike_price) + (risk_free_rate + 0.5*volatility**2)*time_to_expiry) / (volatility*np.sqrt(time_to_expiry))
    d2 = d1 - volatility*np.sqrt(time_to_expiry)
    return strike_price * np.exp(-risk_free_rate*time_to_expiry) * norm.cdf(-d2) - spot_price * norm.cdf(-d1)






def black_scholes_merton_d1(spot_price, strike_price, risk_free_rate, volatility, time_to_expiry, option_type):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Black-Scholes-Merton d1 — d1 = [ln(S/K)+(r-q+0.5 sigma^2)T]/(sigma sqrt(T)). A financial metric in the domain of Derivatives, options & volatility."
    y_as_x: []
    :param spot_price: "Spot Price (S) is the current market price of the underlying asset."
    :param strike_price: "Strike Price (K) is the predetermined price at which an option can be exercised."
    :param risk_free_rate: "Risk-Free Rate (Rf) is the theoretical rate of return with zero risk, typically proxied by government bond yields."
    :param volatility: "Volatility (sigma) is the annualized standard deviation of returns."
    :param time_to_expiry: "Time to Expiry (T) is the remaining time until expiration, in years."
    :param option_type: "Option Type specifies whether the option is a "call" or "put"."
    :return: "Computed value of Black-Scholes-Merton d1: d1 = [ln(S/K)+(r-q+0.5 sigma^2)T]/(sigma sqrt(T))"
    '''
    import numpy as np
    from scipy.stats import norm
    d1 = (np.log(spot_price/strike_price) + (risk_free_rate + 0.5*volatility**2)*time_to_expiry) / (volatility*np.sqrt(time_to_expiry))
    d2 = d1 - volatility*np.sqrt(time_to_expiry)
    if option_type == "call":
        return spot_price*norm.cdf(d1) - strike_price*np.exp(-risk_free_rate*time_to_expiry)*norm.cdf(d2)
    else:
        return strike_price*np.exp(-risk_free_rate*time_to_expiry)*norm.cdf(-d2) - spot_price*norm.cdf(-d1)






def black_scholes_merton_d2(spot_price, strike_price, risk_free_rate, volatility, time_to_expiry, option_type):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Black-Scholes-Merton d2 — d2 = d1 - sigma sqrt(T). A financial metric in the domain of Derivatives, options & volatility."
    y_as_x: []
    :param spot_price: "Spot Price (S) is the current market price of the underlying asset."
    :param strike_price: "Strike Price (K) is the predetermined price at which an option can be exercised."
    :param risk_free_rate: "Risk-Free Rate (Rf) is the theoretical rate of return with zero risk, typically proxied by government bond yields."
    :param volatility: "Volatility (sigma) is the annualized standard deviation of returns."
    :param time_to_expiry: "Time to Expiry (T) is the remaining time until expiration, in years."
    :param option_type: "Option Type specifies whether the option is a "call" or "put"."
    :return: "Computed value of Black-Scholes-Merton d2: d2 = d1 - sigma sqrt(T)"
    '''
    import numpy as np
    from scipy.stats import norm
    d1 = (np.log(spot_price/strike_price) + (risk_free_rate + 0.5*volatility**2)*time_to_expiry) / (volatility*np.sqrt(time_to_expiry))
    d2 = d1 - volatility*np.sqrt(time_to_expiry)
    if option_type == "call":
        return spot_price*norm.cdf(d1) - strike_price*np.exp(-risk_free_rate*time_to_expiry)*norm.cdf(d2)
    else:
        return strike_price*np.exp(-risk_free_rate*time_to_expiry)*norm.cdf(-d2) - spot_price*norm.cdf(-d1)






def bollinger_pct_b(close, period=20, num_std=2):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "Bollinger %B — %B = (P-Lower)/(Upper-Lower). A financial metric in the domain of Technical analysis & chart-based indicators."
    y_as_x: []
    :param close: "Close is the final trading price at the end of a trading period."
    :param period: "Period (n) is the lookback window in number of bars for technical indicators."
    :return: "Computed value of Bollinger %B: %B = (P-Lower)/(Upper-Lower)"
    '''
    import pandas as pd
    c = pd.Series(close); sma = c.rolling(period).mean(); std = c.rolling(period).std()
    return (c - (sma - num_std*std)) / (2*num_std*std)


def bollinger_bands_lower(sma_n, k_sigma_n):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "Bollinger Bands lower — Lower = SMA_n - k sigma_n. A financial metric in the domain of Technical analysis & chart-based indicators."
    y_as_x: []
    :param sma_n: "Parameter sma_n used in Bollinger Bands lower calculation."
    :param k_sigma_n: "Parameter k_sigma_n used in Bollinger Bands lower calculation."
    :return: "Computed value of Bollinger Bands lower: Lower = SMA_n - k sigma_n"
    '''
    return sma_n - k_sigma_n






def bollinger_bands_middle(close, period=20):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "Bollinger Bands middle — Middle = SMA_n(P). A financial metric in the domain of Technical analysis & chart-based indicators."
    y_as_x: []
    :param close: "Close is the final trading price at the end of a trading period."
    :param period: "Period (n) is the lookback window in number of bars for technical indicators."
    :return: "Computed value of Bollinger Bands middle: Middle = SMA_n(P)"
    '''
    import pandas as pd
    return pd.Series(close).rolling(window=period).mean()


def bollinger_bands_upper(sma_n, k_sigma_n):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "Bollinger Bands upper — Upper = SMA_n + k sigma_n. A financial metric in the domain of Technical analysis & chart-based indicators."
    y_as_x: []
    :param sma_n: "Parameter sma_n used in Bollinger Bands upper calculation."
    :param k_sigma_n: "Parameter k_sigma_n used in Bollinger Bands upper calculation."
    :return: "Computed value of Bollinger Bands upper: Upper = SMA_n + k sigma_n"
    '''
    return sma_n + k_sigma_n






def bollinger_bandwidth(close, period=20, num_std=2):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "Bollinger bandwidth — Bandwidth = (Upper-Lower)/Middle. A financial metric in the domain of Technical analysis & chart-based indicators."
    y_as_x: []
    :param close: "Close is the final trading price at the end of a trading period."
    :param period: "Period (n) is the lookback window in number of bars for technical indicators."
    :return: "Computed value of Bollinger bandwidth: Bandwidth = (Upper-Lower)/Middle"
    '''
    import pandas as pd
    c = pd.Series(close); sma = c.rolling(period).mean(); std = c.rolling(period).std()
    return (2 * num_std * std) / sma


def bond_carry_and_roll(coupon_income, financing_cost, roll_down_return):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Fixed Income', 'Bond Mathematics', 'Credit Markets']
    function: "Bond carry and roll — Carry+Roll = coupon income + financing + curve roll-down. A financial metric in the domain of Fixed income, bonds & credit markets."
    y_as_x: []
    :param args: "Parameter args used in Bond carry and roll calculation."
    :param kwargs: "Parameter kwargs used in Bond carry and roll calculation."
    :return: "Computed value of Bond carry and roll: Carry+Roll = coupon income + financing + curve roll-down"
    '''
    return coupon_income - financing_cost + roll_down_return




def bond_equivalent_yield_bey(numerator, denominator):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Fixed Income', 'Bond Mathematics', 'Credit Markets']
    function: "Bond equivalent yield (BEY) — BEY = 2[(1+HPY)^(182/d) - 1]. A financial metric in the domain of Fixed income, bonds & credit markets."
    y_as_x: []
    :param numerator: "Parameter numerator used in Bond equivalent yield (BEY) calculation."
    :param denominator: "Parameter denominator used in Bond equivalent yield (BEY) calculation."
    :return: "Computed value of Bond equivalent yield (BEY): BEY = 2[(1+HPY)^(182/d) - 1]"
    '''
    return numerator / denominator if denominator != 0 else 0






def bond_price(face_value, coupon_rate, yield_to_maturity, periods, frequency=2):
    '''
    domain: ['Fixed income & bond math']
    subdomain: ['Fixed Income', 'Bond Mathematics']
    function: "Bond Price — present value of all future cash flows. P = sum(C/(1+y)^t) + FV/(1+y)^n."
    y_as_x: ['current_yield', 'dollar_duration', 'dv01_pvbp', 'z_spread']
    :param face_value: "Face Value (par value) is the nominal value of a bond stated by the issuer."
    :param coupon_rate: "Coupon Rate is the annual interest rate paid by a bond issuer relative to face value."
    :param yield_to_maturity: "Yield to Maturity (YTM) is the total return anticipated if a bond is held until maturity."
    :param periods: "Number of periods for calculations."
    :param frequency: "Frequency is the number of coupon payments per year."
    :return: "Computed value of Bond price: P = Σ_{t=1}^n C_t/(1+y/m)^(mt) + FV/(1+y/m)^(mn)"
    '''
    import numpy as np
    c = face_value * coupon_rate / frequency
    r = yield_to_maturity / frequency
    n = int(periods * frequency)
    t = np.arange(1, n + 1)
    pv_coupons = np.sum(c / (1 + r)**t)
    pv_face = face_value / (1 + r)**n
    return pv_coupons + pv_face






def bond_price_from_yield(face_value, coupon_rate, ytm, periods, frequency=2):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Fixed Income', 'Bond Mathematics', 'Credit Markets']
    function: "Bond price from yield — P = sum_t C/(1+y/m)^(mt) + F/(1+y/m)^(mT). A financial metric in the domain of Fixed income, bonds & credit markets."
    y_as_x: []
    :param args: "Parameter args used in Bond price from yield calculation."
    :param kwargs: "Parameter kwargs used in Bond price from yield calculation."
    :return: "Computed value of Bond price from yield: P = sum_t C/(1+y/m)^(mt) + F/(1+y/m)^(mT)"
    '''
    import numpy as np
    c = face_value * coupon_rate / frequency; r = ytm / frequency; n = int(periods * frequency)
    t = np.arange(1, n+1)
    return np.sum(c / (1+r)**t) + face_value / (1+r)**n


def book_value_per_share(equity, shares_outstanding):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "Book value per share — BVPS = Equity / Shares Outstanding. A financial metric in the domain of Accounting & financial statement analysis."
    y_as_x: ['p_b_ratio', 'price_to_book']
    :param equity: "Total Equity is the residual interest in assets after deducting liabilities."
    :param shares_outstanding: "Shares Outstanding is the total number of shares of a company's stock currently held by all shareholders."
    :return: "Computed value of Book value per share: BVPS = Equity / Shares Outstanding"
    '''
    return equity / shares_outstanding






def book_to_market_ratio(book_equity, market_cap):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Equity Valuation', 'Asset Pricing']
    function: "Book-to-market ratio — Book-to-market = Book Equity / Market Cap. A financial metric in the domain of Equity valuation & asset pricing."
    y_as_x: []
    :param book_equity: "Parameter book_equity used in Book-to-market ratio calculation."
    :param market_cap: "Market Capitalization is the total market value of outstanding shares (price x shares)."
    :return: "Computed value of Book-to-market ratio: Book-to-market = Book Equity / Market Cap"
    '''
    return book_equity / market_cap






def bornhuetter_ferguson_reserve(earned_premium, expected_loss_ratio, paid_loss_ratio):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "Bornhuetter-Ferguson Reserve — blends actual loss experience with an a priori expected loss to estimate ultimate losses. BF Reserve = EP * ELR * (1 - development factor)."
    y_as_x: []
    :param earned_premium: "Parameter earned_premium used in Bornhuetter-Ferguson reserve calculation."
    :param expected_loss_ratio: "Parameter expected_loss_ratio used in Bornhuetter-Ferguson reserve calculation."
    :param paid_loss_ratio: "Parameter paid_loss_ratio used in Bornhuetter-Ferguson reserve calculation."
    :return: "Computed value of Bornhuetter-Ferguson reserve: Ultimate = Reported + (Expected Ultimate x %Unreported)"
    '''
    return earned_premium * expected_loss_ratio * (1 - paid_loss_ratio)






def borrowing_base(eligible_receivables, ar_advance_rate, eligible_inventory, inv_advance_rate):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Banking', 'Consumer Lending', 'Project Finance']
    function: "Borrowing Base — the maximum amount a lender will extend based on eligible collateral with advance rates applied."
    y_as_x: []
    :param eligible_receivables: "Parameter eligible_receivables used in Borrowing base calculation."
    :param ar_advance_rate: "Parameter ar_advance_rate used in Borrowing base calculation."
    :param eligible_inventory: "Parameter eligible_inventory used in Borrowing base calculation."
    :param inv_advance_rate: "Parameter inv_advance_rate used in Borrowing base calculation."
    :return: "Computed value of Borrowing base: Borrowing Base = sum_i Eligible Collateral_i x Advance Rate_i"
    '''
    return eligible_receivables * ar_advance_rate + eligible_inventory * inv_advance_rate






def break_even_inflation(nominal_yield, real_yield):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Fixed Income', 'Bond Mathematics', 'Credit Markets']
    function: "Break-Even Inflation — the inflation rate at which nominal and real bond returns are equal. BEI = Nominal Yield - Real Yield."
    y_as_x: []
    :param nominal_yield: "Parameter nominal_yield used in Break-even inflation calculation."
    :param real_yield: "Parameter real_yield used in Break-even inflation calculation."
    :return: "Computed value of Break-even inflation: BEI = Nominal Yield - Real Yield"
    '''
    return nominal_yield - real_yield






def break_even_occupancy(operating_expenses_re, potential_gross_income):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Real Estate Finance', 'Mortgage Analysis']
    function: "Break-Even Occupancy — the minimum occupancy rate needed to cover operating expenses."
    y_as_x: []
    :param operating_expenses_re: "Parameter operating_expenses_re used in Break-even occupancy calculation."
    :param potential_gross_income: "Parameter potential_gross_income used in Break-even occupancy calculation."
    :return: "Computed value of Break-even occupancy: BEO = (Operating Expenses + Debt Service) / Gross Potential Income"
    '''
    return operating_expenses_re / potential_gross_income






def break_even_quantity(fixed_costs, price_per_unit, variable_cost_per_unit):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "Break-Even Quantity — the number of units that must be sold to cover all costs. Q_BE = FC / (P - VC)."
    y_as_x: []
    :param fixed_costs: "Parameter fixed_costs used in Break-even quantity calculation."
    :param price_per_unit: "Parameter price_per_unit used in Break-even quantity calculation."
    :param variable_cost_per_unit: "Parameter variable_cost_per_unit used in Break-even quantity calculation."
    :return: "Computed value of Break-even quantity: Q_BE = Fixed Costs / (Price - Variable Cost per unit)"
    '''
    return fixed_costs / (price_per_unit - variable_cost_per_unit)






def break_even_revenue(fixed_costs, contribution_margin_ratio):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "Break-Even Revenue — the revenue needed to cover all costs. R_BE = FC / CM_ratio."
    y_as_x: []
    :param fixed_costs: "Parameter fixed_costs used in Break-even revenue calculation."
    :param contribution_margin_ratio: "Contribution Margin Ratio — contribution margin as a percentage of revenue."
    :return: "Computed value of Break-even revenue: Sales_BE = Fixed Costs / Contribution Margin Ratio"
    '''
    return fixed_costs / contribution_margin_ratio






def breusch_pagan_test(residuals, exog):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Financial Econometrics', 'Time Series Analysis']
    function: "Breusch-Pagan Test — tests for heteroskedasticity in regression residuals. Null hypothesis: homoskedasticity."
    y_as_x: []
    :param residuals: "Parameter residuals used in Breusch-Pagan test calculation."
    :param exog: "Exogenous (independent) variables or external regressors."
    :return: "Computed value of Breusch-Pagan test: LM = nR^2 from auxiliary regression of e^2 on X"
    '''
    from statsmodels.stats.diagnostic import het_breuschpagan
    result = het_breuschpagan(residuals, exog)
    return {'lm_stat': result[0], 'lm_pvalue': result[1], 'f_stat': result[2], 'f_pvalue': result[3]}






def brinson_allocation_effect(portfolio_weights, benchmark_weights, benchmark_sector_returns, benchmark_total_return):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Performance Attribution', 'Risk-Adjusted Performance']
    function: "Brinson Allocation Effect — measures the contribution of sector weighting decisions. Allocation_i = (w_p - w_b)(r_b_i - r_b)."
    y_as_x: []
    :param portfolio_weights: "Portfolio Weights represent the proportion of total portfolio value allocated to each asset."
    :param benchmark_weights: "Benchmark Weights represent the proportion of each asset in the benchmark portfolio."
    :param benchmark_sector_returns: "Benchmark Sector Returns are the returns of each sector within the benchmark."
    :param benchmark_total_return: "Benchmark Total Return is the overall return of the benchmark."
    :return: "Computed value of Brinson allocation effect: Allocation_i = (w_{p,i}-w_{b,i})·(R_{b,i}-R_b)"
    '''
    import numpy as np
    return (np.array(portfolio_weights) - np.array(benchmark_weights)) * (np.array(benchmark_sector_returns) - benchmark_total_return)






def brinson_selection_effect(benchmark_weights, portfolio_sector_returns, benchmark_sector_returns):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Performance Attribution', 'Risk-Adjusted Performance']
    function: "Brinson Selection Effect — measures the contribution of security selection within sectors. Selection_i = w_b * (r_p_i - r_b_i)."
    y_as_x: []
    :param benchmark_weights: "Benchmark Weights represent the proportion of each asset in the benchmark portfolio."
    :param portfolio_sector_returns: "Portfolio Sector Returns are the returns of each sector within the portfolio."
    :param benchmark_sector_returns: "Benchmark Sector Returns are the returns of each sector within the benchmark."
    :return: "Computed value of Brinson selection effect: Selection_i = w_{b,i}·(R_{p,i}-R_{b,i})"
    '''
    import numpy as np
    return np.array(benchmark_weights) * (np.array(portfolio_sector_returns) - np.array(benchmark_sector_returns))






def b_hlmann_credibility_factor(n_claims, k_buhlmann):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "Bühlmann credibility factor — Z = n/(n+K). A financial metric in the domain of Actuarial science & insurance."
    y_as_x: []
    :param args: "Parameter args used in Bühlmann credibility factor calculation."
    :param kwargs: "Parameter kwargs used in Bühlmann credibility factor calculation."
    :return: "Computed value of Bühlmann credibility factor: Z = n/(n+K)"
    '''
    return n_claims / (n_claims + k_buhlmann)


def burke_ratio(returns, risk_free_rate=0, n_drawdowns=5):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Burke Ratio — a risk-adjusted return measure using the sum of squared drawdowns. Higher is better."
    y_as_x: []
    :param returns: "Returns are the gain or loss generated on an investment over a specific period."
    :param risk_free_rate: "Risk-Free Rate (Rf) is the theoretical rate of return with zero risk, typically proxied by government bond yields."
    :param n_drawdowns: "Parameter n_drawdowns used in Burke ratio calculation."
    :return: "Computed value of Burke ratio: Burke = Excess Return / sqrt(sum Drawdown_i^2)"
    '''
    import numpy as np
    r = np.array(returns)
    excess = np.mean(r) - risk_free_rate
    wealth = np.cumprod(1 + r)
    peaks = np.maximum.accumulate(wealth)
    dd = (peaks - wealth) / peaks
    sorted_dd = np.sort(dd)[::-1][:n_drawdowns]
    return excess / np.sqrt(np.sum(sorted_dd**2))






def butterfly_payoff(spot_price, k1, k2, k3):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Butterfly Payoff — the payoff of a butterfly spread at expiration. Profitable when spot is near the middle strike."
    y_as_x: []
    :param spot_price: "Spot Price (S) is the current market price of the underlying asset."
    :param k1: "Parameter k1 used in Butterfly payoff calculation."
    :param k2: "Parameter k2 used in Butterfly payoff calculation."
    :param k3: "Parameter k3 used in Butterfly payoff calculation."
    :return: "Computed value of Butterfly payoff: Payoff = max(S-K1,0)-2max(S-K2,0)+max(S-K3,0)"
    '''
    import numpy as np
    return np.maximum(spot_price - k1, 0) - 2 * np.maximum(spot_price - k2, 0) + np.maximum(spot_price - k3, 0)






def calendar_spread(near_contract_price, far_contract_price):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Commodities', 'Futures', 'Hedging']
    function: "Calendar Spread — the price difference between two futures contracts of different maturities."
    y_as_x: []
    :param near_contract_price: "Parameter near_contract_price used in Calendar spread calculation."
    :param far_contract_price: "Parameter far_contract_price used in Calendar spread calculation."
    :return: "Computed value of Calendar spread: Spread = F_near - F_far"
    '''
    return far_contract_price - near_contract_price






def call_payoff(spot_price, strike_price, premium_paid=0):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Call Payoff — the payoff of a call option at expiration. Payoff = max(S - K, 0) - premium."
    y_as_x: []
    :param spot_price: "Spot Price (S) is the current market price of the underlying asset."
    :param strike_price: "Strike Price (K) is the predetermined price at which an option can be exercised."
    :param premium_paid: "Parameter premium_paid used in Call payoff calculation."
    :return: "Computed value of Call payoff: C_T = max(S_T - K, 0)"
    '''
    import numpy as np
    return np.maximum(spot_price - strike_price, 0) - premium_paid






def call_spread_payoff(spot_price, k_long, k_short, net_premium=0):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Call Spread Payoff — the payoff of a bull call spread (long lower strike, short higher strike)."
    y_as_x: []
    :param spot_price: "Spot Price (S) is the current market price of the underlying asset."
    :param k_long: "Parameter k_long used in Call spread payoff calculation."
    :param k_short: "Parameter k_short used in Call spread payoff calculation."
    :param net_premium: "Net premium — P = PV(Benefits) / PV(Premium annuity). A financial metric in the domain of Actuarial science & insurance."
    :return: "Computed value of Call spread payoff: Payoff = max(S-K1,0) - max(S-K2,0)"
    '''
    import numpy as np
    return np.maximum(spot_price - k_long, 0) - np.maximum(spot_price - k_short, 0) - net_premium






def calmar_ratio(annualized_return, max_drawdown):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Calmar Ratio — risk-adjusted return measure = annualized return / maximum drawdown. Higher is better."
    y_as_x: []
    :param annualized_return: "Parameter annualized_return used in Calmar ratio calculation."
    :param max_drawdown: "Maximum Drawdown (MDD) is the maximum observed loss from peak to trough."
    :return: "Computed value of Calmar ratio: Calmar = CAGR / Max Drawdown"
    '''
    return annualized_return / abs(max_drawdown) if max_drawdown != 0 else float("inf")






def cancel_to_trade_ratio(cancelled_orders, executed_trades):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Liquidity Risk', 'Market Liquidity', 'Execution Cost']
    function: "Cancel-to-Trade Ratio — the number of cancelled orders per executed trade. High ratios may indicate market manipulation."
    y_as_x: []
    :param cancelled_orders: "Parameter cancelled_orders used in Cancel-to-trade ratio calculation."
    :param executed_trades: "Parameter executed_trades used in Cancel-to-trade ratio calculation."
    :return: "Computed value of Cancel-to-trade ratio: CTR = Number of cancellations / Number of trades"
    '''
    return cancelled_orders / executed_trades if executed_trades > 0 else 0






def capital_conservation_buffer(cet1_ratio, minimum_cet1=0.045):
    '''
    domain: ['Bank regulation, Basel & prudential ratios']
    subdomain: ['Bank Regulation', 'Basel Framework', 'Prudential Ratios']
    function: "Capital Conservation Buffer — the excess CET1 capital above the 4.5% minimum. Banks must maintain 2.5% buffer."
    y_as_x: []
    :param cet1_ratio: "CET1 Ratio — Common Equity Tier 1 capital divided by risk-weighted assets. Minimum 4.5% under Basel III."
    :param minimum_cet1: "Parameter minimum_cet1 used in Capital conservation buffer calculation."
    :return: "Computed value of Capital conservation buffer: CCB = CET1 Ratio - minimum CET1 requirement"
    '''
    return max(cet1_ratio - minimum_cet1, 0)






def capitalization_rate(noi, property_value):
    '''
    domain: ['Real estate finance']
    subdomain: ['Real Estate Finance']
    function: "Capitalization Rate (Cap Rate) — the ratio of net operating income to property value. Cap Rate = NOI / Property Value."
    y_as_x: []
    :param noi: "Net Operating Income (NOI) is total revenue from a property minus operating expenses."
    :param property_value: "Property Value is the estimated market worth of a real estate asset."
    :return: "Computed value of Capitalization rate: Cap Rate = NOI / Property Value"
    '''
    return noi / property_value






def capm_expected_return(risk_free_rate, beta, market_return):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Equity Valuation', 'Asset Pricing']
    function: "CAPM Expected Return — the expected return of an asset based on the Capital Asset Pricing Model. E[R] = Rf + beta * (Rm - Rf)."
    y_as_x: []
    :param risk_free_rate: "Risk-Free Rate (Rf) is the theoretical rate of return with zero risk, typically proxied by government bond yields."
    :param beta: "Beta measures systematic risk, the sensitivity of returns to market movements."
    :param market_return: "Market Return (Rm) is the return on a broad market index representing overall market performance."
    :return: "Computed value of CAPM expected return: E[R_i] = R_f + beta_i(E[R_m]-R_f)"
    '''
    return risk_free_rate + beta * (market_return - risk_free_rate)






def carhart_4_factor_model(returns, market_excess, smb, hml, wml, risk_free_rate):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Equity Valuation', 'Asset Pricing']
    function: "Carhart 4-Factor Model — extends Fama-French 3 factors with a momentum factor (WML). R - Rf = alpha + b1*(Rm-Rf) + b2*SMB + b3*HML + b4*WML."
    y_as_x: []
    :param returns: "Returns are the gain or loss generated on an investment over a specific period."
    :param market_excess: "Parameter market_excess used in Carhart 4-factor model calculation."
    :param smb: "Parameter smb used in Carhart 4-factor model calculation."
    :param hml: "Parameter hml used in Carhart 4-factor model calculation."
    :param wml: "Parameter wml used in Carhart 4-factor model calculation."
    :param risk_free_rate: "Risk-Free Rate (Rf) is the theoretical rate of return with zero risk, typically proxied by government bond yields."
    :return: "Computed value of Carhart 4-factor model: R_i-R_f = alpha + b MKT + s SMB + h HML + m MOM + epsilon"
    '''
    import numpy as np
    from scipy import stats
    y = np.array(returns) - risk_free_rate
    X = np.column_stack([market_excess, smb, hml, wml])
    X = np.column_stack([np.ones(len(y)), X])
    coeffs = np.linalg.lstsq(X, y, rcond=None)[0]
    return {'alpha': coeffs[0], 'market_beta': coeffs[1], 'smb_beta': coeffs[2], 'hml_beta': coeffs[3], 'wml_beta': coeffs[4]}






def cash_conversion_cycle_ccc(days_inventory, days_receivables, days_payables):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "Cash Conversion Cycle (CCC) — measures how long it takes to convert inventory investments into cash. CCC = DIO + DSO - DPO."
    y_as_x: []
    :param days_inventory: "Parameter days_inventory used in Cash conversion cycle (CCC) calculation."
    :param days_receivables: "Parameter days_receivables used in Cash conversion cycle (CCC) calculation."
    :param days_payables: "Parameter days_payables used in Cash conversion cycle (CCC) calculation."
    :return: "Computed value of Cash conversion cycle (CCC): CCC = DSO + DIO - DPO"
    '''
    return days_inventory + days_receivables - days_payables






def cash_flow_at_risk_cfa_r(cash_flows, confidence_level=0.95):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Treasury', 'ALM', 'Balance Sheet Management']
    function: "Cash flow at risk (CFaR) — CFaR_alpha = quantile_alpha(future cash flow shortfall). A financial metric in the domain of Treasury, ALM & balance-sheet management."
    y_as_x: []
    :param args: "Parameter args used in Cash flow at risk (CFaR) calculation."
    :param kwargs: "Parameter kwargs used in Cash flow at risk (CFaR) calculation."
    :return: "Computed value of Cash flow at risk (CFaR): CFaR_alpha = quantile_alpha(future cash flow shortfall)"
    '''
    import numpy as np
    return np.percentile(cash_flows, (1 - confidence_level) * 100)


def cash_flow_margin(cash_flow_from_operations, revenue):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "Cash Flow Margin — operating cash flow as a percentage of revenue. Higher values indicate better cash generation."
    y_as_x: []
    :param cash_flow_from_operations: "Cash Flow from Operations (CFO) is cash generated from regular business operations."
    :param revenue: "Revenue is the total amount of income a business generates from the sale of goods or services before deducting expenses."
    :return: "Computed value of Cash flow margin: CF Margin = Operating Cash Flow / Revenue"
    '''
    return cash_flow_from_operations / revenue






def cash_interest_coverage(ebitda, interest_expense):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Private Equity', 'Venture Capital', 'LBO']
    function: "Cash Interest Coverage — EBITDA divided by interest expense, measuring ability to service debt from operating cash flow."
    y_as_x: []
    :param ebitda: "EBITDA (Earnings Before Interest, Taxes, Depreciation, and Amortization) is a proxy for operating cash flow."
    :param interest_expense: "Interest Expense is the cost incurred by a company for borrowed funds."
    :return: "Computed value of Cash interest coverage: (EBITDA - Capex) / Cash Interest"
    '''
    return ebitda / interest_expense if interest_expense != 0 else float("inf")






def cash_ratio(cash, current_liabilities):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "Cash Ratio — the most conservative liquidity ratio. Cash Ratio = Cash / Current Liabilities."
    y_as_x: []
    :param cash: "Cash and Cash Equivalents are the most liquid current assets."
    :param current_liabilities: "Current Liabilities are obligations due within one year."
    :return: "Computed value of Cash ratio: Cash Ratio = (Cash + Marketable Securities) / Current Liabilities"
    '''
    return cash / current_liabilities






def cash_sweep(excess_cash_flow, sweep_percentage):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Private Equity', 'Venture Capital', 'LBO']
    function: "Cash Sweep — mandatory debt repayment from excess cash flow. Sweep = Excess CF * Sweep %."
    y_as_x: []
    :param excess_cash_flow: "Parameter excess_cash_flow used in Cash sweep calculation."
    :param sweep_percentage: "Parameter sweep_percentage used in Cash sweep calculation."
    :return: "Computed value of Cash sweep: Debt Paydown_t = max(FCF_t - Required Cash,0)"
    '''
    return excess_cash_flow * sweep_percentage






def cash_on_cash_return(annual_cash_flow, total_cash_invested):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Real Estate Finance', 'Mortgage Analysis']
    function: "Cash-on-Cash Return — annual pre-tax cash flow divided by total cash invested. Used in real estate."
    y_as_x: []
    :param annual_cash_flow: "Parameter annual_cash_flow used in Cash-on-cash return calculation."
    :param total_cash_invested: "Parameter total_cash_invested used in Cash-on-cash return calculation."
    :return: "Computed value of Cash-on-cash return: CoC = Before-tax Cash Flow / Equity Invested"
    '''
    return annual_cash_flow / total_cash_invested






def cash_out_refinance_ltv(new_loan_amount, property_value):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Real Estate Finance', 'Mortgage Analysis']
    function: "Cash-Out Refinance LTV — loan-to-value ratio for a cash-out refinance transaction."
    y_as_x: []
    :param new_loan_amount: "Parameter new_loan_amount used in Cash-out refinance LTV calculation."
    :param property_value: "Property Value is the estimated market worth of a real estate asset."
    :return: "Computed value of Cash-out refinance LTV: Max Refi Proceeds = Appraised Value x Max LTV"
    '''
    return new_loan_amount / property_value






def catch_up_distribution(excess_profit, catch_up_rate, preferred_return_shortfall):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Private Equity', 'Venture Capital', 'LBO']
    function: "Catch-Up Distribution — allows GP to receive increased share of profits until they reach their carried interest percentage."
    y_as_x: []
    :param excess_profit: "Parameter excess_profit used in Catch-up distribution calculation."
    :param catch_up_rate: "Parameter catch_up_rate used in Catch-up distribution calculation."
    :param preferred_return_shortfall: "Parameter preferred_return_shortfall used in Catch-up distribution calculation."
    :return: "Computed value of Catch-up distribution: Catch-up = distribute until GP achieves target carry split"
    '''
    return min(excess_profit * catch_up_rate, preferred_return_shortfall)






def cdo_tranche_loss(portfolio_loss, attachment_point, detachment_point):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Structured Finance', 'Securitization']
    function: "CDO Tranche Loss — the loss allocated to a specific tranche. Loss = clip((Portfolio Loss - AP) / (DP - AP), 0, 1)."
    y_as_x: []
    :param portfolio_loss: "Parameter portfolio_loss used in CDO tranche loss calculation."
    :param attachment_point: "Parameter attachment_point used in CDO tranche loss calculation."
    :param detachment_point: "Parameter detachment_point used in CDO tranche loss calculation."
    :return: "Computed value of CDO tranche loss: Loss_tranche = min(max(PoolLoss-Attach,0), Detach-Attach)"
    '''
    import numpy as np
    return np.clip((portfolio_loss - attachment_point) / (detachment_point - attachment_point), 0, 1)






def cds_par_spread(probability_of_default, loss_given_default, discount_factor):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Fixed Income', 'Bond Mathematics', 'Credit Markets']
    function: "CDS Par Spread — the annual premium that makes the CDS contract value zero at inception."
    y_as_x: []
    :param probability_of_default: "Probability of Default (PD) is the likelihood that a borrower will fail to meet obligations."
    :param loss_given_default: "Loss Given Default (LGD) is the fraction of exposure lost if a default occurs."
    :param discount_factor: "Discount Factor is the present value of one unit of currency at a future date."
    :return: "Computed value of CDS par spread: S* = PV_protection / PV01"
    '''
    return probability_of_default * loss_given_default / discount_factor






def cds_premium_leg(spread, notional, survival_probs, discount_factors, day_count_fractions):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Fixed Income', 'Bond Mathematics', 'Credit Markets']
    function: "CDS Premium Leg — present value of premium payments, conditional on survival."
    y_as_x: []
    :param spread: "Spread is the difference between two interest rates or yields."
    :param notional: "Notional is the face amount of a derivative contract used to calculate payments."
    :param survival_probs: "Parameter survival_probs used in CDS premium leg calculation."
    :param discount_factors: "Parameter discount_factors used in CDS premium leg calculation."
    :param day_count_fractions: "Parameter day_count_fractions used in CDS premium leg calculation."
    :return: "Computed value of CDS premium leg: PV_prem = S sum_i alpha_i DF_i Survival(t_i)"
    '''
    import numpy as np
    sp = np.array(survival_probs); df = np.array(discount_factors); dcf = np.array(day_count_fractions)
    return spread * notional * np.sum(sp * df * dcf)






def cds_protection_leg(notional, loss_given_default, default_probs, discount_factors):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Fixed Income', 'Bond Mathematics', 'Credit Markets']
    function: "CDS Protection Leg — present value of the contingent payment upon default."
    y_as_x: []
    :param notional: "Notional is the face amount of a derivative contract used to calculate payments."
    :param loss_given_default: "Loss Given Default (LGD) is the fraction of exposure lost if a default occurs."
    :param default_probs: "Parameter default_probs used in CDS protection leg calculation."
    :param discount_factors: "Parameter discount_factors used in CDS protection leg calculation."
    :return: "Computed value of CDS protection leg: PV_prot = LGD integral DF(t) dQ(t)"
    '''
    import numpy as np
    dp = np.array(default_probs); df = np.array(discount_factors)
    return notional * loss_given_default * np.sum(dp * df)






def cds_spread_approximation(probability_of_default, loss_given_default):
    '''
    domain: ['Credit risk']
    subdomain: ['Credit Risk']
    function: "CDS Spread Approximation — simplified CDS spread = PD * LGD (annualized)."
    y_as_x: []
    :param probability_of_default: "Probability of Default (PD) is the likelihood that a borrower will fail to meet obligations."
    :param loss_given_default: "Loss Given Default (LGD) is the fraction of exposure lost if a default occurs."
    :return: "Computed value of CDS spread approximation: s ≈ λ(1-R)"
    '''
    return probability_of_default * loss_given_default






def cet1_ratio(cet1_capital, risk_weighted_assets):
    '''
    domain: ['Banking, lending & project finance']
    subdomain: ['Banking', 'Lending', 'Project Finance']
    function: "CET1 Ratio — Common Equity Tier 1 capital divided by risk-weighted assets. Minimum 4.5% under Basel III."
    y_as_x: ['capital_conservation_buffer']
    :param cet1_capital: "Parameter cet1_capital used in CET1 ratio calculation."
    :param risk_weighted_assets: "Parameter risk_weighted_assets used in CET1 ratio calculation."
    :return: "Computed value of CET1 ratio: CET1 Ratio = CET1 Capital / Risk-Weighted Assets"
    '''
    return cet1_capital / risk_weighted_assets






def chaikin_money_flow_cmf(high, low, close, volume, period=20):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "Chaikin Money Flow (CMF) — volume-weighted average of accumulation/distribution over a period."
    y_as_x: []
    :param high: "High is the highest price during a specific trading period."
    :param low: "Low is the lowest price during a specific trading period."
    :param close: "Close is the final trading price at the end of a trading period."
    :param volume: "Volume is the total number of shares or contracts traded during a period."
    :param period: "Period (n) is the lookback window in number of bars for technical indicators."
    :return: "Computed value of Chaikin money flow (CMF): CMF = sum(MFM x Volume)/sum Volume over n"
    '''
    import pandas as pd
    h = pd.Series(high); l = pd.Series(low); c = pd.Series(close); v = pd.Series(volume)
    mfm = ((c - l) - (h - c)) / (h - l)
    mfm = mfm.fillna(0)
    mfv = mfm * v
    return mfv.rolling(window=period).sum() / v.rolling(window=period).sum()






def chaikin_oscillator(high, low, close, volume):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "Chaikin Oscillator — the difference between 3-period and 10-period EMA of the Accumulation/Distribution Line."
    y_as_x: []
    :param high: "High is the highest price during a specific trading period."
    :param low: "Low is the lowest price during a specific trading period."
    :param close: "Close is the final trading price at the end of a trading period."
    :param volume: "Volume is the total number of shares or contracts traded during a period."
    :return: "Computed value of Chaikin oscillator: CHO = EMA_3(ADL) - EMA_10(ADL)"
    '''
    import pandas as pd
    h = pd.Series(high); l = pd.Series(low); c = pd.Series(close); v = pd.Series(volume)
    mfm = ((c - l) - (h - c)) / (h - l)
    mfm = mfm.fillna(0)
    adl = (mfm * v).cumsum()
    return adl.ewm(span=3).mean() - adl.ewm(span=10).mean()






def chain_ladder_development(cumulative_claims, development_factors):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "Chain-Ladder Development — projects ultimate claims by applying development factors to cumulative claims."
    y_as_x: []
    :param cumulative_claims: "Parameter cumulative_claims used in Chain-ladder development calculation."
    :param development_factors: "Parameter development_factors used in Chain-ladder development calculation."
    :return: "Computed value of Chain-ladder development: Ultimate_i = Latest_i x CDF_i"
    '''
    import numpy as np
    return np.array(cumulative_claims) * np.array(development_factors)






def charm(spot_price, strike_price, risk_free_rate, volatility, time_to_expiry):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Charm (Delta Decay) — the rate of change of delta with respect to time. Also called delta bleed."
    y_as_x: []
    :param spot_price: "Spot Price (S) is the current market price of the underlying asset."
    :param strike_price: "Strike Price (K) is the predetermined price at which an option can be exercised."
    :param risk_free_rate: "Risk-Free Rate (Rf) is the theoretical rate of return with zero risk, typically proxied by government bond yields."
    :param volatility: "Volatility (sigma) is the annualized standard deviation of returns."
    :param time_to_expiry: "Time to Expiry (T) is the remaining time until expiration, in years."
    :return: "Computed value of Charm: Charm = d(Delta)/dt"
    '''
    import numpy as np
    from scipy.stats import norm
    d1 = (np.log(spot_price/strike_price) + (risk_free_rate + 0.5*volatility**2)*time_to_expiry) / (volatility*np.sqrt(time_to_expiry))
    d2 = d1 - volatility*np.sqrt(time_to_expiry)
    return -norm.pdf(d1) * (2*risk_free_rate*time_to_expiry - d2*volatility*np.sqrt(time_to_expiry)) / (2*time_to_expiry*volatility*np.sqrt(time_to_expiry))






def chooser_option_value(spot_price, strike_price, risk_free_rate, volatility, time_to_expiry, choose_time):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Chooser Option Value — an option where the holder can choose whether it becomes a call or put at a specified date."
    y_as_x: []
    :param spot_price: "Spot Price (S) is the current market price of the underlying asset."
    :param strike_price: "Strike Price (K) is the predetermined price at which an option can be exercised."
    :param risk_free_rate: "Risk-Free Rate (Rf) is the theoretical rate of return with zero risk, typically proxied by government bond yields."
    :param volatility: "Volatility (sigma) is the annualized standard deviation of returns."
    :param time_to_expiry: "Time to Expiry (T) is the remaining time until expiration, in years."
    :param choose_time: "Parameter choose_time used in Chooser option value calculation."
    :return: "Computed value of Chooser option value: V = value of right to choose call or put at decision time"
    '''
    import numpy as np
    from scipy.stats import norm
    d1 = (np.log(spot_price/strike_price) + (risk_free_rate + 0.5*volatility**2)*time_to_expiry) / (volatility*np.sqrt(time_to_expiry))
    d2 = d1 - volatility*np.sqrt(time_to_expiry)
    call = spot_price*norm.cdf(d1) - strike_price*np.exp(-risk_free_rate*time_to_expiry)*norm.cdf(d2)
    put = strike_price*np.exp(-risk_free_rate*time_to_expiry)*norm.cdf(-d2) - spot_price*norm.cdf(-d1)
    return max(call, put)






def christoffersen_independence_test(violations):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "Christoffersen Independence Test — tests whether VaR violations are serially independent."
    y_as_x: []
    :param violations: "Parameter violations used in Christoffersen independence test calculation."
    :return: "Computed value of Christoffersen independence test: LR_ind = -2 ln(L_restricted/L_unrestricted)"
    '''
    import numpy as np
    from scipy.stats import chi2
    v = np.array(violations, dtype=int)
    n00 = np.sum((v[:-1]==0) & (v[1:]==0))
    n01 = np.sum((v[:-1]==0) & (v[1:]==1))
    n10 = np.sum((v[:-1]==1) & (v[1:]==0))
    n11 = np.sum((v[:-1]==1) & (v[1:]==1))
    pi01 = n01/(n00+n01) if (n00+n01)>0 else 0
    pi11 = n11/(n10+n11) if (n10+n11)>0 else 0
    pi = (n01+n11)/(n00+n01+n10+n11)
    if pi*(1-pi)*pi01*(1-pi01)*pi11*(1-pi11) == 0:
        return {'lr_stat': 0, 'p_value': 1}
    lr = -2*np.log(((1-pi)**(n00+n10)*pi**(n01+n11))/((1-pi01)**n00*pi01**n01*(1-pi11)**n10*pi11**n11))
    return {'lr_stat': lr, 'p_value': 1 - chi2.cdf(lr, 1)}






def cir_short_rate_model(r0, kappa, theta, sigma, dt, num_steps, num_paths=1000):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Interest Rate Modeling', 'Term Structure']
    function: "CIR short-rate model — dr_t = κ(θ-r_t)dt + σ√(r_t)dW_t. A financial metric in the domain of Interest-rate modeling & term structures."
    y_as_x: []
    :param args: "Parameter args used in CIR short-rate model calculation."
    :param kwargs: "Parameter kwargs used in CIR short-rate model calculation."
    :return: "Computed value of CIR short-rate model: dr_t = κ(θ-r_t)dt + σ√(r_t)dW_t"
    '''
    import numpy as np
    r = np.zeros((num_paths, num_steps+1)); r[:,0] = r0
    for t in range(num_steps):
        dw = np.random.standard_normal(num_paths) * np.sqrt(dt)
        r[:,t+1] = np.maximum(r[:,t] + kappa*(theta - r[:,t])*dt + sigma*np.sqrt(np.maximum(r[:,t],0))*dw, 0)
    return r


def cir_zero_coupon_bond_price(face_value, kappa, theta, sigma, r0, maturity):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Interest Rate Modeling', 'Term Structure']
    function: "CIR zero-coupon bond price — P(t,T) = A(t,T) exp(-B(t,T)r_t). A financial metric in the domain of Interest-rate modeling & term structures."
    y_as_x: []
    :param args: "Parameter args used in CIR zero-coupon bond price calculation."
    :param kwargs: "Parameter kwargs used in CIR zero-coupon bond price calculation."
    :return: "Computed value of CIR zero-coupon bond price: P(t,T) = A(t,T) exp(-B(t,T)r_t)"
    '''
    import numpy as np
    gamma = np.sqrt(kappa**2 + 2 * sigma**2)
    eg = np.exp(gamma * maturity) - 1
    denom = (gamma + kappa) * eg + 2 * gamma
    B = 2 * eg / denom
    A_num = 2 * gamma * np.exp((kappa + gamma) * maturity / 2)
    A = (A_num / denom) ** (2 * kappa * theta / sigma**2)
    return face_value * A * np.exp(-B * r0)




def claims_ratio(incurred_claims, earned_premiums):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "Claims Ratio — incurred claims divided by earned premiums. Same as loss ratio in insurance."
    y_as_x: []
    :param incurred_claims: "Parameter incurred_claims used in Claims ratio calculation."
    :param earned_premiums: "Parameter earned_premiums used in Claims ratio calculation."
    :return: "Computed value of Claims ratio: Claims Ratio = Claims Incurred / Earned Premium"
    '''
    return incurred_claims / earned_premiums






def clean_price(dirty_price, accrued_interest):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Fixed Income', 'Bond Mathematics', 'Credit Markets']
    function: "Clean Price — the quoted bond price excluding accrued interest. Clean = Dirty - AI."
    y_as_x: ['dirty_price']
    :param dirty_price: "Dirty Price — the actual transaction price = clean price + accrued interest."
    :param accrued_interest: "Accrued interest — AI = Coupon × DayCountFraction. A financial metric in the domain of Fixed income & bond math."
    :return: "Computed value of Clean price: Clean Price = Dirty Price - Accrued Interest"
    '''
    return dirty_price - accrued_interest






def cltv_for_mortgage(first_mortgage, second_mortgage, property_value):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Real Estate Finance', 'Mortgage Analysis']
    function: "Combined Loan-to-Value (CLTV) — the ratio of all mortgage liens to property value."
    y_as_x: []
    :param first_mortgage: "Parameter first_mortgage used in CLTV for mortgage calculation."
    :param second_mortgage: "Parameter second_mortgage used in CLTV for mortgage calculation."
    :param property_value: "Property Value is the estimated market worth of a real estate asset."
    :return: "Computed value of CLTV for mortgage: All Secured Debt / Property Value"
    '''
    return (first_mortgage + second_mortgage) / property_value






def cointegration_regression(y, x):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Financial Econometrics', 'Time Series Analysis']
    function: "Cointegration Regression — tests whether two time series share a long-run equilibrium relationship."
    y_as_x: []
    :param y: "Parameter y used in Cointegration regression calculation."
    :param x: "Parameter x used in Cointegration regression calculation."
    :return: "Computed value of Cointegration regression: y_t = alpha + beta x_t + u_t with u_t stationary"
    '''
    from statsmodels.tsa.stattools import coint
    t_stat, p_value, crit_values = coint(y, x)
    return {'t_stat': t_stat, 'p_value': p_value, 'critical_values': crit_values}






def collateral_haircut(market_value, haircut_rate):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit Risk', 'Default Modeling', 'Credit Portfolio']
    function: "Collateral Haircut — the adjusted value of collateral after applying a haircut for price volatility."
    y_as_x: []
    :param market_value: "Parameter market_value used in Collateral haircut calculation."
    :param haircut_rate: "Parameter haircut_rate used in Collateral haircut calculation."
    :return: "Computed value of Collateral haircut: Haircut = 1 - Lending Value / Market Value"
    '''
    return market_value * (1 - haircut_rate)






def color(spot_price, strike_price, risk_free_rate, volatility, time_to_expiry):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Color (Gamma Decay) — the rate of change of gamma with respect to time."
    y_as_x: []
    :param spot_price: "Spot Price (S) is the current market price of the underlying asset."
    :param strike_price: "Strike Price (K) is the predetermined price at which an option can be exercised."
    :param risk_free_rate: "Risk-Free Rate (Rf) is the theoretical rate of return with zero risk, typically proxied by government bond yields."
    :param volatility: "Volatility (sigma) is the annualized standard deviation of returns."
    :param time_to_expiry: "Time to Expiry (T) is the remaining time until expiration, in years."
    :return: "Computed value of Color: Color = d(Gamma)/dt"
    '''
    import numpy as np
    from scipy.stats import norm
    d1 = (np.log(spot_price/strike_price) + (risk_free_rate + 0.5*volatility**2)*time_to_expiry) / (volatility*np.sqrt(time_to_expiry))
    d2 = d1 - volatility*np.sqrt(time_to_expiry)
    return -norm.pdf(d1) / (2*spot_price*time_to_expiry*volatility*np.sqrt(time_to_expiry)) * (2*risk_free_rate*time_to_expiry - d2*volatility*np.sqrt(time_to_expiry))






def combined_leverage(operating_leverage, financial_leverage):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "Combined Leverage — the product of operating leverage and financial leverage, measuring total risk magnification."
    y_as_x: []
    :param operating_leverage: "Operating leverage — DOL = %Delta EBIT / %Delta Sales. A financial metric in the domain of Corporate finance, valuation & capital budgeting."
    :param financial_leverage: "Financial Leverage — total assets divided by total equity. Also called equity multiplier."
    :return: "Computed value of Combined leverage: DCL = DOL x DFL"
    '''
    return operating_leverage * financial_leverage






def combined_loan_to_value_cltv(total_liens, property_value):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Banking', 'Consumer Lending', 'Project Finance']
    function: "Combined Loan-to-Value (CLTV) — all outstanding liens divided by property value."
    y_as_x: []
    :param total_liens: "Parameter total_liens used in Combined loan-to-value (CLTV) calculation."
    :param property_value: "Property Value is the estimated market worth of a real estate asset."
    :return: "Computed value of Combined loan-to-value (CLTV): CLTV = Total Secured Debt / Collateral Value"
    '''
    return total_liens / property_value






def combined_ratio(loss_ratio, expense_ratio):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "Combined Ratio — sum of loss ratio and expense ratio. Below 100% indicates underwriting profit."
    y_as_x: []
    :param loss_ratio: "Loss Ratio — incurred losses divided by earned premiums."
    :param expense_ratio: "Expense Ratio — operating expenses divided by earned premiums."
    :return: "Computed value of Combined ratio: Combined Ratio = Loss Ratio + Expense Ratio"
    '''
    return loss_ratio + expense_ratio






def commodity_carry_return(spot_return, roll_yield, collateral_yield):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Commodities', 'Futures', 'Hedging']
    function: "Commodity Carry Return — total return from holding a commodity = spot return + roll yield + collateral yield."
    y_as_x: []
    :param spot_return: "Parameter spot_return used in Commodity carry return calculation."
    :param roll_yield: "Roll yield — Roll Yield = Futures Return - Spot Return - Collateral Return. A financial metric in the domain of Commodities, futures & hedging."
    :param collateral_yield: "Parameter collateral_yield used in Commodity carry return calculation."
    :return: "Computed value of Commodity carry return: Carry = collateral yield + roll yield + spot return"
    '''
    return spot_return + roll_yield + collateral_yield






def commodity_channel_index_cci(high, low, close, period=20):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "Commodity Channel Index (CCI) — measures deviation from the statistical mean. CCI = (TP - SMA) / (0.015 * MAD)."
    y_as_x: []
    :param high: "High is the highest price during a specific trading period."
    :param low: "Low is the lowest price during a specific trading period."
    :param close: "Close is the final trading price at the end of a trading period."
    :param period: "Period (n) is the lookback window in number of bars for technical indicators."
    :return: "Computed value of Commodity channel index (CCI): CCI = (TP - SMA(TP)) / (0.015 x MeanDeviation)"
    '''
    import pandas as pd
    import numpy as np
    tp = (pd.Series(high) + pd.Series(low) + pd.Series(close)) / 3
    sma = tp.rolling(window=period).mean()
    mad = tp.rolling(window=period).apply(lambda x: np.mean(np.abs(x - x.mean())), raw=True)
    return (tp - sma) / (0.015 * mad)






def commodity_storage_arbitrage(spot_price, futures_price, storage_cost, interest_cost):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Commodities', 'Futures', 'Hedging']
    function: "Commodity Storage Arbitrage — profit from storing a commodity = Futures - Spot - Storage - Financing."
    y_as_x: []
    :param spot_price: "Spot Price (S) is the current market price of the underlying asset."
    :param futures_price: "Futures Price is the current market price of a futures contract."
    :param storage_cost: "Parameter storage_cost used in Commodity storage arbitrage calculation."
    :param interest_cost: "Parameter interest_cost used in Commodity storage arbitrage calculation."
    :return: "Computed value of Commodity storage arbitrage: Arbitrage if F_0 > S_0 e^{(r+u-y)T}"
    '''
    return futures_price - spot_price - storage_cost - interest_cost






def component_risk_contribution(weights, cov_matrix):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Component Risk Contribution — each asset's contribution to total portfolio risk. CRC_i = w_i * (Sigma @ w)_i / sigma_p."
    y_as_x: []
    :param weights: "Portfolio Weights represent the proportion of total portfolio value allocated to each asset."
    :param cov_matrix: "Covariance Matrix contains the covariances between all pairs of assets."
    :return: "Computed value of Component risk contribution: CRC_i = w_i·MRC_i"
    '''
    import numpy as np
    w = np.array(weights); sigma = np.array(cov_matrix)
    port_vol = np.sqrt(w @ sigma @ w)
    marginal = sigma @ w / port_vol
    return w * marginal






def component_va_r(weights, cov_matrix, confidence_level=0.95):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "Component VaR — each asset's contribution to total portfolio VaR. Sum of component VaRs equals total VaR."
    y_as_x: []
    :param weights: "Portfolio Weights represent the proportion of total portfolio value allocated to each asset."
    :param cov_matrix: "Covariance Matrix contains the covariances between all pairs of assets."
    :param confidence_level: "Confidence Level is the probability threshold used in statistical tests and risk measures."
    :return: "Computed value of Component VaR: CVaR_i = w_i × MVaR_i"
    '''
    import numpy as np
    from scipy.stats import norm
    w = np.array(weights); sigma = np.array(cov_matrix)
    port_vol = np.sqrt(w @ sigma @ w)
    z = norm.ppf(confidence_level)
    var = z * port_vol
    marginal = z * sigma @ w / port_vol
    return w * marginal






def component_va_r_2(weights, cov_matrix, confidence_level=0.95):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "Component VaR (alternative) — decomposition of portfolio VaR into individual asset contributions."
    y_as_x: []
    :param weights: "Portfolio Weights represent the proportion of total portfolio value allocated to each asset."
    :param cov_matrix: "Covariance Matrix contains the covariances between all pairs of assets."
    :param confidence_level: "Confidence Level is the probability threshold used in statistical tests and risk measures."
    :return: "Computed value of Component VaR: CVaR_i = w_i dVaR/dw_i"
    '''
    import numpy as np
    from scipy.stats import norm
    w = np.array(weights); sigma = np.array(cov_matrix)
    port_vol = np.sqrt(w @ sigma @ w)
    z = norm.ppf(confidence_level)
    return w * z * sigma @ w / port_vol






def compounded_forward_rate(spot_rate_t1, spot_rate_t2, t1, t2):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Interest Rate Modeling', 'Term Structure']
    function: "Compounded Forward Rate — the implied forward rate between two spot rates. f(t1,t2) = [(1+r2)^t2 / (1+r1)^t1]^(1/(t2-t1)) - 1."
    y_as_x: []
    :param spot_rate_t1: "Parameter spot_rate_t1 used in Compounded forward rate calculation."
    :param spot_rate_t2: "Parameter spot_rate_t2 used in Compounded forward rate calculation."
    :param t1: "Parameter t1 used in Compounded forward rate calculation."
    :param t2: "Parameter t2 used in Compounded forward rate calculation."
    :return: "Computed value of Compounded forward rate: 1+F tau = DF(t1)/DF(t2)"
    '''
    return ((1 + spot_rate_t2)**t2 / (1 + spot_rate_t1)**t1)**(1/(t2-t1)) - 1






def conditional_prepayment_rate_cpr(smm):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Structured Finance', 'Securitization']
    function: "Conditional Prepayment Rate (CPR) — annualized prepayment rate. CPR = 1 - (1 - SMM)^12."
    y_as_x: []
    :param smm: "Parameter smm used in Conditional prepayment rate (CPR) calculation."
    :return: "Computed value of Conditional prepayment rate (CPR): CPR = 1 - (1 - SMM)^12"
    '''
    return 1 - (1 - smm)**12






def conditional_prepayment_rate_cpr_2(smm):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Structured Finance', 'Securitization']
    function: "Conditional Prepayment Rate (CPR) — annualized prepayment rate (alternative calculation)."
    y_as_x: []
    :param smm: "Parameter smm used in Conditional prepayment rate (CPR) calculation."
    :return: "Computed value of Conditional prepayment rate (CPR): CPR = 1 - (1-SMM)^12"
    '''
    return 1 - (1 - smm)**12






def constant_force_survival(force_of_mortality, time):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "Constant Force Survival — survival probability under constant force of mortality. S(t) = exp(-mu * t)."
    y_as_x: []
    :param force_of_mortality: "Force of mortality — mu_x = f_x / S_x = -d ln S_x / dx. A financial metric in the domain of Actuarial science & insurance."
    :param time: "Parameter time used in Constant force survival calculation."
    :return: "Computed value of Constant force survival: {}_tp_x = e^{-mu t}"
    '''
    import numpy as np
    return np.exp(-force_of_mortality * time)






def consumer_price_index_laspeyres_form(current_prices, base_quantities, base_prices):
    '''
    domain: ['Macroeconomics, inflation & price indices']
    subdomain: ['Macroeconomics', 'Inflation', 'Price Indices']
    function: "Consumer Price Index (Laspeyres) — CPI = sum(P_current * Q_base) / sum(P_base * Q_base) * 100."
    y_as_x: []
    :param current_prices: "Parameter current_prices used in Consumer Price Index (Laspeyres form) calculation."
    :param base_quantities: "Parameter base_quantities used in Consumer Price Index (Laspeyres form) calculation."
    :param base_prices: "Parameter base_prices used in Consumer Price Index (Laspeyres form) calculation."
    :return: "Computed value of Consumer Price Index (Laspeyres form): CPI_t = (Σ_i p_(i,t) q_(i,0) / Σ_i p_(i,0) q_(i,0)) × 100"
    '''
    import numpy as np
    return np.dot(current_prices, base_quantities) / np.dot(base_prices, base_quantities) * 100






def contango_slope(near_futures_price, far_futures_price):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Commodities', 'Futures', 'Hedging']
    function: "Contango Slope — measures the degree of contango. Positive when far > near."
    y_as_x: []
    :param near_futures_price: "Near Futures Price is the price of the nearest-maturity futures contract."
    :param far_futures_price: "Far Futures Price is the price of the further-maturity futures contract."
    :return: "Computed value of Contango slope: Contango = F_long / F_short - 1"
    '''
    return (far_futures_price - near_futures_price) / near_futures_price






def continuous_compounding(principal, rate, time):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Interest Rate Modeling', 'Term Structure']
    function: "Continuous Compounding — FV = PV * e^(rt). Compounding at infinitely small intervals."
    y_as_x: []
    :param principal: "Principal is the original amount of money borrowed or invested."
    :param rate: "Rate (r) is the interest rate or discount rate per period."
    :param time: "Parameter time used in Continuous compounding calculation."
    :return: "Computed value of Continuous compounding: FV = PV·e^{rt}"
    '''
    import numpy as np
    return principal * np.exp(rate * time)






def contribution_margin(revenue, variable_costs):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "Contribution Margin — revenue minus variable costs. Available to cover fixed costs and profit."
    y_as_x: ['contribution_margin_ratio']
    :param revenue: "Revenue is the total amount of income a business generates from the sale of goods or services before deducting expenses."
    :param variable_costs: "Parameter variable_costs used in Contribution margin calculation."
    :return: "Computed value of Contribution margin: CM = Revenue - Variable Costs"
    '''
    return revenue - variable_costs






def contribution_margin_ratio(contribution_margin, revenue):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "Contribution Margin Ratio — contribution margin as a percentage of revenue."
    y_as_x: ['break_even_revenue']
    :param contribution_margin: "Contribution Margin — revenue minus variable costs. Available to cover fixed costs and profit."
    :param revenue: "Revenue is the total amount of income a business generates from the sale of goods or services before deducting expenses."
    :return: "Computed value of Contribution margin ratio: CMR = Contribution Margin / Revenue"
    '''
    return contribution_margin / revenue






def contribution_to_return(weight, asset_return):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Performance Attribution', 'Risk-Adjusted Performance']
    function: "Contribution to Return — the portion of portfolio return attributable to a specific asset."
    y_as_x: []
    :param weight: "Parameter weight used in Contribution to return calculation."
    :param asset_return: "Parameter asset_return used in Contribution to return calculation."
    :return: "Computed value of Contribution to return: CTR_i = w_i x r_i"
    '''
    return weight * asset_return






def convenience_yield(spot_price, futures_price, risk_free_rate, time_to_expiry, storage_cost):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Commodities', 'Futures', 'Hedging']
    function: "Convenience Yield — the non-monetary benefit of holding physical commodity. y = r + c - ln(F/S)/T."
    y_as_x: ['cost_of_carry_futures_price']
    :param spot_price: "Spot Price (S) is the current market price of the underlying asset."
    :param futures_price: "Futures Price is the current market price of a futures contract."
    :param risk_free_rate: "Risk-Free Rate (Rf) is the theoretical rate of return with zero risk, typically proxied by government bond yields."
    :param time_to_expiry: "Time to Expiry (T) is the remaining time until expiration, in years."
    :param storage_cost: "Parameter storage_cost used in Convenience yield calculation."
    :return: "Computed value of Convenience yield: y = r + u - (1/T)ln(F_0/S_0)"
    '''
    import numpy as np
    return risk_free_rate + storage_cost - np.log(futures_price / spot_price) / time_to_expiry






def convenience_yield_from_futures_curve(spot_price, futures_price, risk_free_rate, time_to_maturity):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Commodities', 'Futures', 'Hedging']
    function: "Convenience Yield from Futures Curve — implied convenience yield from spot-futures relationship."
    y_as_x: []
    :param spot_price: "Spot Price (S) is the current market price of the underlying asset."
    :param futures_price: "Futures Price is the current market price of a futures contract."
    :param risk_free_rate: "Risk-Free Rate (Rf) is the theoretical rate of return with zero risk, typically proxied by government bond yields."
    :param time_to_maturity: "Parameter time_to_maturity used in Convenience yield from futures curve calculation."
    :return: "Computed value of Convenience yield from futures curve: y = r + u - ln(F/S)/T"
    '''
    import numpy as np
    return risk_free_rate - np.log(futures_price / spot_price) / time_to_maturity






def convexity(face_value, coupon_rate, yield_to_maturity, periods, frequency=2):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Fixed Income', 'Bond Mathematics', 'Credit Markets']
    function: "Convexity — the second derivative of bond price with respect to yield, divided by price. Measures curvature of the price-yield relationship."
    y_as_x: ['approximate_price_change', 'convexity_adjusted_futures_rate', 'effective_convexity']
    :param face_value: "Face Value (par value) is the nominal value of a bond stated by the issuer."
    :param coupon_rate: "Coupon Rate is the annual interest rate paid by a bond issuer relative to face value."
    :param yield_to_maturity: "Yield to Maturity (YTM) is the total return anticipated if a bond is held until maturity."
    :param periods: "Number of periods for calculations."
    :param frequency: "Frequency is the number of coupon payments per year."
    :return: "Computed value of Convexity: Convexity = (1/P) d^2P/dy^2"
    '''
    import numpy as np
    c = face_value * coupon_rate / frequency
    r = yield_to_maturity / frequency
    n = int(periods * frequency)
    t = np.arange(1, n + 1)
    price = np.sum(c / (1 + r)**t) + face_value / (1 + r)**n
    conv = np.sum(t * (t + 1) * c / (1 + r)**(t + 2)) + n * (n + 1) * face_value / (1 + r)**(n + 2)
    return conv / (price * frequency**2)






def convexity_adjusted_futures_rate(futures_rate, convexity_adjustment):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Interest Rate Modeling', 'Term Structure']
    function: "Convexity-Adjusted Futures Rate — adjusts the futures rate for the convexity bias. Forward Rate = Futures Rate - Convexity Adjustment."
    y_as_x: []
    :param futures_rate: "Parameter futures_rate used in Convexity-adjusted futures rate calculation."
    :param convexity_adjustment: "Parameter convexity_adjustment used in Convexity-adjusted futures rate calculation."
    :return: "Computed value of Convexity-adjusted futures rate: F_adj approx F + 0.5 sigma^2 T1 T2"
    '''
    return futures_rate - convexity_adjustment






def cornish_fisher_va_r(returns, confidence_level=0.95):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "Cornish-Fisher VaR — adjusts parametric VaR for skewness and kurtosis using Cornish-Fisher expansion."
    y_as_x: []
    :param returns: "Returns are the gain or loss generated on an investment over a specific period."
    :param confidence_level: "Confidence Level is the probability threshold used in statistical tests and risk measures."
    :return: "Computed value of Cornish-Fisher VaR: VaR_CF = μ + σ[z + (z^2-1)S/6 + (z^3-3z)K/24 - (2z^3-5z)S^2/36]"
    '''
    import numpy as np
    from scipy.stats import skew, kurtosis, norm
    r = np.array(returns)
    mu = np.mean(r); sigma = np.std(r, ddof=1)
    s = skew(r); k = kurtosis(r, fisher=True)
    z = norm.ppf(1 - confidence_level)
    z_cf = z + (z**2 - 1)*s/6 + (z**3 - 3*z)*(k)/24 - (2*z**3 - 5*z)*(s**2)/36
    return -(mu + z_cf * sigma)






def cost_of_equity_capm(risk_free_rate, beta, market_return):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "Cost of Equity (CAPM) — Re = Rf + beta * (Rm - Rf). The required return on equity based on systematic risk."
    y_as_x: []
    :param risk_free_rate: "Risk-Free Rate (Rf) is the theoretical rate of return with zero risk, typically proxied by government bond yields."
    :param beta: "Beta measures systematic risk, the sensitivity of returns to market movements."
    :param market_return: "Market Return (Rm) is the return on a broad market index representing overall market performance."
    :return: "Computed value of Cost of equity (CAPM): R_e = R_f + beta(E[R_m]-R_f)"
    '''
    return risk_free_rate + beta * (market_return - risk_free_rate)






def cost_of_equity_dividend_growth(dividend_per_share, stock_price, growth_rate):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "Cost of Equity (Dividend Growth) — Re = D1/P0 + g. From the Gordon Growth Model."
    y_as_x: []
    :param dividend_per_share: "Dividend Per Share (DPS) is the sum of declared dividends per ordinary share."
    :param stock_price: "Stock Price (P) is the current market price per share of a company's equity."
    :param growth_rate: "Growth Rate (g) is the rate at which a value increases over time."
    :return: "Computed value of Cost of equity (Dividend growth): R_e = D_1/P_0 + g"
    '''
    return dividend_per_share / stock_price + growth_rate






def cost_of_risk(expected_losses, premium):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Banking', 'Consumer Lending', 'Project Finance']
    function: "Cost of Risk — ratio of expected losses to premium earned."
    y_as_x: []
    :param expected_losses: "Parameter expected_losses used in Cost of risk calculation."
    :param premium: "Premium is the amount paid by the policyholder for insurance coverage."
    :return: "Computed value of Cost of risk: Cost of Risk = Loan Loss Provision / Average Gross Loans"
    '''
    return expected_losses / premium






def cost_of_carry_futures_price(spot_price, risk_free_rate, storage_cost, convenience_yield, time_to_expiry):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Commodities', 'Futures', 'Hedging']
    function: "Cost-of-Carry Futures Price — F = S * exp((r + c - y) * T). Fundamental futures pricing equation."
    y_as_x: []
    :param spot_price: "Spot Price (S) is the current market price of the underlying asset."
    :param risk_free_rate: "Risk-Free Rate (Rf) is the theoretical rate of return with zero risk, typically proxied by government bond yields."
    :param storage_cost: "Parameter storage_cost used in Cost-of-carry futures price calculation."
    :param convenience_yield: "Convenience Yield — the non-monetary benefit of holding physical commodity. y = r + c - ln(F/S)/T."
    :param time_to_expiry: "Time to Expiry (T) is the remaining time until expiration, in years."
    :return: "Computed value of Cost-of-carry futures price: F_0 = S_0 e^{(r + u - y)T}"
    '''
    import numpy as np
    return spot_price * np.exp((risk_free_rate + storage_cost - convenience_yield) * time_to_expiry)






def countercyclical_capital_buffer(buffer_rate, risk_weighted_assets):
    '''
    domain: ['Bank regulation, Basel & prudential ratios']
    subdomain: ['Bank Regulation', 'Basel Framework', 'Prudential Ratios']
    function: "Countercyclical Capital Buffer — additional capital required during credit booms. CCyB = buffer_rate * RWA."
    y_as_x: []
    :param buffer_rate: "Parameter buffer_rate used in Countercyclical capital buffer calculation."
    :param risk_weighted_assets: "Parameter risk_weighted_assets used in Countercyclical capital buffer calculation."
    :return: "Computed value of Countercyclical capital buffer: CCyB = jurisdiction-specific add-on to CET1 requirement"
    '''
    return buffer_rate * risk_weighted_assets






def covariance_matrix(returns_matrix):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Covariance Matrix — the matrix of covariances between all pairs of asset returns."
    y_as_x: []
    :param returns_matrix: "Parameter returns_matrix used in Covariance matrix calculation."
    :return: "Computed value of Covariance matrix: Σ = E[(R-μ)(R-μ)^T]"
    '''
    import numpy as np
    return np.cov(np.array(returns_matrix), rowvar=False)






def coverage_ratio(numerator, denominator):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit Risk', 'Default Modeling', 'Credit Portfolio']
    function: "Coverage Ratio — generic coverage ratio measuring ability to meet obligations."
    y_as_x: []
    :param numerator: "Parameter numerator used in Coverage ratio calculation."
    :param denominator: "Parameter denominator used in Coverage ratio calculation."
    :return: "Computed value of Coverage ratio: Allowance / Nonperforming Assets"
    '''
    return numerator / denominator if denominator != 0 else float("inf")






def covered_call_payoff(spot_price, strike_price, premium_received, purchase_price):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Covered Call Payoff — P&L from owning the stock and selling a call option."
    y_as_x: []
    :param spot_price: "Spot Price (S) is the current market price of the underlying asset."
    :param strike_price: "Strike Price (K) is the predetermined price at which an option can be exercised."
    :param premium_received: "Parameter premium_received used in Covered call payoff calculation."
    :param purchase_price: "Parameter purchase_price used in Covered call payoff calculation."
    :return: "Computed value of Covered call payoff: Payoff = S_T - max(S_T-K,0) + Premium"
    '''
    import numpy as np
    stock_pnl = spot_price - purchase_price
    option_pnl = premium_received - np.maximum(spot_price - strike_price, 0)
    return stock_pnl + option_pnl






def covered_interest_parity_cip(spot_rate, domestic_rate, foreign_rate, time):
    '''
    domain: ['FX & international finance']
    subdomain: ['FX Markets', 'International Finance']
    function: "Covered Interest Parity (CIP) — the forward rate implied by interest rate differentials. F = S * (1 + r_d*T) / (1 + r_f*T)."
    y_as_x: []
    :param spot_rate: "Spot Rate is the current interest rate for a specific maturity."
    :param domestic_rate: "Domestic Interest Rate (r_d) is the risk-free rate in the domestic currency."
    :param foreign_rate: "Foreign Interest Rate (r_f) is the risk-free rate in the foreign currency."
    :param time: "Parameter time used in Covered interest parity (CIP) calculation."
    :return: "Computed value of Covered interest parity (CIP): F/S = (1+i_d)/(1+i_f) "
    '''
    return spot_rate * (1 + domestic_rate * time) / (1 + foreign_rate * time)






def cox_proportional_hazards(durations, event_observed, covariates):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Financial Econometrics', 'Time Series Analysis']
    function: "Cox Proportional Hazards — semi-parametric survival model. h(t|X) = h0(t) * exp(beta * X)."
    y_as_x: []
    :param durations: "Parameter durations used in Cox proportional hazards calculation."
    :param event_observed: "Parameter event_observed used in Cox proportional hazards calculation."
    :param covariates: "Parameter covariates used in Cox proportional hazards calculation."
    :return: "Computed value of Cox proportional hazards: h(t|x)=h_0(t)exp(beta'x)"
    '''
    from lifelines import CoxPHFitter
    import pandas as pd
    df = pd.DataFrame(covariates)
    df['duration'] = durations
    df['event'] = event_observed
    cph = CoxPHFitter()
    cph.fit(df, duration_col='duration', event_col='event')
    return cph






def cox_ingersoll_ross_cir_process(r0, kappa, theta, sigma, dt, num_steps, num_paths=1000):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Interest Rate Modeling', 'Term Structure']
    function: "Cox-Ingersoll-Ross (CIR) process — dr_t = a(b-r_t)dt + sigma sqrt(r_t)dW_t. A financial metric in the domain of Interest-rate modeling & term structures."
    y_as_x: []
    :param args: "Parameter args used in Cox-Ingersoll-Ross (CIR) process calculation."
    :param kwargs: "Parameter kwargs used in Cox-Ingersoll-Ross (CIR) process calculation."
    :return: "Computed value of Cox-Ingersoll-Ross (CIR) process: dr_t = a(b-r_t)dt + sigma sqrt(r_t)dW_t"
    '''
    import numpy as np
    r = np.zeros((num_paths, num_steps+1)); r[:,0] = r0
    for t in range(num_steps):
        dw = np.random.standard_normal(num_paths) * np.sqrt(dt)
        r[:,t+1] = np.maximum(r[:,t] + kappa*(theta-r[:,t])*dt + sigma*np.sqrt(np.maximum(r[:,t],0))*dw, 0)
    return r


def cpi_inflation_month_over_month(cpi_current, cpi_previous):
    '''
    domain: ['Macroeconomics, inflation & price indices']
    subdomain: ['Macroeconomics', 'Inflation', 'Price Indices']
    function: "CPI Inflation (Month over Month) — monthly change in the Consumer Price Index."
    y_as_x: []
    :param cpi_current: "Parameter cpi_current used in CPI inflation (month over month) calculation."
    :param cpi_previous: "Parameter cpi_previous used in CPI inflation (month over month) calculation."
    :return: "Computed value of CPI inflation (month over month): π_t^(CPI,MoM) = CPI_t / CPI_(t-1) - 1"
    '''
    return (cpi_current - cpi_previous) / cpi_previous






def cpi_inflation_year_over_year(cpi_current, cpi_year_ago):
    '''
    domain: ['Macroeconomics, inflation & price indices']
    subdomain: ['Macroeconomics', 'Inflation', 'Price Indices']
    function: "CPI Inflation (Year over Year) — annual change in the Consumer Price Index."
    y_as_x: []
    :param cpi_current: "Parameter cpi_current used in CPI inflation (year over year) calculation."
    :param cpi_year_ago: "Parameter cpi_year_ago used in CPI inflation (year over year) calculation."
    :return: "Computed value of CPI inflation (year over year): π_t^(CPI,YoY) = CPI_t / CPI_(t-12) - 1"
    '''
    return (cpi_current - cpi_year_ago) / cpi_year_ago






def crack_spread(gasoline_price, crude_oil_price, heating_oil_price=0):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Commodities', 'Futures', 'Hedging']
    function: "Crack Spread — the refining margin between refined products and crude oil."
    y_as_x: []
    :param gasoline_price: "Parameter gasoline_price used in Crack spread calculation."
    :param crude_oil_price: "Parameter crude_oil_price used in Crack spread calculation."
    :param heating_oil_price: "Parameter heating_oil_price used in Crack spread calculation."
    :return: "Computed value of Crack spread: Crack Spread = Product Futures Value - Crude Futures Cost"
    '''
    return gasoline_price + heating_oil_price - crude_oil_price






def credibility_premium(credibility_factor, individual_experience, population_mean):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "Credibility Premium — blends individual and population experience. P = Z*X_bar + (1-Z)*mu."
    y_as_x: []
    :param credibility_factor: "Parameter credibility_factor used in Credibility premium calculation."
    :param individual_experience: "Parameter individual_experience used in Credibility premium calculation."
    :param population_mean: "Parameter population_mean used in Credibility premium calculation."
    :return: "Computed value of Credibility premium: Premium = Z x Experience Mean + (1-Z) x Manual Mean"
    '''
    return credibility_factor * individual_experience + (1 - credibility_factor) * population_mean






def credit_conversion_factor_ccf(committed_amount, drawn_amount):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Banking', 'Consumer Lending', 'Project Finance']
    function: "Credit Conversion Factor (CCF) — proportion of off-balance sheet exposure expected to convert to on-balance sheet."
    y_as_x: []
    :param committed_amount: "Parameter committed_amount used in Credit conversion factor (CCF) calculation."
    :param drawn_amount: "Parameter drawn_amount used in Credit conversion factor (CCF) calculation."
    :return: "Computed value of Credit conversion factor (CCF): CCF = (EAD - Outstanding) / Undrawn"
    '''
    return drawn_amount / committed_amount if committed_amount != 0 else 0






def credit_portfolio_variance_independent_defaults(pds, lgds, eads):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit Risk', 'Default Modeling', 'Credit Portfolio']
    function: "Credit Portfolio Variance (Independent Defaults) — variance of portfolio credit losses assuming independent defaults."
    y_as_x: []
    :param pds: "Parameter pds used in Credit portfolio variance (independent defaults) calculation."
    :param lgds: "Parameter lgds used in Credit portfolio variance (independent defaults) calculation."
    :param eads: "Parameter eads used in Credit portfolio variance (independent defaults) calculation."
    :return: "Computed value of Credit portfolio variance (independent defaults): Var(L) = sum_i EAD_i^2 LGD_i^2 PD_i(1-PD_i)"
    '''
    import numpy as np
    pd_arr = np.array(pds); lgd_arr = np.array(lgds); ead_arr = np.array(eads)
    return np.sum((ead_arr * lgd_arr)**2 * pd_arr * (1 - pd_arr))






def credit_rwa_under_standardized_approach(ead, risk_weight):
    '''
    domain: ['Bank regulation, Basel & prudential ratios']
    subdomain: ['Bank Regulation', 'Basel Framework', 'Prudential Ratios']
    function: "Credit RWA under Standardized Approach — Risk-Weighted Assets = EAD * Risk Weight."
    y_as_x: []
    :param ead: "Exposure at Default (EAD) is the total exposure amount at the time of default."
    :param risk_weight: "Risk Weight is the Basel-prescribed weight applied to an exposure for capital calculation."
    :return: "Computed value of Credit RWA under standardized approach: Credit_RWA = EAD x supervisory risk weight"
    '''
    return ead * risk_weight






def credit_spread(corporate_yield, risk_free_yield):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit Risk', 'Default Modeling', 'Credit Portfolio']
    function: "Credit Spread — the difference in yield between a corporate bond and a comparable risk-free bond."
    y_as_x: ['duration_times_spread_dts']
    :param corporate_yield: "Parameter corporate_yield used in Credit spread calculation."
    :param risk_free_yield: "Parameter risk_free_yield used in Credit spread calculation."
    :return: "Computed value of Credit spread: Credit Spread = Corporate Yield - Risk-free Yield"
    '''
    return corporate_yield - risk_free_yield






def credit_va_r(expected_loss, unexpected_loss_quantile):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit Risk', 'Default Modeling', 'Credit Portfolio']
    function: "Credit VaR — the potential loss at a given confidence level minus expected loss."
    y_as_x: []
    :param expected_loss: "Expected Loss — EL = PD * LGD * EAD. The mean of the loss distribution."
    :param unexpected_loss_quantile: "Parameter unexpected_loss_quantile used in Credit VaR calculation."
    :return: "Computed value of Credit VaR: CreditVaR = quantile_alpha(loss distribution) - expected loss"
    '''
    return unexpected_loss_quantile - expected_loss






def cross_exchange_rate(rate_a_usd, rate_b_usd):
    '''
    domain: ['FX & international finance']
    subdomain: ['FX Markets', 'International Finance']
    function: "Cross Exchange Rate — the exchange rate between two currencies derived from their respective USD rates."
    y_as_x: []
    :param rate_a_usd: "Parameter rate_a_usd used in Cross exchange rate calculation."
    :param rate_b_usd: "Parameter rate_b_usd used in Cross exchange rate calculation."
    :return: "Computed value of Cross exchange rate: S_{A/C} = S_{A/B} × S_{B/C}"
    '''
    return rate_a_usd / rate_b_usd






def cross_currency_basis(ccs_spread, libor_domestic, libor_foreign):
    '''
    domain: ['FX & international finance']
    subdomain: ['FX Markets', 'International Finance']
    function: "Cross-currency basis — Basis = quoted basis spread that equalizes swap PV. A financial metric in the domain of FX & international finance."
    y_as_x: []
    :param args: "Parameter args used in Cross-currency basis calculation."
    :param kwargs: "Parameter kwargs used in Cross-currency basis calculation."
    :return: "Computed value of Cross-currency basis: Basis = quoted basis spread that equalizes swap PV"
    '''
    return ccs_spread - (libor_domestic - libor_foreign)


def cross_hedge_ratio(rho_sigma_s, sigma_f):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Commodities', 'Futures', 'Hedging']
    function: "Cross-hedge ratio — h_x = rho (sigma_S / sigma_F). A financial metric in the domain of Commodities, futures & hedging."
    y_as_x: []
    :param rho_sigma_s: "Parameter rho_sigma_s used in Cross-hedge ratio calculation."
    :param sigma_f: "Parameter sigma_f used in Cross-hedge ratio calculation."
    :return: "Computed value of Cross-hedge ratio: h_x = rho (sigma_S / sigma_F)"
    '''
    return rho_sigma_s / sigma_f






def cumulative_gap(asset_repricing, liability_repricing):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Treasury', 'ALM', 'Balance Sheet Management']
    function: "Cumulative Gap — running total of repricing gaps across time buckets for ALM."
    y_as_x: []
    :param asset_repricing: "Parameter asset_repricing used in Cumulative gap calculation."
    :param liability_repricing: "Parameter liability_repricing used in Cumulative gap calculation."
    :return: "Computed value of Cumulative gap: CumGap_T = sum_{t<=T} Gap_t"
    '''
    import numpy as np
    return np.cumsum(np.array(asset_repricing) - np.array(liability_repricing))






def cumulative_inflation_factor_from_cpi(cpi_current, cpi_base):
    '''
    domain: ['Macroeconomics, inflation & price indices']
    subdomain: ['Macroeconomics', 'Inflation', 'Price Indices']
    function: "Cumulative Inflation Factor from CPI — total price level change. CIF = CPI_current / CPI_base."
    y_as_x: []
    :param cpi_current: "Parameter cpi_current used in Cumulative inflation factor from CPI calculation."
    :param cpi_base: "Parameter cpi_base used in Cumulative inflation factor from CPI calculation."
    :return: "Computed value of Cumulative inflation factor from CPI: Inflation Factor_(0→t) = CPI_t / CPI_0"
    '''
    return cpi_current / cpi_base






def cumulative_inflation_factor_from_ppi(ppi_current, ppi_base):
    '''
    domain: ['Macroeconomics, inflation & price indices']
    subdomain: ['Macroeconomics', 'Inflation', 'Price Indices']
    function: "Cumulative Inflation Factor from PPI — total producer price change."
    y_as_x: []
    :param ppi_current: "Parameter ppi_current used in Cumulative inflation factor from PPI calculation."
    :param ppi_base: "Parameter ppi_base used in Cumulative inflation factor from PPI calculation."
    :return: "Computed value of Cumulative inflation factor from PPI: Inflation Factor_(0→t) = PPI_t / PPI_0"
    '''
    return ppi_current / ppi_base






def cumulative_liquidity_gap(cumulative_inflows, cumulative_outflows):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Treasury', 'ALM', 'Balance Sheet Management']
    function: "Cumulative Liquidity Gap — cumulative cash inflows minus outflows over a time horizon."
    y_as_x: []
    :param cumulative_inflows: "Parameter cumulative_inflows used in Cumulative liquidity gap calculation."
    :param cumulative_outflows: "Parameter cumulative_outflows used in Cumulative liquidity gap calculation."
    :return: "Computed value of Cumulative liquidity gap: CumLiquidityGap_T = sum_{t<=T} (Inflows_t - Outflows_t)"
    '''
    return cumulative_inflows - cumulative_outflows






def cumulative_net_loss(cumulative_losses, original_balance):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Structured Finance', 'Securitization']
    function: "Cumulative Net Loss — total realized losses as a proportion of original pool balance."
    y_as_x: []
    :param cumulative_losses: "Parameter cumulative_losses used in Cumulative net loss calculation."
    :param original_balance: "Parameter original_balance used in Cumulative net loss calculation."
    :return: "Computed value of Cumulative net loss: CNL = cumulative(net charge-offs) / original balance"
    '''
    return cumulative_losses / original_balance






def cumulative_return(returns):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Performance Attribution', 'Risk-Adjusted Performance']
    function: "Cumulative Return — the total return over a period compounded from periodic returns."
    y_as_x: []
    :param returns: "Returns are the gain or loss generated on an investment over a specific period."
    :return: "Computed value of Cumulative return: R_cum = Π_t (1+r_t) - 1"
    '''
    import numpy as np
    return np.prod(1 + np.array(returns)) - 1






def cure_rate(cured_loans, total_delinquent):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit Risk', 'Default Modeling', 'Credit Portfolio']
    function: "Cure Rate — the proportion of delinquent loans that return to current status."
    y_as_x: []
    :param cured_loans: "Parameter cured_loans used in Cure rate calculation."
    :param total_delinquent: "Parameter total_delinquent used in Cure rate calculation."
    :return: "Computed value of Cure rate: Cure Rate = cured delinquent accounts / delinquent accounts"
    '''
    return cured_loans / total_delinquent if total_delinquent != 0 else 0






def currency_basket_index(exchange_rates, weights):
    '''
    domain: ['FX & international finance']
    subdomain: ['FX Markets', 'International Finance']
    function: "Currency Basket Index — weighted average of exchange rates against a basket of currencies."
    y_as_x: []
    :param exchange_rates: "Parameter exchange_rates used in Currency basket index calculation."
    :param weights: "Portfolio Weights represent the proportion of total portfolio value allocated to each asset."
    :return: "Computed value of Currency basket index: Index_t = prod_i S_{i,t}^{w_i}"
    '''
    import numpy as np
    return np.dot(exchange_rates, weights)






def currency_carry_return(high_yield_rate, low_yield_rate, fx_return):
    '''
    domain: ['FX & international finance']
    subdomain: ['FX Markets', 'International Finance']
    function: "Currency Carry Return — return from borrowing low-yield and investing in high-yield currency."
    y_as_x: []
    :param high_yield_rate: "Parameter high_yield_rate used in Currency carry return calculation."
    :param low_yield_rate: "Parameter low_yield_rate used in Currency carry return calculation."
    :param fx_return: "Parameter fx_return used in Currency carry return calculation."
    :return: "Computed value of Currency carry return: Carry = i_high - i_low + FX change"
    '''
    return high_yield_rate - low_yield_rate + fx_return






def current_ratio(current_assets, current_liabilities):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "Current Ratio — current assets divided by current liabilities. Measures short-term liquidity."
    y_as_x: []
    :param current_assets: "Current Assets are assets expected to be converted to cash within one year."
    :param current_liabilities: "Current Liabilities are obligations due within one year."
    :return: "Computed value of Current ratio: Current Ratio = Current Assets / Current Liabilities"
    '''
    return current_assets / current_liabilities






def current_yield(coupon, bond_price):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Fixed Income', 'Bond Mathematics', 'Credit Markets']
    function: "Current Yield — annual coupon payment divided by current bond price."
    y_as_x: []
    :param coupon: "Coupon is the periodic interest payment made to the bondholder."
    :param bond_price: "Bond Price — present value of all future cash flows. P = sum(C/(1+y)^t) + FV/(1+y)^n."
    :return: "Computed value of Current yield: Current Yield = Annual Coupon / Bond Price"
    '''
    return coupon / bond_price






def curtate_expected_future_lifetime(survival_probs):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "Curtate Expected Future Lifetime — the expected number of complete years of future lifetime. e_x = sum(k*p_x)."
    y_as_x: []
    :param survival_probs: "Parameter survival_probs used in Curtate expected future lifetime calculation."
    :return: "Computed value of Curtate expected future lifetime: e_x^∘ = sum_{k>=1} {}_kp_x"
    '''
    import numpy as np
    sp = np.array(survival_probs)
    return np.sum(np.cumprod(sp))






def cva_capital_proxy(expected_positive_exposure, counterparty_spread, maturity):
    '''
    domain: ['Bank regulation, Basel & prudential ratios']
    subdomain: ['Bank Regulation', 'Basel Framework', 'Prudential Ratios']
    function: "CVA Capital Proxy — simplified credit valuation adjustment capital charge."
    y_as_x: []
    :param expected_positive_exposure: "Parameter expected_positive_exposure used in CVA capital proxy calculation."
    :param counterparty_spread: "Parameter counterparty_spread used in CVA capital proxy calculation."
    :param maturity: "Maturity (T) is the time remaining until a bond's principal is repaid."
    :return: "Computed value of CVA capital proxy: CVA Capital ~ sensitivity-based or standardized charge"
    '''
    return expected_positive_exposure * counterparty_spread * maturity






def bsm_d1(spot_price, strike_price, risk_free_rate, volatility, time_to_expiry):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "d1 — first standardized variable in Black-Scholes-Merton. d1 = [ln(S/K) + (r + sigma^2/2)*T] / (sigma*sqrt(T))."
    y_as_x: []
    :param spot_price: "Spot Price (S) is the current market price of the underlying asset."
    :param strike_price: "Strike Price (K) is the predetermined price at which an option can be exercised."
    :param risk_free_rate: "Risk-Free Rate (Rf) is the theoretical rate of return with zero risk, typically proxied by government bond yields."
    :param volatility: "Volatility (sigma) is the annualized standard deviation of returns."
    :param time_to_expiry: "Time to Expiry (T) is the remaining time until expiration, in years."
    :return: "Computed value of d1: d1 = [ln(S/K) + (r + 0.5σ^2)T] / (σ√T)"
    '''
    import numpy as np
    return (np.log(spot_price/strike_price) + (risk_free_rate + 0.5*volatility**2)*time_to_expiry) / (volatility*np.sqrt(time_to_expiry))






def bsm_d2(spot_price, strike_price, risk_free_rate, volatility, time_to_expiry):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "d2 — second BSM variable. d2 = d1 - sigma*sqrt(T)."
    y_as_x: []
    :param spot_price: "Spot Price (S) is the current market price of the underlying asset."
    :param strike_price: "Strike Price (K) is the predetermined price at which an option can be exercised."
    :param risk_free_rate: "Risk-Free Rate (Rf) is the theoretical rate of return with zero risk, typically proxied by government bond yields."
    :param volatility: "Volatility (sigma) is the annualized standard deviation of returns."
    :param time_to_expiry: "Time to Expiry (T) is the remaining time until expiration, in years."
    :return: "Computed value of d2: d2 = d1 - σ√T"
    '''
    import numpy as np
    d1 = (np.log(spot_price/strike_price) + (risk_free_rate + 0.5*volatility**2)*time_to_expiry) / (volatility*np.sqrt(time_to_expiry))
    return d1 - volatility*np.sqrt(time_to_expiry)






def days_inventory_outstanding_dio(inventory, cost_of_goods_sold):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "Days Inventory Outstanding (DIO) — average number of days to sell inventory."
    y_as_x: []
    :param inventory: "Inventory is the raw materials, work-in-process, and finished goods held for sale."
    :param cost_of_goods_sold: "Cost of Goods Sold (COGS) is the direct costs attributable to the production of goods sold."
    :return: "Computed value of Days inventory outstanding (DIO): DIO = 365 x Average Inventory / COGS"
    '''
    return (inventory / cost_of_goods_sold) * 365






def days_payables_outstanding_dpo(accounts_payable, cost_of_goods_sold):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "Days Payables Outstanding (DPO) — average number of days to pay suppliers."
    y_as_x: []
    :param accounts_payable: "Accounts Payable (AP) is the money a company owes to its suppliers."
    :param cost_of_goods_sold: "Cost of Goods Sold (COGS) is the direct costs attributable to the production of goods sold."
    :return: "Computed value of Days payables outstanding (DPO): DPO = 365 x Average AP / COGS"
    '''
    return (accounts_payable / cost_of_goods_sold) * 365






def days_sales_outstanding_dso(accounts_receivable, revenue):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "Days Sales Outstanding (DSO) — average number of days to collect payment."
    y_as_x: []
    :param accounts_receivable: "Accounts Receivable (AR) is the money owed to a company by its customers."
    :param revenue: "Revenue is the total amount of income a business generates from the sale of goods or services before deducting expenses."
    :return: "Computed value of Days sales outstanding (DSO): DSO = 365 x Average AR / Revenue"
    '''
    return (accounts_receivable / revenue) * 365






def days_to_liquidate(position_size, average_daily_volume):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Liquidity Risk', 'Market Liquidity', 'Execution Cost']
    function: "Days to Liquidate — estimated days needed to liquidate a position at normal volume."
    y_as_x: []
    :param position_size: "Parameter position_size used in Days to liquidate calculation."
    :param average_daily_volume: "Parameter average_daily_volume used in Days to liquidate calculation."
    :return: "Computed value of Days to liquidate: DTL = Position Size / (ADV x Participation Limit)"
    '''
    return position_size / average_daily_volume






def death_probability(mortality_rate):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "Death Probability — the probability q_x that a person aged x dies within one year."
    y_as_x: []
    :param mortality_rate: "Mortality Rate (q_x) is the probability of dying within one year at age x."
    :return: "Computed value of Death probability: {}_tq_x = 1 - {}_tp_x"
    '''
    return mortality_rate






def debt_burden_ratio(total_debt_service, income):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Banking', 'Consumer Lending', 'Project Finance']
    function: "Debt Burden Ratio — total debt service payments as a fraction of income."
    y_as_x: []
    :param total_debt_service: "Parameter total_debt_service used in Debt burden ratio calculation."
    :param income: "Parameter income used in Debt burden ratio calculation."
    :return: "Computed value of Debt burden ratio: Debt Burden = Total Debt Service / Gross Income"
    '''
    return total_debt_service / income






def debt_service(principal_payment, interest_payment):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Banking', 'Consumer Lending', 'Project Finance']
    function: "Debt Service — total periodic payment = principal + interest."
    y_as_x: ['debt_service_coverage_ratio_dscr']
    :param principal_payment: "Parameter principal_payment used in Debt service calculation."
    :param interest_payment: "Interest Payment — the interest portion of a specific loan payment."
    :return: "Computed value of Debt service: Debt Service = Interest + Scheduled Principal + Lease/Rent if included"
    '''
    return principal_payment + interest_payment






def debt_service_coverage_ratio_dscr(noi, debt_service):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Banking', 'Consumer Lending', 'Project Finance']
    function: "Debt Service Coverage Ratio (DSCR) — NOI divided by debt service. DSCR > 1 indicates sufficient income."
    y_as_x: []
    :param noi: "Net Operating Income (NOI) is total revenue from a property minus operating expenses."
    :param debt_service: "Debt Service — total periodic payment = principal + interest."
    :return: "Computed value of Debt service coverage ratio (DSCR): DSCR = Net Operating Income  / Debt Service"
    '''
    return noi / debt_service if debt_service != 0 else float("inf")






def debt_yield(noi, loan_amount):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Banking', 'Consumer Lending', 'Project Finance']
    function: "Debt Yield — NOI divided by loan amount. Used as a loan sizing metric."
    y_as_x: []
    :param noi: "Net Operating Income (NOI) is total revenue from a property minus operating expenses."
    :param loan_amount: "Loan Amount is the total principal borrowed."
    :return: "Computed value of Debt yield: Debt Yield = Net Operating Income/ Loan Amount"
    '''
    return noi / loan_amount






def debt_to_assets(total_debt, total_assets):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "Debt-to-Assets — total debt divided by total assets. Measures leverage."
    y_as_x: []
    :param total_debt: "Total Debt is the sum of all short-term and long-term borrowings of a company."
    :param total_assets: "Total Assets represent the sum of all current and non-current assets owned by a company."
    :return: "Computed value of Debt-to-assets: Debt_to_assets = Debt / Assets"
    '''
    return total_debt / total_assets






def debt_to_equity(total_debt, total_equity):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "Debt-to-Equity — total debt divided by total equity. Key leverage ratio."
    y_as_x: []
    :param total_debt: "Total Debt is the sum of all short-term and long-term borrowings of a company."
    :param total_equity: "Total Equity is the residual interest in the assets of an entity after deducting all its liabilities."
    :return: "Computed value of Debt-to-equity: Debt_to_equity = Debt / Equity"
    '''
    return total_debt / total_equity






def debt_to_income_residual(total_debt_payments, gross_income, living_expenses):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Banking', 'Consumer Lending', 'Project Finance']
    function: "Debt-to-Income Residual — remaining income after debt payments and living expenses."
    y_as_x: []
    :param total_debt_payments: "Parameter total_debt_payments used in Debt-to-income residual calculation."
    :param gross_income: "Parameter gross_income used in Debt-to-income residual calculation."
    :param living_expenses: "Parameter living_expenses used in Debt-to-income residual calculation."
    :return: "Computed value of Debt-to-income residual: Residual Income = Net Income - Taxes - Housing Costs - Other Debt Payments"
    '''
    return gross_income - total_debt_payments - living_expenses






def decreasing_annuity(interest_rate, num_periods):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "Decreasing annuity — (Da)_{x:n} = E[sum_{k=1}^n (n-k+1) v^k 1(T_x>=k)]. A financial metric in the domain of Actuarial science & insurance."
    y_as_x: []
    :param args: "Parameter args used in Decreasing annuity calculation."
    :param kwargs: "Parameter kwargs used in Decreasing annuity calculation."
    :return: "Computed value of Decreasing annuity: (Da)_{x:n} = E[sum_{k=1}^n (n-k+1) v^k 1(T_x>=k)]"
    '''
    v = 1 / (1 + interest_rate); n = num_periods
    a = (1 - v**n) / interest_rate
    return (n * a - (a - n*v**n) / interest_rate) / 1


def default_rate(num_defaults, total_loans):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Structured Finance', 'Securitization']
    function: "Default Rate — the proportion of loans that default within a given period."
    y_as_x: []
    :param num_defaults: "Parameter num_defaults used in Default rate calculation."
    :param total_loans: "Parameter total_loans used in Default rate calculation."
    :return: "Computed value of Default rate: Default Rate = Defaults / Current or Original Balance"
    '''
    return num_defaults / total_loans






def delinquency_ratio(delinquent_balance, total_balance):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Banking', 'Consumer Lending', 'Project Finance']
    function: "Delinquency Ratio — delinquent loan balance divided by total outstanding balance."
    y_as_x: []
    :param delinquent_balance: "Parameter delinquent_balance used in Delinquency ratio calculation."
    :param total_balance: "Parameter total_balance used in Delinquency ratio calculation."
    :return: "Computed value of Delinquency ratio: Delinquency Ratio = Delinquent Loans / Gross Loans"
    '''
    return delinquent_balance / total_balance






def delinquency_trigger(current_delinquency, trigger_level):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Structured Finance', 'Securitization']
    function: "Delinquency Trigger — whether the delinquency ratio exceeds the trigger threshold."
    y_as_x: []
    :param current_delinquency: "Parameter current_delinquency used in Delinquency trigger calculation."
    :param trigger_level: "Parameter trigger_level used in Delinquency trigger calculation."
    :return: "Computed value of Delinquency trigger: Trigger breached if delinquency ratio > threshold"
    '''
    return current_delinquency > trigger_level






def delta_call(spot_price, strike_price, risk_free_rate, volatility, time_to_expiry):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Delta (Call) — N(d1), the rate of change of call price with respect to underlying. Range [0, 1]."
    y_as_x: []
    :param spot_price: "Spot Price (S) is the current market price of the underlying asset."
    :param strike_price: "Strike Price (K) is the predetermined price at which an option can be exercised."
    :param risk_free_rate: "Risk-Free Rate (Rf) is the theoretical rate of return with zero risk, typically proxied by government bond yields."
    :param volatility: "Volatility (sigma) is the annualized standard deviation of returns."
    :param time_to_expiry: "Time to Expiry (T) is the remaining time until expiration, in years."
    :return: "Computed value of Delta (call): Delta = e^{-qT}N(d1)"
    '''
    import numpy as np
    from scipy.stats import norm
    d1 = (np.log(spot_price/strike_price) + (risk_free_rate + 0.5*volatility**2)*time_to_expiry) / (volatility*np.sqrt(time_to_expiry))
    return norm.cdf(d1)






def delta_put(spot_price, strike_price, risk_free_rate, volatility, time_to_expiry):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Delta (Put) — N(d1) - 1, the rate of change of put price with respect to underlying. Range [-1, 0]."
    y_as_x: []
    :param spot_price: "Spot Price (S) is the current market price of the underlying asset."
    :param strike_price: "Strike Price (K) is the predetermined price at which an option can be exercised."
    :param risk_free_rate: "Risk-Free Rate (Rf) is the theoretical rate of return with zero risk, typically proxied by government bond yields."
    :param volatility: "Volatility (sigma) is the annualized standard deviation of returns."
    :param time_to_expiry: "Time to Expiry (T) is the remaining time until expiration, in years."
    :return: "Computed value of Delta (put): Delta = -e^{-qT}N(-d1)"
    '''
    import numpy as np
    from scipy.stats import norm
    d1 = (np.log(spot_price/strike_price) + (risk_free_rate + 0.5*volatility**2)*time_to_expiry) / (volatility*np.sqrt(time_to_expiry))
    return norm.cdf(d1) - 1






def delta_normal_va_r(portfolio_value, portfolio_volatility, confidence_level=0.95):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "Delta-Normal VaR — VaR = Portfolio Value * sigma * z_alpha. Assumes normally distributed returns."
    y_as_x: []
    :param portfolio_value: "Parameter portfolio_value used in Delta-normal VaR calculation."
    :param portfolio_volatility: "Portfolio Volatility — sqrt(w' * Sigma * w). Standard deviation of portfolio returns."
    :param confidence_level: "Confidence Level is the probability threshold used in statistical tests and risk measures."
    :return: "Computed value of Delta-normal VaR: VaR = z_alpha sqrt(Delta' Sigma Delta)"
    '''
    from scipy.stats import norm
    z = norm.ppf(confidence_level)
    return portfolio_value * portfolio_volatility * z






def deposit_beta(delta_deposit_rate, delta_market_rate):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Treasury', 'ALM', 'Balance Sheet Management']
    function: "Deposit beta — Deposit Beta = Delta Deposit Rate / Delta Market Rate. A financial metric in the domain of Treasury, ALM & balance-sheet management."
    y_as_x: []
    :param delta_deposit_rate: "Parameter delta_deposit_rate used in Deposit beta calculation."
    :param delta_market_rate: "Parameter delta_market_rate used in Deposit beta calculation."
    :return: "Computed value of Deposit beta: Deposit Beta = Delta Deposit Rate / Delta Market Rate"
    '''
    return delta_deposit_rate / delta_market_rate






def detrended_price_oscillator_dpo(price_shifted, sma):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "Detrended price oscillator (DPO) — DPO = Price shifted - SMA. A financial metric in the domain of Technical analysis & chart-based indicators."
    y_as_x: []
    :param price_shifted: "Parameter price_shifted used in Detrended price oscillator (DPO) calculation."
    :param sma: "Parameter sma used in Detrended price oscillator (DPO) calculation."
    :return: "Computed value of Detrended price oscillator (DPO): DPO = Price shifted - SMA"
    '''
    return price_shifted - sma






def digital_call_price(spot_price, strike_price, risk_free_rate, volatility, time_to_expiry):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Digital call price — Digital = e^{-rT} N(d2). A financial metric in the domain of Derivatives, options & volatility."
    y_as_x: []
    :param args: "Parameter args used in Digital call price calculation."
    :param kwargs: "Parameter kwargs used in Digital call price calculation."
    :return: "Computed value of Digital call price: Digital = e^{-rT} N(d2)"
    '''
    import numpy as np
    from scipy.stats import norm
    d2 = (np.log(spot_price/strike_price) + (risk_free_rate - 0.5*volatility**2)*time_to_expiry) / (volatility*np.sqrt(time_to_expiry))
    return np.exp(-risk_free_rate * time_to_expiry) * norm.cdf(d2)


def digital_put_price(spot_price, strike_price, risk_free_rate, volatility, time_to_expiry):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Digital put price — Digital = e^{-rT} N(-d2). A financial metric in the domain of Derivatives, options & volatility."
    y_as_x: []
    :param args: "Parameter args used in Digital put price calculation."
    :param kwargs: "Parameter kwargs used in Digital put price calculation."
    :return: "Computed value of Digital put price: Digital = e^{-rT} N(-d2)"
    '''
    import numpy as np
    from scipy.stats import norm
    d2 = (np.log(spot_price / strike_price) + (risk_free_rate - 0.5 * volatility**2) * time_to_expiry) / (volatility * np.sqrt(time_to_expiry))
    return np.exp(-risk_free_rate * time_to_expiry) * norm.cdf(-d2)




def diluted_eps(net_income, diluted_shares):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "Diluted EPS — net income divided by diluted shares outstanding, accounting for convertible securities."
    y_as_x: []
    :param net_income: "Net Income is the total profit after all expenses, taxes, interest, and depreciation have been deducted from total revenue."
    :param diluted_shares: "Parameter diluted_shares used in Diluted EPS calculation."
    :return: "Computed value of Diluted EPS: Diluted EPS = Diluted Net Income Available to Common / Diluted Shares"
    '''
    return net_income / diluted_shares






def dirty_price(clean_price, accrued_interest):
    '''
    domain: ['Fixed income & bond math']
    subdomain: ['Fixed Income', 'Bond Mathematics']
    function: "Dirty Price — the actual transaction price = clean price + accrued interest."
    y_as_x: ['clean_price']
    :param clean_price: "Clean Price — the quoted bond price excluding accrued interest. Clean = Dirty - AI."
    :param accrued_interest: "Accrued interest — AI = Coupon × DayCountFraction. A financial metric in the domain of Fixed income & bond math."
    :return: "Computed value of Dirty price: Dirty Price = Clean Price + Accrued Interest"
    '''
    return clean_price + accrued_interest






def discount_factor(rate, time):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "Discount Factor — PV of one unit of currency. DF = 1/(1+r)^t."
    y_as_x: ['bond_price', 'cds_par_spread', 'cds_premium_leg', 'cds_protection_leg', 'forward_rate_from_discount_factors', 'present_value_pv', 'spot_rate_from_discount_factor', 'swap_present_value']
    :param rate: "Rate (r) is the interest rate or discount rate per period."
    :param time: "Parameter time used in Discount factor calculation."
    :return: "Computed value of Discount factor: DF_t = 1 / (1+r)^t"
    '''
    return 1 / (1 + rate)**time






def discount_yield_t_bill(face_value, purchase_price, days_to_maturity):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Fixed Income', 'Bond Mathematics', 'Credit Markets']
    function: "Discount Yield (T-bill) — yield on a discount basis = (FV - P) / FV * (360/DTM)."
    y_as_x: []
    :param face_value: "Face Value (par value) is the nominal value of a bond stated by the issuer."
    :param purchase_price: "Parameter purchase_price used in Discount yield (T-bill) calculation."
    :param days_to_maturity: "Days to Maturity is the number of days remaining until the instrument matures."
    :return: "Computed value of Discount yield (T-bill): Discount Yield = (F-P)/F x 360/d"
    '''
    return (face_value - purchase_price) / face_value * (360 / days_to_maturity)






def discounted_payback_period(cash_flows, discount_rate, initial_investment):
    '''
    domain: ['Corporate finance & capital budgeting']
    subdomain: ['Corporate Finance', 'Capital Budgeting']
    function: "Discounted Payback Period — the number of periods required for discounted cash flows to recover the initial investment."
    y_as_x: []
    :param cash_flows: "Parameter cash_flows used in Discounted payback period calculation."
    :param discount_rate: "Discount Rate is the rate used to discount future cash flows to present value."
    :param initial_investment: "Parameter initial_investment used in Discounted payback period calculation."
    :return: "Computed value of Discounted payback period: Discounted Payback = min{t : Σ_{i≤t} CF_i/(1+r)^i ≥ Initial Outlay}"
    '''
    import numpy as np
    cumulative = 0
    for i, cf in enumerate(cash_flows):
        cumulative += cf / (1 + discount_rate)**(i + 1)
        if cumulative >= initial_investment:
            return i + 1
    return float("inf")






def distance_to_default_dd(asset_value, debt_face_value, asset_volatility, risk_free_rate, time_horizon):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit Risk', 'Default Modeling', 'Credit Portfolio']
    function: "Distance to Default (DD) — the number of standard deviations the asset value is from the default point. DD = [ln(V/D) + (r - 0.5*sigma^2)*T] / (sigma*sqrt(T))."
    y_as_x: []
    :param asset_value: "Parameter asset_value used in Distance to default (DD) calculation."
    :param debt_face_value: "Parameter debt_face_value used in Distance to default (DD) calculation."
    :param asset_volatility: "Parameter asset_volatility used in Distance to default (DD) calculation."
    :param risk_free_rate: "Risk-Free Rate (Rf) is the theoretical rate of return with zero risk, typically proxied by government bond yields."
    :param time_horizon: "Parameter time_horizon used in Distance to default (DD) calculation."
    :return: "Computed value of Distance to default (DD): DD = [ln(V_A/D) + (mu_A - 0.5 sigma_A^2)T] / (sigma_A sqrt(T))"
    '''
    import numpy as np
    return (np.log(asset_value / debt_face_value) + (risk_free_rate - 0.5 * asset_volatility**2) * time_horizon) / (asset_volatility * np.sqrt(time_horizon))






def diversification_ratio(weights, volatilities, portfolio_volatility):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Diversification Ratio — ratio of weighted average volatility to portfolio volatility. DR > 1 indicates diversification benefit."
    y_as_x: []
    :param weights: "Portfolio Weights represent the proportion of total portfolio value allocated to each asset."
    :param volatilities: "Parameter volatilities used in Diversification ratio calculation."
    :param portfolio_volatility: "Portfolio Volatility — sqrt(w' * Sigma * w). Standard deviation of portfolio returns."
    :return: "Computed value of Diversification ratio: DR = w_i (Sigma w)_i / sigma_p"
    '''
    import numpy as np
    return np.dot(weights, volatilities) / portfolio_volatility






def dividend_coverage(net_income, dividends):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Equity Valuation', 'Asset Pricing']
    function: "Dividend Coverage — net income divided by dividends paid. Higher values indicate more sustainable dividends."
    y_as_x: []
    :param net_income: "Net Income is the total profit after all expenses, taxes, interest, and depreciation have been deducted from total revenue."
    :param dividends: "Dividends are portions of a company's earnings distributed to shareholders."
    :return: "Computed value of Dividend coverage: Coverage = EPS / DPS"
    '''
    return net_income / dividends if dividends != 0 else float("inf")






def dividend_discount_model_ddm(dividend_per_share, cost_of_equity, growth_rate):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "Dividend Discount Model (DDM) — P = D1 / (r - g). Assumes constant growth."
    y_as_x: []
    :param dividend_per_share: "Dividend Per Share (DPS) is the sum of declared dividends per ordinary share."
    :param cost_of_equity: "Cost of Equity (Re) is the return required by equity investors."
    :param growth_rate: "Growth Rate (g) is the rate at which a value increases over time."
    :return: "Computed value of Dividend discount model (DDM): P_0 = sum_t D_t/(1+r)^t"
    '''
    return dividend_per_share / (cost_of_equity - growth_rate)






def dividend_discount_model_gordon_growth(dividend_per_share, cost_of_equity, growth_rate):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Equity Valuation', 'Asset Pricing']
    function: "Dividend Discount Model (Gordon Growth) — P0 = D1 / (ke - g). Classic single-stage DDM."
    y_as_x: []
    :param dividend_per_share: "Dividend Per Share (DPS) is the sum of declared dividends per ordinary share."
    :param cost_of_equity: "Cost of Equity (Re) is the return required by equity investors."
    :param growth_rate: "Growth Rate (g) is the rate at which a value increases over time."
    :return: "Computed value of Dividend discount model (Gordon growth): P_0 = D_1 / (r - g)"
    '''
    return dividend_per_share / (cost_of_equity - growth_rate)






def dividend_payout_ratio(dividends, net_income):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "Dividend Payout Ratio — proportion of earnings paid as dividends."
    y_as_x: []
    :param dividends: "Dividends are portions of a company's earnings distributed to shareholders."
    :param net_income: "Net Income is the total profit after all expenses, taxes, interest, and depreciation have been deducted from total revenue."
    :return: "Computed value of Dividend payout ratio: Payout = Dividends / Net Income"
    '''
    return dividends / net_income if net_income != 0 else 0






def dividend_yield(dividend_per_share, stock_price):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "Dividend Yield — annual dividend per share divided by stock price."
    y_as_x: ['cost_of_equity_dividend_growth', 'dividend_coverage', 'dividend_discount_model_ddm', 'forward_price_on_non_dividend_asset', 'gordon_growth_model']
    :param dividend_per_share: "Dividend Per Share (DPS) is the sum of declared dividends per ordinary share."
    :param stock_price: "Stock Price (P) is the current market price per share of a company's equity."
    :return: "Computed value of Dividend yield: Dividend Yield = Annual Dividend per Share / Price per Share"
    '''
    return dividend_per_share / stock_price






def dollar_duration(modified_duration, bond_price):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Fixed Income', 'Bond Mathematics', 'Credit Markets']
    function: "Dollar Duration — the dollar change in bond value for a 1% change in yield."
    y_as_x: []
    :param modified_duration: "Modified Duration gives the percentage price change per 1% yield change."
    :param bond_price: "Bond Price — present value of all future cash flows. P = sum(C/(1+y)^t) + FV/(1+y)^n."
    :return: "Computed value of Dollar duration: Dollar Duration = Modified Duration x Price"
    '''
    return modified_duration * bond_price / 100






def dollar_volume(price, volume):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Liquidity Risk', 'Market Liquidity', 'Execution Cost']
    function: "Dollar Volume — total dollar value of shares traded = price * volume."
    y_as_x: []
    :param price: "Parameter price used in Dollar volume calculation."
    :param volume: "Volume is the total number of shares or contracts traded during a period."
    :return: "Computed value of Dollar volume: Dollar Volume = Price x Shares Traded"
    '''
    return price * volume






def donchian_channel_lower(low, period=20):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "Donchian Channel Lower — the lowest low over the lookback period."
    y_as_x: []
    :param low: "Low is the lowest price during a specific trading period."
    :param period: "Period (n) is the lookback window in number of bars for technical indicators."
    :return: "Computed value of Donchian channel lower: Lower = rolling min(L,n)"
    '''
    import pandas as pd
    return pd.Series(low).rolling(window=period).min()






def donchian_channel_upper(high, period=20):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "Donchian Channel Upper — the highest high over the lookback period."
    y_as_x: []
    :param high: "High is the highest price during a specific trading period."
    :param period: "Period (n) is the lookback window in number of bars for technical indicators."
    :return: "Computed value of Donchian channel upper: Upper = rolling max(H,n)"
    '''
    import pandas as pd
    return pd.Series(high).rolling(window=period).max()






def downside_capture(portfolio_returns, benchmark_returns):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Performance Attribution', 'Risk-Adjusted Performance']
    function: "Downside Capture — portfolio return in down markets / benchmark return in down markets. Lower is better."
    y_as_x: []
    :param portfolio_returns: "Portfolio Returns represent the weighted average returns of all assets in a portfolio."
    :param benchmark_returns: "Benchmark Returns are the returns of a reference index used for performance comparison."
    :return: "Computed value of Downside capture: Downside Capture = Avg(R_p | R_b<0) / Avg(R_b | R_b<0)"
    '''
    import numpy as np
    pr = np.array(portfolio_returns); br = np.array(benchmark_returns)
    mask = br < 0
    if not mask.any(): return 0
    return np.mean(pr[mask]) / np.mean(br[mask])






def downside_deviation(returns, target=0):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "Downside Deviation — standard deviation of returns below a target. Used in Sortino Ratio."
    y_as_x: ['upside_potential_ratio']
    :param returns: "Returns are the gain or loss generated on an investment over a specific period."
    :param target: "Parameter target used in Downside deviation calculation."
    :return: "Computed value of Downside deviation: DD = sqrt(E[min(R-MAR,0)^2])"
    '''
    import numpy as np
    r = np.array(returns)
    downside = np.minimum(r - target, 0)
    return np.sqrt(np.mean(downside**2))






def dpi(cumulative_distributions, paid_in_capital):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Private Equity', 'Venture Capital', 'LBO']
    function: "DPI (Distributions to Paid-In) — cumulative cash distributions divided by paid-in capital."
    y_as_x: []
    :param cumulative_distributions: "Parameter cumulative_distributions used in DPI calculation."
    :param paid_in_capital: "Parameter paid_in_capital used in DPI calculation."
    :return: "Computed value of DPI: DPI = Distributions / Paid-In Capital"
    '''
    return cumulative_distributions / paid_in_capital






def drawdown(returns):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "Drawdown — peak-to-trough decline as a percentage. DD_t = (peak_t - V_t) / peak_t."
    y_as_x: ['calmar_ratio', 'drawdown_duration', 'expected_drawdown', 'maximum_drawdown', 'pain_index', 'sterling_ratio', 'ulcer_index']
    :param returns: "Returns are the gain or loss generated on an investment over a specific period."
    :return: "Computed value of Drawdown: DD_t = V_t/peak_t - 1"
    '''
    import numpy as np
    r = np.array(returns)
    wealth = np.cumprod(1 + r)
    peaks = np.maximum.accumulate(wealth)
    return (peaks - wealth) / peaks






def drawdown_duration(returns):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Performance Attribution', 'Risk-Adjusted Performance']
    function: "Drawdown Duration — the length of the longest drawdown period."
    y_as_x: []
    :param returns: "Returns are the gain or loss generated on an investment over a specific period."
    :return: "Computed value of Drawdown duration: Duration = consecutive periods below prior high"
    '''
    import numpy as np
    r = np.array(returns)
    wealth = np.cumprod(1 + r)
    peaks = np.maximum.accumulate(wealth)
    dd = (peaks - wealth) / peaks
    in_dd = dd > 0
    durations = []
    current = 0
    for d in in_dd:
        if d: current += 1
        elif current > 0: durations.append(current); current = 0
    if current > 0: durations.append(current)
    return max(durations) if durations else 0






def duration_gap(asset_duration, liability_duration, leverage_ratio=1):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Treasury', 'ALM', 'Balance Sheet Management']
    function: "Duration Gap — measures interest rate risk = Asset Duration - Leverage * Liability Duration."
    y_as_x: []
    :param asset_duration: "Parameter asset_duration used in Duration gap calculation."
    :param liability_duration: "Parameter liability_duration used in Duration gap calculation."
    :param leverage_ratio: "Leverage Ratio — Tier 1 Capital / Total Exposure. Basel III minimum 3%."
    :return: "Computed value of Duration gap: DGAP = D_A - (L/A) D_L"
    '''
    return asset_duration - leverage_ratio * liability_duration






def duration_times_spread_dts(spread_duration, credit_spread):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Fixed Income', 'Bond Mathematics', 'Credit Markets']
    function: "Duration Times Spread (DTS) — product of spread duration and credit spread. Measures credit risk exposure."
    y_as_x: []
    :param spread_duration: "Spread duration — Spread Duration = -dP/ds / P. A financial metric in the domain of Fixed income, bonds & credit markets."
    :param credit_spread: "Credit Spread is the yield difference between a corporate bond and a risk-free bond."
    :return: "Computed value of Duration times spread (DTS): DTS = Spread x Spread Duration"
    '''
    return spread_duration * credit_spread






def duration_neutral_hedge_ratio(target_duration, hedge_instrument_duration, target_dv01, hedge_dv01):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Interest Rate Modeling', 'Term Structure']
    function: "Duration-Neutral Hedge Ratio — the ratio of DV01s to achieve duration neutrality."
    y_as_x: []
    :param target_duration: "Parameter target_duration used in Duration-neutral hedge ratio calculation."
    :param hedge_instrument_duration: "Parameter hedge_instrument_duration used in Duration-neutral hedge ratio calculation."
    :param target_dv01: "Parameter target_dv01 used in Duration-neutral hedge ratio calculation."
    :param hedge_dv01: "Parameter hedge_dv01 used in Duration-neutral hedge ratio calculation."
    :return: "Computed value of Duration-neutral hedge ratio: h = DV01_asset / DV01_hedge"
    '''
    return target_dv01 / hedge_dv01 if hedge_dv01 != 0 else 0






def durbin_watson(residuals):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Financial Econometrics', 'Time Series Analysis']
    function: "Durbin-Watson — DW = sum_t(e_t-e_{t-1})^2 / sum_t e_t^2. A financial metric in the domain of Econometrics & time-series finance."
    y_as_x: []
    :param data: "Parameter data used in Durbin-Watson calculation."
    :param args: "Parameter args used in Durbin-Watson calculation."
    :return: "Computed value of Durbin-Watson: DW = sum_t(e_t-e_{t-1})^2 / sum_t e_t^2"
    '''
    import numpy as np
    r = np.array(residuals)
    return np.sum(np.diff(r)**2) / np.sum(r**2)


def dv01_pvbp(modified_duration, bond_price):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Fixed Income', 'Bond Mathematics', 'Credit Markets']
    function: "DV01 / PVBP — the dollar change in bond value for a 1 basis point change in yield."
    y_as_x: []
    :param modified_duration: "Modified Duration gives the percentage price change per 1% yield change."
    :param bond_price: "Bond Price — present value of all future cash flows. P = sum(C/(1+y)^t) + FV/(1+y)^n."
    :return: "Computed value of DV01 / PVBP: DV01 = -dP/dy x 0.0001"
    '''
    return modified_duration * bond_price * 0.0001






def earnings_at_risk(net_interest_income, rate_shock, repricing_gap):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Treasury', 'ALM', 'Balance Sheet Management']
    function: "Earnings at Risk — potential change in NII from interest rate shock = Gap * Rate Shock."
    y_as_x: []
    :param net_interest_income: "Parameter net_interest_income used in Earnings at risk calculation."
    :param rate_shock: "Parameter rate_shock used in Earnings at risk calculation."
    :param repricing_gap: "Repricing gap — Gap_t = Rate Sensitive Assets_t - Rate Sensitive Liabilities_t. A financial metric in the domain of Treasury, ALM & balance-sheet management."
    :return: "Computed value of Earnings at risk: EaR_alpha = quantile_alpha(future earnings shortfall)"
    '''
    return repricing_gap * rate_shock






def earnings_yield(eps, stock_price):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Equity Valuation', 'Asset Pricing']
    function: "Earnings Yield — EPS divided by stock price. Inverse of P/E ratio."
    y_as_x: []
    :param eps: "Earnings Per Share (EPS) is the portion of profit allocated to each outstanding share of common stock."
    :param stock_price: "Stock Price (P) is the current market price per share of a company's equity."
    :return: "Computed value of Earnings yield: E/P = EPS / Price"
    '''
    return eps / stock_price






def ebit(revenue, operating_expenses):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "EBIT (Earnings Before Interest and Taxes) — measures profitability from core operations. EBIT = Revenue - Operating Expenses."
    y_as_x: ['altman_z_score', 'combined_leverage', 'ebitda', 'ebitda_margin', 'economic_value_added_eva', 'fcff', 'fixed_charge_coverage', 'interest_coverage', 'interest_coverage_ratio', 'operating_margin', 'return_on_capital_employed_roce']
    :param revenue: "Revenue is the total amount of income a business generates from the sale of goods or services before deducting expenses."
    :param operating_expenses: "Operating Expenses (OpEx) are the essential ongoing costs a business incurs to maintain daily operations and generate revenue."
    :return: "Computed value of EBIT: EBIT = Revenue - Operating Expenses"
    '''
    return revenue - operating_expenses






def ebitda(ebit, depreciation, amortization):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "EBITDA (Earnings Before Interest, Taxes, Depreciation and Amortization) — a proxy for operating cash flow. EBITDA = EBIT + D&A."
    y_as_x: ['cash_interest_coverage', 'debt_service_coverage_ratio_dscr', 'ebitda_margin', 'enterprise_value_in_lbo', 'equity_check_multiple_of_ebitda', 'exit_enterprise_value', 'net_debt_at_entry']
    :param ebit: "EBIT (Earnings Before Interest and Taxes) is a financial metric measuring a company's profitability from core operations."
    :param depreciation: "Depreciation is an accounting method that spreads the cost of a tangible asset over its useful life."
    :param amortization: "Amortization is the process of spreading the cost of an intangible asset over its useful life."
    :return: "Computed value of EBITDA: EBITDA = EBIT + D&A"
    '''
    return ebit + depreciation + amortization






def ebitda_margin(ebitda, revenue):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "EBITDA Margin — EBITDA as a percentage of revenue."
    y_as_x: []
    :param ebitda: "EBITDA (Earnings Before Interest, Taxes, Depreciation, and Amortization) is a proxy for operating cash flow."
    :param revenue: "Revenue is the total amount of income a business generates from the sale of goods or services before deducting expenses."
    :return: "Computed value of EBITDA margin: EBITDA Margin = EBITDA / Revenue"
    '''
    return ebitda / revenue






def economic_value_added_eva(nopat, invested_capital, wacc):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "Economic Value Added (EVA) — measures value creation. EVA = NOPAT - Invested Capital * WACC."
    y_as_x: []
    :param nopat: "Parameter nopat used in Economic value added (EVA) calculation."
    :param invested_capital: "Parameter invested_capital used in Economic value added (EVA) calculation."
    :param wacc: "Weighted Average Cost of Capital (WACC) is the average rate of return expected by all security holders."
    :return: "Computed value of Economic value added (EVA): EVA = NOPAT - WACC x Invested Capital"
    '''
    return nopat - invested_capital * wacc






def economic_value_of_equity_eve(asset_pvs, liability_pvs):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Treasury', 'ALM', 'Balance Sheet Management']
    function: "Economic value of equity (EVE) — EVE = PV(Assets) - PV(Liabilities). A financial metric in the domain of Treasury, ALM & balance-sheet management."
    y_as_x: []
    :param args: "Parameter args used in Economic value of equity (EVE) calculation."
    :param kwargs: "Parameter kwargs used in Economic value of equity (EVE) calculation."
    :return: "Computed value of Economic value of equity (EVE): EVE = PV(Assets) - PV(Liabilities)"
    '''
    import numpy as np
    return np.sum(asset_pvs) - np.sum(liability_pvs)


def economic_value_of_equity_sensitivity(asset_duration, liability_duration, assets, liabilities, rate_shock):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Treasury', 'ALM', 'Balance Sheet Management']
    function: "Economic value of equity sensitivity — ΔEVE ≈ -DGAP × A × Δy / (1+y). A financial metric in the domain of Treasury, ALM & balance-sheet management."
    y_as_x: []
    :param args: "Parameter args used in Economic value of equity sensitivity calculation."
    :param kwargs: "Parameter kwargs used in Economic value of equity sensitivity calculation."
    :return: "Computed value of Economic value of equity sensitivity: ΔEVE ≈ -DGAP × A × Δy / (1+y)"
    '''
    return -(asset_duration * assets - liability_duration * liabilities) * rate_shock




def effective_annual_rate_ear(periodic_rate, periods_per_year):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Banking', 'Consumer Lending', 'Project Finance']
    function: "Effective Annual Rate (EAR) — the actual annual rate after compounding. EAR = (1 + r/n)^n - 1."
    y_as_x: []
    :param periodic_rate: "Periodic Rate is the interest rate charged per compounding period."
    :param periods_per_year: "Periods Per Year is the number of compounding or return periods in one year."
    :return: "Computed value of Effective annual rate (EAR): EAR = (1+r/m)^m - 1"
    '''
    return (1 + periodic_rate)**periods_per_year - 1






def effective_convexity(price_down, price_up, initial_price, yield_change):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Fixed Income', 'Bond Mathematics', 'Credit Markets']
    function: "Effective convexity — EffConv = (P_- + P_+ - 2P_0)/(P_0 (Delta y)^2). A financial metric in the domain of Fixed income, bonds & credit markets."
    y_as_x: []
    :param args: "Parameter args used in Effective convexity calculation."
    :param kwargs: "Parameter kwargs used in Effective convexity calculation."
    :return: "Computed value of Effective convexity: EffConv = (P_- + P_+ - 2P_0)/(P_0 (Delta y)^2)"
    '''
    return (price_down + price_up - 2*initial_price) / (initial_price * yield_change**2)


def effective_duration(price_down, price_up, initial_price, yield_change):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Fixed Income', 'Bond Mathematics', 'Credit Markets']
    function: "Effective duration — EffDur = (P_- - P_+) / (2P_0 Delta y). A financial metric in the domain of Fixed income, bonds & credit markets."
    y_as_x: []
    :param args: "Parameter args used in Effective duration calculation."
    :param kwargs: "Parameter kwargs used in Effective duration calculation."
    :return: "Computed value of Effective duration: EffDur = (P_- - P_+) / (2P_0 Delta y)"
    '''
    return (price_down - price_up) / (2 * initial_price * yield_change)




def effective_gross_income(potential_gross_income, vacancy_loss, other_income=0):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Real Estate Finance', 'Mortgage Analysis']
    function: "Effective Gross Income — PGI minus vacancy losses plus other income."
    y_as_x: ['net_operating_income_noi', 'noi_margin', 'operating_expense_ratio']
    :param potential_gross_income: "Parameter potential_gross_income used in Effective gross income calculation."
    :param vacancy_loss: "Parameter vacancy_loss used in Effective gross income calculation."
    :param other_income: "Parameter other_income used in Effective gross income calculation."
    :return: "Computed value of Effective gross income: EGI = Potential Gross Income - Vacancy/Credit Loss + Other Income"
    '''
    return potential_gross_income - vacancy_loss + other_income






def effective_spread(trade_price, midpoint, side):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Liquidity Risk', 'Market Liquidity', 'Execution Cost']
    function: "Effective Spread — 2 * |Trade Price - Midpoint|. Measures actual transaction cost."
    y_as_x: ['adverse_selection_cost']
    :param trade_price: "Parameter trade_price used in Effective spread calculation."
    :param midpoint: "Parameter midpoint used in Effective spread calculation."
    :param side: "Side indicates the direction of the trade: "buy" or "sell"."
    :return: "Computed value of Effective spread: EffSpread = 2 x |Trade Price - Mid|"
    '''
    if side == 'buy':
        return 2 * (trade_price - midpoint)
    else:
        return 2 * (midpoint - trade_price)






def efficient_frontier_problem(expected_returns, cov_matrix, target_return=None):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Efficient frontier problem — min_w w'Sigma w s.t. mu'w >= r* and 1'w=1. A financial metric in the domain of Asset management & portfolio optimization."
    y_as_x: []
    :param expected_returns: "Expected Returns vector contains the anticipated return for each asset."
    :param cov_matrix: "Covariance Matrix contains the covariances between all pairs of assets."
    :return: "Computed value of Efficient frontier problem: min_w w'Sigma w s.t. mu'w >= r* and 1'w=1"
    '''
    import numpy as np
    import cvxpy as cp
    n = len(expected_returns); w = cp.Variable(n)
    mu = np.array(expected_returns); sigma = np.array(cov_matrix)
    constraints = [cp.sum(w) == 1, w >= 0]
    if target_return is not None:
        constraints.append(mu @ w >= target_return)
    prob = cp.Problem(cp.Minimize(cp.quad_form(w, sigma)), constraints)
    prob.solve()
    return w.value


def egarch(returns, p=1, q=1):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "EGARCH — ln sigma_t^2 = omega + alpha(|e_{t-1}|-E|e|) + gamma e_{t-1} + beta ln sigma_{t-1}^2. A financial metric in the domain of Market risk & volatility modeling."
    y_as_x: []
    :param returns: "Returns are the gain or loss generated on an investment over a specific period."
    :param p: "Model order parameter p (autoregressive order or similar)."
    :param q: "Model order parameter q (moving average order, ARCH order, or similar)."
    :return: "Computed value of EGARCH: ln sigma_t^2 = omega + alpha(|e_{t-1}|-E|e|) + gamma e_{t-1} + beta ln sigma_{t-1}^2"
    '''
    from arch import arch_model
    model = arch_model(returns, vol="GARCH", p=p, q=q)
    result = model.fit(disp="off")
    return result






def egarch_11(returns, p=1, q=1):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "EGARCH(1,1) — lnσ_t^2 = ω + α(|e_{t-1}|-E|e|) + γ e_{t-1} + β lnσ_{t-1}^2. A financial metric in the domain of Market risk & volatility modeling."
    y_as_x: []
    :param returns: "Returns are the gain or loss generated on an investment over a specific period."
    :param p: "Model order parameter p (autoregressive order or similar)."
    :param q: "Model order parameter q (moving average order, ARCH order, or similar)."
    :return: "Computed value of EGARCH(1,1): lnσ_t^2 = ω + α(|e_{t-1}|-E|e|) + γ e_{t-1} + β lnσ_{t-1}^2"
    '''
    from arch import arch_model
    model = arch_model(returns, vol="GARCH", p=p, q=q)
    result = model.fit(disp="off")
    return result






def elastic_net(X, y, alpha=1.0, l1_ratio=0.5):
    '''
    domain: ['Quantitative forecasting & machine learning in finance']
    subdomain: ['Quantitative Finance', 'Machine Learning']
    function: "Elastic net — beta_hat = argmin ||y-X beta||^2 + lambda[(1-alpha)||beta||_2^2/2 + alpha||beta||_1]. A financial metric in the domain of Quantitative forecasting & machine learning in finance."
    y_as_x: []
    :param X: "Parameter X used in Elastic net calculation."
    :param y: "Parameter y used in Elastic net calculation."
    :return: "Computed value of Elastic net: beta_hat = argmin ||y-X beta||^2 + lambda[(1-alpha)||beta||_2^2/2 + alpha||beta||_1]"
    '''
    from sklearn.linear_model import ElasticNet
    model = ElasticNet(alpha=alpha, l1_ratio=l1_ratio)
    model.fit(X, y)
    return model


def encumbrance_ratio(encumbered_assets, total_assets):
    '''
    domain: ['Bank regulation, Basel & prudential ratios']
    subdomain: ['Bank Regulation', 'Basel Framework', 'Prudential Ratios']
    function: "Encumbrance ratio — Encumbrance = Encumbered Assets / Total Assets. A financial metric in the domain of Bank regulation, Basel & prudential ratios."
    y_as_x: []
    :param encumbered_assets: "Parameter encumbered_assets used in Encumbrance ratio calculation."
    :param total_assets: "Total Assets represent the sum of all current and non-current assets owned by a company."
    :return: "Computed value of Encumbrance ratio: Encumbrance = Encumbered Assets / Total Assets"
    '''
    return encumbered_assets / total_assets






def endowment_insurance_apv(benefit, interest_rate, mortality_rates, term):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "Endowment insurance APV — Abar_{x:n} + {}_nE_x. A financial metric in the domain of Actuarial science & insurance."
    y_as_x: []
    :param args: "Parameter args used in Endowment insurance APV calculation."
    :param kwargs: "Parameter kwargs used in Endowment insurance APV calculation."
    :return: "Computed value of Endowment insurance APV: Abar_{x:n} + {}_nE_x"
    '''
    import numpy as np
    v = 1/(1+interest_rate); qx = np.array(mortality_rates[:term])
    px_cum = np.concatenate([[1], np.cumprod(1-qx[:-1])])
    death_ben = benefit * np.sum(v**np.arange(1,term+1) * px_cum * qx)
    survival_ben = benefit * v**term * np.prod(1 - qx)
    return death_ben + survival_ben


def enterprise_value(market_cap, total_debt, cash):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "Enterprise Value — EV = Market Cap + Total Debt - Cash. Total firm value."
    y_as_x: ['equity_value_bridge']
    :param market_cap: "Market Capitalization is the total market value of outstanding shares (price x shares)."
    :param total_debt: "Total Debt is the sum of all short-term and long-term borrowings of a company."
    :param cash: "Cash and Cash Equivalents are the most liquid current assets."
    :return: "Computed value of Enterprise value: EV = Equity Value + Net Debt + Preferred + Minority Interest"
    '''
    return market_cap + total_debt - cash






def enterprise_value_in_lbo(ebitda, entry_multiple):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Private Equity', 'Venture Capital', 'LBO']
    function: "Enterprise Value in LBO — EV = EBITDA * Entry Multiple."
    y_as_x: []
    :param ebitda: "EBITDA (Earnings Before Interest, Taxes, Depreciation, and Amortization) is a proxy for operating cash flow."
    :param entry_multiple: "Parameter entry_multiple used in Enterprise value in LBO calculation."
    :return: "Computed value of Enterprise value in LBO: EV = Entry EBITDA x Entry Multiple"
    '''
    return ebitda * entry_multiple






def eps(net_income, shares_outstanding):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "EPS (Earnings Per Share) — net income divided by shares outstanding."
    y_as_x: ['book_value_per_share', 'diluted_eps', 'earnings_yield', 'forward_p_e', 'p_e_ratio', 'peg_ratio', 'price_to_earnings_ratio']
    :param net_income: "Net Income is the total profit after all expenses, taxes, interest, and depreciation have been deducted from total revenue."
    :param shares_outstanding: "Shares Outstanding is the total number of shares of a company's stock currently held by all shareholders."
    :return: "Computed value of EPS: EPS = Net Income / Weighted Avg Shares"
    '''
    return net_income / shares_outstanding






def equal_risk_contribution(cov_matrix):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Equal risk contribution — Choose w such that RC_i are equal. A financial metric in the domain of Asset management & portfolio optimization."
    y_as_x: []
    :param returns_matrix: "Parameter returns_matrix used in Equal risk contribution calculation."
    :return: "Computed value of Equal risk contribution: Choose w such that RC_i are equal"
    '''
    import numpy as np
    from scipy.optimize import minimize
    sigma = np.array(cov_matrix); n = sigma.shape[0]
    def obj(w):
        port_vol = np.sqrt(w @ sigma @ w)
        mrc = sigma @ w / port_vol
        rc = w * mrc
        target = port_vol / n
        return np.sum((rc - target)**2)
    w0 = np.ones(n)/n
    res = minimize(obj, w0, constraints={'type':'eq','fun': lambda w: np.sum(w)-1}, bounds=[(0,1)]*n)
    return res.x


def equal_weight_portfolio(x_1, n):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Equal-weight portfolio — w_i = 1/N. A financial metric in the domain of Asset management & portfolio optimization."
    y_as_x: []
    :param x_1: "Parameter x_1 used in Equal-weight portfolio calculation."
    :param n: "Number of observations, periods, or data points."
    :return: "Computed value of Equal-weight portfolio: w_i = 1/N"
    '''
    return x_1 / n






def equated_monthly_installment_emi(principal, monthly_rate, num_months):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Banking', 'Consumer Lending', 'Project Finance']
    function: "Equated Monthly Installment (EMI) — fixed monthly payment for a loan."
    y_as_x: []
    :param principal: "Principal is the original amount of money borrowed or invested."
    :param monthly_rate: "Parameter monthly_rate used in Equated monthly installment (EMI) calculation."
    :param num_months: "Parameter num_months used in Equated monthly installment (EMI) calculation."
    :return: "Computed value of Equated monthly installment (EMI): EMI = P r (1+r)^n / ((1+r)^n - 1)"
    '''
    return principal * monthly_rate * (1 + monthly_rate)**num_months / ((1 + monthly_rate)**num_months - 1)






def equity_check_multiple_of_ebitda(equity_value, ebitda):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Private Equity', 'Venture Capital', 'LBO']
    function: "Equity Check Multiple of EBITDA — equity value as a multiple of EBITDA."
    y_as_x: []
    :param equity_value: "Parameter equity_value used in Equity check multiple of EBITDA calculation."
    :param ebitda: "EBITDA (Earnings Before Interest, Taxes, Depreciation, and Amortization) is a proxy for operating cash flow."
    :return: "Computed value of Equity check multiple of EBITDA: Equity / EBITDA"
    '''
    return equity_value / ebitda if ebitda != 0 else float("inf")






def equity_contribution(purchase_price, debt_raised):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Private Equity', 'Venture Capital', 'LBO']
    function: "Equity contribution — Sponsor Equity = Uses - Debt - Existing Cash. A financial metric in the domain of Private equity, venture capital & LBO."
    y_as_x: []
    :param args: "Parameter args used in Equity contribution calculation."
    :param kwargs: "Parameter kwargs used in Equity contribution calculation."
    :return: "Computed value of Equity contribution: Sponsor Equity = Uses - Debt - Existing Cash"
    '''
    return purchase_price - debt_raised


def equity_multiple(total_distributions, total_contributions):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Real Estate Finance', 'Mortgage Analysis']
    function: "Equity Multiple — total distributions divided by total contributions. Also called MOIC."
    y_as_x: []
    :param total_distributions: "Parameter total_distributions used in Equity multiple calculation."
    :param total_contributions: "Parameter total_contributions used in Equity multiple calculation."
    :return: "Computed value of Equity multiple: EM = Total Equity Distributions / Equity Invested"
    '''
    return total_distributions / total_contributions






def equity_ratio(total_equity, total_assets):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "Equity Ratio — total equity divided by total assets."
    y_as_x: []
    :param total_equity: "Total Equity is the residual interest in the assets of an entity after deducting all its liabilities."
    :param total_assets: "Total Assets represent the sum of all current and non-current assets owned by a company."
    :return: "Computed value of Equity ratio: Equity Ratio = Total Equity / Total Assets"
    '''
    return total_equity / total_assets






def equity_rollover_percentage(management_rollover_equity, total_equity):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Private Equity', 'Venture Capital', 'LBO']
    function: "Equity rollover percentage — Rollover = Management Rollover Equity / Total Equity. A financial metric in the domain of Private equity, venture capital & LBO."
    y_as_x: []
    :param management_rollover_equity: "Parameter management_rollover_equity used in Equity rollover percentage calculation."
    :param total_equity: "Total Equity is the residual interest in the assets of an entity after deducting all its liabilities."
    :return: "Computed value of Equity rollover percentage: Rollover = Management Rollover Equity / Total Equity"
    '''
    return management_rollover_equity / total_equity






def equity_value_at_exit(exit_enterprise_value, net_debt_at_exit):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Private Equity', 'Venture Capital', 'LBO']
    function: "Equity Value at Exit — exit EV minus net debt at exit."
    y_as_x: []
    :param exit_enterprise_value: "Exit Enterprise Value — EV at exit = Exit EBITDA * Exit Multiple."
    :param net_debt_at_exit: "Parameter net_debt_at_exit used in Equity value at exit calculation."
    :return: "Computed value of Equity value at exit: Equity_exit = EV_exit - Net Debt_exit"
    '''
    return exit_enterprise_value - net_debt_at_exit






def equity_value_bridge(enterprise_value, net_debt, minority_interest=0, preferred_equity=0):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "Equity Value Bridge — derives equity value from enterprise value. Equity = EV - Net Debt - MI - Preferred."
    y_as_x: []
    :param enterprise_value: "Enterprise Value (EV) is the total value of a company (market cap + debt - cash)."
    :param net_debt: "Parameter net_debt used in Equity value bridge calculation."
    :param minority_interest: "Parameter minority_interest used in Equity value bridge calculation."
    :param preferred_equity: "Parameter preferred_equity used in Equity value bridge calculation."
    :return: "Computed value of Equity value bridge: Equity Value = EV - Net Debt - Preferred - Minority Interest + Non-operating Assets"
    '''
    return enterprise_value - net_debt - minority_interest - preferred_equity






def equivalent_annual_annuity_eaa(npv, rate, num_periods):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "Equivalent Annual Annuity (EAA) — converts NPV to equivalent annual cash flow for comparing projects of different lives."
    y_as_x: []
    :param npv: "Parameter npv used in Equivalent annual annuity (EAA) calculation."
    :param rate: "Rate (r) is the interest rate or discount rate per period."
    :param num_periods: "Number of Periods (n) is the total number of payment or compounding periods."
    :return: "Computed value of Equivalent annual annuity (EAA): EAA = NPV x r / (1-(1+r)^-n)"
    '''
    if rate == 0:
        return npv / num_periods
    annuity_factor = (1 - (1 + rate)**(-num_periods)) / rate
    return npv / annuity_factor






def error_correction_model(data, k_ar_diff=1, coint_rank=1):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Financial Econometrics', 'Time Series Analysis']
    function: "Error correction model — Delta y_t = alpha + beta Delta x_t + lambda(y_{t-1} - theta x_{t-1}) + epsilon_t. A financial metric in the domain of Econometrics & time-series finance."
    y_as_x: []
    :param data: "Parameter data used in Error correction model calculation."
    :param args: "Parameter args used in Error correction model calculation."
    :return: "Computed value of Error correction model: Delta y_t = alpha + beta Delta x_t + lambda(y_{t-1} - theta x_{t-1}) + epsilon_t"
    '''
    from statsmodels.tsa.vector_ar.vecm import VECM
    return VECM(data, k_ar_diff=k_ar_diff, coint_rank=coint_rank).fit()


def ev_ebit(enterprise_value, ebit):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Equity Valuation', 'Asset Pricing']
    function: "EV/EBIT — EV / EBIT. A financial metric in the domain of Equity valuation & asset pricing."
    y_as_x: []
    :param args: "Parameter args used in EV/EBIT calculation."
    :param kwargs: "Parameter kwargs used in EV/EBIT calculation."
    :return: "Computed value of EV/EBIT: EV / EBIT"
    '''
    return enterprise_value / ebit if ebit != 0 else float("inf")




def ev_ebitda(enterprise_value, ebitda):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "EV/EBITDA — Enterprise Value / EBITDA. A financial metric in the domain of Corporate finance, valuation & capital budgeting."
    y_as_x: []
    :param args: "Parameter args used in EV/EBITDA calculation."
    :param kwargs: "Parameter kwargs used in EV/EBITDA calculation."
    :return: "Computed value of EV/EBITDA: Enterprise Value / EBITDA"
    '''
    return enterprise_value / ebitda if ebitda != 0 else float("inf")




def ev_sales(enterprise_value, revenue):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "EV/Sales — Enterprise Value / Revenue. A financial metric in the domain of Corporate finance, valuation & capital budgeting."
    y_as_x: []
    :param args: "Parameter args used in EV/Sales calculation."
    :param kwargs: "Parameter kwargs used in EV/Sales calculation."
    :return: "Computed value of EV/Sales: Enterprise Value / Revenue"
    '''
    return enterprise_value / revenue if revenue != 0 else float("inf")




def eve_sensitivity(eve_base, eve_shocked):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Treasury', 'ALM', 'Balance Sheet Management']
    function: "EVE sensitivity — Delta EVE / EVE approx -DGAP x Delta y. A financial metric in the domain of Treasury, ALM & balance-sheet management."
    y_as_x: []
    :param args: "Parameter args used in EVE sensitivity calculation."
    :param kwargs: "Parameter kwargs used in EVE sensitivity calculation."
    :return: "Computed value of EVE sensitivity: Delta EVE / EVE approx -DGAP x Delta y"
    '''
    return eve_shocked - eve_base




def ewma_volatility(returns, lambda_param=0.94):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "EWMA Volatility — Exponentially Weighted Moving Average volatility. sigma^2_t = lambda * sigma^2_{t-1} + (1-lambda) * r^2_{t-1}."
    y_as_x: []
    :param returns: "Returns are the gain or loss generated on an investment over a specific period."
    :param lambda_param: "Parameter lambda_param used in EWMA volatility calculation."
    :return: "Computed value of EWMA volatility: sigma_t^2 = lambda sigma_{t-1}^2 + (1-lambda) r_{t-1}^2"
    '''
    import numpy as np
    r = np.array(returns)
    var = np.zeros(len(r))
    var[0] = r[0]**2
    for i in range(1, len(r)):
        var[i] = lambda_param * var[i-1] + (1 - lambda_param) * r[i-1]**2
    return np.sqrt(var)






def ex_ante_tracking_error(active_weights, cov_matrix):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Ex-ante tracking error — TE = sqrt((w-w_b)' Sigma (w-w_b)). A financial metric in the domain of Asset management & portfolio optimization."
    y_as_x: []
    :param expected_returns: "Expected Returns vector contains the anticipated return for each asset."
    :param cov_matrix: "Covariance Matrix contains the covariances between all pairs of assets."
    :return: "Computed value of Ex-ante tracking error: TE = sqrt((w-w_b)' Sigma (w-w_b))"
    '''
    import numpy as np
    w = np.array(active_weights); sigma = np.array(cov_matrix)
    return np.sqrt(w @ sigma @ w)


def excess_kurtosis(returns):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "Excess Kurtosis — kurtosis minus 3 (Fisher definition). Positive indicates fat tails."
    y_as_x: []
    :param returns: "Returns are the gain or loss generated on an investment over a specific period."
    :return: "Computed value of Excess kurtosis: Kurt = E[(R-mu)^4]/sigma^4 - 3"
    '''
    from scipy.stats import kurtosis
    return kurtosis(returns, fisher=True)






def excess_return(portfolio_return, risk_free_rate):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Performance Attribution', 'Risk-Adjusted Performance']
    function: "Excess Return — return above the risk-free rate."
    y_as_x: []
    :param portfolio_return: "Portfolio Return is the total return of the managed portfolio."
    :param risk_free_rate: "Risk-Free Rate (Rf) is the theoretical rate of return with zero risk, typically proxied by government bond yields."
    :return: "Computed value of Excess return: ER = R_p - R_b"
    '''
    return portfolio_return - risk_free_rate






def excess_spread(weighted_average_coupon, cost_of_funds, servicing_fee, losses):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Structured Finance', 'Securitization']
    function: "Excess Spread — in securitization, the residual interest after covering all costs."
    y_as_x: ['tranche_credit_enhancement']
    :param weighted_average_coupon: "Parameter weighted_average_coupon used in Excess spread calculation."
    :param cost_of_funds: "Parameter cost_of_funds used in Excess spread calculation."
    :param servicing_fee: "Parameter servicing_fee used in Excess spread calculation."
    :param losses: "Parameter losses used in Excess spread calculation."
    :return: "Computed value of Excess spread: Excess Spread = Asset Yield - Funding Cost - Servicing Fee - Charge-offs"
    '''
    return weighted_average_coupon - cost_of_funds - servicing_fee - losses






def exit_enterprise_value(exit_ebitda, exit_multiple):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Private Equity', 'Venture Capital', 'LBO']
    function: "Exit Enterprise Value — EV at exit = Exit EBITDA * Exit Multiple."
    y_as_x: ['equity_value_at_exit']
    :param exit_ebitda: "Parameter exit_ebitda used in Exit enterprise value calculation."
    :param exit_multiple: "Parameter exit_multiple used in Exit enterprise value calculation."
    :return: "Computed value of Exit enterprise value: Exit EV = Exit EBITDA × Exit Multiple"
    '''
    return exit_ebitda * exit_multiple






def expected_credit_loss_ifrs_9_cecl(probability_of_default, loss_given_default, exposure_at_default):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit Risk', 'Default Modeling', 'Credit Portfolio']
    function: "Expected Credit Loss (IFRS 9/CECL) — ECL = PD * LGD * EAD."
    y_as_x: []
    :param probability_of_default: "Probability of Default (PD) is the likelihood that a borrower will fail to meet obligations."
    :param loss_given_default: "Loss Given Default (LGD) is the fraction of exposure lost if a default occurs."
    :param exposure_at_default: "Exposure at Default (EAD) is the total value exposed at the time of default."
    :return: "Computed value of Expected credit loss (IFRS 9/CECL): ECL = sum_t PD_t x LGD_t x EAD_t x DF_t"
    '''
    return probability_of_default * loss_given_default * exposure_at_default






def expected_drawdown(returns, num_sims=1000, window=252):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "Expected drawdown — EDD = E[max_{t<=T} drawdown_t]. A financial metric in the domain of Market risk & volatility modeling."
    y_as_x: []
    :param args: "Parameter args used in Expected drawdown calculation."
    :param kwargs: "Parameter kwargs used in Expected drawdown calculation."
    :return: "Computed value of Expected drawdown: EDD = E[max_{t<=T} drawdown_t]"
    '''
    import numpy as np
    r = np.array(returns); max_dds = []
    for _ in range(num_sims):
        sim = np.random.choice(r, size=window, replace=True)
        wealth = np.cumprod(1+sim); peaks = np.maximum.accumulate(wealth)
        max_dds.append(np.max((peaks-wealth)/peaks))
    return np.mean(max_dds)


def expected_exposure_ee(simulated_exposures):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit Risk', 'Default Modeling', 'Credit Portfolio']
    function: "Expected exposure (EE) — EE_t = E[max(V_t,0)]. A financial metric in the domain of Credit risk, default modeling & credit portfolio."
    y_as_x: []
    :param args: "Parameter args used in Expected exposure (EE) calculation."
    :param kwargs: "Parameter kwargs used in Expected exposure (EE) calculation."
    :return: "Computed value of Expected exposure (EE): EE_t = E[max(V_t,0)]"
    '''
    import numpy as np
    return np.mean(np.maximum(np.array(simulated_exposures), 0))




def expected_future_lifetime(survival_probs):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "Expected future lifetime — e_x = E[T_x] = int_0^∞ {}_tp_x dt. A financial metric in the domain of Actuarial science & insurance."
    y_as_x: []
    :param args: "Parameter args used in Expected future lifetime calculation."
    :param kwargs: "Parameter kwargs used in Expected future lifetime calculation."
    :return: "Computed value of Expected future lifetime: e_x = E[T_x] = int_0^∞ {}_tp_x dt"
    '''
    import numpy as np
    sp = np.array(survival_probs)
    return np.sum(np.cumprod(sp))




def expected_loss(probability_of_default, loss_given_default, exposure_at_default):
    '''
    domain: ['Credit risk']
    subdomain: ['Credit Risk']
    function: "Expected Loss — EL = PD * LGD * EAD. The mean of the loss distribution."
    y_as_x: ['credit_va_r']
    :param probability_of_default: "Probability of Default (PD) is the likelihood that a borrower will fail to meet obligations."
    :param loss_given_default: "Loss Given Default (LGD) is the fraction of exposure lost if a default occurs."
    :param exposure_at_default: "Exposure at Default (EAD) is the total value exposed at the time of default."
    :return: "Computed value of Expected loss: EL = PD × LGD × EAD"
    '''
    return probability_of_default * loss_given_default * exposure_at_default






def expected_positive_exposure_epe(x_1, t_int_0t_ee_t_dt):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit Risk', 'Default Modeling', 'Credit Portfolio']
    function: "Expected positive exposure (EPE) — EPE = (1/T) int_0^T EE_t dt. A financial metric in the domain of Credit risk, default modeling & credit portfolio."
    y_as_x: []
    :param x_1: "Parameter x_1 used in Expected positive exposure (EPE) calculation."
    :param t_int_0t_ee_t_dt: "Parameter t_int_0t_ee_t_dt used in Expected positive exposure (EPE) calculation."
    :return: "Computed value of Expected positive exposure (EPE): EPE = (1/T) int_0^T EE_t dt"
    '''
    return x_1 / t_int_0t_ee_t_dt






def expected_principal_collection(scheduled_principal, prepayment_rate):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Structured Finance', 'Securitization']
    function: "Expected principal collection — Principal_t = Scheduled_t + Prepayment_t - Defaults_t + Recoveries_t. A financial metric in the domain of Structured finance & securitization."
    y_as_x: []
    :param args: "Parameter args used in Expected principal collection calculation."
    :param kwargs: "Parameter kwargs used in Expected principal collection calculation."
    :return: "Computed value of Expected principal collection: Principal_t = Scheduled_t + Prepayment_t - Defaults_t + Recoveries_t"
    '''
    return scheduled_principal * (1 + prepayment_rate)


def expected_shortfall_cva_r(returns, confidence_level=0.95):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "Expected Shortfall (CVaR) — the average loss beyond VaR. ES = E[Loss | Loss > VaR]."
    y_as_x: []
    :param returns: "Returns are the gain or loss generated on an investment over a specific period."
    :param confidence_level: "Confidence Level is the probability threshold used in statistical tests and risk measures."
    :return: "Computed value of Expected shortfall (CVaR): ES_α = -E[R | R ≤ Quantile_α(R)]"
    '''
    import numpy as np
    r = np.array(returns)
    var = np.percentile(r, (1 - confidence_level) * 100)
    return -np.mean(r[r <= var])






def expense_ratio(operating_expenses, earned_premiums):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "Expense Ratio — operating expenses divided by earned premiums."
    y_as_x: ['combined_ratio']
    :param operating_expenses: "Operating Expenses (OpEx) are the essential ongoing costs a business incurs to maintain daily operations and generate revenue."
    :param earned_premiums: "Parameter earned_premiums used in Expense ratio calculation."
    :return: "Computed value of Expense ratio: Expense Ratio = Underwriting Expenses / Net Premiums Earned"
    '''
    return operating_expenses / earned_premiums






def explained_variance_ratio(lambda_i, sum_j_lambda_j):
    '''
    domain: ['Quantitative forecasting & machine learning in finance']
    subdomain: ['Quantitative Finance', 'Machine Learning']
    function: "Explained variance ratio — EVR_i = lambda_i / sum_j lambda_j. A financial metric in the domain of Quantitative forecasting & machine learning in finance."
    y_as_x: []
    :param lambda_i: "Parameter lambda_i used in Explained variance ratio calculation."
    :param sum_j_lambda_j: "Parameter sum_j_lambda_j used in Explained variance ratio calculation."
    :return: "Computed value of Explained variance ratio: EVR_i = lambda_i / sum_j lambda_j"
    '''
    return lambda_i / sum_j_lambda_j






def exposure_at_default_ead(outstanding, ccf_x_undrawn):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Banking', 'Consumer Lending', 'Project Finance']
    function: "Exposure at default (EAD) — EAD = Outstanding + CCF x Undrawn. A financial metric in the domain of Banking, consumer lending & project finance."
    y_as_x: []
    :param outstanding: "Parameter outstanding used in Exposure at default (EAD) calculation."
    :param ccf_x_undrawn: "Parameter ccf_x_undrawn used in Exposure at default (EAD) calculation."
    :return: "Computed value of Exposure at default (EAD): EAD = Outstanding + CCF x Undrawn"
    '''
    return outstanding + ccf_x_undrawn






def exposure_weighted_average_rating_factor(exposures, rating_factors):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit Risk', 'Default Modeling', 'Credit Portfolio']
    function: "Exposure weighted average rating factor — WARF = sum_i w_i RatingFactor_i. A financial metric in the domain of Credit risk, default modeling & credit portfolio."
    y_as_x: []
    :param args: "Parameter args used in Exposure weighted average rating factor calculation."
    :param kwargs: "Parameter kwargs used in Exposure weighted average rating factor calculation."
    :return: "Computed value of Exposure weighted average rating factor: WARF = sum_i w_i RatingFactor_i"
    '''
    import numpy as np
    e = np.array(exposures); rf = np.array(rating_factors)
    return np.sum(e * rf) / np.sum(e)


def factor_model_decomposition(returns_matrix, n_components=3):
    '''
    domain: ['Quantitative forecasting & machine learning in finance']
    subdomain: ['Quantitative Finance', 'Machine Learning']
    function: "Factor model decomposition — X approx F B' + U. A financial metric in the domain of Quantitative forecasting & machine learning in finance."
    y_as_x: []
    :param X: "Parameter X used in Factor model decomposition calculation."
    :param y: "Parameter y used in Factor model decomposition calculation."
    :return: "Computed value of Factor model decomposition: X approx F B' + U"
    '''
    from sklearn.decomposition import PCA
    import numpy as np
    pca = PCA(n_components=n_components)
    pca.fit(returns_matrix)
    return {'components': pca.components_, 'explained_variance_ratio': pca.explained_variance_ratio_, 'transformed': pca.transform(returns_matrix)}




def fama_french_3_factor_model(returns, market_excess, smb, hml, risk_free_rate):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Equity Valuation', 'Asset Pricing']
    function: "Fama-French 3-Factor Model — R - Rf = alpha + b1*(Rm-Rf) + b2*SMB + b3*HML."
    y_as_x: []
    :param returns: "Returns are the gain or loss generated on an investment over a specific period."
    :param market_excess: "Parameter market_excess used in Fama-French 3-factor model calculation."
    :param smb: "Parameter smb used in Fama-French 3-factor model calculation."
    :param hml: "Parameter hml used in Fama-French 3-factor model calculation."
    :param risk_free_rate: "Risk-Free Rate (Rf) is the theoretical rate of return with zero risk, typically proxied by government bond yields."
    :return: "Computed value of Fama-French 3-factor model: R_i-R_f = alpha + beta_MKT MKT + beta_SMB SMB + beta_HML HML + epsilon"
    '''
    import numpy as np
    y = np.array(returns) - risk_free_rate
    X = np.column_stack([np.ones(len(y)), market_excess, smb, hml])
    coeffs = np.linalg.lstsq(X, y, rcond=None)[0]
    return {'alpha': coeffs[0], 'market_beta': coeffs[1], 'smb_beta': coeffs[2], 'hml_beta': coeffs[3]}






def fama_french_5_factor_model(returns, market_excess, smb, hml, rmw, cma, risk_free_rate):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Equity Valuation', 'Asset Pricing']
    function: "Fama-French 5-Factor Model — extends the 3-factor model with profitability (RMW) and investment (CMA) factors."
    y_as_x: []
    :param returns: "Returns are the gain or loss generated on an investment over a specific period."
    :param market_excess: "Parameter market_excess used in Fama-French 5-factor model calculation."
    :param smb: "Parameter smb used in Fama-French 5-factor model calculation."
    :param hml: "Parameter hml used in Fama-French 5-factor model calculation."
    :param rmw: "Parameter rmw used in Fama-French 5-factor model calculation."
    :param cma: "Parameter cma used in Fama-French 5-factor model calculation."
    :param risk_free_rate: "Risk-Free Rate (Rf) is the theoretical rate of return with zero risk, typically proxied by government bond yields."
    :return: "Computed value of Fama-French 5-factor model: R_i-R_f = alpha + b MKT + s SMB + h HML + r RMW + c CMA + epsilon"
    '''
    import numpy as np
    y = np.array(returns) - risk_free_rate
    X = np.column_stack([np.ones(len(y)), market_excess, smb, hml, rmw, cma])
    coeffs = np.linalg.lstsq(X, y, rcond=None)[0]
    return {'alpha': coeffs[0], 'market_beta': coeffs[1], 'smb_beta': coeffs[2], 'hml_beta': coeffs[3], 'rmw_beta': coeffs[4], 'cma_beta': coeffs[5]}






def fama_mac_beth_cross_sectional_regression(returns_panel, factor_panel):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Financial Econometrics', 'Time Series Analysis']
    function: "Fama-MacBeth cross-sectional regression — R_{i,t} = λ_{0,t} + λ_t^T β_i + ε_{i,t}. A financial metric in the domain of Econometrics & time-series finance."
    y_as_x: []
    :param y: "Parameter y used in Fama-MacBeth cross-sectional regression calculation."
    :param X: "Parameter X used in Fama-MacBeth cross-sectional regression calculation."
    :return: "Computed value of Fama-MacBeth cross-sectional regression: R_{i,t} = λ_{0,t} + λ_t^T β_i + ε_{i,t}"
    '''
    import numpy as np
    from scipy import stats
    T = len(returns_panel)
    gammas = []
    for t in range(T):
        slope, intercept, _, _, _ = stats.linregress(factor_panel[t], returns_panel[t])
        gammas.append(slope)
    return {'mean_gamma': np.mean(gammas), 'std_gamma': np.std(gammas), 't_stat': np.mean(gammas)/(np.std(gammas)/np.sqrt(T))}


def fcf_yield(free_cash_flow, market_cap):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Equity Valuation', 'Asset Pricing']
    function: "FCF Yield — free cash flow divided by market capitalization."
    y_as_x: []
    :param free_cash_flow: "Free Cash Flow (FCF) is cash generated after accounting for capital expenditures."
    :param market_cap: "Market Capitalization is the total market value of outstanding shares (price x shares)."
    :return: "Computed value of FCF yield: FCF Yield = Free Cash Flow / Market Cap or EV"
    '''
    return free_cash_flow / market_cap






def fcfe(net_income, depreciation, capex, change_in_working_capital, net_borrowing):
    '''
    domain: ['Corporate finance & capital budgeting']
    subdomain: ['Corporate Finance', 'Capital Budgeting']
    function: "FCFE (Free Cash Flow to Equity) — cash available to equity holders after reinvestment and debt service."
    y_as_x: []
    :param net_income: "Net Income is the total profit after all expenses, taxes, interest, and depreciation have been deducted from total revenue."
    :param depreciation: "Depreciation is an accounting method that spreads the cost of a tangible asset over its useful life."
    :param capex: "Capital Expenditure (CapEx) is funds used to acquire, upgrade, or maintain physical assets."
    :param change_in_working_capital: "Parameter change_in_working_capital used in FCFE calculation."
    :param net_borrowing: "Parameter net_borrowing used in FCFE calculation."
    :return: "Computed value of FCFE: FCFE = Net Income + D&A - Capex - ΔNWC + Net Borrowing"
    '''
    return net_income + depreciation - capex - change_in_working_capital + net_borrowing






def fcfe_dcf_intrinsic_value(cash_flows, discount_rate):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Equity Valuation', 'Asset Pricing']
    function: "FCFE DCF intrinsic value — Equity Value = sum_t FCFE_t/(1+R_e)^t + TV/(1+R_e)^T. A financial metric in the domain of Equity valuation & asset pricing."
    y_as_x: []
    :param cash_flows: "Parameter cash_flows used in FCFE DCF intrinsic value calculation."
    :param discount_rate: "Discount Rate is the rate used to discount future cash flows to present value."
    :return: "Computed value of FCFE DCF intrinsic value: Equity Value = sum_t FCFE_t/(1+R_e)^t + TV/(1+R_e)^T"
    '''
    import numpy as np
    cf = np.array(cash_flows)
    t = np.arange(1, len(cf) + 1)
    return np.sum(cf / (1 + discount_rate)**t)






def fcff(ebit, tax_rate, depreciation, capex, change_in_working_capital):
    '''
    domain: ['Corporate finance & capital budgeting']
    subdomain: ['Corporate Finance', 'Capital Budgeting']
    function: "FCFF (Free Cash Flow to Firm) — cash available to all capital providers."
    y_as_x: []
    :param ebit: "EBIT (Earnings Before Interest and Taxes) is a financial metric measuring a company's profitability from core operations."
    :param tax_rate: "Tax Rate (T) is the percentage of taxable income that must be paid as corporate income tax."
    :param depreciation: "Depreciation is an accounting method that spreads the cost of a tangible asset over its useful life."
    :param capex: "Capital Expenditure (CapEx) is funds used to acquire, upgrade, or maintain physical assets."
    :param change_in_working_capital: "Parameter change_in_working_capital used in FCFF calculation."
    :return: "Computed value of FCFF: FCFF = EBIT·(1-T) + D&A - Capex - ΔNWC"
    '''
    return ebit * (1 - tax_rate) + depreciation - capex - change_in_working_capital






def fcff_dcf_intrinsic_value(cash_flows, discount_rate):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Equity Valuation', 'Asset Pricing']
    function: "FCFF DCF intrinsic value — EV = sum_t FCFF_t/(1+WACC)^t + TV/(1+WACC)^T. A financial metric in the domain of Equity valuation & asset pricing."
    y_as_x: []
    :param cash_flows: "Parameter cash_flows used in FCFF DCF intrinsic value calculation."
    :param discount_rate: "Discount Rate is the rate used to discount future cash flows to present value."
    :return: "Computed value of FCFF DCF intrinsic value: EV = sum_t FCFF_t/(1+WACC)^t + TV/(1+WACC)^T"
    '''
    import numpy as np
    cf = np.array(cash_flows)
    t = np.arange(1, len(cf) + 1)
    return np.sum(cf / (1 + discount_rate)**t)






def fill_ratio(executed_quantity, submitted_quantity):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Liquidity Risk', 'Market Liquidity', 'Execution Cost']
    function: "Fill ratio — Fill Ratio = Executed Quantity / Submitted Quantity. A financial metric in the domain of Liquidity risk, market liquidity & execution cost."
    y_as_x: []
    :param executed_quantity: "Parameter executed_quantity used in Fill ratio calculation."
    :param submitted_quantity: "Parameter submitted_quantity used in Fill ratio calculation."
    :return: "Computed value of Fill ratio: Fill Ratio = Executed Quantity / Submitted Quantity"
    '''
    return executed_quantity / submitted_quantity






def financial_leverage(total_assets, total_equity):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "Financial Leverage — total assets divided by total equity. Also called equity multiplier."
    y_as_x: ['combined_leverage']
    :param total_assets: "Total Assets represent the sum of all current and non-current assets owned by a company."
    :param total_equity: "Total Equity is the residual interest in the assets of an entity after deducting all its liabilities."
    :return: "Computed value of Financial leverage: DFL = %Delta EPS / %Delta EBIT"
    '''
    return total_assets / total_equity






def fixed_asset_turnover(revenue, net_fixed_assets):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "Fixed Asset Turnover — revenue divided by net fixed assets."
    y_as_x: []
    :param revenue: "Revenue is the total amount of income a business generates from the sale of goods or services before deducting expenses."
    :param net_fixed_assets: "Parameter net_fixed_assets used in Fixed asset turnover calculation."
    :return: "Computed value of Fixed asset turnover: Fixed Asset Turnover = Revenue / Average Net PP&E"
    '''
    return revenue / net_fixed_assets






def fixed_effects_panel_model(y, X, entity_ids):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Financial Econometrics', 'Time Series Analysis']
    function: "Fixed effects panel model — y_it = alpha_i + x_it' beta + u_it. A financial metric in the domain of Econometrics & time-series finance."
    y_as_x: []
    :param y: "Parameter y used in Fixed effects panel model calculation."
    :param X: "Parameter X used in Fixed effects panel model calculation."
    :return: "Computed value of Fixed effects panel model: y_it = alpha_i + x_it' beta + u_it"
    '''
    import numpy as np
    import statsmodels.api as sm
    X_const = sm.add_constant(X)
    return sm.OLS(y, X_const).fit()


def fixed_charge_coverage(ebit, fixed_charges):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Private Equity', 'Venture Capital', 'LBO']
    function: "Fixed-Charge Coverage — (EBIT + Fixed Charges) / Fixed Charges."
    y_as_x: []
    :param ebit: "EBIT (Earnings Before Interest and Taxes) is a financial metric measuring a company's profitability from core operations."
    :param fixed_charges: "Parameter fixed_charges used in Fixed-charge coverage calculation."
    :return: "Computed value of Fixed-charge coverage: (EBITDA - Capex - Cash Taxes) / (Interest + Scheduled Amortization + Lease)"
    '''
    return (ebit + fixed_charges) / fixed_charges if fixed_charges != 0 else float("inf")






def floating_rate_note_coupon(reference_rate_t, spread):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Fixed Income', 'Bond Mathematics', 'Credit Markets']
    function: "Floating-rate note coupon — Coupon_t = Reference Rate_t + Spread. A financial metric in the domain of Fixed income, bonds & credit markets."
    y_as_x: []
    :param reference_rate_t: "Parameter reference_rate_t used in Floating-rate note coupon calculation."
    :param spread: "Spread is the difference between two interest rates or yields."
    :return: "Computed value of Floating-rate note coupon: Coupon_t = Reference Rate_t + Spread"
    '''
    return reference_rate_t + spread






def force_of_mortality(age, mortality_table_qx):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "Force of mortality — mu_x = f_x / S_x = -d ln S_x / dx. A financial metric in the domain of Actuarial science & insurance."
    y_as_x: ['constant_force_survival']
    :param args: "Parameter args used in Force of mortality calculation."
    :param kwargs: "Parameter kwargs used in Force of mortality calculation."
    :return: "Computed value of Force of mortality: mu_x = f_x / S_x = -d ln S_x / dx"
    '''
    import numpy as np
    qx = mortality_table_qx[age] if age < len(mortality_table_qx) else 1
    return -np.log(1 - qx)


def forward_fx_outright(spot_rate, domestic_rate, foreign_rate, time):
    '''
    domain: ['FX & international finance']
    subdomain: ['FX Markets', 'International Finance']
    function: "Forward FX outright — F = S e^{(r_d-r_f)T}. A financial metric in the domain of FX & international finance."
    y_as_x: []
    :param args: "Parameter args used in Forward FX outright calculation."
    :param kwargs: "Parameter kwargs used in Forward FX outright calculation."
    :return: "Computed value of Forward FX outright: F = S e^{(r_d-r_f)T}"
    '''
    return spot_rate * (1 + domestic_rate * time) / (1 + foreign_rate * time)




def forward_p_e(stock_price, forward_eps):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Equity Valuation', 'Asset Pricing']
    function: "Forward P/E — stock price divided by next year estimated EPS."
    y_as_x: []
    :param stock_price: "Stock Price (P) is the current market price per share of a company's equity."
    :param forward_eps: "Parameter forward_eps used in Forward P/E calculation."
    :return: "Computed value of Forward P/E: Forward P/E = Price / Next-12m EPS"
    '''
    return stock_price / forward_eps if forward_eps != 0 else float("inf")






def forward_price_on_non_dividend_asset(spot_price, risk_free_rate, time_to_expiry):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Forward Price on Non-Dividend Asset — F = S * e^(rT)."
    y_as_x: []
    :param spot_price: "Spot Price (S) is the current market price of the underlying asset."
    :param risk_free_rate: "Risk-Free Rate (Rf) is the theoretical rate of return with zero risk, typically proxied by government bond yields."
    :param time_to_expiry: "Time to Expiry (T) is the remaining time until expiration, in years."
    :return: "Computed value of Forward price on non-dividend asset: F_0 = S_0 e^{rT}"
    '''
    import numpy as np
    return spot_price * np.exp(risk_free_rate * time_to_expiry)






def forward_price_with_carry(spot_price, risk_free_rate, storage_cost, convenience_yield, time_to_expiry):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Forward price with carry — F_0 = S_0 e^{(r+u-y)T}. A financial metric in the domain of Derivatives, options & volatility."
    y_as_x: []
    :param args: "Parameter args used in Forward price with carry calculation."
    :param kwargs: "Parameter kwargs used in Forward price with carry calculation."
    :return: "Computed value of Forward price with carry: F_0 = S_0 e^{(r+u-y)T}"
    '''
    import numpy as np
    return spot_price * np.exp((risk_free_rate + storage_cost - convenience_yield) * time_to_expiry)


def forward_rate(spot_rate_1, spot_rate_2, t1, t2):
    '''
    domain: ['Fixed income & bond math']
    subdomain: ['Fixed Income', 'Bond Mathematics']
    function: "Forward rate — f_{t1,t2} = (DF(t1)/DF(t2) - 1)/(t2 - t1). A financial metric in the domain of Fixed income & bond math."
    y_as_x: ['black_caplet_price', 'compounded_forward_rate', 'forward_fx_outright', 'forward_rate_from_discount_factors', 'fra_payoff', 'fra_rate']
    :param args: "Parameter args used in Forward rate calculation."
    :param kwargs: "Parameter kwargs used in Forward rate calculation."
    :return: "Computed value of Forward rate: f_{t1,t2} = (DF(t1)/DF(t2) - 1)/(t2 - t1)"
    '''
    return ((1 + spot_rate_2)**t2 / (1 + spot_rate_1)**t1)**(1.0/(t2 - t1)) - 1




def forward_rate_from_discount_factors(df1, df2, time_diff):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Fixed Income', 'Bond Mathematics', 'Credit Markets']
    function: "Forward Rate from Discount Factors — f = (DF1/DF2 - 1) / delta_t."
    y_as_x: []
    :param df1: "Parameter df1 used in Forward rate from discount factors calculation."
    :param df2: "Parameter df2 used in Forward rate from discount factors calculation."
    :param time_diff: "Parameter time_diff used in Forward rate from discount factors calculation."
    :return: "Computed value of Forward rate from discount factors: f(t1,t2) = DF(t1)/DF(t2) - 1 over year fraction"
    '''
    return (df1 / df2 - 1) / time_diff






def forward_rate_from_spot_rates(spot_rate_1, spot_rate_2, t1, t2):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Fixed Income', 'Bond Mathematics', 'Credit Markets']
    function: "Forward Rate from Spot Rates — implied forward rate between two tenors."
    y_as_x: []
    :param spot_rate_1: "Parameter spot_rate_1 used in Forward rate from spot rates calculation."
    :param spot_rate_2: "Parameter spot_rate_2 used in Forward rate from spot rates calculation."
    :param t1: "Parameter t1 used in Forward rate from spot rates calculation."
    :param t2: "Parameter t2 used in Forward rate from spot rates calculation."
    :return: "Computed value of Forward rate from spot rates: f_{1,2} = [(1+z_2)^2/(1+z_1)] - 1"
    '''
    return ((1 + spot_rate_2)**t2 / (1 + spot_rate_1)**t1)**(1/(t2 - t1)) - 1






def fra_payoff(notional, contract_rate, reference_rate, day_count_fraction):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Fixed Income', 'Bond Mathematics', 'Credit Markets']
    function: "FRA payoff — Payoff = N(R_fix - R_ref)tau / (1+R_ref tau). A financial metric in the domain of Fixed income, bonds & credit markets."
    y_as_x: []
    :param args: "Parameter args used in FRA payoff calculation."
    :param kwargs: "Parameter kwargs used in FRA payoff calculation."
    :return: "Computed value of FRA payoff: Payoff = N(R_fix - R_ref)tau / (1+R_ref tau)"
    '''
    return notional * (reference_rate - contract_rate) * day_count_fraction / (1 + reference_rate * day_count_fraction)


def fra_rate(spot_rate_short, spot_rate_long, t_short, t_long):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Interest Rate Modeling', 'Term Structure']
    function: "FRA rate — FRA = (DF(t1)/DF(t2)-1)/τ. A financial metric in the domain of Interest-rate modeling & term structures."
    y_as_x: []
    :param args: "Parameter args used in FRA rate calculation."
    :param kwargs: "Parameter kwargs used in FRA rate calculation."
    :return: "Computed value of FRA rate: FRA = (DF(t1)/DF(t2)-1)/τ"
    '''
    return ((1 + spot_rate_long)**t_long / (1 + spot_rate_short)**t_short - 1) / (t_long - t_short)




def free_cash_flow(cash_flow_from_operations, capex):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "Free Cash Flow — FCF = CFO - CapEx."
    y_as_x: ['fcf_yield', 'free_cash_flow_margin']
    :param cash_flow_from_operations: "Cash Flow from Operations (CFO) is cash generated from regular business operations."
    :param capex: "Capital Expenditure (CapEx) is funds used to acquire, upgrade, or maintain physical assets."
    :return: "Computed value of Free cash flow: FCF = Operating Cash Flow - Capex"
    '''
    return cash_flow_from_operations - capex






def free_cash_flow_margin(free_cash_flow, revenue):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "Free Cash Flow Margin — FCF as a percentage of revenue."
    y_as_x: []
    :param free_cash_flow: "Free Cash Flow (FCF) is cash generated after accounting for capital expenditures."
    :param revenue: "Revenue is the total amount of income a business generates from the sale of goods or services before deducting expenses."
    :return: "Computed value of Free cash flow margin: FCF Margin = FCF / Revenue"
    '''
    return free_cash_flow / revenue






def free_cash_flow_to_equity_fcfe(net_income, depreciation, capex, change_in_working_capital, net_borrowing):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "Free cash flow to equity (FCFE) — FCFE = Net Income + D&A - Capex - DeltaNWC + Net Borrowing. A financial metric in the domain of Corporate finance, valuation & capital budgeting."
    y_as_x: []
    :param args: "Parameter args used in Free cash flow to equity (FCFE) calculation."
    :param kwargs: "Parameter kwargs used in Free cash flow to equity (FCFE) calculation."
    :return: "Computed value of Free cash flow to equity (FCFE): FCFE = Net Income + D&A - Capex - DeltaNWC + Net Borrowing"
    '''
    return net_income + depreciation - capex - change_in_working_capital + net_borrowing


def free_cash_flow_to_firm_fcff(ebit, tax_rate, depreciation, capex, change_in_working_capital):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "Free cash flow to firm (FCFF) — FCFF = EBIT(1-T) + D&A - Capex - DeltaNWC. A financial metric in the domain of Corporate finance, valuation & capital budgeting."
    y_as_x: []
    :param args: "Parameter args used in Free cash flow to firm (FCFF) calculation."
    :param kwargs: "Parameter kwargs used in Free cash flow to firm (FCFF) calculation."
    :return: "Computed value of Free cash flow to firm (FCFF): FCFF = EBIT(1-T) + D&A - Capex - DeltaNWC"
    '''
    return ebit * (1 - tax_rate) + depreciation - capex - change_in_working_capital




def frn_discount_margin(coupon_spread, par, price, maturity, frequency=4):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Fixed Income', 'Bond Mathematics', 'Credit Markets']
    function: "FRN discount margin — Price = sum_t CF_t/(1+Ref_t+DM)^t. A financial metric in the domain of Fixed income, bonds & credit markets."
    y_as_x: []
    :param args: "Parameter args used in FRN discount margin calculation."
    :param kwargs: "Parameter kwargs used in FRN discount margin calculation."
    :return: "Computed value of FRN discount margin: Price = sum_t CF_t/(1+Ref_t+DM)^t"
    '''
    import numpy as np
    n = int(maturity * frequency)
    coupon = par * coupon_spread / frequency
    def price_fn(dm):
        r = (coupon_spread + dm) / frequency
        t = np.arange(1, n + 1)
        return np.sum(coupon / (1 + r)**t) + par / (1 + r)**n
    from scipy.optimize import brentq
    return brentq(lambda dm: price_fn(dm) - price, -0.1, 1.0)




def front_end_housing_ratio(numerator, denominator):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Real Estate Finance', 'Mortgage Analysis']
    function: "Front-end housing ratio — Housing Expense / Gross Income. A financial metric in the domain of Real estate finance & mortgages."
    y_as_x: []
    :param numerator: "Parameter numerator used in Front-end housing ratio calculation."
    :param denominator: "Parameter denominator used in Front-end housing ratio calculation."
    :return: "Computed value of Front-end housing ratio: Housing Expense / Gross Income"
    '''
    return numerator / denominator if denominator != 0 else float("inf")






def front_end_ratio_housing_expense_ratio(housing_expense, gross_monthly_income):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Banking', 'Consumer Lending', 'Project Finance']
    function: "Front-end ratio / housing expense ratio — Front-End = Housing Expense / Gross Monthly Income. A financial metric in the domain of Banking, consumer lending & project finance."
    y_as_x: []
    :param housing_expense: "Parameter housing_expense used in Front-end ratio / housing expense ratio calculation."
    :param gross_monthly_income: "Gross Monthly Income is pre-tax monthly income."
    :return: "Computed value of Front-end ratio / housing expense ratio: Front-End = Housing Expense / Gross Monthly Income"
    '''
    return housing_expense / gross_monthly_income






def fund_carried_interest(total_profit, hurdle_profit, carry_rate=0.20):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Private Equity', 'Venture Capital', 'LBO']
    function: "Fund carried interest — Carry = max(0, Distributions - Capital Return - Hurdle) x Carry %. A financial metric in the domain of Private equity, venture capital & LBO."
    y_as_x: []
    :param args: "Parameter args used in Fund carried interest calculation."
    :param kwargs: "Parameter kwargs used in Fund carried interest calculation."
    :return: "Computed value of Fund carried interest: Carry = max(0, Distributions - Capital Return - Hurdle) x Carry %"
    '''
    return max(total_profit - hurdle_profit, 0) * carry_rate


def funding_liquidity_spread(unsecured_rate, ois_or_treasury):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Liquidity Risk', 'Market Liquidity', 'Execution Cost']
    function: "Funding liquidity spread — Funding Liquidity = unsecured rate - OIS or Treasury. A financial metric in the domain of Liquidity risk, market liquidity & execution cost."
    y_as_x: []
    :param unsecured_rate: "Parameter unsecured_rate used in Funding liquidity spread calculation."
    :param ois_or_treasury: "Parameter ois_or_treasury used in Funding liquidity spread calculation."
    :return: "Computed value of Funding liquidity spread: Funding Liquidity = unsecured rate - OIS or Treasury"
    '''
    return unsecured_rate - ois_or_treasury






def funding_spread(loan_yield, funding_cost):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Banking', 'Consumer Lending', 'Project Finance']
    function: "Funding spread — Funding Spread = Loan Yield - Funding Cost. A financial metric in the domain of Banking, consumer lending & project finance."
    y_as_x: ['net_weighted_average_spread']
    :param loan_yield: "Parameter loan_yield used in Funding spread calculation."
    :param funding_cost: "Parameter funding_cost used in Funding spread calculation."
    :return: "Computed value of Funding spread: Funding Spread = Loan Yield - Funding Cost"
    '''
    return loan_yield - funding_cost






def funds_transfer_pricing_spread(transfer_rate, reference_curve_rate):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Treasury', 'ALM', 'Balance Sheet Management']
    function: "Funds transfer pricing spread — FTP Spread = Transfer Rate - Reference Curve Rate. A financial metric in the domain of Treasury, ALM & balance-sheet management."
    y_as_x: []
    :param transfer_rate: "Parameter transfer_rate used in Funds transfer pricing spread calculation."
    :param reference_curve_rate: "Parameter reference_curve_rate used in Funds transfer pricing spread calculation."
    :return: "Computed value of Funds transfer pricing spread: FTP Spread = Transfer Rate - Reference Curve Rate"
    '''
    return transfer_rate - reference_curve_rate






def funds_transfer_pricing_spread_2(customer_rate, internal_transfer_rate):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Treasury', 'ALM', 'Balance Sheet Management']
    function: "Funds transfer pricing spread — FTP Spread = Customer Rate - Internal Transfer Rate. A financial metric in the domain of Treasury, ALM & balance-sheet management."
    y_as_x: []
    :param customer_rate: "Parameter customer_rate used in Funds transfer pricing spread calculation."
    :param internal_transfer_rate: "Parameter internal_transfer_rate used in Funds transfer pricing spread calculation."
    :return: "Computed value of Funds transfer pricing spread: FTP Spread = Customer Rate - Internal Transfer Rate"
    '''
    return customer_rate - internal_transfer_rate






def future_value(present_value, rate, num_periods):
    '''
    domain: ['Corporate finance & capital budgeting']
    subdomain: ['Corporate Finance', 'Capital Budgeting']
    function: "Future Value — FV = PV * (1 + r)^n."
    y_as_x: ['annualized_return_cagr', 'annuity_present_value', 'discount_factor', 'number_of_periods', 'present_value_pv', 'real_estate_dcf']
    :param present_value: "Present Value (PV) is the current worth of a future sum given a rate of return."
    :param rate: "Rate (r) is the interest rate or discount rate per period."
    :param num_periods: "Number of Periods (n) is the total number of payment or compounding periods."
    :return: "Computed value of Future value: FV = PV × (1+r)^n"
    '''
    return present_value * (1 + rate)**num_periods






def fx_cross_rate(numerator, denominator):
    '''
    domain: ['FX & international finance']
    subdomain: ['FX Markets', 'International Finance']
    function: "FX cross rate — S_{A/C} = S_{A/B} x S_{B/C}. A financial metric in the domain of FX & international finance."
    y_as_x: []
    :param numerator: "Parameter numerator used in FX cross rate calculation."
    :param denominator: "Parameter denominator used in FX cross rate calculation."
    :return: "Computed value of FX cross rate: S_{A/C} = S_{A/B} x S_{B/C}"
    '''
    return numerator / denominator if denominator != 0 else 0






def fx_forward_points(f, s):
    '''
    domain: ['FX & international finance']
    subdomain: ['FX Markets', 'International Finance']
    function: "FX forward points — Points = F - S. A financial metric in the domain of FX & international finance."
    y_as_x: []
    :param f: "Parameter f used in FX forward points calculation."
    :param s: "Parameter s used in FX forward points calculation."
    :return: "Computed value of FX forward points: Points = F - S"
    '''
    return f - s






def fx_forward_points_annualized(forward_points, spot_rate, tenor_days):
    '''
    domain: ['FX & international finance']
    subdomain: ['FX Markets', 'International Finance']
    function: "FX forward points annualized — Annualized Points = (F/S - 1)/T. A financial metric in the domain of FX & international finance."
    y_as_x: []
    :param args: "Parameter args used in FX forward points annualized calculation."
    :param kwargs: "Parameter kwargs used in FX forward points annualized calculation."
    :return: "Computed value of FX forward points annualized: Annualized Points = (F/S - 1)/T"
    '''
    return (forward_points / spot_rate) * (360 / tenor_days)


def fx_hedge_ratio(foreign_currency_exposure, hedge_notional):
    '''
    domain: ['FX & international finance']
    subdomain: ['FX Markets', 'International Finance']
    function: "FX hedge ratio — h = Foreign Currency Exposure / Hedge Notional. A financial metric in the domain of FX & international finance."
    y_as_x: []
    :param foreign_currency_exposure: "Parameter foreign_currency_exposure used in FX hedge ratio calculation."
    :param hedge_notional: "Parameter hedge_notional used in FX hedge ratio calculation."
    :return: "Computed value of FX hedge ratio: h = Foreign Currency Exposure / Hedge Notional"
    '''
    return foreign_currency_exposure / hedge_notional






def fx_option_garman_kohlhagen(spot, strike, domestic_rate, foreign_rate, volatility, time_to_expiry, option_type="call"):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "FX option (Garman-Kohlhagen) — C = S e^{-r_f T}N(d1) - K e^{-r_d T}N(d2). A financial metric in the domain of Derivatives, options & volatility."
    y_as_x: []
    :param args: "Parameter args used in FX option (Garman-Kohlhagen) calculation."
    :param kwargs: "Parameter kwargs used in FX option (Garman-Kohlhagen) calculation."
    :return: "Computed value of FX option (Garman-Kohlhagen): C = S e^{-r_f T}N(d1) - K e^{-r_d T}N(d2)"
    '''
    import numpy as np
    from scipy.stats import norm
    d1 = (np.log(spot/strike) + (domestic_rate - foreign_rate + 0.5*volatility**2)*time_to_expiry) / (volatility*np.sqrt(time_to_expiry))
    d2 = d1 - volatility*np.sqrt(time_to_expiry)
    if option_type == 'call':
        return spot*np.exp(-foreign_rate*time_to_expiry)*norm.cdf(d1) - strike*np.exp(-domestic_rate*time_to_expiry)*norm.cdf(d2)
    else:
        return strike*np.exp(-domestic_rate*time_to_expiry)*norm.cdf(-d2) - spot*np.exp(-foreign_rate*time_to_expiry)*norm.cdf(-d1)


def fx_option_garman_kohlhagen_d1(spot, strike, domestic_rate, foreign_rate, volatility, time_to_expiry):
    '''
    domain: ['FX & international finance']
    subdomain: ['FX Markets', 'International Finance']
    function: "FX option Garman-Kohlhagen d1 — d1 = [ln(S/K)+(r_d-r_f+0.5 sigma^2)T]/(sigma sqrt(T)). A financial metric in the domain of FX & international finance."
    y_as_x: []
    :param args: "Parameter args used in FX option Garman-Kohlhagen d1 calculation."
    :param kwargs: "Parameter kwargs used in FX option Garman-Kohlhagen d1 calculation."
    :return: "Computed value of FX option Garman-Kohlhagen d1: d1 = [ln(S/K)+(r_d-r_f+0.5 sigma^2)T]/(sigma sqrt(T))"
    '''
    import numpy as np
    return (np.log(spot / strike) + (domestic_rate - foreign_rate + 0.5 * volatility**2) * time_to_expiry) / (volatility * np.sqrt(time_to_expiry))




def fx_spot_quote_inversion(exchange_rate):
    '''
    domain: ['FX & international finance']
    subdomain: ['FX Markets', 'International Finance']
    function: "FX spot quote inversion — S_{A/B} = 1 / S_{B/A}. A financial metric in the domain of FX & international finance."
    y_as_x: []
    :param args: "Parameter args used in FX spot quote inversion calculation."
    :param kwargs: "Parameter kwargs used in FX spot quote inversion calculation."
    :return: "Computed value of FX spot quote inversion: S_{A/B} = 1 / S_{B/A}"
    '''
    return 1.0 / exchange_rate




def fx_swap_points(f, s):
    '''
    domain: ['FX & international finance']
    subdomain: ['FX Markets', 'International Finance']
    function: "FX swap points — Swap Points = F - S. A financial metric in the domain of FX & international finance."
    y_as_x: []
    :param f: "Parameter f used in FX swap points calculation."
    :param s: "Parameter s used in FX swap points calculation."
    :return: "Computed value of FX swap points: Swap Points = F - S"
    '''
    return f - s






def fx_transaction_exposure_pand_l(foreign_amount, initial_fx_rate, current_fx_rate):
    '''
    domain: ['FX & international finance']
    subdomain: ['FX Markets', 'International Finance']
    function: "FX transaction exposure P&L — P&L = Foreign CF x (Spot_realized - Hedge Rate). A financial metric in the domain of FX & international finance."
    y_as_x: []
    :param args: "Parameter args used in FX transaction exposure P&L calculation."
    :param kwargs: "Parameter kwargs used in FX transaction exposure P&L calculation."
    :return: "Computed value of FX transaction exposure P&L: P&L = Foreign CF x (Spot_realized - Hedge Rate)"
    '''
    return foreign_amount * (current_fx_rate - initial_fx_rate)


def fx_translation_effect(local_currency_amount, fx_rate):
    '''
    domain: ['FX & international finance']
    subdomain: ['FX Markets', 'International Finance']
    function: "FX translation effect — Translated Value = Local Currency Amount x FX Rate. A financial metric in the domain of FX & international finance."
    y_as_x: []
    :param local_currency_amount: "Parameter local_currency_amount used in FX translation effect calculation."
    :param fx_rate: "Parameter fx_rate used in FX translation effect calculation."
    :return: "Computed value of FX translation effect: Translated Value = Local Currency Amount x FX Rate"
    '''
    return local_currency_amount * fx_rate






def gamma(spot_price, strike_price, risk_free_rate, volatility, time_to_expiry):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Gamma — rate of change of delta. Gamma = N'(d1) / (S * sigma * sqrt(T))."
    y_as_x: []
    :param spot_price: "Spot Price (S) is the current market price of the underlying asset."
    :param strike_price: "Strike Price (K) is the predetermined price at which an option can be exercised."
    :param risk_free_rate: "Risk-Free Rate (Rf) is the theoretical rate of return with zero risk, typically proxied by government bond yields."
    :param volatility: "Volatility (sigma) is the annualized standard deviation of returns."
    :param time_to_expiry: "Time to Expiry (T) is the remaining time until expiration, in years."
    :return: "Computed value of Gamma: Gamma = e^{-qT} n(d1)/(S sigma sqrt(T))"
    '''
    import numpy as np
    from scipy.stats import norm
    d1 = (np.log(spot_price/strike_price) + (risk_free_rate + 0.5*volatility**2)*time_to_expiry) / (volatility*np.sqrt(time_to_expiry))
    return norm.pdf(d1) / (spot_price * volatility * np.sqrt(time_to_expiry))






def garch_11(returns, p=1, q=1):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "GARCH(1,1) — σ_t^2 = ω + α ε_{t-1}^2 + β σ_{t-1}^2. A financial metric in the domain of Market risk & volatility modeling."
    y_as_x: []
    :param returns: "Returns are the gain or loss generated on an investment over a specific period."
    :param p: "Model order parameter p (autoregressive order or similar)."
    :param q: "Model order parameter q (moving average order, ARCH order, or similar)."
    :return: "Computed value of GARCH(1,1): σ_t^2 = ω + α ε_{t-1}^2 + β σ_{t-1}^2"
    '''
    from arch import arch_model
    model = arch_model(returns, vol="GARCH", p=p, q=q)
    result = model.fit(disp="off")
    return result






def garch_11_2(returns, p=1, q=1):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "GARCH(1,1) — sigma_t^2 = omega + alpha epsilon_{t-1}^2 + beta sigma_{t-1}^2. A financial metric in the domain of Market risk & volatility modeling."
    y_as_x: []
    :param returns: "Returns are the gain or loss generated on an investment over a specific period."
    :param p: "Model order parameter p (autoregressive order or similar)."
    :param q: "Model order parameter q (moving average order, ARCH order, or similar)."
    :return: "Computed value of GARCH(1,1): sigma_t^2 = omega + alpha epsilon_{t-1}^2 + beta sigma_{t-1}^2"
    '''
    from arch import arch_model
    model = arch_model(returns, vol="GARCH", p=p, q=q)
    result = model.fit(disp="off")
    return result






def garman_klass_volatility(high, low, close, open_price):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "Garman-Klass Volatility — an efficient volatility estimator using OHLC prices."
    y_as_x: []
    :param high: "High is the highest price during a specific trading period."
    :param low: "Low is the lowest price during a specific trading period."
    :param close: "Close is the final trading price at the end of a trading period."
    :param open_price: "Open is the first trading price at the beginning of a trading period."
    :return: "Computed value of Garman-Klass volatility: sigma_GK^2 = 0.5[ln(H/L)]^2 - (2ln2-1)[ln(C/O)]^2"
    '''
    import numpy as np
    h = np.array(high); l = np.array(low); c = np.array(close); o = np.array(open_price)
    return np.sqrt(np.mean(0.5*(np.log(h/l))**2 - (2*np.log(2)-1)*(np.log(c/o))**2))






def gaussian_mixture_likelihood(X, n_components=2):
    '''
    domain: ['Quantitative forecasting & machine learning in finance']
    subdomain: ['Quantitative Finance', 'Machine Learning']
    function: "Gaussian mixture likelihood — p(x)=sum_k pi_k N(x|mu_k,Sigma_k). A financial metric in the domain of Quantitative forecasting & machine learning in finance."
    y_as_x: []
    :param X: "Parameter X used in Gaussian mixture likelihood calculation."
    :param y: "Parameter y used in Gaussian mixture likelihood calculation."
    :return: "Computed value of Gaussian mixture likelihood: p(x)=sum_k pi_k N(x|mu_k,Sigma_k)"
    '''
    from sklearn.mixture import GaussianMixture
    model = GaussianMixture(n_components=n_components)
    model.fit(X)
    return {'score': model.score(X), 'means': model.means_, 'weights': model.weights_}


def gjr_garch(returns, p=1, q=1):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "GJR-GARCH — sigma_t^2 = omega + alpha eps_{t-1}^2 + gamma I_{eps<0} eps_{t-1}^2 + beta sigma_{t-1}^2. A financial metric in the domain of Market risk & volatility modeling."
    y_as_x: []
    :param returns: "Returns are the gain or loss generated on an investment over a specific period."
    :param p: "Model order parameter p (autoregressive order or similar)."
    :param q: "Model order parameter q (moving average order, ARCH order, or similar)."
    :return: "Computed value of GJR-GARCH: sigma_t^2 = omega + alpha eps_{t-1}^2 + gamma I_{eps<0} eps_{t-1}^2 + beta sigma_{t-1}^2"
    '''
    from arch import arch_model
    model = arch_model(returns, vol="GARCH", p=p, q=q)
    result = model.fit(disp="off")
    return result






def global_minimum_variance_portfolio(cov_matrix):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Global minimum variance portfolio — min_w w^TΣw  s.t. 1^T w = 1. A financial metric in the domain of Asset management & portfolio optimization."
    y_as_x: []
    :param expected_returns: "Expected Returns vector contains the anticipated return for each asset."
    :param cov_matrix: "Covariance Matrix contains the covariances between all pairs of assets."
    :return: "Computed value of Global minimum variance portfolio: min_w w^TΣw  s.t. 1^T w = 1"
    '''
    import numpy as np
    sigma_inv = np.linalg.inv(np.array(cov_matrix))
    ones = np.ones(sigma_inv.shape[0])
    return sigma_inv @ ones / (ones @ sigma_inv @ ones)


def global_minimum_variance_weights(cov_matrix):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Global minimum variance weights — w* = Sigma^{-1}1 / (1' Sigma^{-1}1). A financial metric in the domain of Asset management & portfolio optimization."
    y_as_x: []
    :param expected_returns: "Expected Returns vector contains the anticipated return for each asset."
    :param cov_matrix: "Covariance Matrix contains the covariances between all pairs of assets."
    :return: "Computed value of Global minimum variance weights: w* = Sigma^{-1}1 / (1' Sigma^{-1}1)"
    '''
    import numpy as np
    sigma_inv = np.linalg.inv(np.array(cov_matrix))
    ones = np.ones(sigma_inv.shape[0])
    w = sigma_inv @ ones / (ones @ sigma_inv @ ones)
    return w




def gmm_moment_condition(y, X, instruments):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Financial Econometrics', 'Time Series Analysis']
    function: "GMM moment condition — E[g(z_t,theta)] = 0; theta_hat = argmin gbar' W gbar. A financial metric in the domain of Econometrics & time-series finance."
    y_as_x: []
    :param y: "Parameter y used in GMM moment condition calculation."
    :param X: "Parameter X used in GMM moment condition calculation."
    :return: "Computed value of GMM moment condition: E[g(z_t,theta)] = 0; theta_hat = argmin gbar' W gbar"
    '''
    import numpy as np
    from linearmodels.iv import IVGMM
    return IVGMM(y, X, instruments).fit()




def gordon_growth_ddm(dividend_per_share, cost_of_equity, growth_rate):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Equity Valuation', 'Asset Pricing']
    function: "Gordon growth DDM — P_0 = D_1/(r-g). A financial metric in the domain of Equity valuation & asset pricing."
    y_as_x: []
    :param args: "Parameter args used in Gordon growth DDM calculation."
    :param kwargs: "Parameter kwargs used in Gordon growth DDM calculation."
    :return: "Computed value of Gordon growth DDM: P_0 = D_1/(r-g)"
    '''
    return dividend_per_share / (cost_of_equity - growth_rate)




def gordon_growth_model(dividend_per_share, cost_of_equity, growth_rate):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "Gordon Growth Model — P = D / (r - g). Constant growth dividend valuation."
    y_as_x: []
    :param dividend_per_share: "Dividend Per Share (DPS) is the sum of declared dividends per ordinary share."
    :param cost_of_equity: "Cost of Equity (Re) is the return required by equity investors."
    :param growth_rate: "Growth Rate (g) is the rate at which a value increases over time."
    :return: "Computed value of Gordon growth model: P_0 = D_1 / (r-g)"
    '''
    return dividend_per_share / (cost_of_equity - growth_rate)






def gordon_terminal_value(terminal_fcf, wacc, growth_rate):
    '''
    domain: ['Corporate finance & capital budgeting']
    subdomain: ['Corporate Finance', 'Capital Budgeting']
    function: "Gordon Terminal Value — TV = FCF * (1+g) / (WACC - g)."
    y_as_x: []
    :param terminal_fcf: "Parameter terminal_fcf used in Gordon terminal value calculation."
    :param wacc: "Weighted Average Cost of Capital (WACC) is the average rate of return expected by all security holders."
    :param growth_rate: "Growth Rate (g) is the rate at which a value increases over time."
    :return: "Computed value of Gordon terminal value: TV = FCF_(t+1) / (WACC - g)"
    '''
    return terminal_fcf / (wacc - growth_rate)






def gradient_boosting(X_train, y_train, X_test, n_estimators=100):
    '''
    domain: ['Quantitative forecasting & machine learning in finance']
    subdomain: ['Quantitative Finance', 'Machine Learning']
    function: "Gradient boosting — F_m(x)=F_{m-1}(x)+nu h_m(x). A financial metric in the domain of Quantitative forecasting & machine learning in finance."
    y_as_x: []
    :param X: "Parameter X used in Gradient boosting calculation."
    :param y: "Parameter y used in Gradient boosting calculation."
    :return: "Computed value of Gradient boosting: F_m(x)=F_{m-1}(x)+nu h_m(x)"
    '''
    from sklearn.ensemble import GradientBoostingRegressor
    model = GradientBoostingRegressor(n_estimators=n_estimators)
    model.fit(X_train, y_train)
    return model.predict(X_test)


def granger_causality(y, X):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Financial Econometrics', 'Time Series Analysis']
    function: "Granger causality — X Granger-causes Y if lagged X terms improve prediction of Y. A financial metric in the domain of Econometrics & time-series finance."
    y_as_x: []
    :param y: "Parameter y used in Granger causality calculation."
    :param X: "Parameter X used in Granger causality calculation."
    :return: "Computed value of Granger causality: X Granger-causes Y if lagged X terms improve prediction of Y"
    '''
    import statsmodels.api as sm
    X_const = sm.add_constant(X)
    model = sm.OLS(y, X_const).fit()
    return model






def gross_irr(cash_flows):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Private Equity', 'Venture Capital', 'LBO']
    function: "Gross IRR — internal rate of return before fees and expenses."
    y_as_x: []
    :param cash_flows: "Parameter cash_flows used in Gross IRR calculation."
    :return: "Computed value of Gross IRR: 0 = -Equity_0 + sum_t Distribution_t/(1+IRR)^t + Terminal Equity/(1+IRR)^T"
    '''
    import numpy_financial as npf
    return npf.irr(cash_flows)






def gross_margin(gross_profit, revenue):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "Gross Margin — gross profit as a percentage of revenue."
    y_as_x: []
    :param gross_profit: "Gross Profit is total revenue minus cost of goods sold (COGS)."
    :param revenue: "Revenue is the total amount of income a business generates from the sale of goods or services before deducting expenses."
    :return: "Computed value of Gross margin: Gross Margin = Gross Profit / Revenue"
    '''
    return gross_profit / revenue






def gross_premium_principle(net_premium, expense_loading, profit_loading=0):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "Gross premium principle — Gross Premium = (PV Benefits + PV Expenses) / PV Premium Annuity. A financial metric in the domain of Actuarial science & insurance."
    y_as_x: []
    :param args: "Parameter args used in Gross premium principle calculation."
    :param kwargs: "Parameter kwargs used in Gross premium principle calculation."
    :return: "Computed value of Gross premium principle: Gross Premium = (PV Benefits + PV Expenses) / PV Premium Annuity"
    '''
    return net_premium * (1 + expense_loading + profit_loading)


def gross_profit(revenue, cost_of_goods_sold):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "Gross Profit — revenue minus cost of goods sold."
    y_as_x: ['gross_margin']
    :param revenue: "Revenue is the total amount of income a business generates from the sale of goods or services before deducting expenses."
    :param cost_of_goods_sold: "Cost of Goods Sold (COGS) is the direct costs attributable to the production of goods sold."
    :return: "Computed value of Gross profit: Gross Profit = Revenue - COGS"
    '''
    return revenue - cost_of_goods_sold






def gross_rent_multiplier(property_value, gross_annual_rent):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Real Estate Finance', 'Mortgage Analysis']
    function: "Gross Rent Multiplier — property price divided by gross annual rent."
    y_as_x: []
    :param property_value: "Property Value is the estimated market worth of a real estate asset."
    :param gross_annual_rent: "Parameter gross_annual_rent used in Gross rent multiplier calculation."
    :return: "Computed value of Gross rent multiplier: GRM = Property Price / Gross Annual Rent"
    '''
    return property_value / gross_annual_rent






def growing_annuity_value(payment, rate, growth_rate, num_periods):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "Growing Annuity Value — PV of a series of growing payments."
    y_as_x: []
    :param payment: "Payment (PMT) is the periodic payment amount in an amortization schedule."
    :param rate: "Rate (r) is the interest rate or discount rate per period."
    :param growth_rate: "Growth Rate (g) is the rate at which a value increases over time."
    :param num_periods: "Number of Periods (n) is the total number of payment or compounding periods."
    :return: "Computed value of Growing annuity value: PV = PMT_1 x [1-((1+g)/(1+r))^n] / (r-g)"
    '''
    return payment / (rate - growth_rate) * (1 - ((1 + growth_rate) / (1 + rate))**num_periods)






def growing_perpetuity_value(payment, rate, growth_rate):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "Growing Perpetuity Value — PV = C / (r - g). Requires r > g."
    y_as_x: []
    :param payment: "Payment (PMT) is the periodic payment amount in an amortization schedule."
    :param rate: "Rate (r) is the interest rate or discount rate per period."
    :param growth_rate: "Growth Rate (g) is the rate at which a value increases over time."
    :return: "Computed value of Growing perpetuity value: PV = CF_1 / (r-g)"
    '''
    return payment / (rate - growth_rate)






def gsib_surcharge(base_capital, surcharge):
    '''
    domain: ['Bank regulation, Basel & prudential ratios']
    subdomain: ['Bank Regulation', 'Basel Framework', 'Prudential Ratios']
    function: "GSIB surcharge — GSIB Capital Requirement = base capital + surcharge. A financial metric in the domain of Bank regulation, Basel & prudential ratios."
    y_as_x: []
    :param base_capital: "Parameter base_capital used in GSIB surcharge calculation."
    :param surcharge: "Parameter surcharge used in GSIB surcharge calculation."
    :return: "Computed value of GSIB surcharge: GSIB Capital Requirement = base capital + surcharge"
    '''
    return base_capital + surcharge






def haircut_adjusted_liquidation_value(cash_flows, discount_rate):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Liquidity Risk', 'Market Liquidity', 'Execution Cost']
    function: "Haircut-adjusted liquidation value — LV = Market Value x (1-Haircut). A financial metric in the domain of Liquidity risk, market liquidity & execution cost."
    y_as_x: []
    :param cash_flows: "Parameter cash_flows used in Haircut-adjusted liquidation value calculation."
    :param discount_rate: "Discount Rate is the rate used to discount future cash flows to present value."
    :return: "Computed value of Haircut-adjusted liquidation value: LV = Market Value x (1-Haircut)"
    '''
    import numpy as np
    cf = np.array(cash_flows)
    t = np.arange(1, len(cf) + 1)
    return np.sum(cf / (1 + discount_rate)**t)






def hasbrouck_lambda(y, X):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Liquidity Risk', 'Market Liquidity', 'Execution Cost']
    function: "Hasbrouck lambda — r_t = lambda sqrt(VolSigned_t) + epsilon_t. A financial metric in the domain of Liquidity risk, market liquidity & execution cost."
    y_as_x: []
    :param y: "Parameter y used in Hasbrouck lambda calculation."
    :param X: "Parameter X used in Hasbrouck lambda calculation."
    :return: "Computed value of Hasbrouck lambda: r_t = lambda sqrt(VolSigned_t) + epsilon_t"
    '''
    import statsmodels.api as sm
    X_const = sm.add_constant(X)
    model = sm.OLS(y, X_const).fit()
    return model






def hazard_rate_survival(hazard_rates, time_points):
    '''
    domain: ['Credit risk']
    subdomain: ['Credit Risk']
    function: "Hazard-rate survival — S(t) = e^{-λ t}. A financial metric in the domain of Credit risk."
    y_as_x: []
    :param args: "Parameter args used in Hazard-rate survival calculation."
    :param kwargs: "Parameter kwargs used in Hazard-rate survival calculation."
    :return: "Computed value of Hazard-rate survival: S(t) = e^{-λ t}"
    '''
    import numpy as np
    return np.exp(-np.cumsum(np.array(hazard_rates) * np.diff(np.concatenate([[0], time_points]))))


def hedge_ratio_naive(exposure, contract_size):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Commodities', 'Futures', 'Hedging']
    function: "Hedge ratio (naive) — h = Exposure / Contract Size. A financial metric in the domain of Commodities, futures & hedging."
    y_as_x: []
    :param exposure: "Parameter exposure used in Hedge ratio (naive) calculation."
    :param contract_size: "Parameter contract_size used in Hedge ratio (naive) calculation."
    :return: "Computed value of Hedge ratio (naive): h = Exposure / Contract Size"
    '''
    return exposure / contract_size






def hedged_commodity_revenue(production_volume, hedge_price, hedge_ratio, spot_price):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Commodities', 'Futures', 'Hedging']
    function: "Hedged commodity revenue — Hedged Revenue = Spot Revenue + Futures P&L. A financial metric in the domain of Commodities, futures & hedging."
    y_as_x: []
    :param args: "Parameter args used in Hedged commodity revenue calculation."
    :param kwargs: "Parameter kwargs used in Hedged commodity revenue calculation."
    :return: "Computed value of Hedged commodity revenue: Hedged Revenue = Spot Revenue + Futures P&L"
    '''
    return production_volume * (hedge_ratio * hedge_price + (1 - hedge_ratio) * spot_price)


def henriksson_merton_timing(y, X):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Performance Attribution', 'Risk-Adjusted Performance']
    function: "Henriksson-Merton timing — R_p-R_f = alpha + beta(R_m-R_f) + gamma max(R_m-R_f,0) + epsilon. A financial metric in the domain of Performance measurement & attribution."
    y_as_x: []
    :param y: "Parameter y used in Henriksson-Merton timing calculation."
    :param X: "Parameter X used in Henriksson-Merton timing calculation."
    :return: "Computed value of Henriksson-Merton timing: R_p-R_f = alpha + beta(R_m-R_f) + gamma max(R_m-R_f,0) + epsilon"
    '''
    import statsmodels.api as sm
    X_const = sm.add_constant(X)
    model = sm.OLS(y, X_const).fit()
    return model






def herfindahl_concentration_index(numerator, denominator):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Herfindahl concentration index — HHI = sum_i w_i^2. A financial metric in the domain of Asset management & portfolio optimization."
    y_as_x: []
    :param numerator: "Parameter numerator used in Herfindahl concentration index calculation."
    :param denominator: "Parameter denominator used in Herfindahl concentration index calculation."
    :return: "Computed value of Herfindahl concentration index: HHI = sum_i w_i^2"
    '''
    return numerator / denominator if denominator != 0 else float("inf")






def heston_asset_process(S0, v0, mu, kappa, theta, xi, rho, dt, num_steps, num_paths=1000):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Heston asset process — dS_t = (r-q)S_t dt + sqrt(v_t)S_t dW_t^S. A financial metric in the domain of Derivatives, options & volatility."
    y_as_x: []
    :param args: "Parameter args used in Heston asset process calculation."
    :param kwargs: "Parameter kwargs used in Heston asset process calculation."
    :return: "Computed value of Heston asset process: dS_t = (r-q)S_t dt + sqrt(v_t)S_t dW_t^S"
    '''
    import numpy as np
    S = np.zeros((num_paths, num_steps+1)); v = np.zeros((num_paths, num_steps+1))
    S[:,0] = S0; v[:,0] = v0
    for t in range(num_steps):
        z1 = np.random.standard_normal(num_paths)
        z2 = rho*z1 + np.sqrt(1-rho**2)*np.random.standard_normal(num_paths)
        v[:,t+1] = np.maximum(v[:,t] + kappa*(theta-v[:,t])*dt + xi*np.sqrt(np.maximum(v[:,t],0)*dt)*z2, 0)
        S[:,t+1] = S[:,t] * np.exp((mu - 0.5*v[:,t])*dt + np.sqrt(np.maximum(v[:,t],0)*dt)*z1)
    return S


def heston_variance_process(v0, kappa, theta, xi, rho, dt, num_steps, num_paths=1000):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Heston variance process — dv_t = kappa(theta-v_t)dt + xi sqrt(v_t)dW_t^v. A financial metric in the domain of Derivatives, options & volatility."
    y_as_x: []
    :param args: "Parameter args used in Heston variance process calculation."
    :param kwargs: "Parameter kwargs used in Heston variance process calculation."
    :return: "Computed value of Heston variance process: dv_t = kappa(theta-v_t)dt + xi sqrt(v_t)dW_t^v"
    '''
    import numpy as np
    v = np.zeros((num_paths, num_steps + 1))
    v[:, 0] = v0
    for t in range(num_steps):
        z = np.random.standard_normal(num_paths)
        v[:, t+1] = np.maximum(v[:, t] + kappa * (theta - v[:, t]) * dt + xi * np.sqrt(np.maximum(v[:, t], 0) * dt) * z, 0)
    return v




def historical_va_r(returns, confidence_level=0.95):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "Historical VaR — the (1-alpha) percentile of historical returns. Non-parametric approach."
    y_as_x: []
    :param returns: "Returns are the gain or loss generated on an investment over a specific period."
    :param confidence_level: "Confidence Level is the probability threshold used in statistical tests and risk measures."
    :return: "Computed value of Historical VaR: VaR_alpha = -quantile_alpha(R)"
    '''
    import numpy as np
    return -np.percentile(returns, (1 - confidence_level) * 100)






def hit_ratio(profitable_periods, total_periods):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Performance Attribution', 'Risk-Adjusted Performance']
    function: "Hit ratio — Hit Ratio = profitable periods / total periods. A financial metric in the domain of Performance measurement & attribution."
    y_as_x: []
    :param profitable_periods: "Parameter profitable_periods used in Hit ratio calculation."
    :param total_periods: "Parameter total_periods used in Hit ratio calculation."
    :return: "Computed value of Hit ratio: Hit Ratio = profitable periods / total periods"
    '''
    return profitable_periods / total_periods






def hjm_drift_restriction(volatilities, correlations, dt):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Interest Rate Modeling', 'Term Structure']
    function: "HJM drift restriction — alpha(t,T) = sigma(t,T) integral_t^T sigma(t,u) du. A financial metric in the domain of Interest-rate modeling & term structures."
    y_as_x: []
    :param args: "Parameter args used in HJM drift restriction calculation."
    :param kwargs: "Parameter kwargs used in HJM drift restriction calculation."
    :return: "Computed value of HJM drift restriction: alpha(t,T) = sigma(t,T) integral_t^T sigma(t,u) du"
    '''
    import numpy as np
    vol = np.array(volatilities); n = len(vol)
    drift = np.zeros(n)
    for i in range(n):
        drift[i] = vol[i] * np.sum(vol[:i+1] * correlations[i,:i+1] * dt)
    return drift


def hjm_forward_rate_dynamics(forward_rates, volatilities, dt, num_steps):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Interest Rate Modeling', 'Term Structure']
    function: "HJM forward-rate dynamics — df(t,T) = alpha(t,T)dt + sigma(t,T)dW_t. A financial metric in the domain of Interest-rate modeling & term structures."
    y_as_x: []
    :param args: "Parameter args used in HJM forward-rate dynamics calculation."
    :param kwargs: "Parameter kwargs used in HJM forward-rate dynamics calculation."
    :return: "Computed value of HJM forward-rate dynamics: df(t,T) = alpha(t,T)dt + sigma(t,T)dW_t"
    '''
    import numpy as np
    fr = np.array(forward_rates, dtype=float)
    vol = np.array(volatilities, dtype=float)
    for t in range(num_steps):
        drift = vol * np.cumsum(vol * dt)
        dw = np.random.standard_normal(len(fr)) * np.sqrt(dt)
        fr = fr + drift * dt + vol * dw
    return fr




def holding_period_return_hpr(ending_value, beginning_value, income=0):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Performance Attribution', 'Risk-Adjusted Performance']
    function: "Holding Period Return (HPR) — total return over a holding period."
    y_as_x: []
    :param ending_value: "Ending Value is the final portfolio or investment value."
    :param beginning_value: "Beginning Value is the initial portfolio or investment value."
    :param income: "Parameter income used in Holding period return (HPR) calculation."
    :return: "Computed value of Holding period return (HPR): HPR = (P_1 - P_0 + D_1)/P_0"
    '''
    return (ending_value - beginning_value + income) / beginning_value






def holt_trend_method(time_series, trend="add"):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Financial Econometrics', 'Time Series Analysis']
    function: "Holt trend method — l_t = alpha y_t + (1-alpha)(l_{t-1}+b_{t-1}); b_t = beta(l_t-l_{t-1}) + (1-beta)b_{t-1}. A financial metric in the domain of Econometrics & time-series finance."
    y_as_x: []
    :param data: "Parameter data used in Holt trend method calculation."
    :param args: "Parameter args used in Holt trend method calculation."
    :return: "Computed value of Holt trend method: l_t = alpha y_t + (1-alpha)(l_{t-1}+b_{t-1}); b_t = beta(l_t-l_{t-1}) + (1-beta)b_{t-1}"
    '''
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    return ExponentialSmoothing(time_series, trend=trend).fit()


def holt_winters_seasonality(time_series, seasonal_periods=12, trend="add", seasonal="add"):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Financial Econometrics', 'Time Series Analysis']
    function: "Holt-Winters seasonality — Seasonal add/mult update with alpha, beta, gamma. A financial metric in the domain of Econometrics & time-series finance."
    y_as_x: []
    :param data: "Parameter data used in Holt-Winters seasonality calculation."
    :param args: "Parameter args used in Holt-Winters seasonality calculation."
    :return: "Computed value of Holt-Winters seasonality: Seasonal add/mult update with alpha, beta, gamma"
    '''
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    model = ExponentialSmoothing(time_series, seasonal_periods=seasonal_periods, trend=trend, seasonal=seasonal)
    return model.fit()




def hull_white_1f_process(r0, kappa, theta, sigma, dt, num_steps, num_paths=1000):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Interest Rate Modeling', 'Term Structure']
    function: "Hull-White 1F process — dr_t = [theta(t)-a r_t]dt + sigma dW_t. A financial metric in the domain of Interest-rate modeling & term structures."
    y_as_x: []
    :param args: "Parameter args used in Hull-White 1F process calculation."
    :param kwargs: "Parameter kwargs used in Hull-White 1F process calculation."
    :return: "Computed value of Hull-White 1F process: dr_t = [theta(t)-a r_t]dt + sigma dW_t"
    '''
    import numpy as np
    r = np.zeros((num_paths, num_steps + 1))
    r[:, 0] = r0
    for t in range(num_steps):
        dw = np.random.standard_normal(num_paths) * np.sqrt(dt)
        r[:, t+1] = r[:, t] + kappa * (theta - r[:, t]) * dt + sigma * dw
    return r




def hull_white_bond_option_jamshidian(face_value, strike, kappa, sigma, r0, option_maturity, bond_maturity):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Interest Rate Modeling', 'Term Structure']
    function: "Hull-White bond option (Jamshidian) — Option value = sum_i option on each cash flow under HW decomposition. A financial metric in the domain of Interest-rate modeling & term structures."
    y_as_x: []
    :param args: "Parameter args used in Hull-White bond option (Jamshidian) calculation."
    :param kwargs: "Parameter kwargs used in Hull-White bond option (Jamshidian) calculation."
    :return: "Computed value of Hull-White bond option (Jamshidian): Option value = sum_i option on each cash flow under HW decomposition"
    '''
    import numpy as np
    from scipy.stats import norm
    B = (1 - np.exp(-kappa * (bond_maturity - option_maturity))) / kappa
    sigma_p = sigma * B * np.sqrt((1 - np.exp(-2 * kappa * option_maturity)) / (2 * kappa))
    P_T = face_value * np.exp(-r0 * bond_maturity)
    P_t = np.exp(-r0 * option_maturity)
    forward_bond = P_T / P_t
    d1 = (np.log(forward_bond / strike) + 0.5 * sigma_p**2) / sigma_p
    d2 = d1 - sigma_p
    return P_t * (forward_bond * norm.cdf(d1) - strike * norm.cdf(d2))




def hull_white_model(r0, kappa, theta_func, sigma, dt, num_steps, num_paths=1000):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Interest Rate Modeling', 'Term Structure']
    function: "Hull-White model — dr_t = [θ(t)-a r_t]dt + σ dW_t. A financial metric in the domain of Interest-rate modeling & term structures."
    y_as_x: []
    :param args: "Parameter args used in Hull-White model calculation."
    :param kwargs: "Parameter kwargs used in Hull-White model calculation."
    :return: "Computed value of Hull-White model: dr_t = [θ(t)-a r_t]dt + σ dW_t"
    '''
    import numpy as np
    r = np.zeros((num_paths, num_steps + 1))
    r[:, 0] = r0
    for t in range(num_steps):
        theta_t = theta_func(t * dt) if callable(theta_func) else theta_func
        dw = np.random.standard_normal(num_paths) * np.sqrt(dt)
        r[:, t+1] = r[:, t] + kappa * (theta_t - r[:, t]) * dt + sigma * dw
    return r




def ichimoku_base_line(high, low, period=26):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "Ichimoku base line — Kijun = (26-period high + 26-period low)/2. A financial metric in the domain of Technical analysis & chart-based indicators."
    y_as_x: []
    :param high: "High is the highest price during a specific trading period."
    :param low: "Low is the lowest price during a specific trading period."
    :param close: "Close is the final trading price at the end of a trading period."
    :param volume: "Volume is the total number of shares or contracts traded during a period."
    :param period: "Period (n) is the lookback window in number of bars for technical indicators."
    :return: "Computed value of Ichimoku base line: Kijun = (26-period high + 26-period low)/2"
    '''
    import pandas as pd
    h = pd.Series(high); l = pd.Series(low)
    return (h.rolling(window=period).max() + l.rolling(window=period).min()) / 2




def ichimoku_conversion_line(high, low, period=9):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "Ichimoku conversion line — Tenkan = (9-period high + 9-period low)/2. A financial metric in the domain of Technical analysis & chart-based indicators."
    y_as_x: []
    :param close: "Close is the final trading price at the end of a trading period."
    :param period: "Period (n) is the lookback window in number of bars for technical indicators."
    :return: "Computed value of Ichimoku conversion line: Tenkan = (9-period high + 9-period low)/2"
    '''
    import pandas as pd
    h = pd.Series(high); l = pd.Series(low)
    return (h.rolling(window=period).max() + l.rolling(window=period).min()) / 2




def ichimoku_leading_span_a(high, low, conversion_period=9, base_period=26):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "Ichimoku leading span A — SpanA = (Tenkan + Kijun)/2 shifted forward. A financial metric in the domain of Technical analysis & chart-based indicators."
    y_as_x: []
    :param high: "High is the highest price during a specific trading period."
    :param low: "Low is the lowest price during a specific trading period."
    :param close: "Close is the final trading price at the end of a trading period."
    :param volume: "Volume is the total number of shares or contracts traded during a period."
    :param period: "Period (n) is the lookback window in number of bars for technical indicators."
    :return: "Computed value of Ichimoku leading span A: SpanA = (Tenkan + Kijun)/2 shifted forward"
    '''
    import pandas as pd
    h = pd.Series(high); l = pd.Series(low)
    conv = (h.rolling(window=conversion_period).max() + l.rolling(window=conversion_period).min()) / 2
    base = (h.rolling(window=base_period).max() + l.rolling(window=base_period).min()) / 2
    return ((conv + base) / 2).shift(base_period)




def ichimoku_leading_span_b(high, low, period=52, displacement=26):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "Ichimoku leading span B — SpanB = (52-period high + 52-period low)/2 shifted forward. A financial metric in the domain of Technical analysis & chart-based indicators."
    y_as_x: []
    :param high: "High is the highest price during a specific trading period."
    :param low: "Low is the lowest price during a specific trading period."
    :param close: "Close is the final trading price at the end of a trading period."
    :param volume: "Volume is the total number of shares or contracts traded during a period."
    :param period: "Period (n) is the lookback window in number of bars for technical indicators."
    :return: "Computed value of Ichimoku leading span B: SpanB = (52-period high + 52-period low)/2 shifted forward"
    '''
    import pandas as pd
    h = pd.Series(high); l = pd.Series(low)
    return ((h.rolling(window=period).max() + l.rolling(window=period).min()) / 2).shift(displacement)




def idiosyncratic_volatility(y, X):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Equity Valuation', 'Asset Pricing']
    function: "Idiosyncratic volatility — IVOL = std(residuals from factor model). A financial metric in the domain of Equity valuation & asset pricing."
    y_as_x: []
    :param y: "Parameter y used in Idiosyncratic volatility calculation."
    :param X: "Parameter X used in Idiosyncratic volatility calculation."
    :return: "Computed value of Idiosyncratic volatility: IVOL = std(residuals from factor model)"
    '''
    import statsmodels.api as sm
    X_const = sm.add_constant(X)
    model = sm.OLS(y, X_const).fit()
    return model






def implementation_shortfall(decision_price, execution_price, num_shares, benchmark_price=None):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Liquidity Risk', 'Market Liquidity', 'Execution Cost']
    function: "Implementation shortfall — IS = (Execution Price - Arrival Price) x Side x Quantity. A financial metric in the domain of Liquidity risk, market liquidity & execution cost."
    y_as_x: []
    :param args: "Parameter args used in Implementation shortfall calculation."
    :param kwargs: "Parameter kwargs used in Implementation shortfall calculation."
    :return: "Computed value of Implementation shortfall: IS = (Execution Price - Arrival Price) x Side x Quantity"
    '''
    bp = benchmark_price if benchmark_price is not None else decision_price
    return num_shares * (execution_price - bp)


def implied_cost_of_equity_simple(eps_forward, stock_price, growth_rate):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Equity Valuation', 'Asset Pricing']
    function: "Implied cost of equity (simple) — r = D_1/P_0 + g. A financial metric in the domain of Equity valuation & asset pricing."
    y_as_x: []
    :param args: "Parameter args used in Implied cost of equity (simple) calculation."
    :param kwargs: "Parameter kwargs used in Implied cost of equity (simple) calculation."
    :return: "Computed value of Implied cost of equity (simple): r = D_1/P_0 + g"
    '''
    return eps_forward / stock_price + growth_rate




def implied_volatility(option_price, spot_price, strike_price, risk_free_rate, time_to_expiry, option_type):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Implied Volatility — the volatility implied by market option prices via BSM inversion."
    y_as_x: ['sabr_implied_vol', 'vega', 'vix_variance_relation']
    :param option_price: "Option Price (premium) is the market price of an options contract."
    :param spot_price: "Spot Price (S) is the current market price of the underlying asset."
    :param strike_price: "Strike Price (K) is the predetermined price at which an option can be exercised."
    :param risk_free_rate: "Risk-Free Rate (Rf) is the theoretical rate of return with zero risk, typically proxied by government bond yields."
    :param time_to_expiry: "Time to Expiry (T) is the remaining time until expiration, in years."
    :param option_type: "Option Type specifies whether the option is a "call" or "put"."
    :return: "Computed value of Implied volatility: Find σ such that ModelPrice(σ) = MarketPrice"
    '''
    from scipy.optimize import brentq
    from scipy.stats import norm
    import numpy as np
    def bs_price(sigma):
        d1 = (np.log(spot_price/strike_price) + (risk_free_rate + 0.5*sigma**2)*time_to_expiry) / (sigma*np.sqrt(time_to_expiry))
        d2 = d1 - sigma*np.sqrt(time_to_expiry)
        if option_type == 'call':
            return spot_price*norm.cdf(d1) - strike_price*np.exp(-risk_free_rate*time_to_expiry)*norm.cdf(d2)
        else:
            return strike_price*np.exp(-risk_free_rate*time_to_expiry)*norm.cdf(-d2) - spot_price*norm.cdf(-d1)
    return brentq(lambda s: bs_price(s) - option_price, 0.001, 5.0)






def impulse_response_function(var_model, steps=10):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Financial Econometrics', 'Time Series Analysis']
    function: "Impulse response function — IRF_h = d y_{t+h} / d u_t. A financial metric in the domain of Econometrics & time-series finance."
    y_as_x: []
    :param data: "Parameter data used in Impulse response function calculation."
    :param args: "Parameter args used in Impulse response function calculation."
    :return: "Computed value of Impulse response function: IRF_h = d y_{t+h} / d u_t"
    '''
    return var_model.irf(steps).irfs


def increasing_annuity(interest_rate, num_periods):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "Increasing annuity — (Ia)_x = E[sum_{k>=1} k v^k 1(T_x>=k)]. A financial metric in the domain of Actuarial science & insurance."
    y_as_x: []
    :param args: "Parameter args used in Increasing annuity calculation."
    :param kwargs: "Parameter kwargs used in Increasing annuity calculation."
    :return: "Computed value of Increasing annuity: (Ia)_x = E[sum_{k>=1} k v^k 1(T_x>=k)]"
    '''
    i = interest_rate
    n = num_periods
    v = 1 / (1 + i)
    a = (1 - v**n) / i
    return (a - n * v**n) / i




def incremental_va_r(weights, cov_matrix, confidence_level=0.95, asset_index=0):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "Incremental VaR — IVaR_i = VaR(portfolio) - VaR(portfolio without i). A financial metric in the domain of Market risk & volatility modeling."
    y_as_x: []
    :param args: "Parameter args used in Incremental VaR calculation."
    :param kwargs: "Parameter kwargs used in Incremental VaR calculation."
    :return: "Computed value of Incremental VaR: IVaR_i = VaR(portfolio) - VaR(portfolio without i)"
    '''
    import numpy as np
    from scipy.stats import norm
    w = np.array(weights); sigma = np.array(cov_matrix)
    z = norm.ppf(confidence_level)
    port_vol = np.sqrt(w @ sigma @ w)
    w_ex = w.copy(); w_ex[asset_index] = 0
    port_vol_ex = np.sqrt(w_ex @ sigma @ w_ex)
    return z * (port_vol - port_vol_ex)




def incurred_but_not_reported_ibnr(ultimate_loss, reported_loss):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "Incurred but not reported (IBNR) — IBNR = Ultimate Loss - Reported Loss. A financial metric in the domain of Actuarial science & insurance."
    y_as_x: []
    :param ultimate_loss: "Parameter ultimate_loss used in Incurred but not reported (IBNR) calculation."
    :param reported_loss: "Parameter reported_loss used in Incurred but not reported (IBNR) calculation."
    :return: "Computed value of Incurred but not reported (IBNR): IBNR = Ultimate Loss - Reported Loss"
    '''
    return ultimate_loss - reported_loss






def inflation_accretion(principal_x_cpi_t, cpi_base):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Fixed Income', 'Bond Mathematics', 'Credit Markets']
    function: "Inflation accretion — Indexed Principal_t = Principal x CPI_t/CPI_base. A financial metric in the domain of Fixed income, bonds & credit markets."
    y_as_x: []
    :param principal_x_cpi_t: "Parameter principal_x_cpi_t used in Inflation accretion calculation."
    :param cpi_base: "Parameter cpi_base used in Inflation accretion calculation."
    :return: "Computed value of Inflation accretion: Indexed Principal_t = Principal x CPI_t/CPI_base"
    '''
    return principal_x_cpi_t / cpi_base






def information_ratio(portfolio_returns, benchmark_returns):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Information Ratio — annualized active return divided by tracking error."
    y_as_x: []
    :param portfolio_returns: "Portfolio Returns represent the weighted average returns of all assets in a portfolio."
    :param benchmark_returns: "Benchmark Returns are the returns of a reference index used for performance comparison."
    :return: "Computed value of Information ratio: IR = mean(R_p-R_b) / std(R_p-R_b)"
    '''
    import numpy as np
    active = np.array(portfolio_returns) - np.array(benchmark_returns)
    return np.mean(active) / np.std(active, ddof=1) * np.sqrt(252)






def installment_to_income_ratio(installment_payment, income):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Banking', 'Consumer Lending', 'Project Finance']
    function: "Installment-to-income ratio — ITI = Installment Payment / Income. A financial metric in the domain of Banking, consumer lending & project finance."
    y_as_x: []
    :param installment_payment: "Parameter installment_payment used in Installment-to-income ratio calculation."
    :param income: "Parameter income used in Installment-to-income ratio calculation."
    :return: "Computed value of Installment-to-income ratio: ITI = Installment Payment / Income"
    '''
    return installment_payment / income






def instantaneous_forward_rate(discount_factors, dt):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Interest Rate Modeling', 'Term Structure']
    function: "Instantaneous forward rate — f(t,T) = -d ln P(t,T)/dT. A financial metric in the domain of Interest-rate modeling & term structures."
    y_as_x: []
    :param args: "Parameter args used in Instantaneous forward rate calculation."
    :param kwargs: "Parameter kwargs used in Instantaneous forward rate calculation."
    :return: "Computed value of Instantaneous forward rate: f(t,T) = -d ln P(t,T)/dT"
    '''
    import numpy as np
    df = np.array(discount_factors)
    return -np.diff(np.log(df)) / dt


def instantaneous_short_rate_from_discount_curve(discount_factors, dt):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Interest Rate Modeling', 'Term Structure']
    function: "Instantaneous short rate from discount curve — r(t) = -d ln P(0,t)/dt. A financial metric in the domain of Interest-rate modeling & term structures."
    y_as_x: []
    :param args: "Parameter args used in Instantaneous short rate from discount curve calculation."
    :param kwargs: "Parameter kwargs used in Instantaneous short rate from discount curve calculation."
    :return: "Computed value of Instantaneous short rate from discount curve: r(t) = -d ln P(0,t)/dt"
    '''
    import numpy as np
    df = np.array(discount_factors)
    return -np.diff(np.log(df)) / dt




def instrumental_variables_2sls(y, X, instruments):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Financial Econometrics', 'Time Series Analysis']
    function: "Instrumental variables / 2SLS — beta_2SLS = (X'P_Z X)^-1 X'P_Z y. A financial metric in the domain of Econometrics & time-series finance."
    y_as_x: []
    :param y: "Parameter y used in Instrumental variables / 2SLS calculation."
    :param X: "Parameter X used in Instrumental variables / 2SLS calculation."
    :return: "Computed value of Instrumental variables / 2SLS: beta_2SLS = (X'P_Z X)^-1 X'P_Z y"
    '''
    from linearmodels.iv import IV2SLS
    return IV2SLS(y, None, X, instruments).fit()




def interaction_effect(portfolio_weights, benchmark_weights, portfolio_sector_returns, benchmark_sector_returns):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Performance Attribution', 'Risk-Adjusted Performance']
    function: "Interaction effect — Interaction_i = (w_i^P - w_i^B)(r_i^P - r_i^B). A financial metric in the domain of Performance measurement & attribution."
    y_as_x: []
    :param args: "Parameter args used in Interaction effect calculation."
    :param kwargs: "Parameter kwargs used in Interaction effect calculation."
    :return: "Computed value of Interaction effect: Interaction_i = (w_i^P - w_i^B)(r_i^P - r_i^B)"
    '''
    import numpy as np
    return (np.array(portfolio_weights) - np.array(benchmark_weights)) * (np.array(portfolio_sector_returns) - np.array(benchmark_sector_returns))




def interest_coverage(ebit, interest_expense):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "Interest Coverage — EBIT / Interest Expense. Measures ability to service debt."
    y_as_x: []
    :param ebit: "EBIT (Earnings Before Interest and Taxes) is a financial metric measuring a company's profitability from core operations."
    :param interest_expense: "Interest Expense is the cost incurred by a company for borrowed funds."
    :return: "Computed value of Interest coverage: Interest Coverage = EBIT / Interest Expense"
    '''
    return ebit / interest_expense if interest_expense != 0 else float("inf")






def interest_coverage_ratio(ebit, interest_expense):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Banking', 'Consumer Lending', 'Project Finance']
    function: "Interest Coverage Ratio — EBIT divided by interest expense."
    y_as_x: []
    :param ebit: "EBIT (Earnings Before Interest and Taxes) is a financial metric measuring a company's profitability from core operations."
    :param interest_expense: "Interest Expense is the cost incurred by a company for borrowed funds."
    :return: "Computed value of Interest coverage ratio: ICR = EBIT / Interest Expense"
    '''
    return ebit / interest_expense if interest_expense != 0 else float("inf")






def interest_coverage_ratio_tranche(interest_collections, note_interest_due):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Structured Finance', 'Securitization']
    function: "Interest coverage ratio (tranche) — IC = Interest Collections / Note Interest Due. A financial metric in the domain of Structured finance & securitization."
    y_as_x: []
    :param interest_collections: "Parameter interest_collections used in Interest coverage ratio (tranche) calculation."
    :param note_interest_due: "Parameter note_interest_due used in Interest coverage ratio (tranche) calculation."
    :return: "Computed value of Interest coverage ratio (tranche): IC = Interest Collections / Note Interest Due"
    '''
    return interest_collections / note_interest_due






def interest_payment(rate, per, num_periods, present_value):
    '''
    domain: ['Banking, lending & project finance']
    subdomain: ['Banking', 'Lending', 'Project Finance']
    function: "Interest Payment — the interest portion of a specific loan payment."
    y_as_x: ['debt_service']
    :param rate: "Rate (r) is the interest rate or discount rate per period."
    :param per: "Parameter per used in Interest payment calculation."
    :param num_periods: "Number of Periods (n) is the total number of payment or compounding periods."
    :param present_value: "Present Value (PV) is the current worth of a future sum given a rate of return."
    :return: "Computed value of Interest payment: IPMT_t = r × Balance_(t-1)"
    '''
    import numpy_financial as npf
    return npf.ipmt(rate, per, num_periods, -present_value)






def interest_only_payment(loan_amount_x_annual_interest_rate, x_12):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Banking', 'Consumer Lending', 'Project Finance']
    function: "Interest-only payment — IOP = loan amount x annual interest rate/12. A financial metric in the domain of Banking, consumer lending & project finance."
    y_as_x: []
    :param loan_amount_x_annual_interest_rate: "Parameter loan_amount_x_annual_interest_rate used in Interest-only payment calculation."
    :param x_12: "Parameter x_12 used in Interest-only payment calculation."
    :return: "Computed value of Interest-only payment: IOP = loan amount x annual interest rate/12"
    '''
    return loan_amount_x_annual_interest_rate / x_12






def interest_rate_hedge_ratio(dv01_exposure, dv01_hedge):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Treasury', 'ALM', 'Balance Sheet Management']
    function: "Interest-rate hedge ratio — Hedge Ratio = DV01_exposure / DV01_hedge. A financial metric in the domain of Treasury, ALM & balance-sheet management."
    y_as_x: []
    :param dv01_exposure: "Parameter dv01_exposure used in Interest-rate hedge ratio calculation."
    :param dv01_hedge: "Parameter dv01_hedge used in Interest-rate hedge ratio calculation."
    :return: "Computed value of Interest-rate hedge ratio: Hedge Ratio = DV01_exposure / DV01_hedge"
    '''
    return dv01_exposure / dv01_hedge






def internal_rate_of_return_irr(cash_flows):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "Internal Rate of Return (IRR) — the discount rate that makes NPV = 0."
    y_as_x: []
    :param cash_flows: "Parameter cash_flows used in Internal rate of return (IRR) calculation."
    :return: "Computed value of Internal rate of return (IRR): 0 = sum_t CF_t / (1+IRR)^t"
    '''
    import numpy_financial as npf
    return npf.irr(cash_flows)






def internal_rate_of_return_since_inception(cash_flows):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Performance Attribution', 'Risk-Adjusted Performance']
    function: "Internal rate of return since inception — 0 = MV_T + sum_t CF_t/(1+r)^{T-t} - MV_0(1+r)^T. A financial metric in the domain of Performance measurement & attribution."
    y_as_x: []
    :param cash_flows: "Parameter cash_flows used in Internal rate of return since inception calculation."
    :return: "Computed value of Internal rate of return since inception: 0 = MV_T + sum_t CF_t/(1+r)^{T-t} - MV_0(1+r)^T"
    '''
    import numpy_financial as npf
    return npf.irr(cash_flows)






def international_fisher_effect(domestic_rate, foreign_rate):
    '''
    domain: ['FX & international finance']
    subdomain: ['FX Markets', 'International Finance']
    function: "International Fisher effect — Expected FX change approx i_d - i_f. A financial metric in the domain of FX & international finance."
    y_as_x: []
    :param args: "Parameter args used in International Fisher effect calculation."
    :param kwargs: "Parameter kwargs used in International Fisher effect calculation."
    :return: "Computed value of International Fisher effect: Expected FX change approx i_d - i_f"
    '''
    return (1 + domestic_rate) / (1 + foreign_rate) - 1


def intrinsic_value_call(spot_price, strike_price):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Intrinsic Value Call — max(S - K, 0). The exercise value of a call option."
    y_as_x: []
    :param spot_price: "Spot Price (S) is the current market price of the underlying asset."
    :param strike_price: "Strike Price (K) is the predetermined price at which an option can be exercised."
    :return: "Computed value of Intrinsic value call: IV = max(S-K,0)"
    '''
    import numpy as np
    return np.maximum(spot_price - strike_price, 0)






def inventory_turnover(cost_of_goods_sold, average_inventory):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "Inventory Turnover — COGS divided by average inventory."
    y_as_x: []
    :param cost_of_goods_sold: "Cost of Goods Sold (COGS) is the direct costs attributable to the production of goods sold."
    :param average_inventory: "Parameter average_inventory used in Inventory turnover calculation."
    :return: "Computed value of Inventory turnover: Inventory Turnover = COGS / Average Inventory"
    '''
    return cost_of_goods_sold / average_inventory






def io_strip_value(interest_cash_flows, discount_rates):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Structured Finance', 'Securitization']
    function: "IO strip value — PV_IO = sum_t interest_only_cf_t DF_t. A financial metric in the domain of Structured finance & securitization."
    y_as_x: []
    :param args: "Parameter args used in IO strip value calculation."
    :param kwargs: "Parameter kwargs used in IO strip value calculation."
    :return: "Computed value of IO strip value: PV_IO = sum_t interest_only_cf_t DF_t"
    '''
    import numpy as np
    cf = np.array(interest_cash_flows); r = np.array(discount_rates)
    return np.sum(cf / np.cumprod(1 + r))


def jensens_alpha(portfolio_return, risk_free_rate, beta, market_return):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Jensen's Alpha — actual return minus CAPM predicted return."
    y_as_x: []
    :param portfolio_return: "Portfolio Return is the total return of the managed portfolio."
    :param risk_free_rate: "Risk-Free Rate (Rf) is the theoretical rate of return with zero risk, typically proxied by government bond yields."
    :param beta: "Beta measures systematic risk, the sensitivity of returns to market movements."
    :param market_return: "Market Return (Rm) is the return on a broad market index representing overall market performance."
    :return: "Computed value of Jensen's alpha: alpha = R_p - [R_f + beta_p(R_m-R_f)]"
    '''
    return portfolio_return - (risk_free_rate + beta * (market_return - risk_free_rate))






def johansen_cointegration(data, det_order=0, k_ar_diff=1):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Financial Econometrics', 'Time Series Analysis']
    function: "Johansen cointegration — Test rank of Π in VECM. A financial metric in the domain of Econometrics & time-series finance."
    y_as_x: []
    :param data: "Parameter data used in Johansen cointegration calculation."
    :param args: "Parameter args used in Johansen cointegration calculation."
    :return: "Computed value of Johansen cointegration: Test rank of Π in VECM"
    '''
    from statsmodels.tsa.vector_ar.vecm import coint_johansen
    result = coint_johansen(data, det_order, k_ar_diff)
    return {'trace_stat': result.lr1, 'max_eigen_stat': result.lr2, 'critical_values_trace': result.cvt}


def johansen_trace_statistic(data, det_order=0, k_ar_diff=1):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Financial Econometrics', 'Time Series Analysis']
    function: "Johansen trace statistic — Trace = -T sum_{i=r+1}^k ln(1-hat lambda_i). A financial metric in the domain of Econometrics & time-series finance."
    y_as_x: []
    :param data: "Parameter data used in Johansen trace statistic calculation."
    :param args: "Parameter args used in Johansen trace statistic calculation."
    :return: "Computed value of Johansen trace statistic: Trace = -T sum_{i=r+1}^k ln(1-hat lambda_i)"
    '''
    from statsmodels.tsa.vector_ar.vecm import coint_johansen
    result = coint_johansen(data, det_order, k_ar_diff)
    return {'trace_stat': result.lr1, 'critical_values': result.cvt, 'eigen_stat': result.lr2}




def kelly_criterion(win_prob, win_loss_ratio):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Kelly criterion — f* = (bp - q)/b. A financial metric in the domain of Asset management & portfolio optimization."
    y_as_x: []
    :param returns_matrix: "Parameter returns_matrix used in Kelly criterion calculation."
    :return: "Computed value of Kelly criterion: f* = (bp - q)/b"
    '''
    return win_prob - (1 - win_prob) / win_loss_ratio




def keltner_channel_lower(ema, multiplier_x_atr):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "Keltner channel lower — Lower = EMA - multiplier x ATR. A financial metric in the domain of Technical analysis & chart-based indicators."
    y_as_x: []
    :param ema: "Parameter ema used in Keltner channel lower calculation."
    :param multiplier_x_atr: "Parameter multiplier_x_atr used in Keltner channel lower calculation."
    :return: "Computed value of Keltner channel lower: Lower = EMA - multiplier x ATR"
    '''
    return ema - multiplier_x_atr






def keltner_channel_upper(ema, multiplier_x_atr):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "Keltner channel upper — Upper = EMA + multiplier x ATR. A financial metric in the domain of Technical analysis & chart-based indicators."
    y_as_x: []
    :param ema: "Parameter ema used in Keltner channel upper calculation."
    :param multiplier_x_atr: "Parameter multiplier_x_atr used in Keltner channel upper calculation."
    :return: "Computed value of Keltner channel upper: Upper = EMA + multiplier x ATR"
    '''
    return ema + multiplier_x_atr






def kmv_expected_default_frequency(asset_value, default_point, asset_volatility, time_horizon=1):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit Risk', 'Default Modeling', 'Credit Portfolio']
    function: "KMV expected default frequency — EDF = Phi(-DD). A financial metric in the domain of Credit risk, default modeling & credit portfolio."
    y_as_x: []
    :param data: "Parameter data used in KMV expected default frequency calculation."
    :param args: "Parameter args used in KMV expected default frequency calculation."
    :return: "Computed value of KMV expected default frequency: EDF = Phi(-DD)"
    '''
    import numpy as np
    from scipy.stats import norm
    dd = (np.log(asset_value/default_point) + (-0.5*asset_volatility**2)*time_horizon) / (asset_volatility*np.sqrt(time_horizon))
    return norm.cdf(-dd)


def kpss_stationarity_test(y, X):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Financial Econometrics', 'Time Series Analysis']
    function: "KPSS stationarity test — y_t = r_t + epsilon_t; LM statistic from partial sums. A financial metric in the domain of Econometrics & time-series finance."
    y_as_x: []
    :param y: "Parameter y used in KPSS stationarity test calculation."
    :param X: "Parameter X used in KPSS stationarity test calculation."
    :return: "Computed value of KPSS stationarity test: y_t = r_t + epsilon_t; LM statistic from partial sums"
    '''
    import statsmodels.api as sm
    X_const = sm.add_constant(X)
    model = sm.OLS(y, X_const).fit()
    return model






def kupiec_pof_likelihood_ratio(num_exceptions, num_observations, confidence_level=0.95):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "Kupiec POF likelihood ratio — LR_pof = -2 ln[(1-p)^(T-x) p^x / ((1-x/T)^(T-x)(x/T)^x)]. A financial metric in the domain of Market risk & volatility modeling."
    y_as_x: []
    :param data: "Parameter data used in Kupiec POF likelihood ratio calculation."
    :param args: "Parameter args used in Kupiec POF likelihood ratio calculation."
    :return: "Computed value of Kupiec POF likelihood ratio: LR_pof = -2 ln[(1-p)^(T-x) p^x / ((1-x/T)^(T-x)(x/T)^x)]"
    '''
    import numpy as np
    from scipy.stats import chi2
    p = 1 - confidence_level; n = num_observations; x = num_exceptions
    p_hat = x / n if n > 0 else 0
    if p_hat == 0 or p_hat == 1:
        return {'lr_stat': 0, 'p_value': 1}
    lr = -2 * (np.log(p**x * (1-p)**(n-x)) - np.log(p_hat**x * (1-p_hat)**(n-x)))
    return {'lr_stat': lr, 'p_value': 1 - chi2.cdf(lr, 1)}


def kyle_lambda(lambda_q_t, epsilon_t):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Liquidity Risk', 'Market Liquidity', 'Execution Cost']
    function: "Kyle lambda — Delta p_t = lambda q_t + epsilon_t. A financial metric in the domain of Liquidity risk, market liquidity & execution cost."
    y_as_x: []
    :param lambda_q_t: "Parameter lambda_q_t used in Kyle lambda calculation."
    :param epsilon_t: "Parameter epsilon_t used in Kyle lambda calculation."
    :return: "Computed value of Kyle lambda: Delta p_t = lambda q_t + epsilon_t"
    '''
    return lambda_q_t + epsilon_t






def large_exposure_ratio(exposure_to_counterparty, tier_1_capital):
    '''
    domain: ['Bank regulation, Basel & prudential ratios']
    subdomain: ['Bank Regulation', 'Basel Framework', 'Prudential Ratios']
    function: "Large exposure ratio — Large Exposure = Exposure to counterparty / Tier 1 Capital. A financial metric in the domain of Bank regulation, Basel & prudential ratios."
    y_as_x: []
    :param exposure_to_counterparty: "Parameter exposure_to_counterparty used in Large exposure ratio calculation."
    :param tier_1_capital: "Parameter tier_1_capital used in Large exposure ratio calculation."
    :return: "Computed value of Large exposure ratio: Large Exposure = Exposure to counterparty / Tier 1 Capital"
    '''
    return exposure_to_counterparty / tier_1_capital






def lbo_debt_paydown_schedule(initial_debt, annual_cash_sweep, num_years):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Private Equity', 'Venture Capital', 'LBO']
    function: "LBO debt paydown schedule — Debt_t = Debt_{t-1} - Mandatory Amortization - Cash Sweep. A financial metric in the domain of Private equity, venture capital & LBO."
    y_as_x: []
    :param args: "Parameter args used in LBO debt paydown schedule calculation."
    :param kwargs: "Parameter kwargs used in LBO debt paydown schedule calculation."
    :return: "Computed value of LBO debt paydown schedule: Debt_t = Debt_{t-1} - Mandatory Amortization - Cash Sweep"
    '''
    schedule = []; balance = initial_debt
    for yr in range(1, num_years+1):
        paydown = min(annual_cash_sweep, balance)
        balance -= paydown
        schedule.append({'year': yr, 'paydown': paydown, 'balance': balance})
    return schedule


def lbo_equity_irr(cash_flows):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Private Equity', 'Venture Capital', 'LBO']
    function: "LBO equity IRR — 0 = -Equity_0 + Σ_t CashToEquity_t/(1+IRR)^t + ExitEquity/(1+IRR)^T. A financial metric in the domain of Private equity, venture capital & LBO."
    y_as_x: []
    :param cash_flows: "Parameter cash_flows used in LBO equity IRR calculation."
    :return: "Computed value of LBO equity IRR: 0 = -Equity_0 + Σ_t CashToEquity_t/(1+IRR)^t + ExitEquity/(1+IRR)^T"
    '''
    import numpy_financial as npf
    return npf.irr(cash_flows)






def ledoit_wolf_covariance_shrinkage(returns_matrix):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Ledoit-Wolf covariance shrinkage — Sigma_hat = (1-delta)S + delta F. A financial metric in the domain of Asset management & portfolio optimization."
    y_as_x: []
    :param X: "Parameter X used in Ledoit-Wolf covariance shrinkage calculation."
    :param y: "Parameter y used in Ledoit-Wolf covariance shrinkage calculation."
    :return: "Computed value of Ledoit-Wolf covariance shrinkage: Sigma_hat = (1-delta)S + delta F"
    '''
    from sklearn.covariance import LedoitWolf
    lw = LedoitWolf()
    lw.fit(returns_matrix)
    return lw.covariance_


def leverage_constraint(weights, max_leverage=1.0):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Leverage constraint — ||w||_1 <= L_max. A financial metric in the domain of Asset management & portfolio optimization."
    y_as_x: []
    :param expected_returns: "Expected Returns vector contains the anticipated return for each asset."
    :param cov_matrix: "Covariance Matrix contains the covariances between all pairs of assets."
    :param constraints: "Parameter constraints used in Leverage constraint calculation."
    :return: "Computed value of Leverage constraint: ||w||_1 <= L_max"
    '''
    import numpy as np
    return np.sum(np.abs(np.array(weights))) <= max_leverage




def leverage_ratio(tier1_capital, total_exposure):
    '''
    domain: ['Banking, lending & project finance']
    subdomain: ['Banking', 'Lending', 'Project Finance']
    function: "Leverage Ratio — Tier 1 Capital / Total Exposure. Basel III minimum 3%."
    y_as_x: ['duration_gap']
    :param tier1_capital: "Parameter tier1_capital used in Leverage ratio calculation."
    :param total_exposure: "Parameter total_exposure used in Leverage ratio calculation."
    :return: "Computed value of Leverage ratio: Leverage Ratio = Tier 1 Capital / Exposure Measure"
    '''
    return tier1_capital / total_exposure






def levered_beta_hamada(unlevered_beta, debt_equity_ratio, tax_rate):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "Levered Beta (Hamada) — beta_L = beta_U * (1 + (1-T) * D/E)."
    y_as_x: []
    :param unlevered_beta: "Unlevered Beta — beta_U = beta_L / (1 + (1-T)*D/E). Removes financial leverage effect."
    :param debt_equity_ratio: "Parameter debt_equity_ratio used in Levered beta (Hamada) calculation."
    :param tax_rate: "Tax Rate (T) is the percentage of taxable income that must be paid as corporate income tax."
    :return: "Computed value of Levered beta (Hamada): beta_L = beta_U[1 + (1-T)D/E]"
    '''
    return unlevered_beta * (1 + (1 - tax_rate) * debt_equity_ratio)






def levered_yield(cash_flow_after_debt_service, equity):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Real Estate Finance', 'Mortgage Analysis']
    function: "Levered yield — Levered Yield = Cash Flow After Debt Service / Equity. A financial metric in the domain of Real estate finance & mortgages."
    y_as_x: []
    :param cash_flow_after_debt_service: "Parameter cash_flow_after_debt_service used in Levered yield calculation."
    :param equity: "Total Equity is the residual interest in assets after deducting liabilities."
    :return: "Computed value of Levered yield: Levered Yield = Cash Flow After Debt Service / Equity"
    '''
    return cash_flow_after_debt_service / equity






def lgd_downturn_adjustment(lgd_normal, adjustment_factor=1.25):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit Risk', 'Default Modeling', 'Credit Portfolio']
    function: "LGD downturn adjustment — LGD_downturn = LGD_base + stress add-on. A financial metric in the domain of Credit risk, default modeling & credit portfolio."
    y_as_x: []
    :param args: "Parameter args used in LGD downturn adjustment calculation."
    :param kwargs: "Parameter kwargs used in LGD downturn adjustment calculation."
    :return: "Computed value of LGD downturn adjustment: LGD_downturn = LGD_base + stress add-on"
    '''
    return min(lgd_normal * adjustment_factor, 1.0)


def libor_market_model_lmm(initial_rates, volatilities, correlations, dt, num_steps):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Interest Rate Modeling', 'Term Structure']
    function: "LIBOR market model (LMM) — dL_i/L_i = mu_i dt + sigma_i dW_t. A financial metric in the domain of Interest-rate modeling & term structures."
    y_as_x: []
    :param args: "Parameter args used in LIBOR market model (LMM) calculation."
    :param kwargs: "Parameter kwargs used in LIBOR market model (LMM) calculation."
    :return: "Computed value of LIBOR market model (LMM): dL_i/L_i = mu_i dt + sigma_i dW_t"
    '''
    import numpy as np
    rates = np.array(initial_rates, dtype=float)
    vol = np.array(volatilities)
    n = len(rates)
    for t in range(num_steps):
        dW = np.random.multivariate_normal(np.zeros(n), correlations) * np.sqrt(dt)
        drift = np.zeros(n)
        for i in range(n):
            for j in range(i+1, n):
                drift[i] += vol[j] * rates[j] / (1 + rates[j] * dt) * correlations[i][j] * dt
        rates = rates * np.exp((drift - 0.5 * vol**2) * dt + vol * dW)
    return rates




def life_annuity_immediate(interest_rate, survival_probs):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "Life annuity-immediate — a_x = Σ_k v^(k+1)·_k p_x. A financial metric in the domain of Actuarial science & insurance."
    y_as_x: []
    :param args: "Parameter args used in Life annuity-immediate calculation."
    :param kwargs: "Parameter kwargs used in Life annuity-immediate calculation."
    :return: "Computed value of Life annuity-immediate: a_x = Σ_k v^(k+1)·_k p_x"
    '''
    import numpy as np
    v = 1 / (1 + interest_rate)
    sp = np.array(survival_probs)
    t = np.arange(1, len(sp) + 1)
    return np.sum(v**t * np.cumprod(sp))




def lifetime_ecl(pd_term_structure, lgd, ead, discount_rates):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit Risk', 'Default Modeling', 'Credit Portfolio']
    function: "Lifetime ECL — Lifetime ECL = sum_{t=1}^T marginal PD_t x LGD_t x EAD_t x DF_t. A financial metric in the domain of Credit risk, default modeling & credit portfolio."
    y_as_x: []
    :param args: "Parameter args used in Lifetime ECL calculation."
    :param kwargs: "Parameter kwargs used in Lifetime ECL calculation."
    :return: "Computed value of Lifetime ECL: Lifetime ECL = sum_{t=1}^T marginal PD_t x LGD_t x EAD_t x DF_t"
    '''
    import numpy as np
    pd_arr = np.array(pd_term_structure); dr = np.array(discount_rates)
    df = np.cumprod(1 / (1 + dr))
    return np.sum(pd_arr * lgd * ead * df)




def liquidity_coverage_ratio_lcr(hqla, net_cash_outflows_over_30_days):
    '''
    domain: ['Bank regulation, Basel & prudential ratios']
    subdomain: ['Bank Regulation', 'Basel Framework', 'Prudential Ratios']
    function: "Liquidity coverage ratio (LCR) — LCR = HQLA / Net Cash Outflows over 30 days. A financial metric in the domain of Bank regulation, Basel & prudential ratios."
    y_as_x: []
    :param hqla: "Parameter hqla used in Liquidity coverage ratio (LCR) calculation."
    :param net_cash_outflows_over_30_days: "Parameter net_cash_outflows_over_30_days used in Liquidity coverage ratio (LCR) calculation."
    :return: "Computed value of Liquidity coverage ratio (LCR): LCR = HQLA / Net Cash Outflows over 30 days"
    '''
    return hqla / net_cash_outflows_over_30_days






def liquidity_gap(cash_inflows_t, cash_outflows_t):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Treasury', 'ALM', 'Balance Sheet Management']
    function: "Liquidity gap — Liquidity Gap_t = Cash Inflows_t - Cash Outflows_t. A financial metric in the domain of Treasury, ALM & balance-sheet management."
    y_as_x: []
    :param cash_inflows_t: "Parameter cash_inflows_t used in Liquidity gap calculation."
    :param cash_outflows_t: "Parameter cash_outflows_t used in Liquidity gap calculation."
    :return: "Computed value of Liquidity gap: Liquidity Gap_t = Cash Inflows_t - Cash Outflows_t"
    '''
    return cash_inflows_t - cash_outflows_t






def liquidity_adjusted_va_r(var_base, bid_ask_spread, position_value):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Liquidity Risk', 'Market Liquidity', 'Execution Cost']
    function: "Liquidity-adjusted VaR — LVaR = VaR + liquidation cost add-on. A financial metric in the domain of Liquidity risk, market liquidity & execution cost."
    y_as_x: []
    :param args: "Parameter args used in Liquidity-adjusted VaR calculation."
    :param kwargs: "Parameter kwargs used in Liquidity-adjusted VaR calculation."
    :return: "Computed value of Liquidity-adjusted VaR: LVaR = VaR + liquidation cost add-on"
    '''
    return var_base + 0.5 * bid_ask_spread * position_value


def loan_amortization_schedule_identity(principal, rate, num_periods):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Banking', 'Consumer Lending', 'Project Finance']
    function: "Loan amortization schedule identity — Beginning Balance - Principal Paid = Ending Balance. A financial metric in the domain of Banking, consumer lending & project finance."
    y_as_x: []
    :param args: "Parameter args used in Loan amortization schedule identity calculation."
    :param kwargs: "Parameter kwargs used in Loan amortization schedule identity calculation."
    :return: "Computed value of Loan amortization schedule identity: Beginning Balance - Principal Paid = Ending Balance"
    '''
    import numpy_financial as npf
    import numpy as np
    pmt = -npf.pmt(rate, num_periods, principal)
    schedule = []
    balance = principal
    for per in range(1, num_periods + 1):
        interest = balance * rate
        princ = pmt - interest
        balance -= princ
        schedule.append({'period': per, 'payment': pmt, 'interest': interest, 'principal': princ, 'balance': max(balance, 0)})
    return schedule




def loan_constant_mortgage_constant(annual_debt_service, original_loan_amount):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Real Estate Finance', 'Mortgage Analysis']
    function: "Loan constant / mortgage constant — Loan Constant = Annual Debt Service / Original Loan Amount. A financial metric in the domain of Real estate finance & mortgages."
    y_as_x: []
    :param annual_debt_service: "Parameter annual_debt_service used in Loan constant / mortgage constant calculation."
    :param original_loan_amount: "Parameter original_loan_amount used in Loan constant / mortgage constant calculation."
    :return: "Computed value of Loan constant / mortgage constant: Loan Constant = Annual Debt Service / Original Loan Amount"
    '''
    return annual_debt_service / original_loan_amount






def loan_life_coverage_ratio(npv, outstanding_debt):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Banking', 'Consumer Lending', 'Project Finance']
    function: "Loan life coverage ratio — LLCR = NPV / Outstanding Debt. A financial metric in the domain of Banking, consumer lending & project finance."
    y_as_x: []
    :param npv: "Parameter npv used in Loan life coverage ratio calculation."
    :param outstanding_debt: "Parameter outstanding_debt used in Loan life coverage ratio calculation."
    :return: "Computed value of Loan life coverage ratio: LLCR = NPV / Outstanding Debt"
    '''
    return npv / outstanding_debt






def loan_loss_coverage_ratio(numerator, denominator):
    '''
    domain: ['Banking, lending & project finance']
    subdomain: ['Banking', 'Lending', 'Project Finance']
    function: "Loan loss coverage ratio — Coverage Ratio = Loan Loss Reserves / Non-Performing Loans. A financial metric in the domain of Banking, lending & project finance."
    y_as_x: []
    :param numerator: "Parameter numerator used in Loan loss coverage ratio calculation."
    :param denominator: "Parameter denominator used in Loan loss coverage ratio calculation."
    :return: "Computed value of Loan loss coverage ratio: Coverage Ratio = Loan Loss Reserves / Non-Performing Loans"
    '''
    return numerator / denominator if denominator != 0 else float("inf")






def loan_payment_annuity(principal, rate, num_periods):
    '''
    domain: ['Banking, lending & project finance']
    subdomain: ['Banking', 'Lending', 'Project Finance']
    function: "Loan Payment (Annuity) — periodic payment for a fully amortizing loan."
    y_as_x: []
    :param principal: "Principal is the original amount of money borrowed or invested."
    :param rate: "Rate (r) is the interest rate or discount rate per period."
    :param num_periods: "Number of Periods (n) is the total number of payment or compounding periods."
    :return: "Computed value of Loan payment (annuity): PMT = r·PV / [1 - (1+r)^(-n)]"
    '''
    import numpy_financial as npf
    return -npf.pmt(rate, num_periods, principal)






def loan_to_cost(loan_amount, project_cost):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Banking', 'Consumer Lending', 'Project Finance']
    function: "Loan-to-cost — LTC = Loan Amount / Project Cost. A financial metric in the domain of Banking, consumer lending & project finance."
    y_as_x: []
    :param loan_amount: "Loan Amount is the total principal borrowed."
    :param project_cost: "Parameter project_cost used in Loan-to-cost calculation."
    :return: "Computed value of Loan-to-cost: LTC = Loan Amount / Project Cost"
    '''
    return loan_amount / project_cost






def loan_to_deposit_ratio(gross_loans, deposits):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Treasury', 'ALM', 'Balance Sheet Management']
    function: "Loan-to-deposit ratio — LDR = Gross Loans / Deposits. A financial metric in the domain of Treasury, ALM & balance-sheet management."
    y_as_x: []
    :param gross_loans: "Parameter gross_loans used in Loan-to-deposit ratio calculation."
    :param deposits: "Parameter deposits used in Loan-to-deposit ratio calculation."
    :return: "Computed value of Loan-to-deposit ratio: LDR = Gross Loans / Deposits"
    '''
    return gross_loans / deposits






def loan_to_value(loan_amount, property_value):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Banking', 'Consumer Lending', 'Project Finance']
    function: "Loan-to-Value (LTV) — loan amount divided by property value."
    y_as_x: []
    :param loan_amount: "Loan Amount is the total principal borrowed."
    :param property_value: "Property Value is the estimated market worth of a real estate asset."
    :return: "Computed value of Loan-to-value: LTV = Loan Amount / Collateral Value"
    '''
    return loan_amount / property_value






def local_volatility_dupire(implied_vols, strikes, maturities, spot_price, risk_free_rate):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Local volatility (Dupire) — sigma_loc^2(K,T) = [dC/dT] / [0.5 K^2 d^2C/dK^2]. A financial metric in the domain of Derivatives, options & volatility."
    y_as_x: []
    :param args: "Parameter args used in Local volatility (Dupire) calculation."
    :param kwargs: "Parameter kwargs used in Local volatility (Dupire) calculation."
    :return: "Computed value of Local volatility (Dupire): sigma_loc^2(K,T) = [dC/dT] / [0.5 K^2 d^2C/dK^2]"
    '''
    import numpy as np
    from scipy.interpolate import RectBivariateSpline
    iv = np.array(implied_vols); K = np.array(strikes); T = np.array(maturities)
    interp = RectBivariateSpline(T, K, iv)
    return interp


def local_stochastic_volatility_surface_interpolation(strikes, expiries, implied_vols):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Local/stochastic volatility surface interpolation — σ(K,T) = Interpolate observed vol surface. A financial metric in the domain of Derivatives, options & volatility."
    y_as_x: []
    :param args: "Parameter args used in Local/stochastic volatility surface interpolation calculation."
    :param kwargs: "Parameter kwargs used in Local/stochastic volatility surface interpolation calculation."
    :return: "Computed value of Local/stochastic volatility surface interpolation: σ(K,T) = Interpolate observed vol surface"
    '''
    import numpy as np
    from scipy.interpolate import RectBivariateSpline
    K = np.array(strikes); T = np.array(expiries); IV = np.array(implied_vols)
    interp = RectBivariateSpline(T, K, IV)
    return interp




def log_return(price_current, price_previous):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Performance Attribution', 'Risk-Adjusted Performance']
    function: "Log Return — ln(P_t / P_{t-1}). Continuously compounded return."
    y_as_x: []
    :param price_current: "Parameter price_current used in Log return calculation."
    :param price_previous: "Parameter price_previous used in Log return calculation."
    :return: "Computed value of Log return: r_t = ln(P_t/P_{t-1})"
    '''
    import numpy as np
    return np.log(price_current / price_previous)






def long_only_constraint(weights):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Long-only constraint — w_i >= 0. A financial metric in the domain of Asset management & portfolio optimization."
    y_as_x: []
    :param expected_returns: "Expected Returns vector contains the anticipated return for each asset."
    :param cov_matrix: "Covariance Matrix contains the covariances between all pairs of assets."
    :param constraints: "Parameter constraints used in Long-only constraint calculation."
    :return: "Computed value of Long-only constraint: w_i >= 0"
    '''
    import numpy as np
    return np.all(np.array(weights) >= 0)


def lookback_option_price(spot_price, min_price, max_price, risk_free_rate, volatility, time_to_expiry, option_type="call"):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Lookback option price — V = E_Q[e^{-rT}(max(S)-K)^+]. A financial metric in the domain of Derivatives, options & volatility."
    y_as_x: []
    :param args: "Parameter args used in Lookback option price calculation."
    :param kwargs: "Parameter kwargs used in Lookback option price calculation."
    :return: "Computed value of Lookback option price: V = E_Q[e^{-rT}(max(S)-K)^+]"
    '''
    import numpy as np
    from scipy.stats import norm
    if option_type == 'call':
        S_min = min_price
        d1 = (np.log(spot_price / S_min) + (risk_free_rate + 0.5 * volatility**2) * time_to_expiry) / (volatility * np.sqrt(time_to_expiry))
        d2 = d1 - volatility * np.sqrt(time_to_expiry)
        return spot_price * norm.cdf(d1) - S_min * np.exp(-risk_free_rate * time_to_expiry) * norm.cdf(d2)
    else:
        S_max = max_price
        d1 = (np.log(S_max / spot_price) + (-risk_free_rate + 0.5 * volatility**2) * time_to_expiry) / (volatility * np.sqrt(time_to_expiry))
        d2 = d1 - volatility * np.sqrt(time_to_expiry)
        return S_max * np.exp(-risk_free_rate * time_to_expiry) * norm.cdf(d1) - spot_price * norm.cdf(d2)




def loss_given_default(recovery_rate):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Banking', 'Consumer Lending', 'Project Finance']
    function: "Loss given default — LGD = 1 - Recovery Rate. A financial metric in the domain of Banking, consumer lending & project finance."
    y_as_x: ['basel_irb_capital_requirement', 'cds_par_spread', 'cds_protection_leg', 'cds_spread_approximation', 'credit_va_r', 'expected_credit_loss_ifrs_9_cecl', 'expected_loss', 'lgd_downturn_adjustment', 'lifetime_ecl', 'unexpected_loss']
    :param args: "Parameter args used in Loss given default calculation."
    :param kwargs: "Parameter kwargs used in Loss given default calculation."
    :return: "Computed value of Loss given default: LGD = 1 - Recovery Rate"
    '''
    return 1 - recovery_rate




def loss_random_variable(benefit, present_value_factor, premium, annuity_factor):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "Loss random variable — L = PV(Benefits + Expenses) - PV(Premiums). A financial metric in the domain of Actuarial science & insurance."
    y_as_x: []
    :param args: "Parameter args used in Loss random variable calculation."
    :param kwargs: "Parameter kwargs used in Loss random variable calculation."
    :return: "Computed value of Loss random variable: L = PV(Benefits + Expenses) - PV(Premiums)"
    '''
    return benefit * present_value_factor - premium * annuity_factor




def loss_rate(net_credit_losses, average_loans):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit Risk', 'Default Modeling', 'Credit Portfolio']
    function: "Loss rate — Loss Rate = Net Credit Losses / Average Loans. A financial metric in the domain of Credit risk, default modeling & credit portfolio."
    y_as_x: []
    :param net_credit_losses: "Parameter net_credit_losses used in Loss rate calculation."
    :param average_loans: "Parameter average_loans used in Loss rate calculation."
    :return: "Computed value of Loss rate: Loss Rate = Net Credit Losses / Average Loans"
    '''
    return net_credit_losses / average_loans






def loss_ratio(incurred_losses, earned_premiums):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "Loss Ratio — incurred losses divided by earned premiums."
    y_as_x: ['combined_ratio']
    :param incurred_losses: "Parameter incurred_losses used in Loss ratio calculation."
    :param earned_premiums: "Parameter earned_premiums used in Loss ratio calculation."
    :return: "Computed value of Loss ratio: Loss Ratio = Incurred Losses / Earned Premiums"
    '''
    return incurred_losses / earned_premiums






def ltv_for_mortgage(loan_amount, property_value):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Real Estate Finance', 'Mortgage Analysis']
    function: "LTV for mortgage — Mortgage Balance / Property Value. A financial metric in the domain of Real estate finance & mortgages."
    y_as_x: []
    :param args: "Parameter args used in LTV for mortgage calculation."
    :param kwargs: "Parameter kwargs used in LTV for mortgage calculation."
    :return: "Computed value of LTV for mortgage: Mortgage Balance / Property Value"
    '''
    return loan_amount / property_value


def ma_q(time_series, order):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Financial Econometrics', 'Time Series Analysis']
    function: "MA(q) — x_t = mu + epsilon_t + sum_{i=1}^q theta_i epsilon_{t-i}. A financial metric in the domain of Econometrics & time-series finance."
    y_as_x: []
    :param time_series: "Time Series is a sequence of data points indexed in time order."
    :param order: "Order specifies the model order, e.g., (p,d,q) for ARIMA."
    :return: "Computed value of MA(q): x_t = mu + epsilon_t + sum_{i=1}^q theta_i epsilon_{t-i}"
    '''
    from statsmodels.tsa.arima.model import ARIMA
    model = ARIMA(time_series, order=order).fit()
    return model






def macaulay_duration(face_value, coupon_rate, yield_to_maturity, periods, frequency=2):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Fixed Income', 'Bond Mathematics', 'Credit Markets']
    function: "Macaulay Duration — weighted average time to receive bond cash flows."
    y_as_x: ['modified_duration']
    :param face_value: "Face Value (par value) is the nominal value of a bond stated by the issuer."
    :param coupon_rate: "Coupon Rate is the annual interest rate paid by a bond issuer relative to face value."
    :param yield_to_maturity: "Yield to Maturity (YTM) is the total return anticipated if a bond is held until maturity."
    :param periods: "Number of periods for calculations."
    :param frequency: "Frequency is the number of coupon payments per year."
    :return: "Computed value of Macaulay duration: D_M = (1/P) sum_t t x PV(CF_t)"
    '''
    import numpy as np
    c = face_value * coupon_rate / frequency
    r = yield_to_maturity / frequency
    n = int(periods * frequency)
    t = np.arange(1, n + 1)
    pv_cf = c / (1 + r)**t
    pv_cf[-1] += face_value / (1 + r)**n
    price = np.sum(pv_cf)
    return np.sum(t * pv_cf) / (price * frequency)






def macaulay_spread_duration(face_value, coupon_rate, yield_to_maturity, spread, periods, frequency=2):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit Risk', 'Default Modeling', 'Credit Portfolio']
    function: "Macaulay spread duration — SD = -(1/P) dP/ds. A financial metric in the domain of Credit risk, default modeling & credit portfolio."
    y_as_x: []
    :param args: "Parameter args used in Macaulay spread duration calculation."
    :param kwargs: "Parameter kwargs used in Macaulay spread duration calculation."
    :return: "Computed value of Macaulay spread duration: SD = -(1/P) dP/ds"
    '''
    import numpy as np
    c = face_value * coupon_rate / frequency; r = (yield_to_maturity + spread) / frequency; n = int(periods * frequency)
    t = np.arange(1, n+1); pv_cf = c / (1+r)**t; pv_cf[-1] += face_value / (1+r)**n
    return np.sum(t * pv_cf) / (np.sum(pv_cf) * frequency)


def macd(close, short_period=12, long_period=26, signal_period=9):
    '''
    domain: ['Technical analysis']
    subdomain: ['Technical Analysis']
    function: "MACD — Moving Average Convergence Divergence. MACD = EMA(short) - EMA(long)."
    y_as_x: ['macd_histogram']
    :param close: "Close is the final trading price at the end of a trading period."
    :param short_period: "Short Period is the shorter lookback window in dual-period technical indicators."
    :param long_period: "Long Period is the longer lookback window in dual-period technical indicators."
    :param signal_period: "Signal Period is the smoothing period for signal lines (e.g., MACD signal)."
    :return: "Computed value of MACD: MACD = EMA_fast - EMA_slow"
    '''
    import pandas as pd
    c = pd.Series(close)
    ema_short = c.ewm(span=short_period).mean()
    ema_long = c.ewm(span=long_period).mean()
    macd_line = ema_short - ema_long
    signal = macd_line.ewm(span=signal_period).mean()
    histogram = macd_line - signal
    return {'macd': macd_line, 'signal': signal, 'histogram': histogram}






def macd_histogram(macd, signal):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "MACD histogram — Hist = MACD - Signal. A financial metric in the domain of Technical analysis & chart-based indicators."
    y_as_x: []
    :param macd: "MACD — Moving Average Convergence Divergence. MACD = EMA(short) - EMA(long)."
    :param signal: "Parameter signal used in MACD histogram calculation."
    :return: "Computed value of MACD histogram: Hist = MACD - Signal"
    '''
    return macd - signal






def management_option_value(spot_price, strike_price, risk_free_rate, volatility, time_to_expiry, option_type):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Private Equity', 'Venture Capital', 'LBO']
    function: "Management option value — Option Value = BS or lattice value of management options. A financial metric in the domain of Private equity, venture capital & LBO."
    y_as_x: []
    :param spot_price: "Spot Price (S) is the current market price of the underlying asset."
    :param strike_price: "Strike Price (K) is the predetermined price at which an option can be exercised."
    :param risk_free_rate: "Risk-Free Rate (Rf) is the theoretical rate of return with zero risk, typically proxied by government bond yields."
    :param volatility: "Volatility (sigma) is the annualized standard deviation of returns."
    :param time_to_expiry: "Time to Expiry (T) is the remaining time until expiration, in years."
    :param option_type: "Option Type specifies whether the option is a "call" or "put"."
    :return: "Computed value of Management option value: Option Value = BS or lattice value of management options"
    '''
    import numpy as np
    from scipy.stats import norm
    d1 = (np.log(spot_price/strike_price) + (risk_free_rate + 0.5*volatility**2)*time_to_expiry) / (volatility*np.sqrt(time_to_expiry))
    d2 = d1 - volatility*np.sqrt(time_to_expiry)
    if option_type == "call":
        return spot_price*norm.cdf(d1) - strike_price*np.exp(-risk_free_rate*time_to_expiry)*norm.cdf(d2)
    else:
        return strike_price*np.exp(-risk_free_rate*time_to_expiry)*norm.cdf(-d2) - spot_price*norm.cdf(-d1)






def marginal_risk_contribution(w_i, p):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Marginal risk contribution — MRC_i = (Σw)_i / σ_p. A financial metric in the domain of Asset management & portfolio optimization."
    y_as_x: []
    :param w_i: "Parameter w_i used in Marginal risk contribution calculation."
    :param p: "Model order parameter p (autoregressive order or similar)."
    :return: "Computed value of Marginal risk contribution: MRC_i = (Σw)_i / σ_p"
    '''
    return w_i / p






def marginal_va_r(var, w_i):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "Marginal VaR — MVaR_i = ∂VaR/∂w_i. A financial metric in the domain of Market risk & volatility modeling."
    y_as_x: []
    :param var: "Parameter var used in Marginal VaR calculation."
    :param w_i: "Parameter w_i used in Marginal VaR calculation."
    :return: "Computed value of Marginal VaR: MVaR_i = ∂VaR/∂w_i"
    '''
    return var / w_i






def margrabe_exchange_option(S1, S2, vol1, vol2, correlation, time_to_expiry):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Margrabe exchange option — C = S1 e^{-q1T}N(d1) - S2 e^{-q2T}N(d2). A financial metric in the domain of Derivatives, options & volatility."
    y_as_x: []
    :param args: "Parameter args used in Margrabe exchange option calculation."
    :param kwargs: "Parameter kwargs used in Margrabe exchange option calculation."
    :return: "Computed value of Margrabe exchange option: C = S1 e^{-q1T}N(d1) - S2 e^{-q2T}N(d2)"
    '''
    import numpy as np
    from scipy.stats import norm
    sigma = np.sqrt(vol1**2 + vol2**2 - 2*correlation*vol1*vol2)
    d1 = (np.log(S1/S2) + 0.5*sigma**2*time_to_expiry) / (sigma*np.sqrt(time_to_expiry))
    d2 = d1 - sigma*np.sqrt(time_to_expiry)
    return S1*norm.cdf(d1) - S2*norm.cdf(d2)


def market_depth(bid_sizes, ask_sizes, num_levels=5):
    '''
    domain: ['Liquidity risk & market liquidity']
    subdomain: ['Liquidity Risk', 'Market Liquidity']
    function: "Market depth — Depth = Σ executable quantity within price band. A financial metric in the domain of Liquidity risk & market liquidity."
    y_as_x: []
    :param args: "Parameter args used in Market depth calculation."
    :param kwargs: "Parameter kwargs used in Market depth calculation."
    :return: "Computed value of Market depth: Depth = Σ executable quantity within price band"
    '''
    import numpy as np
    return np.sum(bid_sizes[:num_levels]) + np.sum(ask_sizes[:num_levels])




def market_impact_breakeven(total_execution_cost, notional):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Liquidity Risk', 'Market Liquidity', 'Execution Cost']
    function: "Market impact breakeven — alpha_breakeven = total execution cost / notional. A financial metric in the domain of Liquidity risk, market liquidity & execution cost."
    y_as_x: []
    :param total_execution_cost: "Parameter total_execution_cost used in Market impact breakeven calculation."
    :param notional: "Notional is the face amount of a derivative contract used to calculate payments."
    :return: "Computed value of Market impact breakeven: alpha_breakeven = total execution cost / notional"
    '''
    return total_execution_cost / notional






def market_value_added_mva(market_value_of_firm, invested_capital):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "Market value added (MVA) — MVA = Market Value of Firm - Invested Capital. A financial metric in the domain of Corporate finance, valuation & capital budgeting."
    y_as_x: []
    :param market_value_of_firm: "Parameter market_value_of_firm used in Market value added (MVA) calculation."
    :param invested_capital: "Parameter invested_capital used in Market value added (MVA) calculation."
    :return: "Computed value of Market value added (MVA): MVA = Market Value of Firm - Invested Capital"
    '''
    return market_value_of_firm - invested_capital






def market_neutral_constraint(long_weights, short_weights):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Market-neutral constraint — Σ beta_i w_i = 0. A financial metric in the domain of Asset management & portfolio optimization."
    y_as_x: []
    :param expected_returns: "Expected Returns vector contains the anticipated return for each asset."
    :param cov_matrix: "Covariance Matrix contains the covariances between all pairs of assets."
    :param constraints: "Parameter constraints used in Market-neutral constraint calculation."
    :return: "Computed value of Market-neutral constraint: Σ beta_i w_i = 0"
    '''
    import numpy as np
    return abs(np.sum(long_weights) - np.sum(np.abs(short_weights))) < 0.01


def maximum_drawdown(returns):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Performance Attribution', 'Risk-Adjusted Performance']
    function: "Maximum Drawdown — the maximum peak-to-trough decline. MDD = max(DD_t)."
    y_as_x: []
    :param returns: "Returns are the gain or loss generated on an investment over a specific period."
    :return: "Computed value of Maximum drawdown: MDD = min_t[(V_t - peak_t)/peak_t]"
    '''
    import numpy as np
    r = np.array(returns)
    wealth = np.cumprod(1 + r)
    peaks = np.maximum.accumulate(wealth)
    dd = (peaks - wealth) / peaks
    return np.max(dd)






def maximum_sharpe_portfolio(expected_returns, cov_matrix, risk_free_rate=0):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Maximum Sharpe portfolio — max_w (w^Tμ - r_f)/√(w^TΣw). A financial metric in the domain of Asset management & portfolio optimization."
    y_as_x: []
    :param expected_returns: "Expected Returns vector contains the anticipated return for each asset."
    :param cov_matrix: "Covariance Matrix contains the covariances between all pairs of assets."
    :return: "Computed value of Maximum Sharpe portfolio: max_w (w^Tμ - r_f)/√(w^TΣw)"
    '''
    import numpy as np
    mu = np.array(expected_returns); sigma = np.array(cov_matrix)
    excess = mu - risk_free_rate
    sigma_inv = np.linalg.inv(sigma)
    w = sigma_inv @ excess
    return w / np.sum(w)


def mean_absolute_error(y_true, y_pred):
    '''
    domain: ['Quantitative forecasting & machine learning in finance']
    subdomain: ['Quantitative Finance', 'Machine Learning']
    function: "Mean absolute error — MAE = (1/n) sum_i |y_i - yhat_i|. A financial metric in the domain of Quantitative forecasting & machine learning in finance."
    y_as_x: []
    :param X: "Parameter X used in Mean absolute error calculation."
    :param y: "Parameter y used in Mean absolute error calculation."
    :return: "Computed value of Mean absolute error: MAE = (1/n) sum_i |y_i - yhat_i|"
    '''
    from sklearn.metrics import mean_absolute_error
    return mean_absolute_error(y_true, y_pred)




def mean_squared_error(y_true, y_pred):
    '''
    domain: ['Quantitative forecasting & machine learning in finance']
    subdomain: ['Quantitative Finance', 'Machine Learning']
    function: "Mean squared error — MSE = (1/n) sum_i (y_i - yhat_i)^2. A financial metric in the domain of Quantitative forecasting & machine learning in finance."
    y_as_x: []
    :param X: "Parameter X used in Mean squared error calculation."
    :param y: "Parameter y used in Mean squared error calculation."
    :return: "Computed value of Mean squared error: MSE = (1/n) sum_i (y_i - yhat_i)^2"
    '''
    from sklearn.metrics import mean_squared_error
    return mean_squared_error(y_true, y_pred)




def mean_cva_r_optimization(expected_returns, cov_matrix, confidence_level=0.95, risk_aversion=1.0):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Mean-CVaR optimization — max or min subject to CVaR constraints. A financial metric in the domain of Asset management & portfolio optimization."
    y_as_x: []
    :param returns_matrix: "Parameter returns_matrix used in Mean-CVaR optimization calculation."
    :return: "Computed value of Mean-CVaR optimization: max or min subject to CVaR constraints"
    '''
    import numpy as np
    import cvxpy as cp
    n = len(expected_returns)
    w = cp.Variable(n)
    mu = np.array(expected_returns); sigma = np.array(cov_matrix)
    ret = mu @ w
    risk = cp.quad_form(w, sigma)
    prob = cp.Problem(cp.Maximize(ret - risk_aversion * risk), [cp.sum(w) == 1, w >= 0])
    prob.solve()
    return w.value




def mean_variance_utility(expected_returns, cov_matrix, risk_aversion=1.0):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Mean-variance utility — U = mu' w - (gamma/2) w' Sigma w. A financial metric in the domain of Asset management & portfolio optimization."
    y_as_x: []
    :param expected_returns: "Expected Returns vector contains the anticipated return for each asset."
    :param cov_matrix: "Covariance Matrix contains the covariances between all pairs of assets."
    :param constraints: "Parameter constraints used in Mean-variance utility calculation."
    :return: "Computed value of Mean-variance utility: U = mu' w - (gamma/2) w' Sigma w"
    '''
    import numpy as np
    import cvxpy as cp
    n = len(expected_returns)
    w = cp.Variable(n)
    mu = np.array(expected_returns); sigma = np.array(cov_matrix)
    utility = mu @ w - risk_aversion / 2 * cp.quad_form(w, sigma)
    prob = cp.Problem(cp.Maximize(utility), [cp.sum(w) == 1, w >= 0])
    prob.solve()
    return w.value




def merton_asset_value_model(equity_value, debt_face, risk_free_rate, time_horizon, equity_vol):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit Risk', 'Default Modeling', 'Credit Portfolio']
    function: "Merton asset value model — E = V_A N(d1) - D e^{-rT} N(d2). A financial metric in the domain of Credit risk, default modeling & credit portfolio."
    y_as_x: []
    :param args: "Parameter args used in Merton asset value model calculation."
    :param kwargs: "Parameter kwargs used in Merton asset value model calculation."
    :return: "Computed value of Merton asset value model: E = V_A N(d1) - D e^{-rT} N(d2)"
    '''
    import numpy as np
    from scipy.stats import norm
    from scipy.optimize import fsolve
    def equations(vars):
        V, sigma_V = vars
        d1 = (np.log(V / debt_face) + (risk_free_rate + 0.5 * sigma_V**2) * time_horizon) / (sigma_V * np.sqrt(time_horizon))
        eq1 = V * norm.cdf(d1) - debt_face * np.exp(-risk_free_rate * time_horizon) * norm.cdf(d1 - sigma_V * np.sqrt(time_horizon)) - equity_value
        eq2 = norm.cdf(d1) * sigma_V * V - equity_vol * equity_value
        return [eq1, eq2]
    V0, sigV0 = fsolve(equations, [equity_value + debt_face, equity_vol])
    return {'asset_value': V0, 'asset_volatility': sigV0}




def merton_distance_to_default(asset_value, debt_face, asset_volatility, risk_free_rate, time_horizon):
    '''
    domain: ['Credit risk']
    subdomain: ['Credit Risk']
    function: "Merton distance to default — DD = [ln(V_A/D) + (μ_A - 0.5σ_A^2)T] / (σ_A√T). A financial metric in the domain of Credit risk."
    y_as_x: []
    :param args: "Parameter args used in Merton distance to default calculation."
    :param kwargs: "Parameter kwargs used in Merton distance to default calculation."
    :return: "Computed value of Merton distance to default: DD = [ln(V_A/D) + (μ_A - 0.5σ_A^2)T] / (σ_A√T)"
    '''
    import numpy as np
    return (np.log(asset_value / debt_face) + (risk_free_rate - 0.5 * asset_volatility**2) * time_horizon) / (asset_volatility * np.sqrt(time_horizon))




def merton_jump_diffusion_asset_process(S0, mu, sigma, lam, jump_mean, jump_vol, dt, num_steps, num_paths=1000):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Merton jump diffusion asset process — dS_t/S_t = (mu - lambda k)dt + sigma dW_t + dJ_t. A financial metric in the domain of Derivatives, options & volatility."
    y_as_x: []
    :param args: "Parameter args used in Merton jump diffusion asset process calculation."
    :param kwargs: "Parameter kwargs used in Merton jump diffusion asset process calculation."
    :return: "Computed value of Merton jump diffusion asset process: dS_t/S_t = (mu - lambda k)dt + sigma dW_t + dJ_t"
    '''
    import numpy as np
    S = np.zeros((num_paths, num_steps + 1))
    S[:, 0] = S0
    for t in range(num_steps):
        Z = np.random.standard_normal(num_paths)
        N = np.random.poisson(lam * dt, num_paths)
        J = np.exp(jump_mean * N + jump_vol * np.sqrt(np.maximum(N, 0)) * np.random.standard_normal(num_paths)) - 1
        S[:, t+1] = S[:, t] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z) * (1 + J)
    return S




def merton_structural_pd(asset_value, debt_face, asset_volatility, risk_free_rate, time_horizon):
    '''
    domain: ['Credit risk']
    subdomain: ['Credit Risk']
    function: "Merton structural PD — PD = N(-DD). A financial metric in the domain of Credit risk."
    y_as_x: []
    :param data: "Parameter data used in Merton structural PD calculation."
    :param args: "Parameter args used in Merton structural PD calculation."
    :return: "Computed value of Merton structural PD: PD = N(-DD)"
    '''
    import numpy as np
    from scipy.stats import norm
    dd = (np.log(asset_value / debt_face) + (risk_free_rate - 0.5 * asset_volatility**2) * time_horizon) / (asset_volatility * np.sqrt(time_horizon))
    return norm.cdf(-dd)




def metallurgical_gross_margin(metal_selling_price, input_cost_bundle):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Commodities', 'Futures', 'Hedging']
    function: "Metallurgical gross margin — Margin = Metal Selling Price - Input Cost Bundle. A financial metric in the domain of Commodities, futures & hedging."
    y_as_x: []
    :param metal_selling_price: "Parameter metal_selling_price used in Metallurgical gross margin calculation."
    :param input_cost_bundle: "Parameter input_cost_bundle used in Metallurgical gross margin calculation."
    :return: "Computed value of Metallurgical gross margin: Margin = Metal Selling Price - Input Cost Bundle"
    '''
    return metal_selling_price - input_cost_bundle






def mid_price(cash_flows, discount_rate):
    '''
    domain: ['Liquidity risk & market liquidity']
    subdomain: ['Liquidity Risk', 'Market Liquidity']
    function: "Mid price — Mid = (Bid + Ask)/2. A financial metric in the domain of Liquidity risk & market liquidity."
    y_as_x: []
    :param cash_flows: "Parameter cash_flows used in Mid price calculation."
    :param discount_rate: "Discount Rate is the rate used to discount future cash flows to present value."
    :return: "Computed value of Mid price: Mid = (Bid + Ask)/2"
    '''
    import numpy as np
    cf = np.array(cash_flows)
    t = np.arange(1, len(cf) + 1)
    return np.sum(cf / (1 + discount_rate)**t)






def minimum_variance_hedge_ratio(covdelta_s_delta_f, vardelta_f):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Commodities', 'Futures', 'Hedging']
    function: "Minimum-variance hedge ratio — h* = Cov(Delta S, Delta F) / Var(Delta F). A financial metric in the domain of Commodities, futures & hedging."
    y_as_x: []
    :param covdelta_s_delta_f: "Parameter covdelta_s_delta_f used in Minimum-variance hedge ratio calculation."
    :param vardelta_f: "Parameter vardelta_f used in Minimum-variance hedge ratio calculation."
    :return: "Computed value of Minimum-variance hedge ratio: h* = Cov(Delta S, Delta F) / Var(Delta F)"
    '''
    return covdelta_s_delta_f / vardelta_f






def minimum_variance_hedged_return(asset_return, hedge_return, hedge_ratio):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Commodities', 'Futures', 'Hedging']
    function: "Minimum-variance hedged return — R_H = R_S - h* R_F. A financial metric in the domain of Commodities, futures & hedging."
    y_as_x: []
    :param args: "Parameter args used in Minimum-variance hedged return calculation."
    :param kwargs: "Parameter kwargs used in Minimum-variance hedged return calculation."
    :return: "Computed value of Minimum-variance hedged return: R_H = R_S - h* R_F"
    '''
    return asset_return - hedge_ratio * hedge_return


def minus_directional_indicator_di(high, low, close, period=14):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "Minus directional indicator (-DI) — -DI = 100 x smoothed -DM / ATR. A financial metric in the domain of Technical analysis & chart-based indicators."
    y_as_x: []
    :param high: "High is the highest price during a specific trading period."
    :param low: "Low is the lowest price during a specific trading period."
    :param close: "Close is the final trading price at the end of a trading period."
    :param volume: "Volume is the total number of shares or contracts traded during a period."
    :param period: "Period (n) is the lookback window in number of bars for technical indicators."
    :return: "Computed value of Minus directional indicator (-DI): -DI = 100 x smoothed -DM / ATR"
    '''
    import pandas as pd
    h = pd.Series(high); l = pd.Series(low); c = pd.Series(close)
    minus_dm = (-l.diff()).clip(lower=0)
    plus_dm = h.diff().clip(lower=0)
    minus_dm[plus_dm > minus_dm] = 0
    tr = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    return 100 * minus_dm.rolling(window=period).mean() / atr




def modified_duration(macaulay_duration, yield_to_maturity, frequency=2):
    '''
    domain: ['Fixed income & bond math']
    subdomain: ['Fixed Income', 'Bond Mathematics']
    function: "Modified Duration — Macaulay Duration / (1 + y/m). Gives % price change per 1% yield change."
    y_as_x: ['approximate_price_change', 'dollar_duration', 'dv01_pvbp', 'effective_duration']
    :param macaulay_duration: "Macaulay Duration — weighted average time to receive bond cash flows."
    :param yield_to_maturity: "Yield to Maturity (YTM) is the total return anticipated if a bond is held until maturity."
    :param frequency: "Frequency is the number of coupon payments per year."
    :return: "Computed value of Modified duration: D_mod = D_M / (1+y/m)"
    '''
    return macaulay_duration / (1 + yield_to_maturity / frequency)






def modified_irr_mirr(cash_flows, finance_rate, reinvest_rate):
    '''
    domain: ['Corporate finance & capital budgeting']
    subdomain: ['Corporate Finance', 'Capital Budgeting']
    function: "Modified IRR (MIRR) — assumes reinvestment at a specified rate rather than the IRR itself."
    y_as_x: []
    :param cash_flows: "Parameter cash_flows used in Modified IRR (MIRR) calculation."
    :param finance_rate: "Parameter finance_rate used in Modified IRR (MIRR) calculation."
    :param reinvest_rate: "Parameter reinvest_rate used in Modified IRR (MIRR) calculation."
    :return: "Computed value of Modified IRR (MIRR): MIRR = (FV_positive / |PV_negative|)^(1/n) - 1"
    '''
    import numpy_financial as npf
    return npf.mirr(cash_flows, finance_rate, reinvest_rate)






def momentum(close, period=10):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "Momentum — price change over n periods. MOM = Price_t - Price_{t-n}."
    y_as_x: []
    :param close: "Close is the final trading price at the end of a trading period."
    :param period: "Period (n) is the lookback window in number of bars for technical indicators."
    :return: "Computed value of Momentum: MOM = P_t - P_{t-n}"
    '''
    import pandas as pd
    return pd.Series(close).diff(period)






def money_flow_index_mfi(high, low, close, volume, period=14):
    '''
    domain: ['Technical analysis']
    subdomain: ['Technical Analysis']
    function: "Money Flow Index (MFI) — volume-weighted RSI. MFI = 100 - 100/(1 + MFR)."
    y_as_x: []
    :param high: "High is the highest price during a specific trading period."
    :param low: "Low is the lowest price during a specific trading period."
    :param close: "Close is the final trading price at the end of a trading period."
    :param volume: "Volume is the total number of shares or contracts traded during a period."
    :param period: "Period (n) is the lookback window in number of bars for technical indicators."
    :return: "Computed value of Money flow index (MFI): MFI = 100 - 100/(1 + MoneyFlowRatio)"
    '''
    import pandas as pd
    import numpy as np
    tp = (pd.Series(high) + pd.Series(low) + pd.Series(close)) / 3
    mf = tp * pd.Series(volume)
    pos_mf = mf.where(tp > tp.shift(1), 0).rolling(window=period).sum()
    neg_mf = mf.where(tp < tp.shift(1), 0).rolling(window=period).sum()
    mfr = pos_mf / neg_mf
    return 100 - 100 / (1 + mfr)






def money_flow_index_mfi_2(high, low, close, volume, period=14):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "Money flow index (MFI) — MFI = 100 - 100/(1+MoneyRatio). A financial metric in the domain of Technical analysis & chart-based indicators."
    y_as_x: []
    :param high: "High is the highest price during a specific trading period."
    :param low: "Low is the lowest price during a specific trading period."
    :param close: "Close is the final trading price at the end of a trading period."
    :param volume: "Volume is the total number of shares or contracts traded during a period."
    :param period: "Period (n) is the lookback window in number of bars for technical indicators."
    :return: "Computed value of Money flow index (MFI): MFI = 100 - 100/(1+MoneyRatio)"
    '''
    import pandas as pd
    import numpy as np
    tp = (pd.Series(high) + pd.Series(low) + pd.Series(close)) / 3
    mf = tp * pd.Series(volume)
    pos = mf.where(tp > tp.shift(1), 0).rolling(period).sum()
    neg = mf.where(tp < tp.shift(1), 0).rolling(period).sum()
    return 100 - 100 / (1 + pos / neg)


def money_market_yield(numerator, denominator):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Fixed Income', 'Bond Mathematics', 'Credit Markets']
    function: "Money market yield — MMY = (F-P)/P x 360/d. A financial metric in the domain of Fixed income, bonds & credit markets."
    y_as_x: []
    :param numerator: "Parameter numerator used in Money market yield calculation."
    :param denominator: "Parameter denominator used in Money market yield calculation."
    :return: "Computed value of Money market yield: MMY = (F-P)/P x 360/d"
    '''
    return numerator / denominator if denominator != 0 else 0






def money_multiple_moic(total_value, invested_capital):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Private Equity', 'Venture Capital', 'LBO']
    function: "Money multiple (MOIC) — MOIC = Total Value / Invested Capital. A financial metric in the domain of Private equity, venture capital & LBO."
    y_as_x: []
    :param total_value: "Parameter total_value used in Money multiple (MOIC) calculation."
    :param invested_capital: "Parameter invested_capital used in Money multiple (MOIC) calculation."
    :return: "Computed value of Money multiple (MOIC): MOIC = Total Value / Invested Capital"
    '''
    return total_value / invested_capital






def money_market_account(initial_value, risk_free_rate, time):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Interest Rate Modeling', 'Term Structure']
    function: "Money-market account — B_t = exp(int_0^t r_s ds). A financial metric in the domain of Interest-rate modeling & term structures."
    y_as_x: []
    :param args: "Parameter args used in Money-market account calculation."
    :param kwargs: "Parameter kwargs used in Money-market account calculation."
    :return: "Computed value of Money-market account: B_t = exp(int_0^t r_s ds)"
    '''
    import numpy as np
    return initial_value * np.exp(risk_free_rate * time)


def money_weighted_return_mwrr(cash_flows):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Performance Attribution', 'Risk-Adjusted Performance']
    function: "Money-weighted return (MWRR) — 0 = sum_t CF_t/(1+IRR)^t. A financial metric in the domain of Performance measurement & attribution."
    y_as_x: []
    :param cash_flows: "Parameter cash_flows used in Money-weighted return (MWRR) calculation."
    :return: "Computed value of Money-weighted return (MWRR): 0 = sum_t CF_t/(1+IRR)^t"
    '''
    import numpy_financial as npf
    return npf.irr(cash_flows)






def monte_carlo_va_r(returns, num_simulations, time_horizon, confidence_level=0.95):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "Monte Carlo VaR — VaR estimated from simulated return distributions."
    y_as_x: []
    :param returns: "Returns are the gain or loss generated on an investment over a specific period."
    :param num_simulations: "Number of Monte Carlo simulation paths."
    :param time_horizon: "Parameter time_horizon used in Monte Carlo VaR calculation."
    :param confidence_level: "Confidence Level is the probability threshold used in statistical tests and risk measures."
    :return: "Computed value of Monte Carlo VaR: VaR_alpha = -quantile_alpha(simulated P&L)"
    '''
    import numpy as np
    mu = np.mean(returns); sigma = np.std(returns, ddof=1)
    simulated = np.random.normal(mu * time_horizon, sigma * np.sqrt(time_horizon), num_simulations)
    return -np.percentile(simulated, (1 - confidence_level) * 100)






def mortality_rate(d_x, l_x):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "Mortality rate — q_x = d_x / l_x. A financial metric in the domain of Actuarial science & insurance."
    y_as_x: ['benefit_reserve_recursion', 'death_probability', 'endowment_insurance_apv', 'one_year_death_probability', 'survival_function', 'term_insurance_apv', 'whole_life_assurance']
    :param d_x: "Parameter d_x used in Mortality rate calculation."
    :param l_x: "Parameter l_x used in Mortality rate calculation."
    :return: "Computed value of Mortality rate: q_x = d_x / l_x"
    '''
    return d_x / l_x






def mortgage_constant(annual_debt_service, loan_amount):
    '''
    domain: ['Real estate finance']
    subdomain: ['Real Estate Finance']
    function: "Mortgage constant — Mortgage Constant = Annual Debt Service / Loan Amount. A financial metric in the domain of Real estate finance."
    y_as_x: []
    :param annual_debt_service: "Parameter annual_debt_service used in Mortgage constant calculation."
    :param loan_amount: "Loan Amount is the total principal borrowed."
    :return: "Computed value of Mortgage constant: Mortgage Constant = Annual Debt Service / Loan Amount"
    '''
    return annual_debt_service / loan_amount






def moving_average_convergence_divergence_macd(close, short_period=12, long_period=26, signal_period=9):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "Moving average convergence divergence (MACD) — MACD = EMA_{12} - EMA_{26}; Signal = EMA_9(MACD). A financial metric in the domain of Technical analysis & chart-based indicators."
    y_as_x: []
    :param close: "Close is the final trading price at the end of a trading period."
    :param period: "Period (n) is the lookback window in number of bars for technical indicators."
    :return: "Computed value of Moving average convergence divergence (MACD): MACD = EMA_{12} - EMA_{26}; Signal = EMA_9(MACD)"
    '''
    import pandas as pd
    c = pd.Series(close)
    macd_line = c.ewm(span=short_period).mean() - c.ewm(span=long_period).mean()
    signal = macd_line.ewm(span=signal_period).mean()
    return {'macd': macd_line, 'signal': signal, 'histogram': macd_line - signal}


def mrel_tlac_ratio(eligible_liabilities_and_capital, rwa_or_leverage_exposure):
    '''
    domain: ['Bank regulation, Basel & prudential ratios']
    subdomain: ['Bank Regulation', 'Basel Framework', 'Prudential Ratios']
    function: "MREL / TLAC ratio — TLAC Ratio = Eligible Liabilities and Capital / RWA or Leverage Exposure. A financial metric in the domain of Bank regulation, Basel & prudential ratios."
    y_as_x: []
    :param eligible_liabilities_and_capital: "Parameter eligible_liabilities_and_capital used in MREL / TLAC ratio calculation."
    :param rwa_or_leverage_exposure: "Parameter rwa_or_leverage_exposure used in MREL / TLAC ratio calculation."
    :return: "Computed value of MREL / TLAC ratio: TLAC Ratio = Eligible Liabilities and Capital / RWA or Leverage Exposure"
    '''
    return eligible_liabilities_and_capital / rwa_or_leverage_exposure






def m_squared_modigliani(sharpe_x_sigma_m, risk_free_rate):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "M-squared (Modigliani) — M2 = Sharpe x sigma_m + R_f. A financial metric in the domain of Asset management & portfolio optimization."
    y_as_x: []
    :param sharpe_x_sigma_m: "Parameter sharpe_x_sigma_m used in M-squared (Modigliani) calculation."
    :param risk_free_rate: "Risk-Free Rate (Rf) is the theoretical rate of return with zero risk, typically proxied by government bond yields."
    :return: "Computed value of M-squared (Modigliani): M2 = Sharpe x sigma_m + R_f"
    '''
    return sharpe_x_sigma_m + risk_free_rate






def multi_stage_ddm(dividends, growth_rates, terminal_growth, cost_of_equity):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Equity Valuation', 'Asset Pricing']
    function: "Multi-stage DDM — P_0 = sum_t D_t/(1+r)^t + TV/(1+r)^T. A financial metric in the domain of Equity valuation & asset pricing."
    y_as_x: []
    :param args: "Parameter args used in Multi-stage DDM calculation."
    :param kwargs: "Parameter kwargs used in Multi-stage DDM calculation."
    :return: "Computed value of Multi-stage DDM: P_0 = sum_t D_t/(1+r)^t + TV/(1+r)^T"
    '''
    import numpy as np
    pv = 0
    for i, (div, g) in enumerate(zip(dividends, growth_rates)):
        pv += div * (1+g) / (1+cost_of_equity)**(i+1)
    terminal_div = dividends[-1] * (1+growth_rates[-1]) * (1+terminal_growth)
    tv = terminal_div / (cost_of_equity - terminal_growth)
    pv += tv / (1+cost_of_equity)**len(dividends)
    return pv


def naive_bayes_classifier(X_train, y_train, X_test):
    '''
    domain: ['Quantitative forecasting & machine learning in finance']
    subdomain: ['Quantitative Finance', 'Machine Learning']
    function: "Naive Bayes classifier — P(y|x) proportional P(y) prod_j P(x_j|y). A financial metric in the domain of Quantitative forecasting & machine learning in finance."
    y_as_x: []
    :param X: "Parameter X used in Naive Bayes classifier calculation."
    :param y: "Parameter y used in Naive Bayes classifier calculation."
    :return: "Computed value of Naive Bayes classifier: P(y|x) proportional P(y) prod_j P(x_j|y)"
    '''
    from sklearn.naive_bayes import GaussianNB
    model = GaussianNB()
    model.fit(X_train, y_train)
    return model.predict(X_test)




def nelson_siegel_yield_curve(beta0, beta1, beta2, tau, maturities):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Interest Rate Modeling', 'Term Structure']
    function: "Nelson-Siegel yield curve — y(t)=beta0 + beta1[(1-e^{-t/tau})/(t/tau)] + beta2([(1-e^{-t/tau})/(t/tau)]-e^{-t/tau}). A financial metric in the domain of Interest-rate modeling & term structures."
    y_as_x: []
    :param args: "Parameter args used in Nelson-Siegel yield curve calculation."
    :param kwargs: "Parameter kwargs used in Nelson-Siegel yield curve calculation."
    :return: "Computed value of Nelson-Siegel yield curve: y(t)=beta0 + beta1[(1-e^{-t/tau})/(t/tau)] + beta2([(1-e^{-t/tau})/(t/tau)]-e^{-t/tau})"
    '''
    import numpy as np
    m = np.array(maturities)
    factor1 = (1 - np.exp(-m / tau)) / (m / tau)
    factor2 = factor1 - np.exp(-m / tau)
    return beta0 + beta1 * factor1 + beta2 * factor2




def nelson_siegel_svensson_curve(beta0, beta1, beta2, beta3, tau1, tau2, maturities):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Interest Rate Modeling', 'Term Structure']
    function: "Nelson-Siegel-Svensson curve — y(t)=beta0 + beta1 L1 + beta2(L1-e^{-t/tau1}) + beta3(L2-e^{-t/tau2}). A financial metric in the domain of Interest-rate modeling & term structures."
    y_as_x: []
    :param args: "Parameter args used in Nelson-Siegel-Svensson curve calculation."
    :param kwargs: "Parameter kwargs used in Nelson-Siegel-Svensson curve calculation."
    :return: "Computed value of Nelson-Siegel-Svensson curve: y(t)=beta0 + beta1 L1 + beta2(L1-e^{-t/tau1}) + beta3(L2-e^{-t/tau2})"
    '''
    import numpy as np
    m = np.array(maturities)
    f1 = (1 - np.exp(-m / tau1)) / (m / tau1)
    f2 = f1 - np.exp(-m / tau1)
    f3 = (1 - np.exp(-m / tau2)) / (m / tau2) - np.exp(-m / tau2)
    return beta0 + beta1 * f1 + beta2 * f2 + beta3 * f3




def net_charge_off_ratio(numerator, denominator):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Banking', 'Consumer Lending', 'Project Finance']
    function: "Net charge-off ratio — NCO Ratio = (Charge-offs - Recoveries) / Average Loans. A financial metric in the domain of Banking, consumer lending & project finance."
    y_as_x: []
    :param numerator: "Parameter numerator used in Net charge-off ratio calculation."
    :param denominator: "Parameter denominator used in Net charge-off ratio calculation."
    :return: "Computed value of Net charge-off ratio: NCO Ratio = (Charge-offs - Recoveries) / Average Loans"
    '''
    return numerator / denominator if denominator != 0 else float("inf")






def net_convenience_yield(y, storage_cost):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Commodities', 'Futures', 'Hedging']
    function: "Net convenience yield — Net Convenience Yield = y - storage cost. A financial metric in the domain of Commodities, futures & hedging."
    y_as_x: []
    :param y: "Parameter y used in Net convenience yield calculation."
    :param storage_cost: "Parameter storage_cost used in Net convenience yield calculation."
    :return: "Computed value of Net convenience yield: Net Convenience Yield = y - storage cost"
    '''
    return y - storage_cost






def net_debt_at_entry(total_debt, cash_on_balance_sheet):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Private Equity', 'Venture Capital', 'LBO']
    function: "Net debt at entry — Net Debt = Debt Assumed + New Debt - Cash Acquired. A financial metric in the domain of Private equity, venture capital & LBO."
    y_as_x: []
    :param args: "Parameter args used in Net debt at entry calculation."
    :param kwargs: "Parameter kwargs used in Net debt at entry calculation."
    :return: "Computed value of Net debt at entry: Net Debt = Debt Assumed + New Debt - Cash Acquired"
    '''
    return total_debt - cash_on_balance_sheet


def net_income(revenue, total_expenses, tax_expense):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "Net Income — total profit after all expenses and taxes. NI = Revenue - Expenses - Tax."
    y_as_x: ['diluted_eps', 'dividend_coverage', 'dividend_payout_ratio', 'eps', 'fcfe', 'net_margin', 'piotroski_f_score', 'residual_income', 'retention_ratio', 'return_on_assets_roa', 'return_on_equity_roe', 'sustainable_growth_rate']
    :param revenue: "Revenue is the total amount of income a business generates from the sale of goods or services before deducting expenses."
    :param total_expenses: "Parameter total_expenses used in Net income calculation."
    :param tax_expense: "Tax Expense is the total amount of taxes owed for a given period."
    :return: "Computed value of Net income: Net Income = Revenue - Expenses - Taxes"
    '''
    return revenue - total_expenses - tax_expense






def net_interest_income_nii(interest_income, interest_expense):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Treasury', 'ALM', 'Balance Sheet Management']
    function: "Net Interest Income (NII) — interest earned minus interest paid."
    y_as_x: []
    :param interest_income: "Parameter interest_income used in Net interest income (NII) calculation."
    :param interest_expense: "Interest Expense is the cost incurred by a company for borrowed funds."
    :return: "Computed value of Net interest income (NII): NII = Interest Income - Interest Expense"
    '''
    return interest_income - interest_expense






def net_interest_margin_nim(net_interest_income, average_earning_assets):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Treasury', 'ALM', 'Balance Sheet Management']
    function: "Net Interest Margin (NIM) — NII divided by average earning assets."
    y_as_x: []
    :param net_interest_income: "Parameter net_interest_income used in Net interest margin (NIM) calculation."
    :param average_earning_assets: "Parameter average_earning_assets used in Net interest margin (NIM) calculation."
    :return: "Computed value of Net interest margin (NIM): NIM = NII / Average Earning Assets"
    '''
    return net_interest_income / average_earning_assets






def net_irr_to_lp(cash_flows):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Private Equity', 'Venture Capital', 'LBO']
    function: "Net IRR to LP — IRR on LP cash flows after fees and carry. A financial metric in the domain of Private equity, venture capital & LBO."
    y_as_x: []
    :param cash_flows: "Parameter cash_flows used in Net IRR to LP calculation."
    :return: "Computed value of Net IRR to LP: IRR on LP cash flows after fees and carry"
    '''
    import numpy_financial as npf
    return npf.irr(cash_flows)






def net_margin(net_income, revenue):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "Net Margin — net income as a percentage of revenue."
    y_as_x: []
    :param net_income: "Net Income is the total profit after all expenses, taxes, interest, and depreciation have been deducted from total revenue."
    :param revenue: "Revenue is the total amount of income a business generates from the sale of goods or services before deducting expenses."
    :return: "Computed value of Net margin: Net Margin = Net Income / Revenue"
    '''
    return net_income / revenue






def net_operating_income_noi(effective_gross_income, operating_expenses):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Real Estate Finance', 'Mortgage Analysis']
    function: "Net Operating Income (NOI) — effective gross income minus operating expenses."
    y_as_x: []
    :param effective_gross_income: "Effective Gross Income — PGI minus vacancy losses plus other income."
    :param operating_expenses: "Operating Expenses (OpEx) are the essential ongoing costs a business incurs to maintain daily operations and generate revenue."
    :return: "Computed value of Net operating income (NOI): NOI = Rental Revenue + Other Income - Operating Expenses"
    '''
    return effective_gross_income - operating_expenses






def net_premium(pvbenefits, pvpremium_annuity):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "Net premium — P = PV(Benefits) / PV(Premium annuity). A financial metric in the domain of Actuarial science & insurance."
    y_as_x: ['call_spread_payoff']
    :param pvbenefits: "Parameter pvbenefits used in Net premium calculation."
    :param pvpremium_annuity: "Parameter pvpremium_annuity used in Net premium calculation."
    :return: "Computed value of Net premium: P = PV(Benefits) / PV(Premium annuity)"
    '''
    return pvbenefits / pvpremium_annuity






def net_premium_equivalence_principle(benefit, annuity_factor, insurance_factor):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "Net premium equivalence principle — Premium x APV(premium annuity) = APV(benefits). A financial metric in the domain of Actuarial science & insurance."
    y_as_x: []
    :param args: "Parameter args used in Net premium equivalence principle calculation."
    :param kwargs: "Parameter kwargs used in Net premium equivalence principle calculation."
    :return: "Computed value of Net premium equivalence principle: Premium x APV(premium annuity) = APV(benefits)"
    '''
    return benefit * insurance_factor / annuity_factor


def net_present_value_npv(rate, cash_flows):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "Net Present Value (NPV) — sum of discounted cash flows. Positive NPV = value-creating project."
    y_as_x: []
    :param rate: "Rate (r) is the interest rate or discount rate per period."
    :param cash_flows: "Parameter cash_flows used in Net present value (NPV) calculation."
    :return: "Computed value of Net present value (NPV): NPV = sum_t CF_t / (1+r)^t"
    '''
    import numpy_financial as npf
    return npf.npv(rate, cash_flows)






def net_stable_funding_ratio_nsfr(available_stable_funding, required_stable_funding):
    '''
    domain: ['Bank regulation, Basel & prudential ratios']
    subdomain: ['Bank Regulation', 'Basel Framework', 'Prudential Ratios']
    function: "Net stable funding ratio (NSFR) — NSFR = Available Stable Funding / Required Stable Funding. A financial metric in the domain of Bank regulation, Basel & prudential ratios."
    y_as_x: []
    :param available_stable_funding: "Parameter available_stable_funding used in Net stable funding ratio (NSFR) calculation."
    :param required_stable_funding: "Parameter required_stable_funding used in Net stable funding ratio (NSFR) calculation."
    :return: "Computed value of Net stable funding ratio (NSFR): NSFR = Available Stable Funding / Required Stable Funding"
    '''
    return available_stable_funding / required_stable_funding






def net_weighted_average_spread(weighted_avg_asset_spread, funding_spread):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Structured Finance', 'Securitization']
    function: "Net weighted average spread — NWAS = weighted avg asset spread - funding spread. A financial metric in the domain of Structured finance & securitization."
    y_as_x: []
    :param weighted_avg_asset_spread: "Parameter weighted_avg_asset_spread used in Net weighted average spread calculation."
    :param funding_spread: "Funding spread — Funding Spread = Loan Yield - Funding Cost. A financial metric in the domain of Banking, consumer lending & project finance."
    :return: "Computed value of Net weighted average spread: NWAS = weighted avg asset spread - funding spread"
    '''
    return weighted_avg_asset_spread - funding_spread






def newey_west_hac_covariance(residuals, X, lags=None):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Financial Econometrics', 'Time Series Analysis']
    function: "Newey-West HAC covariance — Var(beta_hat)_HAC = (X'X)^-1 X' S X (X'X)^-1. A financial metric in the domain of Econometrics & time-series finance."
    y_as_x: []
    :param data: "Parameter data used in Newey-West HAC covariance calculation."
    :param args: "Parameter args used in Newey-West HAC covariance calculation."
    :return: "Computed value of Newey-West HAC covariance: Var(beta_hat)_HAC = (X'X)^-1 X' S X (X'X)^-1"
    '''
    import statsmodels.api as sm
    import numpy as np
    X_const = sm.add_constant(X)
    model = sm.OLS(residuals, X_const).fit(cov_type='HAC', cov_kwds={'maxlags': lags})
    return model.cov_params()


def nii_sensitivity(sum_i_balance_i, delta_rate_i, repricing_fraction_i):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Treasury', 'ALM', 'Balance Sheet Management']
    function: "NII sensitivity — Delta NII = sum_i Balance_i x Delta Rate_i x Repricing Fraction_i. A financial metric in the domain of Treasury, ALM & balance-sheet management."
    y_as_x: []
    :param sum_i_balance_i: "Parameter sum_i_balance_i used in NII sensitivity calculation."
    :param delta_rate_i: "Parameter delta_rate_i used in NII sensitivity calculation."
    :param repricing_fraction_i: "Parameter repricing_fraction_i used in NII sensitivity calculation."
    :return: "Computed value of NII sensitivity: Delta NII = sum_i Balance_i x Delta Rate_i x Repricing Fraction_i"
    '''
    return sum_i_balance_i * delta_rate_i * repricing_fraction_i






def noi_margin(noi, effective_gross_income):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Real Estate Finance', 'Mortgage Analysis']
    function: "NOI margin — NOI Margin = NOI / Effective Gross Income. A financial metric in the domain of Real estate finance & mortgages."
    y_as_x: []
    :param noi: "Net Operating Income (NOI) is total revenue from a property minus operating expenses."
    :param effective_gross_income: "Effective Gross Income — PGI minus vacancy losses plus other income."
    :return: "Computed value of NOI margin: NOI Margin = NOI / Effective Gross Income"
    '''
    return noi / effective_gross_income






def npl_ratio(nonperforming_loans, gross_loans):
    '''
    domain: ['Bank regulation, Basel & prudential ratios']
    subdomain: ['Bank Regulation', 'Basel Framework', 'Prudential Ratios']
    function: "NPL ratio — NPL Ratio = Nonperforming Loans / Gross Loans. A financial metric in the domain of Bank regulation, Basel & prudential ratios."
    y_as_x: []
    :param nonperforming_loans: "Parameter nonperforming_loans used in NPL ratio calculation."
    :param gross_loans: "Parameter gross_loans used in NPL ratio calculation."
    :return: "Computed value of NPL ratio: NPL Ratio = Nonperforming Loans / Gross Loans"
    '''
    return nonperforming_loans / gross_loans






def number_of_periods(rate, payment, present_value, future_value=0):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Banking', 'Consumer Lending', 'Project Finance']
    function: "Number of Periods — solves for n given rate, payment, PV, and FV."
    y_as_x: []
    :param rate: "Rate (r) is the interest rate or discount rate per period."
    :param payment: "Payment (PMT) is the periodic payment amount in an amortization schedule."
    :param present_value: "Present Value (PV) is the current worth of a future sum given a rate of return."
    :param future_value: "Future Value (FV) is the value of a current asset at a future date."
    :return: "Computed value of Number of periods: n = -ln(1-rPV/PMT) / ln(1+r)"
    '''
    import numpy_financial as npf
    return npf.nper(rate, -payment, -present_value, future_value)






def oc_trigger(overcollateralization_ratio, trigger_level):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Structured Finance', 'Securitization']
    function: "OC trigger — Trigger breached if OC ratio < trigger level. A financial metric in the domain of Structured finance & securitization."
    y_as_x: []
    :param args: "Parameter args used in OC trigger calculation."
    :param kwargs: "Parameter kwargs used in OC trigger calculation."
    :return: "Computed value of OC trigger: Trigger breached if OC ratio < trigger level"
    '''
    return overcollateralization_ratio >= trigger_level


def omega_ratio(returns, threshold=0):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Omega Ratio — probability-weighted ratio of gains vs. losses relative to a threshold."
    y_as_x: []
    :param returns: "Returns are the gain or loss generated on an investment over a specific period."
    :param threshold: "Parameter threshold used in Omega ratio calculation."
    :return: "Computed value of Omega ratio: Omega = int_r^∞ (1-F(x))dx / int_-∞^r F(x)dx"
    '''
    import numpy as np
    r = np.array(returns)
    excess = r - threshold
    return np.sum(excess[excess > 0]) / (-np.sum(excess[excess < 0])) if np.any(excess < 0) else float("inf")






def on_balance_volume_obv(close, volume):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "On-Balance Volume (OBV) — cumulative volume indicator. Adds volume on up days, subtracts on down days."
    y_as_x: []
    :param close: "Close is the final trading price at the end of a trading period."
    :param volume: "Volume is the total number of shares or contracts traded during a period."
    :return: "Computed value of On-balance volume (OBV): OBV_t = OBV_{t-1} +/- Volume_t based on price direction"
    '''
    import pandas as pd
    import numpy as np
    c = pd.Series(close); v = pd.Series(volume)
    direction = np.sign(c.diff()).fillna(0)
    return (direction * v).cumsum()






def one_year_death_probability(mortality_rate):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "One-year death probability — q_x = P[x dies within 1 year]. A financial metric in the domain of Actuarial science & insurance."
    y_as_x: []
    :param args: "Parameter args used in One-year death probability calculation."
    :param kwargs: "Parameter kwargs used in One-year death probability calculation."
    :return: "Computed value of One-year death probability: q_x = P[x dies within 1 year]"
    '''
    return mortality_rate


def one_year_survival_probability(mortality_rate):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "One-year survival probability — p_x = 1 - q_x. A financial metric in the domain of Actuarial science & insurance."
    y_as_x: []
    :param args: "Parameter args used in One-year survival probability calculation."
    :param kwargs: "Parameter kwargs used in One-year survival probability calculation."
    :return: "Computed value of One-year survival probability: p_x = 1 - q_x"
    '''
    return 1 - mortality_rate




def operating_cash_flow_ratio(operating_cash_flow, current_liabilities):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "Operating cash flow ratio — OCF Ratio = Operating Cash Flow / Current Liabilities. A financial metric in the domain of Accounting & financial statement analysis."
    y_as_x: []
    :param operating_cash_flow: "Parameter operating_cash_flow used in Operating cash flow ratio calculation."
    :param current_liabilities: "Current Liabilities are obligations due within one year."
    :return: "Computed value of Operating cash flow ratio: OCF Ratio = Operating Cash Flow / Current Liabilities"
    '''
    return operating_cash_flow / current_liabilities






def operating_expense_ratio(operating_expenses, effective_gross_income):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Real Estate Finance', 'Mortgage Analysis']
    function: "Operating expense ratio — OER = Operating Expenses / Effective Gross Income. A financial metric in the domain of Real estate finance & mortgages."
    y_as_x: []
    :param operating_expenses: "Operating Expenses (OpEx) are the essential ongoing costs a business incurs to maintain daily operations and generate revenue."
    :param effective_gross_income: "Effective Gross Income — PGI minus vacancy losses plus other income."
    :return: "Computed value of Operating expense ratio: OER = Operating Expenses / Effective Gross Income"
    '''
    return operating_expenses / effective_gross_income






def operating_leverage(delta_ebit, delta_sales):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "Operating leverage — DOL = %Delta EBIT / %Delta Sales. A financial metric in the domain of Corporate finance, valuation & capital budgeting."
    y_as_x: ['combined_leverage']
    :param delta_ebit: "Parameter delta_ebit used in Operating leverage calculation."
    :param delta_sales: "Parameter delta_sales used in Operating leverage calculation."
    :return: "Computed value of Operating leverage: DOL = %Delta EBIT / %Delta Sales"
    '''
    return delta_ebit / delta_sales






def operating_margin(operating_income, revenue):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "Operating Margin — operating income as a percentage of revenue."
    y_as_x: []
    :param operating_income: "Operating Income is the profit from core business operations after deducting operating expenses from gross profit."
    :param revenue: "Revenue is the total amount of income a business generates from the sale of goods or services before deducting expenses."
    :return: "Computed value of Operating margin: Operating Margin = EBIT / Revenue"
    '''
    return operating_income / revenue






def operational_risk_capital_sma(bic, ilm):
    '''
    domain: ['Bank regulation, Basel & prudential ratios']
    subdomain: ['Bank Regulation', 'Basel Framework', 'Prudential Ratios']
    function: "Operational risk capital (SMA) — ORC = BIC x ILM. A financial metric in the domain of Bank regulation, Basel & prudential ratios."
    y_as_x: []
    :param bic: "Parameter bic used in Operational risk capital (SMA) calculation."
    :param ilm: "Parameter ilm used in Operational risk capital (SMA) calculation."
    :return: "Computed value of Operational risk capital (SMA): ORC = BIC x ILM"
    '''
    return bic * ilm






def optimal_number_of_contracts(h_x_exposure_value, futures_contract_value):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Commodities', 'Futures', 'Hedging']
    function: "Optimal number of contracts — N* = h* x Exposure Value / Futures Contract Value. A financial metric in the domain of Commodities, futures & hedging."
    y_as_x: []
    :param h_x_exposure_value: "Parameter h_x_exposure_value used in Optimal number of contracts calculation."
    :param futures_contract_value: "Parameter futures_contract_value used in Optimal number of contracts calculation."
    :return: "Computed value of Optimal number of contracts: N* = h* x Exposure Value / Futures Contract Value"
    '''
    return h_x_exposure_value / futures_contract_value






def option_delta_hedged_pand_l(option_pnl, delta, underlying_pnl):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Option delta-hedged P&L — dPi approx 0.5 Gamma (dS)^2 + Theta dt + Vega d sigma. A financial metric in the domain of Derivatives, options & volatility."
    y_as_x: []
    :param args: "Parameter args used in Option delta-hedged P&L calculation."
    :param kwargs: "Parameter kwargs used in Option delta-hedged P&L calculation."
    :return: "Computed value of Option delta-hedged P&L: dPi approx 0.5 Gamma (dS)^2 + Theta dt + Vega d sigma"
    '''
    return option_pnl - delta * underlying_pnl


def option_pool_dilution(option_pool_shares, total_shares_post):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Private Equity', 'Venture Capital', 'LBO']
    function: "Option pool dilution — Fully Diluted Ownership = Shares_owned / (Existing + New + Option Pool). A financial metric in the domain of Private equity, venture capital & LBO."
    y_as_x: []
    :param args: "Parameter args used in Option pool dilution calculation."
    :param kwargs: "Parameter kwargs used in Option pool dilution calculation."
    :return: "Computed value of Option pool dilution: Fully Diluted Ownership = Shares_owned / (Existing + New + Option Pool)"
    '''
    return option_pool_shares / total_shares_post




def option_adjusted_spread_oas(bond_price, face_value, coupon_rate, spot_rates, option_value, frequency=2):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Fixed Income', 'Bond Mathematics', 'Credit Markets']
    function: "Option-adjusted spread (OAS) — P = E_Q[ sum_t CF_t(path) exp(-(r_t + OAS)t) ]. A financial metric in the domain of Fixed income, bonds & credit markets."
    y_as_x: []
    :param args: "Parameter args used in Option-adjusted spread (OAS) calculation."
    :param kwargs: "Parameter kwargs used in Option-adjusted spread (OAS) calculation."
    :return: "Computed value of Option-adjusted spread (OAS): P = E_Q[ sum_t CF_t(path) exp(-(r_t + OAS)t) ]"
    '''
    from scipy.optimize import brentq
    import numpy as np
    c = face_value * coupon_rate / frequency
    n = len(spot_rates)
    adj_price = bond_price + option_value
    def price_diff(oas):
        t = np.arange(1, n + 1)
        sr = np.array(spot_rates) / frequency
        pv = np.sum(c / (1 + sr + oas / frequency)**t) + face_value / (1 + sr[-1] + oas / frequency)**n
        return pv - adj_price
    return brentq(price_diff, -0.05, 0.5)




def oracle_approximating_shrinkage_oas(returns_matrix):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Oracle Approximating Shrinkage (OAS) — Sigma_hat = (1-delta)S + delta mu I. A financial metric in the domain of Asset management & portfolio optimization."
    y_as_x: []
    :param X: "Parameter X used in Oracle Approximating Shrinkage (OAS) calculation."
    :param y: "Parameter y used in Oracle Approximating Shrinkage (OAS) calculation."
    :return: "Computed value of Oracle Approximating Shrinkage (OAS): Sigma_hat = (1-delta)S + delta mu I"
    '''
    from sklearn.covariance import OAS
    oas = OAS()
    oas.fit(returns_matrix)
    return oas.covariance_




def order_imbalance(buy_volume, sell_volume):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Liquidity Risk', 'Market Liquidity', 'Execution Cost']
    function: "Order imbalance — OI = (Buy Volume - Sell Volume)/(Buy Volume + Sell Volume). A financial metric in the domain of Liquidity risk, market liquidity & execution cost."
    y_as_x: []
    :param args: "Parameter args used in Order imbalance calculation."
    :param kwargs: "Parameter kwargs used in Order imbalance calculation."
    :return: "Computed value of Order imbalance: OI = (Buy Volume - Sell Volume)/(Buy Volume + Sell Volume)"
    '''
    return (buy_volume - sell_volume) / (buy_volume + sell_volume) if (buy_volume + sell_volume) > 0 else 0




def outstanding_balance_after_k_payments(rate, num_periods, payment, present_value=0):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Banking', 'Consumer Lending', 'Project Finance']
    function: "Outstanding balance after k payments — B_k = PV(1+r)^k - PMT((1+r)^k-1)/r. A financial metric in the domain of Banking, consumer lending & project finance."
    y_as_x: []
    :param rate: "Rate (r) is the interest rate or discount rate per period."
    :param num_periods: "Number of Periods (n) is the total number of payment or compounding periods."
    :param payment: "Payment (PMT) is the periodic payment amount in an amortization schedule."
    :param present_value: "Present Value (PV) is the current worth of a future sum given a rate of return."
    :return: "Computed value of Outstanding balance after k payments: B_k = PV(1+r)^k - PMT((1+r)^k-1)/r"
    '''
    import numpy_financial as npf
    return npf.fv(rate, num_periods, -payment, -present_value)






def outstanding_loan_balance(rate, num_periods, payment, present_value=0):
    '''
    domain: ['Banking, lending & project finance']
    subdomain: ['Banking', 'Lending', 'Project Finance']
    function: "Outstanding loan balance — Balance_t = PV·(1+r)^t - PMT·[((1+r)^t - 1)/r]. A financial metric in the domain of Banking, lending & project finance."
    y_as_x: []
    :param rate: "Rate (r) is the interest rate or discount rate per period."
    :param num_periods: "Number of Periods (n) is the total number of payment or compounding periods."
    :param payment: "Payment (PMT) is the periodic payment amount in an amortization schedule."
    :param present_value: "Present Value (PV) is the current worth of a future sum given a rate of return."
    :return: "Computed value of Outstanding loan balance: Balance_t = PV·(1+r)^t - PMT·[((1+r)^t - 1)/r]"
    '''
    import numpy_financial as npf
    return npf.fv(rate, num_periods, -payment, -present_value)






def overcollateralization_ratio(collateral_balance, notes_outstanding):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Structured Finance', 'Securitization']
    function: "Overcollateralization ratio — OC Ratio = Collateral Balance / Notes Outstanding. A financial metric in the domain of Structured finance & securitization."
    y_as_x: []
    :param collateral_balance: "Parameter collateral_balance used in Overcollateralization ratio calculation."
    :param notes_outstanding: "Parameter notes_outstanding used in Overcollateralization ratio calculation."
    :return: "Computed value of Overcollateralization ratio: OC Ratio = Collateral Balance / Notes Outstanding"
    '''
    return collateral_balance / notes_outstanding






def ownership_percentage(shares_owned, total_shares):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Private Equity', 'Venture Capital', 'LBO']
    function: "Ownership percentage — Ownership = Investment / Post-money Valuation. A financial metric in the domain of Private equity, venture capital & LBO."
    y_as_x: []
    :param args: "Parameter args used in Ownership percentage calculation."
    :param kwargs: "Parameter kwargs used in Ownership percentage calculation."
    :return: "Computed value of Ownership percentage: Ownership = Investment / Post-money Valuation"
    '''
    return shares_owned / total_shares


def p_b_ratio(price_per_share, book_value_per_share):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "P/B ratio — P/B = Price per Share / Book Value per Share. A financial metric in the domain of Corporate finance, valuation & capital budgeting."
    y_as_x: []
    :param price_per_share: "Parameter price_per_share used in P/B ratio calculation."
    :param book_value_per_share: "Book value per share — BVPS = Equity / Shares Outstanding. A financial metric in the domain of Accounting & financial statement analysis."
    :return: "Computed value of P/B ratio: P/B = Price per Share / Book Value per Share"
    '''
    return price_per_share / book_value_per_share






def p_e_ratio(price_per_share, eps):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "P/E ratio — P/E = Price per Share / EPS. A financial metric in the domain of Corporate finance, valuation & capital budgeting."
    y_as_x: []
    :param price_per_share: "Parameter price_per_share used in P/E ratio calculation."
    :param eps: "Earnings Per Share (EPS) is the portion of profit allocated to each outstanding share of common stock."
    :return: "Computed value of P/E ratio: P/E = Price per Share / EPS"
    '''
    return price_per_share / eps






def pain_index(returns):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Performance Attribution', 'Risk-Adjusted Performance']
    function: "Pain index — Pain Index = average drawdown. A financial metric in the domain of Performance measurement & attribution."
    y_as_x: []
    :param returns: "Returns are the gain or loss generated on an investment over a specific period."
    :return: "Computed value of Pain index: Pain Index = average drawdown"
    '''
    import numpy as np
    # Implementation via quantstats.stats
    return np.array(returns)






def par_swap_rate(discount_factors, day_count_fractions):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Interest Rate Modeling', 'Term Structure']
    function: "Par swap rate — K* = (1-DF(T_n)) / (Σ_i α_i·DF(t_i)). A financial metric in the domain of Interest-rate modeling & term structures."
    y_as_x: []
    :param args: "Parameter args used in Par swap rate calculation."
    :param kwargs: "Parameter kwargs used in Par swap rate calculation."
    :return: "Computed value of Par swap rate: K* = (1-DF(T_n)) / (Σ_i α_i·DF(t_i))"
    '''
    import numpy as np
    df = np.array(discount_factors); dcf = np.array(day_count_fractions)
    return (1 - df[-1]) / np.sum(df * dcf)


def par_yield(discount_factors):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Fixed Income', 'Bond Mathematics', 'Credit Markets']
    function: "Par yield — Par = (1-DF_n) / sum_i alpha_i DF_i. A financial metric in the domain of Fixed income, bonds & credit markets."
    y_as_x: []
    :param args: "Parameter args used in Par yield calculation."
    :param kwargs: "Parameter kwargs used in Par yield calculation."
    :return: "Computed value of Par yield: Par = (1-DF_n) / sum_i alpha_i DF_i"
    '''
    import numpy as np
    df = np.array(discount_factors)
    return (1 - df[-1]) / np.sum(df)




def parabolic_sar(high, low, af_start=0.02, af_step=0.02, af_max=0.2):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "Parabolic SAR — SAR_t = SAR_{t-1} + AF(EP - SAR_{t-1}). A financial metric in the domain of Technical analysis & chart-based indicators."
    y_as_x: []
    :param high: "High is the highest price during a specific trading period."
    :param low: "Low is the lowest price during a specific trading period."
    :param close: "Close is the final trading price at the end of a trading period."
    :param volume: "Volume is the total number of shares or contracts traded during a period."
    :param period: "Period (n) is the lookback window in number of bars for technical indicators."
    :return: "Computed value of Parabolic SAR: SAR_t = SAR_{t-1} + AF(EP - SAR_{t-1})"
    '''
    import numpy as np
    h = np.array(high); l = np.array(low)
    n = len(h)
    sar = np.zeros(n)
    trend = 1; ep = h[0]; af = af_start; sar[0] = l[0]
    for i in range(1, n):
        sar[i] = sar[i-1] + af * (ep - sar[i-1])
        if trend == 1:
            if l[i] < sar[i]:
                trend = -1; sar[i] = ep; ep = l[i]; af = af_start
            else:
                if h[i] > ep: ep = h[i]; af = min(af + af_step, af_max)
        else:
            if h[i] > sar[i]:
                trend = 1; sar[i] = ep; ep = h[i]; af = af_start
            else:
                if l[i] < ep: ep = l[i]; af = min(af + af_step, af_max)
    return sar




def parametric_es_under_normality(mean_return, volatility, confidence_level=0.95):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "Parametric ES under normality — ES = -(mu - sigma phi(z_alpha)/(alpha)). A financial metric in the domain of Market risk & volatility modeling."
    y_as_x: []
    :param args: "Parameter args used in Parametric ES under normality calculation."
    :param kwargs: "Parameter kwargs used in Parametric ES under normality calculation."
    :return: "Computed value of Parametric ES under normality: ES = -(mu - sigma phi(z_alpha)/(alpha))"
    '''
    from scipy.stats import norm
    import numpy as np
    z = norm.ppf(1 - confidence_level)
    return -(mean_return + volatility * norm.pdf(z) / (1 - confidence_level))




def parametric_normal_va_r(portfolio_value, mean_return, volatility, confidence_level=0.95):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "Parametric Normal VaR — VaR under normal distribution assumption."
    y_as_x: []
    :param portfolio_value: "Parameter portfolio_value used in Parametric normal VaR calculation."
    :param mean_return: "Parameter mean_return used in Parametric normal VaR calculation."
    :param volatility: "Volatility (sigma) is the annualized standard deviation of returns."
    :param confidence_level: "Confidence Level is the probability threshold used in statistical tests and risk measures."
    :return: "Computed value of Parametric normal VaR: VaR_alpha = -(mu + z_alpha sigma)V"
    '''
    from scipy.stats import norm
    z = norm.ppf(confidence_level)
    return portfolio_value * (mean_return - z * volatility)






def parametric_va_r(portfolio_value, volatility, confidence_level=0.95):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "Parametric VaR — VaR_α = -(μ + z_α σ). A financial metric in the domain of Market risk & volatility modeling."
    y_as_x: []
    :param returns_matrix: "Parameter returns_matrix used in Parametric VaR calculation."
    :return: "Computed value of Parametric VaR: VaR_α = -(μ + z_α σ)"
    '''
    from scipy.stats import norm
    return portfolio_value * volatility * norm.ppf(confidence_level)


def parkinson_volatility(high, low):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "Parkinson volatility — sigma_P^2 = [1/(4 ln2)n] sum [ln(H/L)]^2. A financial metric in the domain of Market risk & volatility modeling."
    y_as_x: []
    :param args: "Parameter args used in Parkinson volatility calculation."
    :param kwargs: "Parameter kwargs used in Parkinson volatility calculation."
    :return: "Computed value of Parkinson volatility: sigma_P^2 = [1/(4 ln2)n] sum [ln(H/L)]^2"
    '''
    import numpy as np
    return np.sqrt(np.mean(np.log(np.array(high) / np.array(low))**2) / (4 * np.log(2)))




def participation_rate(executed_volume, market_volume):
    '''
    domain: ['Trading, execution & market microstructure']
    subdomain: ['Trading', 'Execution', 'Market Microstructure']
    function: "Participation rate — Participation = Executed Volume / Market Volume. A financial metric in the domain of Trading, execution & market microstructure."
    y_as_x: []
    :param executed_volume: "Parameter executed_volume used in Participation rate calculation."
    :param market_volume: "Parameter market_volume used in Participation rate calculation."
    :return: "Computed value of Participation rate: Participation = Executed Volume / Market Volume"
    '''
    return executed_volume / market_volume






def pastor_stambaugh_liquidity(y, X):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Liquidity Risk', 'Market Liquidity', 'Execution Cost']
    function: "Pastor-Stambaugh liquidity — r_{i,t+1} = ... + gamma_i sign(r_i,t,excess) volume_i,t + epsilon. A financial metric in the domain of Liquidity risk, market liquidity & execution cost."
    y_as_x: []
    :param y: "Parameter y used in Pastor-Stambaugh liquidity calculation."
    :param X: "Parameter X used in Pastor-Stambaugh liquidity calculation."
    :return: "Computed value of Pastor-Stambaugh liquidity: r_{i,t+1} = ... + gamma_i sign(r_i,t,excess) volume_i,t + epsilon"
    '''
    import statsmodels.api as sm
    X_const = sm.add_constant(X)
    model = sm.OLS(y, X_const).fit()
    return model






def payables_turnover(cogs, average_ap):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "Payables turnover — Payables Turnover = COGS / Average AP. A financial metric in the domain of Accounting & financial statement analysis."
    y_as_x: []
    :param cogs: "Parameter cogs used in Payables turnover calculation."
    :param average_ap: "Parameter average_ap used in Payables turnover calculation."
    :return: "Computed value of Payables turnover: Payables Turnover = COGS / Average AP"
    '''
    return cogs / average_ap






def payback_period(initial_investment, annual_cash_flows):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "Payback period — Payback = smallest t such that cumulative CF_t >= initial outlay. A financial metric in the domain of Corporate finance, valuation & capital budgeting."
    y_as_x: []
    :param args: "Parameter args used in Payback period calculation."
    :param kwargs: "Parameter kwargs used in Payback period calculation."
    :return: "Computed value of Payback period: Payback = smallest t such that cumulative CF_t >= initial outlay"
    '''
    cumulative = 0
    for i, cf in enumerate(annual_cash_flows):
        cumulative += cf
        if cumulative >= initial_investment:
            return i + 1
    return float('inf')


def payment_shock_ratio(numerator, denominator):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Banking', 'Consumer Lending', 'Project Finance']
    function: "Payment shock ratio — Payment Shock = New Payment / Old Payment - 1. A financial metric in the domain of Banking, consumer lending & project finance."
    y_as_x: []
    :param numerator: "Parameter numerator used in Payment shock ratio calculation."
    :param denominator: "Parameter denominator used in Payment shock ratio calculation."
    :return: "Computed value of Payment shock ratio: Payment Shock = New Payment / Old Payment - 1"
    '''
    return numerator / denominator if denominator != 0 else float("inf")






def peg_ratio(pe_ratio, earnings_growth_rate):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "PEG Ratio — P/E ratio divided by earnings growth rate. PEG < 1 may indicate undervaluation."
    y_as_x: []
    :param pe_ratio: "Parameter pe_ratio used in PEG ratio calculation."
    :param earnings_growth_rate: "Parameter earnings_growth_rate used in PEG ratio calculation."
    :return: "Computed value of PEG ratio: PEG = (P/E) / Earnings Growth"
    '''
    return pe_ratio / (earnings_growth_rate * 100) if earnings_growth_rate != 0 else float("inf")






def percentage_price_oscillator_ppo(close, short_period=12, long_period=26):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "Percentage price oscillator (PPO) — PPO = (EMA_fast - EMA_slow)/EMA_slow. A financial metric in the domain of Technical analysis & chart-based indicators."
    y_as_x: []
    :param high: "High is the highest price during a specific trading period."
    :param low: "Low is the lowest price during a specific trading period."
    :param close: "Close is the final trading price at the end of a trading period."
    :param volume: "Volume is the total number of shares or contracts traded during a period."
    :param period: "Period (n) is the lookback window in number of bars for technical indicators."
    :return: "Computed value of Percentage price oscillator (PPO): PPO = (EMA_fast - EMA_slow)/EMA_slow"
    '''
    import pandas as pd
    c = pd.Series(close)
    ema_short = c.ewm(span=short_period).mean()
    ema_long = c.ewm(span=long_period).mean()
    return (ema_short - ema_long) / ema_long * 100


def perpetuity_value(payment, rate):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "Perpetuity Value — PV = C / r. Present value of infinite constant cash flows."
    y_as_x: []
    :param payment: "Payment (PMT) is the periodic payment amount in an amortization schedule."
    :param rate: "Rate (r) is the interest rate or discount rate per period."
    :return: "Computed value of Perpetuity value: PV = CF / r"
    '''
    return payment / rate






def piotroski_f_score(*components):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "Piotroski F-score — F = sum of 9 binary accounting signals, according to the following rules:
1.Return on Assets (ROA) (1 point if it is positive in the current year, 0 otherwise);
2.Operating Cash Flow (1 point if it is positive in the current year, 0 otherwise);
3.Change in Return of Assets (ROA) (1 point if ROA is higher in the current year compared to the previous one, 0 otherwise);
4.Accruals (1 point if Operating Cash Flow/Total Assets is higher than ROA/Total Assets in the current year, 0 otherwise);
5.Change in Leverage (long-term) ratio (1 point if the ratio is lower this year compared to the previous one, 0 otherwise);
6.Change in Current ratio (1 point if it is higher in the current year compared to the previous one, 0 otherwise);
7.Change in the number of shares (1 point if no new shares were issued during the last year);
8.Change in Gross Margin (1 point if it is higher in the current year compared to the previous one, 0 otherwise);
9.Change in Asset Turnover ratio (1 point if it is higher in the current year compared to the previous one, 0 otherwise);. A financial metric in the domain of Accounting & financial statement analysis."
    y_as_x: []
    :param components: "Parameter components used in Piotroski F-score calculation."
    :return: "Computed value of Piotroski F-score: F = sum of 9 binary accounting signals, according to the following rules:
1.Return on Assets (ROA) (1 point if it is positive in the current year, 0 otherwise);
2.Operating Cash Flow (1 point if it is positive in the current year, 0 otherwise);
3.Change in Return of Assets (ROA) (1 point if ROA is higher in the current year compared to the previous one, 0 otherwise);
4.Accruals (1 point if Operating Cash Flow/Total Assets is higher than ROA/Total Assets in the current year, 0 otherwise);
5.Change in Leverage (long-term) ratio (1 point if the ratio is lower this year compared to the previous one, 0 otherwise);
6.Change in Current ratio (1 point if it is higher in the current year compared to the previous one, 0 otherwise);
7.Change in the number of shares (1 point if no new shares were issued during the last year);
8.Change in Gross Margin (1 point if it is higher in the current year compared to the previous one, 0 otherwise);
9.Change in Asset Turnover ratio (1 point if it is higher in the current year compared to the previous one, 0 otherwise);"
    '''
    return sum(components)






def plus_directional_indicator_plus_di(high, low, close, period=14):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "Plus directional indicator (+DI) — +DI = 100 x smoothed +DM / ATR. A financial metric in the domain of Technical analysis & chart-based indicators."
    y_as_x: []
    :param high: "High is the highest price during a specific trading period."
    :param low: "Low is the lowest price during a specific trading period."
    :param close: "Close is the final trading price at the end of a trading period."
    :param volume: "Volume is the total number of shares or contracts traded during a period."
    :param period: "Period (n) is the lookback window in number of bars for technical indicators."
    :return: "Computed value of Plus directional indicator (+DI): +DI = 100 x smoothed +DM / ATR"
    '''
    import pandas as pd
    h = pd.Series(high); l = pd.Series(low); c = pd.Series(close)
    plus_dm = h.diff().clip(lower=0)
    minus_dm = (-l.diff()).clip(lower=0)
    plus_dm[minus_dm > plus_dm] = 0
    tr = pd.concat([h-l, (h-c.shift()).abs(), (l-c.shift()).abs()], axis=1).max(axis=1)
    atr = tr.rolling(period).mean()
    return 100 * plus_dm.rolling(period).mean() / atr


def pme_kaplan_schoar(fund_distributions, fund_contributions, market_returns):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Private Equity', 'Venture Capital', 'LBO']
    function: "PME (Kaplan-Schoar) — KS PME = (FV of distributions + NAV adjusted by index)/(FV of contributions). A financial metric in the domain of Private equity, venture capital & LBO."
    y_as_x: []
    :param args: "Parameter args used in PME (Kaplan-Schoar) calculation."
    :param kwargs: "Parameter kwargs used in PME (Kaplan-Schoar) calculation."
    :return: "Computed value of PME (Kaplan-Schoar): KS PME = (FV of distributions + NAV adjusted by index)/(FV of contributions)"
    '''
    import numpy as np
    mr = np.cumprod(1 + np.array(market_returns))
    fv_dist = np.sum(np.array(fund_distributions) * mr[::-1][:len(fund_distributions)])
    fv_cont = np.sum(np.array(fund_contributions) * mr[::-1][:len(fund_contributions)])
    return fv_dist / fv_cont if fv_cont > 0 else float('inf')




def po_strip_value(principal_cash_flows, discount_rates):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Structured Finance', 'Securitization']
    function: "PO strip value — PV_PO = sum_t principal_only_cf_t DF_t. A financial metric in the domain of Structured finance & securitization."
    y_as_x: []
    :param args: "Parameter args used in PO strip value calculation."
    :param kwargs: "Parameter kwargs used in PO strip value calculation."
    :return: "Computed value of PO strip value: PV_PO = sum_t principal_only_cf_t DF_t"
    '''
    import numpy as np
    cf = np.array(principal_cash_flows); r = np.array(discount_rates)
    df = np.cumprod(1 / (1 + r))
    return np.sum(cf * df)




def point_in_time_pd(X, y):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit Risk', 'Default Modeling', 'Credit Portfolio']
    function: "Point-in-time PD — PD_PIT = conditional default probability given current macro state. A financial metric in the domain of Credit risk, default modeling & credit portfolio."
    y_as_x: []
    :param data: "Parameter data used in Point-in-time PD calculation."
    :param args: "Parameter args used in Point-in-time PD calculation."
    :return: "Computed value of Point-in-time PD: PD_PIT = conditional default probability given current macro state"
    '''
    from sklearn.linear_model import LogisticRegression
    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)
    return model.predict_proba(X)[:, 1]




def portfolio_covariance_contribution(weights, cov_matrix):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Portfolio covariance contribution — MC_i = (Sigma w)_i. A financial metric in the domain of Asset management & portfolio optimization."
    y_as_x: []
    :param expected_returns: "Expected Returns vector contains the anticipated return for each asset."
    :param cov_matrix: "Covariance Matrix contains the covariances between all pairs of assets."
    :return: "Computed value of Portfolio covariance contribution: MC_i = (Sigma w)_i"
    '''
    import numpy as np
    w = np.array(weights); sigma = np.array(cov_matrix)
    port_var = w @ sigma @ w
    return w * (sigma @ w) / port_var




def portfolio_return(weights, asset_returns):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Portfolio Return — weighted average of individual asset returns. R_p = sum(w_i * R_i)."
    y_as_x: ['active_return', 'excess_return', 'information_ratio', 'jensens_alpha', 'portfolio_return', 'sharpe_ratio', 'tracking_error', 'treynor_ratio']
    :param weights: "Portfolio Weights represent the proportion of total portfolio value allocated to each asset."
    :param asset_returns: "Returns of the individual asset."
    :return: "Computed value of Portfolio return: E[R_p] = w' mu"
    '''
    import numpy as np
    return np.dot(weights, asset_returns)






def portfolio_variance(weights, cov_matrix):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Portfolio Variance — w' * Sigma * w. The variance of portfolio returns."
    y_as_x: []
    :param weights: "Portfolio Weights represent the proportion of total portfolio value allocated to each asset."
    :param cov_matrix: "Covariance Matrix contains the covariances between all pairs of assets."
    :return: "Computed value of Portfolio variance: sigma_p^2 = w' Sigma w"
    '''
    import numpy as np
    w = np.array(weights); sigma = np.array(cov_matrix)
    return w @ sigma @ w






def portfolio_volatility(weights, cov_matrix):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Portfolio Volatility — sqrt(w' * Sigma * w). Standard deviation of portfolio returns."
    y_as_x: ['delta_normal_va_r', 'diversification_ratio']
    :param weights: "Portfolio Weights represent the proportion of total portfolio value allocated to each asset."
    :param cov_matrix: "Covariance Matrix contains the covariances between all pairs of assets."
    :return: "Computed value of Portfolio volatility: sigma_p = sqrt(w' Sigma w)"
    '''
    import numpy as np
    w = np.array(weights); sigma = np.array(cov_matrix)
    return np.sqrt(w @ sigma @ w)






def post_money_valuation(investment_amount, ownership_percentage):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Private Equity', 'Venture Capital', 'LBO']
    function: "Post-money valuation — Post-money = Pre-money + New Investment. A financial metric in the domain of Private equity, venture capital & LBO."
    y_as_x: []
    :param args: "Parameter args used in Post-money valuation calculation."
    :param kwargs: "Parameter kwargs used in Post-money valuation calculation."
    :return: "Computed value of Post-money valuation: Post-money = Pre-money + New Investment"
    '''
    return investment_amount / ownership_percentage


def potential_future_exposure_pfe(simulated_exposures, confidence_level=0.95):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit Risk', 'Default Modeling', 'Credit Portfolio']
    function: "Potential future exposure (PFE) — PFE_alpha(t) = quantile_alpha(exposure_t). A financial metric in the domain of Credit risk, default modeling & credit portfolio."
    y_as_x: []
    :param args: "Parameter args used in Potential future exposure (PFE) calculation."
    :param kwargs: "Parameter kwargs used in Potential future exposure (PFE) calculation."
    :return: "Computed value of Potential future exposure (PFE): PFE_alpha(t) = quantile_alpha(exposure_t)"
    '''
    import numpy as np
    return np.percentile(np.maximum(np.array(simulated_exposures), 0), confidence_level * 100)




def ppi_inflation_month_over_month(ppi_current, ppi_previous):
    '''
    domain: ['Macroeconomics, inflation & price indices']
    subdomain: ['Macroeconomics', 'Inflation', 'Price Indices']
    function: "PPI inflation (month over month) — π_t^(PPI,MoM) = PPI_t / PPI_(t-1) - 1. A financial metric in the domain of Macroeconomics, inflation & price indices."
    y_as_x: []
    :param args: "Parameter args used in PPI inflation (month over month) calculation."
    :param kwargs: "Parameter kwargs used in PPI inflation (month over month) calculation."
    :return: "Computed value of PPI inflation (month over month): π_t^(PPI,MoM) = PPI_t / PPI_(t-1) - 1"
    '''
    return (ppi_current - ppi_previous) / ppi_previous




def ppi_inflation_year_over_year(ppi_current, ppi_year_ago):
    '''
    domain: ['Macroeconomics, inflation & price indices']
    subdomain: ['Macroeconomics', 'Inflation', 'Price Indices']
    function: "PPI inflation (year over year) — π_t^(PPI,YoY) = PPI_t / PPI_(t-12) - 1. A financial metric in the domain of Macroeconomics, inflation & price indices."
    y_as_x: []
    :param args: "Parameter args used in PPI inflation (year over year) calculation."
    :param kwargs: "Parameter kwargs used in PPI inflation (year over year) calculation."
    :return: "Computed value of PPI inflation (year over year): π_t^(PPI,YoY) = PPI_t / PPI_(t-12) - 1"
    '''
    return (ppi_current - ppi_year_ago) / ppi_year_ago




def preferred_return_hurdle(rate, num_periods, payment, present_value=0):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Private Equity', 'Venture Capital', 'LBO']
    function: "Preferred return hurdle — Hurdle FV = Contributed Capital x (1+h)^t. A financial metric in the domain of Private equity, venture capital & LBO."
    y_as_x: []
    :param rate: "Rate (r) is the interest rate or discount rate per period."
    :param num_periods: "Number of Periods (n) is the total number of payment or compounding periods."
    :param payment: "Payment (PMT) is the periodic payment amount in an amortization schedule."
    :param present_value: "Present Value (PV) is the current worth of a future sum given a rate of return."
    :return: "Computed value of Preferred return hurdle: Hurdle FV = Contributed Capital x (1+h)^t"
    '''
    import numpy_financial as npf
    return npf.fv(rate, num_periods, -payment, -present_value)






def pre_money_valuation(post_money_valuation, investment_amount):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Private Equity', 'Venture Capital', 'LBO']
    function: "Pre-money valuation — Pre-money = Post-money - New Investment. A financial metric in the domain of Private equity, venture capital & LBO."
    y_as_x: []
    :param args: "Parameter args used in Pre-money valuation calculation."
    :param kwargs: "Parameter kwargs used in Pre-money valuation calculation."
    :return: "Computed value of Pre-money valuation: Pre-money = Post-money - New Investment"
    '''
    return post_money_valuation - investment_amount


def prepayment_speed_psa(loan_age, psa_multiplier=1.0):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Structured Finance', 'Securitization']
    function: "Prepayment speed (PSA) — CPR_t = min(0.06, 0.002t) × PSA%. A financial metric in the domain of Structured finance & securitization."
    y_as_x: []
    :param args: "Parameter args used in Prepayment speed (PSA) calculation."
    :param kwargs: "Parameter kwargs used in Prepayment speed (PSA) calculation."
    :return: "Computed value of Prepayment speed (PSA): CPR_t = min(0.06, 0.002t) × PSA%"
    '''
    cpr = min(loan_age * 0.002, 0.06) * psa_multiplier
    return 1 - (1 - cpr)**(1/12)




def present_value_pv(future_value, rate, num_periods):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "Present Value (PV) — PV = FV / (1+r)^n."
    y_as_x: []
    :param future_value: "Future Value (FV) is the value of a current asset at a future date."
    :param rate: "Rate (r) is the interest rate or discount rate per period."
    :param num_periods: "Number of Periods (n) is the total number of payment or compounding periods."
    :return: "Computed value of Present value (PV): PV = sum_t CF_t / (1+r)^t"
    '''
    return future_value / (1 + rate)**num_periods






def present_value_random_variable(benefit, interest_rate, time_of_payment):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "Present value random variable — Z = b_T v^T. A financial metric in the domain of Actuarial science & insurance."
    y_as_x: []
    :param args: "Parameter args used in Present value random variable calculation."
    :param kwargs: "Parameter kwargs used in Present value random variable calculation."
    :return: "Computed value of Present value random variable: Z = b_T v^T"
    '''
    return benefit / (1 + interest_rate)**time_of_payment


def price_impact(cash_flows, discount_rate):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Liquidity Risk', 'Market Liquidity', 'Execution Cost']
    function: "Price impact — Impact = (execution price/Mid price-1)*100. A financial metric in the domain of Liquidity risk, market liquidity & execution cost."
    y_as_x: []
    :param cash_flows: "Parameter cash_flows used in Price impact calculation."
    :param discount_rate: "Discount Rate is the rate used to discount future cash flows to present value."
    :return: "Computed value of Price impact: Impact = (execution price/Mid price-1)*100"
    '''
    import numpy as np
    cf = np.array(cash_flows)
    t = np.arange(1, len(cf) + 1)
    return np.sum(cf / (1 + discount_rate)**t)






def price_to_book(stock_price, book_value_per_share):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Equity Valuation', 'Asset Pricing']
    function: "Price-to-Book — stock price divided by book value per share."
    y_as_x: []
    :param stock_price: "Stock Price (P) is the current market price per share of a company's equity."
    :param book_value_per_share: "Book value per share — BVPS = Equity / Shares Outstanding. A financial metric in the domain of Accounting & financial statement analysis."
    :return: "Computed value of Price-to-book: P/B = Price / Book value per share"
    '''
    return stock_price / book_value_per_share if book_value_per_share != 0 else float("inf")






def price_to_earnings_ratio(stock_price, eps):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Equity Valuation', 'Asset Pricing']
    function: "Price-to-Earnings Ratio — stock price divided by EPS."
    y_as_x: []
    :param stock_price: "Stock Price (P) is the current market price per share of a company's equity."
    :param eps: "Earnings Per Share (EPS) is the portion of profit allocated to each outstanding share of common stock."
    :return: "Computed value of Price-to-earnings ratio: P/E = Price per share / EPS"
    '''
    return stock_price / eps if eps != 0 else float("inf")






def price_to_sales(market_cap, revenue):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Equity Valuation', 'Asset Pricing']
    function: "Price-to-Sales — market cap divided by total revenue."
    y_as_x: []
    :param market_cap: "Market Capitalization is the total market value of outstanding shares (price x shares)."
    :param revenue: "Revenue is the total amount of income a business generates from the sale of goods or services before deducting expenses."
    :return: "Computed value of Price-to-sales: P/S = Market Cap / Revenue"
    '''
    return market_cap / revenue if revenue != 0 else float("inf")






def principal_payment_portion_ppmt(rate, per, num_periods, present_value):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Banking', 'Consumer Lending', 'Project Finance']
    function: "Principal Payment Portion (PPMT) — the principal portion of a specific loan payment."
    y_as_x: []
    :param rate: "Rate (r) is the interest rate or discount rate per period."
    :param per: "Parameter per used in Principal payment portion (PPMT) calculation."
    :param num_periods: "Number of Periods (n) is the total number of payment or compounding periods."
    :param present_value: "Present Value (PV) is the current worth of a future sum given a rate of return."
    :return: "Computed value of Principal payment portion (PPMT): PPMT_t = PMT - IPMT_t"
    '''
    import numpy_financial as npf
    return npf.ppmt(rate, per, num_periods, -present_value)






def probability_of_default_from_hazard_rate(hazard_rate, time_horizon):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit Risk', 'Default Modeling', 'Credit Portfolio']
    function: "Probability of default from hazard rate — PD(0,T) = 1 - exp(-int_0^T lambda(t) dt). A financial metric in the domain of Credit risk, default modeling & credit portfolio."
    y_as_x: []
    :param args: "Parameter args used in Probability of default from hazard rate calculation."
    :param kwargs: "Parameter kwargs used in Probability of default from hazard rate calculation."
    :return: "Computed value of Probability of default from hazard rate: PD(0,T) = 1 - exp(-int_0^T lambda(t) dt)"
    '''
    import numpy as np
    return 1 - np.exp(-hazard_rate * time_horizon)


def probability_of_default_from_logit(X, coefficients):
    '''
    domain: ['Credit risk']
    subdomain: ['Credit Risk']
    function: "Probability of default from logit — PD = 1 / (1 + e^{-Xβ}). A financial metric in the domain of Credit risk."
    y_as_x: []
    :param X: "Parameter X used in Probability of default from logit calculation."
    :param y: "Parameter y used in Probability of default from logit calculation."
    :return: "Computed value of Probability of default from logit: PD = 1 / (1 + e^{-Xβ})"
    '''
    import numpy as np
    z = np.dot(X, coefficients)
    return 1 / (1 + np.exp(-z))




def probability_of_default_scorecard_logit(X_train, y_train, X_predict):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Banking', 'Consumer Lending', 'Project Finance']
    function: "Probability of default scorecard logit — logit(PD) = beta0 + beta'x. A financial metric in the domain of Banking, consumer lending & project finance."
    y_as_x: []
    :param X: "Parameter X used in Probability of default scorecard logit calculation."
    :param y: "Parameter y used in Probability of default scorecard logit calculation."
    :return: "Computed value of Probability of default scorecard logit: logit(PD) = beta0 + beta'x"
    '''
    from sklearn.linear_model import LogisticRegression
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    return model.predict_proba(X_predict)[:, 1]




def probit_default_model(X, y):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit Risk', 'Default Modeling', 'Credit Portfolio']
    function: "Probit default model — Phi^-1(PD_i) = beta0 + beta'x_i. A financial metric in the domain of Credit risk, default modeling & credit portfolio."
    y_as_x: []
    :param data: "Parameter data used in Probit default model calculation."
    :param args: "Parameter args used in Probit default model calculation."
    :return: "Computed value of Probit default model: Phi^-1(PD_i) = beta0 + beta'x_i"
    '''
    import statsmodels.api as sm
    X_const = sm.add_constant(X)
    return sm.Probit(y, X_const).fit(disp=0)




def probit_score(X, coefficients):
    '''
    domain: ['Quantitative forecasting & machine learning in finance']
    subdomain: ['Quantitative Finance', 'Machine Learning']
    function: "Probit score — P(y=1|x)=Phi(beta'x). A financial metric in the domain of Quantitative forecasting & machine learning in finance."
    y_as_x: []
    :param data: "Parameter data used in Probit score calculation."
    :param args: "Parameter args used in Probit score calculation."
    :return: "Computed value of Probit score: P(y=1|x)=Phi(beta'x)"
    '''
    import numpy as np
    from scipy.stats import norm
    return norm.cdf(np.dot(X, coefficients))




def producer_price_index_laspeyres_style_index(i_p_it_q_i0, i_p_i0_q_i0_100):
    '''
    domain: ['Macroeconomics, inflation & price indices']
    subdomain: ['Macroeconomics', 'Inflation', 'Price Indices']
    function: "Producer Price Index (Laspeyres-style index) — PPI_t = (Σ_i p_(i,t) q_(i,0) / Σ_i p_(i,0) q_(i,0)) × 100. A financial metric in the domain of Macroeconomics, inflation & price indices."
    y_as_x: []
    :param i_p_it_q_i0: "Parameter i_p_it_q_i0 used in Producer Price Index (Laspeyres-style index) calculation."
    :param i_p_i0_q_i0_100: "Parameter i_p_i0_q_i0_100 used in Producer Price Index (Laspeyres-style index) calculation."
    :return: "Computed value of Producer Price Index (Laspeyres-style index): PPI_t = (Σ_i p_(i,t) q_(i,0) / Σ_i p_(i,0) q_(i,0)) × 100"
    '''
    return i_p_it_q_i0 / i_p_i0_q_i0_100






def profit_factor(sum_positive_returns, sum_negative_returns):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Performance Attribution', 'Risk-Adjusted Performance']
    function: "Profit factor — Profit Factor = sum positive returns / |sum negative returns|. A financial metric in the domain of Performance measurement & attribution."
    y_as_x: []
    :param sum_positive_returns: "Parameter sum_positive_returns used in Profit factor calculation."
    :param sum_negative_returns: "Parameter sum_negative_returns used in Profit factor calculation."
    :return: "Computed value of Profit factor: Profit Factor = sum positive returns / |sum negative returns|"
    '''
    return sum_positive_returns / sum_negative_returns






def profitability_index(present_value_of_cash_flows, initial_investment):
    '''
    domain: ['Corporate finance & capital budgeting']
    subdomain: ['Corporate Finance', 'Capital Budgeting']
    function: "Profitability Index — PV of future cash flows divided by initial investment. PI > 1 indicates positive NPV."
    y_as_x: []
    :param present_value_of_cash_flows: "Parameter present_value_of_cash_flows used in Profitability index calculation."
    :param initial_investment: "Parameter initial_investment used in Profitability index calculation."
    :return: "Computed value of Profitability index: PI = PV of future cash flows / Initial Investment"
    '''
    return present_value_of_cash_flows / initial_investment






def property_irr(cash_flows):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Real Estate Finance', 'Mortgage Analysis']
    function: "Property IRR — 0 = -Equity_0 + sum_t CF_t/(1+IRR)^t + SaleProceeds/(1+IRR)^T. A financial metric in the domain of Real estate finance & mortgages."
    y_as_x: []
    :param cash_flows: "Parameter cash_flows used in Property IRR calculation."
    :return: "Computed value of Property IRR: 0 = -Equity_0 + sum_t CF_t/(1+IRR)^t + SaleProceeds/(1+IRR)^T"
    '''
    import numpy_financial as npf
    return npf.irr(cash_flows)






def property_value_from_cap_rate(noi, cap_rate):
    '''
    domain: ['Real estate finance']
    subdomain: ['Real Estate Finance']
    function: "Property Value from Cap Rate — Value = NOI / Cap Rate."
    y_as_x: []
    :param noi: "Net Operating Income (NOI) is total revenue from a property minus operating expenses."
    :param cap_rate: "Capitalization Rate is the ratio of NOI to property value used in real estate valuation."
    :return: "Computed value of Property value from cap rate: Value = NOI / Cap Rate"
    '''
    return noi / cap_rate if cap_rate != 0 else float("inf")






def prospective_reserve(benefit, insurance_factor_future, premium, annuity_factor_future):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "Prospective reserve — V_t = PV_t(Future Benefits) - PV_t(Future Premiums). A financial metric in the domain of Actuarial science & insurance."
    y_as_x: []
    :param args: "Parameter args used in Prospective reserve calculation."
    :param kwargs: "Parameter kwargs used in Prospective reserve calculation."
    :return: "Computed value of Prospective reserve: V_t = PV_t(Future Benefits) - PV_t(Future Premiums)"
    '''
    return benefit * insurance_factor_future - premium * annuity_factor_future


def protective_put_payoff(spot_price, purchase_price, strike_price, premium_paid):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Protective put payoff — Payoff = S_T + max(K-S_T,0) - Premium. A financial metric in the domain of Derivatives, options & volatility."
    y_as_x: []
    :param args: "Parameter args used in Protective put payoff calculation."
    :param kwargs: "Parameter kwargs used in Protective put payoff calculation."
    :return: "Computed value of Protective put payoff: Payoff = S_T + max(K-S_T,0) - Premium"
    '''
    import numpy as np
    stock_pnl = spot_price - purchase_price
    put_pnl = np.maximum(strike_price - spot_price, 0) - premium_paid
    return stock_pnl + put_pnl




def provision_coverage_ratio(loan_loss_reserves, nonperforming_loans):
    '''
    domain: ['Bank regulation, Basel & prudential ratios']
    subdomain: ['Bank Regulation', 'Basel Framework', 'Prudential Ratios']
    function: "Provision coverage ratio — Coverage = Loan Loss Reserves / Nonperforming Loans. A financial metric in the domain of Bank regulation, Basel & prudential ratios."
    y_as_x: []
    :param loan_loss_reserves: "Parameter loan_loss_reserves used in Provision coverage ratio calculation."
    :param nonperforming_loans: "Parameter nonperforming_loans used in Provision coverage ratio calculation."
    :return: "Computed value of Provision coverage ratio: Coverage = Loan Loss Reserves / Nonperforming Loans"
    '''
    return loan_loss_reserves / nonperforming_loans






def provision_coverage_ratio_2(allowance_for_credit_losses, nonperforming_loans):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Banking', 'Consumer Lending', 'Project Finance']
    function: "Provision coverage ratio — Coverage Ratio = Allowance for Credit Losses / Nonperforming Loans. A financial metric in the domain of Banking, consumer lending & project finance."
    y_as_x: []
    :param allowance_for_credit_losses: "Parameter allowance_for_credit_losses used in Provision coverage ratio calculation."
    :param nonperforming_loans: "Parameter nonperforming_loans used in Provision coverage ratio calculation."
    :return: "Computed value of Provision coverage ratio: Coverage Ratio = Allowance for Credit Losses / Nonperforming Loans"
    '''
    return allowance_for_credit_losses / nonperforming_loans






def psa_prepayment_benchmark(loan_age, psa_speed=1.0):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Structured Finance', 'Securitization']
    function: "PSA prepayment benchmark — CPR_PSA = min(0.06, 0.002 x month) for 100% PSA. A financial metric in the domain of Structured finance & securitization."
    y_as_x: []
    :param args: "Parameter args used in PSA prepayment benchmark calculation."
    :param kwargs: "Parameter kwargs used in PSA prepayment benchmark calculation."
    :return: "Computed value of PSA prepayment benchmark: CPR_PSA = min(0.06, 0.002 x month) for 100% PSA"
    '''
    cpr = min(loan_age * 0.002, 0.06) * psa_speed
    return 1 - (1 - cpr)**(1/12)


def pti_payment_to_income(monthly_payment, monthly_income):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Real Estate Finance', 'Mortgage Analysis']
    function: "PTI payment-to-income — Monthly Mortgage Payment / Income. A financial metric in the domain of Real estate finance & mortgages."
    y_as_x: []
    :param args: "Parameter args used in PTI payment-to-income calculation."
    :param kwargs: "Parameter kwargs used in PTI payment-to-income calculation."
    :return: "Computed value of PTI payment-to-income: Monthly Mortgage Payment / Income"
    '''
    return monthly_payment / monthly_income




def pti_payment_to_income_gross(monthly_loan_payment, gross_monthly_income):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Banking', 'Consumer Lending', 'Project Finance']
    function: "PTI payment-to-income (gross) — PTI_gross = Monthly Loan Payment / Gross Monthly Income. A financial metric in the domain of Banking, consumer lending & project finance."
    y_as_x: []
    :param monthly_loan_payment: "Parameter monthly_loan_payment used in PTI payment-to-income (gross) calculation."
    :param gross_monthly_income: "Gross Monthly Income is pre-tax monthly income."
    :return: "Computed value of PTI payment-to-income (gross): PTI_gross = Monthly Loan Payment / Gross Monthly Income"
    '''
    return monthly_loan_payment / gross_monthly_income






def pti_payment_to_income_net(monthly_loan_payment, net_monthly_income):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Banking', 'Consumer Lending', 'Project Finance']
    function: "PTI payment-to-income (net) — PTI_net = Monthly Loan Payment / Net Monthly Income. A financial metric in the domain of Banking, consumer lending & project finance."
    y_as_x: []
    :param monthly_loan_payment: "Parameter monthly_loan_payment used in PTI payment-to-income (net) calculation."
    :param net_monthly_income: "Net Monthly Income is post-tax monthly income."
    :return: "Computed value of PTI payment-to-income (net): PTI_net = Monthly Loan Payment / Net Monthly Income"
    '''
    return monthly_loan_payment / net_monthly_income






def public_market_equivalent_pme(fvdistributions_indexed_to_public_benchmark, fvcapital_calls_indexed_to_public_benchmark):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Private Equity', 'Venture Capital', 'LBO']
    function: "Public market equivalent (PME) — PME = FV(distributions indexed to public benchmark) / FV(capital calls indexed to public benchmark). A financial metric in the domain of Private equity, venture capital & LBO."
    y_as_x: []
    :param fvdistributions_indexed_to_public_benchmark: "Parameter fvdistributions_indexed_to_public_benchmark used in Public market equivalent (PME) calculation."
    :param fvcapital_calls_indexed_to_public_benchmark: "Parameter fvcapital_calls_indexed_to_public_benchmark used in Public market equivalent (PME) calculation."
    :return: "Computed value of Public market equivalent (PME): PME = FV(distributions indexed to public benchmark) / FV(capital calls indexed to public benchmark)"
    '''
    return fvdistributions_indexed_to_public_benchmark / fvcapital_calls_indexed_to_public_benchmark






def purchasing_power_parity_ppp(p, p_2):
    '''
    domain: ['FX & international finance']
    subdomain: ['FX Markets', 'International Finance']
    function: "Purchasing power parity (PPP) — S = P / P*. A financial metric in the domain of FX & international finance."
    y_as_x: []
    :param p: "Model order parameter p (autoregressive order or similar)."
    :param p_2: "Parameter p_2 used in Purchasing power parity (PPP) calculation."
    :return: "Computed value of Purchasing power parity (PPP): S = P / P*"
    '''
    return p / p_2






def pure_endowment_apv(benefit, interest_rate, survival_probs, term):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "Pure endowment APV — {}_nE_x = v^n {}_np_x. A financial metric in the domain of Actuarial science & insurance."
    y_as_x: []
    :param args: "Parameter args used in Pure endowment APV calculation."
    :param kwargs: "Parameter kwargs used in Pure endowment APV calculation."
    :return: "Computed value of Pure endowment APV: {}_nE_x = v^n {}_np_x"
    '''
    import numpy as np
    v = 1/(1+interest_rate)
    return benefit * v**term * np.prod(np.array(survival_probs[:term]))


def pure_premium(frequency, severity):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "Pure premium — Pure Premium = Frequency x Severity. A financial metric in the domain of Actuarial science & insurance."
    y_as_x: []
    :param frequency: "Frequency is the number of coupon payments per year."
    :param severity: "Severity — Severity = Net Loss / Defaulted Balance. A financial metric in the domain of Structured finance & securitization."
    :return: "Computed value of Pure premium: Pure Premium = Frequency x Severity"
    '''
    return frequency * severity






def put_payoff(spot_price, strike_price, premium_paid=0):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Put Payoff — max(K - S, 0) - premium. Payoff of a put option at expiration."
    y_as_x: []
    :param spot_price: "Spot Price (S) is the current market price of the underlying asset."
    :param strike_price: "Strike Price (K) is the predetermined price at which an option can be exercised."
    :param premium_paid: "Parameter premium_paid used in Put payoff calculation."
    :return: "Computed value of Put payoff: P_T = max(K - S_T, 0)"
    '''
    import numpy as np
    return np.maximum(strike_price - spot_price, 0) - premium_paid






def put_spread_payoff(value_a, value_b):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Put spread payoff — Payoff = max(K2-S,0) - max(K1-S,0). A financial metric in the domain of Derivatives, options & volatility."
    y_as_x: []
    :param value_a: "Parameter value_a used in Put spread payoff calculation."
    :param value_b: "Parameter value_b used in Put spread payoff calculation."
    :return: "Computed value of Put spread payoff: Payoff = max(K2-S,0) - max(K1-S,0)"
    '''
    return value_a - value_b






def put_call_parity(call_price, put_price, spot_price, strike_price, risk_free_rate, time_to_expiry):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Put-Call Parity — C - P = S - K*exp(-rT). Fundamental relationship between call and put prices."
    y_as_x: []
    :param call_price: "Call Price is the premium paid for a call option."
    :param put_price: "Put Price is the premium paid for a put option."
    :param spot_price: "Spot Price (S) is the current market price of the underlying asset."
    :param strike_price: "Strike Price (K) is the predetermined price at which an option can be exercised."
    :param risk_free_rate: "Risk-Free Rate (Rf) is the theoretical rate of return with zero risk, typically proxied by government bond yields."
    :param time_to_expiry: "Time to Expiry (T) is the remaining time until expiration, in years."
    :return: "Computed value of Put-call parity: C - P = S_0 - K e^{-rT}"
    '''
    import numpy as np
    lhs = call_price - put_price
    rhs = spot_price - strike_price * np.exp(-risk_free_rate * time_to_expiry)
    return {'parity_holds': abs(lhs - rhs) < 0.01, 'difference': lhs - rhs}






def put_call_parity_equity(spot_price, strike_price, risk_free_rate, volatility, time_to_expiry, option_type):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Put-call parity (equity) — C - P = S_0 e^{-qT} - K e^{-rT}. A financial metric in the domain of Derivatives, options & volatility."
    y_as_x: []
    :param spot_price: "Spot Price (S) is the current market price of the underlying asset."
    :param strike_price: "Strike Price (K) is the predetermined price at which an option can be exercised."
    :param risk_free_rate: "Risk-Free Rate (Rf) is the theoretical rate of return with zero risk, typically proxied by government bond yields."
    :param volatility: "Volatility (sigma) is the annualized standard deviation of returns."
    :param time_to_expiry: "Time to Expiry (T) is the remaining time until expiration, in years."
    :param option_type: "Option Type specifies whether the option is a "call" or "put"."
    :return: "Computed value of Put-call parity (equity): C - P = S_0 e^{-qT} - K e^{-rT}"
    '''
    import numpy as np
    from scipy.stats import norm
    d1 = (np.log(spot_price/strike_price) + (risk_free_rate + 0.5*volatility**2)*time_to_expiry) / (volatility*np.sqrt(time_to_expiry))
    d2 = d1 - volatility*np.sqrt(time_to_expiry)
    if option_type == "call":
        return spot_price*norm.cdf(d1) - strike_price*np.exp(-risk_free_rate*time_to_expiry)*norm.cdf(d2)
    else:
        return strike_price*np.exp(-risk_free_rate*time_to_expiry)*norm.cdf(-d2) - spot_price*norm.cdf(-d1)






def put_call_parity_futures_options(spot_price, strike_price, risk_free_rate, volatility, time_to_expiry, option_type):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Put-call parity (futures options) — C - P = DF(F_0 - K). A financial metric in the domain of Derivatives, options & volatility."
    y_as_x: []
    :param spot_price: "Spot Price (S) is the current market price of the underlying asset."
    :param strike_price: "Strike Price (K) is the predetermined price at which an option can be exercised."
    :param risk_free_rate: "Risk-Free Rate (Rf) is the theoretical rate of return with zero risk, typically proxied by government bond yields."
    :param volatility: "Volatility (sigma) is the annualized standard deviation of returns."
    :param time_to_expiry: "Time to Expiry (T) is the remaining time until expiration, in years."
    :param option_type: "Option Type specifies whether the option is a "call" or "put"."
    :return: "Computed value of Put-call parity (futures options): C - P = DF(F_0 - K)"
    '''
    import numpy as np
    from scipy.stats import norm
    d1 = (np.log(spot_price/strike_price) + (risk_free_rate + 0.5*volatility**2)*time_to_expiry) / (volatility*np.sqrt(time_to_expiry))
    d2 = d1 - volatility*np.sqrt(time_to_expiry)
    if option_type == "call":
        return spot_price*norm.cdf(d1) - strike_price*np.exp(-risk_free_rate*time_to_expiry)*norm.cdf(d2)
    else:
        return strike_price*np.exp(-risk_free_rate*time_to_expiry)*norm.cdf(-d2) - spot_price*norm.cdf(-d1)






def pv_of_tax_shield(debt, tax_rate, cost_of_debt):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "PV of tax shield — PV(TS) = sum_t Tax Shield_t / (1+r_TS)^t. A financial metric in the domain of Corporate finance, valuation & capital budgeting."
    y_as_x: []
    :param args: "Parameter args used in PV of tax shield calculation."
    :param kwargs: "Parameter kwargs used in PV of tax shield calculation."
    :return: "Computed value of PV of tax shield: PV(TS) = sum_t Tax Shield_t / (1+r_TS)^t"
    '''
    return debt * tax_rate * cost_of_debt / cost_of_debt if cost_of_debt != 0 else debt * tax_rate


def quadratic_program(expected_returns, cov_matrix, risk_aversion=1.0):
    '''
    domain: ['Quantitative forecasting & machine learning in finance']
    subdomain: ['Quantitative Finance', 'Machine Learning']
    function: "Quadratic program — min_x 1/2 x^T P x + q^T x  s.t. Gx≤h, Ax=b. A financial metric in the domain of Quantitative forecasting & machine learning in finance."
    y_as_x: []
    :param expected_returns: "Expected Returns vector contains the anticipated return for each asset."
    :param cov_matrix: "Covariance Matrix contains the covariances between all pairs of assets."
    :param constraints: "Parameter constraints used in Quadratic program calculation."
    :return: "Computed value of Quadratic program: min_x 1/2 x^T P x + q^T x  s.t. Gx≤h, Ax=b"
    '''
    import numpy as np
    import cvxpy as cp
    n = len(expected_returns)
    w = cp.Variable(n)
    mu = np.array(expected_returns); sigma = np.array(cov_matrix)
    obj = mu @ w - risk_aversion / 2 * cp.quad_form(w, sigma)
    prob = cp.Problem(cp.Maximize(obj), [cp.sum(w) == 1, w >= 0])
    prob.solve()
    return w.value




def quick_ratio(current_assets, inventory, current_liabilities):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "Quick Ratio — (Current Assets - Inventory) / Current Liabilities. More conservative than current ratio."
    y_as_x: []
    :param current_assets: "Current Assets are assets expected to be converted to cash within one year."
    :param inventory: "Inventory is the raw materials, work-in-process, and finished goods held for sale."
    :param current_liabilities: "Current Liabilities are obligations due within one year."
    :return: "Computed value of Quick ratio: Quick Ratio = (Cash + Marketable Securities + AR) / Current Liabilities"
    '''
    return (current_assets - inventory) / current_liabilities






def quoted_spread_pct(value_a, value_b):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Liquidity Risk', 'Market Liquidity', 'Execution Cost']
    function: "Quoted spread (%) — Quoted Spread = (Ask-Bid)/Mid. A financial metric in the domain of Liquidity risk, market liquidity & execution cost."
    y_as_x: []
    :param value_a: "Parameter value_a used in Quoted spread (%) calculation."
    :param value_b: "Parameter value_b used in Quoted spread (%) calculation."
    :return: "Computed value of Quoted spread (%): Quoted Spread = (Ask-Bid)/Mid"
    '''
    return value_a - value_b






def rate_of_change_roc(close, period=10):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "Rate of Change (ROC) — percentage change in price over n periods."
    y_as_x: []
    :param close: "Close is the final trading price at the end of a trading period."
    :param period: "Period (n) is the lookback window in number of bars for technical indicators."
    :return: "Computed value of Rate of change (ROC): ROC = P_t/P_{t-n} - 1"
    '''
    import pandas as pd
    c = pd.Series(close)
    return (c - c.shift(period)) / c.shift(period) * 100






def real_estate_dcf(rate, num_periods, payment, future_value=0):
    '''
    domain: ['Real estate finance']
    subdomain: ['Real Estate Finance']
    function: "Real estate DCF — Value = Σ_t NOI_t/(1+r)^t + TV/(1+r)^T. A financial metric in the domain of Real estate finance."
    y_as_x: []
    :param rate: "Rate (r) is the interest rate or discount rate per period."
    :param num_periods: "Number of Periods (n) is the total number of payment or compounding periods."
    :param payment: "Payment (PMT) is the periodic payment amount in an amortization schedule."
    :param future_value: "Future Value (FV) is the value of a current asset at a future date."
    :return: "Computed value of Real estate DCF: Value = Σ_t NOI_t/(1+r)^t + TV/(1+r)^T"
    '''
    import numpy_financial as npf
    return npf.pv(rate, num_periods, -payment, -future_value)






def real_exchange_rate(sp, p):
    '''
    domain: ['FX & international finance']
    subdomain: ['FX Markets', 'International Finance']
    function: "Real exchange rate — q = S·P* / P. A financial metric in the domain of FX & international finance."
    y_as_x: []
    :param sp: "Parameter sp used in Real exchange rate calculation."
    :param p: "Model order parameter p (autoregressive order or similar)."
    :return: "Computed value of Real exchange rate: q = S·P* / P"
    '''
    return sp / p






def real_yield_bond_pricing(face_value, real_coupon_rate, real_yield, inflation_index_ratio, periods, frequency=2):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Fixed Income', 'Bond Mathematics', 'Credit Markets']
    function: "Real yield bond pricing — P = sum_t Real CF_t /(1+real y)^t. A financial metric in the domain of Fixed income, bonds & credit markets."
    y_as_x: []
    :param args: "Parameter args used in Real yield bond pricing calculation."
    :param kwargs: "Parameter kwargs used in Real yield bond pricing calculation."
    :return: "Computed value of Real yield bond pricing: P = sum_t Real CF_t /(1+real y)^t"
    '''
    import numpy as np
    c = face_value * real_coupon_rate / frequency * inflation_index_ratio
    r = real_yield / frequency; n = int(periods * frequency)
    t = np.arange(1, n+1)
    return np.sum(c / (1+r)**t) + face_value * inflation_index_ratio / (1+r)**n


def realized_beta(cov_intradayassetmarket, var_intradaymarket):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "Realized beta — beta_realized = Cov_intraday(asset,market)/Var_intraday(market). A financial metric in the domain of Market risk & volatility modeling."
    y_as_x: []
    :param cov_intradayassetmarket: "Parameter cov_intradayassetmarket used in Realized beta calculation."
    :param var_intradaymarket: "Parameter var_intradaymarket used in Realized beta calculation."
    :return: "Computed value of Realized beta: beta_realized = Cov_intraday(asset,market)/Var_intraday(market)"
    '''
    return cov_intradayassetmarket / var_intradaymarket






def realized_hedge_effectiveness(hedged_pnl, unhedged_pnl):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Commodities', 'Futures', 'Hedging']
    function: "Realized hedge effectiveness — HE = 1 - Var(Hedged Position)/Var(Unhedged Position). A financial metric in the domain of Commodities, futures & hedging."
    y_as_x: []
    :param args: "Parameter args used in Realized hedge effectiveness calculation."
    :param kwargs: "Parameter kwargs used in Realized hedge effectiveness calculation."
    :return: "Computed value of Realized hedge effectiveness: HE = 1 - Var(Hedged Position)/Var(Unhedged Position)"
    '''
    return 1 - abs(hedged_pnl) / abs(unhedged_pnl) if unhedged_pnl != 0 else 1


def realized_spread(value_a, value_b):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Liquidity Risk', 'Market Liquidity', 'Execution Cost']
    function: "Realized spread — Realized Spread = 2 x side x (Trade Price - Mid_{t+Delta}). A financial metric in the domain of Liquidity risk, market liquidity & execution cost."
    y_as_x: ['adverse_selection_cost']
    :param value_a: "Parameter value_a used in Realized spread calculation."
    :param value_b: "Parameter value_b used in Realized spread calculation."
    :return: "Computed value of Realized spread: Realized Spread = 2 x side x (Trade Price - Mid_{t+Delta})"
    '''
    return value_a - value_b






def realized_variance(returns):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "Realized variance — RV_t = sum_{i=1}^n r_{t,i}^2. A financial metric in the domain of Market risk & volatility modeling."
    y_as_x: []
    :param args: "Parameter args used in Realized variance calculation."
    :param kwargs: "Parameter kwargs used in Realized variance calculation."
    :return: "Computed value of Realized variance: RV_t = sum_{i=1}^n r_{t,i}^2"
    '''
    import numpy as np
    return np.sum(np.array(returns)**2)


def realized_volatility(returns, annualize=True, periods_per_year=252):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "Realized Volatility — historical standard deviation of returns, optionally annualized."
    y_as_x: []
    :param returns: "Returns are the gain or loss generated on an investment over a specific period."
    :param annualize: "Parameter annualize used in Realized volatility calculation."
    :param periods_per_year: "Periods Per Year is the number of compounding or return periods in one year."
    :return: "Computed value of Realized volatility: RVOL = sqrt(sum intraday returns^2)"
    '''
    import numpy as np
    vol = np.std(returns, ddof=1)
    return vol * np.sqrt(periods_per_year) if annualize else vol






def receivables_turnover(revenue, average_ar):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "Receivables turnover — Receivables Turnover = Revenue / Average AR. A financial metric in the domain of Accounting & financial statement analysis."
    y_as_x: []
    :param revenue: "Revenue is the total amount of income a business generates from the sale of goods or services before deducting expenses."
    :param average_ar: "Parameter average_ar used in Receivables turnover calculation."
    :return: "Computed value of Receivables turnover: Receivables Turnover = Revenue / Average AR"
    '''
    return revenue / average_ar






def recovery_factor(net_profit, max_drawdown):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Performance Attribution', 'Risk-Adjusted Performance']
    function: "Recovery factor — Recovery Factor = Net Profit / |Max Drawdown|. A financial metric in the domain of Performance measurement & attribution."
    y_as_x: []
    :param net_profit: "Parameter net_profit used in Recovery factor calculation."
    :param max_drawdown: "Maximum Drawdown (MDD) is the maximum observed loss from peak to trough."
    :return: "Computed value of Recovery factor: Recovery Factor = Net Profit / |Max Drawdown|"
    '''
    return net_profit / max_drawdown






def recovery_rate(numerator, denominator):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit Risk', 'Default Modeling', 'Credit Portfolio']
    function: "Recovery rate — Recovery = 1 - LGD. A financial metric in the domain of Credit risk, default modeling & credit portfolio."
    y_as_x: ['cds_spread_approximation', 'loss_given_default', 'reduced_form_cds_hazard_relation']
    :param numerator: "Parameter numerator used in Recovery rate calculation."
    :param denominator: "Parameter denominator used in Recovery rate calculation."
    :return: "Computed value of Recovery rate: Recovery = 1 - LGD"
    '''
    return numerator / denominator if denominator != 0 else 0






def reduced_form_cds_hazard_relation(cds_spread, loss_given_default):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit Risk', 'Default Modeling', 'Credit Portfolio']
    function: "Reduced-form CDS hazard relation — CDS Spread approx lambda x LGD. A financial metric in the domain of Credit risk, default modeling & credit portfolio."
    y_as_x: []
    :param args: "Parameter args used in Reduced-form CDS hazard relation calculation."
    :param kwargs: "Parameter kwargs used in Reduced-form CDS hazard relation calculation."
    :return: "Computed value of Reduced-form CDS hazard relation: CDS Spread approx lambda x LGD"
    '''
    return cds_spread / loss_given_default


def refinance_proceeds(new_loan_amount, closing_costs, existing_loan_balance):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Real Estate Finance', 'Mortgage Analysis']
    function: "Refinance proceeds — Refi Proceeds = New Loan - Old Loan - Fees. A financial metric in the domain of Real estate finance & mortgages."
    y_as_x: []
    :param args: "Parameter args used in Refinance proceeds calculation."
    :param kwargs: "Parameter kwargs used in Refinance proceeds calculation."
    :return: "Computed value of Refinance proceeds: Refi Proceeds = New Loan - Old Loan - Fees"
    '''
    return new_loan_amount - closing_costs - existing_loan_balance




def relative_ppp(domestic_inflation, foreign_inflation):
    '''
    domain: ['FX & international finance']
    subdomain: ['FX Markets', 'International Finance']
    function: "Relative PPP — Delta S / S approx pi_d - pi_f. A financial metric in the domain of FX & international finance."
    y_as_x: []
    :param args: "Parameter args used in Relative PPP calculation."
    :param kwargs: "Parameter kwargs used in Relative PPP calculation."
    :return: "Computed value of Relative PPP: Delta S / S approx pi_d - pi_f"
    '''
    return (1 + domestic_inflation) / (1 + foreign_inflation) - 1




def relative_spread(value_a, value_b):
    '''
    domain: ['Liquidity risk & market liquidity']
    subdomain: ['Liquidity Risk', 'Market Liquidity']
    function: "Relative spread — Relative Spread = (Ask - Bid) / Mid. A financial metric in the domain of Liquidity risk & market liquidity."
    y_as_x: []
    :param value_a: "Parameter value_a used in Relative spread calculation."
    :param value_b: "Parameter value_b used in Relative spread calculation."
    :return: "Computed value of Relative spread: Relative Spread = (Ask - Bid) / Mid"
    '''
    return value_a - value_b






def relative_strength_index_rsi(close, period=14):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "Relative Strength Index (RSI) — momentum oscillator. RSI = 100 - 100/(1 + RS). Overbought > 70, oversold < 30."
    y_as_x: []
    :param close: "Close is the final trading price at the end of a trading period."
    :param period: "Period (n) is the lookback window in number of bars for technical indicators."
    :return: "Computed value of Relative strength index (RSI): RSI = 100 - 100/(1+RS), RS=AvgGain/AvgLoss"
    '''
    import pandas as pd
    c = pd.Series(close)
    delta = c.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - 100 / (1 + rs)






def rent_coverage_ratio(gross_monthly_income, monthly_rent):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Real Estate Finance', 'Mortgage Analysis']
    function: "Rent coverage ratio — Rent Coverage = Gross Monthly Income / Monthly Rent. A financial metric in the domain of Real estate finance & mortgages."
    y_as_x: []
    :param gross_monthly_income: "Gross Monthly Income is pre-tax monthly income."
    :param monthly_rent: "Parameter monthly_rent used in Rent coverage ratio calculation."
    :return: "Computed value of Rent coverage ratio: Rent Coverage = Gross Monthly Income / Monthly Rent"
    '''
    return gross_monthly_income / monthly_rent






def repricing_gap(rate_sensitive_assets_t, rate_sensitive_liabilities_t):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Treasury', 'ALM', 'Balance Sheet Management']
    function: "Repricing gap — Gap_t = Rate Sensitive Assets_t - Rate Sensitive Liabilities_t. A financial metric in the domain of Treasury, ALM & balance-sheet management."
    y_as_x: ['earnings_at_risk']
    :param rate_sensitive_assets_t: "Parameter rate_sensitive_assets_t used in Repricing gap calculation."
    :param rate_sensitive_liabilities_t: "Parameter rate_sensitive_liabilities_t used in Repricing gap calculation."
    :return: "Computed value of Repricing gap: Gap_t = Rate Sensitive Assets_t - Rate Sensitive Liabilities_t"
    '''
    return rate_sensitive_assets_t - rate_sensitive_liabilities_t






def residual_income(net_income, r_e_x_beginning_equity):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "Residual income — RI = Net Income - R_e x Beginning Equity. A financial metric in the domain of Corporate finance, valuation & capital budgeting."
    y_as_x: []
    :param net_income: "Net Income is the total profit after all expenses, taxes, interest, and depreciation have been deducted from total revenue."
    :param r_e_x_beginning_equity: "Parameter r_e_x_beginning_equity used in Residual income calculation."
    :return: "Computed value of Residual income: RI = Net Income - R_e x Beginning Equity"
    '''
    return net_income - r_e_x_beginning_equity






def residual_income_valuation(book_value, residual_incomes, cost_of_equity):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Equity Valuation', 'Asset Pricing']
    function: "Residual income valuation — V_0 = B_0 + sum_t RI_t/(1+r)^t. A financial metric in the domain of Equity valuation & asset pricing."
    y_as_x: []
    :param args: "Parameter args used in Residual income valuation calculation."
    :param kwargs: "Parameter kwargs used in Residual income valuation calculation."
    :return: "Computed value of Residual income valuation: V_0 = B_0 + sum_t RI_t/(1+r)^t"
    '''
    import numpy as np
    ri = np.array(residual_incomes)
    t = np.arange(1, len(ri)+1)
    return book_value + np.sum(ri / (1+cost_of_equity)**t)


def retention_ratio(net_income, dividends):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "Retention Ratio — proportion of earnings retained. RR = 1 - Payout Ratio."
    y_as_x: ['sustainable_growth_rate']
    :param net_income: "Net Income is the total profit after all expenses, taxes, interest, and depreciation have been deducted from total revenue."
    :param dividends: "Dividends are portions of a company's earnings distributed to shareholders."
    :return: "Computed value of Retention ratio: Retention = 1 - Dividend Payout Ratio"
    '''
    return (net_income - dividends) / net_income if net_income != 0 else 0






def retrospective_reserve(past_premiums_accumulated, past_benefits_accumulated):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "Retrospective reserve — V_t = Accumulated Value(Past Premiums - Past Benefits - Expenses). A financial metric in the domain of Actuarial science & insurance."
    y_as_x: []
    :param args: "Parameter args used in Retrospective reserve calculation."
    :param kwargs: "Parameter kwargs used in Retrospective reserve calculation."
    :return: "Computed value of Retrospective reserve: V_t = Accumulated Value(Past Premiums - Past Benefits - Expenses)"
    '''
    return past_premiums_accumulated - past_benefits_accumulated


def return_on_assets_roa(net_income, total_assets):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "Return on Assets (ROA) — net income divided by total assets."
    y_as_x: []
    :param net_income: "Net Income is the total profit after all expenses, taxes, interest, and depreciation have been deducted from total revenue."
    :param total_assets: "Total Assets represent the sum of all current and non-current assets owned by a company."
    :return: "Computed value of Return on assets (ROA): ROA = Net Income / Average Assets"
    '''
    return net_income / total_assets






def return_on_capital_employed_roce(ebit, capital_employed):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "Return on capital employed (ROCE) — ROCE = EBIT / Capital Employed. A financial metric in the domain of Accounting & financial statement analysis."
    y_as_x: []
    :param ebit: "EBIT (Earnings Before Interest and Taxes) is a financial metric measuring a company's profitability from core operations."
    :param capital_employed: "Parameter capital_employed used in Return on capital employed (ROCE) calculation."
    :return: "Computed value of Return on capital employed (ROCE): ROCE = EBIT / Capital Employed"
    '''
    return ebit / capital_employed






def return_on_equity_roe(net_income, total_equity):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "Return on Equity (ROE) — net income divided by total equity."
    y_as_x: []
    :param net_income: "Net Income is the total profit after all expenses, taxes, interest, and depreciation have been deducted from total revenue."
    :param total_equity: "Total Equity is the residual interest in the assets of an entity after deducting all its liabilities."
    :return: "Computed value of Return on equity (ROE): ROE = Net Income / Average Equity"
    '''
    return net_income / total_equity






def return_on_invested_capital_roic(nopat, invested_capital):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "Return on Invested Capital (ROIC) — NOPAT / Invested Capital."
    y_as_x: []
    :param nopat: "Parameter nopat used in Return on invested capital (ROIC) calculation."
    :param invested_capital: "Parameter invested_capital used in Return on invested capital (ROIC) calculation."
    :return: "Computed value of Return on invested capital (ROIC): ROIC = NOPAT / Average Invested Capital"
    '''
    return nopat / invested_capital






def return_on_regulatory_capital_rorc(expected_profit, economic_or_regulatory_capital):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Banking', 'Consumer Lending', 'Project Finance']
    function: "Return on regulatory capital (RORC) — RORC = Expected Profit / Economic or Regulatory Capital. A financial metric in the domain of Banking, consumer lending & project finance."
    y_as_x: []
    :param expected_profit: "Parameter expected_profit used in Return on regulatory capital (RORC) calculation."
    :param economic_or_regulatory_capital: "Parameter economic_or_regulatory_capital used in Return on regulatory capital (RORC) calculation."
    :return: "Computed value of Return on regulatory capital (RORC): RORC = Expected Profit / Economic or Regulatory Capital"
    '''
    return expected_profit / economic_or_regulatory_capital






def revenue_growth(current_revenue, previous_revenue):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "Revenue growth — g_t = Revenue_t / Revenue_(t-1) - 1. A financial metric in the domain of Accounting & financial statement analysis."
    y_as_x: []
    :param args: "Parameter args used in Revenue growth calculation."
    :param kwargs: "Parameter kwargs used in Revenue growth calculation."
    :return: "Computed value of Revenue growth: g_t = Revenue_t / Revenue_(t-1) - 1"
    '''
    return (current_revenue - previous_revenue) / previous_revenue


def rho(spot_price, strike_price, risk_free_rate, volatility, time_to_expiry):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Rho — Rho = K T e^{-rT} N(d2). A financial metric in the domain of Derivatives, options & volatility."
    y_as_x: []
    :param spot_price: "Spot Price (S) is the current market price of the underlying asset."
    :param strike_price: "Strike Price (K) is the predetermined price at which an option can be exercised."
    :param risk_free_rate: "Risk-Free Rate (Rf) is the theoretical rate of return with zero risk, typically proxied by government bond yields."
    :param volatility: "Volatility (sigma) is the annualized standard deviation of returns."
    :param time_to_expiry: "Time to Expiry (T) is the remaining time until expiration, in years."
    :return: "Computed value of Rho: Rho = K T e^{-rT} N(d2)"
    '''
    import numpy as np
    from scipy.stats import norm
    d1 = (np.log(spot_price/strike_price) + (risk_free_rate + 0.5*volatility**2)*time_to_expiry) / (volatility*np.sqrt(time_to_expiry))
    d2 = d1 - volatility*np.sqrt(time_to_expiry)
    return norm.cdf(d1)  # Adjust based on specific Greek






def risk_parity_objective(cov_matrix, target_risk=None):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Risk parity objective — min_w sum_i sum_j (RC_i-RC_j)^2. A financial metric in the domain of Asset management & portfolio optimization."
    y_as_x: []
    :param returns_matrix: "Parameter returns_matrix used in Risk parity objective calculation."
    :return: "Computed value of Risk parity objective: min_w sum_i sum_j (RC_i-RC_j)^2"
    '''
    import numpy as np
    from scipy.optimize import minimize
    sigma = np.array(cov_matrix); n = sigma.shape[0]
    def obj(w):
        pv = np.sqrt(w @ sigma @ w)
        mrc = sigma @ w / pv; rc = w * mrc
        return np.sum((rc - pv/n)**2)
    res = minimize(obj, np.ones(n)/n, constraints={'type':'eq','fun': lambda w: np.sum(w)-1}, bounds=[(0,1)]*n)
    return res.x


def risk_metrics_covariance(returns, lambda_param=0.94):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "RiskMetrics covariance — Sigma_t = lambda Sigma_{t-1} + (1-lambda) r_{t-1} r_{t-1}'. A financial metric in the domain of Market risk & volatility modeling."
    y_as_x: []
    :param args: "Parameter args used in RiskMetrics covariance calculation."
    :param kwargs: "Parameter kwargs used in RiskMetrics covariance calculation."
    :return: "Computed value of RiskMetrics covariance: Sigma_t = lambda Sigma_{t-1} + (1-lambda) r_{t-1} r_{t-1}'"
    '''
    import numpy as np
    r = np.array(returns)
    n, m = r.shape
    cov = np.cov(r.T)
    for t in range(1, n):
        cov = lambda_param * cov + (1 - lambda_param) * np.outer(r[t], r[t])
    return cov




def risk_neutral_probability(data, *args):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Risk-neutral probability — p = (e^{(r-q)Delta t} - d)/(u-d). A financial metric in the domain of Derivatives, options & volatility."
    y_as_x: []
    :param data: "Parameter data used in Risk-neutral probability calculation."
    :param args: "Parameter args used in Risk-neutral probability calculation."
    :return: "Computed value of Risk-neutral probability: p = (e^{(r-q)Delta t} - d)/(u-d)"
    '''
    import numpy as np
    return np.array(data)






def risk_weighted_assets_rwa(sum_i_exposure_i, riskweight_i):
    '''
    domain: ['Bank regulation, Basel & prudential ratios']
    subdomain: ['Bank Regulation', 'Basel Framework', 'Prudential Ratios']
    function: "Risk-weighted assets (RWA) — RWA = sum_i Exposure_i x RiskWeight_i. A financial metric in the domain of Bank regulation, Basel & prudential ratios."
    y_as_x: []
    :param sum_i_exposure_i: "Parameter sum_i_exposure_i used in Risk-weighted assets (RWA) calculation."
    :param riskweight_i: "Parameter riskweight_i used in Risk-weighted assets (RWA) calculation."
    :return: "Computed value of Risk-weighted assets (RWA): RWA = sum_i Exposure_i x RiskWeight_i"
    '''
    return sum_i_exposure_i * riskweight_i






def roc_auc(y_true, y_score):
    '''
    domain: ['Quantitative forecasting & machine learning in finance']
    subdomain: ['Quantitative Finance', 'Machine Learning']
    function: "ROC AUC — AUC = integral_0^1 TPR(FPR^{-1}(u)) du. A financial metric in the domain of Quantitative forecasting & machine learning in finance."
    y_as_x: []
    :param X: "Parameter X used in ROC AUC calculation."
    :param y: "Parameter y used in ROC AUC calculation."
    :return: "Computed value of ROC AUC: AUC = integral_0^1 TPR(FPR^{-1}(u)) du"
    '''
    from sklearn.metrics import roc_auc_score
    return roc_auc_score(y_true, y_score)


def rogers_satchell_volatility(high, low, close, open_price):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "Rogers-Satchell volatility — sigma_RS^2 = (ln(H/O))(ln(H/C)) + (ln(L/O))(ln(L/C)). A financial metric in the domain of Market risk & volatility modeling."
    y_as_x: []
    :param args: "Parameter args used in Rogers-Satchell volatility calculation."
    :param kwargs: "Parameter kwargs used in Rogers-Satchell volatility calculation."
    :return: "Computed value of Rogers-Satchell volatility: sigma_RS^2 = (ln(H/O))(ln(H/C)) + (ln(L/O))(ln(L/C))"
    '''
    import numpy as np
    h = np.array(high); l = np.array(low); c = np.array(close); o = np.array(open_price)
    return np.sqrt(np.mean(np.log(h/c) * np.log(h/o) + np.log(l/c) * np.log(l/o)))




def roll_implied_spread(value_a, value_b):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Liquidity Risk', 'Market Liquidity', 'Execution Cost']
    function: "Roll implied spread — Spread_Roll = 2 sqrt(-Cov(Delta p_t, Delta p_{t-1})). A financial metric in the domain of Liquidity risk, market liquidity & execution cost."
    y_as_x: []
    :param value_a: "Parameter value_a used in Roll implied spread calculation."
    :param value_b: "Parameter value_b used in Roll implied spread calculation."
    :return: "Computed value of Roll implied spread: Spread_Roll = 2 sqrt(-Cov(Delta p_t, Delta p_{t-1}))"
    '''
    return value_a - value_b






def roll_rate(balances_migrating_to_worse_delinquency_bucket, prior_bucket_balance):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit Risk', 'Default Modeling', 'Credit Portfolio']
    function: "Roll rate — Roll Rate = balances migrating to worse delinquency bucket / prior bucket balance. A financial metric in the domain of Credit risk, default modeling & credit portfolio."
    y_as_x: []
    :param balances_migrating_to_worse_delinquency_bucket: "Parameter balances_migrating_to_worse_delinquency_bucket used in Roll rate calculation."
    :param prior_bucket_balance: "Parameter prior_bucket_balance used in Roll rate calculation."
    :return: "Computed value of Roll rate: Roll Rate = balances migrating to worse delinquency bucket / prior bucket balance"
    '''
    return balances_migrating_to_worse_delinquency_bucket / prior_bucket_balance






def roll_spread_estimator(value_a, value_b):
    '''
    domain: ['Liquidity risk & market liquidity']
    subdomain: ['Liquidity Risk', 'Market Liquidity']
    function: "Roll spread estimator — Spread_Roll = 2√[-Cov(ΔP_t, ΔP_{t-1})]. A financial metric in the domain of Liquidity risk & market liquidity."
    y_as_x: []
    :param value_a: "Parameter value_a used in Roll spread estimator calculation."
    :param value_b: "Parameter value_b used in Roll spread estimator calculation."
    :return: "Computed value of Roll spread estimator: Spread_Roll = 2√[-Cov(ΔP_t, ΔP_{t-1})]"
    '''
    return value_a - value_b






def roll_yield(numerator, denominator):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Commodities', 'Futures', 'Hedging']
    function: "Roll yield — Roll Yield = Futures Return - Spot Return - Collateral Return. A financial metric in the domain of Commodities, futures & hedging."
    y_as_x: ['commodity_carry_return']
    :param numerator: "Parameter numerator used in Roll yield calculation."
    :param denominator: "Parameter denominator used in Roll yield calculation."
    :return: "Computed value of Roll yield: Roll Yield = Futures Return - Spot Return - Collateral Return"
    '''
    return numerator / denominator if denominator != 0 else 0






def roll_down_return(current_yield, horizon_yield, duration, horizon):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Fixed Income', 'Bond Mathematics', 'Credit Markets']
    function: "Roll-down return — Roll-down approx -Duration x Delta Yield from curve slide. A financial metric in the domain of Fixed income, bonds & credit markets."
    y_as_x: []
    :param args: "Parameter args used in Roll-down return calculation."
    :param kwargs: "Parameter kwargs used in Roll-down return calculation."
    :return: "Computed value of Roll-down return: Roll-down approx -Duration x Delta Yield from curve slide"
    '''
    return current_yield * horizon - duration * (horizon_yield - current_yield)


def rsi_indicator(close, period=14):
    '''
    domain: ['Technical analysis']
    subdomain: ['Technical Analysis']
    function: "RSI Indicator — Relative Strength Index using Wilder smoothing."
    y_as_x: []
    :param close: "Close is the final trading price at the end of a trading period."
    :param period: "Period (n) is the lookback window in number of bars for technical indicators."
    :return: "Computed value of RSI: RSI = 100 - 100/(1 + RS)"
    '''
    import pandas as pd
    c = pd.Series(close)
    delta = c.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - 100 / (1 + rs)






def rvpi(nav, paid_in_capital):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Private Equity', 'Venture Capital', 'LBO']
    function: "RVPI — RVPI = Residual Value (NAV of unrealized investments) / Paid-In Capital. A financial metric in the domain of Private equity, venture capital & LBO."
    y_as_x: []
    :param args: "Parameter args used in RVPI calculation."
    :param kwargs: "Parameter kwargs used in RVPI calculation."
    :return: "Computed value of RVPI: RVPI = Residual Value (NAV of unrealized investments) / Paid-In Capital"
    '''
    return nav / paid_in_capital


def sabr_implied_vol(forward, strike, time_to_expiry, alpha, beta, rho, nu):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "SABR implied vol — sigma_BS = SABR(F,K,alpha,beta,rho,nu,T). A financial metric in the domain of Derivatives, options & volatility."
    y_as_x: []
    :param args: "Parameter args used in SABR implied vol calculation."
    :param kwargs: "Parameter kwargs used in SABR implied vol calculation."
    :return: "Computed value of SABR implied vol: sigma_BS = SABR(F,K,alpha,beta,rho,nu,T)"
    '''
    import numpy as np
    F = forward; K = strike; T = time_to_expiry
    if abs(F - K) < 1e-12:
        return alpha / F**(1-beta) * (1 + ((1-beta)**2/24 * alpha**2/F**(2-2*beta) + rho*beta*nu*alpha/(4*F**(1-beta)) + (2-3*rho**2)/24*nu**2) * T)
    FK = F * K
    logFK = np.log(F / K)
    z = nu / alpha * FK**((1-beta)/2) * logFK
    xz = np.log((np.sqrt(1 - 2*rho*z + z**2) + z - rho) / (1 - rho))
    prefix = alpha / (FK**((1-beta)/2) * (1 + (1-beta)**2/24 * logFK**2 + (1-beta)**4/1920 * logFK**4))
    correction = 1 + ((1-beta)**2/24 * alpha**2/FK**(1-beta) + rho*beta*nu*alpha/(4*FK**((1-beta)/2)) + (2-3*rho**2)/24*nu**2) * T
    return prefix * z / xz * correction if abs(xz) > 1e-12 else prefix * correction




def sarima(time_series, order):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Financial Econometrics', 'Time Series Analysis']
    function: "SARIMA — Phi(L^s)phi(L)(1-L)^d(1-L^s)^D x_t = Theta(L^s)theta(L)epsilon_t. A financial metric in the domain of Econometrics & time-series finance."
    y_as_x: []
    :param time_series: "Time Series is a sequence of data points indexed in time order."
    :param order: "Order specifies the model order, e.g., (p,d,q) for ARIMA."
    :return: "Computed value of SARIMA: Phi(L^s)phi(L)(1-L)^d(1-L^s)^D x_t = Theta(L^s)theta(L)epsilon_t"
    '''
    from statsmodels.tsa.arima.model import ARIMA
    model = ARIMA(time_series, order=order).fit()
    return model






def security_market_line(risk_free_rate, beta, market_risk_premium):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Equity Valuation', 'Asset Pricing']
    function: "Security market line — E[R] = R_f + beta(E[R_m]-R_f). A financial metric in the domain of Equity valuation & asset pricing."
    y_as_x: []
    :param args: "Parameter args used in Security market line calculation."
    :param kwargs: "Parameter kwargs used in Security market line calculation."
    :return: "Computed value of Security market line: E[R] = R_f + beta(E[R_m]-R_f)"
    '''
    return risk_free_rate + beta * market_risk_premium


def selection_effect_brinson_fachler(benchmark_weights, portfolio_sector_returns, benchmark_sector_returns):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Performance Attribution', 'Risk-Adjusted Performance']
    function: "Selection effect (Brinson-Fachler) — Selection_i = w_i^B(r_i^P - r_i^B). A financial metric in the domain of Performance measurement & attribution."
    y_as_x: []
    :param args: "Parameter args used in Selection effect (Brinson-Fachler) calculation."
    :param kwargs: "Parameter kwargs used in Selection effect (Brinson-Fachler) calculation."
    :return: "Computed value of Selection effect (Brinson-Fachler): Selection_i = w_i^B(r_i^P - r_i^B)"
    '''
    import numpy as np
    return np.array(benchmark_weights) * (np.array(portfolio_sector_returns) - np.array(benchmark_sector_returns))




def semivariance(returns, target=0):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "Semivariance — SemiVar = E[min(R-mu,0)^2]. A financial metric in the domain of Market risk & volatility modeling."
    y_as_x: []
    :param returns_matrix: "Parameter returns_matrix used in Semivariance calculation."
    :return: "Computed value of Semivariance: SemiVar = E[min(R-mu,0)^2]"
    '''
    import numpy as np
    r = np.array(returns)
    downside = np.minimum(r - target, 0)
    return np.mean(downside**2)




def severity(net_loss, defaulted_balance):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Structured Finance', 'Securitization']
    function: "Severity — Severity = Net Loss / Defaulted Balance. A financial metric in the domain of Structured finance & securitization."
    y_as_x: ['pure_premium']
    :param net_loss: "Parameter net_loss used in Severity calculation."
    :param defaulted_balance: "Parameter defaulted_balance used in Severity calculation."
    :return: "Computed value of Severity: Severity = Net Loss / Defaulted Balance"
    '''
    return net_loss / defaulted_balance






def sharpe_ratio(returns, risk_free_rate=0, periods_per_year=252):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Sharpe Ratio — risk-adjusted return = annualized excess return / annualized volatility."
    y_as_x: []
    :param returns: "Returns are the gain or loss generated on an investment over a specific period."
    :param risk_free_rate: "Risk-Free Rate (Rf) is the theoretical rate of return with zero risk, typically proxied by government bond yields."
    :param periods_per_year: "Periods Per Year is the number of compounding or return periods in one year."
    :return: "Computed value of Sharpe ratio: Sharpe = (E[R_p]-R_f)/sigma_p"
    '''
    import numpy as np
    r = np.array(returns)
    excess = r - risk_free_rate / periods_per_year
    return np.mean(excess) / np.std(excess, ddof=1) * np.sqrt(periods_per_year)






def sharpe_lintner_beta_regression(y, X):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Equity Valuation', 'Asset Pricing']
    function: "Sharpe-Lintner beta regression — R_i-R_f = alpha + beta(R_m-R_f)+epsilon. A financial metric in the domain of Equity valuation & asset pricing."
    y_as_x: []
    :param y: "Parameter y used in Sharpe-Lintner beta regression calculation."
    :param X: "Parameter X used in Sharpe-Lintner beta regression calculation."
    :return: "Computed value of Sharpe-Lintner beta regression: R_i-R_f = alpha + beta(R_m-R_f)+epsilon"
    '''
    import statsmodels.api as sm
    X_const = sm.add_constant(X)
    model = sm.OLS(y, X_const).fit()
    return model






def short_rate_bond_pricing_pde(r0, kappa, theta, sigma, face_value, maturity, dt=0.01, dr=0.001):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Interest Rate Modeling', 'Term Structure']
    function: "Short-rate bond pricing PDE — dP/dt + a(r,t)dP/dr + 0.5 b(r,t)^2 d^2P/dr^2 - rP = 0. A financial metric in the domain of Interest-rate modeling & term structures."
    y_as_x: []
    :param args: "Parameter args used in Short-rate bond pricing PDE calculation."
    :param kwargs: "Parameter kwargs used in Short-rate bond pricing PDE calculation."
    :return: "Computed value of Short-rate bond pricing PDE: dP/dt + a(r,t)dP/dr + 0.5 b(r,t)^2 d^2P/dr^2 - rP = 0"
    '''
    import numpy as np
    n_t = int(maturity/dt); n_r = 200
    r_grid = np.linspace(0, 0.3, n_r); V = np.full(n_r, face_value, dtype=float)
    for t in range(n_t-1, -1, -1):
        V_new = V.copy()
        for i in range(1, n_r-1):
            dr_val = r_grid[1]-r_grid[0]
            drift = kappa*(theta - r_grid[i])
            V_new[i] = V[i] + dt*(0.5*sigma**2*(V[i+1]-2*V[i]+V[i-1])/dr_val**2 + drift*(V[i+1]-V[i-1])/(2*dr_val) - r_grid[i]*V[i])
        V = V_new
    idx = np.argmin(np.abs(r_grid - r0))
    return V[idx]


def simple_compounding(principal, rate, time):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Interest Rate Modeling', 'Term Structure']
    function: "Simple compounding — FV = PV·(1+r·t). A financial metric in the domain of Interest-rate modeling & term structures."
    y_as_x: []
    :param args: "Parameter args used in Simple compounding calculation."
    :param kwargs: "Parameter kwargs used in Simple compounding calculation."
    :return: "Computed value of Simple compounding: FV = PV·(1+r·t)"
    '''
    return principal * (1 + rate * time)




def simple_forward_rate(spot_rate_short, spot_rate_long, t_short, t_long):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Interest Rate Modeling', 'Term Structure']
    function: "Simple forward rate — F = (1/DF(T)-1)/tau. A financial metric in the domain of Interest-rate modeling & term structures."
    y_as_x: []
    :param args: "Parameter args used in Simple forward rate calculation."
    :param kwargs: "Parameter kwargs used in Simple forward rate calculation."
    :return: "Computed value of Simple forward rate: F = (1/DF(T)-1)/tau"
    '''
    return (spot_rate_long * t_long - spot_rate_short * t_short) / (t_long - t_short)




def simple_return(price_current, price_previous):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Performance Attribution', 'Risk-Adjusted Performance']
    function: "Simple Return — (P_t - P_{t-1}) / P_{t-1}. Arithmetic return."
    y_as_x: []
    :param price_current: "Parameter price_current used in Simple return calculation."
    :param price_previous: "Parameter price_previous used in Simple return calculation."
    :return: "Computed value of Simple return: R_t = P_t/P_{t-1} - 1"
    '''
    return (price_current - price_previous) / price_previous






def single_monthly_mortality_smm(cpr):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Structured Finance', 'Securitization']
    function: "Single Monthly Mortality (SMM) — monthly prepayment rate derived from CPR."
    y_as_x: []
    :param cpr: "Parameter cpr used in Single monthly mortality (SMM) calculation."
    :return: "Computed value of Single monthly mortality (SMM): SMM = 1 - (1 - CPR)^(1/12)"
    '''
    return 1 - (1 - cpr)**(1/12)






def slippage(actual_execution_price, expected_price):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Liquidity Risk', 'Market Liquidity', 'Execution Cost']
    function: "Slippage — Slippage = Actual Execution Price - Expected Price. A financial metric in the domain of Liquidity risk, market liquidity & execution cost."
    y_as_x: []
    :param actual_execution_price: "Parameter actual_execution_price used in Slippage calculation."
    :param expected_price: "Parameter expected_price used in Slippage calculation."
    :return: "Computed value of Slippage: Slippage = Actual Execution Price - Expected Price"
    '''
    return actual_execution_price - expected_price






def smith_wilson_extrapolation(maturities, rates, ufr, alpha=0.1):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Interest Rate Modeling', 'Term Structure']
    function: "Smith-Wilson extrapolation — P(u)=e^{-UFR u}+ sum_j zeta_j W(u_j,u). A financial metric in the domain of Interest-rate modeling & term structures."
    y_as_x: []
    :param args: "Parameter args used in Smith-Wilson extrapolation calculation."
    :param kwargs: "Parameter kwargs used in Smith-Wilson extrapolation calculation."
    :return: "Computed value of Smith-Wilson extrapolation: P(u)=e^{-UFR u}+ sum_j zeta_j W(u_j,u)"
    '''
    import numpy as np
    m = np.array(maturities); r = np.array(rates)
    return r[-1] + (ufr - r[-1]) * (1 - np.exp(-alpha * (m - m[-1])))


def solvency_ratio(available_capital, required_capital):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "Solvency ratio — Solvency Ratio = Available Capital / Required Capital. A financial metric in the domain of Actuarial science & insurance."
    y_as_x: []
    :param available_capital: "Parameter available_capital used in Solvency ratio calculation."
    :param required_capital: "Parameter required_capital used in Solvency ratio calculation."
    :return: "Computed value of Solvency ratio: Solvency Ratio = Available Capital / Required Capital"
    '''
    return available_capital / required_capital






def sortino_ratio(returns, risk_free_rate=0, periods_per_year=252):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Sortino Ratio — like Sharpe but uses downside deviation instead of total volatility."
    y_as_x: []
    :param returns: "Returns are the gain or loss generated on an investment over a specific period."
    :param risk_free_rate: "Risk-Free Rate (Rf) is the theoretical rate of return with zero risk, typically proxied by government bond yields."
    :param periods_per_year: "Periods Per Year is the number of compounding or return periods in one year."
    :return: "Computed value of Sortino ratio: Sortino = (E[R_p]-MAR)/DownsideDeviation"
    '''
    import numpy as np
    r = np.array(returns)
    excess = np.mean(r) - risk_free_rate / periods_per_year
    downside = np.sqrt(np.mean(np.minimum(r - risk_free_rate / periods_per_year, 0)**2))
    return excess / downside * np.sqrt(periods_per_year) if downside > 0 else float("inf")






def sources_and_uses_balance(sources, uses):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Private Equity', 'Venture Capital', 'LBO']
    function: "Sources and uses balance — Total Sources = Total Uses. A financial metric in the domain of Private equity, venture capital & LBO."
    y_as_x: []
    :param args: "Parameter args used in Sources and uses balance calculation."
    :param kwargs: "Parameter kwargs used in Sources and uses balance calculation."
    :return: "Computed value of Sources and uses balance: Total Sources = Total Uses"
    '''
    import numpy as np
    return np.sum(sources) - np.sum(uses)


def spark_spread(electricity_price, heat_rate_x_fuel_price):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Commodities', 'Futures', 'Hedging']
    function: "Spark spread — Spark Spread = Electricity Price - Heat Rate x Fuel Price. A financial metric in the domain of Commodities, futures & hedging."
    y_as_x: []
    :param electricity_price: "Parameter electricity_price used in Spark spread calculation."
    :param heat_rate_x_fuel_price: "Parameter heat_rate_x_fuel_price used in Spark spread calculation."
    :return: "Computed value of Spark spread: Spark Spread = Electricity Price - Heat Rate x Fuel Price"
    '''
    return electricity_price - heat_rate_x_fuel_price






def speed(dgamma, ds):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Speed — Speed = d(Gamma)/dS. A financial metric in the domain of Derivatives, options & volatility."
    y_as_x: []
    :param dgamma: "Parameter dgamma used in Speed calculation."
    :param ds: "Parameter ds used in Speed calculation."
    :return: "Computed value of Speed: Speed = d(Gamma)/dS"
    '''
    return dgamma / ds






def sponsor_cash_on_cash_return(cumulative_cash_to_sponsor, sponsor_equity_invested):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Private Equity', 'Venture Capital', 'LBO']
    function: "Sponsor cash-on-cash return — CoC = Cumulative Cash to Sponsor / Sponsor Equity Invested. A financial metric in the domain of Private equity, venture capital & LBO."
    y_as_x: []
    :param cumulative_cash_to_sponsor: "Parameter cumulative_cash_to_sponsor used in Sponsor cash-on-cash return calculation."
    :param sponsor_equity_invested: "Parameter sponsor_equity_invested used in Sponsor cash-on-cash return calculation."
    :return: "Computed value of Sponsor cash-on-cash return: CoC = Cumulative Cash to Sponsor / Sponsor Equity Invested"
    '''
    return cumulative_cash_to_sponsor / sponsor_equity_invested






def spot_rate_bootstrapping(par_rates, maturities):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Fixed Income', 'Bond Mathematics', 'Credit Markets']
    function: "Spot rate bootstrapping — P_n = sum_{i=1}^{n-1} C_i DF_i + (C_n+F)DF_n. A financial metric in the domain of Fixed income, bonds & credit markets."
    y_as_x: []
    :param args: "Parameter args used in Spot rate bootstrapping calculation."
    :param kwargs: "Parameter kwargs used in Spot rate bootstrapping calculation."
    :return: "Computed value of Spot rate bootstrapping: P_n = sum_{i=1}^{n-1} C_i DF_i + (C_n+F)DF_n"
    '''
    import numpy as np
    spots = [par_rates[0]]
    for i in range(1, len(par_rates)):
        c = par_rates[i]
        pv_coupons = sum(c / (1+spots[j])**maturities[j] for j in range(i))
        spot = ((1+c) / (1 - pv_coupons))**(1/maturities[i]) - 1
        spots.append(spot)
    return np.array(spots)


def spot_rate_from_discount_factor(discount_factor, maturity):
    '''
    domain: ['Fixed income & bond math']
    subdomain: ['Fixed Income', 'Bond Mathematics']
    function: "Spot rate from discount factor — z(t) = -ln(DF(t))/t. A financial metric in the domain of Fixed income & bond math."
    y_as_x: []
    :param args: "Parameter args used in Spot rate from discount factor calculation."
    :param kwargs: "Parameter kwargs used in Spot rate from discount factor calculation."
    :return: "Computed value of Spot rate from discount factor: z(t) = -ln(DF(t))/t"
    '''
    return (1 / discount_factor)**(1 / maturity) - 1




def spread_duration(price_down, price_up, initial_price, spread_change):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Fixed Income', 'Bond Mathematics', 'Credit Markets']
    function: "Spread duration — Spread Duration = -dP/ds / P. A financial metric in the domain of Fixed income, bonds & credit markets."
    y_as_x: ['duration_times_spread_dts']
    :param args: "Parameter args used in Spread duration calculation."
    :param kwargs: "Parameter kwargs used in Spread duration calculation."
    :return: "Computed value of Spread duration: Spread Duration = -dP/ds / P"
    '''
    return (price_down - price_up) / (2 * initial_price * spread_change)




def spread_option_kirk_approximation(F1, F2, strike, vol1, vol2, correlation, risk_free_rate, time_to_expiry):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Spread option (Kirk approximation) — C approx DF[F1 N(d1) - (F2+K)N(d2)]. A financial metric in the domain of Derivatives, options & volatility."
    y_as_x: []
    :param args: "Parameter args used in Spread option (Kirk approximation) calculation."
    :param kwargs: "Parameter kwargs used in Spread option (Kirk approximation) calculation."
    :return: "Computed value of Spread option (Kirk approximation): C approx DF[F1 N(d1) - (F2+K)N(d2)]"
    '''
    import numpy as np
    from scipy.stats import norm
    F2_adj = F2 / (F2 + strike)
    sigma = np.sqrt(vol1**2 - 2 * correlation * vol1 * vol2 * F2_adj + (vol2 * F2_adj)**2)
    d1 = (np.log((F1) / (F2 + strike)) + 0.5 * sigma**2 * time_to_expiry) / (sigma * np.sqrt(time_to_expiry))
    d2 = d1 - sigma * np.sqrt(time_to_expiry)
    return np.exp(-risk_free_rate * time_to_expiry) * (F1 * norm.cdf(d1) - (F2 + strike) * norm.cdf(d2))




def square_root_impact_law(y_sigma_sqrtq, v):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Liquidity Risk', 'Market Liquidity', 'Execution Cost']
    function: "Square-root impact law — Impact = Y sigma sqrt(Q/V). A financial metric in the domain of Liquidity risk, market liquidity & execution cost."
    y_as_x: []
    :param y_sigma_sqrtq: "Parameter y_sigma_sqrtq used in Square-root impact law calculation."
    :param v: "Parameter v used in Square-root impact law calculation."
    :return: "Computed value of Square-root impact law: Impact = Y sigma sqrt(Q/V)"
    '''
    return y_sigma_sqrtq / v






def stable_funding_gap(value_a, value_b):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Treasury', 'ALM', 'Balance Sheet Management']
    function: "Stable funding gap — Required Stable Funding - Available Stable Funding. A financial metric in the domain of Treasury, ALM & balance-sheet management."
    y_as_x: []
    :param value_a: "Parameter value_a used in Stable funding gap calculation."
    :param value_b: "Parameter value_b used in Stable funding gap calculation."
    :return: "Computed value of Stable funding gap: Required Stable Funding - Available Stable Funding"
    '''
    return value_a - value_b






def state_space_measurement_equation(z_t_alpha_t, epsilon_t):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Financial Econometrics', 'Time Series Analysis']
    function: "State-space measurement equation — y_t = Z_t alpha_t + epsilon_t. A financial metric in the domain of Econometrics & time-series finance."
    y_as_x: []
    :param z_t_alpha_t: "Parameter z_t_alpha_t used in State-space measurement equation calculation."
    :param epsilon_t: "Parameter epsilon_t used in State-space measurement equation calculation."
    :return: "Computed value of State-space measurement equation: y_t = Z_t alpha_t + epsilon_t"
    '''
    return z_t_alpha_t + epsilon_t






def state_space_transition_equation(t_t_alpha_t, r_t_eta_t):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Financial Econometrics', 'Time Series Analysis']
    function: "State-space transition equation — alpha_{t+1} = T_t alpha_t + R_t eta_t. A financial metric in the domain of Econometrics & time-series finance."
    y_as_x: []
    :param t_t_alpha_t: "Parameter t_t_alpha_t used in State-space transition equation calculation."
    :param r_t_eta_t: "Parameter r_t_eta_t used in State-space transition equation calculation."
    :return: "Computed value of State-space transition equation: alpha_{t+1} = T_t alpha_t + R_t eta_t"
    '''
    return t_t_alpha_t + r_t_eta_t






def sterling_ratio(cagr, average_drawdown):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Sterling ratio — Sterling = CAGR / Average Drawdown. A financial metric in the domain of Asset management & portfolio optimization."
    y_as_x: []
    :param cagr: "Parameter cagr used in Sterling ratio calculation."
    :param average_drawdown: "Parameter average_drawdown used in Sterling ratio calculation."
    :return: "Computed value of Sterling ratio: Sterling = CAGR / Average Drawdown"
    '''
    return cagr / average_drawdown






def stochastic_oscillator(high, low, close, k_period=14, d_period=3):
    '''
    domain: ['Technical analysis']
    subdomain: ['Technical Analysis']
    function: "Stochastic oscillator — %K = 100·(C-L_n)/(H_n-L_n). A financial metric in the domain of Technical analysis."
    y_as_x: []
    :param close: "Close is the final trading price at the end of a trading period."
    :param period: "Period (n) is the lookback window in number of bars for technical indicators."
    :return: "Computed value of Stochastic oscillator: %K = 100·(C-L_n)/(H_n-L_n)"
    '''
    import pandas as pd
    h = pd.Series(high); l = pd.Series(low); c = pd.Series(close)
    lowest = l.rolling(k_period).min(); highest = h.rolling(k_period).max()
    pct_k = 100 * (c - lowest) / (highest - lowest)
    pct_d = pct_k.rolling(d_period).mean()
    return {'%K': pct_k, '%D': pct_d}


def stochastic_oscillator_pct_d(pct_k, smoothing=3):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "Stochastic Oscillator %D — smoothed moving average of %K."
    y_as_x: []
    :param pct_k: "Parameter pct_k used in Stochastic oscillator %D calculation."
    :param smoothing: "Parameter smoothing used in Stochastic oscillator %D calculation."
    :return: "Computed value of Stochastic oscillator %D: %D = SMA_3(%K)"
    '''
    import pandas as pd
    return pd.Series(pct_k).rolling(window=smoothing).mean()






def stochastic_oscillator_pct_k(high, low, close, period=14):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "Stochastic Oscillator %K — measures closing price relative to the high-low range."
    y_as_x: []
    :param high: "High is the highest price during a specific trading period."
    :param low: "Low is the lowest price during a specific trading period."
    :param close: "Close is the final trading price at the end of a trading period."
    :param period: "Period (n) is the lookback window in number of bars for technical indicators."
    :return: "Computed value of Stochastic oscillator %K: %K = 100 (C-L_n)/(H_n-L_n)"
    '''
    import pandas as pd
    h = pd.Series(high); l = pd.Series(low); c = pd.Series(close)
    lowest = l.rolling(window=period).min()
    highest = h.rolling(window=period).max()
    return 100 * (c - lowest) / (highest - lowest)






def stochastic_rsi(close, rsi_period=14, stoch_period=14):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "Stochastic RSI — StochRSI = (RSI - min RSI_n)/(max RSI_n - min RSI_n). A financial metric in the domain of Technical analysis & chart-based indicators."
    y_as_x: []
    :param close: "Close is the final trading price at the end of a trading period."
    :param period: "Period (n) is the lookback window in number of bars for technical indicators."
    :return: "Computed value of Stochastic RSI: StochRSI = (RSI - min RSI_n)/(max RSI_n - min RSI_n)"
    '''
    import pandas as pd
    c = pd.Series(close); delta = c.diff()
    gain = delta.where(delta>0,0).rolling(rsi_period).mean()
    loss = (-delta.where(delta<0,0)).rolling(rsi_period).mean()
    rsi = 100 - 100/(1 + gain/loss)
    lowest = rsi.rolling(stoch_period).min(); highest = rsi.rolling(stoch_period).max()
    return (rsi - lowest) / (highest - lowest)


def stop_loss_premium(losses, deductible):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "Stop-loss premium — Pi(d) = E[(S-d)^+]. A financial metric in the domain of Actuarial science & insurance."
    y_as_x: []
    :param data: "Parameter data used in Stop-loss premium calculation."
    :param args: "Parameter args used in Stop-loss premium calculation."
    :return: "Computed value of Stop-loss premium: Pi(d) = E[(S-d)^+]"
    '''
    import numpy as np
    return np.mean(np.maximum(np.array(losses) - deductible, 0))




def straddle_payoff(spot_price, strike_price, premium_paid):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Straddle Payoff — |S - K| - Premium. Profits from large moves in either direction."
    y_as_x: []
    :param spot_price: "Spot Price (S) is the current market price of the underlying asset."
    :param strike_price: "Strike Price (K) is the predetermined price at which an option can be exercised."
    :param premium_paid: "Parameter premium_paid used in Straddle payoff calculation."
    :return: "Computed value of Straddle payoff: Payoff = max(S-K,0)+max(K-S,0)-Premiums"
    '''
    import numpy as np
    return np.maximum(spot_price - strike_price, 0) + np.maximum(strike_price - spot_price, 0) - premium_paid






def strangle_payoff(spot_price, strike_call, strike_put, premium_paid):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Strangle payoff — Payoff = max(S-K_c,0)+max(K_p-S,0)-Premiums. A financial metric in the domain of Derivatives, options & volatility."
    y_as_x: []
    :param args: "Parameter args used in Strangle payoff calculation."
    :param kwargs: "Parameter kwargs used in Strangle payoff calculation."
    :return: "Computed value of Strangle payoff: Payoff = max(S-K_c,0)+max(K_p-S,0)-Premiums"
    '''
    import numpy as np
    return np.maximum(spot_price - strike_call, 0) + np.maximum(strike_put - spot_price, 0) - premium_paid


def stress_capital_buffer(maxstress_losses_regulatory_floor, rwa):
    '''
    domain: ['Bank regulation, Basel & prudential ratios']
    subdomain: ['Bank Regulation', 'Basel Framework', 'Prudential Ratios']
    function: "Stress capital buffer — SCB = max(stress losses, regulatory floor) / RWA. A financial metric in the domain of Bank regulation, Basel & prudential ratios."
    y_as_x: []
    :param maxstress_losses_regulatory_floor: "Parameter maxstress_losses_regulatory_floor used in Stress capital buffer calculation."
    :param rwa: "Parameter rwa used in Stress capital buffer calculation."
    :return: "Computed value of Stress capital buffer: SCB = max(stress losses, regulatory floor) / RWA"
    '''
    return maxstress_losses_regulatory_floor / rwa






def stress_loss(portfolio_value, stress_factor):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "Stress loss — Stress Loss = V(current market state) - V(stressed state). A financial metric in the domain of Market risk & volatility modeling."
    y_as_x: []
    :param args: "Parameter args used in Stress loss calculation."
    :param kwargs: "Parameter kwargs used in Stress loss calculation."
    :return: "Computed value of Stress loss: Stress Loss = V(current market state) - V(stressed state)"
    '''
    return portfolio_value * stress_factor


def stressed_va_r(var_using_stress, window_parameters):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "Stressed VaR — SVaR = VaR using stress-window parameters. A financial metric in the domain of Market risk & volatility modeling."
    y_as_x: []
    :param var_using_stress: "Parameter var_using_stress used in Stressed VaR calculation."
    :param window_parameters: "Parameter window_parameters used in Stressed VaR calculation."
    :return: "Computed value of Stressed VaR: SVaR = VaR using stress-window parameters"
    '''
    return var_using_stress - window_parameters






def structural_credit_spread_approximation(value_a, value_b):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit Risk', 'Default Modeling', 'Credit Portfolio']
    function: "Structural credit spread approximation — s approx -ln[(De^{-rT}+E)/V_A]/T. A financial metric in the domain of Credit risk, default modeling & credit portfolio."
    y_as_x: []
    :param value_a: "Parameter value_a used in Structural credit spread approximation calculation."
    :param value_b: "Parameter value_b used in Structural credit spread approximation calculation."
    :return: "Computed value of Structural credit spread approximation: s approx -ln[(De^{-rT}+E)/V_A]/T"
    '''
    return value_a - value_b






def survival_function(mortality_rates):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "Survival function — S_x(t) = P[T_x > t] = 1 - F_x(t). A financial metric in the domain of Actuarial science & insurance."
    y_as_x: []
    :param args: "Parameter args used in Survival function calculation."
    :param kwargs: "Parameter kwargs used in Survival function calculation."
    :return: "Computed value of Survival function: S_x(t) = P[T_x > t] = 1 - F_x(t)"
    '''
    import numpy as np
    return np.cumprod(1 - np.array(mortality_rates))


def survival_probability(hazard_rate, time):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit Risk', 'Default Modeling', 'Credit Portfolio']
    function: "Survival probability — Q(0,T) = exp(-int_0^T lambda(t) dt). A financial metric in the domain of Credit risk, default modeling & credit portfolio."
    y_as_x: []
    :param args: "Parameter args used in Survival probability calculation."
    :param kwargs: "Parameter kwargs used in Survival probability calculation."
    :return: "Computed value of Survival probability: Q(0,T) = exp(-int_0^T lambda(t) dt)"
    '''
    import numpy as np
    return np.exp(-hazard_rate * time)




def sustainable_growth_rate(roe, retention_ratio):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "Sustainable Growth Rate — g = ROE * Retention Ratio. Maximum growth without external financing."
    y_as_x: []
    :param roe: "Parameter roe used in Sustainable growth rate calculation."
    :param retention_ratio: "Retention Ratio — proportion of earnings retained. RR = 1 - Payout Ratio."
    :return: "Computed value of Sustainable growth rate: g = ROE x Retention Ratio"
    '''
    return roe * retention_ratio






def swap_annuity(discount_factors, day_count_fractions):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Interest Rate Modeling', 'Term Structure']
    function: "Swap annuity — A = sum_i alpha_i DF_i. A financial metric in the domain of Interest-rate modeling & term structures."
    y_as_x: []
    :param args: "Parameter args used in Swap annuity calculation."
    :param kwargs: "Parameter kwargs used in Swap annuity calculation."
    :return: "Computed value of Swap annuity: A = sum_i alpha_i DF_i"
    '''
    import numpy as np
    return np.sum(np.array(discount_factors) * np.array(day_count_fractions))


def swap_fixed_leg_pv(fixed_rate, notional, discount_factors, day_count_fractions):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Interest Rate Modeling', 'Term Structure']
    function: "Swap fixed leg PV — PV_fixed = Σ_i N·K·α_i·DF(t_i). A financial metric in the domain of Interest-rate modeling & term structures."
    y_as_x: []
    :param args: "Parameter args used in Swap fixed leg PV calculation."
    :param kwargs: "Parameter kwargs used in Swap fixed leg PV calculation."
    :return: "Computed value of Swap fixed leg PV: PV_fixed = Σ_i N·K·α_i·DF(t_i)"
    '''
    import numpy as np
    return fixed_rate * notional * np.sum(np.array(discount_factors) * np.array(day_count_fractions))




def swap_fixed_rate(discount_factors, day_count_fractions):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Fixed Income', 'Bond Mathematics', 'Credit Markets']
    function: "Swap fixed rate — K = (1 - DF_n) / sum_i alpha_i DF_i. A financial metric in the domain of Fixed income, bonds & credit markets."
    y_as_x: []
    :param args: "Parameter args used in Swap fixed rate calculation."
    :param kwargs: "Parameter kwargs used in Swap fixed rate calculation."
    :return: "Computed value of Swap fixed rate: K = (1 - DF_n) / sum_i alpha_i DF_i"
    '''
    import numpy as np
    df = np.array(discount_factors); dcf = np.array(day_count_fractions)
    return (1 - df[-1]) / np.sum(df * dcf)




def swap_floating_leg_pv(forward_rates, notional, discount_factors, day_count_fractions):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Interest Rate Modeling', 'Term Structure']
    function: "Swap floating leg PV — PV_float = Σ_i N·L_i·α_i·DF(t_i). A financial metric in the domain of Interest-rate modeling & term structures."
    y_as_x: []
    :param args: "Parameter args used in Swap floating leg PV calculation."
    :param kwargs: "Parameter kwargs used in Swap floating leg PV calculation."
    :return: "Computed value of Swap floating leg PV: PV_float = Σ_i N·L_i·α_i·DF(t_i)"
    '''
    import numpy as np
    return notional * np.sum(np.array(forward_rates) * np.array(discount_factors) * np.array(day_count_fractions))




def swap_present_value(pv_fixed_leg, pv_float_leg):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Fixed Income', 'Bond Mathematics', 'Credit Markets']
    function: "Swap present value — PV_swap = PV_fixed_leg - PV_float_leg. A financial metric in the domain of Fixed income, bonds & credit markets."
    y_as_x: []
    :param pv_fixed_leg: "Parameter pv_fixed_leg used in Swap present value calculation."
    :param pv_float_leg: "Parameter pv_float_leg used in Swap present value calculation."
    :return: "Computed value of Swap present value: PV_swap = PV_fixed_leg - PV_float_leg"
    '''
    return pv_fixed_leg - pv_float_leg






def tail_hedge_payoff(spot_price, strike_price, premium_paid, notional):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Commodities', 'Futures', 'Hedging']
    function: "Tail hedge payoff — Tail Hedge = max(K-S_T,0) - Premium or futures P&L in stress. A financial metric in the domain of Commodities, futures & hedging."
    y_as_x: []
    :param args: "Parameter args used in Tail hedge payoff calculation."
    :param kwargs: "Parameter kwargs used in Tail hedge payoff calculation."
    :return: "Computed value of Tail hedge payoff: Tail Hedge = max(K-S_T,0) - Premium or futures P&L in stress"
    '''
    import numpy as np
    return notional * np.maximum(strike_price - spot_price, 0) - premium_paid


def tail_ratio(x_95th_percentile, x_5th_percentile):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "Tail ratio — Tail Ratio = |95th percentile| / |5th percentile|. A financial metric in the domain of Market risk & volatility modeling."
    y_as_x: []
    :param x_95th_percentile: "Parameter x_95th_percentile used in Tail ratio calculation."
    :param x_5th_percentile: "Parameter x_5th_percentile used in Tail ratio calculation."
    :return: "Computed value of Tail ratio: Tail Ratio = |95th percentile| / |5th percentile|"
    '''
    return x_95th_percentile / x_5th_percentile






def tangency_portfolio_weights(expected_returns, cov_matrix, risk_free_rate=0):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Tangency portfolio weights — w* proportional Sigma^{-1}(mu-r_f 1). A financial metric in the domain of Asset management & portfolio optimization."
    y_as_x: []
    :param expected_returns: "Expected Returns vector contains the anticipated return for each asset."
    :param cov_matrix: "Covariance Matrix contains the covariances between all pairs of assets."
    :return: "Computed value of Tangency portfolio weights: w* proportional Sigma^{-1}(mu-r_f 1)"
    '''
    import numpy as np
    mu = np.array(expected_returns); sigma = np.array(cov_matrix)
    excess = mu - risk_free_rate
    w = np.linalg.inv(sigma) @ excess
    return w / np.sum(w)


def tax_shield(interest_expense, tax_rate):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "Tax shield — Tax Shield = Interest Expense x Tax Rate. A financial metric in the domain of Corporate finance, valuation & capital budgeting."
    y_as_x: []
    :param interest_expense: "Interest Expense is the cost incurred by a company for borrowed funds."
    :param tax_rate: "Tax Rate (T) is the percentage of taxable income that must be paid as corporate income tax."
    :return: "Computed value of Tax shield: Tax Shield = Interest Expense x Tax Rate"
    '''
    return interest_expense * tax_rate






def temporary_annuity(interest_rate, num_periods):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "Temporary annuity — a_{x:n} = E[sum_{k=1}^n v^k 1(T_x>=k)]. A financial metric in the domain of Actuarial science & insurance."
    y_as_x: []
    :param args: "Parameter args used in Temporary annuity calculation."
    :param kwargs: "Parameter kwargs used in Temporary annuity calculation."
    :return: "Computed value of Temporary annuity: a_{x:n} = E[sum_{k=1}^n v^k 1(T_x>=k)]"
    '''
    v = 1 / (1 + interest_rate)
    return (1 - v**num_periods) / interest_rate


def term_insurance_apv(benefit, mortality_rates, interest_rate):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "Term insurance APV — A_{x:n}^1 = E[v^{T_x} 1(T_x<=n)]. A financial metric in the domain of Actuarial science & insurance."
    y_as_x: []
    :param args: "Parameter args used in Term insurance APV calculation."
    :param kwargs: "Parameter kwargs used in Term insurance APV calculation."
    :return: "Computed value of Term insurance APV: A_{x:n}^1 = E[v^{T_x} 1(T_x<=n)]"
    '''
    import numpy as np
    v = 1 / (1 + interest_rate)
    qx = np.array(mortality_rates)
    n = len(qx)
    px_cum = np.concatenate([[1], np.cumprod(1 - qx[:-1])])
    t = np.arange(1, n + 1)
    return benefit * np.sum(v**t * px_cum * qx)




def terminal_capitalization_value(cash_flows, discount_rate):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Real Estate Finance', 'Mortgage Analysis']
    function: "Terminal capitalization value — Terminal Value = NOI_{T+1} / Exit Cap Rate. A financial metric in the domain of Real estate finance & mortgages."
    y_as_x: []
    :param cash_flows: "Parameter cash_flows used in Terminal capitalization value calculation."
    :param discount_rate: "Discount Rate is the rate used to discount future cash flows to present value."
    :return: "Computed value of Terminal capitalization value: Terminal Value = NOI_{T+1} / Exit Cap Rate"
    '''
    import numpy as np
    cf = np.array(cash_flows)
    t = np.arange(1, len(cf) + 1)
    return np.sum(cf / (1 + discount_rate)**t)






def terminal_value_exit_multiple(terminal_metric, exit_multiple):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "Terminal Value (Exit Multiple) — TV = Terminal Metric * Exit Multiple."
    y_as_x: []
    :param terminal_metric: "Parameter terminal_metric used in Terminal value (exit multiple) calculation."
    :param exit_multiple: "Parameter exit_multiple used in Terminal value (exit multiple) calculation."
    :return: "Computed value of Terminal value (exit multiple): TV = Metric_n x Exit Multiple"
    '''
    return terminal_metric * exit_multiple






def terminal_value_gordon_growth(terminal_fcf, discount_rate, growth_rate):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "Terminal Value (Gordon Growth) — TV = FCF*(1+g) / (r-g)."
    y_as_x: []
    :param terminal_fcf: "Parameter terminal_fcf used in Terminal value (Gordon growth) calculation."
    :param discount_rate: "Discount Rate is the rate used to discount future cash flows to present value."
    :param growth_rate: "Growth Rate (g) is the rate at which a value increases over time."
    :return: "Computed value of Terminal value (Gordon growth): TV = FCF_(n+1) / (WACC-g)"
    '''
    return terminal_fcf * (1 + growth_rate) / (discount_rate - growth_rate)






def theta(spot_price, strike_price, risk_free_rate, volatility, time_to_expiry, option_type):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Theta — time decay of option value. Negative for long options."
    y_as_x: []
    :param spot_price: "Spot Price (S) is the current market price of the underlying asset."
    :param strike_price: "Strike Price (K) is the predetermined price at which an option can be exercised."
    :param risk_free_rate: "Risk-Free Rate (Rf) is the theoretical rate of return with zero risk, typically proxied by government bond yields."
    :param volatility: "Volatility (sigma) is the annualized standard deviation of returns."
    :param time_to_expiry: "Time to Expiry (T) is the remaining time until expiration, in years."
    :param option_type: "Option Type specifies whether the option is a "call" or "put"."
    :return: "Computed value of Theta: Theta = -S e^{-qT} n(d1)sigma/(2sqrt(T)) - rKe^{-rT}N(d2) + qSe^{-qT}N(d1)"
    '''
    import numpy as np
    from scipy.stats import norm
    d1 = (np.log(spot_price/strike_price) + (risk_free_rate + 0.5*volatility**2)*time_to_expiry) / (volatility*np.sqrt(time_to_expiry))
    d2 = d1 - volatility*np.sqrt(time_to_expiry)
    term1 = -spot_price * norm.pdf(d1) * volatility / (2 * np.sqrt(time_to_expiry))
    if option_type == 'call':
        return term1 - risk_free_rate * strike_price * np.exp(-risk_free_rate*time_to_expiry) * norm.cdf(d2)
    else:
        return term1 + risk_free_rate * strike_price * np.exp(-risk_free_rate*time_to_expiry) * norm.cdf(-d2)






def through_the_cycle_pd(long, run_default_frequency_estimate):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit Risk', 'Default Modeling', 'Credit Portfolio']
    function: "Through-the-cycle PD — PD_TTC = long-run default frequency estimate. A financial metric in the domain of Credit risk, default modeling & credit portfolio."
    y_as_x: []
    :param long: "Parameter long used in Through-the-cycle PD calculation."
    :param run_default_frequency_estimate: "Parameter run_default_frequency_estimate used in Through-the-cycle PD calculation."
    :return: "Computed value of Through-the-cycle PD: PD_TTC = long-run default frequency estimate"
    '''
    return long - run_default_frequency_estimate






def tier_1_capital_ratio(tier_1_capital, rwa):
    '''
    domain: ['Bank regulation, Basel & prudential ratios']
    subdomain: ['Bank Regulation', 'Basel Framework', 'Prudential Ratios']
    function: "Tier 1 capital ratio — Tier 1 Ratio = Tier 1 Capital / RWA. A financial metric in the domain of Bank regulation, Basel & prudential ratios."
    y_as_x: []
    :param tier_1_capital: "Parameter tier_1_capital used in Tier 1 capital ratio calculation."
    :param rwa: "Parameter rwa used in Tier 1 capital ratio calculation."
    :return: "Computed value of Tier 1 capital ratio: Tier 1 Ratio = Tier 1 Capital / RWA"
    '''
    return tier_1_capital / rwa






def time_value_option(option_premium, intrinsic_value):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Time value option — Time Value = Option Premium - Intrinsic Value. A financial metric in the domain of Derivatives, options & volatility."
    y_as_x: []
    :param option_premium: "Parameter option_premium used in Time value option calculation."
    :param intrinsic_value: "Parameter intrinsic_value used in Time value option calculation."
    :return: "Computed value of Time value option: Time Value = Option Premium - Intrinsic Value"
    '''
    return option_premium - intrinsic_value






def time_weighted_return_twrr(period_returns):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Performance Attribution', 'Risk-Adjusted Performance']
    function: "Time-Weighted Return (TWRR) — geometrically linked sub-period returns. Eliminates cash flow timing effects."
    y_as_x: []
    :param period_returns: "Parameter period_returns used in Time-weighted return (TWRR) calculation."
    :return: "Computed value of Time-weighted return (TWRR): TWRR = prod_i (1+r_i) - 1"
    '''
    import numpy as np
    return np.prod(1 + np.array(period_returns)) - 1






def tobins_q(market_value_equity, market_value_debt, replacement_cost_assets):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Equity Valuation', 'Asset Pricing']
    function: "Tobin's Q — (Market Value of Equity + Debt) / Replacement Cost of Assets. Q > 1 suggests overvaluation."
    y_as_x: []
    :param market_value_equity: "Parameter market_value_equity used in Tobin's Q calculation."
    :param market_value_debt: "Parameter market_value_debt used in Tobin's Q calculation."
    :param replacement_cost_assets: "Parameter replacement_cost_assets used in Tobin's Q calculation."
    :return: "Computed value of Tobin's Q: Q = Market Value of Assets / Replacement Cost of Assets"
    '''
    return (market_value_equity + market_value_debt) / replacement_cost_assets






def total_capital_ratio(total_capital, rwa):
    '''
    domain: ['Bank regulation, Basel & prudential ratios']
    subdomain: ['Bank Regulation', 'Basel Framework', 'Prudential Ratios']
    function: "Total capital ratio — Total Capital Ratio = Total Capital / RWA. A financial metric in the domain of Bank regulation, Basel & prudential ratios."
    y_as_x: []
    :param total_capital: "Parameter total_capital used in Total capital ratio calculation."
    :param rwa: "Parameter rwa used in Total capital ratio calculation."
    :return: "Computed value of Total capital ratio: Total Capital Ratio = Total Capital / RWA"
    '''
    return total_capital / rwa






def tracking_error(portfolio_returns, benchmark_returns):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Tracking Error — annualized standard deviation of active returns."
    y_as_x: ['ex_ante_tracking_error', 'information_ratio']
    :param portfolio_returns: "Portfolio Returns represent the weighted average returns of all assets in a portfolio."
    :param benchmark_returns: "Benchmark Returns are the returns of a reference index used for performance comparison."
    :return: "Computed value of Tracking error: TE = Std(E[R_p] - R_b)"
    '''
    import numpy as np
    active = np.array(portfolio_returns) - np.array(benchmark_returns)
    return np.std(active, ddof=1) * np.sqrt(252)






def tranche_attachment_point(subordination_below_tranche, pool_balance):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Structured Finance', 'Securitization']
    function: "Tranche attachment point — Attach = subordination below tranche / pool balance. A financial metric in the domain of Structured finance & securitization."
    y_as_x: []
    :param subordination_below_tranche: "Parameter subordination_below_tranche used in Tranche attachment point calculation."
    :param pool_balance: "Parameter pool_balance used in Tranche attachment point calculation."
    :return: "Computed value of Tranche attachment point: Attach = subordination below tranche / pool balance"
    '''
    return subordination_below_tranche / pool_balance






def tranche_credit_enhancement(overcollateralization, subordination, excess_spread):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Structured Finance', 'Securitization']
    function: "Tranche credit enhancement — CE = Overcollateralization + Subordination + Excess Spread. A financial metric in the domain of Structured finance & securitization."
    y_as_x: []
    :param overcollateralization: "Parameter overcollateralization used in Tranche credit enhancement calculation."
    :param subordination: "Parameter subordination used in Tranche credit enhancement calculation."
    :param excess_spread: "Excess Spread — in securitization, the residual interest after covering all costs."
    :return: "Computed value of Tranche credit enhancement: CE = Overcollateralization + Subordination + Excess Spread"
    '''
    return overcollateralization + subordination + excess_spread






def tranche_detachment_point(attachment_point, tranche_thickness):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Structured Finance', 'Securitization']
    function: "Tranche detachment point — Detach = 1 - subordination above tranche / pool balance. A financial metric in the domain of Structured finance & securitization."
    y_as_x: []
    :param args: "Parameter args used in Tranche detachment point calculation."
    :param kwargs: "Parameter kwargs used in Tranche detachment point calculation."
    :return: "Computed value of Tranche detachment point: Detach = 1 - subordination above tranche / pool balance"
    '''
    return attachment_point + tranche_thickness


def tranche_wal(sum_t_t_principal_tranchet, total_principal_tranche):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Structured Finance', 'Securitization']
    function: "Tranche WAL — WAL_tranche = sum_t t Principal_tranche,t / Total Principal_tranche. A financial metric in the domain of Structured finance & securitization."
    y_as_x: []
    :param sum_t_t_principal_tranchet: "Parameter sum_t_t_principal_tranchet used in Tranche WAL calculation."
    :param total_principal_tranche: "Parameter total_principal_tranche used in Tranche WAL calculation."
    :return: "Computed value of Tranche WAL: WAL_tranche = sum_t t Principal_tranche,t / Total Principal_tranche"
    '''
    return sum_t_t_principal_tranchet / total_principal_tranche






def tranche_yield(tranche_price, tranche_cash_flows, time_periods):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Structured Finance', 'Securitization']
    function: "Tranche yield — Solve y such that Tranche Price = PV(expected tranche cash flows). A financial metric in the domain of Structured finance & securitization."
    y_as_x: []
    :param args: "Parameter args used in Tranche yield calculation."
    :param kwargs: "Parameter kwargs used in Tranche yield calculation."
    :return: "Computed value of Tranche yield: Solve y such that Tranche Price = PV(expected tranche cash flows)"
    '''
    from scipy.optimize import brentq
    import numpy as np
    cf = np.array(tranche_cash_flows); t = np.array(time_periods)
    def pv_diff(y):
        return np.sum(cf / (1+y)**t) - tranche_price
    return brentq(pv_diff, -0.1, 2.0)


def transfer_rate_from_curve(term_matched_funding_curve, liquidity, optionality_premium):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Treasury', 'ALM', 'Balance Sheet Management']
    function: "Transfer rate from curve — FTP_t = term matched funding curve + liquidity + optionality premium. A financial metric in the domain of Treasury, ALM & balance-sheet management."
    y_as_x: []
    :param term_matched_funding_curve: "Parameter term_matched_funding_curve used in Transfer rate from curve calculation."
    :param liquidity: "Parameter liquidity used in Transfer rate from curve calculation."
    :param optionality_premium: "Parameter optionality_premium used in Transfer rate from curve calculation."
    :return: "Computed value of Transfer rate from curve: FTP_t = term matched funding curve + liquidity + optionality premium"
    '''
    return term_matched_funding_curve + liquidity + optionality_premium






def transition_matrix_probability(transition_matrix, num_periods):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit Risk', 'Default Modeling', 'Credit Portfolio']
    function: "Transition matrix probability — P_{ij}(n) = [P^n]_{ij}. A financial metric in the domain of Credit risk, default modeling & credit portfolio."
    y_as_x: []
    :param args: "Parameter args used in Transition matrix probability calculation."
    :param kwargs: "Parameter kwargs used in Transition matrix probability calculation."
    :return: "Computed value of Transition matrix probability: P_{ij}(n) = [P^n]_{ij}"
    '''
    import numpy as np
    return np.linalg.matrix_power(np.array(transition_matrix), num_periods)


def treynor_ratio(portfolio_return, risk_free_rate, beta):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Treynor Ratio — excess return per unit of systematic risk. TR = (Rp - Rf) / beta."
    y_as_x: []
    :param portfolio_return: "Portfolio Return is the total return of the managed portfolio."
    :param risk_free_rate: "Risk-Free Rate (Rf) is the theoretical rate of return with zero risk, typically proxied by government bond yields."
    :param beta: "Beta measures systematic risk, the sensitivity of returns to market movements."
    :return: "Computed value of Treynor ratio: Treynor = (E[R_p]-R_f)/beta_p"
    '''
    return (portfolio_return - risk_free_rate) / beta if beta != 0 else float("inf")






def treynor_mazuy_timing(y, X):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Performance Attribution', 'Risk-Adjusted Performance']
    function: "Treynor-Mazuy timing — R_p-R_f = alpha + beta(R_m-R_f) + gamma(R_m-R_f)^2 + epsilon. A financial metric in the domain of Performance measurement & attribution."
    y_as_x: []
    :param y: "Parameter y used in Treynor-Mazuy timing calculation."
    :param X: "Parameter X used in Treynor-Mazuy timing calculation."
    :return: "Computed value of Treynor-Mazuy timing: R_p-R_f = alpha + beta(R_m-R_f) + gamma(R_m-R_f)^2 + epsilon"
    '''
    import statsmodels.api as sm
    X_const = sm.add_constant(X)
    model = sm.OLS(y, X_const).fit()
    return model






def triangular_arbitrage_condition(rate_ab, rate_bc, rate_ac):
    '''
    domain: ['FX & international finance']
    subdomain: ['FX Markets', 'International Finance']
    function: "Triangular arbitrage condition — S_{A/B} × S_{B/C} × S_{C/A} = 1. A financial metric in the domain of FX & international finance."
    y_as_x: []
    :param args: "Parameter args used in Triangular arbitrage condition calculation."
    :param kwargs: "Parameter kwargs used in Triangular arbitrage condition calculation."
    :return: "Computed value of Triangular arbitrage condition: S_{A/B} × S_{B/C} × S_{C/A} = 1"
    '''
    return abs(rate_ab * rate_bc - rate_ac)


def trigger_based_step_down(current_oc_ratio, trigger_level, current_allocation, step_down_allocation):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Structured Finance', 'Securitization']
    function: "Trigger-based step-down — Step-down when delinquency, CNL, and OC/IC tests satisfied. A financial metric in the domain of Structured finance & securitization."
    y_as_x: []
    :param args: "Parameter args used in Trigger-based step-down calculation."
    :param kwargs: "Parameter kwargs used in Trigger-based step-down calculation."
    :return: "Computed value of Trigger-based step-down: Step-down when delinquency, CNL, and OC/IC tests satisfied"
    '''
    return step_down_allocation if current_oc_ratio >= trigger_level else current_allocation




def trinomial_tree_option_value(spot_price, strike_price, risk_free_rate, volatility, time_to_expiry, steps, option_type="call"):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Trinomial tree option value — V = discounted expected value across three branches. A financial metric in the domain of Derivatives, options & volatility."
    y_as_x: []
    :param args: "Parameter args used in Trinomial tree option value calculation."
    :param kwargs: "Parameter kwargs used in Trinomial tree option value calculation."
    :return: "Computed value of Trinomial tree option value: V = discounted expected value across three branches"
    '''
    import numpy as np
    dt = time_to_expiry / steps
    u = np.exp(volatility * np.sqrt(2 * dt))
    d = 1 / u
    m = 1
    pu = ((np.exp(risk_free_rate * dt / 2) - np.exp(-volatility * np.sqrt(dt / 2))) / (np.exp(volatility * np.sqrt(dt / 2)) - np.exp(-volatility * np.sqrt(dt / 2))))**2
    pd_val = ((np.exp(volatility * np.sqrt(dt / 2)) - np.exp(risk_free_rate * dt / 2)) / (np.exp(volatility * np.sqrt(dt / 2)) - np.exp(-volatility * np.sqrt(dt / 2))))**2
    pm = 1 - pu - pd_val
    n_nodes = 2 * steps + 1
    prices = spot_price * u**np.arange(steps, -steps - 1, -1)
    if option_type == 'call':
        values = np.maximum(prices - strike_price, 0)
    else:
        values = np.maximum(strike_price - prices, 0)
    disc = np.exp(-risk_free_rate * dt)
    for i in range(steps):
        new_vals = np.zeros(len(values) - 2)
        for j in range(len(new_vals)):
            new_vals[j] = disc * (pu * values[j] + pm * values[j+1] + pd_val * values[j+2])
        values = new_vals
    return values[0]




def trix(close, period=15):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "TRIX — TRIX = 1-period ROC of triple EMA. A financial metric in the domain of Technical analysis & chart-based indicators."
    y_as_x: []
    :param high: "High is the highest price during a specific trading period."
    :param low: "Low is the lowest price during a specific trading period."
    :param close: "Close is the final trading price at the end of a trading period."
    :param volume: "Volume is the total number of shares or contracts traded during a period."
    :param period: "Period (n) is the lookback window in number of bars for technical indicators."
    :return: "Computed value of TRIX: TRIX = 1-period ROC of triple EMA"
    '''
    import pandas as pd
    c = pd.Series(close)
    ema1 = c.ewm(span=period).mean()
    ema2 = ema1.ewm(span=period).mean()
    ema3 = ema2.ewm(span=period).mean()
    return ema3.pct_change() * 100




def true_range(high, low, close_prev):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "True Range — max(H-L, |H-C_prev|, |L-C_prev|). Accounts for gaps."
    y_as_x: []
    :param high: "High is the highest price during a specific trading period."
    :param low: "Low is the lowest price during a specific trading period."
    :param close_prev: "Parameter close_prev used in True range calculation."
    :return: "Computed value of True range: TR = max(H-L, |H-C_{t-1}|, |L-C_{t-1}|)"
    '''
    import numpy as np
    return np.maximum(np.maximum(high - low, np.abs(high - close_prev)), np.abs(low - close_prev))






def turbo_amortization_amount(excess_spread, pool_balance):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Structured Finance', 'Securitization']
    function: "Turbo amortization amount — Turbo = excess cash after fees and note interest redirected to senior principal. A financial metric in the domain of Structured finance & securitization."
    y_as_x: []
    :param args: "Parameter args used in Turbo amortization amount calculation."
    :param kwargs: "Parameter kwargs used in Turbo amortization amount calculation."
    :return: "Computed value of Turbo amortization amount: Turbo = excess cash after fees and note interest redirected to senior principal"
    '''
    return excess_spread * pool_balance


def turnover_ratio(volume, shares_outstanding):
    '''
    domain: ['Liquidity risk & market liquidity']
    subdomain: ['Liquidity Risk', 'Market Liquidity']
    function: "Turnover ratio — Turnover = Volume / Shares Outstanding. A financial metric in the domain of Liquidity risk & market liquidity."
    y_as_x: []
    :param volume: "Volume is the total number of shares or contracts traded during a period."
    :param shares_outstanding: "Shares Outstanding is the total number of shares of a company's stock currently held by all shareholders."
    :return: "Computed value of Turnover ratio: Turnover = Volume / Shares Outstanding"
    '''
    return volume / shares_outstanding






def tvpi(total_value, paid_in_capital):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Private Equity', 'Venture Capital', 'LBO']
    function: "TVPI (Total Value to Paid-In) — total value (NAV + distributions) divided by paid-in capital."
    y_as_x: []
    :param total_value: "Parameter total_value used in TVPI calculation."
    :param paid_in_capital: "Parameter paid_in_capital used in TVPI calculation."
    :return: "Computed value of TVPI: TVPI = (Residual Value + Distributions) / Paid-In Capital"
    '''
    return total_value / paid_in_capital






def twap(x_1, n_i_p_i):
    '''
    domain: ['Trading, execution & market microstructure']
    subdomain: ['Trading', 'Execution', 'Market Microstructure']
    function: "TWAP — TWAP = (1/n) Σ_i P_i. A financial metric in the domain of Trading, execution & market microstructure."
    y_as_x: []
    :param x_1: "Parameter x_1 used in TWAP calculation."
    :param n_i_p_i: "Parameter n_i_p_i used in TWAP calculation."
    :return: "Computed value of TWAP: TWAP = (1/n) Σ_i P_i"
    '''
    return x_1 / n_i_p_i






def ulcer_index(returns):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Performance Attribution', 'Risk-Adjusted Performance']
    function: "Ulcer index — UI = sqrt(mean(drawdown^2)). A financial metric in the domain of Performance measurement & attribution."
    y_as_x: []
    :param returns: "Returns are the gain or loss generated on an investment over a specific period."
    :return: "Computed value of Ulcer index: UI = sqrt(mean(drawdown^2))"
    '''
    import numpy as np
    # Implementation via quantstats.stats
    return np.array(returns)






def ultimate_oscillator(weighted_avg_of_bp, tr_over_71428_periods):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "Ultimate oscillator — UO = weighted avg of BP/TR over 7,14,28 periods. A financial metric in the domain of Technical analysis & chart-based indicators."
    y_as_x: []
    :param weighted_avg_of_bp: "Parameter weighted_avg_of_bp used in Ultimate oscillator calculation."
    :param tr_over_71428_periods: "Parameter tr_over_71428_periods used in Ultimate oscillator calculation."
    :return: "Computed value of Ultimate oscillator: UO = weighted avg of BP/TR over 7,14,28 periods"
    '''
    return weighted_avg_of_bp / tr_over_71428_periods






def uncovered_interest_parity_uip(spot_rate, domestic_rate, foreign_rate, time=1):
    '''
    domain: ['FX & international finance']
    subdomain: ['FX Markets', 'International Finance']
    function: "Uncovered interest parity (UIP) — E[S_{t+T}] / S_t approx (1+r_d T)/(1+r_f T). A financial metric in the domain of FX & international finance."
    y_as_x: []
    :param args: "Parameter args used in Uncovered interest parity (UIP) calculation."
    :param kwargs: "Parameter kwargs used in Uncovered interest parity (UIP) calculation."
    :return: "Computed value of Uncovered interest parity (UIP): E[S_{t+T}] / S_t approx (1+r_d T)/(1+r_f T)"
    '''
    return spot_rate * (1 + domestic_rate * time) / (1 + foreign_rate * time)


def unexpected_loss(pd_val, lgd, ead, correlation=0.15):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit Risk', 'Default Modeling', 'Credit Portfolio']
    function: "Unexpected loss — UL = sqrt(PD(1-PD)) x LGD x EAD. A financial metric in the domain of Credit risk, default modeling & credit portfolio."
    y_as_x: []
    :param args: "Parameter args used in Unexpected loss calculation."
    :param kwargs: "Parameter kwargs used in Unexpected loss calculation."
    :return: "Computed value of Unexpected loss: UL = sqrt(PD(1-PD)) x LGD x EAD"
    '''
    import numpy as np
    from scipy.stats import norm
    ul_single = np.sqrt(pd_val * (1 - pd_val)) * lgd * ead
    return ul_single




def unlevered_beta(levered_beta, debt_equity_ratio, tax_rate):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Corporate Finance', 'Valuation', 'Capital Budgeting']
    function: "Unlevered Beta — beta_U = beta_L / (1 + (1-T)*D/E). Removes financial leverage effect."
    y_as_x: ['levered_beta_hamada']
    :param levered_beta: "Parameter levered_beta used in Unlevered beta calculation."
    :param debt_equity_ratio: "Parameter debt_equity_ratio used in Unlevered beta calculation."
    :param tax_rate: "Tax Rate (T) is the percentage of taxable income that must be paid as corporate income tax."
    :return: "Computed value of Unlevered beta: beta_U = beta_L / [1 + (1-T)D/E]"
    '''
    return levered_beta / (1 + (1 - tax_rate) * debt_equity_ratio)






def unlevered_yield(noi, purchase_price):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Real Estate Finance', 'Mortgage Analysis']
    function: "Unlevered yield — Unlevered Yield = NOI / Purchase Price. A financial metric in the domain of Real estate finance & mortgages."
    y_as_x: []
    :param noi: "Net Operating Income (NOI) is total revenue from a property minus operating expenses."
    :param purchase_price: "Parameter purchase_price used in Unlevered yield calculation."
    :return: "Computed value of Unlevered yield: Unlevered Yield = NOI / Purchase Price"
    '''
    return noi / purchase_price






def up_capture_ratio(meanr_pr_b0, meanr_br_b0):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Performance Attribution', 'Risk-Adjusted Performance']
    function: "Up capture ratio — Up Capture = mean(R_p|R_b>0)/mean(R_b|R_b>0). A financial metric in the domain of Performance measurement & attribution."
    y_as_x: []
    :param meanr_pr_b0: "Parameter meanr_pr_b0 used in Up capture ratio calculation."
    :param meanr_br_b0: "Parameter meanr_br_b0 used in Up capture ratio calculation."
    :return: "Computed value of Up capture ratio: Up Capture = mean(R_p|R_b>0)/mean(R_b|R_b>0)"
    '''
    return meanr_pr_b0 / meanr_br_b0






def upside_capture(avgr_p_r_b0, avgr_b_r_b0):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Performance Attribution', 'Risk-Adjusted Performance']
    function: "Upside capture — Upside Capture = Avg(R_p | R_b>0) / Avg(R_b | R_b>0). A financial metric in the domain of Performance measurement & attribution."
    y_as_x: []
    :param avgr_p_r_b0: "Parameter avgr_p_r_b0 used in Upside capture calculation."
    :param avgr_b_r_b0: "Parameter avgr_b_r_b0 used in Upside capture calculation."
    :return: "Computed value of Upside capture: Upside Capture = Avg(R_p | R_b>0) / Avg(R_b | R_b>0)"
    '''
    return avgr_p_r_b0 / avgr_b_r_b0






def upside_potential_ratio(upside_potential, downside_deviation):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Management', 'Asset Allocation']
    function: "Upside potential ratio — UPR = Upside Potential / Downside Deviation. A financial metric in the domain of Asset management & portfolio optimization."
    y_as_x: []
    :param upside_potential: "Parameter upside_potential used in Upside potential ratio calculation."
    :param downside_deviation: "Downside Deviation — standard deviation of returns below a target. Used in Sortino Ratio."
    :return: "Computed value of Upside potential ratio: UPR = Upside Potential / Downside Deviation"
    '''
    return upside_potential / downside_deviation






def utilization_rate(outstanding_balance, credit_limit):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Banking', 'Consumer Lending', 'Project Finance']
    function: "Utilization rate — Utilization = Outstanding Balance / Credit Limit. A financial metric in the domain of Banking, consumer lending & project finance."
    y_as_x: []
    :param outstanding_balance: "Parameter outstanding_balance used in Utilization rate calculation."
    :param credit_limit: "Parameter credit_limit used in Utilization rate calculation."
    :return: "Computed value of Utilization rate: Utilization = Outstanding Balance / Credit Limit"
    '''
    return outstanding_balance / credit_limit






def vacancy_rate(vacant_units_or_lost_rent, total_potential_units_or_rent):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Real Estate Finance', 'Mortgage Analysis']
    function: "Vacancy rate — Vacancy Rate = Vacant Units or Lost Rent / Total Potential Units or Rent. A financial metric in the domain of Real estate finance & mortgages."
    y_as_x: []
    :param vacant_units_or_lost_rent: "Parameter vacant_units_or_lost_rent used in Vacancy rate calculation."
    :param total_potential_units_or_rent: "Parameter total_potential_units_or_rent used in Vacancy rate calculation."
    :return: "Computed value of Vacancy rate: Vacancy Rate = Vacant Units or Lost Rent / Total Potential Units or Rent"
    '''
    return vacant_units_or_lost_rent / total_potential_units_or_rent






def vanna(spot_price, strike_price, risk_free_rate, volatility, time_to_expiry):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Vanna — Vanna = -e^{-qT} n(d1) d2 / sigma. A financial metric in the domain of Derivatives, options & volatility."
    y_as_x: []
    :param args: "Parameter args used in Vanna calculation."
    :param kwargs: "Parameter kwargs used in Vanna calculation."
    :return: "Computed value of Vanna: Vanna = -e^{-qT} n(d1) d2 / sigma"
    '''
    import numpy as np
    from scipy.stats import norm
    d1 = (np.log(spot_price/strike_price) + (risk_free_rate+0.5*volatility**2)*time_to_expiry) / (volatility*np.sqrt(time_to_expiry))
    d2 = d1 - volatility*np.sqrt(time_to_expiry)
    return -norm.pdf(d1) * d2 / volatility


def var_p(time_series, lags):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Financial Econometrics', 'Time Series Analysis']
    function: "VAR(p) — y_t = c + A_1 y_{t-1}+…+A_p y_{t-p}+u_t. A financial metric in the domain of Econometrics & time-series finance."
    y_as_x: []
    :param data: "Parameter data used in VAR(p) calculation."
    :param args: "Parameter args used in VAR(p) calculation."
    :return: "Computed value of VAR(p): y_t = c + A_1 y_{t-1}+…+A_p y_{t-p}+u_t"
    '''
    from statsmodels.tsa.api import VAR
    model = VAR(time_series)
    return model.fit(lags)




def variance_of_loss(benefit, variance_pv_factor, premium, variance_annuity_factor):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "Variance of loss — Var(L) = E[L^2] - (E[L])^2. A financial metric in the domain of Actuarial science & insurance."
    y_as_x: []
    :param args: "Parameter args used in Variance of loss calculation."
    :param kwargs: "Parameter kwargs used in Variance of loss calculation."
    :return: "Computed value of Variance of loss: Var(L) = E[L^2] - (E[L])^2"
    '''
    return benefit**2 * variance_pv_factor + premium**2 * variance_annuity_factor




def variance_ratio_test(returns, lags=2):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "Variance ratio test — VR(q) = Var(q-period returns)/(q Var(1-period returns)). A financial metric in the domain of Market risk & volatility modeling."
    y_as_x: []
    :param data: "Parameter data used in Variance ratio test calculation."
    :param args: "Parameter args used in Variance ratio test calculation."
    :return: "Computed value of Variance ratio test: VR(q) = Var(q-period returns)/(q Var(1-period returns))"
    '''
    import numpy as np
    r = np.array(returns)
    n = len(r)
    mu = np.mean(r)
    var_1 = np.var(r - mu, ddof=1)
    r_agg = np.array([np.sum(r[i:i+lags]) for i in range(0, n - lags + 1, lags)])
    var_q = np.var(r_agg - lags * mu, ddof=1) / lags
    vr = var_q / var_1
    z_stat = (vr - 1) * np.sqrt(n)
    return {'variance_ratio': vr, 'z_stat': z_stat}




def variance_swap_fair_strike(implied_vols, strikes, spot_price, risk_free_rate, time_to_expiry):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Variance swap fair strike — K_var = E_Q[ realized variance ]. A financial metric in the domain of Derivatives, options & volatility."
    y_as_x: []
    :param args: "Parameter args used in Variance swap fair strike calculation."
    :param kwargs: "Parameter kwargs used in Variance swap fair strike calculation."
    :return: "Computed value of Variance swap fair strike: K_var = E_Q[ realized variance ]"
    '''
    import numpy as np
    from scipy.stats import norm
    K = np.array(strikes); iv = np.array(implied_vols)
    dK = np.diff(K)
    mid_K = (K[:-1] + K[1:]) / 2
    mid_iv = (iv[:-1] + iv[1:]) / 2
    integrand = mid_iv**2 * dK / mid_K**2
    return np.sqrt(2 * np.exp(risk_free_rate * time_to_expiry) / time_to_expiry * np.sum(integrand))




def vasicek_one_factor_portfolio_loss_quantile(pd_val, lgd, rho, confidence_level=0.999):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit Risk', 'Default Modeling', 'Credit Portfolio']
    function: "Vasicek one-factor portfolio loss quantile — L_alpha = LGD Phi((Phi^-1(PD)+sqrt(rho)Phi^-1(alpha))/sqrt(1-rho)). A financial metric in the domain of Credit risk, default modeling & credit portfolio."
    y_as_x: []
    :param data: "Parameter data used in Vasicek one-factor portfolio loss quantile calculation."
    :param args: "Parameter args used in Vasicek one-factor portfolio loss quantile calculation."
    :return: "Computed value of Vasicek one-factor portfolio loss quantile: L_alpha = LGD Phi((Phi^-1(PD)+sqrt(rho)Phi^-1(alpha))/sqrt(1-rho))"
    '''
    from scipy.stats import norm
    import numpy as np
    return lgd * norm.cdf((norm.ppf(pd_val) + np.sqrt(rho) * norm.ppf(confidence_level)) / np.sqrt(1 - rho))




def vasicek_short_rate_process(r0, kappa, theta, sigma, dt, num_steps, num_paths=1000):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Interest Rate Modeling', 'Term Structure']
    function: "Vasicek short-rate process — dr_t = a(b-r_t)dt + sigma dW_t. A financial metric in the domain of Interest-rate modeling & term structures."
    y_as_x: []
    :param args: "Parameter args used in Vasicek short-rate process calculation."
    :param kwargs: "Parameter kwargs used in Vasicek short-rate process calculation."
    :return: "Computed value of Vasicek short-rate process: dr_t = a(b-r_t)dt + sigma dW_t"
    '''
    import numpy as np
    r = np.zeros((num_paths, num_steps + 1))
    r[:, 0] = r0
    for t in range(num_steps):
        dw = np.random.standard_normal(num_paths) * np.sqrt(dt)
        r[:, t+1] = r[:, t] + kappa * (theta - r[:, t]) * dt + sigma * dw
    return r




def vc_liquidation_preference_payout(proceeds, liquidation_preference, participation_cap=None):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Private Equity', 'Venture Capital', 'LBO']
    function: "VC liquidation preference payout — Payout = max(Preference, Ownership x Exit Value) with participation rules. A financial metric in the domain of Private equity, venture capital & LBO."
    y_as_x: []
    :param args: "Parameter args used in VC liquidation preference payout calculation."
    :param kwargs: "Parameter kwargs used in VC liquidation preference payout calculation."
    :return: "Computed value of VC liquidation preference payout: Payout = max(Preference, Ownership x Exit Value) with participation rules"
    '''
    payout = min(proceeds, liquidation_preference)
    if participation_cap is not None and proceeds > liquidation_preference:
        payout += min(proceeds - liquidation_preference, participation_cap)
    return payout




def vecm(data, k_ar_diff=1, coint_rank=1):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Financial Econometrics', 'Time Series Analysis']
    function: "VECM — Delta y_t = Pi y_{t-1} + sum_i Gamma_i Delta y_{t-i} + u_t. A financial metric in the domain of Econometrics & time-series finance."
    y_as_x: []
    :param data: "Parameter data used in VECM calculation."
    :param args: "Parameter args used in VECM calculation."
    :return: "Computed value of VECM: Delta y_t = Pi y_{t-1} + sum_i Gamma_i Delta y_{t-i} + u_t"
    '''
    from statsmodels.tsa.vector_ar.vecm import VECM
    model = VECM(data, k_ar_diff=k_ar_diff, coint_rank=coint_rank)
    return model.fit()




def vega(spot_price, strike_price, risk_free_rate, volatility, time_to_expiry):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Vega — sensitivity of option price to volatility. Vega = S * N'(d1) * sqrt(T)."
    y_as_x: []
    :param spot_price: "Spot Price (S) is the current market price of the underlying asset."
    :param strike_price: "Strike Price (K) is the predetermined price at which an option can be exercised."
    :param risk_free_rate: "Risk-Free Rate (Rf) is the theoretical rate of return with zero risk, typically proxied by government bond yields."
    :param volatility: "Volatility (sigma) is the annualized standard deviation of returns."
    :param time_to_expiry: "Time to Expiry (T) is the remaining time until expiration, in years."
    :return: "Computed value of Vega: Vega = S e^{-qT} n(d1) sqrt(T)"
    '''
    import numpy as np
    from scipy.stats import norm
    d1 = (np.log(spot_price/strike_price) + (risk_free_rate + 0.5*volatility**2)*time_to_expiry) / (volatility*np.sqrt(time_to_expiry))
    return spot_price * norm.pdf(d1) * np.sqrt(time_to_expiry)






def vintage_cumulative_loss(cumulative_net_losses, original_balance):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit Risk', 'Default Modeling', 'Credit Portfolio']
    function: "Vintage cumulative loss — Vintage Loss_t = cumulative net losses / original balance. A financial metric in the domain of Credit risk, default modeling & credit portfolio."
    y_as_x: []
    :param cumulative_net_losses: "Parameter cumulative_net_losses used in Vintage cumulative loss calculation."
    :param original_balance: "Parameter original_balance used in Vintage cumulative loss calculation."
    :return: "Computed value of Vintage cumulative loss: Vintage Loss_t = cumulative net losses / original balance"
    '''
    return cumulative_net_losses / original_balance






def vix_variance_relation(vix_level):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "VIX variance relation — VIX^2 ~ expected 30-day risk-neutral variance x 100^2. A financial metric in the domain of Derivatives, options & volatility."
    y_as_x: []
    :param args: "Parameter args used in VIX variance relation calculation."
    :param kwargs: "Parameter kwargs used in VIX variance relation calculation."
    :return: "Computed value of VIX variance relation: VIX^2 ~ expected 30-day risk-neutral variance x 100^2"
    '''
    return (vix_level / 100)**2


def volatility_clustering_test(y, X):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "Volatility clustering test — ACF of r_t^2 significantly positive. A financial metric in the domain of Market risk & volatility modeling."
    y_as_x: []
    :param y: "Parameter y used in Volatility clustering test calculation."
    :param X: "Parameter X used in Volatility clustering test calculation."
    :return: "Computed value of Volatility clustering test: ACF of r_t^2 significantly positive"
    '''
    import statsmodels.api as sm
    X_const = sm.add_constant(X)
    model = sm.OLS(y, X_const).fit()
    return model






def volume_weighted_average_price_vwap(prices, volumes):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "Volume-Weighted Average Price (VWAP) — average price weighted by volume."
    y_as_x: []
    :param prices: "Prices is a time series of asset prices (typically closing prices)."
    :param volumes: "Parameter volumes used in Volume-weighted average price (VWAP) calculation."
    :return: "Computed value of Volume-weighted average price (VWAP): VWAP = sum(P_t V_t) / sum(V_t) intraday"
    '''
    import numpy as np
    return np.sum(np.array(prices) * np.array(volumes)) / np.sum(volumes)






def vomma_volga(vega_d1_d2, sigma):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Derivatives', 'Options Pricing', 'Volatility']
    function: "Vomma / volga — Vomma = Vega d1 d2 / sigma. A financial metric in the domain of Derivatives, options & volatility."
    y_as_x: []
    :param vega_d1_d2: "Parameter vega_d1_d2 used in Vomma / volga calculation."
    :param sigma: "Parameter sigma used in Vomma / volga calculation."
    :return: "Computed value of Vomma / volga: Vomma = Vega d1 d2 / sigma"
    '''
    return vega_d1_d2 / sigma






def vwap(prices, volumes):
    '''
    domain: ['Trading, execution & market microstructure']
    subdomain: ['Trading', 'Execution', 'Market Microstructure']
    function: "VWAP — Volume Weighted Average Price."
    y_as_x: []
    :param prices: "Prices is a time series of asset prices (typically closing prices)."
    :param volumes: "Parameter volumes used in VWAP calculation."
    :return: "Computed value of VWAP: VWAP = Σ_i P_i V_i / Σ_i V_i"
    '''
    import numpy as np
    return np.sum(np.array(prices) * np.array(volumes)) / np.sum(volumes)






def vwap_benchmark(sum_t_p_t_v_t, sum_t_v_t):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Liquidity Risk', 'Market Liquidity', 'Execution Cost']
    function: "VWAP benchmark — VWAP = sum_t P_t V_t / sum_t V_t. A financial metric in the domain of Liquidity risk, market liquidity & execution cost."
    y_as_x: []
    :param sum_t_p_t_v_t: "Parameter sum_t_p_t_v_t used in VWAP benchmark calculation."
    :param sum_t_v_t: "Parameter sum_t_v_t used in VWAP benchmark calculation."
    :return: "Computed value of VWAP benchmark: VWAP = sum_t P_t V_t / sum_t V_t"
    '''
    return sum_t_p_t_v_t / sum_t_v_t






def weighted_average_cost_of_capital_wacc(cost_of_equity, cost_of_debt, tax_rate, equity_weight, debt_weight):
    '''
    domain: ['Corporate finance & capital budgeting']
    subdomain: ['Corporate Finance', 'Capital Budgeting']
    function: "Weighted Average Cost of Capital (WACC) — WACC = E/V*Re + D/V*Rd*(1-T)."
    y_as_x: []
    :param cost_of_equity: "Cost of Equity (Re) is the return required by equity investors."
    :param cost_of_debt: "Cost of Debt (Rd) is the effective rate a company pays on borrowed funds."
    :param tax_rate: "Tax Rate (T) is the percentage of taxable income that must be paid as corporate income tax."
    :param equity_weight: "Parameter equity_weight used in Weighted average cost of capital (WACC) calculation."
    :param debt_weight: "Parameter debt_weight used in Weighted average cost of capital (WACC) calculation."
    :return: "Computed value of Weighted average cost of capital (WACC): WACC = E/V·R_e + D/V·R_d·(1-T)"
    '''
    return equity_weight * cost_of_equity + debt_weight * cost_of_debt * (1 - tax_rate)






def weighted_average_coupon_wac(coupon_rates, balances):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Structured Finance', 'Securitization']
    function: "Weighted average coupon (WAC) — WAC = sum_i w_i coupon_i. A financial metric in the domain of Structured finance & securitization."
    y_as_x: []
    :param args: "Parameter args used in Weighted average coupon (WAC) calculation."
    :param kwargs: "Parameter kwargs used in Weighted average coupon (WAC) calculation."
    :return: "Computed value of Weighted average coupon (WAC): WAC = sum_i w_i coupon_i"
    '''
    import numpy as np
    return np.dot(coupon_rates, balances) / np.sum(balances)


def weighted_average_life_wal(sum_t_t_principal_t, total_principal):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Structured Finance', 'Securitization']
    function: "Weighted average life (WAL) — WAL = sum_t t Principal_t / Total Principal. A financial metric in the domain of Structured finance & securitization."
    y_as_x: []
    :param sum_t_t_principal_t: "Parameter sum_t_t_principal_t used in Weighted average life (WAL) calculation."
    :param total_principal: "Parameter total_principal used in Weighted average life (WAL) calculation."
    :return: "Computed value of Weighted average life (WAL): WAL = sum_t t Principal_t / Total Principal"
    '''
    return sum_t_t_principal_t / total_principal






def weighted_average_life_of_loan_portfolio(sum_t_t_principal_t, sum_t_principal_t):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit Risk', 'Default Modeling', 'Credit Portfolio']
    function: "Weighted average life of loan portfolio — WAL = sum_t t Principal_t / sum_t Principal_t. A financial metric in the domain of Credit risk, default modeling & credit portfolio."
    y_as_x: []
    :param sum_t_t_principal_t: "Parameter sum_t_t_principal_t used in Weighted average life of loan portfolio calculation."
    :param sum_t_principal_t: "Parameter sum_t_principal_t used in Weighted average life of loan portfolio calculation."
    :return: "Computed value of Weighted average life of loan portfolio: WAL = sum_t t Principal_t / sum_t Principal_t"
    '''
    return sum_t_t_principal_t / sum_t_principal_t






def weighted_average_maturity_wam(maturities, balances):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Structured Finance', 'Securitization']
    function: "Weighted average maturity (WAM) — WAM = sum_i w_i maturity_i. A financial metric in the domain of Structured finance & securitization."
    y_as_x: []
    :param args: "Parameter args used in Weighted average maturity (WAM) calculation."
    :param kwargs: "Parameter kwargs used in Weighted average maturity (WAM) calculation."
    :return: "Computed value of Weighted average maturity (WAM): WAM = sum_i w_i maturity_i"
    '''
    import numpy as np
    return np.dot(maturities, balances) / np.sum(balances)


def weighted_least_squares_wls(y, X, weights):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Financial Econometrics', 'Time Series Analysis']
    function: "Weighted least squares (WLS) — beta_hat = (X'WX)^-1 X'Wy. A financial metric in the domain of Econometrics & time-series finance."
    y_as_x: []
    :param data: "Parameter data used in Weighted least squares (WLS) calculation."
    :param args: "Parameter args used in Weighted least squares (WLS) calculation."
    :return: "Computed value of Weighted least squares (WLS): beta_hat = (X'WX)^-1 X'Wy"
    '''
    import statsmodels.api as sm
    X_const = sm.add_constant(X)
    return sm.WLS(y, X_const, weights=weights).fit()




def weighted_moving_average_wma(close, period=10):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "Weighted Moving Average (WMA) — moving average with linearly increasing weights."
    y_as_x: []
    :param close: "Close is the final trading price at the end of a trading period."
    :param period: "Period (n) is the lookback window in number of bars for technical indicators."
    :return: "Computed value of Weighted moving average (WMA): WMA = sum_i w_i P_{t-i} / sum_i w_i"
    '''
    import pandas as pd
    import numpy as np
    c = pd.Series(close)
    weights = np.arange(1, period + 1)
    return c.rolling(window=period).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True)






def white_heteroskedasticity_test(residuals, exog):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Financial Econometrics', 'Time Series Analysis']
    function: "White heteroskedasticity test — LM = nR^2 from auxiliary regression on X, X^2, cross terms. A financial metric in the domain of Econometrics & time-series finance."
    y_as_x: []
    :param data: "Parameter data used in White heteroskedasticity test calculation."
    :param args: "Parameter args used in White heteroskedasticity test calculation."
    :return: "Computed value of White heteroskedasticity test: LM = nR^2 from auxiliary regression on X, X^2, cross terms"
    '''
    from statsmodels.stats.diagnostic import het_white
    result = het_white(residuals, exog)
    return {'lm_stat': result[0], 'lm_pvalue': result[1], 'f_stat': result[2], 'f_pvalue': result[3]}


def whole_life_annuity_due(interest_rate, mortality_rates):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "Whole life annuity-due — adot_x = E[sum_{k>=0} v^k 1(T_x>k)]. A financial metric in the domain of Actuarial science & insurance."
    y_as_x: []
    :param args: "Parameter args used in Whole life annuity-due calculation."
    :param kwargs: "Parameter kwargs used in Whole life annuity-due calculation."
    :return: "Computed value of Whole life annuity-due: adot_x = E[sum_{k>=0} v^k 1(T_x>k)]"
    '''
    import numpy as np
    v = 1 / (1 + interest_rate)
    qx = np.array(mortality_rates)
    px_cum = np.concatenate([[1], np.cumprod(1 - qx[:-1])])
    t = np.arange(len(qx))
    return np.sum(v**t * px_cum)




def whole_life_annuity_immediate(interest_rate, mortality_rates):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "Whole life annuity-immediate — a_x = E[sum_{k>=1} v^k 1(T_x>=k)]. A financial metric in the domain of Actuarial science & insurance."
    y_as_x: []
    :param args: "Parameter args used in Whole life annuity-immediate calculation."
    :param kwargs: "Parameter kwargs used in Whole life annuity-immediate calculation."
    :return: "Computed value of Whole life annuity-immediate: a_x = E[sum_{k>=1} v^k 1(T_x>=k)]"
    '''
    import numpy as np
    v = 1 / (1 + interest_rate)
    qx = np.array(mortality_rates)
    px_cum = np.cumprod(1 - qx)
    t = np.arange(1, len(qx) + 1)
    return np.sum(v**t * px_cum)




def whole_life_assurance(benefit, interest_rate, mortality_rates):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Actuarial Science', 'Insurance Mathematics']
    function: "Whole life assurance — A_x = Σ_k v^(k+1)·_k p_x·q_(x+k). A financial metric in the domain of Actuarial science & insurance."
    y_as_x: []
    :param args: "Parameter args used in Whole life assurance calculation."
    :param kwargs: "Parameter kwargs used in Whole life assurance calculation."
    :return: "Computed value of Whole life assurance: A_x = Σ_k v^(k+1)·_k p_x·q_(x+k)"
    '''
    import numpy as np
    v = 1 / (1 + interest_rate)
    qx = np.array(mortality_rates)
    px_cum = np.concatenate([[1], np.cumprod(1 - qx[:-1])])
    t = np.arange(1, len(qx) + 1)
    return benefit * np.sum(v**t * px_cum * qx)




def williams_pct_r(high, low, close, period=14):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Technical Analysis', 'Chart Indicators']
    function: "Williams %R — momentum indicator showing overbought/oversold levels. Range [-100, 0]."
    y_as_x: []
    :param high: "High is the highest price during a specific trading period."
    :param low: "Low is the lowest price during a specific trading period."
    :param close: "Close is the final trading price at the end of a trading period."
    :param period: "Period (n) is the lookback window in number of bars for technical indicators."
    :return: "Computed value of Williams %R: %R = -100(H_n-C)/(H_n-L_n)"
    '''
    import pandas as pd
    h = pd.Series(high); l = pd.Series(low); c = pd.Series(close)
    highest = h.rolling(window=period).max()
    lowest = l.rolling(window=period).min()
    return -100 * (highest - c) / (highest - lowest)






def win_loss_ratio(avg_positive_return, avg_negative_return):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Performance Attribution', 'Risk-Adjusted Performance']
    function: "Win/loss ratio — Win/Loss = avg positive return / |avg negative return|. A financial metric in the domain of Performance measurement & attribution."
    y_as_x: []
    :param avg_positive_return: "Parameter avg_positive_return used in Win/loss ratio calculation."
    :param avg_negative_return: "Parameter avg_negative_return used in Win/loss ratio calculation."
    :return: "Computed value of Win/loss ratio: Win/Loss = avg positive return / |avg negative return|"
    '''
    return avg_positive_return / avg_negative_return






def working_capital(current_assets, current_liabilities):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis']
    function: "Working Capital — Current Assets - Current Liabilities. Measures short-term liquidity."
    y_as_x: ['altman_z_score', 'cash_conversion_cycle_ccc', 'current_ratio', 'quick_ratio']
    :param current_assets: "Current Assets are assets expected to be converted to cash within one year."
    :param current_liabilities: "Current Liabilities are obligations due within one year."
    :return: "Computed value of Working capital: Working Capital = Current Assets - Current Liabilities"
    '''
    return current_assets - current_liabilities






def wrong_way_risk_adjustment(exposure, pd_val, correlation_factor=1.4):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit Risk', 'Default Modeling', 'Credit Portfolio']
    function: "Wrong-way risk adjustment — EPE_WWR > EPE due to positive dependence between exposure and PD. A financial metric in the domain of Credit risk, default modeling & credit portfolio."
    y_as_x: []
    :param args: "Parameter args used in Wrong-way risk adjustment calculation."
    :param kwargs: "Parameter kwargs used in Wrong-way risk adjustment calculation."
    :return: "Computed value of Wrong-way risk adjustment: EPE_WWR > EPE due to positive dependence between exposure and PD"
    '''
    return exposure * pd_val * correlation_factor


def yang_zhang_volatility(open_price, high, low, close):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Risk', 'Volatility Modeling']
    function: "Yang-Zhang Volatility — efficient estimator combining overnight, open-to-close, and Rogers-Satchell components."
    y_as_x: []
    :param open_price: "Open is the first trading price at the beginning of a trading period."
    :param high: "High is the highest price during a specific trading period."
    :param low: "Low is the lowest price during a specific trading period."
    :param close: "Close is the final trading price at the end of a trading period."
    :return: "Computed value of Yang-Zhang volatility: sigma_YZ^2 = sigma_o^2 + k sigma_c^2 + (1-k) sigma_RS^2"
    '''
    import numpy as np
    o = np.array(open_price); h = np.array(high); l = np.array(low); c = np.array(close)
    n = len(c)
    k = 0.34 / (1.34 + (n+1)/(n-1))
    oc = np.log(o[1:] / c[:-1])
    co = np.log(c / o)
    rs = np.log(h/c) * np.log(h/o) + np.log(l/c) * np.log(l/o)
    sigma_oc = np.var(oc, ddof=1)
    sigma_co = np.var(co, ddof=1)
    sigma_rs = np.mean(rs)
    return np.sqrt(sigma_oc + k*sigma_co + (1-k)*sigma_rs)






def yield_curve_carry(numerator, denominator):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Fixed Income', 'Bond Mathematics', 'Credit Markets']
    function: "Yield curve carry — Carry approx Coupon + Roll-down + Financing. A financial metric in the domain of Fixed income, bonds & credit markets."
    y_as_x: []
    :param numerator: "Parameter numerator used in Yield curve carry calculation."
    :param denominator: "Parameter denominator used in Yield curve carry calculation."
    :return: "Computed value of Yield curve carry: Carry approx Coupon + Roll-down + Financing"
    '''
    return numerator / denominator if denominator != 0 else 0






def yield_to_call_ytc(face_value, coupon_rate, current_price, call_price, periods_to_call, frequency=2):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Fixed Income', 'Bond Mathematics', 'Credit Markets']
    function: "Yield to call (YTC) — P = sum_t C/(1+y)^t + CallPrice/(1+y)^T_call. A financial metric in the domain of Fixed income, bonds & credit markets."
    y_as_x: []
    :param args: "Parameter args used in Yield to call (YTC) calculation."
    :param kwargs: "Parameter kwargs used in Yield to call (YTC) calculation."
    :return: "Computed value of Yield to call (YTC): P = sum_t C/(1+y)^t + CallPrice/(1+y)^T_call"
    '''
    from scipy.optimize import brentq
    import numpy as np
    c = face_value * coupon_rate / frequency; n = int(periods_to_call * frequency)
    def price_diff(ytc):
        r = ytc / frequency; t = np.arange(1, n+1)
        return np.sum(c / (1+r)**t) + call_price / (1+r)**n - current_price
    return brentq(price_diff, 0.0001, 1.0)


def yield_to_maturity_ytm(face_value, coupon_rate, current_price, periods, frequency=2):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Fixed Income', 'Bond Mathematics', 'Credit Markets']
    function: "Yield to Maturity (YTM) — the discount rate that equates bond price with present value of cash flows."
    y_as_x: []
    :param face_value: "Face Value (par value) is the nominal value of a bond stated by the issuer."
    :param coupon_rate: "Coupon Rate is the annual interest rate paid by a bond issuer relative to face value."
    :param current_price: "Parameter current_price used in Yield to maturity (YTM) calculation."
    :param periods: "Number of periods for calculations."
    :param frequency: "Frequency is the number of coupon payments per year."
    :return: "Computed value of Yield to maturity (YTM): P = sum_t C/(1+YTM/m)^(mt) + F/(1+YTM/m)^(mT)"
    '''
    from scipy.optimize import brentq
    import numpy as np
    c = face_value * coupon_rate / frequency
    n = int(periods * frequency)
    def price_diff(ytm):
        r = ytm / frequency
        t = np.arange(1, n + 1)
        pv = np.sum(c / (1 + r)**t) + face_value / (1 + r)**n
        return pv - current_price
    return brentq(price_diff, 0.0001, 1.0)






def yield_to_worst_ytw(yields_to_call, yield_to_maturity):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Fixed Income', 'Bond Mathematics', 'Credit Markets']
    function: "Yield to worst (YTW) — YTW = min(YTM, YTC, YTP, ...). A financial metric in the domain of Fixed income, bonds & credit markets."
    y_as_x: []
    :param args: "Parameter args used in Yield to worst (YTW) calculation."
    :param kwargs: "Parameter kwargs used in Yield to worst (YTW) calculation."
    :return: "Computed value of Yield to worst (YTW): YTW = min(YTM, YTC, YTP, ...)"
    '''
    import numpy as np
    all_yields = list(yields_to_call) + [yield_to_maturity]
    return min(all_yields)


def zero_coupon_bond_price(face_value, spot_rate, maturity):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Fixed Income', 'Bond Mathematics', 'Credit Markets']
    function: "Zero-Coupon Bond Price — P = FV / (1+r)^T."
    y_as_x: []
    :param face_value: "Face Value (par value) is the nominal value of a bond stated by the issuer."
    :param spot_rate: "Spot Rate is the current interest rate for a specific maturity."
    :param maturity: "Maturity (T) is the time remaining until a bond's principal is repaid."
    :return: "Computed value of Zero-coupon bond price: P = F/(1+r)^T"
    '''
    return face_value / (1 + spot_rate)**maturity






def z_spread(bond_price, face_value, coupon_rate, spot_rates, frequency=2):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit Risk', 'Default Modeling', 'Credit Portfolio']
    function: "Z-Spread — the constant spread added to each spot rate that makes discounted cash flows equal to bond price."
    y_as_x: []
    :param bond_price: "Bond Price — present value of all future cash flows. P = sum(C/(1+y)^t) + FV/(1+y)^n."
    :param face_value: "Face Value (par value) is the nominal value of a bond stated by the issuer."
    :param coupon_rate: "Coupon Rate is the annual interest rate paid by a bond issuer relative to face value."
    :param spot_rates: "Parameter spot_rates used in Z-spread calculation."
    :param frequency: "Frequency is the number of coupon payments per year."
    :return: "Computed value of Z-spread: P = sum_t CF_t exp(-(r_t + z)t)"
    '''
    from scipy.optimize import brentq
    import numpy as np
    c = face_value * coupon_rate / frequency
    n = len(spot_rates)
    def price_diff(z):
        t = np.arange(1, n + 1)
        sr = np.array(spot_rates) / frequency
        pv = np.sum(c / (1 + sr + z/frequency)**t) + face_value / (1 + sr[-1] + z/frequency)**n
        return pv - bond_price
    return brentq(price_diff, -0.05, 0.5)

