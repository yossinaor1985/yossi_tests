"""
Financial Functions - Batch 3 (Equations 204-305)
"""
import numpy as np
import pandas as pd
from scipy import stats


# ---------------------------------------------------------------------------
# 1. currency_basket_index
# ---------------------------------------------------------------------------
def currency_basket_index(spot_rates, weights):
    '''
    domain: ['FX & international finance']
    subdomain: ['Currency baskets & indices']
    function: "Computes a geometric currency basket index as the product of spot exchange rates raised to their respective basket weights."
    y_as_x: []
    :param spot_rates: "Array of spot exchange rates S_{i,t} for each currency in the basket"
    :param weights: "Array of portfolio weights w_i for each currency, summing to 1"
    :return: "Currency basket index value: Index_t = prod_i S_{i,t}^{w_i}"
    '''
    spot_rates = np.asarray(spot_rates, dtype=float)
    weights = np.asarray(weights, dtype=float)
    return np.prod(spot_rates ** weights)


# ---------------------------------------------------------------------------
# 2. currency_carry_return
# ---------------------------------------------------------------------------
def currency_carry_return(i_high, i_low, fx_change):
    '''
    domain: ['FX & international finance']
    subdomain: ['Currency carry trades']
    function: "Computes the return from a currency carry trade, which involves borrowing in a low-interest-rate currency and investing in a high-interest-rate currency, adjusted for FX movements."
    y_as_x: []
    :param i_high: "Interest rate of the high-yield (investment) currency"
    :param i_low: "Interest rate of the low-yield (funding) currency"
    :param fx_change: "Change in the exchange rate over the holding period (positive means high-yield currency appreciated)"
    :return: "Currency carry return: Carry = i_high - i_low + FX change"
    '''
    return i_high - i_low + fx_change


# ---------------------------------------------------------------------------
# 3. current_ratio
# ---------------------------------------------------------------------------
def current_ratio(current_assets, current_liabilities):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Liquidity ratios']
    function: "Computes the current ratio, a liquidity metric indicating the firm's ability to meet short-term obligations from current assets."
    y_as_x: ['cash_conversion_cycle_ccc', 'piotroski_f_score']
    :param current_assets: "Total current assets on the balance sheet"
    :param current_liabilities: "Total current liabilities on the balance sheet"
    :return: "Current Ratio = Current Assets / Current Liabilities"
    '''
    return current_assets / current_liabilities


# ---------------------------------------------------------------------------
# 4. current_yield
# ---------------------------------------------------------------------------
def current_yield(annual_coupon, bond_price):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Bond yield measures']
    function: "Computes the current yield of a bond, which relates the annual coupon payment to the current market price."
    y_as_x: []
    :param annual_coupon: "Annual coupon payment of the bond"
    :param bond_price: "Current market price of the bond"
    :return: "Current Yield = Annual Coupon / Bond Price"
    '''
    return annual_coupon / bond_price


# ---------------------------------------------------------------------------
# 5. curtate_expected_future_lifetime
# ---------------------------------------------------------------------------
def curtate_expected_future_lifetime(survival_probs):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Life contingencies & mortality']
    function: "Computes the curtate expected future lifetime, which is the expected number of complete years lived beyond age x."
    y_as_x: []
    :param survival_probs: "Array of k-year survival probabilities {}_kp_x for k = 1, 2, 3, ... representing the probability that a life aged x survives at least k more years"
    :return: "Curtate expected future lifetime: e_x = sum_{k>=1} {}_kp_x"
    '''
    try:
        from actuarialmath import LifeTable
        # Use actuarialmath if a LifeTable object is passed
        if hasattr(survival_probs, 'e_x'):
            return survival_probs.e_x()
    except ImportError:
        pass
    return float(np.sum(survival_probs))


# ---------------------------------------------------------------------------
# 6. cva_capital_proxy
# ---------------------------------------------------------------------------
def cva_capital_proxy(ead, lgd, pd, maturity, risk_weight_factor=1.0):
    '''
    domain: ['Bank regulation, Basel & prudential ratios']
    subdomain: ['Counterparty credit risk & CVA']
    function: "Computes a proxy for the Credit Valuation Adjustment (CVA) capital charge under Basel III standardised approach, capturing potential mark-to-market losses from counterparty default."
    y_as_x: []
    :param ead: "Exposure at default for the counterparty"
    :param lgd: "Loss given default fraction for the counterparty"
    :param pd: "Probability of default of the counterparty"
    :param maturity: "Effective maturity of the exposure in years"
    :param risk_weight_factor: "Supervisory risk weight scaling factor (default 1.0)"
    :return: "CVA capital proxy charge based on sensitivity or standardized approach"
    '''
    return risk_weight_factor * ead * lgd * pd * maturity


# ---------------------------------------------------------------------------
# 7. d1
# ---------------------------------------------------------------------------
def d1(S, K, r, sigma, T):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Black-Scholes model components']
    function: "Computes d1, the first argument to the cumulative normal distribution in the Black-Scholes formula, measuring how far the option is in-the-money adjusted for volatility and time."
    y_as_x: ['d2', 'delta_call', 'delta_put', 'gamma', 'theta', 'vega', 'vanna', 'vomma_over_volga', 'black_scholes_call', 'black_scholes_put', 'digital_call_price', 'digital_put_price']
    :param S: "Current price of the underlying asset"
    :param K: "Strike price of the option"
    :param r: "Risk-free interest rate (annualized, continuous compounding)"
    :param sigma: "Volatility of the underlying asset (annualized)"
    :param T: "Time to expiration in years"
    :return: "d1 = [ln(S/K) + (r + 0.5*sigma^2)*T] / (sigma*sqrt(T))"
    '''
    return (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))


# ---------------------------------------------------------------------------
# 8. d2
# ---------------------------------------------------------------------------
def d2(d1_val, sigma, T):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Black-Scholes model components']
    function: "Computes d2, the second argument to the cumulative normal distribution in the Black-Scholes formula, derived from d1."
    y_as_x: ['digital_call_price', 'digital_put_price', 'black_scholes_call', 'black_scholes_put', 'rho', 'theta']
    :param d1_val: "The d1 value from the Black-Scholes formula"
    :param sigma: "Volatility of the underlying asset (annualized)"
    :param T: "Time to expiration in years"
    :return: "d2 = d1 - sigma*sqrt(T)"
    '''
    return d1_val - sigma * np.sqrt(T)


# ---------------------------------------------------------------------------
# 9. days_inventory_outstanding_dio
# ---------------------------------------------------------------------------
def days_inventory_outstanding_dio(average_inventory, cogs):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Activity / efficiency ratios']
    function: "Computes days inventory outstanding, measuring how many days on average it takes to sell inventory."
    y_as_x: ['cash_conversion_cycle_ccc']
    :param average_inventory: "Average inventory over the period"
    :param cogs: "Cost of goods sold over the period"
    :return: "DIO = 365 * Average Inventory / COGS"
    '''
    return 365.0 * average_inventory / cogs


# ---------------------------------------------------------------------------
# 10. days_payables_outstanding_dpo
# ---------------------------------------------------------------------------
def days_payables_outstanding_dpo(average_ap, cogs):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Activity / efficiency ratios']
    function: "Computes days payables outstanding, measuring how many days on average a company takes to pay its suppliers."
    y_as_x: ['cash_conversion_cycle_ccc']
    :param average_ap: "Average accounts payable over the period"
    :param cogs: "Cost of goods sold over the period"
    :return: "DPO = 365 * Average AP / COGS"
    '''
    return 365.0 * average_ap / cogs


# ---------------------------------------------------------------------------
# 11. days_sales_outstanding_dso
# ---------------------------------------------------------------------------
def days_sales_outstanding_dso(average_ar, revenue):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Activity / efficiency ratios']
    function: "Computes days sales outstanding, measuring how many days on average it takes to collect revenue after a sale."
    y_as_x: ['cash_conversion_cycle_ccc']
    :param average_ar: "Average accounts receivable over the period"
    :param revenue: "Total revenue over the period"
    :return: "DSO = 365 * Average AR / Revenue"
    '''
    return 365.0 * average_ar / revenue


# ---------------------------------------------------------------------------
# 12. days_to_liquidate
# ---------------------------------------------------------------------------
def days_to_liquidate(position_size, adv, participation_limit):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Position liquidation metrics']
    function: "Computes the estimated number of days required to liquidate a position given average daily volume and a participation rate constraint."
    y_as_x: []
    :param position_size: "Total size of the position to be liquidated (in shares or notional)"
    :param adv: "Average daily volume traded in the security"
    :param participation_limit: "Maximum fraction of daily volume that the trader is willing to capture (e.g., 0.10 for 10%)"
    :return: "DTL = Position Size / (ADV * Participation Limit)"
    '''
    return position_size / (adv * participation_limit)


# ---------------------------------------------------------------------------
# 13. death_probability
# ---------------------------------------------------------------------------
def death_probability(survival_prob):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Life contingencies & mortality']
    function: "Computes the t-year death probability for a life aged x, given the corresponding survival probability."
    y_as_x: []
    :param survival_prob: "The t-year survival probability {}_tp_x for a life aged x"
    :return: "Death probability: {}_tq_x = 1 - {}_tp_x"
    '''
    return 1.0 - survival_prob


# ---------------------------------------------------------------------------
# 14. debt_burden_ratio
# ---------------------------------------------------------------------------
def debt_burden_ratio(total_debt_service, gross_income):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Debt affordability ratios']
    function: "Computes the debt burden ratio, measuring what fraction of gross income is consumed by total debt service payments."
    y_as_x: []
    :param total_debt_service: "Total periodic debt service payments (interest + principal + lease/rent if applicable)"
    :param gross_income: "Borrower's gross periodic income"
    :return: "Debt Burden = Total Debt Service / Gross Income"
    '''
    return total_debt_service / gross_income


# ---------------------------------------------------------------------------
# 15. debt_service
# ---------------------------------------------------------------------------
def debt_service(interest, scheduled_principal, lease_rent=0.0):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Debt affordability ratios']
    function: "Computes total debt service, summing interest payments, scheduled principal repayments, and optionally lease or rent obligations."
    y_as_x: ['debt_burden_ratio', 'debt_service_coverage_ratio_dscr', 'break_even_occupancy']
    :param interest: "Periodic interest payment obligation"
    :param scheduled_principal: "Scheduled principal repayment for the period"
    :param lease_rent: "Lease or rent payment included in debt service, if applicable (default 0)"
    :return: "Debt Service = Interest + Scheduled Principal + Lease/Rent"
    '''
    return interest + scheduled_principal + lease_rent


# ---------------------------------------------------------------------------
# 16. debt_service_coverage_ratio_dscr
# ---------------------------------------------------------------------------
def debt_service_coverage_ratio_dscr(net_operating_income, debt_service_amount):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Credit & project finance ratios']
    function: "Computes the debt service coverage ratio, a key metric for lenders indicating how many times net operating income covers required debt service."
    y_as_x: []
    :param net_operating_income: "Net operating income of the project or property"
    :param debt_service_amount: "Total periodic debt service obligation"
    :return: "DSCR = Net Operating Income / Debt Service"
    '''
    return net_operating_income / debt_service_amount


# ---------------------------------------------------------------------------
# 17. debt_yield
# ---------------------------------------------------------------------------
def debt_yield(net_operating_income, loan_amount):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Credit & project finance ratios']
    function: "Computes the debt yield, a lender's underwriting metric expressing net operating income as a percentage of loan amount, independent of interest rate or amortization."
    y_as_x: []
    :param net_operating_income: "Net operating income of the property or project"
    :param loan_amount: "Total loan amount outstanding"
    :return: "Debt Yield = Net Operating Income / Loan Amount"
    '''
    return net_operating_income / loan_amount


# ---------------------------------------------------------------------------
# 18. debt_to_assets
# ---------------------------------------------------------------------------
def debt_to_assets(debt, assets):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Leverage ratios']
    function: "Computes the debt-to-assets ratio, measuring the proportion of a company's assets that are financed by debt."
    y_as_x: []
    :param debt: "Total debt of the company"
    :param assets: "Total assets of the company"
    :return: "Debt_to_assets = Debt / Assets"
    '''
    return debt / assets


# ---------------------------------------------------------------------------
# 19. debt_to_equity
# ---------------------------------------------------------------------------
def debt_to_equity(debt, equity):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Leverage ratios']
    function: "Computes the debt-to-equity ratio, measuring the degree of financial leverage by comparing total debt to shareholders' equity."
    y_as_x: ['levered_beta_hamada', 'unlevered_beta']
    :param debt: "Total debt of the company"
    :param equity: "Total shareholders' equity of the company"
    :return: "Debt_to_equity = Debt / Equity"
    '''
    return debt / equity


# ---------------------------------------------------------------------------
# 20. debt_to_income_residual
# ---------------------------------------------------------------------------
def debt_to_income_residual(net_income, taxes, housing_costs, other_debt_payments):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Debt affordability ratios']
    function: "Computes residual income, which is the amount of income remaining after deducting taxes, housing costs, and other debt payments."
    y_as_x: []
    :param net_income: "Borrower's net income"
    :param taxes: "Income tax obligation for the period"
    :param housing_costs: "Monthly housing costs (mortgage/rent, insurance, taxes)"
    :param other_debt_payments: "All other monthly debt payments (auto, student loans, credit cards, etc.)"
    :return: "Residual Income = Net Income - Taxes - Housing Costs - Other Debt Payments"
    '''
    return net_income - taxes - housing_costs - other_debt_payments


# ---------------------------------------------------------------------------
# 21. decreasing_annuity
# ---------------------------------------------------------------------------
def decreasing_annuity(x, n, interest_rate, life_table=None):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Life annuities']
    function: "Computes the actuarial present value of a decreasing annuity, where payments decrease by 1 each year, weighted by survival probabilities."
    y_as_x: []
    :param x: "Current age of the annuitant"
    :param n: "Duration of the annuity in years"
    :param interest_rate: "Annual effective interest rate for discounting"
    :param life_table: "Mortality/life table object or array of k-year survival probabilities for ages x+1 through x+n (optional; if None, assumes certain annuity)"
    :return: "(Da)_{x:n} = E[sum_{k=1}^n (n-k+1) v^k 1(T_x>=k)]"
    '''
    v = 1.0 / (1.0 + interest_rate)
    result = 0.0
    for k in range(1, n + 1):
        if life_table is not None:
            kpx = life_table[k - 1] if hasattr(life_table, '__getitem__') else 1.0
        else:
            kpx = 1.0
        result += (n - k + 1) * (v ** k) * kpx
    return result


# ---------------------------------------------------------------------------
# 22. default_rate
# ---------------------------------------------------------------------------
def default_rate(defaults, balance):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Pool performance metrics']
    function: "Computes the default rate of a loan pool as the ratio of defaulted balance to the current or original pool balance."
    y_as_x: []
    :param defaults: "Dollar amount of defaults in the period"
    :param balance: "Current or original pool balance used as denominator"
    :return: "Default Rate = Defaults / Balance"
    '''
    return defaults / balance


# ---------------------------------------------------------------------------
# 23. delinquency_ratio
# ---------------------------------------------------------------------------
def delinquency_ratio(delinquent_loans, gross_loans):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Credit quality metrics']
    function: "Computes the delinquency ratio, measuring the fraction of the loan portfolio that is past due."
    y_as_x: ['delinquency_trigger']
    :param delinquent_loans: "Total outstanding balance of delinquent loans"
    :param gross_loans: "Total gross loan portfolio balance"
    :return: "Delinquency Ratio = Delinquent Loans / Gross Loans"
    '''
    return delinquent_loans / gross_loans


# ---------------------------------------------------------------------------
# 24. delinquency_trigger
# ---------------------------------------------------------------------------
def delinquency_trigger(delinquency_ratio_val, threshold):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Pool performance triggers']
    function: "Evaluates whether a delinquency trigger has been breached in a securitization structure, which may redirect cash flows to protect senior tranches."
    y_as_x: []
    :param delinquency_ratio_val: "Current delinquency ratio of the pool (output of delinquency_ratio function)"
    :param threshold: "Trigger threshold for the delinquency ratio"
    :return: "Boolean indicating whether the trigger is breached (True if delinquency_ratio > threshold)"
    '''
    return delinquency_ratio_val > threshold


# ---------------------------------------------------------------------------
# 25. delta_call
# ---------------------------------------------------------------------------
def delta_call(S, K, r, sigma, T, q=0.0):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Option Greeks']
    function: "Computes the delta of a European call option, representing the sensitivity of the call price to changes in the underlying asset price."
    y_as_x: []
    :param S: "Current price of the underlying asset"
    :param K: "Strike price of the option"
    :param r: "Risk-free interest rate (annualized, continuous compounding)"
    :param sigma: "Volatility of the underlying asset (annualized)"
    :param T: "Time to expiration in years"
    :param q: "Continuous dividend yield of the underlying (default 0)"
    :return: "Delta = e^{-qT} * N(d1)"
    '''
    d1_val = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    return np.exp(-q * T) * stats.norm.cdf(d1_val)


# ---------------------------------------------------------------------------
# 26. delta_put
# ---------------------------------------------------------------------------
def delta_put(S, K, r, sigma, T, q=0.0):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Option Greeks']
    function: "Computes the delta of a European put option, representing the sensitivity of the put price to changes in the underlying asset price."
    y_as_x: []
    :param S: "Current price of the underlying asset"
    :param K: "Strike price of the option"
    :param r: "Risk-free interest rate (annualized, continuous compounding)"
    :param sigma: "Volatility of the underlying asset (annualized)"
    :param T: "Time to expiration in years"
    :param q: "Continuous dividend yield of the underlying (default 0)"
    :return: "Delta = -e^{-qT} * N(-d1)"
    '''
    d1_val = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    return -np.exp(-q * T) * stats.norm.cdf(-d1_val)


# ---------------------------------------------------------------------------
# 27. delta_normal_var
# ---------------------------------------------------------------------------
def delta_normal_var(delta, cov_matrix, z_alpha=None, alpha=0.05):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Value-at-Risk models']
    function: "Computes delta-normal Value-at-Risk for a portfolio of linear positions by combining position deltas with the covariance matrix of risk factors."
    y_as_x: []
    :param delta: "Vector of position sensitivities (deltas) to risk factors"
    :param cov_matrix: "Covariance matrix of risk factor returns (Sigma)"
    :param z_alpha: "Z-score for the confidence level (if None, derived from alpha)"
    :param alpha: "Significance level (default 0.05 for 95% confidence)"
    :return: "VaR = z_alpha * sqrt(Delta' * Sigma * Delta)"
    '''
    delta = np.asarray(delta, dtype=float)
    cov_matrix = np.asarray(cov_matrix, dtype=float)
    if z_alpha is None:
        z_alpha = stats.norm.ppf(1 - alpha)
    portfolio_var = float(delta @ cov_matrix @ delta)
    return z_alpha * np.sqrt(portfolio_var)


# ---------------------------------------------------------------------------
# 28. deposit_beta
# ---------------------------------------------------------------------------
def deposit_beta(deposit_rate_changes, market_rate_changes):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Asset-liability management & funding']
    function: "Estimates the deposit beta, the sensitivity of deposit rates to market rate changes, via OLS regression."
    y_as_x: []
    :param deposit_rate_changes: "Array of period-over-period changes in deposit rates"
    :param market_rate_changes: "Array of period-over-period changes in the benchmark market rate"
    :return: "Deposit Beta = slope coefficient from OLS regression of deposit rate changes on market rate changes"
    '''
    import statsmodels.api as sm
    X = sm.add_constant(np.asarray(market_rate_changes, dtype=float))
    y = np.asarray(deposit_rate_changes, dtype=float)
    model = sm.OLS(y, X).fit()
    return model.params[1]


# ---------------------------------------------------------------------------
# 29. detrended_price_oscillator_dpo
# ---------------------------------------------------------------------------
def detrended_price_oscillator_dpo(close, period=20):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Oscillators']
    function: "Computes the Detrended Price Oscillator, which removes the trend from prices to identify cycles by comparing a shifted price to its simple moving average."
    y_as_x: []
    :param close: "Array or Series of closing prices"
    :param period: "Look-back period for the SMA (default 20)"
    :return: "DPO = Price shifted back by (period/2 + 1) periods minus SMA of close"
    '''
    close = pd.Series(close, dtype=float)
    sma = close.rolling(window=period).mean()
    shift = period // 2 + 1
    dpo = close.shift(shift) - sma
    return dpo


# ---------------------------------------------------------------------------
# 30. digital_call_price
# ---------------------------------------------------------------------------
def digital_call_price(S, K, r, sigma, T):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Exotic options']
    function: "Computes the price of a European digital (binary) call option, which pays a fixed amount if the underlying is above the strike at expiration."
    y_as_x: []
    :param S: "Current price of the underlying asset"
    :param K: "Strike price of the option"
    :param r: "Risk-free interest rate (annualized, continuous compounding)"
    :param sigma: "Volatility of the underlying asset (annualized)"
    :param T: "Time to expiration in years"
    :return: "Digital Call = e^{-rT} * N(d2)"
    '''
    d1_val = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2_val = d1_val - sigma * np.sqrt(T)
    return np.exp(-r * T) * stats.norm.cdf(d2_val)


# ---------------------------------------------------------------------------
# 31. digital_put_price
# ---------------------------------------------------------------------------
def digital_put_price(S, K, r, sigma, T):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Exotic options']
    function: "Computes the price of a European digital (binary) put option, which pays a fixed amount if the underlying is below the strike at expiration."
    y_as_x: []
    :param S: "Current price of the underlying asset"
    :param K: "Strike price of the option"
    :param r: "Risk-free interest rate (annualized, continuous compounding)"
    :param sigma: "Volatility of the underlying asset (annualized)"
    :param T: "Time to expiration in years"
    :return: "Digital Put = e^{-rT} * N(-d2)"
    '''
    d1_val = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2_val = d1_val - sigma * np.sqrt(T)
    return np.exp(-r * T) * stats.norm.cdf(-d2_val)


# ---------------------------------------------------------------------------
# 32. diluted_eps
# ---------------------------------------------------------------------------
def diluted_eps(diluted_net_income, diluted_shares):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Earnings metrics']
    function: "Computes diluted earnings per share, accounting for all potentially dilutive securities such as options, warrants, and convertible instruments."
    y_as_x: []
    :param diluted_net_income: "Net income available to common shareholders adjusted for dilutive effects"
    :param diluted_shares: "Weighted average diluted shares outstanding including the impact of all dilutive securities"
    :return: "Diluted EPS = Diluted Net Income Available to Common / Diluted Shares"
    '''
    return diluted_net_income / diluted_shares


# ---------------------------------------------------------------------------
# 33. dirty_price
# ---------------------------------------------------------------------------
def dirty_price(clean_price_val, accrued_interest):
    '''
    domain: ['Fixed income & bond math']
    subdomain: ['Bond pricing']
    function: "Computes the dirty (invoice) price of a bond as the sum of the clean price and accrued interest since the last coupon date."
    y_as_x: []
    :param clean_price_val: "Clean price of the bond (excluding accrued interest)"
    :param accrued_interest: "Accrued interest from the last coupon date to the settlement date"
    :return: "Dirty Price = Clean Price + Accrued Interest"
    '''
    return clean_price_val + accrued_interest


# ---------------------------------------------------------------------------
# 34. discount_factor
# ---------------------------------------------------------------------------
def discount_factor(r, t):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Time value of money']
    function: "Computes the discount factor, representing the present value of one unit of currency received at a future time t."
    y_as_x: ['expected_credit_loss_ifrs_9_over_cecl', 'lifetime_ecl', 'forward_rate_from_discount_factors', 'compounded_forward_rate', 'fra_rate', 'cds_premium_leg']
    :param r: "Periodic discount rate (e.g., annual rate)"
    :param t: "Number of periods until payment"
    :return: "DF_t = 1 / (1 + r)^t"
    '''
    return 1.0 / (1.0 + r) ** t


# ---------------------------------------------------------------------------
# 35. discount_yield_t_bill
# ---------------------------------------------------------------------------
def discount_yield_t_bill(face_value, price, days_to_maturity):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Money market instruments']
    function: "Computes the discount yield for a Treasury bill, which quotes the return on a bank discount basis."
    y_as_x: []
    :param face_value: "Face (par) value of the T-bill"
    :param price: "Purchase price of the T-bill"
    :param days_to_maturity: "Number of days until the T-bill matures"
    :return: "Discount Yield = (F - P) / F * 360 / d"
    '''
    return (face_value - price) / face_value * 360.0 / days_to_maturity


# ---------------------------------------------------------------------------
# 36. discounted_payback_period
# ---------------------------------------------------------------------------
def discounted_payback_period(initial_outlay, cash_flows, rate):
    '''
    domain: ['Corporate finance & capital budgeting']
    subdomain: ['Capital budgeting decision rules']
    function: "Computes the discounted payback period, which is the minimum number of periods required for the sum of discounted cash flows to equal or exceed the initial investment."
    y_as_x: []
    :param initial_outlay: "Initial investment outlay (positive number)"
    :param cash_flows: "Array of expected periodic cash flows"
    :param rate: "Discount rate per period"
    :return: "Discounted Payback = min{t : sum_{i<=t} CF_i / (1+r)^i >= Initial Outlay}"
    '''
    cumulative = 0.0
    for t, cf in enumerate(cash_flows, start=1):
        cumulative += cf / (1.0 + rate) ** t
        if cumulative >= initial_outlay:
            # Interpolate the fractional year
            prev_cum = cumulative - cf / (1.0 + rate) ** t
            remaining = initial_outlay - prev_cum
            fraction = remaining / (cf / (1.0 + rate) ** t)
            return (t - 1) + fraction
    return np.nan  # Payback never achieved


# ---------------------------------------------------------------------------
# 37. distance_to_default_dd
# ---------------------------------------------------------------------------
def distance_to_default_dd(V_A, D, mu_A, sigma_A, T):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Structural credit models']
    function: "Computes the Merton distance to default, measuring how many standard deviations the firm's asset value is from the default barrier."
    y_as_x: ['kmv_expected_default_frequency', 'merton_structural_pd']
    :param V_A: "Current market value of the firm's assets"
    :param D: "Face value of debt (default barrier)"
    :param mu_A: "Expected return on the firm's assets (drift)"
    :param sigma_A: "Volatility of the firm's assets"
    :param T: "Time horizon in years"
    :return: "DD = [ln(V_A/D) + (mu_A - 0.5*sigma_A^2)*T] / (sigma_A * sqrt(T))"
    '''
    return (np.log(V_A / D) + (mu_A - 0.5 * sigma_A ** 2) * T) / (sigma_A * np.sqrt(T))


# ---------------------------------------------------------------------------
# 38. diversification_ratio
# ---------------------------------------------------------------------------
def diversification_ratio(weights, cov_matrix):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio risk decomposition']
    function: "Computes the diversification ratio, which compares the weighted average of individual asset volatilities to the portfolio volatility, measuring the benefit of diversification."
    y_as_x: []
    :param weights: "Array of portfolio weights"
    :param cov_matrix: "Covariance matrix of asset returns"
    :return: "DR = sum_i w_i * sigma_i / sigma_p, where sigma_p = sqrt(w' Sigma w)"
    '''
    w = np.asarray(weights, dtype=float)
    cov = np.asarray(cov_matrix, dtype=float)
    individual_vols = np.sqrt(np.diag(cov))
    weighted_vol_sum = np.dot(w, individual_vols)
    portfolio_vol = np.sqrt(w @ cov @ w)
    return weighted_vol_sum / portfolio_vol


# ---------------------------------------------------------------------------
# 39. dividend_coverage
# ---------------------------------------------------------------------------
def dividend_coverage(eps_val, dps):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Dividend analysis']
    function: "Computes the dividend coverage ratio, indicating how many times earnings per share covers dividends per share."
    y_as_x: []
    :param eps_val: "Earnings per share"
    :param dps: "Dividends per share"
    :return: "Coverage = EPS / DPS"
    '''
    return eps_val / dps


# ---------------------------------------------------------------------------
# 40. dividend_discount_model_ddm
# ---------------------------------------------------------------------------
def dividend_discount_model_ddm(dividends, discount_rate):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Equity valuation']
    function: "Computes the intrinsic value of a stock using the general dividend discount model, discounting all expected future dividends."
    y_as_x: []
    :param dividends: "Array of expected future dividends D_t for t = 1, 2, ... T"
    :param discount_rate: "Required rate of return for equity"
    :return: "P_0 = sum_t D_t / (1 + r)^t"
    '''
    pv = 0.0
    for t, d in enumerate(dividends, start=1):
        pv += d / (1.0 + discount_rate) ** t
    return pv


# ---------------------------------------------------------------------------
# 41. dividend_discount_model_gordon_growth
# ---------------------------------------------------------------------------
def dividend_discount_model_gordon_growth(D1, r, g):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Dividend valuation models']
    function: "Computes the intrinsic value of a stock using the Gordon Growth Model, assuming dividends grow at a constant rate in perpetuity."
    y_as_x: []
    :param D1: "Expected dividend in the next period"
    :param r: "Required rate of return on equity"
    :param g: "Constant growth rate of dividends (must be less than r)"
    :return: "P_0 = D_1 / (r - g)"
    '''
    return D1 / (r - g)


# ---------------------------------------------------------------------------
# 42. dividend_payout_ratio
# ---------------------------------------------------------------------------
def dividend_payout_ratio(dividends, net_income):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Dividend metrics']
    function: "Computes the dividend payout ratio, indicating the proportion of net income distributed as dividends."
    y_as_x: ['retention_ratio', 'sustainable_growth_rate']
    :param dividends: "Total dividends paid in the period"
    :param net_income: "Net income for the period"
    :return: "Payout = Dividends / Net Income"
    '''
    return dividends / net_income


# ---------------------------------------------------------------------------
# 43. dividend_yield
# ---------------------------------------------------------------------------
def dividend_yield(annual_dividend_per_share, price_per_share):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Equity valuation']
    function: "Computes the dividend yield, expressing the annual dividend as a percentage of the current share price."
    y_as_x: ['cost_of_equity_dividend_growth']
    :param annual_dividend_per_share: "Annual dividend per share"
    :param price_per_share: "Current market price per share"
    :return: "Dividend Yield = Annual Dividend per Share / Price per Share"
    '''
    return annual_dividend_per_share / price_per_share


# ---------------------------------------------------------------------------
# 44. dollar_duration
# ---------------------------------------------------------------------------
def dollar_duration(modified_duration, price):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Bond risk measures']
    function: "Computes the dollar duration of a bond, which measures the dollar change in bond price for a one-unit change in yield."
    y_as_x: []
    :param modified_duration: "Modified duration of the bond"
    :param price: "Current market price of the bond"
    :return: "Dollar Duration = Modified Duration * Price"
    '''
    return modified_duration * price


# ---------------------------------------------------------------------------
# 45. dollar_volume
# ---------------------------------------------------------------------------
def dollar_volume(price, shares_traded):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Volume & trading activity']
    function: "Computes the dollar volume of trading, used as a measure of liquidity."
    y_as_x: ['amihud_illiquidity']
    :param price: "Price of the security (or average price over the period)"
    :param shares_traded: "Number of shares traded"
    :return: "Dollar Volume = Price * Shares Traded"
    '''
    return price * shares_traded


# ---------------------------------------------------------------------------
# 46. donchian_channel_lower
# ---------------------------------------------------------------------------
def donchian_channel_lower(low, period=20):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Volatility & channel indicators']
    function: "Computes the lower Donchian channel as the rolling minimum of the low price over the specified period."
    y_as_x: []
    :param low: "Array or Series of low prices"
    :param period: "Look-back period for the rolling minimum (default 20)"
    :return: "Lower = rolling min(Low, n)"
    '''
    low = pd.Series(low, dtype=float)
    return low.rolling(window=period).min()


# ---------------------------------------------------------------------------
# 47. donchian_channel_upper
# ---------------------------------------------------------------------------
def donchian_channel_upper(high, period=20):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Volatility & channel indicators']
    function: "Computes the upper Donchian channel as the rolling maximum of the high price over the specified period."
    y_as_x: []
    :param high: "Array or Series of high prices"
    :param period: "Look-back period for the rolling maximum (default 20)"
    :return: "Upper = rolling max(High, n)"
    '''
    high = pd.Series(high, dtype=float)
    return high.rolling(window=period).max()


# ---------------------------------------------------------------------------
# 48. downside_capture
# ---------------------------------------------------------------------------
def downside_capture(portfolio_returns, benchmark_returns):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Capture ratios']
    function: "Computes the downside capture ratio, measuring how much of the benchmark's negative performance the portfolio captures during down markets."
    y_as_x: []
    :param portfolio_returns: "Array or Series of portfolio returns"
    :param benchmark_returns: "Array or Series of benchmark returns"
    :return: "Downside Capture = Avg(R_p | R_b < 0) / Avg(R_b | R_b < 0)"
    '''
    portfolio_returns = np.asarray(portfolio_returns, dtype=float)
    benchmark_returns = np.asarray(benchmark_returns, dtype=float)
    down_mask = benchmark_returns < 0
    if not np.any(down_mask):
        return np.nan
    avg_port_down = np.mean(portfolio_returns[down_mask])
    avg_bench_down = np.mean(benchmark_returns[down_mask])
    return avg_port_down / avg_bench_down


# ---------------------------------------------------------------------------
# 49. downside_deviation
# ---------------------------------------------------------------------------
def downside_deviation(returns, mar=0.0):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Downside risk measures']
    function: "Computes the downside deviation (second lower partial moment), measuring the volatility of returns below a minimum acceptable return."
    y_as_x: ['sortino_ratio', 'upside_potential_ratio']
    :param returns: "Array or Series of periodic returns"
    :param mar: "Minimum acceptable return threshold (default 0)"
    :return: "DD = sqrt(E[min(R - MAR, 0)^2])"
    '''
    returns = np.asarray(returns, dtype=float)
    downside = np.minimum(returns - mar, 0.0)
    return np.sqrt(np.mean(downside ** 2))


# ---------------------------------------------------------------------------
# 50. dpi
# ---------------------------------------------------------------------------
def dpi(distributions, paid_in_capital):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Fund performance multiples']
    function: "Computes the Distributions to Paid-In capital ratio, measuring the realized return multiple of a private equity fund."
    y_as_x: []
    :param distributions: "Total distributions (cash returned) to limited partners"
    :param paid_in_capital: "Total capital contributed (called) by limited partners"
    :return: "DPI = Distributions / Paid-In Capital"
    '''
    return distributions / paid_in_capital


# ---------------------------------------------------------------------------
# 51. drawdown
# ---------------------------------------------------------------------------
def drawdown(values):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Drawdown analysis']
    function: "Computes the drawdown series, representing the percentage decline from the running peak at each point in time."
    y_as_x: ['maximum_drawdown', 'drawdown_duration', 'expected_drawdown', 'burke_ratio', 'calmar_ratio', 'sterling_ratio', 'pain_index', 'ulcer_index']
    :param values: "Array or Series of portfolio values or cumulative wealth"
    :return: "DD_t = V_t / peak_t - 1 (series of drawdowns, negative when below peak)"
    '''
    values = np.asarray(values, dtype=float)
    peak = np.maximum.accumulate(values)
    return values / peak - 1.0


# ---------------------------------------------------------------------------
# 52. drawdown_duration
# ---------------------------------------------------------------------------
def drawdown_duration(values):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Drawdown analysis']
    function: "Computes the duration of drawdown periods, counting consecutive periods where the portfolio value remains below its prior peak."
    y_as_x: []
    :param values: "Array or Series of portfolio values or cumulative wealth"
    :return: "Array of drawdown durations in number of periods"
    '''
    values = np.asarray(values, dtype=float)
    peak = np.maximum.accumulate(values)
    in_drawdown = values < peak
    durations = []
    current_duration = 0
    for below in in_drawdown:
        if below:
            current_duration += 1
        else:
            if current_duration > 0:
                durations.append(current_duration)
            current_duration = 0
    if current_duration > 0:
        durations.append(current_duration)
    return durations


# ---------------------------------------------------------------------------
# 53. duration_gap
# ---------------------------------------------------------------------------
def duration_gap(D_A, D_L, liabilities, assets):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Asset-liability management']
    function: "Computes the duration gap, measuring the mismatch between the durations of assets and liabilities, weighted by the leverage ratio."
    y_as_x: ['economic_value_of_equity_sensitivity', 'eve_sensitivity']
    :param D_A: "Duration of assets"
    :param D_L: "Duration of liabilities"
    :param liabilities: "Total market value of liabilities"
    :param assets: "Total market value of assets"
    :return: "DGAP = D_A - (L/A) * D_L"
    '''
    return D_A - (liabilities / assets) * D_L


# ---------------------------------------------------------------------------
# 54. duration_times_spread_dts
# ---------------------------------------------------------------------------
def duration_times_spread_dts(spread, spread_duration):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Credit spread risk measures']
    function: "Computes duration times spread, a measure of credit spread risk that combines spread level with spread sensitivity."
    y_as_x: []
    :param spread: "Credit spread of the bond in decimal (e.g., 0.02 for 200bps)"
    :param spread_duration: "Spread duration of the bond"
    :return: "DTS = Spread * Spread Duration"
    '''
    return spread * spread_duration


# ---------------------------------------------------------------------------
# 55. duration_neutral_hedge_ratio
# ---------------------------------------------------------------------------
def duration_neutral_hedge_ratio(dv01_asset, dv01_hedge):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Interest rate hedging']
    function: "Computes the duration-neutral hedge ratio, determining the notional amount of the hedging instrument needed to neutralize interest rate risk."
    y_as_x: []
    :param dv01_asset: "DV01 (dollar value of a basis point) of the asset or exposure being hedged"
    :param dv01_hedge: "DV01 of the hedging instrument"
    :return: "h = DV01_asset / DV01_hedge"
    '''
    return dv01_asset / dv01_hedge


# ---------------------------------------------------------------------------
# 56. durbin_watson
# ---------------------------------------------------------------------------
def durbin_watson(residuals):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Regression diagnostics']
    function: "Computes the Durbin-Watson statistic to test for first-order serial autocorrelation in regression residuals."
    y_as_x: []
    :param residuals: "Array of regression residuals"
    :return: "DW = sum_t (e_t - e_{t-1})^2 / sum_t e_t^2"
    '''
    from statsmodels.stats.stattools import durbin_watson as dw
    return float(dw(np.asarray(residuals, dtype=float)))


# ---------------------------------------------------------------------------
# 57. dv01_over_pvbp
# ---------------------------------------------------------------------------
def dv01_over_pvbp(price_down, price_up, delta_yield=0.0001):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Bond risk measures']
    function: "Computes the DV01 (dollar value of a basis point), also known as PVBP, measuring the change in bond price for a one-basis-point change in yield."
    y_as_x: ['duration_neutral_hedge_ratio', 'interest_rate_hedge_ratio']
    :param price_down: "Bond price when yield decreases by delta_yield"
    :param price_up: "Bond price when yield increases by delta_yield"
    :param delta_yield: "Yield shift amount in decimal (default 0.0001 = 1bp)"
    :return: "DV01 = -(P_up - P_down) / (2 * delta_yield / 0.0001) -- approximation: (P_down - P_up) / 2"
    '''
    return (price_down - price_up) / 2.0


# ---------------------------------------------------------------------------
# 58. earnings_at_risk
# ---------------------------------------------------------------------------
def earnings_at_risk(earnings_distribution, alpha=0.05):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Earnings risk management']
    function: "Computes Earnings at Risk, the quantile of the projected earnings shortfall distribution at a given confidence level."
    y_as_x: []
    :param earnings_distribution: "Array of simulated or projected future earnings"
    :param alpha: "Significance level (default 0.05 for 5th percentile)"
    :return: "EaR_alpha = quantile_alpha(future earnings shortfall)"
    '''
    earnings_distribution = np.asarray(earnings_distribution, dtype=float)
    return float(np.percentile(earnings_distribution, alpha * 100))


# ---------------------------------------------------------------------------
# 59. earnings_yield
# ---------------------------------------------------------------------------
def earnings_yield(eps_val, price):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Valuation multiples']
    function: "Computes the earnings yield, the inverse of the P/E ratio, representing earnings as a fraction of price."
    y_as_x: []
    :param eps_val: "Earnings per share"
    :param price: "Current market price per share"
    :return: "E/P = EPS / Price"
    '''
    return eps_val / price


# ---------------------------------------------------------------------------
# 60. ebit
# ---------------------------------------------------------------------------
def ebit(revenue, operating_expenses):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Income statement metrics']
    function: "Computes Earnings Before Interest and Taxes by subtracting operating expenses from revenue."
    y_as_x: ['ebitda', 'ebitda_margin', 'operating_margin', 'interest_coverage', 'interest_coverage_ratio', 'financial_leverage', 'return_on_capital_employed_roce', 'ev_over_ebit', 'free_cash_flow_to_firm_fcff', 'fcff']
    :param revenue: "Total revenue"
    :param operating_expenses: "Total operating expenses"
    :return: "EBIT = Revenue - Operating Expenses"
    '''
    return revenue - operating_expenses


# ---------------------------------------------------------------------------
# 61. ebitda
# ---------------------------------------------------------------------------
def ebitda(ebit_val, depreciation_amortization):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Income statement metrics']
    function: "Computes Earnings Before Interest, Taxes, Depreciation, and Amortization by adding D&A back to EBIT."
    y_as_x: ['ebitda_margin', 'ev_over_ebitda', 'enterprise_value_in_lbo', 'exit_enterprise_value', 'equity_check_multiple_of_ebitda', 'cash_interest_coverage', 'fixed_charge_coverage']
    :param ebit_val: "Earnings Before Interest and Taxes"
    :param depreciation_amortization: "Depreciation and amortization charges"
    :return: "EBITDA = EBIT + D&A"
    '''
    return ebit_val + depreciation_amortization


# ---------------------------------------------------------------------------
# 62. ebitda_margin
# ---------------------------------------------------------------------------
def ebitda_margin(ebitda_val, revenue):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Profitability ratios']
    function: "Computes the EBITDA margin, expressing operating profitability before non-cash charges as a fraction of revenue."
    y_as_x: []
    :param ebitda_val: "Earnings Before Interest, Taxes, Depreciation, and Amortization"
    :param revenue: "Total revenue"
    :return: "EBITDA Margin = EBITDA / Revenue"
    '''
    return ebitda_val / revenue


# ---------------------------------------------------------------------------
# 63. economic_value_added_eva
# ---------------------------------------------------------------------------
def economic_value_added_eva(nopat, wacc, invested_capital):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Value-based management']
    function: "Computes Economic Value Added, measuring the true economic profit by deducting a charge for all capital employed."
    y_as_x: []
    :param nopat: "Net Operating Profit After Taxes"
    :param wacc: "Weighted average cost of capital"
    :param invested_capital: "Total invested capital (equity + debt)"
    :return: "EVA = NOPAT - WACC * Invested Capital"
    '''
    return nopat - wacc * invested_capital


# ---------------------------------------------------------------------------
# 64. economic_value_of_equity_eve
# ---------------------------------------------------------------------------
def economic_value_of_equity_eve(pv_assets, pv_liabilities):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Asset-liability management']
    function: "Computes the Economic Value of Equity, the difference between the present value of all asset and liability cash flows."
    y_as_x: ['eve_sensitivity']
    :param pv_assets: "Present value of all asset cash flows"
    :param pv_liabilities: "Present value of all liability cash flows"
    :return: "EVE = PV(Assets) - PV(Liabilities)"
    '''
    return pv_assets - pv_liabilities


# ---------------------------------------------------------------------------
# 65. economic_value_of_equity_sensitivity
# ---------------------------------------------------------------------------
def economic_value_of_equity_sensitivity(duration_gap_val, assets, delta_y, y):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Asset-liability management']
    function: "Computes the sensitivity of Economic Value of Equity to a change in interest rates, using the duration gap."
    y_as_x: []
    :param duration_gap_val: "Duration gap (DGAP) of the balance sheet"
    :param assets: "Total market value of assets"
    :param delta_y: "Parallel shift in yield curve (in decimal)"
    :param y: "Current yield level (in decimal)"
    :return: "Delta_EVE ~ -DGAP * A * Delta_y / (1 + y)"
    '''
    return -duration_gap_val * assets * delta_y / (1.0 + y)


# ---------------------------------------------------------------------------
# 66. effective_annual_rate_ear
# ---------------------------------------------------------------------------
def effective_annual_rate_ear(nominal_rate, compounding_periods):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Interest rate conversions']
    function: "Converts a nominal interest rate with periodic compounding to an effective annual rate."
    y_as_x: []
    :param nominal_rate: "Nominal (stated) annual interest rate"
    :param compounding_periods: "Number of compounding periods per year (m)"
    :return: "EAR = (1 + r/m)^m - 1"
    '''
    return (1.0 + nominal_rate / compounding_periods) ** compounding_periods - 1.0


# ---------------------------------------------------------------------------
# 67. effective_convexity
# ---------------------------------------------------------------------------
def effective_convexity(price_down, price_up, price_base, delta_y):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Bond risk measures']
    function: "Computes effective convexity using a finite difference approach, capturing the curvature of the price-yield relationship including embedded option effects."
    y_as_x: []
    :param price_down: "Bond price when yield decreases by delta_y (P_-)"
    :param price_up: "Bond price when yield increases by delta_y (P_+)"
    :param price_base: "Bond price at the current yield (P_0)"
    :param delta_y: "Yield shock in decimal"
    :return: "EffConv = (P_- + P_+ - 2*P_0) / (P_0 * (Delta_y)^2)"
    '''
    return (price_down + price_up - 2.0 * price_base) / (price_base * delta_y ** 2)


# ---------------------------------------------------------------------------
# 68. effective_duration
# ---------------------------------------------------------------------------
def effective_duration(price_down, price_up, price_base, delta_y):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Bond risk measures']
    function: "Computes effective duration using a finite difference approach, capturing interest rate sensitivity including the impact of embedded options."
    y_as_x: []
    :param price_down: "Bond price when yield decreases by delta_y (P_-)"
    :param price_up: "Bond price when yield increases by delta_y (P_+)"
    :param price_base: "Bond price at the current yield (P_0)"
    :param delta_y: "Yield shock in decimal"
    :return: "EffDur = (P_- - P_+) / (2 * P_0 * Delta_y)"
    '''
    return (price_down - price_up) / (2.0 * price_base * delta_y)


# ---------------------------------------------------------------------------
# 69. effective_gross_income
# ---------------------------------------------------------------------------
def effective_gross_income(potential_gross_income, vacancy_credit_loss, other_income=0.0):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Property income analysis']
    function: "Computes effective gross income for a property, adjusting potential gross income for vacancy and credit losses and adding other income."
    y_as_x: ['operating_expense_ratio', 'noi_margin']
    :param potential_gross_income: "Total potential rental income assuming full occupancy"
    :param vacancy_credit_loss: "Estimated losses from vacancy and tenant credit defaults"
    :param other_income: "Additional income (parking, laundry, fees, etc., default 0)"
    :return: "EGI = Potential Gross Income - Vacancy/Credit Loss + Other Income"
    '''
    return potential_gross_income - vacancy_credit_loss + other_income


# ---------------------------------------------------------------------------
# 70. effective_spread
# ---------------------------------------------------------------------------
def effective_spread(trade_price, mid_price):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Spread measures']
    function: "Computes the effective spread, a measure of actual transaction costs that captures the deviation of the trade price from the midpoint."
    y_as_x: ['adverse_selection_cost']
    :param trade_price: "Actual execution price of the trade"
    :param mid_price: "Midpoint of the bid-ask spread at the time of the trade"
    :return: "EffSpread = 2 * |Trade Price - Mid|"
    '''
    return 2.0 * abs(trade_price - mid_price)


# ---------------------------------------------------------------------------
# 71. efficient_frontier_problem
# ---------------------------------------------------------------------------
def efficient_frontier_problem(expected_returns, cov_matrix, target_return=None):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio optimization']
    function: "Solves the mean-variance efficient frontier optimization problem: minimize portfolio variance subject to a target return and full-investment constraint."
    y_as_x: []
    :param expected_returns: "Array of expected returns for each asset"
    :param cov_matrix: "Covariance matrix of asset returns"
    :param target_return: "Target portfolio return (if None, finds the minimum variance portfolio)"
    :return: "Optimal portfolio weights solving min w'Sigma w s.t. mu'w >= r* and 1'w = 1"
    '''
    from pypfopt import EfficientFrontier as EF
    from pypfopt import expected_returns as er_module
    mu = pd.Series(expected_returns)
    S = pd.DataFrame(cov_matrix)
    ef = EF(mu, S)
    if target_return is not None:
        ef.efficient_return(target_return)
    else:
        ef.min_volatility()
    return dict(ef.clean_weights())


# ---------------------------------------------------------------------------
# 72. egarch
# ---------------------------------------------------------------------------
def egarch(returns, p=1, q=1):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['GARCH family models']
    function: "Fits an EGARCH model to a return series, capturing asymmetric volatility effects where negative shocks have a larger impact on volatility than positive shocks."
    y_as_x: []
    :param returns: "Array or Series of financial returns"
    :param p: "Order of the GARCH component (default 1)"
    :param q: "Order of the ARCH component (default 1)"
    :return: "Fitted EGARCH model result with estimated parameters omega, alpha, gamma, beta"
    '''
    from arch import arch_model
    returns = np.asarray(returns, dtype=float) * 100  # arch expects percentage returns
    model = arch_model(returns, vol='EGARCH', p=p, q=q, mean='Zero')
    result = model.fit(disp='off')
    return result


# ---------------------------------------------------------------------------
# 73. egarch_11
# ---------------------------------------------------------------------------
def egarch_11(returns):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['GARCH family models']
    function: "Fits an EGARCH(1,1) model to a return series, a specific case of the exponential GARCH model that captures leverage effects in volatility."
    y_as_x: []
    :param returns: "Array or Series of financial returns"
    :return: "Fitted EGARCH(1,1) model result with parameters omega, alpha, gamma, beta"
    '''
    from arch import arch_model
    returns = np.asarray(returns, dtype=float) * 100
    model = arch_model(returns, vol='EGARCH', p=1, q=1, mean='Zero')
    result = model.fit(disp='off')
    return result


# ---------------------------------------------------------------------------
# 74. elastic_net
# ---------------------------------------------------------------------------
def elastic_net(X, y, alpha=1.0, l1_ratio=0.5):
    '''
    domain: ['Quantitative forecasting & machine learning in finance']
    subdomain: ['Regularized regression']
    function: "Fits an Elastic Net regression model that combines L1 (Lasso) and L2 (Ridge) penalties for feature selection and shrinkage."
    y_as_x: []
    :param X: "Feature matrix of shape (n_samples, n_features)"
    :param y: "Target variable array of shape (n_samples,)"
    :param alpha: "Overall regularization strength (lambda in the formula)"
    :param l1_ratio: "Mixing parameter between L1 and L2 penalties (0 = Ridge, 1 = Lasso)"
    :return: "Fitted ElasticNet model with coefficient estimates"
    '''
    from sklearn.linear_model import ElasticNet as EN
    model = EN(alpha=alpha, l1_ratio=l1_ratio)
    model.fit(X, y)
    return model


# ---------------------------------------------------------------------------
# 75. encumbrance_ratio
# ---------------------------------------------------------------------------
def encumbrance_ratio(encumbered_assets, total_assets):
    '''
    domain: ['Bank regulation, Basel & prudential ratios']
    subdomain: ['Asset encumbrance & pledging']
    function: "Computes the encumbrance ratio, indicating the fraction of a bank's total assets that are pledged or encumbered."
    y_as_x: []
    :param encumbered_assets: "Total value of assets that are pledged, collateralized, or otherwise encumbered"
    :param total_assets: "Total assets on the balance sheet"
    :return: "Encumbrance = Encumbered Assets / Total Assets"
    '''
    return encumbered_assets / total_assets


# ---------------------------------------------------------------------------
# 76. endowment_insurance_apv
# ---------------------------------------------------------------------------
def endowment_insurance_apv(x, n, interest_rate, life_table=None):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Life insurance products']
    function: "Computes the actuarial present value of an endowment insurance contract, which pays a benefit upon death within n years or survival to the end of the n-year term."
    y_as_x: []
    :param x: "Current age of the insured"
    :param n: "Duration of the endowment in years"
    :param interest_rate: "Annual effective interest rate for discounting"
    :param life_table: "Mortality/life table data; if array, treated as survival probabilities kpx for k=1..n"
    :return: "Endowment APV = term insurance APV + pure endowment APV"
    '''
    v = 1.0 / (1.0 + interest_rate)
    if life_table is not None and hasattr(life_table, '__getitem__'):
        # term insurance part: sum of v^(k+1) * kpx * q_{x+k}
        probs = np.asarray(life_table[:n], dtype=float)
        term_apv = 0.0
        for k in range(n):
            kpx = probs[k] if k < len(probs) else 0.0
            if k == 0:
                q_xk = 1.0 - probs[0]
            else:
                q_xk = probs[k - 1] - probs[k] if k < len(probs) else 0.0
            term_apv += (v ** (k + 1)) * max(q_xk, 0)
        # pure endowment part
        npx = probs[n - 1] if n - 1 < len(probs) else 0.0
        pure_endowment = (v ** n) * npx
        return term_apv + pure_endowment
    else:
        # Certain case (no mortality): benefit paid at n for sure
        return v ** n


# ---------------------------------------------------------------------------
# 77. enterprise_value
# ---------------------------------------------------------------------------
def enterprise_value(equity_value, net_debt, preferred=0.0, minority_interest=0.0):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Valuation multiples']
    function: "Computes enterprise value, the total value of a firm inclusive of all claims from equity holders, debt holders, preferred stock holders, and minority interests."
    y_as_x: ['ev_over_ebitda', 'ev_over_ebit', 'ev_over_sales', 'equity_value_bridge']
    :param equity_value: "Market capitalization (equity value)"
    :param net_debt: "Total debt minus cash and cash equivalents"
    :param preferred: "Market value of preferred stock (default 0)"
    :param minority_interest: "Market value of minority interest (default 0)"
    :return: "EV = Equity Value + Net Debt + Preferred + Minority Interest"
    '''
    return equity_value + net_debt + preferred + minority_interest


# ---------------------------------------------------------------------------
# 78. enterprise_value_in_lbo
# ---------------------------------------------------------------------------
def enterprise_value_in_lbo(entry_ebitda, entry_multiple):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['LBO transaction modeling']
    function: "Computes the enterprise value at entry in a leveraged buyout transaction."
    y_as_x: []
    :param entry_ebitda: "EBITDA at the time of the LBO entry"
    :param entry_multiple: "EV/EBITDA multiple used for the acquisition"
    :return: "EV = Entry EBITDA * Entry Multiple"
    '''
    return entry_ebitda * entry_multiple


# ---------------------------------------------------------------------------
# 79. eps
# ---------------------------------------------------------------------------
def eps(net_income, weighted_avg_shares):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Earnings metrics']
    function: "Computes basic earnings per share, allocating net income across the weighted average number of common shares outstanding."
    y_as_x: ['p_over_e_ratio', 'price_to_earnings_ratio', 'forward_p_over_e', 'peg_ratio', 'dividend_coverage', 'earnings_yield', 'financial_leverage']
    :param net_income: "Net income available to common shareholders"
    :param weighted_avg_shares: "Weighted average number of common shares outstanding during the period"
    :return: "EPS = Net Income / Weighted Avg Shares"
    '''
    return net_income / weighted_avg_shares


# ---------------------------------------------------------------------------
# 80. equal_risk_contribution
# ---------------------------------------------------------------------------
def equal_risk_contribution(expected_returns, cov_matrix):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Risk-based portfolio construction']
    function: "Solves for portfolio weights such that each asset contributes equally to the total portfolio risk."
    y_as_x: []
    :param expected_returns: "Array of expected returns for each asset"
    :param cov_matrix: "Covariance matrix of asset returns"
    :return: "Weights w such that all risk contributions RC_i are equal"
    '''
    try:
        import riskfolio as rp
        port = rp.Portfolio(returns=pd.DataFrame())
        port.mu = np.asarray(expected_returns, dtype=float).reshape(-1, 1) if np.ndim(expected_returns) == 1 else expected_returns
        port.cov = np.asarray(cov_matrix, dtype=float)
        w = port.rp_optimization(model='Classic', rm='MV', rf=0.0, b=None)
        return w
    except (ImportError, Exception):
        # Manual fallback using scipy
        from scipy.optimize import minimize
        n = len(expected_returns)
        cov = np.asarray(cov_matrix, dtype=float)

        def risk_budget_obj(w):
            port_vol = np.sqrt(w @ cov @ w)
            mrc = cov @ w / port_vol
            rc = w * mrc
            target_rc = port_vol / n
            return np.sum((rc - target_rc) ** 2)

        w0 = np.ones(n) / n
        constraints = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0}]
        bounds = [(0.0, 1.0)] * n
        result = minimize(risk_budget_obj, w0, method='SLSQP', bounds=bounds, constraints=constraints)
        return result.x


# ---------------------------------------------------------------------------
# 81. equal_weight_portfolio
# ---------------------------------------------------------------------------
def equal_weight_portfolio(n):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio construction rules']
    function: "Constructs an equal-weight portfolio by assigning identical weights to all N assets."
    y_as_x: []
    :param n: "Number of assets in the portfolio"
    :return: "Array of weights w_i = 1/N for each asset"
    '''
    return np.ones(n) / n


# ---------------------------------------------------------------------------
# 82. equated_monthly_installment_emi
# ---------------------------------------------------------------------------
def equated_monthly_installment_emi(principal, monthly_rate, n_months):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Loan amortization']
    function: "Computes the equated monthly installment for a fully amortizing loan using the annuity formula."
    y_as_x: []
    :param principal: "Loan principal amount"
    :param monthly_rate: "Monthly interest rate (annual rate / 12)"
    :param n_months: "Total number of monthly payments"
    :return: "EMI = P * r * (1+r)^n / ((1+r)^n - 1)"
    '''
    import numpy_financial as npf
    return -npf.pmt(monthly_rate, n_months, principal)


# ---------------------------------------------------------------------------
# 83. equity_check_multiple_of_ebitda
# ---------------------------------------------------------------------------
def equity_check_multiple_of_ebitda(equity, ebitda_val):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['LBO transaction modeling']
    function: "Computes the equity check as a multiple of EBITDA, measuring how much equity the sponsor is investing relative to the target's earnings."
    y_as_x: []
    :param equity: "Total equity investment by the sponsor"
    :param ebitda_val: "EBITDA of the target company"
    :return: "Equity / EBITDA"
    '''
    return equity / ebitda_val


# ---------------------------------------------------------------------------
# 84. equity_contribution
# ---------------------------------------------------------------------------
def equity_contribution(total_uses, total_debt, existing_cash=0.0):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['LBO sources & uses']
    function: "Computes the sponsor equity contribution required in an LBO or acquisition, as the residual after debt financing and existing cash."
    y_as_x: []
    :param total_uses: "Total uses of funds (purchase price + fees + refinancing)"
    :param total_debt: "Total debt raised to finance the transaction"
    :param existing_cash: "Cash on the target's balance sheet available to fund the transaction (default 0)"
    :return: "Sponsor Equity = Uses - Debt - Existing Cash"
    '''
    return total_uses - total_debt - existing_cash


# ---------------------------------------------------------------------------
# 85. equity_multiple
# ---------------------------------------------------------------------------
def equity_multiple(total_equity_distributions, equity_invested):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Real estate investment returns']
    function: "Computes the equity multiple for a real estate investment, measuring total cash distributions relative to equity invested."
    y_as_x: []
    :param total_equity_distributions: "Total cash distributions received by the equity investor over the holding period"
    :param equity_invested: "Initial equity investment"
    :return: "EM = Total Equity Distributions / Equity Invested"
    '''
    return total_equity_distributions / equity_invested


# ---------------------------------------------------------------------------
# 86. equity_ratio
# ---------------------------------------------------------------------------
def equity_ratio(total_equity, total_assets):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Leverage ratios']
    function: "Computes the equity ratio, indicating the proportion of a company's assets financed by shareholders' equity."
    y_as_x: []
    :param total_equity: "Total shareholders' equity"
    :param total_assets: "Total assets on the balance sheet"
    :return: "Equity Ratio = Total Equity / Total Assets"
    '''
    return total_equity / total_assets


# ---------------------------------------------------------------------------
# 87. equity_rollover_percentage
# ---------------------------------------------------------------------------
def equity_rollover_percentage(management_rollover_equity, total_equity):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['LBO transaction structuring']
    function: "Computes the percentage of total equity contributed through management rollover in an LBO transaction."
    y_as_x: []
    :param management_rollover_equity: "Equity rolled over by incumbent management"
    :param total_equity: "Total equity in the transaction"
    :return: "Rollover = Management Rollover Equity / Total Equity"
    '''
    return management_rollover_equity / total_equity


# ---------------------------------------------------------------------------
# 88. equity_value_at_exit
# ---------------------------------------------------------------------------
def equity_value_at_exit(ev_exit, net_debt_exit):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['LBO exit analysis']
    function: "Computes the equity value at exit in an LBO by deducting remaining net debt from the exit enterprise value."
    y_as_x: ['lbo_equity_irr', 'sponsor_cash_on_cash_return']
    :param ev_exit: "Enterprise value at exit"
    :param net_debt_exit: "Net debt outstanding at exit"
    :return: "Equity_exit = EV_exit - Net Debt_exit"
    '''
    return ev_exit - net_debt_exit


# ---------------------------------------------------------------------------
# 89. equity_value_bridge
# ---------------------------------------------------------------------------
def equity_value_bridge(enterprise_value_val, net_debt, preferred=0.0, minority_interest=0.0, non_operating_assets=0.0):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Valuation bridges']
    function: "Computes equity value from enterprise value by deducting net debt, preferred stock, and minority interest, then adding non-operating assets."
    y_as_x: []
    :param enterprise_value_val: "Enterprise value of the firm"
    :param net_debt: "Net debt (total debt minus cash)"
    :param preferred: "Market value of preferred stock (default 0)"
    :param minority_interest: "Market value of minority interest (default 0)"
    :param non_operating_assets: "Value of non-operating assets such as excess cash, investments (default 0)"
    :return: "Equity Value = EV - Net Debt - Preferred - Minority Interest + Non-operating Assets"
    '''
    return enterprise_value_val - net_debt - preferred - minority_interest + non_operating_assets


# ---------------------------------------------------------------------------
# 90. equivalent_annual_annuity_eaa
# ---------------------------------------------------------------------------
def equivalent_annual_annuity_eaa(npv, rate, n):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Capital budgeting decision rules']
    function: "Converts a project's NPV into an equivalent annual annuity for comparing projects with different lifespans."
    y_as_x: []
    :param npv: "Net present value of the project"
    :param rate: "Discount rate per period"
    :param n: "Number of periods (project life)"
    :return: "EAA = NPV * r / (1 - (1+r)^-n)"
    '''
    return npv * rate / (1.0 - (1.0 + rate) ** (-n))


# ---------------------------------------------------------------------------
# 91. error_correction_model
# ---------------------------------------------------------------------------
def error_correction_model(y, x, max_lags=1):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Cointegration & error correction']
    function: "Estimates a Vector Error Correction Model (VECM), which captures both short-run dynamics and long-run equilibrium relationships between cointegrated time series."
    y_as_x: []
    :param y: "Array or DataFrame of endogenous variables (each column is a variable)"
    :param x: "Not used separately; y should contain all endogenous variables. Provided for compatibility."
    :param max_lags: "Number of lagged difference terms (default 1)"
    :return: "Fitted VECM result with estimated adjustment coefficients and cointegrating relationships"
    '''
    from statsmodels.tsa.vector_ar.vecm import VECM
    data = np.column_stack([y, x]) if x is not None else np.asarray(y)
    model = VECM(data, k_ar_diff=max_lags, coint_rank=1)
    result = model.fit()
    return result


# ---------------------------------------------------------------------------
# 92. ev_over_ebit
# ---------------------------------------------------------------------------
def ev_over_ebit(enterprise_value_val, ebit_val):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Valuation multiples']
    function: "Computes the EV/EBIT valuation multiple, comparing enterprise value to earnings before interest and taxes."
    y_as_x: []
    :param enterprise_value_val: "Enterprise value of the firm"
    :param ebit_val: "Earnings Before Interest and Taxes"
    :return: "EV / EBIT"
    '''
    return enterprise_value_val / ebit_val


# ---------------------------------------------------------------------------
# 93. ev_over_ebitda
# ---------------------------------------------------------------------------
def ev_over_ebitda(enterprise_value_val, ebitda_val):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Valuation multiples']
    function: "Computes the EV/EBITDA valuation multiple, one of the most widely used enterprise value multiples for comparing firms across capital structures."
    y_as_x: []
    :param enterprise_value_val: "Enterprise value of the firm"
    :param ebitda_val: "Earnings Before Interest, Taxes, Depreciation, and Amortization"
    :return: "Enterprise Value / EBITDA"
    '''
    return enterprise_value_val / ebitda_val


# ---------------------------------------------------------------------------
# 94. ev_over_sales
# ---------------------------------------------------------------------------
def ev_over_sales(enterprise_value_val, revenue):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Valuation multiples']
    function: "Computes the EV/Sales valuation multiple, useful for valuing companies with negative or volatile earnings."
    y_as_x: []
    :param enterprise_value_val: "Enterprise value of the firm"
    :param revenue: "Total revenue (sales)"
    :return: "Enterprise Value / Revenue"
    '''
    return enterprise_value_val / revenue


# ---------------------------------------------------------------------------
# 95. eve_sensitivity
# ---------------------------------------------------------------------------
def eve_sensitivity(duration_gap_val, delta_y):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Asset-liability management']
    function: "Computes the relative sensitivity of Economic Value of Equity to interest rate changes using the duration gap."
    y_as_x: []
    :param duration_gap_val: "Duration gap (DGAP) of the balance sheet"
    :param delta_y: "Parallel shift in the yield curve (in decimal)"
    :return: "Delta EVE / EVE ~ -DGAP * Delta_y"
    '''
    return -duration_gap_val * delta_y


# ---------------------------------------------------------------------------
# 96. ewma_volatility
# ---------------------------------------------------------------------------
def ewma_volatility(returns, lam=0.94):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Volatility estimation']
    function: "Computes exponentially weighted moving average (EWMA) volatility, applying a decay factor to weight recent observations more heavily."
    y_as_x: []
    :param returns: "Array or Series of financial returns"
    :param lam: "Decay factor (lambda), typically 0.94 for daily data (RiskMetrics)"
    :return: "Series of EWMA volatility estimates: sigma_t^2 = lambda * sigma_{t-1}^2 + (1-lambda) * r_{t-1}^2"
    '''
    returns = np.asarray(returns, dtype=float)
    n = len(returns)
    variance = np.zeros(n)
    variance[0] = returns[0] ** 2
    for t in range(1, n):
        variance[t] = lam * variance[t - 1] + (1 - lam) * returns[t - 1] ** 2
    return np.sqrt(variance)


# ---------------------------------------------------------------------------
# 97. ex_ante_tracking_error
# ---------------------------------------------------------------------------
def ex_ante_tracking_error(weights, benchmark_weights, cov_matrix):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio risk measurement']
    function: "Computes ex-ante (predicted) tracking error, the expected standard deviation of the portfolio's active return relative to the benchmark."
    y_as_x: []
    :param weights: "Array of portfolio weights"
    :param benchmark_weights: "Array of benchmark weights"
    :param cov_matrix: "Covariance matrix of asset returns"
    :return: "TE = sqrt((w - w_b)' * Sigma * (w - w_b))"
    '''
    w = np.asarray(weights, dtype=float)
    wb = np.asarray(benchmark_weights, dtype=float)
    cov = np.asarray(cov_matrix, dtype=float)
    active = w - wb
    return np.sqrt(active @ cov @ active)


# ---------------------------------------------------------------------------
# 98. excess_kurtosis
# ---------------------------------------------------------------------------
def excess_kurtosis(returns):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Distribution statistics']
    function: "Computes the excess kurtosis of a return distribution, measuring the heaviness of tails relative to a normal distribution."
    y_as_x: ['cornish_fisher_var']
    :param returns: "Array or Series of financial returns"
    :return: "Kurt = E[(R - mu)^4] / sigma^4 - 3"
    '''
    return float(stats.kurtosis(np.asarray(returns, dtype=float), fisher=True))


# ---------------------------------------------------------------------------
# 99. excess_return
# ---------------------------------------------------------------------------
def excess_return(portfolio_return, benchmark_return):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Return decomposition']
    function: "Computes excess return, the difference between the portfolio return and the benchmark or risk-free return."
    y_as_x: ['sharpe_ratio', 'information_ratio', 'burke_ratio', 'treynor_ratio']
    :param portfolio_return: "Portfolio return (or array of portfolio returns)"
    :param benchmark_return: "Benchmark or risk-free return (or array)"
    :return: "ER = R_p - R_b"
    '''
    return np.asarray(portfolio_return, dtype=float) - np.asarray(benchmark_return, dtype=float)


# ---------------------------------------------------------------------------
# 100. excess_spread
# ---------------------------------------------------------------------------
def excess_spread(asset_yield, funding_cost, servicing_fee, charge_offs):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Pool cash flow waterfall']
    function: "Computes excess spread in a securitization, representing the residual income after paying funding costs, servicing fees, and absorbing credit losses."
    y_as_x: ['tranche_credit_enhancement']
    :param asset_yield: "Weighted average yield on the securitized asset pool"
    :param funding_cost: "Weighted average cost of funding (note coupon rates)"
    :param servicing_fee: "Servicing fee rate"
    :param charge_offs: "Net charge-off rate on the pool"
    :return: "Excess Spread = Asset Yield - Funding Cost - Servicing Fee - Charge-offs"
    '''
    return asset_yield - funding_cost - servicing_fee - charge_offs


# ---------------------------------------------------------------------------
# 101. exit_enterprise_value
# ---------------------------------------------------------------------------
def exit_enterprise_value(exit_ebitda, exit_multiple):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['LBO exit analysis']
    function: "Computes the enterprise value at exit in an LBO by multiplying exit EBITDA by the assumed exit EV/EBITDA multiple."
    y_as_x: ['equity_value_at_exit']
    :param exit_ebitda: "Projected EBITDA at the time of exit"
    :param exit_multiple: "Assumed EV/EBITDA exit multiple"
    :return: "Exit EV = Exit EBITDA * Exit Multiple"
    '''
    return exit_ebitda * exit_multiple


# ---------------------------------------------------------------------------
# 102. expected_credit_loss_ifrs_9_over_cecl
# ---------------------------------------------------------------------------
def expected_credit_loss_ifrs_9_over_cecl(pd_array, lgd_array, ead_array, df_array):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Expected credit loss provisioning']
    function: "Computes expected credit loss under IFRS 9 or CECL frameworks, summing across all time periods the product of probability of default, loss given default, exposure at default, and the discount factor."
    y_as_x: []
    :param pd_array: "Array of marginal probabilities of default for each period PD_t"
    :param lgd_array: "Array of loss given default estimates for each period LGD_t"
    :param ead_array: "Array of exposure at default estimates for each period EAD_t"
    :param df_array: "Array of discount factors for each period DF_t"
    :return: "ECL = sum_t PD_t * LGD_t * EAD_t * DF_t"
    '''
    pd_arr = np.asarray(pd_array, dtype=float)
    lgd_arr = np.asarray(lgd_array, dtype=float)
    ead_arr = np.asarray(ead_array, dtype=float)
    df_arr = np.asarray(df_array, dtype=float)
    return float(np.sum(pd_arr * lgd_arr * ead_arr * df_arr))
