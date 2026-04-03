"""
Financial Functions - Batch 6 (Equations 510-611)
"""
import numpy as np
import pandas as pd
from scipy import stats


def money_flow_index_mfi(high, low, close, volume, window=14):
    '''
    domain: ['Technical analysis']
    subdomain: ['Volume indicators']
    function: "Compute Money Flow Index (MFI), a volume-weighted RSI oscillator that measures buying and selling pressure using price and volume data"
    y_as_x: []
    :param high: "Array of high prices"
    :param low: "Array of low prices"
    :param close: "Array of closing prices"
    :param volume: "Array of volume data"
    :param window: "Lookback period, default 14"
    :return: "MFI values ranging from 0 to 100"
    '''
    import talib
    indicator = talib.MFI(high, low, close, volume, timeperiod=window)
    return indicator


def money_flow_index_mfi_v2(high, low, close, volume, timeperiod=14):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Volume indicators']
    function: "Compute Money Flow Index (MFI) using TA-Lib MFI function, measuring buying and selling pressure via price and volume"
    y_as_x: []
    :param high: "Array of high prices"
    :param low: "Array of low prices"
    :param close: "Array of closing prices"
    :param volume: "Array of volume data"
    :param timeperiod: "Lookback period, default 14"
    :return: "MFI values ranging from 0 to 100"
    '''
    import talib
    mfi = talib.MFI(high, low, close, volume, timeperiod=timeperiod)
    return mfi


def money_market_yield(face_value, purchase_price, days_to_maturity):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Short-term instruments', 'Money markets']
    function: "Compute money market yield (CD equivalent yield) from face value, purchase price and days to maturity"
    y_as_x: []
    :param face_value: "Face (par) value of the money market instrument"
    :param purchase_price: "Purchase price of the instrument"
    :param days_to_maturity: "Number of days until maturity"
    :return: "Money market yield as an annualized rate on a 360-day basis"
    '''
    mmy = ((face_value - purchase_price) / purchase_price) * (360.0 / days_to_maturity)
    return mmy


def money_multiple_moic(total_value, invested_capital):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Performance metrics', 'Return multiples']
    function: "Compute Money Multiple (Multiple on Invested Capital, MOIC), the ratio of total value to invested capital"
    y_as_x: []
    :param total_value: "Total value received or expected (distributions + residual value)"
    :param invested_capital: "Total capital invested"
    :return: "MOIC as a multiple"
    '''
    moic = total_value / invested_capital
    return moic


def money_market_account(rate_series, dt):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Risk-free asset', 'Numeraire']
    function: "Compute the money-market account value B(t) = exp(integral_0^t r_s ds) by numerical integration of the short rate path"
    y_as_x: []
    :param rate_series: "Array of instantaneous short rates r_s observed over time"
    :param dt: "Time step between observations"
    :return: "Money market account value at each time step"
    '''
    import QuantLib as ql
    cumulative_integral = np.cumsum(rate_series * dt)
    B_t = np.exp(cumulative_integral)
    return B_t


def money_weighted_return_mwrr(cashflows):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Return calculation', 'IRR-based returns']
    function: "Compute the money-weighted rate of return (MWRR), equivalent to the internal rate of return on investor cash flows"
    y_as_x: []
    :param cashflows: "Array of cash flows (negative for contributions, positive for distributions/ending value)"
    :return: "Money-weighted return (IRR) as a decimal"
    '''
    import numpy_financial as npf
    mwrr = npf.irr(cashflows)
    return mwrr


def monte_carlo_var(returns, confidence_level=0.95, n_simulations=10000):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Value at Risk', 'Monte Carlo simulation']
    function: "Compute Monte Carlo VaR by simulating portfolio returns assuming normal distribution and taking the alpha-quantile"
    y_as_x: []
    :param returns: "Array of historical portfolio returns"
    :param confidence_level: "Confidence level for VaR, default 0.95"
    :param n_simulations: "Number of Monte Carlo simulations, default 10000"
    :return: "VaR estimate as a positive loss amount"
    '''
    mu = np.mean(returns)
    sigma = np.std(returns, ddof=1)
    simulated = np.random.normal(mu, sigma, n_simulations)
    alpha = 1 - confidence_level
    var = -np.percentile(simulated, alpha * 100)
    return var


def mortality_rate(d_x, l_x):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Life tables', 'Mortality']
    function: "Compute mortality rate q_x = d_x / l_x, the probability that a person aged x dies within one year"
    y_as_x: ['one_year_death_probability', 'one_year_survival_probability']
    :param d_x: "Number of deaths between age x and x+1"
    :param l_x: "Number of lives at age x"
    :return: "Mortality rate q_x"
    '''
    q_x = d_x / l_x
    return q_x


def mortgage_constant(rate, nper):
    '''
    domain: ['Real estate finance']
    subdomain: ['Mortgage analysis', 'Debt service']
    function: "Compute the mortgage constant, defined as the annual debt service divided by the loan amount, using the annuity payment formula"
    y_as_x: []
    :param rate: "Annual interest rate (as decimal)"
    :param nper: "Total number of monthly payments"
    :return: "Mortgage constant (annual debt service per unit of loan)"
    '''
    import numpy_financial as npf
    monthly_rate = rate / 12
    monthly_pmt = npf.pmt(monthly_rate, nper, -1.0)
    annual_debt_service = monthly_pmt * 12
    return annual_debt_service


def moving_average_convergence_divergence_macd(close, fastperiod=12, slowperiod=26, signalperiod=9):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Trend indicators', 'Momentum']
    function: "Compute Moving Average Convergence Divergence (MACD), its signal line, and histogram"
    y_as_x: []
    :param close: "Array of closing prices"
    :param fastperiod: "Fast EMA period, default 12"
    :param slowperiod: "Slow EMA period, default 26"
    :param signalperiod: "Signal line EMA period, default 9"
    :return: "Tuple of (MACD line, Signal line, MACD histogram)"
    '''
    import talib
    macd_line, signal_line, histogram = talib.MACD(close, fastperiod=fastperiod,
                                                    slowperiod=slowperiod,
                                                    signalperiod=signalperiod)
    return macd_line, signal_line, histogram


def mrel_over_tlac_ratio(eligible_liabilities_and_capital, rwa, leverage_exposure=None):
    '''
    domain: ['Bank regulation, Basel & prudential ratios']
    subdomain: ['Resolution planning', 'Loss-absorbing capacity']
    function: "Compute MREL/TLAC ratio as eligible liabilities and capital divided by RWA or leverage exposure"
    y_as_x: []
    :param eligible_liabilities_and_capital: "Total eligible liabilities plus capital for loss absorption"
    :param rwa: "Risk-weighted assets"
    :param leverage_exposure: "Leverage exposure measure (optional, if None uses RWA)"
    :return: "TLAC ratio as a decimal"
    '''
    denominator = leverage_exposure if leverage_exposure is not None else rwa
    tlac_ratio = eligible_liabilities_and_capital / denominator
    return tlac_ratio


def m_squared_modigliani(returns, benchmark_returns, risk_free_rate=0.0):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Risk-adjusted returns', 'Performance measurement']
    function: "Compute M-squared (Modigliani-Modigliani) measure: M2 = Sharpe * sigma_market + R_f, measuring risk-adjusted performance relative to the market"
    y_as_x: []
    :param returns: "Array of portfolio returns"
    :param benchmark_returns: "Array of benchmark/market returns"
    :param risk_free_rate: "Risk-free rate per period, default 0.0"
    :return: "M-squared value"
    '''
    import empyrical
    excess_p = np.mean(returns) - risk_free_rate
    sigma_p = np.std(returns, ddof=1)
    sigma_m = np.std(benchmark_returns, ddof=1)
    sharpe = excess_p / sigma_p if sigma_p != 0 else 0.0
    m2 = sharpe * sigma_m + risk_free_rate
    return m2


def multi_stage_ddm(dividends, terminal_value, discount_rate):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Dividend discount models', 'Multi-stage valuation']
    function: "Compute equity value using a multi-stage dividend discount model: P_0 = sum_t D_t/(1+r)^t + TV/(1+r)^T"
    y_as_x: []
    :param dividends: "Array of expected dividends for each explicit forecast period"
    :param terminal_value: "Terminal value at the end of the explicit forecast period"
    :param discount_rate: "Required rate of return (discount rate) as decimal"
    :return: "Present value of the equity"
    '''
    T = len(dividends)
    pv = 0.0
    for t in range(T):
        pv += dividends[t] / (1 + discount_rate) ** (t + 1)
    pv += terminal_value / (1 + discount_rate) ** T
    return pv


def naive_bayes_classifier(X_train, y_train, X_test):
    '''
    domain: ['Quantitative forecasting & machine learning in finance']
    subdomain: ['Classification', 'Bayesian methods']
    function: "Fit a Gaussian Naive Bayes classifier and return predicted probabilities: P(y|x) proportional to P(y) * prod_j P(x_j|y)"
    y_as_x: []
    :param X_train: "Training feature matrix"
    :param y_train: "Training labels"
    :param X_test: "Test feature matrix"
    :return: "Predicted class probabilities for X_test"
    '''
    from sklearn.naive_bayes import GaussianNB
    model = GaussianNB()
    model.fit(X_train, y_train)
    probabilities = model.predict_proba(X_test)
    return probabilities


def nelson_siegel_yield_curve(beta0, beta1, beta2, tau, maturities):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Yield curve fitting', 'Parametric models']
    function: "Compute yields using the Nelson-Siegel model: y(t)=beta0 + beta1*((1-exp(-t/tau))/(t/tau)) + beta2*(((1-exp(-t/tau))/(t/tau))-exp(-t/tau))"
    y_as_x: []
    :param beta0: "Long-term level factor"
    :param beta1: "Short-term slope factor"
    :param beta2: "Medium-term curvature factor"
    :param tau: "Decay parameter controlling the location of the hump"
    :param maturities: "Array of maturities in years"
    :return: "Array of yields for each maturity"
    '''
    maturities = np.asarray(maturities, dtype=float)
    t_over_tau = maturities / tau
    factor1 = (1 - np.exp(-t_over_tau)) / t_over_tau
    factor2 = factor1 - np.exp(-t_over_tau)
    y = beta0 + beta1 * factor1 + beta2 * factor2
    return y


def nelson_siegel_svensson_curve(beta0, beta1, beta2, beta3, tau1, tau2, maturities):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Yield curve fitting', 'Parametric models']
    function: "Compute yields using the Nelson-Siegel-Svensson extension with a second curvature term and second decay parameter"
    y_as_x: []
    :param beta0: "Long-term level factor"
    :param beta1: "Short-term slope factor"
    :param beta2: "First curvature factor"
    :param beta3: "Second curvature factor"
    :param tau1: "First decay parameter"
    :param tau2: "Second decay parameter"
    :param maturities: "Array of maturities in years"
    :return: "Array of yields for each maturity"
    '''
    maturities = np.asarray(maturities, dtype=float)
    t_tau1 = maturities / tau1
    t_tau2 = maturities / tau2
    L1 = (1 - np.exp(-t_tau1)) / t_tau1
    L2 = (1 - np.exp(-t_tau2)) / t_tau2
    y = beta0 + beta1 * L1 + beta2 * (L1 - np.exp(-t_tau1)) + beta3 * (L2 - np.exp(-t_tau2))
    return y


def net_charge_off_ratio(charge_offs, recoveries, average_loans):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Credit losses', 'Asset quality']
    function: "Compute net charge-off ratio: (Charge-offs - Recoveries) / Average Loans"
    y_as_x: []
    :param charge_offs: "Total charge-offs during the period"
    :param recoveries: "Total recoveries during the period"
    :param average_loans: "Average outstanding loan balance"
    :return: "Net charge-off ratio as a decimal"
    '''
    nco_ratio = (charge_offs - recoveries) / average_loans
    return nco_ratio


def net_convenience_yield(gross_convenience_yield, storage_cost):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Cost of carry', 'Convenience yield']
    function: "Compute net convenience yield as gross convenience yield minus storage costs"
    y_as_x: []
    :param gross_convenience_yield: "Gross convenience yield"
    :param storage_cost: "Storage cost per unit of time"
    :return: "Net convenience yield"
    '''
    net_cy = gross_convenience_yield - storage_cost
    return net_cy


def net_debt_at_entry(debt_assumed, new_debt, cash_acquired):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['LBO modeling', 'Capital structure']
    function: "Compute net debt at entry in an LBO: Debt Assumed + New Debt - Cash Acquired"
    y_as_x: []
    :param debt_assumed: "Existing debt assumed in the transaction"
    :param new_debt: "New debt raised for the acquisition"
    :param cash_acquired: "Cash on the target's balance sheet at closing"
    :return: "Net debt at entry"
    '''
    net_debt = debt_assumed + new_debt - cash_acquired
    return net_debt


def net_income(revenue, expenses, taxes):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Income statement', 'Profitability']
    function: "Compute net income: Revenue - Expenses - Taxes"
    y_as_x: ['net_margin', 'eps', 'return_on_assets_roa', 'return_on_equity_roe', 'dividend_payout_ratio', 'residual_income', 'free_cash_flow_to_equity_fcfe', 'fcfe', 'debt_to_income_residual']
    :param revenue: "Total revenue"
    :param expenses: "Total expenses (operating + non-operating)"
    :param taxes: "Total tax expense"
    :return: "Net income"
    '''
    ni = revenue - expenses - taxes
    return ni


def net_interest_income_nii(interest_income, interest_expense):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Interest rate management', 'Banking profitability']
    function: "Compute Net Interest Income (NII) = Interest Income - Interest Expense"
    y_as_x: ['net_interest_margin_nim', 'nii_sensitivity']
    :param interest_income: "Total interest income from earning assets"
    :param interest_expense: "Total interest expense on funding liabilities"
    :return: "Net interest income"
    '''
    nii = interest_income - interest_expense
    return nii


def net_interest_margin_nim(net_interest_income_nii, average_earning_assets):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Profitability metrics', 'Banking ratios']
    function: "Compute Net Interest Margin (NIM) = NII / Average Earning Assets"
    y_as_x: []
    :param net_interest_income_nii: "Net interest income"
    :param average_earning_assets: "Average balance of interest-earning assets"
    :return: "Net interest margin as a decimal"
    '''
    nim = net_interest_income_nii / average_earning_assets
    return nim


def net_irr_to_lp(lp_cashflows):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Fund performance', 'LP returns']
    function: "Compute Net IRR to limited partners (LP), the internal rate of return on LP cash flows after management fees and carried interest"
    y_as_x: []
    :param lp_cashflows: "Array of LP cash flows (negative for capital calls, positive for distributions)"
    :return: "Net IRR to LP as a decimal"
    '''
    import numpy_financial as npf
    irr = npf.irr(lp_cashflows)
    return irr


def net_margin(net_income, revenue):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Profitability ratios']
    function: "Compute net margin: Net Income / Revenue"
    y_as_x: []
    :param net_income: "Net income"
    :param revenue: "Total revenue"
    :return: "Net margin as a decimal"
    '''
    margin = net_income / revenue
    return margin


def net_operating_income_noi(rental_revenue, other_income, operating_expenses):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Property valuation', 'Income analysis']
    function: "Compute Net Operating Income (NOI) = Rental Revenue + Other Income - Operating Expenses"
    y_as_x: ['capitalization_rate', 'debt_service_coverage_ratio_dscr', 'debt_yield', 'noi_margin', 'property_value_from_cap_rate', 'terminal_capitalization_value', 'unlevered_yield']
    :param rental_revenue: "Total rental revenue from the property"
    :param other_income: "Other income (parking, laundry, etc.)"
    :param operating_expenses: "Total operating expenses"
    :return: "Net operating income"
    '''
    noi = rental_revenue + other_income - operating_expenses
    return noi


def net_premium(pv_benefits, pv_premium_annuity):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Premium calculation', 'Life insurance']
    function: "Compute net premium: P = PV(Benefits) / PV(Premium annuity), the pure premium with no expense loading"
    y_as_x: ['net_premium_equivalence_principle']
    :param pv_benefits: "Present value of future benefits"
    :param pv_premium_annuity: "Present value of premium annuity (annuity-due factor)"
    :return: "Net level premium"
    '''
    premium = pv_benefits / pv_premium_annuity
    return premium


def net_premium_equivalence_principle(net_premium, apv_premium_annuity, apv_benefits):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Premium calculation', 'Equivalence principle']
    function: "Verify and compute net premium via the equivalence principle: Premium x APV(premium annuity) = APV(benefits)"
    y_as_x: []
    :param net_premium: "Net premium per period"
    :param apv_premium_annuity: "Actuarial present value of premium annuity"
    :param apv_benefits: "Actuarial present value of benefits"
    :return: "Difference between premium PV and benefit PV (should be zero if equivalence holds)"
    '''
    difference = net_premium * apv_premium_annuity - apv_benefits
    return difference


def net_present_value_npv(rate, cashflows):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Capital budgeting', 'Project evaluation']
    function: "Compute Net Present Value (NPV) = sum_t CF_t / (1+r)^t"
    y_as_x: ['profitability_index', 'equivalent_annual_annuity_eaa', 'adjusted_present_value_apv', 'loan_life_coverage_ratio']
    :param rate: "Discount rate per period"
    :param cashflows: "Array of cash flows starting from period 0"
    :return: "Net present value"
    '''
    import numpy_financial as npf
    npv = npf.npv(rate, cashflows)
    return npv


def net_stable_funding_ratio_nsfr(available_stable_funding, required_stable_funding):
    '''
    domain: ['Bank regulation, Basel & prudential ratios']
    subdomain: ['Liquidity regulation', 'Funding stability']
    function: "Compute Net Stable Funding Ratio (NSFR) = Available Stable Funding / Required Stable Funding"
    y_as_x: ['stable_funding_gap']
    :param available_stable_funding: "Available stable funding per Basel III definition"
    :param required_stable_funding: "Required stable funding per Basel III definition"
    :return: "NSFR ratio (must be >= 1.0 to comply)"
    '''
    nsfr = available_stable_funding / required_stable_funding
    return nsfr


def net_weighted_average_spread(weighted_avg_asset_spread, funding_spread):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Spread analysis', 'Profitability']
    function: "Compute Net Weighted Average Spread (NWAS) = weighted average asset spread - funding spread"
    y_as_x: []
    :param weighted_avg_asset_spread: "Weighted average spread of the underlying asset pool"
    :param funding_spread: "Weighted average funding cost spread of the liabilities"
    :return: "Net weighted average spread"
    '''
    nwas = weighted_avg_asset_spread - funding_spread
    return nwas


def newey_west_hac_covariance(y, X, max_lags=None):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Robust covariance estimation', 'HAC estimators']
    function: "Compute Newey-West heteroscedasticity and autocorrelation consistent (HAC) covariance estimator for OLS regression"
    y_as_x: []
    :param y: "Dependent variable array"
    :param X: "Independent variable matrix (with or without constant)"
    :param max_lags: "Maximum number of lags for Newey-West kernel (None for automatic)"
    :return: "HAC covariance matrix of coefficient estimates"
    '''
    import statsmodels.api as sm
    X_with_const = sm.add_constant(X)
    model = sm.OLS(y, X_with_const).fit(cov_type='HAC', cov_kwds={'maxlags': max_lags})
    return model.cov_params()


def nii_sensitivity(balances, delta_rates, repricing_fractions):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Interest rate risk', 'Earnings sensitivity']
    function: "Compute NII sensitivity: Delta NII = sum_i Balance_i x Delta Rate_i x Repricing Fraction_i"
    y_as_x: []
    :param balances: "Array of balances per bucket"
    :param delta_rates: "Array of rate changes per bucket"
    :param repricing_fractions: "Array of repricing fractions per bucket"
    :return: "Change in net interest income"
    '''
    balances = np.asarray(balances)
    delta_rates = np.asarray(delta_rates)
    repricing_fractions = np.asarray(repricing_fractions)
    delta_nii = np.sum(balances * delta_rates * repricing_fractions)
    return delta_nii


def noi_margin(net_operating_income_noi, effective_gross_income):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Property performance', 'Operating efficiency']
    function: "Compute NOI margin: NOI / Effective Gross Income"
    y_as_x: []
    :param net_operating_income_noi: "Net operating income"
    :param effective_gross_income: "Effective gross income"
    :return: "NOI margin as a decimal"
    '''
    margin = net_operating_income_noi / effective_gross_income
    return margin


def npl_ratio(nonperforming_loans, gross_loans):
    '''
    domain: ['Bank regulation, Basel & prudential ratios']
    subdomain: ['Asset quality', 'Credit risk indicators']
    function: "Compute NPL ratio: Nonperforming Loans / Gross Loans"
    y_as_x: []
    :param nonperforming_loans: "Total nonperforming loans"
    :param gross_loans: "Total gross loans"
    :return: "NPL ratio as a decimal"
    '''
    ratio = nonperforming_loans / gross_loans
    return ratio


def number_of_periods(rate, pmt, pv, fv=0.0):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Time value of money', 'Loan analysis']
    function: "Compute the number of periods required to pay off a loan or reach a future value target: n = -ln(1-rPV/PMT) / ln(1+r)"
    y_as_x: []
    :param rate: "Interest rate per period"
    :param pmt: "Payment per period (negative for outflows)"
    :param pv: "Present value (loan amount, negative for loan)"
    :param fv: "Future value target, default 0.0"
    :return: "Number of periods"
    '''
    import numpy_financial as npf
    nper = npf.nper(rate, pmt, pv, fv)
    return nper


def oc_trigger(oc_ratio, trigger_level):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Trigger mechanisms', 'Credit enhancement']
    function: "Check if overcollateralization trigger is breached: trigger breached if OC ratio < trigger level"
    y_as_x: []
    :param oc_ratio: "Current overcollateralization ratio"
    :param trigger_level: "Trigger threshold level"
    :return: "Boolean indicating whether the trigger is breached (True if breached)"
    '''
    breached = oc_ratio < trigger_level
    return breached


def omega_ratio(returns, required_return=0.0):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Risk-adjusted returns', 'Performance ratios']
    function: "Compute the Omega ratio: ratio of probability-weighted gains to probability-weighted losses relative to a threshold return"
    y_as_x: []
    :param returns: "Array of portfolio returns"
    :param required_return: "Threshold return level, default 0.0"
    :return: "Omega ratio"
    '''
    import empyrical
    omega = empyrical.omega_ratio(returns, risk_free=required_return)
    return omega


def on_balance_volume_obv(close, volume):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Volume indicators']
    function: "Compute On-Balance Volume (OBV): cumulative volume added when price rises, subtracted when price falls"
    y_as_x: []
    :param close: "Array of closing prices"
    :param volume: "Array of trading volumes"
    :return: "OBV values"
    '''
    import talib
    obv = talib.OBV(close, volume)
    return obv


def one_year_death_probability(q_x):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Mortality', 'Life tables']
    function: "Return the one-year death probability q_x = P[x dies within 1 year]"
    y_as_x: ['one_year_survival_probability']
    :param q_x: "One-year mortality rate at age x"
    :return: "One-year death probability"
    '''
    return q_x


def one_year_survival_probability(one_year_death_probability):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Mortality', 'Life tables']
    function: "Compute one-year survival probability: p_x = 1 - q_x"
    y_as_x: []
    :param one_year_death_probability: "One-year death probability q_x"
    :return: "One-year survival probability p_x"
    '''
    p_x = 1 - one_year_death_probability
    return p_x


def operating_cash_flow_ratio(operating_cash_flow, current_liabilities):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Liquidity ratios', 'Cash flow analysis']
    function: "Compute operating cash flow ratio: Operating Cash Flow / Current Liabilities"
    y_as_x: []
    :param operating_cash_flow: "Operating cash flow from the cash flow statement"
    :param current_liabilities: "Total current liabilities"
    :return: "Operating cash flow ratio"
    '''
    ratio = operating_cash_flow / current_liabilities
    return ratio


def operating_expense_ratio(operating_expenses, effective_gross_income):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Operating efficiency', 'Property analysis']
    function: "Compute operating expense ratio (OER) = Operating Expenses / Effective Gross Income"
    y_as_x: []
    :param operating_expenses: "Total operating expenses of the property"
    :param effective_gross_income: "Effective gross income"
    :return: "Operating expense ratio as a decimal"
    '''
    oer = operating_expenses / effective_gross_income
    return oer


def operating_leverage(pct_change_ebit, pct_change_sales):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Leverage analysis', 'Operating risk']
    function: "Compute degree of operating leverage (DOL) = %Change in EBIT / %Change in Sales"
    y_as_x: ['combined_leverage']
    :param pct_change_ebit: "Percentage change in EBIT"
    :param pct_change_sales: "Percentage change in sales"
    :return: "Degree of operating leverage"
    '''
    dol = pct_change_ebit / pct_change_sales
    return dol


def operating_margin(ebit, revenue):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Profitability ratios']
    function: "Compute operating margin: EBIT / Revenue"
    y_as_x: []
    :param ebit: "Earnings before interest and taxes"
    :param revenue: "Total revenue"
    :return: "Operating margin as a decimal"
    '''
    margin = ebit / revenue
    return margin


def operational_risk_capital_sma(bic, ilm):
    '''
    domain: ['Bank regulation, Basel & prudential ratios']
    subdomain: ['Operational risk', 'Basel standardized measurement approach']
    function: "Compute operational risk capital under the Standardized Measurement Approach: ORC = BIC x ILM"
    y_as_x: []
    :param bic: "Business Indicator Component"
    :param ilm: "Internal Loss Multiplier"
    :return: "Operational risk capital charge"
    '''
    orc = bic * ilm
    return orc


def optimal_number_of_contracts(hedge_ratio, exposure_value, futures_contract_value):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Hedging', 'Contract sizing']
    function: "Compute optimal number of futures contracts: N* = h* x Exposure Value / Futures Contract Value"
    y_as_x: []
    :param hedge_ratio: "Optimal hedge ratio h*"
    :param exposure_value: "Dollar value of the exposure to be hedged"
    :param futures_contract_value: "Dollar value of one futures contract"
    :return: "Optimal number of contracts (rounded to nearest integer)"
    '''
    n_star = hedge_ratio * exposure_value / futures_contract_value
    return round(n_star)


def option_delta_hedged_pandl(gamma, delta_s, theta, dt, vega, delta_sigma):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Hedging P&L', 'Greeks']
    function: "Compute delta-hedged P&L of an option position: dPi = 0.5*Gamma*(dS)^2 + Theta*dt + Vega*d_sigma"
    y_as_x: []
    :param gamma: "Option gamma"
    :param delta_s: "Change in underlying price"
    :param theta: "Option theta"
    :param dt: "Time elapsed"
    :param vega: "Option vega"
    :param delta_sigma: "Change in implied volatility"
    :return: "Delta-hedged P&L"
    '''
    dpi = 0.5 * gamma * delta_s**2 + theta * dt + vega * delta_sigma
    return dpi


def option_pool_dilution(shares_owned, existing_shares, new_shares, option_pool_shares):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Dilution', 'Cap table']
    function: "Compute fully diluted ownership percentage after option pool creation"
    y_as_x: []
    :param shares_owned: "Number of shares owned by the investor"
    :param existing_shares: "Existing shares outstanding"
    :param new_shares: "New shares issued in the round"
    :param option_pool_shares: "Shares reserved for the option pool"
    :return: "Fully diluted ownership percentage as a decimal"
    '''
    fully_diluted_total = existing_shares + new_shares + option_pool_shares
    ownership = shares_owned / fully_diluted_total
    return ownership


def option_adjusted_spread_oas(bond_price, cashflows, discount_factors, coupon_dates, n_paths=1000, r_paths=None):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Spread analysis', 'Callable bonds']
    function: "Compute Option-Adjusted Spread (OAS) - the constant spread that when added to the risk-free rate equates model price to market price under Monte Carlo simulation"
    y_as_x: []
    :param bond_price: "Observed market price of the bond"
    :param cashflows: "Array of bond cash flows per path and time"
    :param discount_factors: "Array of risk-free discount factors per path and time"
    :param coupon_dates: "Array of coupon payment dates in years"
    :param n_paths: "Number of Monte Carlo paths"
    :param r_paths: "Simulated short rate paths (n_paths x n_times)"
    :return: "Option-adjusted spread in basis points"
    '''
    from scipy.optimize import brentq

    def price_diff(oas):
        total = 0.0
        for t_idx, t in enumerate(coupon_dates):
            cf = np.mean(cashflows[:, t_idx]) if cashflows.ndim > 1 else cashflows[t_idx]
            df = np.mean(discount_factors[:, t_idx]) if discount_factors.ndim > 1 else discount_factors[t_idx]
            total += cf * df * np.exp(-oas * t)
        return total - bond_price

    try:
        oas = brentq(price_diff, -0.05, 0.20)
    except ValueError:
        oas = np.nan
    return oas


def oracle_approximating_shrinkage_oas(X):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Covariance estimation', 'Shrinkage methods']
    function: "Compute Oracle Approximating Shrinkage (OAS) covariance estimator: Sigma_hat = (1-delta)*S + delta*mu*I"
    y_as_x: []
    :param X: "Matrix of asset returns (n_samples x n_features)"
    :return: "Shrunk covariance matrix"
    '''
    from sklearn.covariance import OAS
    estimator = OAS().fit(X)
    return estimator.covariance_


def order_imbalance(buy_volume, sell_volume):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Order flow analysis', 'Market microstructure']
    function: "Compute order imbalance: OI = (Buy Volume - Sell Volume) / (Buy Volume + Sell Volume)"
    y_as_x: []
    :param buy_volume: "Total buy-initiated volume"
    :param sell_volume: "Total sell-initiated volume"
    :return: "Order imbalance between -1 and 1"
    '''
    oi = (buy_volume - sell_volume) / (buy_volume + sell_volume)
    return oi


def outstanding_balance_after_k_payments(rate, nper, pv, pmt, k):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Loan amortization', 'Balance calculation']
    function: "Compute outstanding loan balance after k payments: B_k = PV*(1+r)^k - PMT*((1+r)^k - 1)/r"
    y_as_x: []
    :param rate: "Interest rate per period"
    :param nper: "Total number of payment periods"
    :param pv: "Original loan amount (positive)"
    :param pmt: "Payment per period (negative for outflow)"
    :param k: "Number of payments already made"
    :return: "Outstanding balance after k payments"
    '''
    import numpy_financial as npf
    balance = npf.fv(rate, k, pmt, -pv)
    return balance


def outstanding_loan_balance(rate, periods_elapsed, pmt, pv):
    '''
    domain: ['Banking, lending & project finance']
    subdomain: ['Loan amortization', 'Balance calculation']
    function: "Compute outstanding loan balance at time t: Balance_t = PV*(1+r)^t - PMT*[((1+r)^t - 1)/r]"
    y_as_x: []
    :param rate: "Interest rate per period"
    :param periods_elapsed: "Number of periods elapsed"
    :param pmt: "Payment per period (negative for outflow)"
    :param pv: "Original present value (loan amount, positive)"
    :return: "Outstanding balance at time t"
    '''
    import numpy_financial as npf
    balance = npf.fv(rate, periods_elapsed, pmt, -pv)
    return balance


def overcollateralization_ratio(collateral_balance, notes_outstanding):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Credit enhancement', 'OC tests']
    function: "Compute overcollateralization ratio: Collateral Balance / Notes Outstanding"
    y_as_x: ['oc_trigger']
    :param collateral_balance: "Total balance of the collateral pool"
    :param notes_outstanding: "Total outstanding balance of issued notes"
    :return: "Overcollateralization ratio"
    '''
    oc_ratio = collateral_balance / notes_outstanding
    return oc_ratio


def ownership_percentage(investment, post_money_valuation):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Cap table', 'Equity ownership']
    function: "Compute ownership percentage: Investment / Post-money Valuation"
    y_as_x: ['option_pool_dilution']
    :param investment: "Amount invested"
    :param post_money_valuation: "Post-money valuation of the company"
    :return: "Ownership percentage as a decimal"
    '''
    ownership = investment / post_money_valuation
    return ownership


def p_over_b_ratio(price_per_share, book_value_per_share):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Valuation multiples', 'Equity valuation']
    function: "Compute Price-to-Book ratio: Price per Share / Book Value per Share"
    y_as_x: []
    :param price_per_share: "Current market price per share"
    :param book_value_per_share: "Book value per share"
    :return: "P/B ratio"
    '''
    pb = price_per_share / book_value_per_share
    return pb


def p_over_e_ratio(price_per_share, eps):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Valuation multiples', 'Equity valuation']
    function: "Compute Price-to-Earnings ratio: Price per Share / EPS"
    y_as_x: ['peg_ratio']
    :param price_per_share: "Current market price per share"
    :param eps: "Earnings per share"
    :return: "P/E ratio"
    '''
    pe = price_per_share / eps
    return pe


def pain_index(returns):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Drawdown analysis', 'Risk metrics']
    function: "Compute the Pain Index, defined as the average drawdown over the evaluation period"
    y_as_x: []
    :param returns: "Array or Series of portfolio returns"
    :return: "Pain index (average drawdown as a positive value)"
    '''
    import quantstats as qs
    wealth = (1 + pd.Series(returns)).cumprod()
    peak = wealth.cummax()
    drawdowns = (wealth - peak) / peak
    pain = -drawdowns.mean()
    return pain


def par_swap_rate(discount_factors, accrual_factors):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Swap pricing', 'Interest rate swaps']
    function: "Compute par swap rate: K* = (1 - DF(T_n)) / (sum_i alpha_i * DF(t_i))"
    y_as_x: []
    :param discount_factors: "Array of discount factors at each payment date"
    :param accrual_factors: "Array of accrual (day count) fractions for each period"
    :return: "Par swap rate"
    '''
    discount_factors = np.asarray(discount_factors)
    accrual_factors = np.asarray(accrual_factors)
    k_star = (1 - discount_factors[-1]) / np.sum(accrual_factors * discount_factors)
    return k_star


def par_yield(discount_factors, accrual_factors):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Yield curve', 'Bond pricing']
    function: "Compute par yield: Par = (1 - DF_n) / sum_i alpha_i * DF_i"
    y_as_x: []
    :param discount_factors: "Array of discount factors for each coupon date"
    :param accrual_factors: "Array of day count fractions for each coupon period"
    :return: "Par yield"
    '''
    discount_factors = np.asarray(discount_factors)
    accrual_factors = np.asarray(accrual_factors)
    par = (1 - discount_factors[-1]) / np.sum(accrual_factors * discount_factors)
    return par


def parabolic_sar(high, low, acceleration=0.02, maximum=0.2):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Trend indicators', 'Stop and reverse']
    function: "Compute Parabolic SAR: SAR_t = SAR_{t-1} + AF*(EP - SAR_{t-1})"
    y_as_x: []
    :param high: "Array of high prices"
    :param low: "Array of low prices"
    :param acceleration: "Acceleration factor, default 0.02"
    :param maximum: "Maximum acceleration factor, default 0.2"
    :return: "Parabolic SAR values"
    '''
    import talib
    sar = talib.SAR(high, low, acceleration=acceleration, maximum=maximum)
    return sar


def parametric_es_under_normality(mu, sigma, alpha=0.05):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Expected shortfall', 'Tail risk']
    function: "Compute parametric Expected Shortfall under normality: ES = -(mu - sigma * phi(z_alpha) / alpha)"
    y_as_x: []
    :param mu: "Mean of portfolio returns"
    :param sigma: "Standard deviation of portfolio returns"
    :param alpha: "Confidence level tail probability, default 0.05"
    :return: "Expected Shortfall as a positive loss"
    '''
    z_alpha = stats.norm.ppf(alpha)
    phi_z = stats.norm.pdf(z_alpha)
    es = -(mu - sigma * phi_z / alpha)
    return es


def parametric_normal_var(returns, confidence_level=0.95):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Value at Risk', 'Parametric methods']
    function: "Compute parametric normal VaR: VaR_alpha = -(mu + z_alpha * sigma) * V"
    y_as_x: []
    :param returns: "Array of portfolio returns"
    :param confidence_level: "Confidence level, default 0.95"
    :return: "Parametric VaR as a positive loss"
    '''
    import empyrical
    mu = np.mean(returns)
    sigma = np.std(returns, ddof=1)
    z_alpha = stats.norm.ppf(1 - confidence_level)
    var = -(mu + z_alpha * sigma)
    return var


def parametric_var(returns, confidence_level=0.95):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Value at Risk', 'Parametric methods']
    function: "Compute parametric VaR: VaR_alpha = -(mu + z_alpha * sigma)"
    y_as_x: ['component_var', 'component_var_v2', 'liquidity_adjusted_var', 'stressed_var']
    :param returns: "Array of portfolio returns"
    :param confidence_level: "Confidence level, default 0.95"
    :return: "Parametric VaR as a positive loss"
    '''
    mu = np.mean(returns)
    sigma = np.std(returns, ddof=1)
    z_alpha = stats.norm.ppf(1 - confidence_level)
    var = -(mu + z_alpha * sigma)
    return var


def parkinson_volatility(high, low):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Volatility estimation', 'Range-based estimators']
    function: "Compute Parkinson volatility estimator: sigma_P^2 = [1/(4*ln(2)*n)] * sum[ln(H/L)]^2"
    y_as_x: []
    :param high: "Array of high prices"
    :param low: "Array of low prices"
    :return: "Parkinson volatility estimate (annualized if daily data, multiply by sqrt(252))"
    '''
    high = np.asarray(high, dtype=float)
    low = np.asarray(low, dtype=float)
    n = len(high)
    log_hl = np.log(high / low)
    sigma_sq = np.sum(log_hl**2) / (4 * np.log(2) * n)
    return np.sqrt(sigma_sq)


def participation_rate(executed_volume, market_volume):
    '''
    domain: ['Trading, execution & market microstructure']
    subdomain: ['Execution analysis', 'Market impact']
    function: "Compute participation rate: Executed Volume / Market Volume"
    y_as_x: ['days_to_liquidate']
    :param executed_volume: "Volume executed by the trader"
    :param market_volume: "Total market volume over the same period"
    :return: "Participation rate as a decimal"
    '''
    rate = executed_volume / market_volume
    return rate


def pastor_stambaugh_liquidity(returns, market_excess_returns, volumes, lags=1):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Liquidity estimation', 'Market microstructure']
    function: "Estimate Pastor-Stambaugh liquidity measure via regression of next-period returns on signed volume"
    y_as_x: []
    :param returns: "Array of asset returns"
    :param market_excess_returns: "Array of market excess returns"
    :param volumes: "Array of dollar volumes"
    :param lags: "Number of lags, default 1"
    :return: "Estimated liquidity gamma coefficient"
    '''
    import statsmodels.api as sm
    excess_returns = returns[:-1]
    signed_volume = np.sign(excess_returns) * volumes[:-1]
    y = returns[1:]
    X = sm.add_constant(np.column_stack([market_excess_returns[1:], signed_volume]))
    model = sm.OLS(y, X).fit()
    gamma = model.params[-1]
    return gamma


def payables_turnover(cogs, average_ap):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Efficiency ratios', 'Working capital']
    function: "Compute payables turnover: COGS / Average Accounts Payable"
    y_as_x: ['days_payables_outstanding_dpo']
    :param cogs: "Cost of goods sold"
    :param average_ap: "Average accounts payable balance"
    :return: "Payables turnover ratio"
    '''
    turnover = cogs / average_ap
    return turnover


def payback_period(initial_outlay, cashflows):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Capital budgeting', 'Project evaluation']
    function: "Compute payback period: the smallest t such that cumulative cash flows >= initial outlay"
    y_as_x: []
    :param initial_outlay: "Initial investment (positive value)"
    :param cashflows: "Array of periodic cash flows (all positive)"
    :return: "Payback period in periods (fractional if interpolated)"
    '''
    cumulative = 0.0
    for t, cf in enumerate(cashflows):
        cumulative += cf
        if cumulative >= initial_outlay:
            if t == 0:
                return initial_outlay / cf
            prev_cumulative = cumulative - cf
            fraction = (initial_outlay - prev_cumulative) / cf
            return t + fraction
    return np.inf


def payment_shock_ratio(new_payment, old_payment):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Underwriting', 'Affordability']
    function: "Compute payment shock ratio: New Payment / Old Payment - 1"
    y_as_x: []
    :param new_payment: "New monthly payment amount"
    :param old_payment: "Previous monthly payment amount"
    :return: "Payment shock ratio as a decimal (0.20 means 20% increase)"
    '''
    shock = new_payment / old_payment - 1
    return shock


def peg_ratio(p_over_e_ratio, earnings_growth):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Valuation multiples', 'Growth-adjusted valuation']
    function: "Compute PEG ratio: (P/E) / Earnings Growth Rate"
    y_as_x: []
    :param p_over_e_ratio: "Price-to-earnings ratio"
    :param earnings_growth: "Earnings growth rate (as a percentage, e.g. 15 for 15%)"
    :return: "PEG ratio"
    '''
    peg = p_over_e_ratio / earnings_growth
    return peg


def percentage_price_oscillator_ppo(close, fastperiod=12, slowperiod=26, matype=1):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Momentum indicators']
    function: "Compute Percentage Price Oscillator (PPO) = (EMA_fast - EMA_slow) / EMA_slow"
    y_as_x: []
    :param close: "Array of closing prices"
    :param fastperiod: "Fast EMA period, default 12"
    :param slowperiod: "Slow EMA period, default 26"
    :param matype: "Moving average type (1=EMA), default 1"
    :return: "PPO values"
    '''
    import talib
    ppo = talib.PPO(close, fastperiod=fastperiod, slowperiod=slowperiod, matype=matype)
    return ppo


def perpetuity_value(cashflow, discount_rate):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Valuation', 'Time value of money']
    function: "Compute perpetuity present value: PV = CF / r"
    y_as_x: ['growing_perpetuity_value']
    :param cashflow: "Constant periodic cash flow"
    :param discount_rate: "Discount rate per period"
    :return: "Present value of the perpetuity"
    '''
    pv = cashflow / discount_rate
    return pv


def piotroski_f_score(roa, operating_cf, delta_roa, ocf_over_ta_vs_roa,
                       delta_leverage, delta_current_ratio, no_new_shares,
                       delta_gross_margin, delta_asset_turnover):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Fundamental analysis', 'Scoring models']
    function: "Compute Piotroski F-score: sum of 9 binary signals assessing profitability, leverage/liquidity, and operating efficiency"
    y_as_x: []
    :param roa: "Return on Assets in current year (positive = 1 point)"
    :param operating_cf: "Operating Cash Flow in current year (positive = 1 point)"
    :param delta_roa: "Change in ROA vs prior year (positive = 1 point)"
    :param ocf_over_ta_vs_roa: "True if Operating CF / Total Assets > ROA (1 point)"
    :param delta_leverage: "Change in long-term leverage ratio (decrease = 1 point)"
    :param delta_current_ratio: "Change in current ratio (increase = 1 point)"
    :param no_new_shares: "True if no new shares issued (1 point)"
    :param delta_gross_margin: "Change in gross margin (increase = 1 point)"
    :param delta_asset_turnover: "Change in asset turnover (increase = 1 point)"
    :return: "Piotroski F-score (integer 0-9)"
    '''
    score = 0
    score += 1 if roa > 0 else 0
    score += 1 if operating_cf > 0 else 0
    score += 1 if delta_roa > 0 else 0
    score += 1 if ocf_over_ta_vs_roa else 0
    score += 1 if delta_leverage < 0 else 0
    score += 1 if delta_current_ratio > 0 else 0
    score += 1 if no_new_shares else 0
    score += 1 if delta_gross_margin > 0 else 0
    score += 1 if delta_asset_turnover > 0 else 0
    return score


def plus_directional_indicator_plusdi(high, low, close, timeperiod=14):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Trend indicators', 'Directional movement']
    function: "Compute Plus Directional Indicator (+DI) = 100 x smoothed +DM / ATR"
    y_as_x: ['average_directional_index_adx', 'adx']
    :param high: "Array of high prices"
    :param low: "Array of low prices"
    :param close: "Array of closing prices"
    :param timeperiod: "Lookback period, default 14"
    :return: "+DI values"
    '''
    import talib
    plus_di = talib.PLUS_DI(high, low, close, timeperiod=timeperiod)
    return plus_di


def pme_kaplan_schoar(distributions, contributions, index_returns, nav_final=0.0):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Performance benchmarking', 'Public market equivalent']
    function: "Compute Kaplan-Schoar PME: ratio of FV of distributions (indexed) plus NAV to FV of contributions (indexed)"
    y_as_x: []
    :param distributions: "Array of distribution amounts by period"
    :param contributions: "Array of contribution amounts by period"
    :param index_returns: "Array of public market index returns per period"
    :param nav_final: "Final NAV of the fund, default 0.0"
    :return: "Kaplan-Schoar PME ratio"
    '''
    n = len(distributions)
    # Compound index from each period to end
    fv_dist = 0.0
    fv_cont = 0.0
    for t in range(n):
        compound = 1.0
        for s in range(t + 1, n):
            compound *= (1 + index_returns[s])
        fv_dist += distributions[t] * compound
        fv_cont += contributions[t] * compound
    fv_dist += nav_final
    pme = fv_dist / fv_cont if fv_cont != 0 else np.nan
    return pme


def po_strip_value(principal_cashflows, discount_factors):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['MBS strips', 'Principal-only']
    function: "Compute PO strip value: PV_PO = sum_t principal_only_cf_t * DF_t"
    y_as_x: []
    :param principal_cashflows: "Array of principal-only cash flows per period"
    :param discount_factors: "Array of discount factors per period"
    :return: "Present value of the PO strip"
    '''
    principal_cashflows = np.asarray(principal_cashflows)
    discount_factors = np.asarray(discount_factors)
    pv_po = np.sum(principal_cashflows * discount_factors)
    return pv_po


def point_in_time_pd(X, macro_state):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['PD estimation', 'Point-in-time models']
    function: "Estimate point-in-time probability of default conditioned on current macroeconomic state using logistic regression"
    y_as_x: []
    :param X: "Feature matrix including borrower characteristics and macro variables"
    :param macro_state: "Current macroeconomic state variables (incorporated into X or as adjustment)"
    :return: "Point-in-time PD estimates"
    '''
    import statsmodels.api as sm
    X_with_const = sm.add_constant(X)
    model = sm.Logit(macro_state, X_with_const)
    result = model.fit(disp=0)
    pd_pit = result.predict(X_with_const)
    return pd_pit


def portfolio_covariance_contribution(weights, covariance_matrix):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Risk decomposition', 'Marginal risk']
    function: "Compute portfolio covariance contribution for each asset: MC_i = (Sigma * w)_i"
    y_as_x: ['component_risk_contribution', 'marginal_risk_contribution']
    :param weights: "Array of portfolio weights"
    :param covariance_matrix: "Covariance matrix of asset returns"
    :return: "Array of marginal covariance contributions per asset"
    '''
    weights = np.asarray(weights)
    covariance_matrix = np.asarray(covariance_matrix)
    mc = covariance_matrix @ weights
    return mc


def portfolio_return(weights, expected_returns):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio construction', 'Return estimation']
    function: "Compute expected portfolio return: E[R_p] = w' * mu"
    y_as_x: ['mean_variance_utility', 'sharpe_ratio']
    :param weights: "Array of portfolio weights"
    :param expected_returns: "Array of expected asset returns"
    :return: "Expected portfolio return"
    '''
    weights = np.asarray(weights)
    expected_returns = np.asarray(expected_returns)
    port_return = weights @ expected_returns
    return port_return


def portfolio_variance(weights, covariance_matrix):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Risk measurement', 'Portfolio construction']
    function: "Compute portfolio variance: sigma_p^2 = w' * Sigma * w"
    y_as_x: ['portfolio_volatility']
    :param weights: "Array of portfolio weights"
    :param covariance_matrix: "Covariance matrix of asset returns"
    :return: "Portfolio variance"
    '''
    weights = np.asarray(weights)
    covariance_matrix = np.asarray(covariance_matrix)
    var = weights @ covariance_matrix @ weights
    return var


def portfolio_volatility(weights, covariance_matrix):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Risk measurement', 'Portfolio construction']
    function: "Compute portfolio volatility: sigma_p = sqrt(w' * Sigma * w)"
    y_as_x: ['sharpe_ratio', 'information_ratio', 'tracking_error', 'marginal_risk_contribution']
    :param weights: "Array of portfolio weights"
    :param covariance_matrix: "Covariance matrix of asset returns"
    :return: "Portfolio volatility (standard deviation)"
    '''
    weights = np.asarray(weights)
    covariance_matrix = np.asarray(covariance_matrix)
    vol = np.sqrt(weights @ covariance_matrix @ weights)
    return vol


def post_money_valuation(pre_money_valuation, new_investment):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Venture capital', 'Valuation']
    function: "Compute post-money valuation: Post-money = Pre-money + New Investment"
    y_as_x: ['ownership_percentage', 'pre_money_valuation']
    :param pre_money_valuation: "Pre-money valuation of the company"
    :param new_investment: "Amount of new investment"
    :return: "Post-money valuation"
    '''
    post_money = pre_money_valuation + new_investment
    return post_money


def potential_future_exposure_pfe(exposure_paths, confidence_level=0.95):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Counterparty credit risk', 'Exposure measurement']
    function: "Compute Potential Future Exposure (PFE) as the quantile of simulated exposure distribution at a given confidence level"
    y_as_x: []
    :param exposure_paths: "Array of simulated exposure values at a given future time (one per path)"
    :param confidence_level: "Confidence level for quantile, default 0.95"
    :return: "PFE at the specified confidence level"
    '''
    pfe = np.percentile(exposure_paths, confidence_level * 100)
    return pfe


def ppi_inflation_month_over_month(ppi_current, ppi_previous):
    '''
    domain: ['Macroeconomics, inflation & price indices']
    subdomain: ['Inflation measurement', 'Producer prices']
    function: "Compute PPI inflation month-over-month: pi_t = PPI_t / PPI_(t-1) - 1"
    y_as_x: ['annualized_ppi_inflation_from_monthly_ppi']
    :param ppi_current: "PPI for the current month"
    :param ppi_previous: "PPI for the previous month"
    :return: "Month-over-month PPI inflation rate"
    '''
    inflation = ppi_current / ppi_previous - 1
    return inflation


def ppi_inflation_year_over_year(ppi_current, ppi_12_months_ago):
    '''
    domain: ['Macroeconomics, inflation & price indices']
    subdomain: ['Inflation measurement', 'Producer prices']
    function: "Compute PPI inflation year-over-year: pi_t = PPI_t / PPI_(t-12) - 1"
    y_as_x: []
    :param ppi_current: "PPI for the current month"
    :param ppi_12_months_ago: "PPI for the same month 12 months ago"
    :return: "Year-over-year PPI inflation rate"
    '''
    inflation = ppi_current / ppi_12_months_ago - 1
    return inflation


def preferred_return_hurdle(contributed_capital, hurdle_rate, periods):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Fund economics', 'Waterfall']
    function: "Compute the preferred return hurdle: Hurdle FV = Contributed Capital x (1+h)^t"
    y_as_x: ['catch_up_distribution', 'fund_carried_interest']
    :param contributed_capital: "Total contributed (paid-in) capital"
    :param hurdle_rate: "Preferred return hurdle rate per period"
    :param periods: "Number of periods"
    :return: "Future value of the hurdle amount"
    '''
    import numpy_financial as npf
    hurdle_fv = npf.fv(hurdle_rate, periods, 0, -contributed_capital)
    return hurdle_fv


def pre_money_valuation(post_money_valuation, new_investment):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Venture capital', 'Valuation']
    function: "Compute pre-money valuation: Pre-money = Post-money - New Investment"
    y_as_x: ['post_money_valuation']
    :param post_money_valuation: "Post-money valuation of the company"
    :param new_investment: "Amount of new investment"
    :return: "Pre-money valuation"
    '''
    pre_money = post_money_valuation - new_investment
    return pre_money


def prepayment_speed_psa(month, psa_pct=100):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Prepayment modeling', 'MBS analysis']
    function: "Compute prepayment speed under the PSA benchmark: CPR_t = min(0.06, 0.002*t) x PSA%"
    y_as_x: ['conditional_prepayment_rate_cpr', 'single_monthly_mortality_smm']
    :param month: "Loan age in months (or array of months)"
    :param psa_pct: "PSA speed as a percentage (100 = 100% PSA), default 100"
    :return: "CPR at the given month(s)"
    '''
    month = np.asarray(month, dtype=float)
    psa_factor = psa_pct / 100.0
    cpr = np.minimum(0.06, 0.002 * month) * psa_factor
    return cpr


def present_value_pv(rate, nper, pmt, fv=0.0):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Time value of money', 'Discounting']
    function: "Compute present value: PV = sum_t CF_t / (1+r)^t using numpy_financial"
    y_as_x: ['net_present_value_npv', 'annuity_present_value', 'profitability_index']
    :param rate: "Discount rate per period"
    :param nper: "Number of periods"
    :param pmt: "Payment per period"
    :param fv: "Future value, default 0.0"
    :return: "Present value"
    '''
    import numpy_financial as npf
    pv = npf.pv(rate, nper, pmt, fv)
    return pv


def present_value_random_variable(benefit_amount, discount_factor, time_of_death):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Life insurance', 'Present value of benefits']
    function: "Compute the present value random variable Z = b_T * v^T for a life insurance contract"
    y_as_x: ['variance_of_loss']
    :param benefit_amount: "Benefit amount b_T paid at time of death"
    :param discount_factor: "Annual discount factor v = 1/(1+i)"
    :param time_of_death: "Time of death T (in years)"
    :return: "Present value of the benefit Z"
    '''
    z = benefit_amount * discount_factor ** time_of_death
    return z


def price_impact(execution_price, mid_price):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Execution cost', 'Market impact']
    function: "Compute price impact: Impact = (execution_price / mid_price - 1) * 100"
    y_as_x: []
    :param execution_price: "Actual execution price"
    :param mid_price: "Mid-market price at time of order"
    :return: "Price impact in percentage points"
    '''
    impact = (execution_price / mid_price - 1) * 100
    return impact


def price_to_book(price, book_value_per_share):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Valuation multiples']
    function: "Compute Price-to-Book ratio: P/B = Price / Book value per share"
    y_as_x: []
    :param price: "Current market price per share"
    :param book_value_per_share: "Book value per share"
    :return: "Price-to-book ratio"
    '''
    pb = price / book_value_per_share
    return pb


def price_to_earnings_ratio(price_per_share, eps):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Valuation multiples']
    function: "Compute Price-to-Earnings ratio: P/E = Price per share / EPS"
    y_as_x: ['peg_ratio', 'earnings_yield']
    :param price_per_share: "Current market price per share"
    :param eps: "Earnings per share"
    :return: "P/E ratio"
    '''
    pe = price_per_share / eps
    return pe


def price_to_sales(market_cap, revenue):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Valuation multiples']
    function: "Compute Price-to-Sales ratio: P/S = Market Cap / Revenue"
    y_as_x: []
    :param market_cap: "Market capitalization"
    :param revenue: "Total revenue"
    :return: "Price-to-sales ratio"
    '''
    ps = market_cap / revenue
    return ps


def principal_payment_portion_ppmt(rate, per, nper, pv, fv=0.0):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Loan amortization', 'Payment breakdown']
    function: "Compute the principal payment portion (PPMT) for a given period: PPMT_t = PMT - IPMT_t"
    y_as_x: []
    :param rate: "Interest rate per period"
    :param per: "Period for which to compute the principal payment (1-indexed)"
    :param nper: "Total number of payment periods"
    :param pv: "Present value (loan amount)"
    :param fv: "Future value, default 0.0"
    :return: "Principal payment portion for the specified period"
    '''
    import numpy_financial as npf
    ppmt = npf.ppmt(rate, per, nper, pv, fv)
    return ppmt


def probability_of_default_from_hazard_rate(hazard_rate, time_horizon):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Hazard rate models', 'PD estimation']
    function: "Compute probability of default from hazard rate: PD(0,T) = 1 - exp(-integral_0^T lambda(t) dt)"
    y_as_x: ['expected_loss', 'expected_credit_loss_ifrs_9_over_cecl', 'survival_probability']
    :param hazard_rate: "Constant hazard rate lambda (or array for time-varying)"
    :param time_horizon: "Time horizon T in years (or array of time steps for time-varying hazard)"
    :return: "Cumulative probability of default over [0, T]"
    '''
    if np.isscalar(hazard_rate):
        pd = 1 - np.exp(-hazard_rate * time_horizon)
    else:
        hazard_rate = np.asarray(hazard_rate)
        time_horizon = np.asarray(time_horizon)
        cumulative_hazard = np.trapz(hazard_rate, time_horizon)
        pd = 1 - np.exp(-cumulative_hazard)
    return pd


def probability_of_default_from_logit(X, beta):
    '''
    domain: ['Credit risk']
    subdomain: ['PD modeling', 'Logistic regression']
    function: "Compute probability of default from logistic regression: PD = 1 / (1 + exp(-X*beta))"
    y_as_x: ['expected_loss', 'expected_credit_loss_ifrs_9_over_cecl', 'basel_irb_capital_requirement']
    :param X: "Feature matrix (n_samples x n_features)"
    :param beta: "Coefficient vector from logistic regression"
    :return: "Array of default probabilities"
    '''
    from sklearn.linear_model import LogisticRegression
    X = np.asarray(X)
    beta = np.asarray(beta)
    linear = X @ beta
    pd = 1.0 / (1.0 + np.exp(-linear))
    return pd


def probability_of_default_scorecard_logit(X_train, y_train, X_predict):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Scorecard modeling', 'PD estimation']
    function: "Estimate probability of default using scorecard logistic regression: logit(PD) = beta0 + beta'x"
    y_as_x: []
    :param X_train: "Training feature matrix"
    :param y_train: "Training default labels (0/1)"
    :param X_predict: "Feature matrix for prediction"
    :return: "Array of predicted default probabilities"
    '''
    from sklearn.linear_model import LogisticRegression
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    pd = model.predict_proba(X_predict)[:, 1]
    return pd


def probit_default_model(y, X):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['PD modeling', 'Probit regression']
    function: "Fit a probit default model: Phi^-1(PD_i) = beta0 + beta'x_i"
    y_as_x: []
    :param y: "Binary default indicator array (0/1)"
    :param X: "Feature matrix of borrower characteristics"
    :return: "Fitted probit model results object"
    '''
    import statsmodels.api as sm
    X_with_const = sm.add_constant(X)
    model = sm.Probit(y, X_with_const)
    result = model.fit(disp=0)
    return result


def probit_score(X, beta):
    '''
    domain: ['Quantitative forecasting & machine learning in finance']
    subdomain: ['Classification', 'Probit models']
    function: "Compute probit score: P(y=1|x) = Phi(beta'x) where Phi is the standard normal CDF"
    y_as_x: []
    :param X: "Feature matrix (n_samples x n_features)"
    :param beta: "Coefficient vector from probit model"
    :return: "Array of predicted probabilities"
    '''
    X = np.asarray(X)
    beta = np.asarray(beta)
    linear = X @ beta
    prob = stats.norm.cdf(linear)
    return prob


def producer_price_index_laspeyres_style_index(prices_current, prices_base, quantities_base):
    '''
    domain: ['Macroeconomics, inflation & price indices']
    subdomain: ['Price indices', 'Producer prices']
    function: "Compute Producer Price Index (Laspeyres-style): PPI_t = (sum_i p_(i,t) * q_(i,0) / sum_i p_(i,0) * q_(i,0)) x 100"
    y_as_x: ['ppi_inflation_month_over_month', 'ppi_inflation_year_over_year', 'cumulative_inflation_factor_from_ppi']
    :param prices_current: "Array of current-period prices for each item"
    :param prices_base: "Array of base-period prices for each item"
    :param quantities_base: "Array of base-period quantities for each item"
    :return: "PPI value (base period = 100)"
    '''
    prices_current = np.asarray(prices_current)
    prices_base = np.asarray(prices_base)
    quantities_base = np.asarray(quantities_base)
    numerator = np.sum(prices_current * quantities_base)
    denominator = np.sum(prices_base * quantities_base)
    ppi = (numerator / denominator) * 100
    return ppi
