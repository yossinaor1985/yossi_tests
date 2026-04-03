"""
Financial Functions - Batch 4 (Equations 306-407)
"""
import numpy as np
import pandas as pd
from scipy import stats


def expected_drawdown(returns):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Drawdown analysis', 'Risk measurement']
    function: "Computes the expected drawdown as the average of the maximum drawdown experienced over rolling windows. EDD = E[max_{t<=T} drawdown_t]"
    y_as_x: []
    :param returns: "Array of periodic returns"
    :return: "Expected drawdown value"
    '''
    cumulative = np.cumprod(1 + np.array(returns))
    running_max = np.maximum.accumulate(cumulative)
    drawdowns = (running_max - cumulative) / running_max
    return np.mean(np.maximum.accumulate(drawdowns))


def expected_exposure_ee(portfolio_values, t):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Counterparty credit risk', 'Exposure modeling']
    function: "Computes expected exposure at time t as the expected value of the positive mark-to-market. EE_t = E[max(V_t,0)]"
    y_as_x: ['expected_positive_exposure_epe']
    :param portfolio_values: "Array of simulated portfolio values at time t"
    :param t: "Time index for the exposure calculation"
    :return: "Expected exposure at time t"
    '''
    values = np.array(portfolio_values)
    return np.mean(np.maximum(values, 0))


def expected_future_lifetime(life_table, x):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Life contingencies', 'Mortality modeling']
    function: "Computes the expected future lifetime (complete expectation of life) for a person aged x. e_x = E[T_x] = integral from 0 to infinity of t_p_x dt"
    y_as_x: []
    :param life_table: "Dictionary with keys 'ages' and 'lx' representing the life table"
    :param x: "Current age of the individual"
    :return: "Expected future lifetime in years"
    '''
    from actuarialmath import LifeTable
    lt = LifeTable(lx=life_table['lx'], ages=life_table['ages'])
    return lt.e_x(x)


def expected_loss(probability_of_default, loss_given_default, exposure_at_default_ead):
    '''
    domain: ['Credit risk']
    subdomain: ['Credit loss estimation', 'Default modeling']
    function: "Computes expected loss as the product of probability of default, loss given default, and exposure at default. EL = PD x LGD x EAD"
    y_as_x: []
    :param probability_of_default: "Probability of default (PD) as a decimal"
    :param loss_given_default: "Loss given default (LGD) as a decimal fraction"
    :param exposure_at_default_ead: "Exposure at default (EAD) in monetary units"
    :return: "Expected loss in monetary units"
    '''
    return probability_of_default * loss_given_default * exposure_at_default_ead


def expected_positive_exposure_epe(expected_exposure_ee_values, T):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Counterparty credit risk', 'Exposure aggregation']
    function: "Computes expected positive exposure as the time-averaged expected exposure over [0,T]. EPE = (1/T) integral from 0 to T of EE_t dt"
    y_as_x: []
    :param expected_exposure_ee_values: "Array of expected exposure values at each time step"
    :param T: "Total time horizon in years"
    :return: "Expected positive exposure (EPE)"
    '''
    ee = np.array(expected_exposure_ee_values)
    return np.mean(ee)


def expected_principal_collection(scheduled_principal, prepayment, defaults, recoveries):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['ABS cash flow modeling', 'Principal waterfall']
    function: "Computes expected principal collection for a securitization tranche. Principal_t = Scheduled_t + Prepayment_t - Defaults_t + Recoveries_t"
    y_as_x: []
    :param scheduled_principal: "Scheduled principal payment for the period"
    :param prepayment: "Prepayment amount for the period"
    :param defaults: "Default amount for the period"
    :param recoveries: "Recovery amount from defaults"
    :return: "Expected principal collection"
    '''
    return scheduled_principal + prepayment - defaults + recoveries


def expected_shortfall_cvar(returns, alpha=0.05):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Tail risk measurement', 'CVaR optimization']
    function: "Computes Expected Shortfall (CVaR) as the expected loss given that losses exceed the VaR threshold. ES_alpha = -E[R | R <= Quantile_alpha(R)]"
    y_as_x: ['mean_cvar_optimization']
    :param returns: "Array or Series of portfolio returns"
    :param alpha: "Significance level (default 0.05 for 95% CVaR)"
    :return: "Expected shortfall (CVaR) as a positive number"
    '''
    returns = np.array(returns)
    var_threshold = np.percentile(returns, alpha * 100)
    tail_returns = returns[returns <= var_threshold]
    return -np.mean(tail_returns) if len(tail_returns) > 0 else 0.0


def expense_ratio(underwriting_expenses, net_premiums_earned):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Insurance profitability', 'Underwriting analysis']
    function: "Computes the expense ratio as the ratio of underwriting expenses to net premiums earned. Expense Ratio = Underwriting Expenses / Net Premiums Earned"
    y_as_x: ['combined_ratio']
    :param underwriting_expenses: "Total underwriting expenses incurred"
    :param net_premiums_earned: "Net premiums earned during the period"
    :return: "Expense ratio as a decimal"
    '''
    return underwriting_expenses / net_premiums_earned


def explained_variance_ratio(eigenvalues):
    '''
    domain: ['Quantitative forecasting & machine learning in finance']
    subdomain: ['Dimensionality reduction', 'Principal component analysis']
    function: "Computes the explained variance ratio for each principal component. EVR_i = lambda_i / sum_j lambda_j"
    y_as_x: []
    :param eigenvalues: "Array of eigenvalues from PCA decomposition"
    :return: "Array of explained variance ratios for each component"
    '''
    eigenvalues = np.array(eigenvalues)
    return eigenvalues / np.sum(eigenvalues)


def exposure_at_default_ead(outstanding, credit_conversion_factor_ccf, undrawn):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Credit risk parameters', 'Regulatory capital']
    function: "Computes exposure at default combining outstanding balance and a credit conversion factor applied to undrawn commitments. EAD = Outstanding + CCF x Undrawn"
    y_as_x: ['expected_loss', 'expected_credit_loss_ifrs_9_over_cecl']
    :param outstanding: "Current outstanding drawn balance"
    :param credit_conversion_factor_ccf: "Credit conversion factor as a decimal"
    :param undrawn: "Undrawn committed amount"
    :return: "Exposure at default in monetary units"
    '''
    return outstanding + credit_conversion_factor_ccf * undrawn


def exposure_weighted_average_rating_factor(weights, rating_factors):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit portfolio analysis', 'Rating assessment']
    function: "Computes the exposure-weighted average rating factor for a portfolio. WARF = sum_i w_i * RatingFactor_i"
    y_as_x: []
    :param weights: "Array of exposure weights (should sum to 1)"
    :param rating_factors: "Array of numeric rating factors for each exposure"
    :return: "Weighted average rating factor"
    '''
    return np.dot(np.array(weights), np.array(rating_factors))


def factor_model_decomposition(X, n_components):
    '''
    domain: ['Quantitative forecasting & machine learning in finance']
    subdomain: ['Factor analysis', 'Dimensionality reduction']
    function: "Performs factor model decomposition using PCA. X approximately equals F * B' + U, where F is the factor score matrix, B is the loadings matrix, and U is the residual"
    y_as_x: []
    :param X: "2D array of asset returns (observations x assets)"
    :param n_components: "Number of factors to extract"
    :return: "Dictionary with keys 'factors', 'loadings', 'residuals'"
    '''
    from sklearn.decomposition import PCA
    pca = PCA(n_components=n_components)
    factors = pca.fit_transform(X)
    loadings = pca.components_.T
    reconstructed = factors @ pca.components_
    residuals = np.array(X) - reconstructed
    return {'factors': factors, 'loadings': loadings, 'residuals': residuals}


def fama_french_3_factor_model(excess_returns, mkt, smb, hml):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Factor models', 'Asset pricing']
    function: "Estimates the Fama-French 3-factor model via OLS regression. R_i - R_f = alpha + beta_MKT * MKT + beta_SMB * SMB + beta_HML * HML + epsilon"
    y_as_x: []
    :param excess_returns: "Series of asset excess returns (R_i - R_f)"
    :param mkt: "Series of market excess returns (MKT factor)"
    :param smb: "Series of SMB (small minus big) factor returns"
    :param hml: "Series of HML (high minus low) factor returns"
    :return: "Dictionary with 'alpha', 'beta_mkt', 'beta_smb', 'beta_hml', 'r_squared'"
    '''
    from linearmodels.asset_pricing import LinearFactorModel
    import pandas as pd
    factors = pd.DataFrame({'MKT': mkt, 'SMB': smb, 'HML': hml})
    X = np.column_stack([np.ones(len(mkt)), mkt, smb, hml])
    y = np.array(excess_returns)
    betas = np.linalg.lstsq(X, y, rcond=None)[0]
    fitted = X @ betas
    ss_res = np.sum((y - fitted) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r_squared = 1 - ss_res / ss_tot if ss_tot != 0 else 0.0
    return {'alpha': betas[0], 'beta_mkt': betas[1], 'beta_smb': betas[2],
            'beta_hml': betas[3], 'r_squared': r_squared}


def fama_french_5_factor_model(excess_returns, mkt, smb, hml, rmw, cma):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Factor models', 'Asset pricing']
    function: "Estimates the Fama-French 5-factor model. R_i - R_f = alpha + b*MKT + s*SMB + h*HML + r*RMW + c*CMA + epsilon"
    y_as_x: []
    :param excess_returns: "Series of asset excess returns"
    :param mkt: "Series of market excess returns"
    :param smb: "Series of SMB factor returns"
    :param hml: "Series of HML factor returns"
    :param rmw: "Series of RMW (robust minus weak profitability) factor returns"
    :param cma: "Series of CMA (conservative minus aggressive investment) factor returns"
    :return: "Dictionary with 'alpha', 'beta_mkt', 'beta_smb', 'beta_hml', 'beta_rmw', 'beta_cma', 'r_squared'"
    '''
    X = np.column_stack([np.ones(len(mkt)), mkt, smb, hml, rmw, cma])
    y = np.array(excess_returns)
    betas = np.linalg.lstsq(X, y, rcond=None)[0]
    fitted = X @ betas
    ss_res = np.sum((y - fitted) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r_squared = 1 - ss_res / ss_tot if ss_tot != 0 else 0.0
    return {'alpha': betas[0], 'beta_mkt': betas[1], 'beta_smb': betas[2],
            'beta_hml': betas[3], 'beta_rmw': betas[4], 'beta_cma': betas[5],
            'r_squared': r_squared}


def fama_macbeth_cross_sectional_regression(returns_panel, betas_panel):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Cross-sectional regression', 'Risk premia estimation']
    function: "Performs Fama-MacBeth two-step cross-sectional regression. At each time t, regress returns on betas to estimate risk premia lambda_t. R_{i,t} = lambda_{0,t} + lambda_t^T * beta_i + epsilon_{i,t}"
    y_as_x: []
    :param returns_panel: "2D array of returns (T x N) where T is time periods and N is assets"
    :param betas_panel: "2D array of factor betas (N x K) where K is number of factors"
    :return: "Dictionary with 'lambda_mean' (average risk premia), 'lambda_se' (standard errors), 't_stats'"
    '''
    returns_panel = np.array(returns_panel)
    betas_panel = np.array(betas_panel)
    T, N = returns_panel.shape
    X = np.column_stack([np.ones(N), betas_panel])
    lambdas = []
    for t in range(T):
        y = returns_panel[t, :]
        lam = np.linalg.lstsq(X, y, rcond=None)[0]
        lambdas.append(lam)
    lambdas = np.array(lambdas)
    lambda_mean = np.mean(lambdas, axis=0)
    lambda_se = np.std(lambdas, axis=0, ddof=1) / np.sqrt(T)
    t_stats = lambda_mean / lambda_se
    return {'lambda_mean': lambda_mean, 'lambda_se': lambda_se, 't_stats': t_stats}


def fcf_yield(free_cash_flow, market_cap):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Valuation multiples', 'Cash flow analysis']
    function: "Computes free cash flow yield as a valuation metric. FCF Yield = Free Cash Flow / Market Cap (or Enterprise Value)"
    y_as_x: []
    :param free_cash_flow: "Free cash flow in monetary units"
    :param market_cap: "Market capitalization or enterprise value"
    :return: "FCF yield as a decimal"
    '''
    return free_cash_flow / market_cap


def fcfe(net_income, depreciation_amortization, capex, delta_nwc, net_borrowing):
    '''
    domain: ['Corporate finance & capital budgeting']
    subdomain: ['Free cash flow', 'Equity valuation']
    function: "Computes Free Cash Flow to Equity. FCFE = Net Income + D&A - Capex - Delta_NWC + Net Borrowing"
    y_as_x: ['fcfe_dcf_intrinsic_value']
    :param net_income: "Net income after taxes"
    :param depreciation_amortization: "Depreciation and amortization expense"
    :param capex: "Capital expenditures"
    :param delta_nwc: "Change in net working capital"
    :param net_borrowing: "Net new borrowing (debt issued minus debt repaid)"
    :return: "Free cash flow to equity"
    '''
    return net_income + depreciation_amortization - capex - delta_nwc + net_borrowing


def fcfe_dcf_intrinsic_value(fcfe_values, cost_of_equity, terminal_value, T):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Discounted cash flow', 'Equity valuation']
    function: "Computes intrinsic equity value using FCFE DCF model. Equity Value = sum_t FCFE_t/(1+R_e)^t + TV/(1+R_e)^T"
    y_as_x: []
    :param fcfe_values: "Array of projected FCFE for each period"
    :param cost_of_equity: "Cost of equity (R_e) as a decimal"
    :param terminal_value: "Terminal value at the end of projection period"
    :param T: "Number of projection periods"
    :return: "Intrinsic equity value"
    '''
    fcfe_arr = np.array(fcfe_values)
    pv_fcfe = np.sum(fcfe_arr / (1 + cost_of_equity) ** np.arange(1, len(fcfe_arr) + 1))
    pv_tv = terminal_value / (1 + cost_of_equity) ** T
    return pv_fcfe + pv_tv


def fcff(ebit, tax_rate, depreciation_amortization, capex, delta_nwc):
    '''
    domain: ['Corporate finance & capital budgeting']
    subdomain: ['Free cash flow', 'Firm valuation']
    function: "Computes Free Cash Flow to Firm. FCFF = EBIT*(1-T) + D&A - Capex - Delta_NWC"
    y_as_x: ['fcff_dcf_intrinsic_value']
    :param ebit: "Earnings before interest and taxes"
    :param tax_rate: "Corporate tax rate as a decimal"
    :param depreciation_amortization: "Depreciation and amortization expense"
    :param capex: "Capital expenditures"
    :param delta_nwc: "Change in net working capital"
    :return: "Free cash flow to firm"
    '''
    return ebit * (1 - tax_rate) + depreciation_amortization - capex - delta_nwc


def fcff_dcf_intrinsic_value(fcff_values, wacc, terminal_value, T):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Discounted cash flow', 'Enterprise valuation']
    function: "Computes enterprise value using FCFF DCF model. EV = sum_t FCFF_t/(1+WACC)^t + TV/(1+WACC)^T"
    y_as_x: []
    :param fcff_values: "Array of projected FCFF for each period"
    :param wacc: "Weighted average cost of capital as a decimal"
    :param terminal_value: "Terminal value at end of projection period"
    :param T: "Number of projection periods"
    :return: "Enterprise value"
    '''
    fcff_arr = np.array(fcff_values)
    pv_fcff = np.sum(fcff_arr / (1 + wacc) ** np.arange(1, len(fcff_arr) + 1))
    pv_tv = terminal_value / (1 + wacc) ** T
    return pv_fcff + pv_tv


def fill_ratio(executed_quantity, submitted_quantity):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Trade execution', 'Order quality']
    function: "Computes the fill ratio as the proportion of submitted order quantity that was executed. Fill Ratio = Executed Quantity / Submitted Quantity"
    y_as_x: []
    :param executed_quantity: "Quantity of order that was filled"
    :param submitted_quantity: "Total quantity submitted in the order"
    :return: "Fill ratio as a decimal between 0 and 1"
    '''
    return executed_quantity / submitted_quantity


def financial_leverage(pct_delta_eps, pct_delta_ebit):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Leverage analysis', 'Capital structure']
    function: "Computes the degree of financial leverage as the ratio of percentage change in EPS to percentage change in EBIT. DFL = %Delta_EPS / %Delta_EBIT"
    y_as_x: ['combined_leverage']
    :param pct_delta_eps: "Percentage change in earnings per share"
    :param pct_delta_ebit: "Percentage change in EBIT"
    :return: "Degree of financial leverage"
    '''
    return pct_delta_eps / pct_delta_ebit


def fixed_asset_turnover(revenue, average_net_ppe):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Efficiency ratios', 'Asset utilization']
    function: "Computes fixed asset turnover measuring how efficiently a company uses its fixed assets to generate revenue. Fixed Asset Turnover = Revenue / Average Net PP&E"
    y_as_x: []
    :param revenue: "Total revenue for the period"
    :param average_net_ppe: "Average net property, plant, and equipment"
    :return: "Fixed asset turnover ratio"
    '''
    return revenue / average_net_ppe


def fixed_effects_panel_model(y, X, entity_ids):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Panel data', 'Fixed effects estimation']
    function: "Estimates a fixed effects panel model by entity demeaning. y_it = alpha_i + x_it' * beta + u_it"
    y_as_x: []
    :param y: "Dependent variable array (N*T,)"
    :param X: "Independent variables array (N*T, K)"
    :param entity_ids: "Array of entity identifiers for each observation"
    :return: "Dictionary with 'betas', 'fixed_effects', 'residuals'"
    '''
    y = np.array(y, dtype=float)
    X = np.array(X, dtype=float)
    entity_ids = np.array(entity_ids)
    unique_ids = np.unique(entity_ids)
    y_demean = np.copy(y)
    X_demean = np.copy(X)
    entity_means_y = {}
    for eid in unique_ids:
        mask = entity_ids == eid
        entity_means_y[eid] = np.mean(y[mask])
        y_demean[mask] -= np.mean(y[mask])
        X_demean[mask] -= np.mean(X[mask], axis=0)
    betas = np.linalg.lstsq(X_demean, y_demean, rcond=None)[0]
    fixed_effects = {}
    for eid in unique_ids:
        mask = entity_ids == eid
        fixed_effects[eid] = np.mean(y[mask]) - np.mean(X[mask], axis=0) @ betas
    residuals = y_demean - X_demean @ betas
    return {'betas': betas, 'fixed_effects': fixed_effects, 'residuals': residuals}


def fixed_charge_coverage(ebitda, capex, cash_taxes, interest, scheduled_amortization, lease_payments):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Debt service capacity', 'Coverage ratios']
    function: "Computes the fixed-charge coverage ratio. FCCR = (EBITDA - Capex - Cash Taxes) / (Interest + Scheduled Amortization + Lease)"
    y_as_x: []
    :param ebitda: "Earnings before interest, taxes, depreciation, and amortization"
    :param capex: "Capital expenditures"
    :param cash_taxes: "Cash taxes paid"
    :param interest: "Interest payments"
    :param scheduled_amortization: "Scheduled debt amortization payments"
    :param lease_payments: "Lease payments"
    :return: "Fixed-charge coverage ratio"
    '''
    return (ebitda - capex - cash_taxes) / (interest + scheduled_amortization + lease_payments)


def floating_rate_note_coupon(reference_rate, spread):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Floating rate instruments', 'Coupon calculation']
    function: "Computes the coupon rate for a floating-rate note. Coupon_t = Reference Rate_t + Spread"
    y_as_x: []
    :param reference_rate: "Reference rate (e.g., SOFR, EURIBOR) at the reset date"
    :param spread: "Fixed spread over the reference rate in decimal"
    :return: "Floating-rate note coupon rate"
    '''
    return reference_rate + spread


def force_of_mortality(life_table, x):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Mortality modeling', 'Survival analysis']
    function: "Computes the force of mortality (hazard rate) at age x. mu_x = f_x / S_x = -d ln S_x / dx"
    y_as_x: []
    :param life_table: "Dictionary with keys 'ages' and 'lx' representing the life table"
    :param x: "Age at which to compute the force of mortality"
    :return: "Force of mortality at age x"
    '''
    from actuarialmath import LifeTable
    lt = LifeTable(lx=life_table['lx'], ages=life_table['ages'])
    return lt.mu_x(x)


def forward_fx_outright(spot_rate, r_domestic, r_foreign, T):
    '''
    domain: ['FX & international finance']
    subdomain: ['FX forwards', 'Interest rate parity']
    function: "Computes the forward FX outright rate using covered interest rate parity. F = S * e^{(r_d - r_f) * T}"
    y_as_x: ['fx_forward_points', 'fx_forward_points_annualized']
    :param spot_rate: "Current spot FX rate"
    :param r_domestic: "Domestic risk-free interest rate (continuous)"
    :param r_foreign: "Foreign risk-free interest rate (continuous)"
    :param T: "Time to maturity in years"
    :return: "Forward FX rate"
    '''
    return spot_rate * np.exp((r_domestic - r_foreign) * T)


def forward_p_over_e(price, forward_eps):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Valuation multiples', 'Earnings analysis']
    function: "Computes the forward price-to-earnings ratio. Forward P/E = Price / Next-12-month EPS"
    y_as_x: []
    :param price: "Current stock price"
    :param forward_eps: "Estimated earnings per share for the next 12 months"
    :return: "Forward P/E ratio"
    '''
    return price / forward_eps


def forward_price_on_non_dividend_asset(S0, r, T):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Forward pricing', 'No-arbitrage pricing']
    function: "Computes the forward price on a non-dividend-paying asset. F_0 = S_0 * e^{r*T}"
    y_as_x: []
    :param S0: "Current spot price of the asset"
    :param r: "Risk-free interest rate (continuous compounding)"
    :param T: "Time to maturity in years"
    :return: "Forward price"
    '''
    return S0 * np.exp(r * T)


def forward_price_with_carry(S0, r, storage_cost, convenience_yield, T):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Forward pricing', 'Cost of carry']
    function: "Computes the forward price with cost of carry including storage and convenience yield. F_0 = S_0 * e^{(r + u - y) * T}"
    y_as_x: []
    :param S0: "Current spot price"
    :param r: "Risk-free interest rate (continuous compounding)"
    :param storage_cost: "Storage cost rate (u) per annum"
    :param convenience_yield: "Convenience yield (y) per annum"
    :param T: "Time to maturity in years"
    :return: "Forward price with carry"
    '''
    return S0 * np.exp((r + storage_cost - convenience_yield) * T)


def forward_rate(df_t1, df_t2, t1, t2):
    '''
    domain: ['Fixed income & bond math']
    subdomain: ['Term structure', 'Forward rates']
    function: "Computes the simple forward rate between t1 and t2 from discount factors. f_{t1,t2} = (DF(t1)/DF(t2) - 1) / (t2 - t1)"
    y_as_x: []
    :param df_t1: "Discount factor at time t1"
    :param df_t2: "Discount factor at time t2"
    :param t1: "Start time in years"
    :param t2: "End time in years"
    :return: "Simple forward rate between t1 and t2"
    '''
    return (df_t1 / df_t2 - 1) / (t2 - t1)


def forward_rate_from_discount_factors(df_t1, df_t2, t1, t2):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Term structure', 'Forward rates']
    function: "Computes the forward rate from discount factors over a specified year fraction. f(t1,t2) = (DF(t1)/DF(t2) - 1) / year_fraction"
    y_as_x: []
    :param df_t1: "Discount factor at time t1"
    :param df_t2: "Discount factor at time t2"
    :param t1: "Start time in years"
    :param t2: "End time in years"
    :return: "Forward rate between t1 and t2"
    '''
    year_fraction = t2 - t1
    return (df_t1 / df_t2 - 1) / year_fraction


def forward_rate_from_spot_rates(z1, z2, t1, t2):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Term structure', 'Forward rates']
    function: "Computes the forward rate from spot rates. f_{1,2} = [(1+z_2)^t2 / (1+z_1)^t1]^(1/(t2-t1)) - 1"
    y_as_x: []
    :param z1: "Spot rate for maturity t1"
    :param z2: "Spot rate for maturity t2"
    :param t1: "Time to first maturity in years"
    :param t2: "Time to second maturity in years"
    :return: "Forward rate between t1 and t2"
    '''
    return ((1 + z2) ** t2 / (1 + z1) ** t1) ** (1 / (t2 - t1)) - 1


def fra_payoff(notional, fixed_rate, reference_rate, tau):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Interest rate derivatives', 'Forward rate agreements']
    function: "Computes the settlement payoff of a forward rate agreement. Payoff = N * (R_fix - R_ref) * tau / (1 + R_ref * tau)"
    y_as_x: []
    :param notional: "Notional principal amount"
    :param fixed_rate: "Agreed fixed rate of the FRA"
    :param reference_rate: "Actual reference rate at settlement"
    :param tau: "Day count fraction for the FRA period"
    :return: "FRA settlement payoff (positive = receiver gains)"
    '''
    return notional * (fixed_rate - reference_rate) * tau / (1 + reference_rate * tau)


def fra_rate(df_t1, df_t2, tau):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Forward rate agreements', 'Term structure']
    function: "Computes the fair FRA rate from discount factors. FRA = (DF(t1)/DF(t2) - 1) / tau"
    y_as_x: []
    :param df_t1: "Discount factor at the start date of the FRA"
    :param df_t2: "Discount factor at the end date of the FRA"
    :param tau: "Day count fraction for the FRA period"
    :return: "Fair FRA rate"
    '''
    return (df_t1 / df_t2 - 1) / tau


def free_cash_flow(operating_cash_flow, capex):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Cash flow analysis', 'Free cash flow']
    function: "Computes free cash flow as operating cash flow minus capital expenditures. FCF = Operating Cash Flow - Capex"
    y_as_x: ['free_cash_flow_margin', 'fcf_yield']
    :param operating_cash_flow: "Cash flow from operating activities"
    :param capex: "Capital expenditures"
    :return: "Free cash flow"
    '''
    return operating_cash_flow - capex


def free_cash_flow_margin(free_cash_flow, revenue):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Profitability ratios', 'Cash flow analysis']
    function: "Computes free cash flow margin as a percentage of revenue. FCF Margin = FCF / Revenue"
    y_as_x: []
    :param free_cash_flow: "Free cash flow in monetary units"
    :param revenue: "Total revenue for the period"
    :return: "Free cash flow margin as a decimal"
    '''
    return free_cash_flow / revenue


def free_cash_flow_to_equity_fcfe(net_income, depreciation_amortization, capex, delta_nwc, net_borrowing):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Equity cash flow', 'Valuation']
    function: "Computes free cash flow to equity holders. FCFE = Net Income + D&A - Capex - Delta_NWC + Net Borrowing"
    y_as_x: []
    :param net_income: "Net income after taxes"
    :param depreciation_amortization: "Depreciation and amortization expense"
    :param capex: "Capital expenditures"
    :param delta_nwc: "Change in net working capital"
    :param net_borrowing: "Net new debt issuance minus repayment"
    :return: "Free cash flow to equity"
    '''
    return net_income + depreciation_amortization - capex - delta_nwc + net_borrowing


def free_cash_flow_to_firm_fcff(ebit, tax_rate, depreciation_amortization, capex, delta_nwc):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Firm cash flow', 'Valuation']
    function: "Computes free cash flow to the firm available to all capital providers. FCFF = EBIT*(1-T) + D&A - Capex - Delta_NWC"
    y_as_x: []
    :param ebit: "Earnings before interest and taxes"
    :param tax_rate: "Corporate tax rate as a decimal"
    :param depreciation_amortization: "Depreciation and amortization expense"
    :param capex: "Capital expenditures"
    :param delta_nwc: "Change in net working capital"
    :return: "Free cash flow to firm"
    '''
    return ebit * (1 - tax_rate) + depreciation_amortization - capex - delta_nwc


def frn_discount_margin(price, cash_flows, reference_rates, times):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Floating rate instruments', 'Yield analysis']
    function: "Computes the discount margin of a floating-rate note by solving for DM such that Price = sum_t CF_t / (1 + Ref_t + DM)^t"
    y_as_x: []
    :param price: "Current market price of the FRN"
    :param cash_flows: "Array of projected cash flows"
    :param reference_rates: "Array of reference rates for each period"
    :param times: "Array of time to each cash flow in years"
    :return: "Discount margin in decimal"
    '''
    from scipy.optimize import brentq
    cf = np.array(cash_flows)
    ref = np.array(reference_rates)
    t = np.array(times)

    def pv_diff(dm):
        pv = np.sum(cf / (1 + ref + dm) ** t)
        return pv - price

    return brentq(pv_diff, -0.05, 0.20)


def front_end_housing_ratio(housing_expense, gross_income):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Mortgage qualification', 'Affordability ratios']
    function: "Computes the front-end housing ratio measuring housing expense as a proportion of gross income. Housing Expense / Gross Income"
    y_as_x: []
    :param housing_expense: "Monthly housing expense (PITI)"
    :param gross_income: "Gross monthly income"
    :return: "Front-end housing ratio as a decimal"
    '''
    return housing_expense / gross_income


def front_end_ratio_over_housing_expense_ratio(housing_expense, gross_monthly_income):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Mortgage underwriting', 'Affordability ratios']
    function: "Computes the front-end ratio (housing expense ratio) for mortgage qualification. Front-End = Housing Expense / Gross Monthly Income"
    y_as_x: []
    :param housing_expense: "Monthly housing expense including PITI"
    :param gross_monthly_income: "Gross monthly income"
    :return: "Front-end ratio as a decimal"
    '''
    return housing_expense / gross_monthly_income


def fund_carried_interest(distributions, capital_return, hurdle, carry_pct):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Fund economics', 'Carried interest']
    function: "Computes fund carried interest (promote) for GPs. Carry = max(0, Distributions - Capital Return - Hurdle) * Carry%"
    y_as_x: []
    :param distributions: "Total distributions to date"
    :param capital_return: "Total capital returned to LPs"
    :param hurdle: "Hurdle amount (preferred return threshold)"
    :param carry_pct: "Carried interest percentage (typically 0.20)"
    :return: "Carried interest amount"
    '''
    return max(0, distributions - capital_return - hurdle) * carry_pct


def funding_liquidity_spread(unsecured_rate, benchmark_rate):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Funding risk', 'Liquidity premium']
    function: "Computes the funding liquidity spread as the difference between unsecured borrowing rate and a benchmark. Funding Liquidity = unsecured rate - OIS or Treasury"
    y_as_x: []
    :param unsecured_rate: "Unsecured interbank borrowing rate"
    :param benchmark_rate: "OIS or Treasury benchmark rate"
    :return: "Funding liquidity spread"
    '''
    return unsecured_rate - benchmark_rate


def funding_spread(loan_yield, funding_cost):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Net interest margin', 'Spread analysis']
    function: "Computes the funding spread as the difference between loan yield and funding cost. Funding Spread = Loan Yield - Funding Cost"
    y_as_x: []
    :param loan_yield: "Yield on the loan portfolio"
    :param funding_cost: "Cost of funding (borrowing rate)"
    :return: "Funding spread in decimal"
    '''
    return loan_yield - funding_cost


def funds_transfer_pricing_spread(transfer_rate, reference_curve_rate):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Funds transfer pricing', 'Internal pricing']
    function: "Computes the FTP spread as the difference between the internal transfer rate and the reference curve rate. FTP Spread = Transfer Rate - Reference Curve Rate"
    y_as_x: []
    :param transfer_rate: "Internal transfer rate assigned to the product"
    :param reference_curve_rate: "Rate from the reference yield curve"
    :return: "Funds transfer pricing spread"
    '''
    return transfer_rate - reference_curve_rate


def funds_transfer_pricing_spread_v2(customer_rate, internal_transfer_rate):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Funds transfer pricing', 'Business unit profitability']
    function: "Computes the FTP spread from the business unit perspective. FTP Spread = Customer Rate - Internal Transfer Rate"
    y_as_x: []
    :param customer_rate: "Rate charged to or paid by the customer"
    :param internal_transfer_rate: "Internal transfer rate from treasury"
    :return: "Funds transfer pricing spread"
    '''
    return customer_rate - internal_transfer_rate


def future_value(present_value_pv, rate, nper, pmt=0):
    '''
    domain: ['Corporate finance & capital budgeting']
    subdomain: ['Time value of money', 'Compounding']
    function: "Computes the future value of an investment using compound interest. FV = PV * (1+r)^n (plus annuity component if pmt provided)"
    y_as_x: []
    :param present_value_pv: "Present value (initial investment)"
    :param rate: "Interest rate per period"
    :param nper: "Number of compounding periods"
    :param pmt: "Payment per period (default 0)"
    :return: "Future value"
    '''
    import numpy_financial as npf
    return npf.fv(rate, nper, pmt, -present_value_pv)


def fx_cross_rate(rate_a_b, rate_b_c):
    '''
    domain: ['FX & international finance']
    subdomain: ['FX cross rates', 'Currency conversion']
    function: "Computes the cross rate between currencies A and C via currency B. S_{A/C} = S_{A/B} * S_{B/C}"
    y_as_x: []
    :param rate_a_b: "FX rate of currency A per unit of currency B"
    :param rate_b_c: "FX rate of currency B per unit of currency C"
    :return: "Cross rate of currency A per unit of currency C"
    '''
    return rate_a_b * rate_b_c


def fx_forward_points(forward_rate_val, spot_rate):
    '''
    domain: ['FX & international finance']
    subdomain: ['FX forwards', 'Forward points']
    function: "Computes forward points as the difference between forward and spot rates. Points = F - S"
    y_as_x: []
    :param forward_rate_val: "Forward FX rate"
    :param spot_rate: "Spot FX rate"
    :return: "Forward points"
    '''
    return forward_rate_val - spot_rate


def fx_forward_points_annualized(forward_rate_val, spot_rate, T):
    '''
    domain: ['FX & international finance']
    subdomain: ['FX forwards', 'Annualized points']
    function: "Computes annualized forward points as a percentage. Annualized Points = (F/S - 1) / T"
    y_as_x: []
    :param forward_rate_val: "Forward FX rate"
    :param spot_rate: "Spot FX rate"
    :param T: "Time to maturity in years"
    :return: "Annualized forward points as a decimal"
    '''
    return (forward_rate_val / spot_rate - 1) / T


def fx_hedge_ratio(foreign_currency_exposure, hedge_notional):
    '''
    domain: ['FX & international finance']
    subdomain: ['FX hedging', 'Risk management']
    function: "Computes the FX hedge ratio as the proportion of foreign currency exposure covered by hedges. h = Foreign Currency Exposure / Hedge Notional"
    y_as_x: []
    :param foreign_currency_exposure: "Total foreign currency exposure in base currency"
    :param hedge_notional: "Notional amount of FX hedges"
    :return: "FX hedge ratio"
    '''
    return foreign_currency_exposure / hedge_notional


def fx_option_garman_kohlhagen(S, K, r_d, r_f, sigma, T, option_type='call'):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['FX options', 'Garman-Kohlhagen model']
    function: "Prices an FX option using the Garman-Kohlhagen model. C = S*e^{-r_f*T}*N(d1) - K*e^{-r_d*T}*N(d2)"
    y_as_x: []
    :param S: "Current spot FX rate"
    :param K: "Strike price"
    :param r_d: "Domestic risk-free interest rate (continuous)"
    :param r_f: "Foreign risk-free interest rate (continuous)"
    :param sigma: "Volatility of the FX rate"
    :param T: "Time to maturity in years"
    :param option_type: "'call' or 'put' (default 'call')"
    :return: "Option price"
    '''
    d1 = (np.log(S / K) + (r_d - r_f + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == 'call':
        return S * np.exp(-r_f * T) * stats.norm.cdf(d1) - K * np.exp(-r_d * T) * stats.norm.cdf(d2)
    else:
        return K * np.exp(-r_d * T) * stats.norm.cdf(-d2) - S * np.exp(-r_f * T) * stats.norm.cdf(-d1)


def fx_option_garman_kohlhagen_d1(S, K, r_d, r_f, sigma, T):
    '''
    domain: ['FX & international finance']
    subdomain: ['FX options', 'Option Greeks']
    function: "Computes d1 in the Garman-Kohlhagen model. d1 = [ln(S/K) + (r_d - r_f + 0.5*sigma^2)*T] / (sigma*sqrt(T))"
    y_as_x: ['fx_option_garman_kohlhagen']
    :param S: "Current spot FX rate"
    :param K: "Strike price"
    :param r_d: "Domestic risk-free interest rate (continuous)"
    :param r_f: "Foreign risk-free interest rate (continuous)"
    :param sigma: "Volatility of the FX rate"
    :param T: "Time to maturity in years"
    :return: "d1 value"
    '''
    return (np.log(S / K) + (r_d - r_f + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))


def fx_spot_quote_inversion(rate_b_a):
    '''
    domain: ['FX & international finance']
    subdomain: ['FX quoting', 'Currency conversion']
    function: "Inverts a spot FX quote. S_{A/B} = 1 / S_{B/A}"
    y_as_x: []
    :param rate_b_a: "FX spot rate B per unit of A"
    :return: "Inverted FX rate A per unit of B"
    '''
    return 1.0 / rate_b_a


def fx_swap_points(forward_rate_val, spot_rate):
    '''
    domain: ['FX & international finance']
    subdomain: ['FX swaps', 'Swap points']
    function: "Computes FX swap points as the difference between forward and spot rates. Swap Points = F - S"
    y_as_x: []
    :param forward_rate_val: "Forward FX rate"
    :param spot_rate: "Spot FX rate"
    :return: "FX swap points"
    '''
    return forward_rate_val - spot_rate


def fx_transaction_exposure_pandl(foreign_cash_flow, spot_realized, hedge_rate):
    '''
    domain: ['FX & international finance']
    subdomain: ['FX risk management', 'Transaction exposure']
    function: "Computes P&L from FX transaction exposure. P&L = Foreign CF * (Spot_realized - Hedge Rate)"
    y_as_x: []
    :param foreign_cash_flow: "Foreign currency cash flow amount"
    :param spot_realized: "Realized spot FX rate at settlement"
    :param hedge_rate: "Hedged or budgeted FX rate"
    :return: "Transaction exposure P&L in domestic currency"
    '''
    return foreign_cash_flow * (spot_realized - hedge_rate)


def fx_translation_effect(local_currency_amount, fx_rate):
    '''
    domain: ['FX & international finance']
    subdomain: ['FX translation', 'Accounting exposure']
    function: "Translates a local currency amount to reporting currency. Translated Value = Local Currency Amount * FX Rate"
    y_as_x: []
    :param local_currency_amount: "Amount in local (foreign) currency"
    :param fx_rate: "FX rate (reporting currency per unit of local currency)"
    :return: "Translated value in reporting currency"
    '''
    return local_currency_amount * fx_rate


def gamma(S, K, r, q, sigma, T):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Option Greeks', 'Gamma risk']
    function: "Computes option gamma, the rate of change of delta with respect to underlying price. Gamma = e^{-qT} * n(d1) / (S * sigma * sqrt(T))"
    y_as_x: ['speed', 'color']
    :param S: "Current price of the underlying asset"
    :param K: "Strike price"
    :param r: "Risk-free interest rate (continuous compounding)"
    :param q: "Continuous dividend yield"
    :param sigma: "Volatility of the underlying"
    :param T: "Time to maturity in years"
    :return: "Option gamma value"
    '''
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    return np.exp(-q * T) * stats.norm.pdf(d1) / (S * sigma * np.sqrt(T))


def garch_11(returns, omega=None, alpha=None, beta=None):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Volatility modeling', 'GARCH']
    function: "Fits a GARCH(1,1) model to return series. sigma_t^2 = omega + alpha * epsilon_{t-1}^2 + beta * sigma_{t-1}^2"
    y_as_x: []
    :param returns: "Array or Series of asset returns"
    :param omega: "Long-run variance weight (if None, estimated from data)"
    :param alpha: "ARCH coefficient (if None, estimated from data)"
    :param beta: "GARCH coefficient (if None, estimated from data)"
    :return: "Dictionary with 'params' (omega, alpha, beta), 'conditional_volatility', 'residuals'"
    '''
    from arch import arch_model
    returns = np.array(returns) * 100  # arch expects percentage returns
    model = arch_model(returns, vol='Garch', p=1, q=1, mean='Constant')
    result = model.fit(disp='off')
    return {
        'params': {'omega': result.params['omega'],
                   'alpha': result.params['alpha[1]'],
                   'beta': result.params['beta[1]']},
        'conditional_volatility': result.conditional_volatility / 100,
        'residuals': result.resid / 100
    }


def garch_11_v2(returns):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Volatility modeling', 'GARCH']
    function: "Fits a GARCH(1,1) model variant and returns forecast variance. sigma_t^2 = omega + alpha*epsilon_{t-1}^2 + beta*sigma_{t-1}^2"
    y_as_x: []
    :param returns: "Array or Series of asset returns"
    :return: "Dictionary with 'params', 'conditional_volatility', 'forecast_variance'"
    '''
    from arch import arch_model
    returns = np.array(returns) * 100
    model = arch_model(returns, vol='Garch', p=1, q=1, mean='Zero')
    result = model.fit(disp='off')
    forecast = result.forecast(horizon=1)
    return {
        'params': {'omega': result.params['omega'],
                   'alpha': result.params['alpha[1]'],
                   'beta': result.params['beta[1]']},
        'conditional_volatility': result.conditional_volatility / 100,
        'forecast_variance': forecast.variance.values[-1, 0] / 10000
    }


def garman_klass_volatility(high, low, close, open_price):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Volatility estimation', 'Range-based estimators']
    function: "Computes Garman-Klass volatility estimator using OHLC data. sigma_GK^2 = 0.5*[ln(H/L)]^2 - (2*ln2-1)*[ln(C/O)]^2"
    y_as_x: []
    :param high: "Array of high prices"
    :param low: "Array of low prices"
    :param close: "Array of closing prices"
    :param open_price: "Array of opening prices"
    :return: "Garman-Klass volatility estimate (annualized if daily data)"
    '''
    high = np.array(high)
    low = np.array(low)
    close = np.array(close)
    open_price = np.array(open_price)
    n = len(high)
    term1 = 0.5 * np.log(high / low) ** 2
    term2 = (2 * np.log(2) - 1) * np.log(close / open_price) ** 2
    daily_var = np.mean(term1 - term2)
    return np.sqrt(daily_var * 252)


def gaussian_mixture_likelihood(X, n_components=2):
    '''
    domain: ['Quantitative forecasting & machine learning in finance']
    subdomain: ['Mixture models', 'Density estimation']
    function: "Fits a Gaussian mixture model and returns log-likelihood. p(x) = sum_k pi_k * N(x|mu_k, Sigma_k)"
    y_as_x: []
    :param X: "Array of observations (n_samples, n_features) or (n_samples,)"
    :param n_components: "Number of mixture components (default 2)"
    :return: "Dictionary with 'means', 'covariances', 'weights', 'log_likelihood'"
    '''
    from sklearn.mixture import GaussianMixture
    X = np.array(X)
    if X.ndim == 1:
        X = X.reshape(-1, 1)
    gmm = GaussianMixture(n_components=n_components, random_state=42)
    gmm.fit(X)
    return {
        'means': gmm.means_,
        'covariances': gmm.covariances_,
        'weights': gmm.weights_,
        'log_likelihood': gmm.score(X) * len(X)
    }


def gjr_garch(returns):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Asymmetric volatility', 'GJR-GARCH']
    function: "Fits a GJR-GARCH model capturing asymmetric volatility response. sigma_t^2 = omega + alpha*eps_{t-1}^2 + gamma*I_{eps<0}*eps_{t-1}^2 + beta*sigma_{t-1}^2"
    y_as_x: []
    :param returns: "Array or Series of asset returns"
    :return: "Dictionary with 'params' (omega, alpha, gamma, beta), 'conditional_volatility'"
    '''
    from arch import arch_model
    returns = np.array(returns) * 100
    model = arch_model(returns, vol='Garch', p=1, o=1, q=1, mean='Constant')
    result = model.fit(disp='off')
    return {
        'params': {'omega': result.params['omega'],
                   'alpha': result.params['alpha[1]'],
                   'gamma': result.params['gamma[1]'],
                   'beta': result.params['beta[1]']},
        'conditional_volatility': result.conditional_volatility / 100
    }


def global_minimum_variance_portfolio(expected_returns, cov_matrix):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio optimization', 'Minimum variance']
    function: "Finds the global minimum variance portfolio weights. min_w w^T * Sigma * w subject to 1^T * w = 1"
    y_as_x: []
    :param expected_returns: "Series or dict of expected returns keyed by asset name"
    :param cov_matrix: "Covariance matrix as DataFrame or 2D array"
    :return: "Dictionary of optimal weights by asset"
    '''
    from pypfopt import EfficientFrontier
    ef = EfficientFrontier(expected_returns, cov_matrix)
    ef.min_volatility()
    return dict(ef.clean_weights())


def global_minimum_variance_weights(cov_matrix):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio optimization', 'Minimum variance']
    function: "Computes global minimum variance portfolio weights analytically. w* = Sigma^{-1} * 1 / (1' * Sigma^{-1} * 1)"
    y_as_x: []
    :param cov_matrix: "Covariance matrix (N x N array)"
    :return: "Array of minimum variance portfolio weights"
    '''
    cov = np.array(cov_matrix)
    cov_inv = np.linalg.inv(cov)
    ones = np.ones(cov.shape[0])
    weights = cov_inv @ ones / (ones @ cov_inv @ ones)
    return weights


def gmm_moment_condition(y, X, Z):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['GMM estimation', 'Instrumental variables']
    function: "Estimates parameters using GMM with moment conditions. E[g(z_t, theta)] = 0; theta_hat = argmin gbar' * W * gbar"
    y_as_x: []
    :param y: "Dependent variable array"
    :param X: "Endogenous variable array (N, K)"
    :param Z: "Instrument variable array (N, L) where L >= K"
    :return: "Dictionary with 'theta', 'j_stat', 'standard_errors'"
    '''
    y = np.array(y, dtype=float)
    X = np.array(X, dtype=float)
    Z = np.array(Z, dtype=float)
    if X.ndim == 1:
        X = X.reshape(-1, 1)
    if Z.ndim == 1:
        Z = Z.reshape(-1, 1)
    # Two-step GMM
    # First stage: identity weight matrix
    ZtZ_inv = np.linalg.inv(Z.T @ Z)
    P_z = Z @ ZtZ_inv @ Z.T
    theta_iv = np.linalg.lstsq(P_z @ X, P_z @ y, rcond=None)[0]
    resid = y - X @ theta_iv
    # Optimal weight matrix
    S = (Z.T * resid) @ (Z * resid[:, None]) / len(y)
    S_inv = np.linalg.inv(S)
    theta = np.linalg.lstsq(X.T @ Z @ S_inv @ Z.T @ X, X.T @ Z @ S_inv @ Z.T @ y, rcond=None)[0]
    resid2 = y - X @ theta
    g_bar = Z.T @ resid2 / len(y)
    j_stat = len(y) * g_bar @ S_inv @ g_bar
    bread = X.T @ Z @ S_inv @ Z.T @ X / len(y)
    se = np.sqrt(np.diag(np.linalg.inv(bread)) / len(y))
    return {'theta': theta, 'j_stat': j_stat, 'standard_errors': se}


def gordon_growth_ddm(D1, r, g):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Dividend discount model', 'Equity valuation']
    function: "Computes stock price using the Gordon growth dividend discount model. P_0 = D_1 / (r - g)"
    y_as_x: []
    :param D1: "Expected dividend next period"
    :param r: "Required rate of return"
    :param g: "Constant dividend growth rate"
    :return: "Intrinsic stock price"
    '''
    return D1 / (r - g)


def gordon_growth_model(D1, r, g):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Dividend discount model', 'Equity valuation']
    function: "Computes the present value of a perpetually growing dividend stream. P_0 = D_1 / (r - g)"
    y_as_x: []
    :param D1: "Expected dividend at time 1"
    :param r: "Required rate of return (discount rate)"
    :param g: "Constant dividend growth rate (g < r)"
    :return: "Present value (stock price)"
    '''
    return D1 / (r - g)


def gordon_terminal_value(fcf_next, wacc, g):
    '''
    domain: ['Corporate finance & capital budgeting']
    subdomain: ['Terminal value', 'DCF valuation']
    function: "Computes the terminal value using the Gordon growth perpetuity formula. TV = FCF_(t+1) / (WACC - g)"
    y_as_x: ['fcff_dcf_intrinsic_value', 'fcfe_dcf_intrinsic_value']
    :param fcf_next: "Free cash flow in the first year beyond the projection period"
    :param wacc: "Weighted average cost of capital"
    :param g: "Long-term perpetual growth rate"
    :return: "Terminal value"
    '''
    return fcf_next / (wacc - g)


def gradient_boosting(X_train, y_train, X_test, n_estimators=100, learning_rate=0.1, max_depth=3):
    '''
    domain: ['Quantitative forecasting & machine learning in finance']
    subdomain: ['Ensemble methods', 'Gradient boosting']
    function: "Fits a gradient boosting regression model. F_m(x) = F_{m-1}(x) + nu * h_m(x)"
    y_as_x: []
    :param X_train: "Training feature matrix"
    :param y_train: "Training target array"
    :param X_test: "Test feature matrix for prediction"
    :param n_estimators: "Number of boosting stages (default 100)"
    :param learning_rate: "Learning rate / shrinkage (default 0.1)"
    :param max_depth: "Maximum depth of individual trees (default 3)"
    :return: "Dictionary with 'predictions', 'feature_importances', 'train_score'"
    '''
    from sklearn.ensemble import GradientBoostingRegressor
    model = GradientBoostingRegressor(
        n_estimators=n_estimators, learning_rate=learning_rate,
        max_depth=max_depth, random_state=42)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    return {
        'predictions': predictions,
        'feature_importances': model.feature_importances_,
        'train_score': model.score(X_train, y_train)
    }


def granger_causality(y, x, max_lag=4):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Causality testing', 'Time series analysis']
    function: "Performs Granger causality test to determine if lagged values of X improve prediction of Y"
    y_as_x: []
    :param y: "Dependent variable time series"
    :param x: "Independent variable time series (potential cause)"
    :param max_lag: "Maximum number of lags to test (default 4)"
    :return: "Dictionary with 'f_statistic', 'p_value', 'optimal_lag' for each tested lag"
    '''
    from statsmodels.tsa.stattools import grangercausalitytests
    data = np.column_stack([y, x])
    results = grangercausalitytests(data, maxlag=max_lag, verbose=False)
    output = {}
    for lag, res in results.items():
        test_result = res[0]['ssr_ftest']
        output[lag] = {'f_statistic': test_result[0], 'p_value': test_result[1]}
    return output


def gross_irr(cash_flows):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Fund performance', 'IRR calculation']
    function: "Computes gross IRR for a PE fund from equity cash flows. 0 = -Equity_0 + sum_t Distribution_t/(1+IRR)^t + Terminal_Equity/(1+IRR)^T"
    y_as_x: ['net_irr_to_lp']
    :param cash_flows: "Array of cash flows (negative for investments, positive for distributions)"
    :return: "Gross IRR as a decimal"
    '''
    import numpy_financial as npf
    return npf.irr(cash_flows)


def gross_margin(gross_profit, revenue):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Profitability ratios', 'Margin analysis']
    function: "Computes gross margin as the ratio of gross profit to revenue. Gross Margin = Gross Profit / Revenue"
    y_as_x: []
    :param gross_profit: "Gross profit (Revenue - COGS)"
    :param revenue: "Total revenue"
    :return: "Gross margin as a decimal"
    '''
    return gross_profit / revenue


def gross_premium_principle(pv_benefits, pv_expenses, pv_premium_annuity):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Premium calculation', 'Life insurance pricing']
    function: "Computes gross premium using the equivalence principle. Gross Premium = (PV Benefits + PV Expenses) / PV Premium Annuity"
    y_as_x: []
    :param pv_benefits: "Present value of future benefit payments"
    :param pv_expenses: "Present value of future expenses"
    :param pv_premium_annuity: "Present value of a premium annuity factor"
    :return: "Gross premium amount per period"
    '''
    return (pv_benefits + pv_expenses) / pv_premium_annuity


def gross_profit(revenue, cogs):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Income statement', 'Profitability']
    function: "Computes gross profit as revenue less cost of goods sold. Gross Profit = Revenue - COGS"
    y_as_x: ['gross_margin']
    :param revenue: "Total revenue"
    :param cogs: "Cost of goods sold"
    :return: "Gross profit"
    '''
    return revenue - cogs


def gross_rent_multiplier(property_price, gross_annual_rent):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Property valuation', 'Rental analysis']
    function: "Computes the gross rent multiplier for property valuation. GRM = Property Price / Gross Annual Rent"
    y_as_x: []
    :param property_price: "Purchase price of the property"
    :param gross_annual_rent: "Total annual gross rental income"
    :return: "Gross rent multiplier"
    '''
    return property_price / gross_annual_rent


def growing_annuity_value(pmt1, r, g, n):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Time value of money', 'Growing annuity']
    function: "Computes the present value of a growing annuity. PV = PMT_1 * [1 - ((1+g)/(1+r))^n] / (r - g)"
    y_as_x: []
    :param pmt1: "First payment at time 1"
    :param r: "Discount rate per period"
    :param g: "Growth rate per period"
    :param n: "Number of periods"
    :return: "Present value of the growing annuity"
    '''
    if abs(r - g) < 1e-10:
        return pmt1 * n / (1 + r)
    return pmt1 * (1 - ((1 + g) / (1 + r)) ** n) / (r - g)


def growing_perpetuity_value(cf1, r, g):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Time value of money', 'Growing perpetuity']
    function: "Computes the present value of a growing perpetuity. PV = CF_1 / (r - g)"
    y_as_x: []
    :param cf1: "Cash flow at time 1"
    :param r: "Discount rate (must be greater than g)"
    :param g: "Constant growth rate"
    :return: "Present value of the growing perpetuity"
    '''
    return cf1 / (r - g)


def gsib_surcharge(base_capital, surcharge_rate):
    '''
    domain: ['Bank regulation, Basel & prudential ratios']
    subdomain: ['Capital requirements', 'GSIB regulation']
    function: "Computes the total capital requirement for a G-SIB including the surcharge. GSIB Capital Requirement = base capital + surcharge"
    y_as_x: []
    :param base_capital: "Base minimum capital requirement"
    :param surcharge_rate: "G-SIB surcharge rate as a decimal"
    :return: "Total G-SIB capital requirement"
    '''
    return base_capital * (1 + surcharge_rate)


def haircut_adjusted_liquidation_value(market_value, haircut):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Collateral valuation', 'Liquidation risk']
    function: "Computes the haircut-adjusted liquidation value of an asset. LV = Market Value * (1 - Haircut)"
    y_as_x: []
    :param market_value: "Current market value of the asset"
    :param haircut: "Haircut percentage as a decimal"
    :return: "Liquidation value after haircut"
    '''
    return market_value * (1 - haircut)


def hasbrouck_lambda(returns, signed_volume):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Market microstructure', 'Price impact estimation']
    function: "Estimates Hasbrouck's lambda (price impact coefficient) via regression. r_t = lambda * sqrt(VolSigned_t) + epsilon_t"
    y_as_x: []
    :param returns: "Array of asset returns"
    :param signed_volume: "Array of signed trading volume (positive for buys, negative for sells)"
    :return: "Dictionary with 'lambda_coeff', 'r_squared', 'p_value'"
    '''
    import statsmodels.api as sm
    returns = np.array(returns)
    signed_volume = np.array(signed_volume)
    sqrt_signed_vol = np.sign(signed_volume) * np.sqrt(np.abs(signed_volume))
    X = sm.add_constant(sqrt_signed_vol)
    model = sm.OLS(returns, X).fit()
    return {
        'lambda_coeff': model.params[1],
        'r_squared': model.rsquared,
        'p_value': model.pvalues[1]
    }


def hazard_rate_survival(hazard_rate, t):
    '''
    domain: ['Credit risk']
    subdomain: ['Default modeling', 'Survival analysis']
    function: "Computes survival probability from a constant hazard rate. S(t) = e^{-lambda * t}"
    y_as_x: ['probability_of_default_from_hazard_rate']
    :param hazard_rate: "Constant hazard rate (lambda)"
    :param t: "Time horizon in years"
    :return: "Survival probability at time t"
    '''
    return np.exp(-hazard_rate * t)


def hedge_ratio_naive(exposure, contract_size):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Hedge ratio', 'Futures hedging']
    function: "Computes the naive hedge ratio as the number of contracts needed. h = Exposure / Contract Size"
    y_as_x: []
    :param exposure: "Total exposure to be hedged in monetary or physical units"
    :param contract_size: "Size of one futures contract"
    :return: "Number of contracts (may need rounding)"
    '''
    return exposure / contract_size


def hedged_commodity_revenue(spot_revenue, futures_pandl):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Commodity hedging', 'Revenue management']
    function: "Computes total hedged revenue combining spot and futures positions. Hedged Revenue = Spot Revenue + Futures P&L"
    y_as_x: []
    :param spot_revenue: "Revenue from spot market sales"
    :param futures_pandl: "Profit or loss from futures hedging position"
    :return: "Total hedged commodity revenue"
    '''
    return spot_revenue + futures_pandl


def henriksson_merton_timing(rp_rf, rm_rf):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Market timing', 'Performance attribution']
    function: "Estimates Henriksson-Merton market timing model. R_p - R_f = alpha + beta*(R_m - R_f) + gamma*max(R_m - R_f, 0) + epsilon"
    y_as_x: []
    :param rp_rf: "Array of portfolio excess returns (R_p - R_f)"
    :param rm_rf: "Array of market excess returns (R_m - R_f)"
    :return: "Dictionary with 'alpha', 'beta', 'gamma' (timing coefficient), 'r_squared'"
    '''
    import statsmodels.api as sm
    rp_rf = np.array(rp_rf)
    rm_rf = np.array(rm_rf)
    timing_var = np.maximum(rm_rf, 0)
    X = sm.add_constant(np.column_stack([rm_rf, timing_var]))
    model = sm.OLS(rp_rf, X).fit()
    return {
        'alpha': model.params[0],
        'beta': model.params[1],
        'gamma': model.params[2],
        'r_squared': model.rsquared
    }


def herfindahl_concentration_index(weights):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio concentration', 'Diversification measurement']
    function: "Computes the Herfindahl-Hirschman Index measuring portfolio concentration. HHI = sum_i w_i^2"
    y_as_x: []
    :param weights: "Array of portfolio weights"
    :return: "HHI value (ranges from 1/N for equal weight to 1 for single asset)"
    '''
    w = np.array(weights)
    return np.sum(w ** 2)


def heston_asset_process(S0, r, q, v0, kappa, theta, xi, rho, T, n_steps, n_paths):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Stochastic volatility', 'Heston model']
    function: "Simulates asset price paths under the Heston stochastic volatility model. dS_t = (r-q)*S_t*dt + sqrt(v_t)*S_t*dW_t^S"
    y_as_x: []
    :param S0: "Initial asset price"
    :param r: "Risk-free interest rate"
    :param q: "Continuous dividend yield"
    :param v0: "Initial variance"
    :param kappa: "Mean reversion speed of variance"
    :param theta: "Long-run variance level"
    :param xi: "Volatility of variance (vol of vol)"
    :param rho: "Correlation between asset and variance Brownian motions"
    :param T: "Time horizon in years"
    :param n_steps: "Number of time steps"
    :param n_paths: "Number of simulation paths"
    :return: "Dictionary with 'asset_paths' (n_paths x n_steps+1), 'variance_paths'"
    '''
    dt = T / n_steps
    S = np.zeros((n_paths, n_steps + 1))
    v = np.zeros((n_paths, n_steps + 1))
    S[:, 0] = S0
    v[:, 0] = v0
    for t in range(n_steps):
        z1 = np.random.standard_normal(n_paths)
        z2 = rho * z1 + np.sqrt(1 - rho ** 2) * np.random.standard_normal(n_paths)
        v_pos = np.maximum(v[:, t], 0)
        v[:, t + 1] = v[:, t] + kappa * (theta - v_pos) * dt + xi * np.sqrt(v_pos * dt) * z2
        v[:, t + 1] = np.maximum(v[:, t + 1], 0)
        S[:, t + 1] = S[:, t] * np.exp((r - q - 0.5 * v_pos) * dt + np.sqrt(v_pos * dt) * z1)
    return {'asset_paths': S, 'variance_paths': v}


def heston_variance_process(v0, kappa, theta, xi, T, n_steps, n_paths):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Stochastic volatility', 'Variance process']
    function: "Simulates the Heston variance process. dv_t = kappa*(theta - v_t)*dt + xi*sqrt(v_t)*dW_t^v"
    y_as_x: ['heston_asset_process']
    :param v0: "Initial variance"
    :param kappa: "Mean reversion speed"
    :param theta: "Long-run variance level"
    :param xi: "Volatility of variance"
    :param T: "Time horizon in years"
    :param n_steps: "Number of time steps"
    :param n_paths: "Number of simulation paths"
    :return: "Array of variance paths (n_paths x n_steps+1)"
    '''
    dt = T / n_steps
    v = np.zeros((n_paths, n_steps + 1))
    v[:, 0] = v0
    for t in range(n_steps):
        v_pos = np.maximum(v[:, t], 0)
        dW = np.random.standard_normal(n_paths) * np.sqrt(dt)
        v[:, t + 1] = v[:, t] + kappa * (theta - v_pos) * dt + xi * np.sqrt(v_pos) * dW
        v[:, t + 1] = np.maximum(v[:, t + 1], 0)
    return v


def historical_var(returns, alpha=0.05):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Value at Risk', 'Historical simulation']
    function: "Computes historical Value at Risk from the empirical return distribution. VaR_alpha = -quantile_alpha(R)"
    y_as_x: ['liquidity_adjusted_var']
    :param returns: "Array or Series of historical returns"
    :param alpha: "Significance level (default 0.05 for 95% VaR)"
    :return: "Historical VaR as a positive number"
    '''
    returns = np.array(returns)
    return -np.percentile(returns, alpha * 100)


def hit_ratio(returns):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Strategy performance', 'Win rate']
    function: "Computes the hit ratio as the proportion of profitable periods. Hit Ratio = profitable periods / total periods"
    y_as_x: []
    :param returns: "Array of periodic returns"
    :return: "Hit ratio as a decimal between 0 and 1"
    '''
    returns = np.array(returns)
    return np.sum(returns > 0) / len(returns)


def hjm_drift_restriction(sigma_func, t, T):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['HJM framework', 'No-arbitrage drift']
    function: "Computes the HJM drift restriction ensuring no-arbitrage. alpha(t,T) = sigma(t,T) * integral_t^T sigma(t,u) du"
    y_as_x: ['hjm_forward_rate_dynamics']
    :param sigma_func: "Volatility function sigma(t, T) that takes two arguments"
    :param t: "Current time"
    :param T: "Forward rate maturity"
    :return: "No-arbitrage drift alpha(t,T)"
    '''
    from scipy.integrate import quad
    sigma_tT = sigma_func(t, T)
    integral, _ = quad(lambda u: sigma_func(t, u), t, T)
    return sigma_tT * integral


def hjm_forward_rate_dynamics(f0, sigma_func, t, T, dt, dW):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['HJM framework', 'Forward rate dynamics']
    function: "Updates forward rate using HJM dynamics. df(t,T) = alpha(t,T)*dt + sigma(t,T)*dW_t"
    y_as_x: []
    :param f0: "Current forward rate f(t,T)"
    :param sigma_func: "Volatility function sigma(t,T)"
    :param t: "Current time"
    :param T: "Forward rate maturity"
    :param dt: "Time step"
    :param dW: "Brownian motion increment"
    :return: "Updated forward rate f(t+dt, T)"
    '''
    from scipy.integrate import quad
    sigma_tT = sigma_func(t, T)
    integral, _ = quad(lambda u: sigma_func(t, u), t, T)
    alpha_tT = sigma_tT * integral
    return f0 + alpha_tT * dt + sigma_tT * dW


def holding_period_return_hpr(P1, P0, D1=0):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Return measurement', 'Holding period return']
    function: "Computes holding period return including dividends. HPR = (P_1 - P_0 + D_1) / P_0"
    y_as_x: ['time_weighted_return_twrr']
    :param P1: "Ending price"
    :param P0: "Beginning price"
    :param D1: "Dividends or distributions received (default 0)"
    :return: "Holding period return as a decimal"
    '''
    return (P1 - P0 + D1) / P0


def holt_trend_method(series, alpha=0.3, beta=0.1, forecast_periods=5):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Exponential smoothing', 'Trend forecasting']
    function: "Applies Holt's linear trend method (double exponential smoothing). l_t = alpha*y_t + (1-alpha)*(l_{t-1} + b_{t-1}); b_t = beta*(l_t - l_{t-1}) + (1-beta)*b_{t-1}"
    y_as_x: []
    :param series: "Time series data as array or pandas Series"
    :param alpha: "Level smoothing parameter (default 0.3)"
    :param beta: "Trend smoothing parameter (default 0.1)"
    :param forecast_periods: "Number of periods to forecast (default 5)"
    :return: "Dictionary with 'fitted_values', 'forecast', 'level', 'trend'"
    '''
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    series = pd.Series(series).reset_index(drop=True)
    model = ExponentialSmoothing(series, trend='add', seasonal=None)
    result = model.fit(smoothing_level=alpha, smoothing_trend=beta, optimized=False)
    forecast = result.forecast(forecast_periods)
    return {
        'fitted_values': result.fittedvalues.values,
        'forecast': forecast.values,
        'level': result.level.values if hasattr(result, 'level') else None,
        'trend': result.trend.values if hasattr(result, 'trend') else None
    }


def holt_winters_seasonality(series, seasonal_periods, trend='add', seasonal='add', forecast_periods=5):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Exponential smoothing', 'Seasonal forecasting']
    function: "Applies Holt-Winters exponential smoothing with seasonality. Seasonal additive or multiplicative update with alpha, beta, gamma parameters"
    y_as_x: []
    :param series: "Time series data as array or pandas Series"
    :param seasonal_periods: "Number of periods in a seasonal cycle"
    :param trend: "'add' for additive or 'mul' for multiplicative trend (default 'add')"
    :param seasonal: "'add' for additive or 'mul' for multiplicative seasonality (default 'add')"
    :param forecast_periods: "Number of periods to forecast (default 5)"
    :return: "Dictionary with 'fitted_values', 'forecast', 'params'"
    '''
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    series = pd.Series(series).reset_index(drop=True)
    model = ExponentialSmoothing(series, trend=trend, seasonal=seasonal,
                                  seasonal_periods=seasonal_periods)
    result = model.fit()
    forecast = result.forecast(forecast_periods)
    return {
        'fitted_values': result.fittedvalues.values,
        'forecast': forecast.values,
        'params': {
            'alpha': result.params.get('smoothing_level', None),
            'beta': result.params.get('smoothing_trend', None),
            'gamma': result.params.get('smoothing_seasonal', None)
        }
    }


def hull_white_1f_process(r0, a, sigma, theta_func, T, n_steps, n_paths):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Short rate models', 'Hull-White model']
    function: "Simulates short rate paths under the Hull-White 1-factor model. dr_t = [theta(t) - a*r_t]*dt + sigma*dW_t"
    y_as_x: ['hull_white_bond_option_jamshidian']
    :param r0: "Initial short rate"
    :param a: "Mean reversion speed"
    :param sigma: "Volatility of the short rate"
    :param theta_func: "Function theta(t) calibrated to the initial term structure"
    :param T: "Time horizon in years"
    :param n_steps: "Number of time steps"
    :param n_paths: "Number of simulation paths"
    :return: "Array of short rate paths (n_paths x n_steps+1)"
    '''
    dt = T / n_steps
    rates = np.zeros((n_paths, n_steps + 1))
    rates[:, 0] = r0
    for t_idx in range(n_steps):
        t = t_idx * dt
        theta_t = theta_func(t)
        dW = np.random.standard_normal(n_paths) * np.sqrt(dt)
        rates[:, t_idx + 1] = rates[:, t_idx] + (theta_t - a * rates[:, t_idx]) * dt + sigma * dW
    return rates


def hull_white_bond_option_jamshidian(face_value, strike, r0, a, sigma, T_option, T_bond, coupon_rate=0, frequency=2):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Interest rate derivatives', 'Bond options']
    function: "Prices a bond option under Hull-White using Jamshidian decomposition. Decomposes bond option into a portfolio of options on individual cash flows"
    y_as_x: []
    :param face_value: "Face value of the underlying bond"
    :param strike: "Strike price of the bond option"
    :param r0: "Current short rate"
    :param a: "Mean reversion speed"
    :param sigma: "Short rate volatility"
    :param T_option: "Option maturity in years"
    :param T_bond: "Bond maturity in years"
    :param coupon_rate: "Annual coupon rate as a decimal (default 0)"
    :param frequency: "Coupon frequency per year (default 2)"
    :return: "Dictionary with 'call_price', 'put_price'"
    '''
    def B(t1, t2):
        return (1 - np.exp(-a * (t2 - t1))) / a

    def P(t, T_val, r):
        b = B(t, T_val)
        A_val = np.exp((b - (T_val - t)) * (a ** 2 * 0 - sigma ** 2 / (2 * a ** 2)) -
                        sigma ** 2 * b ** 2 / (4 * a))
        return A_val * np.exp(-b * r)

    # Generate cash flow times
    coupon = face_value * coupon_rate / frequency
    cf_times = np.arange(T_option + 1.0 / frequency, T_bond + 1e-10, 1.0 / frequency)
    cf_amounts = np.full(len(cf_times), coupon)
    if len(cf_amounts) > 0:
        cf_amounts[-1] += face_value

    if len(cf_amounts) == 0:
        cf_times = np.array([T_bond])
        cf_amounts = np.array([face_value])

    sigma_p = sigma * B(T_option, cf_times) * np.sqrt((1 - np.exp(-2 * a * T_option)) / (2 * a))

    # Find r* such that sum of discounted CFs = strike
    from scipy.optimize import brentq

    def bond_price_at_r(r_star):
        return np.sum(cf_amounts * np.exp(-B(T_option, cf_times) * r_star)) - strike

    try:
        r_star = brentq(bond_price_at_r, -0.2, 0.5)
    except ValueError:
        r_star = r0

    X_i = np.exp(-B(T_option, cf_times) * r_star)
    h_i = (1 / sigma_p) * np.log(cf_amounts * P(0, cf_times, r0) / (X_i * P(0, T_option, r0) * strike / np.sum(cf_amounts * X_i))) + sigma_p / 2

    call_price = np.sum(cf_amounts * P(0, cf_times, r0) * stats.norm.cdf(h_i) -
                         X_i * P(0, T_option, r0) * (strike / np.sum(cf_amounts * X_i)) * stats.norm.cdf(h_i - sigma_p))
    put_price = call_price - np.sum(cf_amounts * P(0, cf_times, r0)) + strike * P(0, T_option, r0)

    return {'call_price': max(call_price, 0), 'put_price': max(put_price, 0)}


def hull_white_model(r0, a, sigma, theta_func, T, n_steps):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Short rate models', 'Hull-White calibration']
    function: "Simulates a single short rate path under the Hull-White model. dr_t = [theta(t) - a*r_t]*dt + sigma*dW_t"
    y_as_x: []
    :param r0: "Initial short rate"
    :param a: "Mean reversion speed"
    :param sigma: "Short rate volatility"
    :param theta_func: "Time-dependent drift function theta(t)"
    :param T: "Time horizon in years"
    :param n_steps: "Number of simulation time steps"
    :return: "Dictionary with 'times', 'rates' arrays"
    '''
    dt = T / n_steps
    times = np.linspace(0, T, n_steps + 1)
    rates = np.zeros(n_steps + 1)
    rates[0] = r0
    for i in range(n_steps):
        t = times[i]
        dW = np.random.standard_normal() * np.sqrt(dt)
        rates[i + 1] = rates[i] + (theta_func(t) - a * rates[i]) * dt + sigma * dW
    return {'times': times, 'rates': rates}


def ichimoku_base_line(high, low, period=26):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Ichimoku cloud', 'Trend indicators']
    function: "Computes the Ichimoku Kijun-sen (base line). Kijun = (26-period high + 26-period low) / 2"
    y_as_x: ['ichimoku_leading_span_a']
    :param high: "Array or Series of high prices"
    :param low: "Array or Series of low prices"
    :param period: "Lookback period (default 26)"
    :return: "Series of Kijun-sen values"
    '''
    high = pd.Series(high)
    low = pd.Series(low)
    highest = high.rolling(window=period).max()
    lowest = low.rolling(window=period).min()
    return (highest + lowest) / 2


def ichimoku_conversion_line(high, low, period=9):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Ichimoku cloud', 'Trend indicators']
    function: "Computes the Ichimoku Tenkan-sen (conversion line). Tenkan = (9-period high + 9-period low) / 2"
    y_as_x: ['ichimoku_leading_span_a']
    :param high: "Array or Series of high prices"
    :param low: "Array or Series of low prices"
    :param period: "Lookback period (default 9)"
    :return: "Series of Tenkan-sen values"
    '''
    high = pd.Series(high)
    low = pd.Series(low)
    highest = high.rolling(window=period).max()
    lowest = low.rolling(window=period).min()
    return (highest + lowest) / 2
