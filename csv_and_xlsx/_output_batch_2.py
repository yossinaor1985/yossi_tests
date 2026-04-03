"""
Financial Functions - Batch 2 (Equations 102-203)
"""
import numpy as np
import pandas as pd
from scipy import stats


# ---------------------------------------------------------------------------
# 1. break_even_inflation
# ---------------------------------------------------------------------------
def break_even_inflation(nominal_yield, real_yield):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Inflation-linked bonds', 'Yield analysis']
    function: "Computes break-even inflation (BEI), the inflation rate at which an investor is indifferent between nominal and inflation-linked bonds."
    y_as_x: []
    :param nominal_yield: "Yield on a nominal (non-inflation-linked) bond of the same maturity"
    :param real_yield: "Yield on an inflation-linked (real) bond such as TIPS"
    :return: "Break-even inflation rate: BEI = Nominal Yield - Real Yield"
    '''
    return nominal_yield - real_yield


# ---------------------------------------------------------------------------
# 2. break_even_occupancy
# ---------------------------------------------------------------------------
def break_even_occupancy(operating_expenses, debt_service, gross_potential_income):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Property analysis', 'Occupancy metrics']
    function: "Computes the minimum occupancy rate at which property revenue covers operating expenses and debt service."
    y_as_x: []
    :param operating_expenses: "Total operating expenses for the property"
    :param debt_service: "Total debt service payments (principal + interest)"
    :param gross_potential_income: "Maximum rental income if the property were 100% occupied"
    :return: "Break-even occupancy ratio: BEO = (Operating Expenses + Debt Service) / Gross Potential Income"
    '''
    return (operating_expenses + debt_service) / gross_potential_income


# ---------------------------------------------------------------------------
# 3. break_even_quantity
# ---------------------------------------------------------------------------
def break_even_quantity(fixed_costs, price, variable_cost_per_unit):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Break-even analysis', 'Cost-volume-profit']
    function: "Computes the number of units that must be sold to cover all fixed and variable costs."
    y_as_x: []
    :param fixed_costs: "Total fixed costs that do not vary with production volume"
    :param price: "Selling price per unit"
    :param variable_cost_per_unit: "Variable cost incurred per unit produced"
    :return: "Break-even quantity: Q_BE = Fixed Costs / (Price - Variable Cost per unit)"
    '''
    return fixed_costs / (price - variable_cost_per_unit)


# ---------------------------------------------------------------------------
# 4. break_even_revenue
# ---------------------------------------------------------------------------
def break_even_revenue(fixed_costs, contribution_margin_ratio):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Break-even analysis', 'Cost-volume-profit']
    function: "Computes the revenue level at which total contribution margin equals fixed costs, yielding zero profit."
    y_as_x: []
    :param fixed_costs: "Total fixed costs that do not vary with sales volume"
    :param contribution_margin_ratio: "Contribution margin as a fraction of revenue (CM / Revenue)"
    :return: "Break-even revenue: Sales_BE = Fixed Costs / Contribution Margin Ratio"
    '''
    return fixed_costs / contribution_margin_ratio


# ---------------------------------------------------------------------------
# 5. breusch_pagan_test
# ---------------------------------------------------------------------------
def breusch_pagan_test(y, X):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Regression diagnostics', 'Heteroskedasticity testing']
    function: "Performs the Breusch-Pagan Lagrange Multiplier test for heteroskedasticity in a linear regression."
    y_as_x: []
    :param y: "Dependent variable array (n,)"
    :param X: "Independent variable matrix (n x k), should include a constant column if desired"
    :return: "Tuple of (LM statistic, p-value, F-statistic, F p-value) from the auxiliary regression of squared residuals on X"
    '''
    import statsmodels.api as sm
    from statsmodels.stats.diagnostic import het_breuschpagan
    model = sm.OLS(y, X).fit()
    bp_test = het_breuschpagan(model.resid, model.model.exog)
    return bp_test  # (lm_stat, lm_pvalue, fvalue, f_pvalue)


# ---------------------------------------------------------------------------
# 6. brinson_allocation_effect
# ---------------------------------------------------------------------------
def brinson_allocation_effect(w_portfolio, w_benchmark, r_benchmark_sector, r_benchmark_total):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Brinson attribution', 'Portfolio performance']
    function: "Computes the allocation effect for a single sector in Brinson performance attribution, measuring the value added by over/under-weighting a sector."
    y_as_x: []
    :param w_portfolio: "Portfolio weight for sector i"
    :param w_benchmark: "Benchmark weight for sector i"
    :param r_benchmark_sector: "Benchmark return for sector i"
    :param r_benchmark_total: "Total benchmark return across all sectors"
    :return: "Allocation effect: (w_p,i - w_b,i) * (R_b,i - R_b)"
    '''
    return (w_portfolio - w_benchmark) * (r_benchmark_sector - r_benchmark_total)


# ---------------------------------------------------------------------------
# 7. brinson_selection_effect
# ---------------------------------------------------------------------------
def brinson_selection_effect(w_benchmark, r_portfolio_sector, r_benchmark_sector):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Brinson attribution', 'Portfolio performance']
    function: "Computes the selection (stock-picking) effect for a single sector in Brinson performance attribution."
    y_as_x: []
    :param w_benchmark: "Benchmark weight for sector i"
    :param r_portfolio_sector: "Portfolio return for sector i"
    :param r_benchmark_sector: "Benchmark return for sector i"
    :return: "Selection effect: w_b,i * (R_p,i - R_b,i)"
    '''
    return w_benchmark * (r_portfolio_sector - r_benchmark_sector)


# ---------------------------------------------------------------------------
# 8. buhlmann_credibility_factor
# ---------------------------------------------------------------------------
def buhlmann_credibility_factor(n, k):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Credibility theory', 'Premium ratemaking']
    function: "Computes the Buhlmann credibility factor Z, which determines how much weight to assign to an individual's own claims experience versus the collective prior."
    y_as_x: ['credibility_premium']
    :param n: "Number of observations (exposure units or years of experience)"
    :param k: "Buhlmann K parameter, ratio of expected process variance to variance of hypothetical means"
    :return: "Credibility factor: Z = n / (n + K), ranges from 0 to 1"
    '''
    return n / (n + k)


# ---------------------------------------------------------------------------
# 9. burke_ratio
# ---------------------------------------------------------------------------
def burke_ratio(returns, risk_free_rate=0.0):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Risk-adjusted return', 'Drawdown-based measures']
    function: "Computes the Burke ratio, which measures risk-adjusted return using the square root of the sum of squared drawdowns."
    y_as_x: []
    :param returns: "Pandas Series of periodic returns"
    :param risk_free_rate: "Risk-free rate for the same period as returns (default 0)"
    :return: "Burke ratio: Excess Return / sqrt(sum of squared drawdowns)"
    '''
    cumulative = (1 + returns).cumprod()
    running_max = cumulative.cummax()
    drawdowns = (cumulative - running_max) / running_max
    drawdown_sq_sum = (drawdowns ** 2).sum()
    excess_return = returns.mean() * len(returns) - risk_free_rate
    if drawdown_sq_sum == 0:
        return np.inf
    return excess_return / np.sqrt(drawdown_sq_sum)


# ---------------------------------------------------------------------------
# 10. butterfly_payoff
# ---------------------------------------------------------------------------
def butterfly_payoff(S, K1, K2, K3):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Option strategies', 'Payoff diagrams']
    function: "Computes the payoff of a long butterfly spread at expiration using three strike prices (K1 < K2 < K3)."
    y_as_x: []
    :param S: "Underlying asset price at expiration (scalar or array)"
    :param K1: "Lower strike price"
    :param K2: "Middle strike price"
    :param K3: "Upper strike price"
    :return: "Butterfly payoff: max(S-K1,0) - 2*max(S-K2,0) + max(S-K3,0)"
    '''
    S = np.asarray(S, dtype=float)
    return np.maximum(S - K1, 0) - 2 * np.maximum(S - K2, 0) + np.maximum(S - K3, 0)


# ---------------------------------------------------------------------------
# 11. calendar_spread
# ---------------------------------------------------------------------------
def calendar_spread(F_near, F_far):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Futures spreads', 'Term structure trading']
    function: "Computes the calendar (time) spread between near-term and far-term futures contracts."
    y_as_x: []
    :param F_near: "Price of the near-term (front-month) futures contract"
    :param F_far: "Price of the far-term (back-month) futures contract"
    :return: "Calendar spread: F_near - F_far"
    '''
    return F_near - F_far


# ---------------------------------------------------------------------------
# 12. call_payoff
# ---------------------------------------------------------------------------
def call_payoff(S_T, K):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Option payoffs', 'Vanilla options']
    function: "Computes the payoff of a European call option at expiration."
    y_as_x: ['covered_call_payoff']
    :param S_T: "Underlying asset price at expiration (scalar or array)"
    :param K: "Strike price of the call option"
    :return: "Call payoff: max(S_T - K, 0)"
    '''
    return np.maximum(np.asarray(S_T, dtype=float) - K, 0)


# ---------------------------------------------------------------------------
# 13. call_spread_payoff
# ---------------------------------------------------------------------------
def call_spread_payoff(S, K1, K2):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Option strategies', 'Vertical spreads']
    function: "Computes the payoff of a bull call spread (long call at K1, short call at K2 where K2 > K1) at expiration."
    y_as_x: []
    :param S: "Underlying asset price at expiration (scalar or array)"
    :param K1: "Lower strike price (long call)"
    :param K2: "Upper strike price (short call)"
    :return: "Call spread payoff: max(S-K1,0) - max(S-K2,0)"
    '''
    S = np.asarray(S, dtype=float)
    return np.maximum(S - K1, 0) - np.maximum(S - K2, 0)


# ---------------------------------------------------------------------------
# 14. calmar_ratio
# ---------------------------------------------------------------------------
def calmar_ratio(returns, period='daily'):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Risk-adjusted return', 'Drawdown-based measures']
    function: "Computes the Calmar ratio: annualized compound return (CAGR) divided by the maximum drawdown."
    y_as_x: []
    :param returns: "Pandas Series of periodic returns"
    :param period: "Frequency of returns: 'daily', 'monthly', or 'yearly' (default 'daily')"
    :return: "Calmar ratio: CAGR / |Max Drawdown|"
    '''
    import empyrical
    return empyrical.calmar_ratio(returns, period=period)


# ---------------------------------------------------------------------------
# 15. cancel_to_trade_ratio
# ---------------------------------------------------------------------------
def cancel_to_trade_ratio(num_cancellations, num_trades):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Order flow metrics', 'Market microstructure']
    function: "Computes the cancel-to-trade ratio, a measure of order cancellation activity relative to executed trades."
    y_as_x: []
    :param num_cancellations: "Number of order cancellations in the period"
    :param num_trades: "Number of executed trades in the period"
    :return: "Cancel-to-trade ratio: Number of cancellations / Number of trades"
    '''
    return num_cancellations / num_trades


# ---------------------------------------------------------------------------
# 16. capital_conservation_buffer
# ---------------------------------------------------------------------------
def capital_conservation_buffer(cet1_ratio, min_cet1_requirement):
    '''
    domain: ['Bank regulation, Basel & prudential ratios']
    subdomain: ['Capital adequacy', 'Basel III buffers']
    function: "Computes the capital conservation buffer (CCB), the excess CET1 ratio above the minimum regulatory requirement."
    y_as_x: []
    :param cet1_ratio: "Bank's Common Equity Tier 1 ratio"
    :param min_cet1_requirement: "Minimum CET1 requirement (e.g., 4.5% under Basel III)"
    :return: "Capital conservation buffer: CET1 Ratio - Minimum CET1 requirement"
    '''
    return cet1_ratio - min_cet1_requirement


# ---------------------------------------------------------------------------
# 17. capitalization_rate
# ---------------------------------------------------------------------------
def capitalization_rate(net_operating_income, property_value):
    '''
    domain: ['Real estate finance']
    subdomain: ['Property valuation', 'Income approach']
    function: "Computes the capitalization rate (cap rate), used to value income-producing real estate."
    y_as_x: ['property_value_from_cap_rate']
    :param net_operating_income: "Net operating income (NOI) generated by the property"
    :param property_value: "Current market value or purchase price of the property"
    :return: "Cap rate: NOI / Property Value"
    '''
    return net_operating_income / property_value


# ---------------------------------------------------------------------------
# 18. capm_expected_return
# ---------------------------------------------------------------------------
def capm_expected_return(risk_free_rate, beta, market_return):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Capital asset pricing', 'Expected return models']
    function: "Computes the expected return of an asset using the Capital Asset Pricing Model (CAPM)."
    y_as_x: ['security_market_line']
    :param risk_free_rate: "Risk-free rate of return (e.g., Treasury yield)"
    :param beta: "Systematic risk (beta) of the asset relative to the market portfolio"
    :param market_return: "Expected return on the market portfolio"
    :return: "CAPM expected return: E[R_i] = R_f + beta_i * (E[R_m] - R_f)"
    '''
    return risk_free_rate + beta * (market_return - risk_free_rate)


# ---------------------------------------------------------------------------
# 19. carhart_4_factor_model
# ---------------------------------------------------------------------------
def carhart_4_factor_model(returns, factor_returns):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Factor models', 'Asset pricing']
    function: "Estimates the Carhart 4-factor model: R_i - R_f = alpha + b*MKT + s*SMB + h*HML + m*MOM + epsilon using OLS regression."
    y_as_x: []
    :param returns: "Pandas DataFrame with columns: 'excess_return', 'MKT', 'SMB', 'HML', 'MOM'"
    :param factor_returns: "Not used if returns DataFrame already has all columns; alternatively a DataFrame with factor columns"
    :return: "Dictionary with 'alpha', 'betas' (dict of factor loadings), 'r_squared', 'residuals'"
    '''
    import statsmodels.api as sm
    if isinstance(returns, pd.DataFrame) and all(c in returns.columns for c in ['excess_return', 'MKT', 'SMB', 'HML', 'MOM']):
        y = returns['excess_return']
        X = returns[['MKT', 'SMB', 'HML', 'MOM']]
    else:
        y = returns
        X = factor_returns[['MKT', 'SMB', 'HML', 'MOM']]
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()
    return {
        'alpha': model.params.get('const', model.params.iloc[0]),
        'betas': {name: model.params[name] for name in ['MKT', 'SMB', 'HML', 'MOM']},
        'r_squared': model.rsquared,
        'residuals': model.resid
    }


# ---------------------------------------------------------------------------
# 20. cash_conversion_cycle_ccc
# ---------------------------------------------------------------------------
def cash_conversion_cycle_ccc(days_sales_outstanding, days_inventory_outstanding, days_payables_outstanding):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Working capital management', 'Liquidity analysis']
    function: "Computes the cash conversion cycle (CCC), measuring the number of days it takes to convert resource inputs into cash flows."
    y_as_x: []
    :param days_sales_outstanding: "Average number of days to collect receivables (DSO)"
    :param days_inventory_outstanding: "Average number of days inventory is held before sale (DIO)"
    :param days_payables_outstanding: "Average number of days to pay suppliers (DPO)"
    :return: "CCC = DSO + DIO - DPO"
    '''
    return days_sales_outstanding + days_inventory_outstanding - days_payables_outstanding


# ---------------------------------------------------------------------------
# 21. cash_flow_at_risk_cfar
# ---------------------------------------------------------------------------
def cash_flow_at_risk_cfar(cash_flows, alpha=0.05):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Cash flow risk', 'Enterprise risk management']
    function: "Computes Cash Flow at Risk (CFaR), the quantile-based worst-case shortfall in future cash flows at a given confidence level."
    y_as_x: []
    :param cash_flows: "Array or Series of simulated or historical future cash flows"
    :param alpha: "Significance level (e.g., 0.05 for 95% confidence)"
    :return: "CFaR at the given alpha level (the alpha-quantile of the cash flow distribution)"
    '''
    cash_flows = np.asarray(cash_flows, dtype=float)
    return np.quantile(cash_flows, alpha)


# ---------------------------------------------------------------------------
# 22. cash_flow_margin
# ---------------------------------------------------------------------------
def cash_flow_margin(operating_cash_flow, revenue):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Profitability ratios', 'Cash flow analysis']
    function: "Computes cash flow margin, measuring how efficiently a company converts revenue into operating cash flow."
    y_as_x: []
    :param operating_cash_flow: "Cash generated from operating activities"
    :param revenue: "Total revenue or net sales"
    :return: "Cash flow margin: Operating Cash Flow / Revenue"
    '''
    return operating_cash_flow / revenue


# ---------------------------------------------------------------------------
# 23. cash_interest_coverage
# ---------------------------------------------------------------------------
def cash_interest_coverage(ebitda, capex, cash_interest):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Credit analysis', 'Debt capacity']
    function: "Computes cash interest coverage, measuring the ability to pay interest from cash earnings after capital expenditures."
    y_as_x: []
    :param ebitda: "Earnings before interest, taxes, depreciation, and amortization"
    :param capex: "Capital expenditures"
    :param cash_interest: "Total cash interest expense"
    :return: "Cash interest coverage: (EBITDA - Capex) / Cash Interest"
    '''
    return (ebitda - capex) / cash_interest


# ---------------------------------------------------------------------------
# 24. cash_ratio
# ---------------------------------------------------------------------------
def cash_ratio(cash, marketable_securities, current_liabilities):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Liquidity ratios', 'Short-term solvency']
    function: "Computes the cash ratio, the most conservative liquidity ratio measuring ability to cover current liabilities with the most liquid assets."
    y_as_x: []
    :param cash: "Cash and cash equivalents"
    :param marketable_securities: "Short-term marketable securities"
    :param current_liabilities: "Total current liabilities"
    :return: "Cash ratio: (Cash + Marketable Securities) / Current Liabilities"
    '''
    return (cash + marketable_securities) / current_liabilities


# ---------------------------------------------------------------------------
# 25. cash_sweep
# ---------------------------------------------------------------------------
def cash_sweep(free_cash_flow, required_cash):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['LBO mechanics', 'Debt repayment']
    function: "Computes the cash sweep amount available for mandatory debt repayment from excess free cash flow."
    y_as_x: []
    :param free_cash_flow: "Free cash flow available in the period"
    :param required_cash: "Minimum cash required to be retained for operations"
    :return: "Cash sweep (debt paydown): max(FCF - Required Cash, 0)"
    '''
    return max(free_cash_flow - required_cash, 0)


# ---------------------------------------------------------------------------
# 26. cash_on_cash_return
# ---------------------------------------------------------------------------
def cash_on_cash_return(before_tax_cash_flow, equity_invested):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Investment return', 'Real estate returns']
    function: "Computes cash-on-cash return, a simple measure of income return on equity invested in real estate."
    y_as_x: []
    :param before_tax_cash_flow: "Before-tax annual cash flow from the property"
    :param equity_invested: "Total equity (cash) invested in the property"
    :return: "Cash-on-cash return: Before-tax Cash Flow / Equity Invested"
    '''
    return before_tax_cash_flow / equity_invested


# ---------------------------------------------------------------------------
# 27. cash_out_refinance_ltv
# ---------------------------------------------------------------------------
def cash_out_refinance_ltv(appraised_value, max_ltv):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Mortgage refinancing', 'Lending criteria']
    function: "Computes the maximum refinance proceeds for a cash-out refinance based on appraised value and maximum LTV ratio."
    y_as_x: []
    :param appraised_value: "Current appraised value of the property"
    :param max_ltv: "Maximum loan-to-value ratio allowed by the lender (e.g., 0.80)"
    :return: "Maximum refinance proceeds: Appraised Value x Max LTV"
    '''
    return appraised_value * max_ltv


# ---------------------------------------------------------------------------
# 28. catch_up_distribution
# ---------------------------------------------------------------------------
def catch_up_distribution(total_profit, preferred_return_amount, gp_carry_pct, catch_up_rate=1.0):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Waterfall distribution', 'GP economics']
    function: "Computes the GP catch-up distribution in a private equity waterfall, after the preferred return hurdle is met."
    y_as_x: []
    :param total_profit: "Total profit available for distribution"
    :param preferred_return_amount: "Cumulative preferred return already distributed to LPs"
    :param gp_carry_pct: "GP carried interest percentage (e.g., 0.20 for 20%)"
    :param catch_up_rate: "Fraction of incremental profits allocated to GP during catch-up (default 1.0 = 100%)"
    :return: "GP catch-up amount needed to reach target carry split"
    '''
    remaining_profit = total_profit - preferred_return_amount
    if remaining_profit <= 0:
        return 0.0
    # Target: GP should have gp_carry_pct of total profit
    target_gp_total = total_profit * gp_carry_pct
    # GP has received 0 so far (catch-up starts after pref return to LP)
    catch_up_needed = target_gp_total / catch_up_rate
    return min(catch_up_needed, remaining_profit)


# ---------------------------------------------------------------------------
# 29. cdo_tranche_loss
# ---------------------------------------------------------------------------
def cdo_tranche_loss(pool_loss, attachment_point, detachment_point):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['CDO tranching', 'Credit structuring']
    function: "Computes the loss absorbed by a CDO tranche given the total pool loss and the tranche attachment/detachment points."
    y_as_x: []
    :param pool_loss: "Total portfolio/pool loss amount (scalar or array)"
    :param attachment_point: "Tranche attachment point (lower bound, e.g. 0.03 for 3%)"
    :param detachment_point: "Tranche detachment point (upper bound, e.g. 0.07 for 7%)"
    :return: "Tranche loss: min(max(PoolLoss - Attach, 0), Detach - Attach)"
    '''
    pool_loss = np.asarray(pool_loss, dtype=float)
    return np.minimum(np.maximum(pool_loss - attachment_point, 0), detachment_point - attachment_point)


# ---------------------------------------------------------------------------
# 30. cds_par_spread
# ---------------------------------------------------------------------------
def cds_par_spread(recovery_rate, hazard_rate, maturity_years, risk_free_rate):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Credit derivatives', 'CDS pricing']
    function: "Computes the CDS par spread as the ratio of the protection leg PV to the risky annuity (PV01)."
    y_as_x: []
    :param recovery_rate: "Expected recovery rate on the reference entity (e.g., 0.40)"
    :param hazard_rate: "Constant hazard (default intensity) rate per year"
    :param maturity_years: "CDS contract maturity in years"
    :param risk_free_rate: "Continuous risk-free rate"
    :return: "Par spread S* = PV_protection / PV01"
    '''
    dt = 0.25  # quarterly payments
    times = np.arange(dt, maturity_years + dt, dt)
    survival = np.exp(-hazard_rate * times)
    df = np.exp(-risk_free_rate * times)
    # Protection leg: LGD * integral of DF * dQ
    survival_prev = np.exp(-hazard_rate * (times - dt))
    default_prob = survival_prev - survival
    pv_protection = (1 - recovery_rate) * np.sum(df * default_prob)
    # Premium leg: PV01 = sum of dt * DF * Survival
    pv01 = np.sum(dt * df * survival)
    if pv01 == 0:
        return 0.0
    return pv_protection / pv01


# ---------------------------------------------------------------------------
# 31. cds_premium_leg
# ---------------------------------------------------------------------------
def cds_premium_leg(spread, discount_factors, survival_probs, accrual_fractions):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Credit derivatives', 'CDS pricing']
    function: "Computes the present value of the CDS premium (fee) leg."
    y_as_x: ['cds_par_spread']
    :param spread: "CDS spread (annual, e.g., 0.01 for 100 bps)"
    :param discount_factors: "Array of discount factors for each payment date"
    :param survival_probs: "Array of survival probabilities for each payment date"
    :param accrual_fractions: "Array of accrual period fractions (year fractions between payment dates)"
    :return: "PV_prem = S * sum(alpha_i * DF_i * Survival(t_i))"
    '''
    discount_factors = np.asarray(discount_factors, dtype=float)
    survival_probs = np.asarray(survival_probs, dtype=float)
    accrual_fractions = np.asarray(accrual_fractions, dtype=float)
    return spread * np.sum(accrual_fractions * discount_factors * survival_probs)


# ---------------------------------------------------------------------------
# 32. cds_protection_leg
# ---------------------------------------------------------------------------
def cds_protection_leg(lgd, discount_factors, default_probs):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Credit derivatives', 'CDS pricing']
    function: "Computes the present value of the CDS protection (contingent) leg."
    y_as_x: ['cds_par_spread']
    :param lgd: "Loss given default (1 - Recovery Rate)"
    :param discount_factors: "Array of discount factors for each period"
    :param default_probs: "Array of marginal default probabilities for each period (dQ)"
    :return: "PV_prot = LGD * sum(DF(t_i) * dQ(t_i))"
    '''
    discount_factors = np.asarray(discount_factors, dtype=float)
    default_probs = np.asarray(default_probs, dtype=float)
    return lgd * np.sum(discount_factors * default_probs)


# ---------------------------------------------------------------------------
# 33. cds_spread_approximation
# ---------------------------------------------------------------------------
def cds_spread_approximation(hazard_rate, recovery_rate):
    '''
    domain: ['Credit risk']
    subdomain: ['Credit derivatives', 'Default modeling']
    function: "Approximates the CDS spread using the reduced-form relationship: s ~ lambda * (1 - R)."
    y_as_x: []
    :param hazard_rate: "Constant hazard rate (default intensity) lambda"
    :param recovery_rate: "Expected recovery rate R (e.g., 0.40)"
    :return: "Approximate CDS spread: s = lambda * (1 - R)"
    '''
    return hazard_rate * (1 - recovery_rate)


# ---------------------------------------------------------------------------
# 34. cet1_ratio
# ---------------------------------------------------------------------------
def cet1_ratio(cet1_capital, risk_weighted_assets):
    '''
    domain: ['Banking, lending & project finance']
    subdomain: ['Capital adequacy', 'Regulatory ratios']
    function: "Computes the Common Equity Tier 1 (CET1) ratio, a key Basel III capital adequacy measure."
    y_as_x: ['capital_conservation_buffer', 'countercyclical_capital_buffer']
    :param cet1_capital: "Common Equity Tier 1 capital"
    :param risk_weighted_assets: "Total risk-weighted assets"
    :return: "CET1 Ratio = CET1 Capital / Risk-Weighted Assets"
    '''
    return cet1_capital / risk_weighted_assets


# ---------------------------------------------------------------------------
# 35. chaikin_money_flow_cmf
# ---------------------------------------------------------------------------
def chaikin_money_flow_cmf(high, low, close, volume, period=20):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Volume indicators', 'Money flow']
    function: "Computes the Chaikin Money Flow (CMF), measuring buying/selling pressure over a lookback period."
    y_as_x: []
    :param high: "Numpy array of high prices"
    :param low: "Numpy array of low prices"
    :param close: "Numpy array of closing prices"
    :param volume: "Numpy array of trading volumes"
    :param period: "Lookback period (default 20)"
    :return: "CMF = sum(MFM * Volume) / sum(Volume) over n periods"
    '''
    import talib
    # talib doesn't have CMF directly, compute manually
    high = np.asarray(high, dtype=float)
    low = np.asarray(low, dtype=float)
    close = np.asarray(close, dtype=float)
    volume = np.asarray(volume, dtype=float)
    hl_range = high - low
    hl_range[hl_range == 0] = 1e-10
    mfm = ((close - low) - (high - close)) / hl_range
    mf_volume = mfm * volume
    cmf = pd.Series(mf_volume).rolling(period).sum() / pd.Series(volume).rolling(period).sum()
    return cmf.values


# ---------------------------------------------------------------------------
# 36. chaikin_oscillator
# ---------------------------------------------------------------------------
def chaikin_oscillator(high, low, close, volume, fastperiod=3, slowperiod=10):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Volume indicators', 'Oscillators']
    function: "Computes the Chaikin Oscillator (CHO), the difference between fast and slow EMAs of the Accumulation/Distribution Line."
    y_as_x: []
    :param high: "Numpy array of high prices"
    :param low: "Numpy array of low prices"
    :param close: "Numpy array of closing prices"
    :param volume: "Numpy array of trading volumes"
    :param fastperiod: "Fast EMA period (default 3)"
    :param slowperiod: "Slow EMA period (default 10)"
    :return: "Chaikin Oscillator: EMA_fast(ADL) - EMA_slow(ADL)"
    '''
    import talib
    return talib.ADOSC(high, low, close, volume, fastperiod=fastperiod, slowperiod=slowperiod)


# ---------------------------------------------------------------------------
# 37. chain_ladder_development
# ---------------------------------------------------------------------------
def chain_ladder_development(latest_cumulative, cdf):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Reserving', 'Loss development']
    function: "Projects ultimate claims using the chain-ladder development method by applying cumulative development factors (CDFs) to the latest cumulative claims."
    y_as_x: []
    :param latest_cumulative: "Latest cumulative claims amount for the origin year"
    :param cdf: "Cumulative development factor (CDF) from the latest development period to ultimate"
    :return: "Ultimate claims: Ultimate = Latest * CDF"
    '''
    return latest_cumulative * cdf


# ---------------------------------------------------------------------------
# 38. charm
# ---------------------------------------------------------------------------
def charm(S, K, T, r, sigma, option_type='call', dT=1/365):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Greeks', 'Second-order sensitivities']
    function: "Computes charm (delta decay), the rate of change of delta with respect to the passage of time."
    y_as_x: []
    :param S: "Current underlying asset price"
    :param K: "Strike price"
    :param T: "Time to expiration in years"
    :param r: "Risk-free interest rate (continuous)"
    :param sigma: "Volatility of the underlying"
    :param option_type: "'call' or 'put' (default 'call')"
    :param dT: "Time increment for numerical differentiation (default 1/365)"
    :return: "Charm: d(Delta)/dt computed numerically"
    '''
    from scipy.stats import norm
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == 'call':
        charm_val = -np.exp(-r * T) * (norm.pdf(d1) * (2 * r * T - d2 * sigma * np.sqrt(T)) / (2 * T * sigma * np.sqrt(T)))
    else:
        charm_val = -np.exp(-r * T) * (norm.pdf(d1) * (2 * r * T - d2 * sigma * np.sqrt(T)) / (2 * T * sigma * np.sqrt(T)))
        # For puts, charm has the same formula for the time-dependent part
        # but delta itself differs; the decay component is:
        charm_val = charm_val + r * np.exp(-r * T) * norm.cdf(-d1)
        # Correction: re-derive
    # More robust: numerical
    d1_1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d1_2 = (np.log(S / K) + (r + 0.5 * sigma**2) * (T - dT)) / (sigma * np.sqrt(T - dT)) if T > dT else d1_1
    if option_type == 'call':
        delta_1 = norm.cdf(d1_1)
        delta_2 = norm.cdf(d1_2) if T > dT else delta_1
    else:
        delta_1 = norm.cdf(d1_1) - 1
        delta_2 = (norm.cdf(d1_2) - 1) if T > dT else delta_1
    return (delta_2 - delta_1) / (-dT)


# ---------------------------------------------------------------------------
# 39. chooser_option_value
# ---------------------------------------------------------------------------
def chooser_option_value(S, K, T_choose, T_expire, r, sigma, q=0.0):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Exotic options', 'Chooser options']
    function: "Values a simple chooser option that gives the holder the right to choose between a call and a put at the decision date."
    y_as_x: []
    :param S: "Current underlying asset price"
    :param K: "Strike price for both the call and put"
    :param T_choose: "Time to the choice date in years"
    :param T_expire: "Time to expiration in years (T_expire > T_choose)"
    :param r: "Risk-free interest rate (continuous)"
    :param sigma: "Volatility of the underlying"
    :param q: "Continuous dividend yield (default 0)"
    :return: "Chooser option value using the Rubinstein (1991) decomposition"
    '''
    from scipy.stats import norm
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T_expire) / (sigma * np.sqrt(T_expire))
    d2 = d1 - sigma * np.sqrt(T_expire)
    y = (np.log(S / K) + (r - q) * T_expire + 0.5 * sigma**2 * T_choose) / (sigma * np.sqrt(T_choose))
    # Simple chooser = Call(S, K, T_expire) + Put(S, K*exp(-(r-q)*(T_expire-T_choose)), T_choose)
    # But standard decomposition:
    call_value = S * np.exp(-q * T_expire) * norm.cdf(d1) - K * np.exp(-r * T_expire) * norm.cdf(d2)
    # Put component via parity adjustment
    d1_choose = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T_choose) / (sigma * np.sqrt(T_choose))
    d2_choose = d1_choose - sigma * np.sqrt(T_choose)
    # Chooser = C(S,K,T_expire) - S*exp(-q*T_expire)*N(-d1) + K*exp(-r*T_expire)*N(-d2_choose)
    # Using Rubinstein's formula:
    chooser = (S * np.exp(-q * T_expire) * norm.cdf(d1)
               - K * np.exp(-r * T_expire) * norm.cdf(d2)
               - S * np.exp(-q * T_expire) * norm.cdf(-y)
               + K * np.exp(-r * T_expire) * norm.cdf(-y + sigma * np.sqrt(T_choose)))
    return chooser


# ---------------------------------------------------------------------------
# 40. christoffersen_independence_test
# ---------------------------------------------------------------------------
def christoffersen_independence_test(hit_sequence):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Backtesting', 'VaR validation']
    function: "Performs the Christoffersen (1998) independence test for VaR violations, testing whether exceptions are serially independent."
    y_as_x: []
    :param hit_sequence: "Binary array where 1 indicates a VaR violation (hit) and 0 indicates no violation"
    :return: "Tuple of (LR_ind statistic, p-value) under chi-squared(1) distribution"
    '''
    hits = np.asarray(hit_sequence, dtype=int)
    n = len(hits)
    # Count transitions
    n00 = n01 = n10 = n11 = 0
    for i in range(n - 1):
        if hits[i] == 0 and hits[i+1] == 0:
            n00 += 1
        elif hits[i] == 0 and hits[i+1] == 1:
            n01 += 1
        elif hits[i] == 1 and hits[i+1] == 0:
            n10 += 1
        else:
            n11 += 1
    # Transition probabilities
    p01 = n01 / (n00 + n01) if (n00 + n01) > 0 else 0
    p11 = n11 / (n10 + n11) if (n10 + n11) > 0 else 0
    # Unconditional probability
    pi_hat = (n01 + n11) / (n00 + n01 + n10 + n11) if (n00 + n01 + n10 + n11) > 0 else 0

    # Log-likelihoods
    def safe_log(x):
        return np.log(x) if x > 0 else 0

    ll_unrestricted = (n00 * safe_log(1 - p01) + n01 * safe_log(p01)
                       + n10 * safe_log(1 - p11) + n11 * safe_log(p11))
    ll_restricted = ((n00 + n10) * safe_log(1 - pi_hat)
                     + (n01 + n11) * safe_log(pi_hat))

    lr_ind = -2 * (ll_restricted - ll_unrestricted)
    p_value = 1 - stats.chi2.cdf(lr_ind, 1)
    return (lr_ind, p_value)


# ---------------------------------------------------------------------------
# 41. cir_short_rate_model
# ---------------------------------------------------------------------------
def cir_short_rate_model(r0, kappa, theta, sigma, T, n_steps=252, n_paths=1000, seed=None):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Short-rate models', 'Stochastic processes']
    function: "Simulates the Cox-Ingersoll-Ross (CIR) short-rate process: dr_t = kappa*(theta - r_t)*dt + sigma*sqrt(r_t)*dW_t."
    y_as_x: ['cir_zero_coupon_bond_price']
    :param r0: "Initial short rate"
    :param kappa: "Speed of mean reversion"
    :param theta: "Long-run mean level of the short rate"
    :param sigma: "Volatility parameter"
    :param T: "Time horizon in years"
    :param n_steps: "Number of time steps (default 252)"
    :param n_paths: "Number of simulation paths (default 1000)"
    :param seed: "Random seed for reproducibility (optional)"
    :return: "Numpy array of shape (n_paths, n_steps+1) with simulated short rate paths"
    '''
    if seed is not None:
        np.random.seed(seed)
    dt = T / n_steps
    rates = np.zeros((n_paths, n_steps + 1))
    rates[:, 0] = r0
    for t in range(n_steps):
        r_t = rates[:, t]
        r_t = np.maximum(r_t, 0)  # Ensure non-negative
        dW = np.random.standard_normal(n_paths) * np.sqrt(dt)
        rates[:, t + 1] = r_t + kappa * (theta - r_t) * dt + sigma * np.sqrt(r_t) * dW
        rates[:, t + 1] = np.maximum(rates[:, t + 1], 0)
    return rates


# ---------------------------------------------------------------------------
# 42. cir_zero_coupon_bond_price
# ---------------------------------------------------------------------------
def cir_zero_coupon_bond_price(r, kappa, theta, sigma, T):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Bond pricing', 'Affine term structure']
    function: "Computes the zero-coupon bond price under the CIR model: P(t,T) = A(t,T)*exp(-B(t,T)*r_t)."
    y_as_x: []
    :param r: "Current short rate"
    :param kappa: "Speed of mean reversion"
    :param theta: "Long-run mean level"
    :param sigma: "Volatility parameter"
    :param T: "Time to maturity in years"
    :return: "Zero-coupon bond price under CIR model"
    '''
    gamma = np.sqrt(kappa**2 + 2 * sigma**2)
    exp_gamma_T = np.exp(gamma * T)
    denom = (gamma + kappa) * (exp_gamma_T - 1) + 2 * gamma

    B = 2 * (exp_gamma_T - 1) / denom
    A = (2 * gamma * np.exp((kappa + gamma) * T / 2) / denom) ** (2 * kappa * theta / sigma**2)

    return A * np.exp(-B * r)


# ---------------------------------------------------------------------------
# 43. claims_ratio
# ---------------------------------------------------------------------------
def claims_ratio(claims_incurred, earned_premium):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Insurance ratios', 'Underwriting performance']
    function: "Computes the claims ratio (loss ratio), measuring the proportion of earned premium consumed by claims."
    y_as_x: ['combined_ratio']
    :param claims_incurred: "Total claims incurred during the period"
    :param earned_premium: "Total earned premium during the period"
    :return: "Claims ratio: Claims Incurred / Earned Premium"
    '''
    return claims_incurred / earned_premium


# ---------------------------------------------------------------------------
# 44. clean_price
# ---------------------------------------------------------------------------
def clean_price(dirty_price, accrued_interest):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Bond pricing', 'Settlement']
    function: "Computes the clean (quoted) price of a bond by subtracting accrued interest from the dirty (full) price."
    y_as_x: []
    :param dirty_price: "Dirty (full invoice) price of the bond including accrued interest"
    :param accrued_interest: "Accrued interest from the last coupon date to the settlement date"
    :return: "Clean price: Dirty Price - Accrued Interest"
    '''
    return dirty_price - accrued_interest


# ---------------------------------------------------------------------------
# 45. cltv_for_mortgage
# ---------------------------------------------------------------------------
def cltv_for_mortgage(all_secured_debt, property_value):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Mortgage metrics', 'Lending criteria']
    function: "Computes the combined loan-to-value (CLTV) ratio for a mortgage considering all secured debt on the property."
    y_as_x: []
    :param all_secured_debt: "Total of all secured debt against the property (first mortgage + second lien + HELOC, etc.)"
    :param property_value: "Current market or appraised value of the property"
    :return: "CLTV = All Secured Debt / Property Value"
    '''
    return all_secured_debt / property_value


# ---------------------------------------------------------------------------
# 46. cointegration_regression
# ---------------------------------------------------------------------------
def cointegration_regression(y, x):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Time series analysis', 'Cointegration']
    function: "Performs the Engle-Granger two-step cointegration test between two time series."
    y_as_x: []
    :param y: "Dependent time series (array-like)"
    :param x: "Independent time series (array-like)"
    :return: "Tuple of (t-statistic, p-value, critical values dict) from statsmodels coint test"
    '''
    from statsmodels.tsa.stattools import coint
    result = coint(y, x)
    return result  # (t_stat, p_value, crit_values)


# ---------------------------------------------------------------------------
# 47. collateral_haircut
# ---------------------------------------------------------------------------
def collateral_haircut(lending_value, market_value):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Collateral management', 'Risk mitigation']
    function: "Computes the haircut applied to collateral, representing the discount from market value to lending value."
    y_as_x: []
    :param lending_value: "Value at which the collateral is accepted for lending purposes"
    :param market_value: "Current market value of the collateral"
    :return: "Haircut = 1 - Lending Value / Market Value"
    '''
    return 1 - lending_value / market_value


# ---------------------------------------------------------------------------
# 48. color
# ---------------------------------------------------------------------------
def color(S, K, T, r, sigma, dT=1/365):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Greeks', 'Third-order sensitivities']
    function: "Computes color (gamma decay), the rate of change of gamma with respect to time."
    y_as_x: []
    :param S: "Current underlying asset price"
    :param K: "Strike price"
    :param T: "Time to expiration in years"
    :param r: "Risk-free interest rate (continuous)"
    :param sigma: "Volatility of the underlying"
    :param dT: "Time increment for numerical differentiation (default 1/365)"
    :return: "Color: d(Gamma)/dt computed analytically"
    '''
    from scipy.stats import norm
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    color_val = -norm.pdf(d1) / (2 * S * T * sigma * np.sqrt(T)) * (
        2 * r * T - d2 * sigma * np.sqrt(T) + 1
    )
    return color_val


# ---------------------------------------------------------------------------
# 49. combined_leverage
# ---------------------------------------------------------------------------
def combined_leverage(degree_of_operating_leverage, degree_of_financial_leverage):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Leverage analysis', 'Risk analysis']
    function: "Computes the degree of combined leverage (DCL), capturing the total sensitivity of EPS to changes in sales."
    y_as_x: []
    :param degree_of_operating_leverage: "Degree of operating leverage (DOL)"
    :param degree_of_financial_leverage: "Degree of financial leverage (DFL)"
    :return: "Combined leverage: DCL = DOL x DFL"
    '''
    return degree_of_operating_leverage * degree_of_financial_leverage


# ---------------------------------------------------------------------------
# 50. combined_loan_to_value_cltv
# ---------------------------------------------------------------------------
def combined_loan_to_value_cltv(total_secured_debt, collateral_value):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Lending metrics', 'Credit underwriting']
    function: "Computes the combined loan-to-value (CLTV) ratio for all secured debt against collateral."
    y_as_x: []
    :param total_secured_debt: "Sum of all secured loans against the collateral"
    :param collateral_value: "Appraised or market value of the collateral"
    :return: "CLTV = Total Secured Debt / Collateral Value"
    '''
    return total_secured_debt / collateral_value


# ---------------------------------------------------------------------------
# 51. combined_ratio
# ---------------------------------------------------------------------------
def combined_ratio(loss_ratio, expense_ratio):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Insurance ratios', 'Underwriting profitability']
    function: "Computes the combined ratio, the primary measure of insurance underwriting profitability. A ratio below 100% indicates underwriting profit."
    y_as_x: []
    :param loss_ratio: "Loss ratio (claims incurred / earned premium)"
    :param expense_ratio: "Expense ratio (underwriting expenses / earned premium)"
    :return: "Combined ratio: Loss Ratio + Expense Ratio"
    '''
    return loss_ratio + expense_ratio


# ---------------------------------------------------------------------------
# 52. commodity_carry_return
# ---------------------------------------------------------------------------
def commodity_carry_return(collateral_yield, roll_yield, spot_return):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Commodity returns', 'Return decomposition']
    function: "Decomposes total commodity futures return into its three components: collateral yield, roll yield, and spot return."
    y_as_x: []
    :param collateral_yield: "Return earned on the collateral backing the futures position (e.g., T-bill yield)"
    :param roll_yield: "Return from rolling futures contracts (contango gives negative, backwardation positive)"
    :param spot_return: "Return from the change in the spot price of the commodity"
    :return: "Total carry return: collateral yield + roll yield + spot return"
    '''
    return collateral_yield + roll_yield + spot_return


# ---------------------------------------------------------------------------
# 53. commodity_channel_index_cci
# ---------------------------------------------------------------------------
def commodity_channel_index_cci(high, low, close, timeperiod=14):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Momentum indicators', 'Overbought/oversold']
    function: "Computes the Commodity Channel Index (CCI), measuring the deviation of the typical price from its moving average."
    y_as_x: []
    :param high: "Numpy array of high prices"
    :param low: "Numpy array of low prices"
    :param close: "Numpy array of closing prices"
    :param timeperiod: "Lookback period (default 14)"
    :return: "CCI = (TP - SMA(TP)) / (0.015 * Mean Deviation)"
    '''
    import talib
    return talib.CCI(high, low, close, timeperiod=timeperiod)


# ---------------------------------------------------------------------------
# 54. commodity_storage_arbitrage
# ---------------------------------------------------------------------------
def commodity_storage_arbitrage(F0, S0, r, u, y, T):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Storage economics', 'Arbitrage strategies']
    function: "Determines whether a commodity storage arbitrage opportunity exists by comparing the futures price to the theoretical no-arbitrage bound."
    y_as_x: []
    :param F0: "Observed futures price"
    :param S0: "Current spot price"
    :param r: "Risk-free interest rate (continuous)"
    :param u: "Storage cost rate (continuous, per annum)"
    :param y: "Convenience yield rate (continuous, per annum)"
    :param T: "Time to maturity in years"
    :return: "Dictionary with 'theoretical_price', 'observed_price', 'arbitrage_profit', and 'arbitrage_exists' (bool)"
    '''
    theoretical = S0 * np.exp((r + u - y) * T)
    profit = F0 - theoretical
    return {
        'theoretical_price': theoretical,
        'observed_price': F0,
        'arbitrage_profit': profit,
        'arbitrage_exists': F0 > theoretical
    }


# ---------------------------------------------------------------------------
# 55. component_risk_contribution
# ---------------------------------------------------------------------------
def component_risk_contribution(weights, cov_matrix):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Risk budgeting', 'Portfolio risk']
    function: "Computes the component risk contribution (CRC) for each asset: CRC_i = w_i * MRC_i, where MRC is the marginal risk contribution."
    y_as_x: []
    :param weights: "Array of portfolio weights"
    :param cov_matrix: "Covariance matrix of asset returns (n x n)"
    :return: "Array of component risk contributions (CRC_i = w_i * (Sigma @ w)_i / sigma_p)"
    '''
    weights = np.asarray(weights, dtype=float)
    cov_matrix = np.asarray(cov_matrix, dtype=float)
    port_var = weights @ cov_matrix @ weights
    port_vol = np.sqrt(port_var)
    mrc = (cov_matrix @ weights) / port_vol
    return weights * mrc


# ---------------------------------------------------------------------------
# 56. component_var
# ---------------------------------------------------------------------------
def component_var(weights, cov_matrix, confidence=0.95, portfolio_value=1.0):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Value at Risk', 'Risk decomposition']
    function: "Computes component VaR for each asset, decomposing total portfolio VaR into additive contributions."
    y_as_x: []
    :param weights: "Array of portfolio weights"
    :param cov_matrix: "Covariance matrix of asset returns (n x n)"
    :param confidence: "Confidence level (default 0.95)"
    :param portfolio_value: "Total portfolio value (default 1.0)"
    :return: "Array of component VaR values (sum equals total portfolio VaR)"
    '''
    weights = np.asarray(weights, dtype=float)
    cov_matrix = np.asarray(cov_matrix, dtype=float)
    z = stats.norm.ppf(confidence)
    port_var = weights @ cov_matrix @ weights
    port_vol = np.sqrt(port_var)
    mvar = z * (cov_matrix @ weights) / port_vol
    return weights * mvar * portfolio_value


# ---------------------------------------------------------------------------
# 57. component_var_v2
# ---------------------------------------------------------------------------
def component_var_v2(weights, cov_matrix, confidence=0.95, portfolio_value=1.0):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Value at Risk', 'Risk decomposition']
    function: "Computes component VaR using the partial derivative approach: CVaR_i = w_i * dVaR/dw_i."
    y_as_x: []
    :param weights: "Array of portfolio weights"
    :param cov_matrix: "Covariance matrix of asset returns (n x n)"
    :param confidence: "Confidence level (default 0.95)"
    :param portfolio_value: "Total portfolio value (default 1.0)"
    :return: "Array of component VaR values"
    '''
    weights = np.asarray(weights, dtype=float)
    cov_matrix = np.asarray(cov_matrix, dtype=float)
    z = stats.norm.ppf(confidence)
    port_vol = np.sqrt(weights @ cov_matrix @ weights)
    # dVaR/dw_i = z * (Sigma @ w)_i / port_vol
    dvar_dw = z * (cov_matrix @ weights) / port_vol
    return weights * dvar_dw * portfolio_value


# ---------------------------------------------------------------------------
# 58. compounded_forward_rate
# ---------------------------------------------------------------------------
def compounded_forward_rate(df_t1, df_t2, tau):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Forward rates', 'Discount factors']
    function: "Computes the simply-compounded forward rate between two dates from discount factors."
    y_as_x: []
    :param df_t1: "Discount factor to time t1"
    :param df_t2: "Discount factor to time t2 (t2 > t1)"
    :param tau: "Year fraction between t1 and t2"
    :return: "Forward rate F such that (1 + F*tau) = DF(t1)/DF(t2)"
    '''
    return (df_t1 / df_t2 - 1) / tau


# ---------------------------------------------------------------------------
# 59. conditional_prepayment_rate_cpr
# ---------------------------------------------------------------------------
def conditional_prepayment_rate_cpr(smm):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Prepayment modeling', 'MBS analytics']
    function: "Converts the single monthly mortality (SMM) rate to an annualized conditional prepayment rate (CPR)."
    y_as_x: []
    :param smm: "Single monthly mortality rate"
    :return: "CPR = 1 - (1 - SMM)^12"
    '''
    return 1 - (1 - smm) ** 12


# ---------------------------------------------------------------------------
# 60. conditional_prepayment_rate_cpr_v2
# ---------------------------------------------------------------------------
def conditional_prepayment_rate_cpr_v2(smm):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Prepayment modeling', 'MBS analytics']
    function: "Converts the single monthly mortality (SMM) rate to an annualized conditional prepayment rate (CPR). Equivalent formulation."
    y_as_x: []
    :param smm: "Single monthly mortality rate"
    :return: "CPR = 1 - (1 - SMM)^12"
    '''
    return 1 - (1 - smm) ** 12


# ---------------------------------------------------------------------------
# 61. constant_force_survival
# ---------------------------------------------------------------------------
def constant_force_survival(mu, t):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Survival models', 'Life contingencies']
    function: "Computes the survival probability under a constant force of mortality model."
    y_as_x: []
    :param mu: "Constant force of mortality (hazard rate)"
    :param t: "Time period in years"
    :return: "Survival probability: t_p_x = exp(-mu * t)"
    '''
    return np.exp(-mu * t)


# ---------------------------------------------------------------------------
# 62. consumer_price_index_laspeyres_form
# ---------------------------------------------------------------------------
def consumer_price_index_laspeyres_form(prices_current, prices_base, quantities_base):
    '''
    domain: ['Macroeconomics, inflation & price indices']
    subdomain: ['Price indices', 'CPI construction']
    function: "Computes the Consumer Price Index using the Laspeyres formula with base-period quantities as weights."
    y_as_x: ['cpi_inflation_month_over_month', 'cpi_inflation_year_over_year', 'cumulative_inflation_factor_from_cpi']
    :param prices_current: "Array of current period prices for each item"
    :param prices_base: "Array of base period prices for each item"
    :param quantities_base: "Array of base period quantities (weights) for each item"
    :return: "CPI = (sum(p_t * q_0) / sum(p_0 * q_0)) * 100"
    '''
    prices_current = np.asarray(prices_current, dtype=float)
    prices_base = np.asarray(prices_base, dtype=float)
    quantities_base = np.asarray(quantities_base, dtype=float)
    return (np.sum(prices_current * quantities_base) / np.sum(prices_base * quantities_base)) * 100


# ---------------------------------------------------------------------------
# 63. contango_slope
# ---------------------------------------------------------------------------
def contango_slope(F_long, F_short):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Futures term structure', 'Contango/backwardation']
    function: "Computes the contango slope between two futures contracts of different maturities."
    y_as_x: []
    :param F_long: "Price of the longer-dated futures contract"
    :param F_short: "Price of the shorter-dated futures contract"
    :return: "Contango slope: F_long / F_short - 1 (positive indicates contango)"
    '''
    return F_long / F_short - 1


# ---------------------------------------------------------------------------
# 64. continuous_compounding
# ---------------------------------------------------------------------------
def continuous_compounding(pv, r, t):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Compounding conventions', 'Time value of money']
    function: "Computes the future value using continuous compounding."
    y_as_x: []
    :param pv: "Present value (initial investment)"
    :param r: "Continuously compounded annual interest rate"
    :param t: "Time in years"
    :return: "Future value: FV = PV * exp(r * t)"
    '''
    return pv * np.exp(r * t)


# ---------------------------------------------------------------------------
# 65. contribution_margin
# ---------------------------------------------------------------------------
def contribution_margin(revenue, variable_costs):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Cost analysis', 'Profitability']
    function: "Computes the contribution margin, the amount of revenue remaining after deducting variable costs."
    y_as_x: ['contribution_margin_ratio', 'break_even_revenue']
    :param revenue: "Total revenue"
    :param variable_costs: "Total variable costs"
    :return: "Contribution margin: Revenue - Variable Costs"
    '''
    return revenue - variable_costs


# ---------------------------------------------------------------------------
# 66. contribution_margin_ratio
# ---------------------------------------------------------------------------
def contribution_margin_ratio(contribution_margin, revenue):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Cost analysis', 'Profitability']
    function: "Computes the contribution margin ratio, expressing the contribution margin as a percentage of revenue."
    y_as_x: ['break_even_revenue']
    :param contribution_margin: "Total contribution margin (Revenue - Variable Costs)"
    :param revenue: "Total revenue"
    :return: "Contribution margin ratio: CM / Revenue"
    '''
    return contribution_margin / revenue


# ---------------------------------------------------------------------------
# 67. contribution_to_return
# ---------------------------------------------------------------------------
def contribution_to_return(weight, asset_return):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Return decomposition', 'Portfolio analysis']
    function: "Computes the contribution of a single asset or sector to the total portfolio return."
    y_as_x: ['portfolio_return']
    :param weight: "Weight of the asset in the portfolio"
    :param asset_return: "Return of the asset over the period"
    :return: "Contribution to return: w_i * r_i"
    '''
    return weight * asset_return


# ---------------------------------------------------------------------------
# 68. convenience_yield
# ---------------------------------------------------------------------------
def convenience_yield(r, u, F0, S0, T):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Storage economics', 'Commodity pricing']
    function: "Backs out the implied convenience yield from the observed futures price and spot price."
    y_as_x: ['cost_of_carry_futures_price', 'commodity_storage_arbitrage']
    :param r: "Risk-free interest rate (continuous)"
    :param u: "Storage cost rate (continuous, per annum)"
    :param F0: "Observed futures price"
    :param S0: "Current spot price"
    :param T: "Time to maturity in years"
    :return: "Convenience yield: y = r + u - (1/T)*ln(F0/S0)"
    '''
    return r + u - (1 / T) * np.log(F0 / S0)


# ---------------------------------------------------------------------------
# 69. convenience_yield_from_futures_curve
# ---------------------------------------------------------------------------
def convenience_yield_from_futures_curve(r, u, F, S, T):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Storage economics', 'Commodity pricing']
    function: "Computes the implied convenience yield from a futures curve observation."
    y_as_x: []
    :param r: "Risk-free interest rate (continuous)"
    :param u: "Storage cost rate (continuous, per annum)"
    :param F: "Observed futures price at maturity T"
    :param S: "Current spot price"
    :param T: "Time to maturity in years"
    :return: "Convenience yield: y = r + u - ln(F/S)/T"
    '''
    return r + u - np.log(F / S) / T


# ---------------------------------------------------------------------------
# 70. convexity
# ---------------------------------------------------------------------------
def convexity(face_value, coupon_rate, ytm, periods, freq=2):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Bond analytics', 'Interest rate risk']
    function: "Computes the convexity of a fixed-rate bond, measuring the curvature of the price-yield relationship."
    y_as_x: ['approximate_price_change', 'convexity_adjusted_futures_rate']
    :param face_value: "Par (face) value of the bond"
    :param coupon_rate: "Annual coupon rate"
    :param ytm: "Yield to maturity (annual)"
    :param periods: "Total number of coupon periods remaining"
    :param freq: "Coupon frequency per year (default 2 for semi-annual)"
    :return: "Convexity: (1/P) * sum(t*(t+1)*CF_t / (1+y/freq)^(t+2)) / freq^2"
    '''
    coupon = face_value * coupon_rate / freq
    y = ytm / freq
    price = 0.0
    conv_sum = 0.0
    for t in range(1, periods + 1):
        cf = coupon if t < periods else coupon + face_value
        df = (1 + y) ** t
        price += cf / df
        conv_sum += t * (t + 1) * cf / ((1 + y) ** (t + 2))
    convexity_val = conv_sum / (price * freq**2)
    return convexity_val


# ---------------------------------------------------------------------------
# 71. convexity_adjusted_futures_rate
# ---------------------------------------------------------------------------
def convexity_adjusted_futures_rate(futures_rate, sigma, T1, T2):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Futures pricing', 'Convexity adjustment']
    function: "Applies a convexity adjustment to convert a futures rate to an equivalent forward rate."
    y_as_x: []
    :param futures_rate: "Observed futures rate (e.g., Eurodollar futures implied rate)"
    :param sigma: "Volatility of the short rate"
    :param T1: "Start time of the forward period in years"
    :param T2: "End time of the forward period in years"
    :return: "Adjusted forward rate: F_adj = F_futures - 0.5 * sigma^2 * T1 * T2"
    '''
    return futures_rate - 0.5 * sigma**2 * T1 * T2


# ---------------------------------------------------------------------------
# 72. cornish_fisher_var
# ---------------------------------------------------------------------------
def cornish_fisher_var(mu, sigma, skewness, excess_kurtosis, confidence=0.95):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Value at Risk', 'Non-normal distributions']
    function: "Computes the Cornish-Fisher expansion VaR, adjusting the standard normal quantile for skewness and kurtosis."
    y_as_x: []
    :param mu: "Expected return (mean)"
    :param sigma: "Standard deviation of returns"
    :param skewness: "Skewness of the return distribution (S)"
    :param excess_kurtosis: "Excess kurtosis of the return distribution (K)"
    :param confidence: "Confidence level (default 0.95)"
    :return: "Cornish-Fisher VaR: mu + sigma * [z + (z^2-1)*S/6 + (z^3-3z)*K/24 - (2z^3-5z)*S^2/36]"
    '''
    z = stats.norm.ppf(1 - confidence)  # negative quantile for loss
    z_cf = (z
            + (z**2 - 1) * skewness / 6
            + (z**3 - 3 * z) * excess_kurtosis / 24
            - (2 * z**3 - 5 * z) * skewness**2 / 36)
    return -(mu + sigma * z_cf)


# ---------------------------------------------------------------------------
# 73. cost_of_equity_capm
# ---------------------------------------------------------------------------
def cost_of_equity_capm(risk_free_rate, beta, market_return):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Cost of capital', 'Equity valuation']
    function: "Computes the cost of equity using the Capital Asset Pricing Model (CAPM)."
    y_as_x: ['weighted_average_cost_of_capital_wacc']
    :param risk_free_rate: "Risk-free rate of return"
    :param beta: "Equity beta of the company"
    :param market_return: "Expected market return"
    :return: "Cost of equity: R_e = R_f + beta * (E[R_m] - R_f)"
    '''
    return risk_free_rate + beta * (market_return - risk_free_rate)


# ---------------------------------------------------------------------------
# 74. cost_of_equity_dividend_growth
# ---------------------------------------------------------------------------
def cost_of_equity_dividend_growth(D1, P0, g):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Cost of capital', 'Dividend discount']
    function: "Computes the cost of equity using the Gordon Growth (dividend discount) model."
    y_as_x: ['weighted_average_cost_of_capital_wacc']
    :param D1: "Expected dividend per share next period"
    :param P0: "Current stock price"
    :param g: "Constant dividend growth rate"
    :return: "Cost of equity: R_e = D1/P0 + g"
    '''
    return D1 / P0 + g


# ---------------------------------------------------------------------------
# 75. cost_of_risk
# ---------------------------------------------------------------------------
def cost_of_risk(loan_loss_provision, average_gross_loans):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Credit risk', 'Asset quality']
    function: "Computes the cost of risk ratio, measuring the provision charge relative to the average loan book."
    y_as_x: []
    :param loan_loss_provision: "Total loan loss provision (impairment charge) for the period"
    :param average_gross_loans: "Average gross loan balance over the period"
    :return: "Cost of risk: Loan Loss Provision / Average Gross Loans"
    '''
    return loan_loss_provision / average_gross_loans


# ---------------------------------------------------------------------------
# 76. cost_of_carry_futures_price
# ---------------------------------------------------------------------------
def cost_of_carry_futures_price(S0, r, u, y, T):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Futures pricing', 'Cost of carry']
    function: "Computes the theoretical futures price using the cost-of-carry model for commodities."
    y_as_x: ['commodity_storage_arbitrage']
    :param S0: "Current spot price"
    :param r: "Risk-free interest rate (continuous)"
    :param u: "Storage cost rate (continuous, per annum)"
    :param y: "Convenience yield rate (continuous, per annum)"
    :param T: "Time to maturity in years"
    :return: "Futures price: F_0 = S_0 * exp((r + u - y) * T)"
    '''
    return S0 * np.exp((r + u - y) * T)


# ---------------------------------------------------------------------------
# 77. countercyclical_capital_buffer
# ---------------------------------------------------------------------------
def countercyclical_capital_buffer(jurisdiction_buffer_rate, rwa):
    '''
    domain: ['Bank regulation, Basel & prudential ratios']
    subdomain: ['Capital adequacy', 'Macroprudential regulation']
    function: "Computes the countercyclical capital buffer (CCyB) amount, a jurisdiction-specific add-on to the CET1 capital requirement."
    y_as_x: []
    :param jurisdiction_buffer_rate: "CCyB rate set by the national authority (e.g., 0.025 for 2.5%)"
    :param rwa: "Risk-weighted assets"
    :return: "CCyB capital amount: jurisdiction_buffer_rate * RWA"
    '''
    return jurisdiction_buffer_rate * rwa


# ---------------------------------------------------------------------------
# 78. covariance_matrix
# ---------------------------------------------------------------------------
def covariance_matrix(returns):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Risk modeling', 'Covariance estimation']
    function: "Estimates the sample covariance matrix of asset returns using the PyPortfolioOpt library."
    y_as_x: ['portfolio_variance', 'portfolio_volatility', 'component_risk_contribution', 'component_var', 'component_var_v2', 'global_minimum_variance_portfolio', 'efficient_frontier_problem', 'maximum_sharpe_portfolio']
    :param returns: "Pandas DataFrame of asset returns where columns are assets"
    :return: "Pandas DataFrame of the sample covariance matrix"
    '''
    from pypfopt.risk_models import sample_cov
    return sample_cov(returns)


# ---------------------------------------------------------------------------
# 79. coverage_ratio
# ---------------------------------------------------------------------------
def coverage_ratio(allowance, nonperforming_assets):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Asset quality', 'Loan loss reserves']
    function: "Computes the coverage ratio, measuring the adequacy of loan loss reserves relative to nonperforming assets."
    y_as_x: []
    :param allowance: "Allowance for loan losses (reserves)"
    :param nonperforming_assets: "Total nonperforming assets (NPAs)"
    :return: "Coverage ratio: Allowance / Nonperforming Assets"
    '''
    return allowance / nonperforming_assets


# ---------------------------------------------------------------------------
# 80. covered_call_payoff
# ---------------------------------------------------------------------------
def covered_call_payoff(S_T, K, premium):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Option strategies', 'Income strategies']
    function: "Computes the payoff of a covered call position (long stock + short call) at expiration."
    y_as_x: []
    :param S_T: "Underlying asset price at expiration (scalar or array)"
    :param K: "Strike price of the short call"
    :param premium: "Premium received from selling the call option"
    :return: "Covered call payoff: S_T - max(S_T - K, 0) + Premium"
    '''
    S_T = np.asarray(S_T, dtype=float)
    return S_T - np.maximum(S_T - K, 0) + premium


# ---------------------------------------------------------------------------
# 81. covered_interest_parity_cip
# ---------------------------------------------------------------------------
def covered_interest_parity_cip(S, i_domestic, i_foreign):
    '''
    domain: ['FX & international finance']
    subdomain: ['Interest rate parity', 'FX forwards']
    function: "Computes the theoretical forward exchange rate using covered interest rate parity (CIP)."
    y_as_x: []
    :param S: "Current spot exchange rate (domestic/foreign)"
    :param i_domestic: "Domestic interest rate for the period"
    :param i_foreign: "Foreign interest rate for the period"
    :return: "Forward rate: F = S * (1 + i_d) / (1 + i_f)"
    '''
    return S * (1 + i_domestic) / (1 + i_foreign)


# ---------------------------------------------------------------------------
# 82. cox_proportional_hazards
# ---------------------------------------------------------------------------
def cox_proportional_hazards(data, duration_col, event_col):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Survival analysis', 'Hazard modeling']
    function: "Fits a Cox Proportional Hazards model: h(t|x) = h_0(t) * exp(beta' * x)."
    y_as_x: []
    :param data: "Pandas DataFrame with covariates, duration, and event columns"
    :param duration_col: "Name of the column containing time-to-event durations"
    :param event_col: "Name of the column containing event indicators (1 = event, 0 = censored)"
    :return: "Fitted CoxPHFitter object with accessible .summary, .hazards_, .predict_survival_function()"
    '''
    from lifelines import CoxPHFitter
    cph = CoxPHFitter()
    cph.fit(data, duration_col=duration_col, event_col=event_col)
    return cph


# ---------------------------------------------------------------------------
# 83. cox_ingersoll_ross_cir_process
# ---------------------------------------------------------------------------
def cox_ingersoll_ross_cir_process(r0, a, b, sigma, T, n_steps=252, n_paths=1000, seed=None):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Short-rate models', 'Stochastic processes']
    function: "Simulates the CIR process: dr_t = a*(b - r_t)*dt + sigma*sqrt(r_t)*dW_t."
    y_as_x: []
    :param r0: "Initial short rate"
    :param a: "Speed of mean reversion"
    :param b: "Long-run mean level"
    :param sigma: "Volatility parameter"
    :param T: "Time horizon in years"
    :param n_steps: "Number of time steps (default 252)"
    :param n_paths: "Number of simulation paths (default 1000)"
    :param seed: "Random seed for reproducibility (optional)"
    :return: "Numpy array of shape (n_paths, n_steps+1) with simulated rate paths"
    '''
    if seed is not None:
        np.random.seed(seed)
    dt = T / n_steps
    rates = np.zeros((n_paths, n_steps + 1))
    rates[:, 0] = r0
    for t in range(n_steps):
        r_t = np.maximum(rates[:, t], 0)
        dW = np.random.standard_normal(n_paths) * np.sqrt(dt)
        rates[:, t + 1] = r_t + a * (b - r_t) * dt + sigma * np.sqrt(r_t) * dW
        rates[:, t + 1] = np.maximum(rates[:, t + 1], 0)
    return rates


# ---------------------------------------------------------------------------
# 84. cpi_inflation_month_over_month
# ---------------------------------------------------------------------------
def cpi_inflation_month_over_month(cpi_t, cpi_t_minus_1):
    '''
    domain: ['Macroeconomics, inflation & price indices']
    subdomain: ['Inflation measurement', 'CPI analysis']
    function: "Computes month-over-month CPI inflation rate."
    y_as_x: ['annualized_cpi_inflation_from_monthly_cpi']
    :param cpi_t: "CPI value in the current month"
    :param cpi_t_minus_1: "CPI value in the previous month"
    :return: "MoM inflation: CPI_t / CPI_(t-1) - 1"
    '''
    return cpi_t / cpi_t_minus_1 - 1


# ---------------------------------------------------------------------------
# 85. cpi_inflation_year_over_year
# ---------------------------------------------------------------------------
def cpi_inflation_year_over_year(cpi_t, cpi_t_minus_12):
    '''
    domain: ['Macroeconomics, inflation & price indices']
    subdomain: ['Inflation measurement', 'CPI analysis']
    function: "Computes year-over-year CPI inflation rate."
    y_as_x: []
    :param cpi_t: "CPI value in the current month"
    :param cpi_t_minus_12: "CPI value 12 months prior"
    :return: "YoY inflation: CPI_t / CPI_(t-12) - 1"
    '''
    return cpi_t / cpi_t_minus_12 - 1


# ---------------------------------------------------------------------------
# 86. crack_spread
# ---------------------------------------------------------------------------
def crack_spread(product_futures_value, crude_futures_cost):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Energy spreads', 'Refining economics']
    function: "Computes the crack spread, measuring the refining margin between crude oil input costs and refined product revenues."
    y_as_x: []
    :param product_futures_value: "Value of refined product futures (e.g., gasoline, heating oil)"
    :param crude_futures_cost: "Cost of crude oil futures input"
    :return: "Crack spread: Product Futures Value - Crude Futures Cost"
    '''
    return product_futures_value - crude_futures_cost


# ---------------------------------------------------------------------------
# 87. credibility_premium
# ---------------------------------------------------------------------------
def credibility_premium(Z, experience_mean, manual_mean):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Credibility theory', 'Premium ratemaking']
    function: "Computes the credibility-weighted premium, blending an individual's own experience with the collective manual rate."
    y_as_x: []
    :param Z: "Credibility factor (0 <= Z <= 1), e.g., from Buhlmann formula"
    :param experience_mean: "Mean claim amount from the individual's own experience"
    :param manual_mean: "Mean claim amount from the manual (collective) rate"
    :return: "Credibility premium: Z * Experience Mean + (1 - Z) * Manual Mean"
    '''
    return Z * experience_mean + (1 - Z) * manual_mean


# ---------------------------------------------------------------------------
# 88. credit_conversion_factor_ccf
# ---------------------------------------------------------------------------
def credit_conversion_factor_ccf(ead, outstanding, undrawn):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Credit risk', 'Exposure estimation']
    function: "Computes the Credit Conversion Factor (CCF), measuring the fraction of undrawn commitments expected to be drawn at default."
    y_as_x: []
    :param ead: "Exposure at default"
    :param outstanding: "Currently outstanding (drawn) amount"
    :param undrawn: "Undrawn (committed but not yet drawn) amount"
    :return: "CCF = (EAD - Outstanding) / Undrawn"
    '''
    return (ead - outstanding) / undrawn


# ---------------------------------------------------------------------------
# 89. credit_portfolio_variance_independent_defaults
# ---------------------------------------------------------------------------
def credit_portfolio_variance_independent_defaults(ead, lgd, pd):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Portfolio credit risk', 'Loss distribution']
    function: "Computes the variance of credit portfolio losses assuming independent defaults across obligors."
    y_as_x: []
    :param ead: "Array of exposure at default for each obligor"
    :param lgd: "Array of loss given default for each obligor"
    :param pd: "Array of probability of default for each obligor"
    :return: "Portfolio loss variance: sum(EAD_i^2 * LGD_i^2 * PD_i * (1 - PD_i))"
    '''
    ead = np.asarray(ead, dtype=float)
    lgd = np.asarray(lgd, dtype=float)
    pd = np.asarray(pd, dtype=float)
    return np.sum(ead**2 * lgd**2 * pd * (1 - pd))


# ---------------------------------------------------------------------------
# 90. credit_rwa_under_standardized_approach
# ---------------------------------------------------------------------------
def credit_rwa_under_standardized_approach(ead, risk_weight):
    '''
    domain: ['Bank regulation, Basel & prudential ratios']
    subdomain: ['Capital adequacy', 'Standardized approach']
    function: "Computes credit risk-weighted assets under the Basel standardized approach."
    y_as_x: ['risk_weighted_assets_rwa']
    :param ead: "Exposure at default"
    :param risk_weight: "Supervisory risk weight (e.g., 0.20 for 20%, 1.00 for 100%)"
    :return: "Credit RWA: EAD * risk weight"
    '''
    return ead * risk_weight


# ---------------------------------------------------------------------------
# 91. credit_spread
# ---------------------------------------------------------------------------
def credit_spread(corporate_yield, risk_free_yield):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit analysis', 'Spread analysis']
    function: "Computes the credit spread, the additional yield demanded for bearing credit risk above the risk-free rate."
    y_as_x: ['cds_spread_approximation', 'structural_credit_spread_approximation', 'duration_times_spread_dts']
    :param corporate_yield: "Yield on a corporate bond"
    :param risk_free_yield: "Yield on a risk-free (government) bond of the same maturity"
    :return: "Credit spread: Corporate Yield - Risk-free Yield"
    '''
    return corporate_yield - risk_free_yield


# ---------------------------------------------------------------------------
# 92. credit_var
# ---------------------------------------------------------------------------
def credit_var(loss_distribution, alpha=0.99):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit risk measurement', 'Economic capital']
    function: "Computes Credit VaR as the difference between the loss quantile at confidence level alpha and the expected loss."
    y_as_x: []
    :param loss_distribution: "Array of simulated portfolio losses"
    :param alpha: "Confidence level (e.g., 0.99 for 99%)"
    :return: "Credit VaR: quantile_alpha(loss) - E[loss]"
    '''
    loss_distribution = np.asarray(loss_distribution, dtype=float)
    expected_loss = np.mean(loss_distribution)
    var_quantile = np.quantile(loss_distribution, alpha)
    return var_quantile - expected_loss


# ---------------------------------------------------------------------------
# 93. cross_exchange_rate
# ---------------------------------------------------------------------------
def cross_exchange_rate(S_AB, S_BC):
    '''
    domain: ['FX & international finance']
    subdomain: ['Exchange rate mechanics', 'Cross rates']
    function: "Computes a cross exchange rate from two bilateral rates sharing a common currency."
    y_as_x: ['triangular_arbitrage_condition']
    :param S_AB: "Exchange rate of currency A per unit of currency B"
    :param S_BC: "Exchange rate of currency B per unit of currency C"
    :return: "Cross rate S_{A/C} = S_{A/B} * S_{B/C}"
    '''
    return S_AB * S_BC


# ---------------------------------------------------------------------------
# 94. cross_currency_basis
# ---------------------------------------------------------------------------
def cross_currency_basis(domestic_rate, foreign_rate, spot_rate, forward_rate, tenor):
    '''
    domain: ['FX & international finance']
    subdomain: ['Cross-currency swaps', 'Basis swaps']
    function: "Computes the cross-currency basis spread that equalizes the present value of a cross-currency swap."
    y_as_x: []
    :param domestic_rate: "Domestic currency interest rate"
    :param foreign_rate: "Foreign currency interest rate"
    :param spot_rate: "Current FX spot rate (domestic/foreign)"
    :param forward_rate: "FX forward rate (domestic/foreign)"
    :param tenor: "Swap tenor in years"
    :return: "Cross-currency basis spread (bps deviation from CIP)"
    '''
    # Implied foreign rate from CIP
    implied_foreign = ((forward_rate / spot_rate) ** (1 / tenor)) * (1 + domestic_rate) - 1
    basis = foreign_rate - implied_foreign
    return basis


# ---------------------------------------------------------------------------
# 95. cross_hedge_ratio
# ---------------------------------------------------------------------------
def cross_hedge_ratio(rho, sigma_S, sigma_F):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Hedging', 'Cross-hedging']
    function: "Computes the optimal cross-hedge ratio when the hedging instrument differs from the exposure."
    y_as_x: []
    :param rho: "Correlation between spot and futures price changes"
    :param sigma_S: "Standard deviation of spot price changes"
    :param sigma_F: "Standard deviation of futures price changes"
    :return: "Cross-hedge ratio: h = rho * (sigma_S / sigma_F)"
    '''
    return rho * (sigma_S / sigma_F)


# ---------------------------------------------------------------------------
# 96. cumulative_gap
# ---------------------------------------------------------------------------
def cumulative_gap(gaps):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Interest rate risk', 'Gap analysis']
    function: "Computes the cumulative repricing gap up to time T, summing individual period gaps."
    y_as_x: []
    :param gaps: "Array of period-by-period repricing gaps"
    :return: "Cumulative gap: CumGap_T = sum of Gap_t for all t <= T"
    '''
    return np.cumsum(np.asarray(gaps, dtype=float))


# ---------------------------------------------------------------------------
# 97. cumulative_inflation_factor_from_cpi
# ---------------------------------------------------------------------------
def cumulative_inflation_factor_from_cpi(cpi_t, cpi_0):
    '''
    domain: ['Macroeconomics, inflation & price indices']
    subdomain: ['Inflation measurement', 'Purchasing power']
    function: "Computes the cumulative inflation factor from a base period to the current period using CPI values."
    y_as_x: ['inflation_accretion']
    :param cpi_t: "CPI value at the current time t"
    :param cpi_0: "CPI value at the base period 0"
    :return: "Cumulative inflation factor: CPI_t / CPI_0"
    '''
    return cpi_t / cpi_0


# ---------------------------------------------------------------------------
# 98. cumulative_inflation_factor_from_ppi
# ---------------------------------------------------------------------------
def cumulative_inflation_factor_from_ppi(ppi_t, ppi_0):
    '''
    domain: ['Macroeconomics, inflation & price indices']
    subdomain: ['Inflation measurement', 'Producer prices']
    function: "Computes the cumulative inflation factor from a base period to the current period using PPI values."
    y_as_x: []
    :param ppi_t: "PPI value at the current time t"
    :param ppi_0: "PPI value at the base period 0"
    :return: "Cumulative inflation factor: PPI_t / PPI_0"
    '''
    return ppi_t / ppi_0


# ---------------------------------------------------------------------------
# 99. cumulative_liquidity_gap
# ---------------------------------------------------------------------------
def cumulative_liquidity_gap(inflows, outflows):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Liquidity risk', 'Cash flow management']
    function: "Computes the cumulative liquidity gap over time, summing net cash flows (inflows minus outflows) across periods."
    y_as_x: []
    :param inflows: "Array of cash inflows per period"
    :param outflows: "Array of cash outflows per period"
    :return: "Cumulative liquidity gap: CumLiqGap_T = sum(Inflows_t - Outflows_t) for t = 1..T"
    '''
    inflows = np.asarray(inflows, dtype=float)
    outflows = np.asarray(outflows, dtype=float)
    return np.cumsum(inflows - outflows)


# ---------------------------------------------------------------------------
# 100. cumulative_net_loss
# ---------------------------------------------------------------------------
def cumulative_net_loss(cumulative_net_charge_offs, original_balance):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['ABS performance', 'Credit metrics']
    function: "Computes the cumulative net loss (CNL) for a securitized pool, measuring total net charge-offs as a fraction of the original pool balance."
    y_as_x: []
    :param cumulative_net_charge_offs: "Total cumulative net charge-offs since pool inception"
    :param original_balance: "Original pool balance at securitization"
    :return: "CNL = cumulative net charge-offs / original balance"
    '''
    return cumulative_net_charge_offs / original_balance


# ---------------------------------------------------------------------------
# 101. cumulative_return
# ---------------------------------------------------------------------------
def cumulative_return(returns):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Return calculation', 'Performance measurement']
    function: "Computes the cumulative return from a series of periodic returns."
    y_as_x: ['annualized_return_cagr', 'maximum_drawdown', 'drawdown']
    :param returns: "Pandas Series of periodic returns"
    :return: "Cumulative return: product(1 + r_t) - 1"
    '''
    import empyrical
    return empyrical.cum_returns_final(returns)


# ---------------------------------------------------------------------------
# 102. cure_rate
# ---------------------------------------------------------------------------
def cure_rate(cured_delinquent_accounts, total_delinquent_accounts):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Delinquency analysis', 'Loan performance']
    function: "Computes the cure rate, the proportion of delinquent accounts that return to current (performing) status."
    y_as_x: []
    :param cured_delinquent_accounts: "Number of delinquent accounts that became current"
    :param total_delinquent_accounts: "Total number of delinquent accounts at the start of the period"
    :return: "Cure rate: cured delinquent accounts / total delinquent accounts"
    '''
    return cured_delinquent_accounts / total_delinquent_accounts
