"""
Financial Functions - Complete Collection (814 Equations)
Auto-generated Python implementations of financial, actuarial, and technical analysis equations.
Date: 03-04-2026
"""
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import norm
import warnings

"""
- It turns out I made a mistake with the domain and subdomain. I gave it empty columns instead of domain and subdomain
to copy from. But I see it did a better job then GPT5.2
- It turns out y_as_x was generated not exactly as requested. It is built on association to a function. 
Not specifically if y is given as x in another function. This turns out to be a much better way because it 
finds more connections. However it requires manual fix.
"""


# ================================================================================
# BATCH 1
# ================================================================================
# fixme
def abnormal_earnings_growth(eps_next, required_return, abnormal_growth_pv):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Equity Valuation', 'Earnings-Based Valuation']
    function: "Computes the intrinsic stock price using the Ohlson-Juettner model: capitalized next-period earnings plus the present value of abnormal earnings growth."
    y_as_x: ['clean_price']
    :param eps_next: "Expected earnings per share for the next period"
    :param required_return: "Required rate of return (cost of equity)"
    :param abnormal_growth_pv: "Present value of future abnormal earnings growth beyond normal earnings"
    :return: "Intrinsic price P_0 = capitalized next earnings + PV abnormal earnings growth"
    '''
    capitalized_earnings = eps_next / required_return
    return capitalized_earnings + abnormal_growth_pv


def abs_pool_factor(current_pool_balance, original_pool_balance):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Asset-Backed Securities', 'Pool Performance']
    function: "Computes the ABS pool factor, which measures the fraction of the original pool balance that remains outstanding at time t."
    y_as_x: []
    :param current_pool_balance: "Current outstanding principal balance of the ABS pool at time t"
    :param original_pool_balance: "Original principal balance of the ABS pool at issuance"
    :return: "Pool factor = Current Pool Balance / Original Pool Balance, ranges from 0 to 1"
    '''
    return current_pool_balance / original_pool_balance


# fixme: change to total assets and fix y_as_x
def accounting_identity(liabilities, equity):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statements', 'Balance Sheet Analysis']
    function: "Computes total assets using the fundamental accounting identity: Assets = Liabilities + Equity."
    y_as_x: ['asset_turnover', 'debt_to_assets', 'book_value_per_share', 'equity_ratio']
    :param liabilities: "Total liabilities of the firm"
    :param equity: "Total shareholders equity of the firm"
    :return: "Total assets = Liabilities + Equity"
    '''
    return liabilities + equity


def accrued_interest(coupon_rate, face_value, day_count_fraction):
    '''
    domain: ['Fixed income & bond math']
    subdomain: ['Bond Pricing', 'Accrued Interest']
    function: "Computes the accrued interest on a bond between coupon dates using the day count fraction. AI = Coupon x DayCountFraction."
    y_as_x: ['dirty_price', 'clean_price']
    :param coupon_rate: "Annual coupon rate of the bond (as decimal)"
    :param face_value: "Face (par) value of the bond"
    :param day_count_fraction: "Fraction of the coupon period elapsed since last coupon date"
    :return: "Accrued interest amount = coupon_rate * face_value * day_count_fraction"
    '''
    coupon = coupon_rate * face_value
    return coupon * day_count_fraction


def accumulation_over_distribution_line(high, low, close, volume):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Volume Indicators', 'Accumulation/Distribution']
    function: "Computes the Accumulation/Distribution Line (ADL), a cumulative volume-based indicator. ADL_t = ADL_{t-1} + MFM_t x Volume_t, where MFM is the Money Flow Multiplier."
    y_as_x: ['chaikin_oscillator']
    :param high: "Array of high prices for each period"
    :param low: "Array of low prices for each period"
    :param close: "Array of closing prices for each period"
    :param volume: "Array of trading volume for each period"
    :return: "Accumulation/Distribution Line as a numpy array"
    '''
    try:
        import talib
        return talib.AD(high, low, close, volume)
    except ImportError:
        high = np.asarray(high, dtype=float)
        low = np.asarray(low, dtype=float)
        close = np.asarray(close, dtype=float)
        volume = np.asarray(volume, dtype=float)
        hl_range = high - low
        mfm = np.where(hl_range != 0, ((close - low) - (high - close)) / hl_range, 0.0)
        mfv = mfm * volume
        return np.cumsum(mfv)


def active_return(portfolio_return, benchmark_return):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Performance', 'Active Management']
    function: "Computes the active return, defined as the difference between the portfolio return and the benchmark return."
    y_as_x: ['information_ratio', 'tracking_error', 'active_risk_budget']
    :param portfolio_return: "Return of the portfolio over the measurement period"
    :param benchmark_return: "Return of the benchmark over the measurement period"
    :return: "Active return AR = R_p - R_b"
    '''
    return portfolio_return - benchmark_return


def active_risk_budget(information_coefficient, breadth):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Risk Budgeting', 'Active Management']
    function: "Computes the expected information ratio using the Fundamental Law of Active Management: IR = IC x sqrt(Breadth)."
    y_as_x: []
    :param information_coefficient: "Correlation between forecasted and realized active returns (IC)"
    :param breadth: "Number of independent investment decisions per year"
    :return: "Expected information ratio IR = IC * sqrt(Breadth)"
    '''
    return information_coefficient * np.sqrt(breadth)


def active_share(portfolio_weights, benchmark_weights):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Construction', 'Active Management']
    function: "Computes Active Share, a measure of how different a portfolio is from its benchmark. Active Share = 0.5 * sum|w_i - w_{b,i}|."
    y_as_x: []
    :param portfolio_weights: "Array of portfolio weights for each security"
    :param benchmark_weights: "Array of benchmark weights for each security"
    :return: "Active Share ranging from 0 (index replication) to 1 (fully active)"
    '''
    portfolio_weights = np.asarray(portfolio_weights, dtype=float)
    benchmark_weights = np.asarray(benchmark_weights, dtype=float)
    return 0.5 * np.sum(np.abs(portfolio_weights - benchmark_weights))


def adf_unit_root_test(time_series, max_lags=None, regression='c'):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Time Series Analysis', 'Stationarity Testing']
    function: "Performs the Augmented Dickey-Fuller unit root test to assess whether a time series is stationary. Tests H0: unit root exists (non-stationary)."
    y_as_x: []
    :param time_series: "Array-like time series data to test for unit root"
    :param max_lags: "Maximum number of lags to include in the test regression (None for automatic)"
    :param regression: "Constant and trend order to include: 'c' (constant only), 'ct' (constant+trend), 'ctt', 'n' (none)"
    :return: "Tuple of (adf_statistic, p_value, lags_used, nobs, critical_values, icbest)"
    '''
    from statsmodels.tsa.stattools import adfuller
    result = adfuller(time_series, maxlag=max_lags, regression=regression)
    return result


# fixme
def adjusted_present_value_apv(npv_unlevered, pv_financing_effects):
    '''
    domain: ['Corporate finance & capital budgeting']
    subdomain: ['Valuation', 'Capital Structure']
    function: "Computes the Adjusted Present Value (APV) as the sum of unlevered NPV and the present value of financing side effects (tax shields, subsidies, etc.)."
    y_as_x: []
    :param npv_unlevered: "Net present value of the project assuming all-equity financing"
    :param pv_financing_effects: "Present value of financing side effects (e.g., tax shields from debt)"
    :return: "APV = NPV_unlevered + PV(financing side effects)"
    '''
    return npv_unlevered + pv_financing_effects


def adjusted_r_squared(r_squared, n, k):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Regression Analysis', 'Model Fit']
    function: "Computes the adjusted R-squared, which penalizes R-squared for the number of regressors to prevent overfitting."
    y_as_x: []
    :param r_squared: "Unadjusted R-squared of the regression"
    :param n: "Number of observations"
    :param k: "Number of independent variables (regressors, excluding intercept)"
    :return: "Adjusted R-squared = 1 - (1-R^2)(n-1)/(n-k-1)"
    '''
    return 1.0 - (1.0 - r_squared) * (n - 1) / (n - k - 1)


def advance_rate(loan_amount, eligible_collateral_base):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Secured Lending', 'Collateral Management']
    function: "Computes the advance rate, which measures the percentage of eligible collateral that the lender is willing to lend against."
    y_as_x: ['borrowing_base']
    :param loan_amount: "Total loan amount extended to the borrower"
    :param eligible_collateral_base: "Total eligible collateral base value"
    :return: "Advance Rate = Loan Amount / Eligible Collateral Base"
    '''
    return loan_amount / eligible_collateral_base


# fixme
def adverse_selection_cost(effective_spread, realized_spread):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Execution Cost Analysis', 'Market Microstructure']
    function: "Computes the adverse selection cost component of the bid-ask spread, representing the cost of trading against informed traders."
    y_as_x: []
    :param effective_spread: "Effective spread: 2 * |trade_price - midpoint|"
    :param realized_spread: "Realized spread: 2 * direction * (trade_price - midpoint_{t+delta})"
    :return: "Adverse selection cost = Effective Spread - Realized Spread"
    '''
    return effective_spread - realized_spread


def adx(high, low, close, timeperiod=14):
    '''
    domain: ['Technical analysis']
    subdomain: ['Trend Indicators', 'Directional Movement']
    function: "Computes the Average Directional Index (ADX), which measures the strength of a trend regardless of direction."
    y_as_x: []
    :param high: "Array of high prices"
    :param low: "Array of low prices"
    :param close: "Array of closing prices"
    :param timeperiod: "Lookback period for the ADX calculation (default 14)"
    :return: "ADX values as a numpy array"
    '''
    import talib
    return talib.ADX(high, low, close, timeperiod=timeperiod)


def affine_term_structure_bond_price(a_coeff, b_coeff, state_vector):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Term Structure Models', 'Affine Models']
    function: "Computes the zero-coupon bond price under an affine term structure model: P(t,T) = exp(A(t,T) + B(t,T)' X_t)."
    y_as_x: []
    :param a_coeff: "Scalar A(t,T) coefficient from the affine model solution"
    :param b_coeff: "Vector B(t,T) of factor loadings from the affine model"
    :param state_vector: "Vector X_t of state variables. usually represent underlying risk drivers (e.g., short rate factors)"
    :return: "Zero-coupon bond price P(t,T) = exp(A + B'X)"
    '''
    b_coeff = np.asarray(b_coeff, dtype=float)
    state_vector = np.asarray(state_vector, dtype=float)
    return np.exp(a_coeff + np.dot(b_coeff, state_vector))


def after_tax_cost_of_debt(pre_tax_cost_of_debt, tax_rate):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Cost of Capital', 'Capital Structure']
    function: "Computes the after-tax cost of debt, reflecting the tax deductibility of interest payments."
    y_as_x: ['weighted_average_cost_of_capital_wacc']
    :param pre_tax_cost_of_debt: "Pre-tax cost of debt (yield on debt, R_d)"
    :param tax_rate: "Marginal corporate tax rate (T)"
    :return: "After-tax cost of debt = R_d * (1 - T)"
    '''
    return pre_tax_cost_of_debt * (1.0 - tax_rate)


def aggregate_loss_distribution(frequency_mean, severity_mean, severity_std, n_simulations=100000, seed=42):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Loss Modeling', 'Aggregate Risk','Actuarial Mathematics', 'Insurance Analytics']
    function: "Simulates the aggregate loss distribution S = sum_{i=1}^N X_i where N is Poisson-distributed claim frequency and X_i are iid severity draws."
    y_as_x: []
    :param frequency_mean: "Mean of the Poisson claim frequency distribution (lambda)"
    :param severity_mean: "Mean of the lognormal severity distribution"
    :param severity_std: "Standard deviation of the lognormal severity distribution"
    :param n_simulations: "Number of Monte Carlo simulations (default 100000)"
    :param seed: "Random seed for reproducibility"
    :return: "Array of simulated aggregate loss values"
    '''
    rng = np.random.default_rng(seed)
    # Lognormal parameters from mean and std
    sigma2 = np.log(1 + (severity_std / severity_mean) ** 2)
    mu = np.log(severity_mean) - 0.5 * sigma2
    sigma = np.sqrt(sigma2)
    frequencies = rng.poisson(frequency_mean, size=n_simulations)
    total_claims = int(np.sum(frequencies))
    severities = rng.lognormal(mu, sigma, size=total_claims)
    aggregate_losses = np.zeros(n_simulations)
    idx = 0
    for i in range(n_simulations):
        n = frequencies[i]
        if n > 0:
            aggregate_losses[i] = np.sum(severities[idx:idx + n])
            idx += n
    return aggregate_losses



def alpha(returns, factor_returns, risk_free_rate=0.0):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Asset Pricing', 'CAPM']
    function: "Computes Jensen's alpha: the excess return of an asset beyond what is predicted by the CAPM. alpha = E[R_i] - [R_f + beta_i(E[R_m]-R_f)]."
    y_as_x: ['alpha_from_regression', 'appraisal_ratio','henriksson_merton_timing']
    :param returns: "Array of asset returns"
    :param factor_returns: "Array of market (benchmark) returns"
    :param risk_free_rate: "Risk-free rate per period (default 0)"
    :return: "Annualized Jensen's alpha"
    '''
    returns = np.asarray(returns, dtype=float)
    factor_returns = np.asarray(factor_returns, dtype=float)
    excess_r = returns - risk_free_rate
    excess_m = factor_returns - risk_free_rate
    b = np.cov(excess_r, excess_m)[0, 1] / np.var(excess_m, ddof=1)
    alpha_val = np.mean(excess_r) - b * np.mean(excess_m)
    return alpha_val


# stopped here
# fixme: add all the y_as_x
def returns(start_val, end_val):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Asset Pricing', 'CAPM']
    function: "Return - the percentage of change between the value at start to the value at end."
    y_as_x: ['alpha_from_regression', 'alpha','amihud_illiquidity','amivest_liquidity_ratio','annualized_return_cagr','annualized_volatility','aparch','arch_q','batting_average',
    'benchmark_relative_optimization','beta','bipower_variation','burke_ratio','calmar_ratio','carhart_4_factor_model',
    'covariance_matrix','cumulative_return','downside_capture','downside_deviation','efficient_frontier_problem','egarch',
    'egarch_11','equal_risk_contribution','ewma_volatility','ex_ante_tracking_error','excess_kurtosis','excess_return',
    'expected_drawdown','expected_shortfall_cvar','garch_11','garch_11_v2','gjr_garch','global_minimum_variance_portfolio',
    'hasbrouck_lambda','henriksson_merton_timing','historical_var','hit_ratio','idiosyncratic_volatility','incremental_var','information_ratio',
    'interaction_effect','ledoit_wolf_covariance_shrinkage','maximum_drawdown','maximum_sharpe_portfolio','mean_cvar_optimization',
    'mean_variance_utility','monte_carlo_var','m_squared_modigliani','omega_ratio','pain_index','parametric_normal_var',
    'parametric_var','pastor_stambaugh_liquidity','portfolio_return']
    :param start_val: "the value at the beginning of the period"
    :param end_val: "the value at the end of the period"
    :return: "end/start-1"
    '''
    return (end_val / start_val) - 1


def alpha_from_regression(portfolio_returns, benchmark_returns, risk_free_rate=0.0):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Regression Analysis', 'Performance Measurement']
    function: "Estimates alpha from a single-factor regression: R_p - R_f = alpha + beta(R_b - R_f) + epsilon."
    y_as_x: []
    :param portfolio_returns: "Array of portfolio returns"
    :param benchmark_returns: "Array of benchmark returns"
    :param risk_free_rate: "Risk-free rate per period (default 0)"
    :return: "Tuple of (alpha, beta, r_squared) from the regression"
    '''
    import statsmodels.api as sm
    y = np.asarray(portfolio_returns, dtype=float) - risk_free_rate
    x = np.asarray(benchmark_returns, dtype=float) - risk_free_rate
    X = sm.add_constant(x)
    model = sm.OLS(y, X).fit()
    return model.params[0], model.params[1], model.rsquared


def altman_z_score(working_capital, total_assets, retained_earnings, ebit, market_cap, total_liabilities, revenue):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Credit Analysis', 'Financial Ratios']
    function: "Computes the Altman Z-score for predicting bankruptcy: Z = 1.2*X1 + 1.4*X2 + 3.3*X3 + 0.6*X4 + 1.0*X5."
    y_as_x: []
    :param working_capital: "Working capital (current assets - current liabilities)"
    :param total_assets: "Total assets of the firm"
    :param retained_earnings: "Retained earnings"
    :param ebit: "Earnings before interest and taxes"
    :param market_cap: "Market capitalization (market value of equity)"
    :param total_liabilities: "Total liabilities"
    :param revenue: "Net sales / revenue"
    :return: "Altman Z-score: >2.99 safe zone, 1.81-2.99 grey zone, <1.81 distress zone"
    '''
    x1 = working_capital / total_assets
    x2 = retained_earnings / total_assets
    x3 = ebit / total_assets
    x4 = market_cap / total_liabilities
    x5 = revenue / total_assets
    return 1.2 * x1 + 1.4 * x2 + 3.3 * x3 + 0.6 * x4 + 1.0 * x5


def american_option_binomial_pricing(spot, strike, rate, volatility, time_to_maturity, steps=100, option_type='call',
                                     dividend_yield=0.0):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Option Pricing', 'Binomial Models']
    function: "Prices an American option using the Cox-Ross-Rubinstein binomial tree, allowing for early exercise at each node."
    y_as_x: []
    :param spot: "Current price of the underlying asset"
    :param strike: "Strike price of the option"
    :param rate: "Risk-free interest rate (annualized, continuous)"
    :param volatility: "Annualized volatility of the underlying"
    :param time_to_maturity: "Time to expiration in years"
    :param steps: "Number of binomial tree steps (default 100)"
    :param option_type: "'call' or 'put'"
    :param dividend_yield: "Continuous dividend yield (default 0)"
    :return: "American option price"
    '''
    dt = time_to_maturity / steps
    u = np.exp(volatility * np.sqrt(dt))
    d = 1.0 / u
    disc = np.exp(-rate * dt)
    p = (np.exp((rate - dividend_yield) * dt) - d) / (u - d)
    # Build asset prices at maturity
    asset_prices = spot * u ** np.arange(steps, -1, -1) * d ** np.arange(0, steps + 1)
    if option_type == 'call':
        option_values = np.maximum(asset_prices - strike, 0.0)
    else:
        option_values = np.maximum(strike - asset_prices, 0.0)
    # Step backward
    for i in range(steps - 1, -1, -1):
        asset_prices = spot * u ** np.arange(i, -1, -1) * d ** np.arange(0, i + 1)
        option_values = disc * (p * option_values[:-1] + (1 - p) * option_values[1:])
        if option_type == 'call':
            intrinsic = np.maximum(asset_prices - strike, 0.0)
        else:
            intrinsic = np.maximum(strike - asset_prices, 0.0)
        option_values = np.maximum(option_values, intrinsic)
    return option_values[0]


def amihud_illiquidity(returns, dollar_volume):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Liquidity Measurement', 'Market Microstructure']
    function: "Computes the Amihud illiquidity measure: ILLIQ = mean(|R_t| / DollarVolume_t). Higher values indicate less liquid assets."
    y_as_x: []
    :param returns: "Array of asset returns"
    :param dollar_volume: "Array of dollar trading volume for each period"
    :return: "Amihud illiquidity ratio"
    '''
    returns = np.asarray(returns, dtype=float)
    dollar_volume = np.asarray(dollar_volume, dtype=float)
    return np.mean(np.abs(returns) / dollar_volume)


def amivest_liquidity_ratio(volume, returns):
    '''
    domain: ['Trading, execution & market microstructure']
    subdomain: ['Liquidity Measurement', 'Market Microstructure']
    function: "Computes the Amivest liquidity ratio: Volume / |Return|. Higher values indicate greater liquidity."
    y_as_x: []
    :param volume: "Array of trading volume (or dollar volume)"
    :param returns: "Array of asset returns"
    :return: "Amivest liquidity ratio = sum(Volume) / sum(|Return|)"
    '''
    volume = np.asarray(volume, dtype=float)
    returns = np.asarray(returns, dtype=float)
    abs_returns = np.abs(returns)
    mask = abs_returns > 0
    return np.sum(volume[mask]) / np.sum(abs_returns[mask])


def amortization_factor(rate, n_periods):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Loan Amortization', 'Mortgage Mathematics']
    function: "Computes the amortization factor (capital recovery factor): AF = r(1+r)^n / ((1+r)^n - 1), which converts a present value into a periodic payment."
    y_as_x: ['equated_monthly_installment_emi', 'loan_payment_annuity']
    :param rate: "Periodic interest rate (e.g., monthly rate)"
    :param n_periods: "Total number of payment periods"
    :return: "Amortization factor"
    '''
    try:
        import numpy_financial as npf
        # pmt returns negative, so negate and divide by 1 to get factor per unit PV
        return -npf.pmt(rate, n_periods, 1.0)
    except ImportError:
        if rate == 0:
            return 1.0 / n_periods
        return rate * (1 + rate) ** n_periods / ((1 + rate) ** n_periods - 1)


def annual_percentage_rate_apr(periodic_rate, periods_per_year):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Consumer Lending', 'Interest Rate Disclosure']
    function: "Computes the Annual Percentage Rate (APR) as periodic rate times the number of periods per year."
    y_as_x: ['effective_annual_rate_ear']
    :param periodic_rate: "Interest rate per period (e.g., monthly rate)"
    :param periods_per_year: "Number of compounding periods per year"
    :return: "APR = periodic_rate * periods_per_year"
    '''
    return periodic_rate * periods_per_year


def annualized_cpi_inflation_from_monthly_cpi(cpi_current, cpi_previous):
    '''
    domain: ['Macroeconomics, inflation & price indices']
    subdomain: ['Inflation Measurement', 'Consumer Price Index']
    function: "Computes annualized CPI inflation from consecutive monthly CPI readings: pi = (CPI_t / CPI_{t-1})^12 - 1."
    y_as_x: []
    :param cpi_current: "CPI value for the current month"
    :param cpi_previous: "CPI value for the previous month"
    :return: "Annualized inflation rate"
    '''
    return (cpi_current / cpi_previous) ** 12 - 1


def annualized_ppi_inflation_from_monthly_ppi(ppi_current, ppi_previous):
    '''
    domain: ['Macroeconomics, inflation & price indices']
    subdomain: ['Inflation Measurement', 'Producer Price Index']
    function: "Computes annualized PPI inflation from consecutive monthly PPI readings: pi = (PPI_t / PPI_{t-1})^12 - 1."
    y_as_x: []
    :param ppi_current: "PPI value for the current month"
    :param ppi_previous: "PPI value for the previous month"
    :return: "Annualized PPI inflation rate"
    '''
    return (ppi_current / ppi_previous) ** 12 - 1


def annualized_return_cagr(returns, period='daily'):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Return Measurement', 'Performance Metrics']
    function: "Computes the Compound Annual Growth Rate (CAGR) or annualized return from a series of periodic returns."
    y_as_x: ['sharpe_ratio', 'calmar_ratio', 'sortino_ratio', 'treynor_ratio', 'information_ratio']
    :param returns: "Array of periodic returns"
    :param period: "'daily', 'weekly', or 'monthly' to determine annualization factor"
    :return: "Annualized return (CAGR)"
    '''
    try:
        import empyrical
        return empyrical.annual_return(returns, period=period)
    except ImportError:
        returns = np.asarray(returns, dtype=float)
        ann_factors = {'daily': 252, 'weekly': 52, 'monthly': 12}
        ann = ann_factors.get(period, 252)
        cum = np.prod(1 + returns)
        n_periods = len(returns)
        return cum ** (ann / n_periods) - 1


def annualized_volatility(returns, period='daily'):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Risk Measurement', 'Volatility']
    function: "Computes annualized volatility by scaling periodic standard deviation: sigma_ann = sigma_period * sqrt(m)."
    y_as_x: ['sharpe_ratio', 'sortino_ratio', 'calmar_ratio', 'parametric_normal_var', 'parametric_var']
    :param returns: "Array of periodic returns"
    :param period: "'daily', 'weekly', or 'monthly' to determine annualization factor"
    :return: "Annualized volatility"
    '''
    try:
        import empyrical
        return empyrical.annual_volatility(returns, period=period)
    except ImportError:
        returns = np.asarray(returns, dtype=float)
        ann_factors = {'daily': 252, 'weekly': 52, 'monthly': 12}
        ann = ann_factors.get(period, 252)
        return np.std(returns, ddof=1) * np.sqrt(ann)


def annuity_future_value(payment, rate, n_periods):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Time Value of Money', 'Annuities']
    function: "Computes the future value of an ordinary annuity: FV = PMT * ((1+r)^n - 1) / r."
    y_as_x: []
    :param payment: "Periodic payment amount (PMT)"
    :param rate: "Interest rate per period"
    :param n_periods: "Total number of periods"
    :return: "Future value of the annuity"
    '''
    try:
        import numpy_financial as npf
        return npf.fv(rate, n_periods, -payment, 0)
    except ImportError:
        if rate == 0:
            return payment * n_periods
        return payment * ((1 + rate) ** n_periods - 1) / rate


def annuity_present_value(payment, rate, n_periods):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Time Value of Money', 'Annuities']
    function: "Computes the present value of an ordinary annuity: PV = PMT * (1 - (1+r)^-n) / r."
    y_as_x: ['adjusted_present_value_apv', 'loan_payment_annuity']
    :param payment: "Periodic payment amount (PMT)"
    :param rate: "Discount rate per period"
    :param n_periods: "Total number of periods"
    :return: "Present value of the annuity"
    '''
    try:
        import numpy_financial as npf
        return -npf.pv(rate, n_periods, payment, 0)
    except ImportError:
        if rate == 0:
            return payment * n_periods
        return payment * (1 - (1 + rate) ** (-n_periods)) / rate


def aparch(returns, omega=0.01, alpha_coeff=0.1, gamma=0.5, delta=2.0, beta_coeff=0.85):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Volatility Modeling', 'GARCH Family']
    function: "Fits an Asymmetric Power ARCH (APARCH) model: sigma_t^delta = omega + alpha(|eps_{t-1}| - gamma*eps_{t-1})^delta + beta*sigma_{t-1}^delta."
    y_as_x: []
    :param returns: "Array of asset returns (or residuals)"
    :param omega: "Constant term in the variance equation"
    :param alpha_coeff: "ARCH coefficient"
    :param gamma: "Asymmetry (leverage) parameter, between -1 and 1"
    :param delta: "Power parameter (delta > 0)"
    :param beta_coeff: "GARCH coefficient"
    :return: "Dictionary with 'conditional_power_vol' array sigma_t^delta and 'params'"
    '''
    try:
        from arch import arch_model
        am = arch_model(np.asarray(returns) * 100, vol='APARCH', p=1, q=1, o=1)
        res = am.fit(disp='off')
        return {'model_result': res, 'conditional_volatility': res.conditional_volatility}
    except (ImportError, Exception):
        returns = np.asarray(returns, dtype=float)
        n = len(returns)
        sigma_delta = np.zeros(n)
        sigma_delta[0] = omega / (1 - alpha_coeff - beta_coeff) if (alpha_coeff + beta_coeff) < 1 else omega
        for t in range(1, n):
            shock = (np.abs(returns[t - 1]) - gamma * returns[t - 1]) ** delta
            sigma_delta[t] = omega + alpha_coeff * shock + beta_coeff * sigma_delta[t - 1]
        return {'conditional_power_vol': sigma_delta,
                'params': {'omega': omega, 'alpha': alpha_coeff, 'gamma': gamma, 'delta': delta, 'beta': beta_coeff}}


def appraisal_ratio(alpha_val, residual_risk):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Performance Measurement', 'Risk-Adjusted Returns']
    function: "Computes the appraisal ratio (Treynor-Black): alpha divided by residual (idiosyncratic) risk."
    y_as_x: []
    :param alpha_val: "Jensen's alpha or regression alpha of the portfolio"
    :param residual_risk: "Standard deviation of the residual (unsystematic) risk from regression"
    :return: "Appraisal ratio = alpha / residual_risk"
    '''
    return alpha_val / residual_risk


def approximate_price_change(modified_duration, convexity, yield_change):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Bond Risk Measures', 'Duration & Convexity']
    function: "Approximates the percentage price change of a bond using duration and convexity: dP/P ~ -D_mod * dy + 0.5 * Convexity * dy^2."
    y_as_x: []
    :param modified_duration: "Modified duration of the bond"
    :param convexity: "Convexity of the bond"
    :param yield_change: "Change in yield (Delta y) in decimal form"
    :return: "Approximate percentage price change dP/P"
    '''
    return -modified_duration * yield_change + 0.5 * convexity * yield_change ** 2


def ar_1(time_series, constant=True):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Time Series Models', 'Autoregressive Models']
    function: "Fits an AR(1) model: y_t = c + phi*y_{t-1} + epsilon_t using OLS or statsmodels AutoReg."
    y_as_x: []
    :param time_series: "Array-like time series data"
    :param constant: "Whether to include a constant term (default True)"
    :return: "Dictionary with 'constant', 'phi', 'residuals', and 'model' keys"
    '''
    from statsmodels.tsa.ar_model import AutoReg
    ts = np.asarray(time_series, dtype=float)
    trend = 'c' if constant else 'n'
    model = AutoReg(ts, lags=1, trend=trend).fit()
    return {'constant': model.params[0] if constant else 0.0, 'phi': model.params[-1], 'residuals': model.resid,
            'model': model}


def ar_1_v2(time_series, constant=True):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Time Series Models', 'Autoregressive Models']
    function: "Fits an AR(1) model (variant): x_t = c + phi*x_{t-1} + epsilon_t."
    y_as_x: []
    :param time_series: "Array-like time series data"
    :param constant: "Whether to include a constant term (default True)"
    :return: "Dictionary with 'constant', 'phi', 'residuals', and 'model' keys"
    '''
    from statsmodels.tsa.ar_model import AutoReg
    ts = np.asarray(time_series, dtype=float)
    trend = 'c' if constant else 'n'
    model = AutoReg(ts, lags=1, trend=trend).fit()
    return {'constant': model.params[0] if constant else 0.0, 'phi': model.params[-1], 'residuals': model.resid,
            'model': model}


def ar_p(time_series, p=1, constant=True):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Time Series Models', 'Autoregressive Models']
    function: "Fits an AR(p) model: x_t = c + sum_{i=1}^p phi_i * x_{t-i} + epsilon_t."
    y_as_x: ['arma_pq', 'arima_pdq']
    :param time_series: "Array-like time series data"
    :param p: "Number of autoregressive lags"
    :param constant: "Whether to include a constant term (default True)"
    :return: "Dictionary with 'params', 'residuals', and 'model' keys"
    '''
    from statsmodels.tsa.ar_model import AutoReg
    ts = np.asarray(time_series, dtype=float)
    trend = 'c' if constant else 'n'
    model = AutoReg(ts, lags=p, trend=trend).fit()
    return {'params': model.params, 'residuals': model.resid, 'model': model}


def arbitrage_pricing_theory_apt(risk_free_rate, betas, factor_risk_premia):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Asset Pricing', 'Factor Models']
    function: "Computes the expected return under the Arbitrage Pricing Theory: E[R_i] = R_f + sum_k beta_ik * lambda_k."
    y_as_x: ['capm_expected_return']
    :param risk_free_rate: "Risk-free rate"
    :param betas: "Array of factor betas (sensitivities) for the asset"
    :param factor_risk_premia: "Array of factor risk premia (lambda_k)"
    :return: "Expected return under APT"
    '''
    betas = np.asarray(betas, dtype=float)
    factor_risk_premia = np.asarray(factor_risk_premia, dtype=float)
    return risk_free_rate + np.dot(betas, factor_risk_premia)


def arch_q(returns, q=1):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Volatility Modeling', 'ARCH Models']
    function: "Fits an ARCH(q) model: sigma_t^2 = omega + sum_{i=1}^q alpha_i * epsilon_{t-i}^2."
    y_as_x: ['garch_11', 'aparch']
    :param returns: "Array of asset returns (percentage or decimal)"
    :param q: "Number of ARCH lags (default 1)"
    :return: "Dictionary with fitted model result and conditional volatility"
    '''
    try:
        from arch import arch_model
        am = arch_model(np.asarray(returns) * 100, vol='ARCH', q=q, mean='Constant')
        res = am.fit(disp='off')
        return {'model_result': res, 'conditional_volatility': res.conditional_volatility}
    except ImportError:
        returns = np.asarray(returns, dtype=float)
        n = len(returns)
        mu = np.mean(returns)
        eps = returns - mu
        var_unconditional = np.var(eps)
        sigma2 = np.full(n, var_unconditional)
        omega = var_unconditional * 0.1
        alphas = np.full(q, 0.9 / q)
        for t in range(q, n):
            sigma2[t] = omega + sum(alphas[i] * eps[t - 1 - i] ** 2 for i in range(q))
        return {'conditional_variance': sigma2, 'residuals': eps}


def arima_pdq(time_series, order=(1, 1, 1)):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Time Series Models', 'ARIMA']
    function: "Fits an ARIMA(p,d,q) model: phi(L)(1-L)^d x_t = c + theta(L)*epsilon_t."
    y_as_x: ['arimax_over_dynamic_regression', 'sarima']
    :param time_series: "Array-like time series data"
    :param order: "Tuple (p, d, q) for AR order, differencing, and MA order"
    :return: "Dictionary with fitted model, params, residuals, and AIC"
    '''
    from statsmodels.tsa.arima.model import ARIMA
    ts = np.asarray(time_series, dtype=float)
    model = ARIMA(ts, order=order).fit()
    return {'model': model, 'params': model.params, 'residuals': model.resid, 'aic': model.aic}


def arimax_over_dynamic_regression(endog, exog, order=(1, 0, 1)):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Time Series Models', 'Dynamic Regression']
    function: "Fits an ARIMAX / dynamic regression model: y_t = beta'x_t + ARIMA errors, using SARIMAX."
    y_as_x: []
    :param endog: "Endogenous (dependent) time series"
    :param exog: "Exogenous (independent) variables, array or DataFrame"
    :param order: "ARIMA order tuple (p, d, q)"
    :return: "Dictionary with fitted model, params, residuals, and AIC"
    '''
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    model = SARIMAX(endog, exog=exog, order=order).fit(disp=False)
    return {'model': model, 'params': model.params, 'residuals': model.resid, 'aic': model.aic}


def arma_pq(time_series, order=(1, 1)):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Time Series Models', 'ARMA']
    function: "Fits an ARMA(p,q) model: x_t = c + sum phi_i*x_{t-i} + epsilon_t + sum theta_i*epsilon_{t-i}."
    y_as_x: ['arima_pdq']
    :param time_series: "Array-like time series data"
    :param order: "Tuple (p, q) for AR and MA orders"
    :return: "Dictionary with fitted model, params, residuals, and AIC"
    '''
    from statsmodels.tsa.arima.model import ARIMA
    ts = np.asarray(time_series, dtype=float)
    arima_order = (order[0], 0, order[1])
    model = ARIMA(ts, order=arima_order).fit()
    return {'model': model, 'params': model.params, 'residuals': model.resid, 'aic': model.aic}


def aroon_down(high, low, timeperiod=25):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Trend Indicators', 'Aroon']
    function: "Computes Aroon Down: AroonDown = 100 * (n - periods since n-period low) / n."
    y_as_x: ['aroon_oscillator']
    :param high: "Array of high prices"
    :param low: "Array of low prices"
    :param timeperiod: "Lookback period (default 25)"
    :return: "Aroon Down values as numpy array"
    '''
    try:
        import talib
        aroon_dn, _ = talib.AROON(high, low, timeperiod=timeperiod)
        return aroon_dn
    except ImportError:
        low = np.asarray(low, dtype=float)
        n = len(low)
        result = np.full(n, np.nan)
        for i in range(timeperiod, n):
            window = low[i - timeperiod:i + 1]
            periods_since_low = timeperiod - np.argmin(window)
            result[i] = 100.0 * (timeperiod - periods_since_low) / timeperiod
        return result


def aroon_oscillator(high, low, timeperiod=25):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Trend Indicators', 'Aroon']
    function: "Computes the Aroon Oscillator: AroonOsc = AroonUp - AroonDown."
    y_as_x: []
    :param high: "Array of high prices"
    :param low: "Array of low prices"
    :param timeperiod: "Lookback period (default 25)"
    :return: "Aroon Oscillator values as numpy array"
    '''
    try:
        import talib
        return talib.AROONOSC(high, low, timeperiod=timeperiod)
    except ImportError:
        high = np.asarray(high, dtype=float)
        low = np.asarray(low, dtype=float)
        n = len(high)
        result = np.full(n, np.nan)
        for i in range(timeperiod, n):
            high_window = high[i - timeperiod:i + 1]
            low_window = low[i - timeperiod:i + 1]
            periods_since_high = timeperiod - np.argmax(high_window)
            periods_since_low = timeperiod - np.argmin(low_window)
            aroon_up_val = 100.0 * (timeperiod - periods_since_high) / timeperiod
            aroon_dn_val = 100.0 * (timeperiod - periods_since_low) / timeperiod
            result[i] = aroon_up_val - aroon_dn_val
        return result


def aroon_up(high, low, timeperiod=25):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Trend Indicators', 'Aroon']
    function: "Computes Aroon Up: AroonUp = 100 * (n - periods since n-period high) / n."
    y_as_x: ['aroon_oscillator']
    :param high: "Array of high prices"
    :param low: "Array of low prices"
    :param timeperiod: "Lookback period (default 25)"
    :return: "Aroon Up values as numpy array"
    '''
    try:
        import talib
        _, aroon_u = talib.AROON(high, low, timeperiod=timeperiod)
        return aroon_u
    except ImportError:
        high = np.asarray(high, dtype=float)
        n = len(high)
        result = np.full(n, np.nan)
        for i in range(timeperiod, n):
            window = high[i - timeperiod:i + 1]
            periods_since_high = timeperiod - np.argmax(window)
            result[i] = 100.0 * (timeperiod - periods_since_high) / timeperiod
        return result


def arrival_price_slippage(executed_price, arrival_price):
    '''
    domain: ['Trading, execution & market microstructure']
    subdomain: ['Execution Cost', 'Transaction Cost Analysis']
    function: "Computes arrival price slippage: the difference between the executed price and the arrival (decision) price."
    y_as_x: ['implementation_shortfall']
    :param executed_price: "Average execution price of the order"
    :param arrival_price: "Price at the time the order was decided (arrival/decision price)"
    :return: "Slippage = Executed Price - Arrival Price"
    '''
    return executed_price - arrival_price


def asian_option_price(spot, strike, rate, volatility, time_to_maturity, n_averaging=12, option_type='call',
                       dividend_yield=0.0, n_simulations=50000, seed=42):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Exotic Options', 'Asian Options']
    function: "Prices an Asian (average price) option using Monte Carlo simulation: V = E_Q[e^{-rT}(average(S) - K)^+]."
    y_as_x: []
    :param spot: "Current price of the underlying"
    :param strike: "Strike price"
    :param rate: "Risk-free rate (annualized)"
    :param volatility: "Annualized volatility"
    :param time_to_maturity: "Time to maturity in years"
    :param n_averaging: "Number of averaging dates"
    :param option_type: "'call' or 'put'"
    :param dividend_yield: "Continuous dividend yield"
    :param n_simulations: "Number of MC paths"
    :param seed: "Random seed"
    :return: "Asian option price"
    '''
    rng = np.random.default_rng(seed)
    dt = time_to_maturity / n_averaging
    drift = (rate - dividend_yield - 0.5 * volatility ** 2) * dt
    diffusion = volatility * np.sqrt(dt)
    z = rng.standard_normal((n_simulations, n_averaging))
    log_returns = drift + diffusion * z
    log_paths = np.cumsum(log_returns, axis=1)
    paths = spot * np.exp(log_paths)
    avg_prices = np.mean(paths, axis=1)
    if option_type == 'call':
        payoffs = np.maximum(avg_prices - strike, 0.0)
    else:
        payoffs = np.maximum(strike - avg_prices, 0.0)
    return np.exp(-rate * time_to_maturity) * np.mean(payoffs)


def asset_swap_spread(bond_coupon_rate, par_swap_rate, bond_dirty_price, face_value=100.0):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Credit Markets', 'Relative Value']
    function: "Computes the asset swap spread: the spread over the floating rate that equates the asset swap package to par."
    y_as_x: []
    :param bond_coupon_rate: "Annual coupon rate of the bond"
    :param par_swap_rate: "Par swap rate for the matching maturity"
    :param bond_dirty_price: "Dirty price of the bond (as percentage of face)"
    :param face_value: "Face value of the bond (default 100)"
    :return: "Asset swap spread in basis points"
    '''
    # Simplified: ASW spread ~ (coupon - swap_rate) + (par - dirty_price) / duration
    # Common approximation
    asw = (bond_coupon_rate - par_swap_rate) + (face_value - bond_dirty_price) / face_value
    return asw


def asset_turnover(revenue, average_total_assets):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Efficiency Ratios', 'Financial Analysis']
    function: "Computes the asset turnover ratio: Revenue / Average Total Assets. Measures how efficiently assets generate revenue."
    y_as_x: ['altman_z_score', 'return_on_assets_roa']
    :param revenue: "Total revenue (net sales)"
    :param average_total_assets: "Average total assets over the period"
    :return: "Asset turnover ratio"
    '''
    return revenue / average_total_assets


def average_loan_age(loan_ages, loan_balances):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['MBS/ABS Analytics', 'Pool Characteristics']
    function: "Computes the weighted average loan age (seasoning) of a pool of loans."
    y_as_x: []
    :param loan_ages: "Array of individual loan ages (in months)"
    :param loan_balances: "Array of individual loan outstanding balances"
    :return: "Weighted average loan age"
    '''
    loan_ages = np.asarray(loan_ages, dtype=float)
    loan_balances = np.asarray(loan_balances, dtype=float)
    return np.sum(loan_ages * loan_balances) / np.sum(loan_balances)


def average_true_range_atr(high, low, close, timeperiod=14):
    '''
    domain: ['Technical analysis']
    subdomain: ['Volatility Indicators', 'True Range']
    function: "Computes the Average True Range (ATR), measuring market volatility as a smoothed average of the true range."
    y_as_x: ['keltner_channel_lower', 'keltner_channel_upper']
    :param high: "Array of high prices"
    :param low: "Array of low prices"
    :param close: "Array of closing prices"
    :param timeperiod: "Smoothing period (default 14)"
    :return: "ATR values as numpy array"
    '''
    try:
        import talib
        return talib.ATR(high, low, close, timeperiod=timeperiod)
    except ImportError:
        high = np.asarray(high, dtype=float)
        low = np.asarray(low, dtype=float)
        close = np.asarray(close, dtype=float)
        n = len(close)
        tr = np.zeros(n)
        tr[0] = high[0] - low[0]
        for i in range(1, n):
            tr[i] = max(high[i] - low[i], abs(high[i] - close[i - 1]), abs(low[i] - close[i - 1]))
        atr_arr = np.full(n, np.nan)
        atr_arr[timeperiod - 1] = np.mean(tr[:timeperiod])
        for i in range(timeperiod, n):
            atr_arr[i] = (atr_arr[i - 1] * (timeperiod - 1) + tr[i]) / timeperiod
        return atr_arr


def awesome_oscillator(high, low, short_period=5, long_period=34):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Momentum Indicators', 'Oscillators']
    function: "Computes the Awesome Oscillator: AO = SMA_5(MedianPrice) - SMA_34(MedianPrice)."
    y_as_x: []
    :param high: "Array of high prices"
    :param low: "Array of low prices"
    :param short_period: "Short SMA period (default 5)"
    :param long_period: "Long SMA period (default 34)"
    :return: "Awesome Oscillator values as numpy array"
    '''
    high = np.asarray(high, dtype=float)
    low = np.asarray(low, dtype=float)
    median_price = (high + low) / 2.0
    # Compute SMAs manually
    n = len(median_price)
    sma_short = np.full(n, np.nan)
    sma_long = np.full(n, np.nan)
    for i in range(short_period - 1, n):
        sma_short[i] = np.mean(median_price[i - short_period + 1:i + 1])
    for i in range(long_period - 1, n):
        sma_long[i] = np.mean(median_price[i - long_period + 1:i + 1])
    return sma_short - sma_long


def bachelier_option_price(forward, strike, volatility, time_to_maturity, discount_factor, option_type='call'):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Option Pricing', 'Normal Model']
    function: "Computes the Bachelier (normal model) option price: Price = DF[(F-K)N(d) + sigma*sqrt(T)*n(d)]."
    y_as_x: []
    :param forward: "Forward price of the underlying (F)"
    :param strike: "Strike price (K)"
    :param volatility: "Normal (Bachelier) volatility in price terms (sigma)"
    :param time_to_maturity: "Time to expiration in years (T)"
    :param discount_factor: "Discount factor from option expiry to valuation date"
    :param option_type: "'call' or 'put'"
    :return: "Bachelier option price"
    '''
    sigma_sqrt_t = volatility * np.sqrt(time_to_maturity)
    if sigma_sqrt_t == 0:
        if option_type == 'call':
            return discount_factor * max(forward - strike, 0.0)
        else:
            return discount_factor * max(strike - forward, 0.0)
    d = (forward - strike) / sigma_sqrt_t
    if option_type == 'call':
        price = discount_factor * ((forward - strike) * stats.norm.cdf(d) + sigma_sqrt_t * stats.norm.pdf(d))
    else:
        price = discount_factor * ((strike - forward) * stats.norm.cdf(-d) + sigma_sqrt_t * stats.norm.pdf(d))
    return price


def back_end_dti_gross_income(total_monthly_debt_payments, gross_monthly_income):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Consumer Lending', 'Underwriting Ratios']
    function: "Computes the back-end debt-to-income ratio using gross income: DTI = Total Monthly Debt Payments / Gross Monthly Income."
    y_as_x: []
    :param total_monthly_debt_payments: "Sum of all monthly debt obligations (mortgage, car, credit cards, etc.)"
    :param gross_monthly_income: "Gross monthly income before taxes"
    :return: "Back-end DTI ratio (gross)"
    '''
    return total_monthly_debt_payments / gross_monthly_income


def back_end_dti_net_income(total_monthly_debt_payments, net_monthly_income):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Consumer Lending', 'Underwriting Ratios']
    function: "Computes the back-end debt-to-income ratio using net income: DTI = Total Monthly Debt Payments / Net Monthly Income."
    y_as_x: []
    :param total_monthly_debt_payments: "Sum of all monthly debt obligations"
    :param net_monthly_income: "Net monthly income after taxes"
    :return: "Back-end DTI ratio (net)"
    '''
    return total_monthly_debt_payments / net_monthly_income


def backtesting_exception_rate(exceptions, total_observations):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Risk Model Validation', 'Backtesting']
    function: "Computes the backtesting exception rate for VaR models: number of exceptions divided by total observations."
    y_as_x: ['kupiec_pof_likelihood_ratio']
    :param exceptions: "Number of VaR breaches (days where loss exceeded VaR)"
    :param total_observations: "Total number of backtesting observations"
    :return: "Exception rate = exceptions / observations"
    '''
    return exceptions / total_observations


def backwardation_slope(futures_long, futures_short):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Futures Markets', 'Term Structure']
    function: "Computes the backwardation slope of a futures curve: Backwardation = 1 - F_long / F_short."
    y_as_x: []
    :param futures_long: "Price of the longer-dated futures contract (F_long)"
    :param futures_short: "Price of the shorter-dated futures contract (F_short)"
    :return: "Backwardation slope; positive indicates backwardation, negative indicates contango"
    '''
    return 1.0 - futures_long / futures_short


def balloon_payment(rate, n_amortization_periods, n_payment_periods, loan_amount):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Loan Structures', 'Balloon Loans']
    function: "Computes the balloon payment: the outstanding balance at maturity for a loan with a shorter term than amortization schedule."
    y_as_x: []
    :param rate: "Periodic interest rate"
    :param n_amortization_periods: "Number of periods for the amortization schedule"
    :param n_payment_periods: "Number of actual payment periods before balloon"
    :param loan_amount: "Original loan amount"
    :return: "Balloon payment (outstanding balance at maturity)"
    '''
    try:
        import numpy_financial as npf
        pmt = npf.pmt(rate, n_amortization_periods, -loan_amount)
        balance = npf.fv(rate, n_payment_periods, -pmt, -loan_amount)
        return balance
    except ImportError:
        if rate == 0:
            pmt = loan_amount / n_amortization_periods
            return loan_amount - pmt * n_payment_periods
        pmt = loan_amount * rate * (1 + rate) ** n_amortization_periods / ((1 + rate) ** n_amortization_periods - 1)
        balance = loan_amount * (1 + rate) ** n_payment_periods - pmt * ((1 + rate) ** n_payment_periods - 1) / rate
        return balance


def barrier_option_price(spot, strike, barrier, rate, volatility, time_to_maturity, option_type='call',
                         barrier_type='down-and-out', dividend_yield=0.0, n_simulations=50000, seed=42):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Exotic Options', 'Barrier Options']
    function: "Prices a barrier option using Monte Carlo simulation. Supports down-and-out, down-and-in, up-and-out, up-and-in barriers."
    y_as_x: []
    :param spot: "Current price of the underlying"
    :param strike: "Strike price"
    :param barrier: "Barrier level"
    :param rate: "Risk-free rate"
    :param volatility: "Annualized volatility"
    :param time_to_maturity: "Time to maturity in years"
    :param option_type: "'call' or 'put'"
    :param barrier_type: "'down-and-out', 'down-and-in', 'up-and-out', or 'up-and-in'"
    :param dividend_yield: "Continuous dividend yield"
    :param n_simulations: "Number of MC paths"
    :param seed: "Random seed"
    :return: "Barrier option price"
    '''
    rng = np.random.default_rng(seed)
    n_steps = 252
    dt = time_to_maturity / n_steps
    drift = (rate - dividend_yield - 0.5 * volatility ** 2) * dt
    diffusion = volatility * np.sqrt(dt)
    z = rng.standard_normal((n_simulations, n_steps))
    log_returns = drift + diffusion * z
    log_paths = np.log(spot) + np.cumsum(log_returns, axis=1)
    paths = np.exp(log_paths)
    paths = np.column_stack([np.full(n_simulations, spot), paths])
    final_prices = paths[:, -1]
    if option_type == 'call':
        payoffs = np.maximum(final_prices - strike, 0.0)
    else:
        payoffs = np.maximum(strike - final_prices, 0.0)
    min_prices = np.min(paths, axis=1)
    max_prices = np.max(paths, axis=1)
    if barrier_type == 'down-and-out':
        knocked = min_prices <= barrier
        payoffs[knocked] = 0.0
    elif barrier_type == 'down-and-in':
        not_knocked = min_prices > barrier
        payoffs[not_knocked] = 0.0
    elif barrier_type == 'up-and-out':
        knocked = max_prices >= barrier
        payoffs[knocked] = 0.0
    elif barrier_type == 'up-and-in':
        not_knocked = max_prices < barrier
        payoffs[not_knocked] = 0.0
    return np.exp(-rate * time_to_maturity) * np.mean(payoffs)


def basel_irb_capital_requirement(pd, lgd, maturity, ead, asset_correlation=None):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Basel Regulation', 'Credit Risk Capital']
    function: "Computes the Basel II/III IRB capital requirement: K = LGD * [Phi((Phi^-1(PD) + sqrt(R)*Phi^-1(0.999))/sqrt(1-R)) - PD] * MA."
    y_as_x: []
    :param pd: "Probability of default (PD)"
    :param lgd: "Loss given default (LGD) as decimal"
    :param maturity: "Effective maturity in years"
    :param ead: "Exposure at default"
    :param asset_correlation: "Asset correlation R (if None, uses Basel corporate formula)"
    :return: "Capital requirement amount"
    '''
    if asset_correlation is None:
        # Basel corporate correlation formula
        r = 0.12 * (1 - np.exp(-50 * pd)) / (1 - np.exp(-50)) + \
            0.24 * (1 - (1 - np.exp(-50 * pd)) / (1 - np.exp(-50)))
    else:
        r = asset_correlation
    # Maturity adjustment
    b = (0.11852 - 0.05478 * np.log(pd)) ** 2
    ma = (1 + (maturity - 2.5) * b) / (1 - 1.5 * b)
    # Capital requirement per unit EAD
    norm_inv_pd = stats.norm.ppf(pd)
    norm_inv_999 = stats.norm.ppf(0.999)
    conditional_pd = stats.norm.cdf((norm_inv_pd + np.sqrt(r) * norm_inv_999) / np.sqrt(1 - r))
    k = lgd * (conditional_pd - pd) * ma
    return k * ead


def basel_standardized_capital_requirement(risk_weighted_assets):
    '''
    domain: ['Bank regulation, Basel & prudential ratios']
    subdomain: ['Basel Regulation', 'Capital Requirements']
    function: "Computes the Basel standardized capital requirement: Capital = 8% x RWA."
    y_as_x: []
    :param risk_weighted_assets: "Total risk-weighted assets"
    :return: "Minimum capital requirement = 0.08 * RWA"
    '''
    return 0.08 * risk_weighted_assets


def basis(spot_price, futures_price):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Futures Markets', 'Basis Trading']
    function: "Computes the basis: Basis = Spot Price - Futures Price."
    y_as_x: ['basis_convergence', 'minimum_variance_hedge_ratio']
    :param spot_price: "Current spot price of the commodity"
    :param futures_price: "Current futures price"
    :return: "Basis = S_t - F_t"
    '''
    return spot_price - futures_price


def basis_convergence(spot_price, futures_price, time_to_maturity, tolerance=1e-6):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Futures Markets', 'Basis Risk']
    function: "Models basis convergence toward zero at futures maturity, assuming linear convergence."
    y_as_x: []
    :param spot_price: "Current spot price"
    :param futures_price: "Current futures price"
    :param time_to_maturity: "Time to maturity in years (0 means at maturity)"
    :param tolerance: "Convergence tolerance"
    :return: "Expected basis at maturity (should approach 0)"
    '''
    current_basis = spot_price - futures_price
    if time_to_maturity <= tolerance:
        return 0.0
    return current_basis * time_to_maturity


def batting_average(portfolio_returns, benchmark_returns):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Performance Metrics', 'Hit Rate']
    function: "Computes the batting average: the fraction of periods where the portfolio outperformed the benchmark."
    y_as_x: []
    :param portfolio_returns: "Array of portfolio returns"
    :param benchmark_returns: "Array of benchmark returns"
    :return: "Batting average = count(alpha_t > 0) / T"
    '''
    portfolio_returns = np.asarray(portfolio_returns, dtype=float)
    benchmark_returns = np.asarray(benchmark_returns, dtype=float)
    active = portfolio_returns - benchmark_returns
    return np.sum(active > 0) / len(active)


def bayesian_shrinkage_return_forecast(mu_prior, mu_sample, shrinkage_lambda):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Return Forecasting', 'Bayesian Methods']
    function: "Computes a Bayesian shrinkage return forecast as a weighted average of prior and sample means."
    y_as_x: ['black_litterman_posterior_mean']
    :param mu_prior: "Prior expected return (or array of prior returns)"
    :param mu_sample: "Sample (historical) expected return (or array)"
    :param shrinkage_lambda: "Shrinkage weight on the prior, between 0 and 1"
    :return: "Shrunk return forecast = lambda * mu_prior + (1-lambda) * mu_sample"
    '''
    mu_prior = np.asarray(mu_prior, dtype=float)
    mu_sample = np.asarray(mu_sample, dtype=float)
    return shrinkage_lambda * mu_prior + (1 - shrinkage_lambda) * mu_sample


def behavioral_duration_of_deposits(rate_changes, deposit_balance_changes):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Asset-Liability Management', 'Non-Maturity Deposits']
    function: "Estimates the behavioral (effective) duration of non-maturity deposits using regression of deposit balance changes on rate changes."
    y_as_x: ['duration_gap']
    :param rate_changes: "Array of interest rate changes (independent variable)"
    :param deposit_balance_changes: "Array of percentage changes in deposit balances"
    :return: "Dictionary with 'duration' (negative of regression slope), 'r_squared', and 'model'"
    '''
    import statsmodels.api as sm
    X = sm.add_constant(np.asarray(rate_changes, dtype=float))
    y = np.asarray(deposit_balance_changes, dtype=float)
    model = sm.OLS(y, X).fit()
    duration = -model.params[1]
    return {'duration': duration, 'r_squared': model.rsquared, 'model': model}


def benchmark_relative_optimization(expected_returns, cov_matrix, benchmark_weights, risk_aversion=1.0):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Optimization', 'Benchmark-Relative']
    function: "Solves the benchmark-relative optimization: min_w (w-w_b)'Sigma(w-w_b) - lambda*mu'(w-w_b), subject to weights summing to 1."
    y_as_x: []
    :param expected_returns: "Array of expected returns for each asset"
    :param cov_matrix: "Covariance matrix of asset returns"
    :param benchmark_weights: "Array of benchmark weights"
    :param risk_aversion: "Risk aversion parameter (lambda)"
    :return: "Optimal portfolio weights"
    '''
    try:
        import cvxpy as cp
        n = len(expected_returns)
        w = cp.Variable(n)
        mu = np.asarray(expected_returns, dtype=float)
        Sigma = np.asarray(cov_matrix, dtype=float)
        wb = np.asarray(benchmark_weights, dtype=float)
        active = w - wb
        objective = cp.Minimize(cp.quad_form(active, Sigma) - risk_aversion * mu @ active)
        constraints = [cp.sum(w) == 1, w >= 0]
        prob = cp.Problem(objective, constraints)
        prob.solve()
        return np.array(w.value).flatten()
    except ImportError:
        # Analytical solution without constraints (unconstrained)
        mu = np.asarray(expected_returns, dtype=float)
        Sigma = np.asarray(cov_matrix, dtype=float)
        wb = np.asarray(benchmark_weights, dtype=float)
        Sigma_inv = np.linalg.inv(Sigma)
        w_star = wb + 0.5 * risk_aversion * Sigma_inv @ mu
        return w_star / np.sum(w_star)


def benefit_reserve_recursion(reserve_t, premium, interest_rate, mortality_rate, benefit):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Life Insurance', 'Reserve Valuation']
    function: "Computes the next-period benefit reserve using the recursion: (V_t + P)(1+i) = q*Benefit + p*V_{t+1}, solving for V_{t+1}."
    y_as_x: ['prospective_reserve', 'retrospective_reserve']
    :param reserve_t: "Reserve at time t (V_t)"
    :param premium: "Premium collected at time t (P)"
    :param interest_rate: "Interest rate per period (i)"
    :param mortality_rate: "Probability of death in period t (q)"
    :param benefit: "Death benefit amount"
    :return: "Reserve at time t+1 (V_{t+1})"
    '''
    p = 1.0 - mortality_rate
    accumulated = (reserve_t + premium) * (1 + interest_rate)
    reserve_next = (accumulated - mortality_rate * benefit) / p
    return reserve_next


def beneish_m_score(dsri, gmi, aqi, sgi, depi, sgai, tata, lvgi):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Earnings Quality', 'Fraud Detection']
    function: "Computes the Beneish M-score for detecting earnings manipulation: M = -4.84 + 0.92*DSRI + 0.528*GMI + 0.404*AQI + 0.892*SGI + 0.115*DEPI - 0.172*SGAI + 4.679*TATA - 0.327*LVGI."
    y_as_x: []
    :param dsri: "Days Sales in Receivables Index"
    :param gmi: "Gross Margin Index"
    :param aqi: "Asset Quality Index"
    :param sgi: "Sales Growth Index"
    :param depi: "Depreciation Index"
    :param sgai: "Selling, General & Administrative expenses Index"
    :param tata: "Total Accruals to Total Assets"
    :param lvgi: "Leverage Index"
    :return: "Beneish M-score; values > -1.78 suggest possible earnings manipulation"
    '''
    return (-4.84 + 0.92 * dsri + 0.528 * gmi + 0.404 * aqi +
            0.892 * sgi + 0.115 * depi - 0.172 * sgai +
            4.679 * tata - 0.327 * lvgi)


def beta(returns, factor_returns, risk_free_rate=0.0):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Asset Pricing', 'CAPM']
    function: "Computes the CAPM beta: beta_i = Cov(R_i, R_m) / Var(R_m)."
    y_as_x: ['alpha', 'capm_expected_return', 'cost_of_equity_capm', 'garch_11',  'levered_beta_hamada', 'probability_of_default_from_logit', 'probit_score', 'sabr_implied_vol', 'security_market_line', 'treynor_ratio', 'unlevered_beta','henriksson_merton_timing']
    :param returns: "Array of asset returns"
    :param factor_returns: "Array of market (benchmark) returns"
    :param risk_free_rate: "Risk-free rate per period (default 0)"
    :return: "Beta coefficient"
    '''
    try:
        import empyrical
        return empyrical.beta(returns, factor_returns, risk_free=risk_free_rate)
    except ImportError:
        returns = np.asarray(returns, dtype=float)
        factor_returns = np.asarray(factor_returns, dtype=float)
        cov_matrix = np.cov(returns, factor_returns)
        return cov_matrix[0, 1] / cov_matrix[1, 1]


def bid_ask_spread(ask_price, bid_price):
    '''
    domain: ['Liquidity risk & market liquidity']
    subdomain: ['Market Microstructure', 'Liquidity Measurement']
    function: "Computes the bid-ask spread: Spread = Ask - Bid."
    y_as_x: ['effective_spread', 'quoted_spread_pct', 'relative_spread', 'mid_price', 'adverse_selection_cost']
    :param ask_price: "Best ask (offer) price"
    :param bid_price: "Best bid price"
    :return: "Bid-ask spread = Ask - Bid"
    '''
    return ask_price - bid_price


def binary_asset_or_nothing_call(spot, strike, rate, volatility, time_to_maturity, dividend_yield=0.0):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Exotic Options', 'Binary Options']
    function: "Prices a binary asset-or-nothing call option: AON = S * e^{-qT} * N(d1)."
    y_as_x: []
    :param spot: "Current price of the underlying (S)"
    :param strike: "Strike price (K)"
    :param rate: "Risk-free rate (r)"
    :param volatility: "Annualized volatility (sigma)"
    :param time_to_maturity: "Time to expiration in years (T)"
    :param dividend_yield: "Continuous dividend yield (q)"
    :return: "Binary asset-or-nothing call price"
    '''
    d1 = (np.log(spot / strike) + (rate - dividend_yield + 0.5 * volatility ** 2) * time_to_maturity) / \
         (volatility * np.sqrt(time_to_maturity))
    return spot * np.exp(-dividend_yield * time_to_maturity) * stats.norm.cdf(d1)


def binomial_down_factor(up_factor):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Option Pricing', 'Binomial Models']
    function: "Computes the binomial down factor: d = 1/u."
    y_as_x: ['binomial_option_pricing', 'american_option_binomial_pricing']
    :param up_factor: "Binomial up factor (u)"
    :return: "Down factor d = 1/u"
    '''
    return 1.0 / up_factor


def binomial_option_pricing(spot, strike, rate, volatility, time_to_maturity, steps=100, option_type='call',
                            dividend_yield=0.0):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Option Pricing', 'Binomial Models']
    function: "Prices a European option using the CRR binomial tree: V = e^{-r*dt}[p*V_u + (1-p)*V_d]."
    y_as_x: ['american_option_binomial_pricing']
    :param spot: "Current price of the underlying"
    :param strike: "Strike price"
    :param rate: "Risk-free rate"
    :param volatility: "Annualized volatility"
    :param time_to_maturity: "Time to maturity in years"
    :param steps: "Number of binomial steps (default 100)"
    :param option_type: "'call' or 'put'"
    :param dividend_yield: "Continuous dividend yield (default 0)"
    :return: "European option price"
    '''
    dt = time_to_maturity / steps
    u = np.exp(volatility * np.sqrt(dt))
    d = 1.0 / u
    disc = np.exp(-rate * dt)
    p = (np.exp((rate - dividend_yield) * dt) - d) / (u - d)
    # Terminal payoffs
    asset_prices = spot * u ** np.arange(steps, -1, -1) * d ** np.arange(0, steps + 1)
    if option_type == 'call':
        option_values = np.maximum(asset_prices - strike, 0.0)
    else:
        option_values = np.maximum(strike - asset_prices, 0.0)
    # Backward induction (European, no early exercise)
    for i in range(steps):
        option_values = disc * (p * option_values[:-1] + (1 - p) * option_values[1:])
    return option_values[0]


def binomial_up_factor(volatility, dt):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Option Pricing', 'Binomial Models']
    function: "Computes the CRR binomial up factor: u = e^{sigma * sqrt(dt)}."
    y_as_x: ['binomial_down_factor', 'binomial_option_pricing', 'american_option_binomial_pricing']
    :param volatility: "Annualized volatility (sigma)"
    :param dt: "Time step size (Delta t) in years"
    :return: "Up factor u = exp(sigma * sqrt(dt))"
    '''
    return np.exp(volatility * np.sqrt(dt))


def bipower_variation(returns):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Realized Volatility', 'Jump Detection']
    function: "Computes bipower variation: BV = mu_1^{-2} * sum |r_i| * |r_{i-1}|, used to estimate integrated variance robust to jumps."
    y_as_x: []
    :param returns: "Array of high-frequency returns"
    :return: "Bipower variation estimate"
    '''
    returns = np.asarray(returns, dtype=float)
    mu_1 = np.sqrt(2.0 / np.pi)
    n = len(returns)
    bv = (1.0 / mu_1 ** 2) * np.sum(np.abs(returns[1:]) * np.abs(returns[:-1])) * n / (n - 1)
    return bv


def black_76_option_price(forward, strike, volatility, time_to_maturity, rate, option_type='call'):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Option Pricing', 'Black 76 Model']
    function: "Prices a European option on a forward/futures using the Black-76 model: Price = DF[F*N(d1) - K*N(d2)] for call."
    y_as_x: ['black_76_commodity_option', 'black_caplet_price', 'black_swaption_price']
    :param forward: "Forward price (F)"
    :param strike: "Strike price (K)"
    :param volatility: "Annualized volatility (sigma)"
    :param time_to_maturity: "Time to expiration in years (T)"
    :param rate: "Risk-free rate for discounting"
    :param option_type: "'call' or 'put'"
    :return: "Black-76 option price"
    '''
    try:
        from py_vollib.black import black
        flag = 'c' if option_type == 'call' else 'p'
        return black.black(flag, forward, strike, time_to_maturity, rate, volatility)
    except (ImportError, Exception):
        df = np.exp(-rate * time_to_maturity)
        sqrt_t = np.sqrt(time_to_maturity)
        d1 = (np.log(forward / strike) + 0.5 * volatility ** 2 * time_to_maturity) / (volatility * sqrt_t)
        d2 = d1 - volatility * sqrt_t
        if option_type == 'call':
            return df * (forward * stats.norm.cdf(d1) - strike * stats.norm.cdf(d2))
        else:
            return df * (strike * stats.norm.cdf(-d2) - forward * stats.norm.cdf(-d1))


def black_caplet_price(forward_rate, strike_rate, volatility, time_to_expiry, discount_factor, tenor):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Interest Rate Derivatives', 'Caps & Floors']
    function: "Prices a caplet using Black's model: Caplet = DF * tau * [F*N(d1) - K*N(d2)]."
    y_as_x: []
    :param forward_rate: "Forward LIBOR/reference rate (F)"
    :param strike_rate: "Cap strike rate (K)"
    :param volatility: "Black (lognormal) volatility of the forward rate"
    :param time_to_expiry: "Time to caplet expiry in years"
    :param discount_factor: "Discount factor from payment date to valuation date"
    :param tenor: "Accrual period length in years (tau, e.g., 0.25 for quarterly)"
    :return: "Caplet price"
    '''
    sqrt_t = np.sqrt(time_to_expiry)
    d1 = (np.log(forward_rate / strike_rate) + 0.5 * volatility ** 2 * time_to_expiry) / (volatility * sqrt_t)
    d2 = d1 - volatility * sqrt_t
    return discount_factor * tenor * (forward_rate * stats.norm.cdf(d1) - strike_rate * stats.norm.cdf(d2))


def black_swaption_price(swap_rate, strike_rate, volatility, time_to_expiry, annuity_factor, option_type='payer'):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Interest Rate Derivatives', 'Swaptions']
    function: "Prices a swaption using Black's model: Swaption = A * [S*N(d1) - K*N(d2)] for payer."
    y_as_x: []
    :param swap_rate: "Forward swap rate (S)"
    :param strike_rate: "Swaption strike rate (K)"
    :param volatility: "Black (lognormal) volatility of the swap rate"
    :param time_to_expiry: "Time to swaption expiry in years"
    :param annuity_factor: "Present value of a basis point (swap annuity, A)"
    :param option_type: "'payer' (call on rates) or 'receiver' (put on rates)"
    :return: "Swaption price"
    '''
    sqrt_t = np.sqrt(time_to_expiry)
    d1 = (np.log(swap_rate / strike_rate) + 0.5 * volatility ** 2 * time_to_expiry) / (volatility * sqrt_t)
    d2 = d1 - volatility * sqrt_t
    if option_type == 'payer':
        return annuity_factor * (swap_rate * stats.norm.cdf(d1) - strike_rate * stats.norm.cdf(d2))
    else:
        return annuity_factor * (strike_rate * stats.norm.cdf(-d2) - swap_rate * stats.norm.cdf(-d1))


def black_76_commodity_option(forward, strike, volatility, time_to_maturity, rate, option_type='call'):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Commodity Derivatives', 'Option Pricing']
    function: "Prices a commodity option using Black-76: C = e^{-rT}[F*N(d1) - K*N(d2)]."
    y_as_x: []
    :param forward: "Forward commodity price (F)"
    :param strike: "Strike price (K)"
    :param volatility: "Annualized volatility (sigma)"
    :param time_to_maturity: "Time to expiration in years (T)"
    :param rate: "Risk-free rate"
    :param option_type: "'call' or 'put'"
    :return: "Black-76 commodity option price"
    '''
    return black_76_option_price(forward, strike, volatility, time_to_maturity, rate, option_type)


def black_litterman_implied_equilibrium_returns(risk_aversion, cov_matrix, market_weights):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Optimization', 'Black-Litterman']
    function: "Computes the Black-Litterman implied equilibrium returns: Pi = delta * Sigma * w_mkt."
    y_as_x: ['black_litterman_posterior_mean']
    :param risk_aversion: "Risk aversion coefficient (delta)"
    :param cov_matrix: "Covariance matrix of asset returns (Sigma)"
    :param market_weights: "Market capitalization weights (w_mkt)"
    :return: "Implied equilibrium excess returns (Pi)"
    '''
    try:
        from pypfopt import black_litterman
        Sigma = np.asarray(cov_matrix, dtype=float)
        w_mkt = np.asarray(market_weights, dtype=float)
        return risk_aversion * Sigma @ w_mkt
    except ImportError:
        Sigma = np.asarray(cov_matrix, dtype=float)
        w_mkt = np.asarray(market_weights, dtype=float)
        return risk_aversion * Sigma @ w_mkt


def black_litterman_posterior_mean(tau, cov_matrix, pi, P, Q, omega):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Optimization', 'Black-Litterman']
    function: "Computes the Black-Litterman posterior mean: mu_BL = [(tau*Sigma)^-1 + P'*Omega^-1*P]^-1 * [(tau*Sigma)^-1*pi + P'*Omega^-1*Q]."
    y_as_x: []
    :param tau: "Scalar uncertainty parameter on equilibrium returns"
    :param cov_matrix: "Covariance matrix of asset returns (Sigma)"
    :param pi: "Prior equilibrium returns (Pi)"
    :param P: "Pick matrix linking views to assets (K x N)"
    :param Q: "View return vector (K x 1)"
    :param omega: "View uncertainty matrix (K x K, diagonal)"
    :return: "Posterior expected returns (mu_BL)"
    '''
    Sigma = np.asarray(cov_matrix, dtype=float)
    pi = np.asarray(pi, dtype=float)
    P = np.asarray(P, dtype=float)
    Q = np.asarray(Q, dtype=float)
    omega = np.asarray(omega, dtype=float)
    tau_sigma_inv = np.linalg.inv(tau * Sigma)
    omega_inv = np.linalg.inv(omega)
    posterior_precision = tau_sigma_inv + P.T @ omega_inv @ P
    posterior_cov = np.linalg.inv(posterior_precision)
    mu_bl = posterior_cov @ (tau_sigma_inv @ pi + P.T @ omega_inv @ Q)
    return mu_bl


def black_scholes_call(spot, strike, time_to_maturity, rate, volatility, dividend_yield=0.0):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Option Pricing', 'Black-Scholes']
    function: "Prices a European call using Black-Scholes: C = S*e^{-qT}*N(d1) - K*e^{-rT}*N(d2)."
    y_as_x: ['put_call_parity', 'delta_call', 'gamma', 'vega', 'theta', 'rho', 'implied_volatility']
    :param spot: "Current price of the underlying (S)"
    :param strike: "Strike price (K)"
    :param time_to_maturity: "Time to expiration in years (T)"
    :param rate: "Risk-free rate (r)"
    :param volatility: "Annualized volatility (sigma)"
    :param dividend_yield: "Continuous dividend yield (q, default 0)"
    :return: "Black-Scholes call price"
    '''
    d1 = black_scholes_merton_d1(spot, strike, time_to_maturity, rate, volatility, dividend_yield)
    d2 = black_scholes_merton_d2(d1, volatility, time_to_maturity)
    call = spot * np.exp(-dividend_yield * time_to_maturity) * stats.norm.cdf(d1) - \
           strike * np.exp(-rate * time_to_maturity) * stats.norm.cdf(d2)
    return call


def black_scholes_put(spot, strike, time_to_maturity, rate, volatility, dividend_yield=0.0):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Option Pricing', 'Black-Scholes']
    function: "Prices a European put using Black-Scholes: P = K*e^{-rT}*N(-d2) - S*e^{-qT}*N(-d1)."
    y_as_x: ['put_call_parity', 'delta_put', 'implied_volatility']
    :param spot: "Current price of the underlying (S)"
    :param strike: "Strike price (K)"
    :param time_to_maturity: "Time to expiration in years (T)"
    :param rate: "Risk-free rate (r)"
    :param volatility: "Annualized volatility (sigma)"
    :param dividend_yield: "Continuous dividend yield (q, default 0)"
    :return: "Black-Scholes put price"
    '''
    d1 = black_scholes_merton_d1(spot, strike, time_to_maturity, rate, volatility, dividend_yield)
    d2 = black_scholes_merton_d2(d1, volatility, time_to_maturity)
    put = strike * np.exp(-rate * time_to_maturity) * stats.norm.cdf(-d2) - \
          spot * np.exp(-dividend_yield * time_to_maturity) * stats.norm.cdf(-d1)
    return put


def black_scholes_merton_d1(spot, strike, time_to_maturity, rate, volatility, dividend_yield=0.0):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Option Pricing', 'Black-Scholes']
    function: "Computes d1 in the Black-Scholes-Merton formula: d1 = [ln(S/K) + (r-q+0.5*sigma^2)*T] / (sigma*sqrt(T))."
    y_as_x: ['black_scholes_merton_d2', 'black_scholes_call', 'black_scholes_put', 'delta_call', 'delta_put', 'gamma', 'vega', 'binary_asset_or_nothing_call']
    :param spot: "Current price of the underlying (S)"
    :param strike: "Strike price (K)"
    :param time_to_maturity: "Time to expiration in years (T)"
    :param rate: "Risk-free rate (r)"
    :param volatility: "Annualized volatility (sigma)"
    :param dividend_yield: "Continuous dividend yield (q, default 0)"
    :return: "d1 value"
    '''
    return (np.log(spot / strike) + (rate - dividend_yield + 0.5 * volatility ** 2) * time_to_maturity) / \
        (volatility * np.sqrt(time_to_maturity))


def black_scholes_merton_d2(d1_value, volatility, time_to_maturity):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Option Pricing', 'Black-Scholes']
    function: "Computes d2 in the Black-Scholes-Merton formula: d2 = d1 - sigma*sqrt(T)."
    y_as_x: ['black_scholes_call', 'black_scholes_put', 'digital_call_price', 'digital_put_price']
    :param d1_value: "Pre-computed d1 value"
    :param volatility: "Annualized volatility (sigma)"
    :param time_to_maturity: "Time to expiration in years (T)"
    :return: "d2 value"
    '''
    return d1_value - volatility * np.sqrt(time_to_maturity)


def bollinger_pctb(close, timeperiod=20, nbdevup=2, nbdevdn=2):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Volatility Indicators', 'Bollinger Bands']
    function: "Computes Bollinger %B: %B = (Price - Lower) / (Upper - Lower), measuring where price is relative to the bands."
    y_as_x: []
    :param close: "Array of closing prices"
    :param timeperiod: "SMA lookback period (default 20)"
    :param nbdevup: "Number of standard deviations for upper band (default 2)"
    :param nbdevdn: "Number of standard deviations for lower band (default 2)"
    :return: "Bollinger %B values as numpy array"
    '''
    try:
        import talib
        upper, middle, lower = talib.BBANDS(close, timeperiod=timeperiod, nbdevup=nbdevup, nbdevdn=nbdevdn)
    except ImportError:
        close = np.asarray(close, dtype=float)
        n = len(close)
        middle = np.full(n, np.nan)
        upper = np.full(n, np.nan)
        lower = np.full(n, np.nan)
        for i in range(timeperiod - 1, n):
            window = close[i - timeperiod + 1:i + 1]
            m = np.mean(window)
            s = np.std(window, ddof=0)
            middle[i] = m
            upper[i] = m + nbdevup * s
            lower[i] = m - nbdevdn * s
    band_width = upper - lower
    close = np.asarray(close, dtype=float)
    return np.where(band_width != 0, (close - lower) / band_width, np.nan)


def bollinger_bands_lower(close, timeperiod=20, nbdev=2):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Volatility Indicators', 'Bollinger Bands']
    function: "Computes the lower Bollinger Band: Lower = SMA_n - k*sigma_n."
    y_as_x: ['bollinger_pctb', 'bollinger_bandwidth']
    :param close: "Array of closing prices"
    :param timeperiod: "SMA lookback period (default 20)"
    :param nbdev: "Number of standard deviations (default 2)"
    :return: "Lower Bollinger Band values as numpy array"
    '''
    try:
        import talib
        _, _, lower = talib.BBANDS(close, timeperiod=timeperiod, nbdevdn=nbdev, nbdevup=nbdev)
        return lower
    except ImportError:
        close = np.asarray(close, dtype=float)
        n = len(close)
        result = np.full(n, np.nan)
        for i in range(timeperiod - 1, n):
            window = close[i - timeperiod + 1:i + 1]
            result[i] = np.mean(window) - nbdev * np.std(window, ddof=0)
        return result


def bollinger_bands_middle(close, timeperiod=20):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Volatility Indicators', 'Bollinger Bands']
    function: "Computes the middle Bollinger Band (simple moving average): Middle = SMA_n(P)."
    y_as_x: ['bollinger_bandwidth', 'bollinger_pctb']
    :param close: "Array of closing prices"
    :param timeperiod: "SMA lookback period (default 20)"
    :return: "Middle Bollinger Band (SMA) values as numpy array"
    '''
    try:
        import talib
        _, middle, _ = talib.BBANDS(close, timeperiod=timeperiod)
        return middle
    except ImportError:
        close = np.asarray(close, dtype=float)
        n = len(close)
        result = np.full(n, np.nan)
        for i in range(timeperiod - 1, n):
            result[i] = np.mean(close[i - timeperiod + 1:i + 1])
        return result


def bollinger_bands_upper(close, timeperiod=20, nbdev=2):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Volatility Indicators', 'Bollinger Bands']
    function: "Computes the upper Bollinger Band: Upper = SMA_n + k*sigma_n."
    y_as_x: ['bollinger_pctb', 'bollinger_bandwidth']
    :param close: "Array of closing prices"
    :param timeperiod: "SMA lookback period (default 20)"
    :param nbdev: "Number of standard deviations (default 2)"
    :return: "Upper Bollinger Band values as numpy array"
    '''
    try:
        import talib
        upper, _, _ = talib.BBANDS(close, timeperiod=timeperiod, nbdevup=nbdev, nbdevdn=nbdev)
        return upper
    except ImportError:
        close = np.asarray(close, dtype=float)
        n = len(close)
        result = np.full(n, np.nan)
        for i in range(timeperiod - 1, n):
            window = close[i - timeperiod + 1:i + 1]
            result[i] = np.mean(window) + nbdev * np.std(window, ddof=0)
        return result


def bollinger_bandwidth(close, timeperiod=20, nbdev=2):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Volatility Indicators', 'Bollinger Bands']
    function: "Computes Bollinger Bandwidth: Bandwidth = (Upper - Lower) / Middle."
    y_as_x: []
    :param close: "Array of closing prices"
    :param timeperiod: "SMA lookback period (default 20)"
    :param nbdev: "Number of standard deviations (default 2)"
    :return: "Bollinger Bandwidth values as numpy array"
    '''
    try:
        import talib
        upper, middle, lower = talib.BBANDS(close, timeperiod=timeperiod, nbdevup=nbdev, nbdevdn=nbdev)
    except ImportError:
        close = np.asarray(close, dtype=float)
        n = len(close)
        upper = np.full(n, np.nan)
        middle = np.full(n, np.nan)
        lower = np.full(n, np.nan)
        for i in range(timeperiod - 1, n):
            window = close[i - timeperiod + 1:i + 1]
            m = np.mean(window)
            s = np.std(window, ddof=0)
            middle[i] = m
            upper[i] = m + nbdev * s
            lower[i] = m - nbdev * s
    return np.where(middle != 0, (upper - lower) / middle, np.nan)


def bond_carry_and_roll(coupon_rate, financing_rate, face_value, roll_down_bps, duration, hold_period=1.0):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Bond Trading', 'Carry & Roll-Down']
    function: "Computes bond carry and roll return: Carry+Roll = coupon income + financing cost + curve roll-down."
    y_as_x: []
    :param coupon_rate: "Annual coupon rate of the bond"
    :param financing_rate: "Repo/financing rate (annualized)"
    :param face_value: "Face value of the bond"
    :param roll_down_bps: "Expected yield change from roll-down in basis points (positive = yield decline)"
    :param duration: "Modified duration of the bond"
    :param hold_period: "Holding period in years (default 1)"
    :return: "Total carry and roll return"
    '''
    coupon_income = coupon_rate * face_value * hold_period
    financing_cost = -financing_rate * face_value * hold_period
    roll_down_return = duration * roll_down_bps / 10000.0 * face_value
    return coupon_income + financing_cost + roll_down_return


def bond_equivalent_yield_bey(holding_period_yield, days_to_maturity):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Bond Yields', 'Yield Conventions']
    function: "Computes the Bond Equivalent Yield: BEY = 2 * [(1+HPY)^(182/d) - 1], converting a holding period yield to a semi-annual bond equivalent."
    y_as_x: []
    :param holding_period_yield: "Holding period yield (HPY) as decimal"
    :param days_to_maturity: "Number of days in the holding period"
    :return: "Bond equivalent yield (annualized, semi-annual basis)"
    '''
    return 2.0 * ((1 + holding_period_yield) ** (182.0 / days_to_maturity) - 1)


def bond_price(coupon_rate, face_value, yield_to_maturity, n_periods, frequency=2):
    '''
    domain: ['Fixed income & bond math']
    subdomain: ['Bond Pricing', 'Present Value']
    function: "Computes the clean bond price: P = sum C/(1+y/m)^t + FV/(1+y/m)^n."
    y_as_x: ['accrued_interest', 'bond_price_from_yield', 'clean_price', 'convexity', 'current_yield', 'dirty_price', 'macaulay_duration', 'modified_duration', 'option_adjusted_spread_oas', 'spread_duration', 'yield_to_maturity_ytm']
    :param coupon_rate: "Annual coupon rate (as decimal)"
    :param face_value: "Face (par) value of the bond"
    :param yield_to_maturity: "Annual yield to maturity (as decimal)"
    :param n_periods: "Total number of coupon periods"
    :param frequency: "Coupon payment frequency per year (default 2 for semi-annual)"
    :return: "Bond price"
    '''
    coupon = coupon_rate * face_value / frequency
    y = yield_to_maturity / frequency
    if y == 0:
        return coupon * n_periods + face_value
    pv_coupons = coupon * (1 - (1 + y) ** (-n_periods)) / y
    pv_face = face_value / (1 + y) ** n_periods
    return pv_coupons + pv_face


def bond_price_from_yield(coupon_rate, face_value, yield_to_maturity, n_periods, frequency=2):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Bond Pricing', 'Yield-Price Relationship']
    function: "Computes bond price from yield: P = sum C/(1+y/m)^t + F/(1+y/m)^T."
    y_as_x: ['approximate_price_change', 'duration_times_spread_dts']
    :param coupon_rate: "Annual coupon rate (as decimal)"
    :param face_value: "Face value"
    :param yield_to_maturity: "Annual yield to maturity"
    :param n_periods: "Total number of coupon periods"
    :param frequency: "Coupon frequency per year (default 2)"
    :return: "Bond price"
    '''
    return bond_price(coupon_rate, face_value, yield_to_maturity, n_periods, frequency)


def book_value_per_share(total_equity, shares_outstanding):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Per-Share Metrics', 'Equity Analysis']
    function: "Computes book value per share: BVPS = Total Equity / Shares Outstanding."
    y_as_x: ['book_to_market_ratio', 'p_over_b_ratio', 'price_to_book']
    :param total_equity: "Total shareholders' equity"
    :param shares_outstanding: "Number of shares outstanding"
    :return: "Book value per share"
    '''
    return total_equity / shares_outstanding


def book_to_market_ratio(book_equity, market_cap):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Valuation Ratios', 'Factor Investing']
    function: "Computes the book-to-market ratio: Book Equity / Market Cap. Key factor in Fama-French models."
    y_as_x: ['fama_french_3_factor_model', 'fama_french_5_factor_model']
    :param book_equity: "Book value of equity"
    :param market_cap: "Market capitalization"
    :return: "Book-to-market ratio"
    '''
    return book_equity / market_cap


def bornhuetter_ferguson_reserve(reported_losses, expected_ultimate_losses, pct_unreported):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Loss Reserving', 'Property & Casualty']
    function: "Computes the Bornhuetter-Ferguson reserve: Ultimate = Reported + Expected Ultimate * %Unreported."
    y_as_x: []
    :param reported_losses: "Currently reported (paid + case reserves) losses"
    :param expected_ultimate_losses: "A priori expected ultimate losses"
    :param pct_unreported: "Estimated percentage of losses still unreported (as decimal, e.g., 0.3 for 30%)"
    :return: "Bornhuetter-Ferguson ultimate loss estimate"
    '''
    return reported_losses + expected_ultimate_losses * pct_unreported


def borrowing_base(eligible_collateral, advance_rates):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Asset-Based Lending', 'Collateral Management']
    function: "Computes the borrowing base: sum of Eligible Collateral_i x Advance Rate_i across collateral categories."
    y_as_x: ['advance_rate']
    :param eligible_collateral: "Array of eligible collateral values by category"
    :param advance_rates: "Array of advance rates for each collateral category"
    :return: "Total borrowing base"
    '''
    eligible_collateral = np.asarray(eligible_collateral, dtype=float)
    advance_rates = np.asarray(advance_rates, dtype=float)
    return np.sum(eligible_collateral * advance_rates)


# ================================================================================
# BATCH 2
# ================================================================================

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
    if isinstance(returns, pd.DataFrame) and all(
            c in returns.columns for c in ['excess_return', 'MKT', 'SMB', 'HML', 'MOM']):
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
def charm(S, K, T, r, sigma, option_type='call', dT=1 / 365):
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
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == 'call':
        charm_val = -np.exp(-r * T) * (
                norm.pdf(d1) * (2 * r * T - d2 * sigma * np.sqrt(T)) / (2 * T * sigma * np.sqrt(T)))
    else:
        charm_val = -np.exp(-r * T) * (
                norm.pdf(d1) * (2 * r * T - d2 * sigma * np.sqrt(T)) / (2 * T * sigma * np.sqrt(T)))
        # For puts, charm has the same formula for the time-dependent part
        # but delta itself differs; the decay component is:
        charm_val = charm_val + r * np.exp(-r * T) * norm.cdf(-d1)
        # Correction: re-derive
    # More robust: numerical
    d1_1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d1_2 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * (T - dT)) / (sigma * np.sqrt(T - dT)) if T > dT else d1_1
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
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T_expire) / (sigma * np.sqrt(T_expire))
    d2 = d1 - sigma * np.sqrt(T_expire)
    y = (np.log(S / K) + (r - q) * T_expire + 0.5 * sigma ** 2 * T_choose) / (sigma * np.sqrt(T_choose))
    # Simple chooser = Call(S, K, T_expire) + Put(S, K*exp(-(r-q)*(T_expire-T_choose)), T_choose)
    # But standard decomposition:
    call_value = S * np.exp(-q * T_expire) * norm.cdf(d1) - K * np.exp(-r * T_expire) * norm.cdf(d2)
    # Put component via parity adjustment
    d1_choose = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T_choose) / (sigma * np.sqrt(T_choose))
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
        if hits[i] == 0 and hits[i + 1] == 0:
            n00 += 1
        elif hits[i] == 0 and hits[i + 1] == 1:
            n01 += 1
        elif hits[i] == 1 and hits[i + 1] == 0:
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
    gamma = np.sqrt(kappa ** 2 + 2 * sigma ** 2)
    exp_gamma_T = np.exp(gamma * T)
    denom = (gamma + kappa) * (exp_gamma_T - 1) + 2 * gamma

    B = 2 * (exp_gamma_T - 1) / denom
    A = (2 * gamma * np.exp((kappa + gamma) * T / 2) / denom) ** (2 * kappa * theta / sigma ** 2)

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
def color(S, K, T, r, sigma, dT=1 / 365):
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
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
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
    y_as_x: ['commodity_storage_arbitrage', 'cost_of_carry_futures_price', 'forward_price_with_carry']
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
    convexity_val = conv_sum / (price * freq ** 2)
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
    return futures_rate - 0.5 * sigma ** 2 * T1 * T2


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
            + (z ** 2 - 1) * skewness / 6
            + (z ** 3 - 3 * z) * excess_kurtosis / 24
            - (2 * z ** 3 - 5 * z) * skewness ** 2 / 36)
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
    y_as_x: ['component_risk_contribution', 'component_var', 'component_var_v2', 'efficient_frontier_problem', 'global_minimum_variance_portfolio', 'maximum_sharpe_portfolio', 'portfolio_covariance_contribution', 'portfolio_variance', 'portfolio_volatility']
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
    y_as_x: ['exposure_at_default_ead']
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
    return np.sum(ead ** 2 * lgd ** 2 * pd * (1 - pd))


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


# ================================================================================
# BATCH 3
# ================================================================================

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
    y_as_x: ['delinquency_trigger', 'trigger_based_step_down']
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
    y_as_x: ['clean_price']
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
    y_as_x: ['bachelier_option_price', 'black_caplet_price', 'cds_premium_leg', 'compounded_forward_rate', 'expected_credit_loss_ifrs_9_over_cecl', 'forward_rate_from_discount_factors', 'fra_rate', 'lifetime_ecl', 'present_value_random_variable', 'spot_rate_from_discount_factor']
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
    y_as_x: ['american_option_binomial_pricing', 'asian_option_price', 'barrier_option_price', 'binary_asset_or_nothing_call', 'binomial_option_pricing', 'black_scholes_call', 'black_scholes_merton_d1', 'black_scholes_put', 'cost_of_equity_dividend_growth']
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
    y_as_x: ['altman_z_score', 'ebitda', 'ebitda_margin', 'ev_over_ebit', 'fcff', 'financial_leverage', 'free_cash_flow_to_firm_fcff', 'interest_coverage', 'interest_coverage_ratio', 'operating_margin', 'return_on_capital_employed_roce']
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
        port.mu = np.asarray(expected_returns, dtype=float).reshape(-1, 1) if np.ndim(
            expected_returns) == 1 else expected_returns
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
    y_as_x: ['sharpe_ratio', 'information_ratio', 'burke_ratio', 'treynor_ratio','fama_french_3_factor_model',
    'fama_french_5_factor_model','information_ratio']
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


# ================================================================================
# BATCH 4
# ================================================================================

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
    y_as_x: ['expected_credit_loss_ifrs_9_over_cecl', 'expected_loss', 'unexpected_loss']
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
    y_as_x: ['black_caplet_price', 'cross_currency_basis']
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
    y_as_x: ['cash_sweep', 'fcf_yield', 'free_cash_flow_margin']
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
    y_as_x: ['net_weighted_average_spread']
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
    y_as_x: ['aparch', 'color', 'mean_variance_utility', 'option_delta_hedged_pandl', 'speed']
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
    h_i = (1 / sigma_p) * np.log(
        cf_amounts * P(0, cf_times, r0) / (X_i * P(0, T_option, r0) * strike / np.sum(cf_amounts * X_i))) + sigma_p / 2

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


# ================================================================================
# BATCH 5
# ================================================================================

def ichimoku_leading_span_a(tenkan_sen, kijun_sen, shift=26):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Ichimoku Cloud']
    function: "Ichimoku Leading Span A: average of Tenkan-sen and Kijun-sen shifted forward"
    y_as_x: []
    :param tenkan_sen: "Tenkan-sen (conversion line) series"
    :param kijun_sen: "Kijun-sen (base line) series"
    :param shift: "Number of periods to shift forward (default 26)"
    :return: "Leading Span A series shifted forward"
    '''
    import talib
    tenkan_sen = pd.Series(tenkan_sen)
    kijun_sen = pd.Series(kijun_sen)
    span_a = (tenkan_sen + kijun_sen) / 2.0
    return span_a.shift(shift)


def ichimoku_leading_span_b(high, low, period=52, shift=26):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Ichimoku Cloud']
    function: "Ichimoku Leading Span B: midpoint of 52-period high and low shifted forward"
    y_as_x: []
    :param high: "High price series"
    :param low: "Low price series"
    :param period: "Lookback period (default 52)"
    :param shift: "Number of periods to shift forward (default 26)"
    :return: "Leading Span B series shifted forward"
    '''
    high = pd.Series(high)
    low = pd.Series(low)
    span_b = (high.rolling(window=period).max() + low.rolling(window=period).min()) / 2.0
    return span_b.shift(shift)



def idiosyncratic_volatility(returns, factor_returns):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Factor models']
    function: "Idiosyncratic volatility: standard deviation of residuals from a factor model regression"
    y_as_x: []
    :param returns: "Asset return series (array-like)"
    :param factor_returns: "Factor returns array or DataFrame (n_obs x n_factors)"
    :return: "Idiosyncratic volatility (std of residuals)"
    '''
    import statsmodels.api as sm
    factor_returns = np.array(factor_returns)
    if factor_returns.ndim == 1:
        factor_returns = factor_returns.reshape(-1, 1)
    X = sm.add_constant(factor_returns)
    model = sm.OLS(np.array(returns), X).fit()
    return np.std(model.resid, ddof=1)


def implementation_shortfall(execution_price, arrival_price, side, quantity):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Execution cost analysis']
    function: "Implementation shortfall: cost of execution relative to arrival price"
    y_as_x: []
    :param execution_price: "Average execution price"
    :param arrival_price: "Price at time of order arrival"
    :param side: "+1 for buy, -1 for sell"
    :param quantity: "Number of shares/units traded"
    :return: "Implementation shortfall cost"
    '''
    return (execution_price - arrival_price) * side * quantity


def implied_cost_of_equity_simple(dividend_next, price, growth_rate):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Cost of equity estimation']
    function: "Implied cost of equity (simple): r = D1/P0 + g"
    y_as_x: []
    :param dividend_next: "Expected next-period dividend (D1)"
    :param price: "Current stock price (P0)"
    :param growth_rate: "Expected perpetual growth rate (g)"
    :return: "Implied cost of equity"
    '''
    return dividend_next / price + growth_rate


def implied_volatility(market_price, S, K, T, r, option_type='call', q=0.0):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Implied volatility']
    function: "Implied volatility: find sigma such that BS model price equals market price"
    y_as_x: []
    :param market_price: "Observed market price of the option"
    :param S: "Underlying spot price"
    :param K: "Strike price"
    :param T: "Time to expiration in years"
    :param r: "Risk-free rate"
    :param option_type: "'call' or 'put'"
    :param q: "Continuous dividend yield (default 0)"
    :return: "Implied volatility (sigma)"
    '''
    from scipy.optimize import brentq

    def bs_price(sigma):
        d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        if option_type == 'call':
            return S * np.exp(-q * T) * stats.norm.cdf(d1) - K * np.exp(-r * T) * stats.norm.cdf(d2)
        else:
            return K * np.exp(-r * T) * stats.norm.cdf(-d2) - S * np.exp(-q * T) * stats.norm.cdf(-d1)

    return brentq(lambda sigma: bs_price(sigma) - market_price, 1e-6, 10.0)


def impulse_response_function(endog, maxlags=2, periods=10):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['VAR models']
    function: "Impulse response function from a VAR model"
    y_as_x: []
    :param endog: "Multivariate time series (DataFrame or 2D array, n_obs x n_vars)"
    :param maxlags: "Number of lags in VAR model"
    :param periods: "Number of periods for IRF"
    :return: "IRF array of shape (periods+1, n_vars, n_vars)"
    '''
    from statsmodels.tsa.api import VAR
    endog = np.array(endog)
    model = VAR(endog)
    results = model.fit(maxlags=maxlags)
    irf = results.irf(periods)
    return irf.irfs


def increasing_annuity(x, interest_rate=0.05, mortality_table=None):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Life annuities']
    function: "Increasing annuity: (Ia)_x = sum of k * v^k * kpx for k>=1"
    y_as_x: []
    :param x: "Age of the annuitant"
    :param interest_rate: "Annual effective interest rate"
    :param mortality_table: "Array of qx values (mortality probabilities) starting at age 0. If None, uses illustrative Makeham table."
    :return: "Actuarial present value of increasing annuity"
    '''
    if mortality_table is None:
        ages = np.arange(0, 121)
        mortality_table = 0.001 + 0.00003 * np.exp(0.04 * ages)
        mortality_table = np.clip(mortality_table, 0, 1)
    v = 1.0 / (1.0 + interest_rate)
    max_age = len(mortality_table) - 1
    result = 0.0
    kpx = 1.0
    for k in range(1, max_age - x + 1):
        kpx *= (1.0 - mortality_table[x + k - 1])
        result += k * (v ** k) * kpx
    return result


def incremental_var(portfolio_returns, component_returns, confidence=0.95):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Value at Risk']
    function: "Incremental VaR: difference in VaR with and without a component"
    y_as_x: []
    :param portfolio_returns: "Portfolio returns series (including component)"
    :param component_returns: "Returns of the component to remove"
    :param confidence: "Confidence level (e.g. 0.95)"
    :return: "Incremental VaR"
    '''
    portfolio_returns = np.array(portfolio_returns)
    component_returns = np.array(component_returns)
    var_full = -np.percentile(portfolio_returns, (1 - confidence) * 100)
    portfolio_without = portfolio_returns - component_returns
    var_without = -np.percentile(portfolio_without, (1 - confidence) * 100)
    return var_full - var_without


def incurred_but_not_reported_ibnr(ultimate_loss, reported_loss):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Reserving']
    function: "IBNR reserve estimate: ultimate loss minus reported loss"
    y_as_x: []
    :param ultimate_loss: "Estimated ultimate incurred loss"
    :param reported_loss: "Currently reported (known) loss"
    :return: "IBNR reserve estimate"
    '''
    return ultimate_loss - reported_loss


def inflation_accretion(principal, cpi_current, cpi_base):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Inflation-linked bonds']
    function: "Inflation accretion: indexed principal adjusted by CPI ratio"
    y_as_x: []
    :param principal: "Original bond principal"
    :param cpi_current: "Current CPI level"
    :param cpi_base: "Base CPI level at issuance"
    :return: "Indexed principal at time t"
    '''
    return principal * (cpi_current / cpi_base)


def information_ratio(returns, benchmark_returns):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Performance measurement']
    function: "Information ratio: mean active return divided by tracking error"
    y_as_x: []
    :param returns: "Portfolio returns series"
    :param benchmark_returns: "Benchmark returns series"
    :return: "Information ratio"
    '''
    returns = np.array(returns)
    benchmark_returns = np.array(benchmark_returns)
    active = returns - benchmark_returns
    return np.mean(active) / np.std(active, ddof=1)


def installment_to_income_ratio(installment_payment, income):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Affordability ratios']
    function: "Installment-to-income ratio: ratio of installment payment to income"
    y_as_x: []
    :param installment_payment: "Monthly installment payment"
    :param income: "Monthly income"
    :return: "Installment-to-income ratio"
    '''
    return installment_payment / income


def instantaneous_forward_rate(discount_factors, times):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Forward rates']
    function: "Instantaneous forward rate: f(t,T) = -d ln P(t,T)/dT"
    y_as_x: []
    :param discount_factors: "Array of discount factors P(0,T)"
    :param times: "Array of corresponding maturities T"
    :return: "Array of instantaneous forward rates"
    '''
    discount_factors = np.array(discount_factors, dtype=float)
    times = np.array(times, dtype=float)
    log_df = np.log(discount_factors)
    fwd_rates = -np.gradient(log_df, times)
    return fwd_rates


def instantaneous_short_rate_from_discount_curve(discount_factors, times):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Short rate models']
    function: "Instantaneous short rate from discount curve: r(t) = -d ln P(0,t)/dt"
    y_as_x: []
    :param discount_factors: "Array of discount factors P(0,t)"
    :param times: "Array of corresponding maturities t"
    :return: "Array of instantaneous short rates"
    '''
    discount_factors = np.array(discount_factors, dtype=float)
    times = np.array(times, dtype=float)
    log_df = np.log(discount_factors)
    short_rates = -np.gradient(log_df, times)
    return short_rates


def instrumental_variables_over_2sls(y, X, Z):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Instrumental variables']
    function: "2SLS instrumental variables estimator: beta = (X'Pz X)^-1 X'Pz y"
    y_as_x: []
    :param y: "Dependent variable array (n,)"
    :param X: "Endogenous regressors array (n x k)"
    :param Z: "Instrument matrix (n x l), l >= k"
    :return: "Dictionary with 'coefficients' and 'fitted_values'"
    '''
    y = np.array(y, dtype=float).ravel()
    X = np.atleast_2d(np.array(X, dtype=float))
    Z = np.atleast_2d(np.array(Z, dtype=float))
    if X.shape[0] == 1 and X.shape[1] > 1:
        X = X.T
    if Z.shape[0] == 1 and Z.shape[1] > 1:
        Z = Z.T
    # Projection matrix Pz = Z(Z'Z)^-1 Z'
    Pz = Z @ np.linalg.inv(Z.T @ Z) @ Z.T
    beta = np.linalg.inv(X.T @ Pz @ X) @ (X.T @ Pz @ y)
    fitted = X @ beta
    return {'coefficients': beta, 'fitted_values': fitted}


def interaction_effect(weights_portfolio, weights_benchmark, returns_portfolio, returns_benchmark):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Brinson attribution']
    function: "Interaction effect: (w_p - w_b) * (r_p - r_b) for each sector"
    y_as_x: []
    :param weights_portfolio: "Portfolio sector weights"
    :param weights_benchmark: "Benchmark sector weights"
    :param returns_portfolio: "Portfolio sector returns"
    :param returns_benchmark: "Benchmark sector returns"
    :return: "Interaction effect per sector (array)"
    '''
    wp = np.array(weights_portfolio)
    wb = np.array(weights_benchmark)
    rp = np.array(returns_portfolio)
    rb = np.array(returns_benchmark)
    return (wp - wb) * (rp - rb)


def interest_coverage(ebit, interest_expense):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Coverage ratios']
    function: "Interest coverage ratio: EBIT divided by interest expense"
    y_as_x: []
    :param ebit: "Earnings before interest and taxes"
    :param interest_expense: "Interest expense"
    :return: "Interest coverage ratio"
    '''
    return ebit / interest_expense


def interest_coverage_ratio(ebit, interest_expense):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Coverage ratios']
    function: "Interest coverage ratio: EBIT / Interest Expense"
    y_as_x: []
    :param ebit: "Earnings before interest and taxes"
    :param interest_expense: "Total interest expense"
    :return: "Interest coverage ratio"
    '''
    return ebit / interest_expense


def interest_coverage_ratio_tranche(interest_collections, note_interest_due):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Tranche coverage']
    function: "Tranche interest coverage ratio: interest collections relative to note interest due"
    y_as_x: []
    :param interest_collections: "Total interest collections available"
    :param note_interest_due: "Interest due on the tranche"
    :return: "Interest coverage ratio for the tranche"
    '''
    return interest_collections / note_interest_due


def interest_payment(rate, per, nper, pv, fv=0):
    '''
    domain: ['Banking, lending & project finance']
    subdomain: ['Loan amortization']
    function: "Interest payment for a given period of an amortizing loan"
    y_as_x: []
    :param rate: "Interest rate per period"
    :param per: "Period for which to compute interest (1-based)"
    :param nper: "Total number of periods"
    :param pv: "Present value (loan amount)"
    :param fv: "Future value (default 0)"
    :return: "Interest portion of payment in given period"
    '''
    import numpy_financial as npf
    return npf.ipmt(rate, per, nper, pv, fv)


def interest_only_payment(loan_amount, annual_interest_rate):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Loan payments']
    function: "Interest-only monthly payment: loan amount times annual rate divided by 12"
    y_as_x: []
    :param loan_amount: "Outstanding loan balance"
    :param annual_interest_rate: "Annual interest rate (decimal)"
    :return: "Monthly interest-only payment"
    '''
    return loan_amount * annual_interest_rate / 12.0


def interest_rate_hedge_ratio(dv01_exposure, dv01_hedge):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Hedging']
    function: "Interest rate hedge ratio: DV01 of exposure divided by DV01 of hedge instrument"
    y_as_x: []
    :param dv01_exposure: "DV01 (dollar value of a basis point) of the exposure"
    :param dv01_hedge: "DV01 of the hedging instrument"
    :return: "Number of hedge units needed (hedge ratio)"
    '''
    return dv01_exposure / dv01_hedge


def internal_rate_of_return_irr(cash_flows):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Capital budgeting']
    function: "Internal rate of return: rate that makes NPV of cash flows equal zero"
    y_as_x: ['lbo_equity_irr', 'internal_rate_of_return_since_inception', 'property_irr']
    :param cash_flows: "Array of cash flows (starting with initial investment, typically negative)"
    :return: "Internal rate of return"
    '''
    import numpy_financial as npf
    return npf.irr(np.array(cash_flows))


def internal_rate_of_return_since_inception(market_value_start, market_value_end, cash_flows, cash_flow_times):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Return calculation']
    function: "IRR since inception including beginning/ending market values and interim cash flows"
    y_as_x: []
    :param market_value_start: "Market value at inception"
    :param market_value_end: "Market value at end"
    :param cash_flows: "Array of interim cash flows (positive = inflow)"
    :param cash_flow_times: "Array of times (in years) of each cash flow from inception"
    :return: "IRR since inception"
    '''
    import numpy_financial as npf
    cash_flows = np.array(cash_flows)
    cash_flow_times = np.array(cash_flow_times)
    # Build total cash flow series: -MV0 at t=0, interim CFs, +MV_end at T
    T = cash_flow_times[-1] if len(cash_flow_times) > 0 else 1.0
    # Simple approach: construct equivalent periodic cash flows
    all_cfs = [-market_value_start] + list(cash_flows) + [market_value_end]
    return npf.irr(np.array(all_cfs))


def international_fisher_effect(domestic_rate, foreign_rate):
    '''
    domain: ['FX & international finance']
    subdomain: ['International parity conditions']
    function: "International Fisher effect: expected FX change approximately equals interest rate differential"
    y_as_x: []
    :param domestic_rate: "Domestic nominal interest rate"
    :param foreign_rate: "Foreign nominal interest rate"
    :return: "Expected change in exchange rate (domestic/foreign)"
    '''
    return domestic_rate - foreign_rate


def intrinsic_value_call(spot_price, strike_price):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Option payoffs']
    function: "Intrinsic value of a call option: max(S - K, 0)"
    y_as_x: ['time_value_option']
    :param spot_price: "Current underlying spot price (S)"
    :param strike_price: "Option strike price (K)"
    :return: "Intrinsic value of the call"
    '''
    return max(spot_price - strike_price, 0.0)


def inventory_turnover(cogs, average_inventory):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Efficiency ratios']
    function: "Inventory turnover: cost of goods sold divided by average inventory"
    y_as_x: []
    :param cogs: "Cost of goods sold"
    :param average_inventory: "Average inventory over the period"
    :return: "Inventory turnover ratio"
    '''
    return cogs / average_inventory


def io_strip_value(interest_cashflows, discount_factors):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['MBS strips']
    function: "Interest-only strip value: present value of interest-only cash flows"
    y_as_x: []
    :param interest_cashflows: "Array of interest-only cash flows per period"
    :param discount_factors: "Array of discount factors corresponding to each period"
    :return: "Present value of IO strip"
    '''
    interest_cashflows = np.array(interest_cashflows)
    discount_factors = np.array(discount_factors)
    return np.sum(interest_cashflows * discount_factors)


def johansen_cointegration(data, det_order=0, k_ar_diff=1):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Cointegration']
    function: "Johansen cointegration test: test rank of Pi matrix in VECM"
    y_as_x: []
    :param data: "Multivariate time series (DataFrame or 2D array, n_obs x n_vars)"
    :param det_order: "Deterministic term order (-1: no constant, 0: constant, 1: trend)"
    :param k_ar_diff: "Number of lagged differences in the VECM"
    :return: "Dictionary with 'trace_stat', 'crit_values_trace', 'eigen_stat', 'crit_values_eigen', 'evec' (eigenvectors)"
    '''
    from statsmodels.tsa.vector_ar.vecm import coint_johansen
    data = np.array(data)
    result = coint_johansen(data, det_order, k_ar_diff)
    return {
        'trace_stat': result.lr1,
        'crit_values_trace': result.cvt,
        'eigen_stat': result.lr2,
        'crit_values_eigen': result.cvm,
        'evec': result.evec
    }


def johansen_trace_statistic(data, det_order=0, k_ar_diff=1):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Cointegration']
    function: "Johansen trace statistic: -T * sum ln(1 - lambda_i) for i=r+1..k"
    y_as_x: []
    :param data: "Multivariate time series (DataFrame or 2D array)"
    :param det_order: "Deterministic term order (-1, 0, or 1)"
    :param k_ar_diff: "Number of lagged differences"
    :return: "Dictionary with 'trace_statistics' and 'critical_values'"
    '''
    from statsmodels.tsa.vector_ar.vecm import coint_johansen
    data = np.array(data)
    result = coint_johansen(data, det_order, k_ar_diff)
    return {
        'trace_statistics': result.lr1,
        'critical_values': result.cvt
    }


def kelly_criterion(win_prob, win_loss_ratio):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Position sizing']
    function: "Kelly criterion: optimal fraction to bet given win probability and payoff ratio"
    y_as_x: []
    :param win_prob: "Probability of winning (p)"
    :param win_loss_ratio: "Ratio of win amount to loss amount (b)"
    :return: "Optimal fraction of capital to wager (f*)"
    '''
    q = 1.0 - win_prob
    return (win_loss_ratio * win_prob - q) / win_loss_ratio


def keltner_channel_lower(close, high, low, ema_period=20, atr_period=10, multiplier=2.0):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Volatility channels']
    function: "Keltner channel lower band: EMA minus multiplier times ATR"
    y_as_x: []
    :param close: "Close price series"
    :param high: "High price series"
    :param low: "Low price series"
    :param ema_period: "EMA period (default 20)"
    :param atr_period: "ATR period (default 10)"
    :param multiplier: "ATR multiplier (default 2.0)"
    :return: "Lower Keltner channel series"
    '''
    close = pd.Series(close)
    high = pd.Series(high)
    low = pd.Series(low)
    ema = close.ewm(span=ema_period, adjust=False).mean()
    tr = pd.concat([high - low, (high - close.shift(1)).abs(), (low - close.shift(1)).abs()], axis=1).max(axis=1)
    atr = tr.rolling(window=atr_period).mean()
    return ema - multiplier * atr


def keltner_channel_upper(close, high, low, ema_period=20, atr_period=10, multiplier=2.0):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Volatility channels']
    function: "Keltner channel upper band: EMA plus multiplier times ATR"
    y_as_x: []
    :param close: "Close price series"
    :param high: "High price series"
    :param low: "Low price series"
    :param ema_period: "EMA period (default 20)"
    :param atr_period: "ATR period (default 10)"
    :param multiplier: "ATR multiplier (default 2.0)"
    :return: "Upper Keltner channel series"
    '''
    close = pd.Series(close)
    high = pd.Series(high)
    low = pd.Series(low)
    ema = close.ewm(span=ema_period, adjust=False).mean()
    tr = pd.concat([high - low, (high - close.shift(1)).abs(), (low - close.shift(1)).abs()], axis=1).max(axis=1)
    atr = tr.rolling(window=atr_period).mean()
    return ema + multiplier * atr


def kmv_expected_default_frequency(distance_to_default):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Structural models']
    function: "KMV expected default frequency: EDF = Phi(-DD)"
    y_as_x: []
    :param distance_to_default: "Distance to default (DD)"
    :return: "Expected default frequency (probability)"
    '''
    return stats.norm.cdf(-distance_to_default)


def kpss_stationarity_test(series, regression='c', nlags='auto'):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Stationarity tests']
    function: "KPSS stationarity test: null hypothesis is that the series is stationary"
    y_as_x: []
    :param series: "Time series (array-like)"
    :param regression: "'c' for constant, 'ct' for constant + trend"
    :param nlags: "Number of lags or 'auto'"
    :return: "Dictionary with 'statistic', 'p_value', 'lags', 'critical_values'"
    '''
    from statsmodels.tsa.stattools import kpss
    series = np.array(series)
    stat, p_value, lags, crit = kpss(series, regression=regression, nlags=nlags)
    return {
        'statistic': stat,
        'p_value': p_value,
        'lags': lags,
        'critical_values': crit
    }


def kupiec_pof_likelihood_ratio(T, x, p):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Backtesting VaR']
    function: "Kupiec proportion of failures test: LR statistic for VaR backtesting"
    y_as_x: []
    :param T: "Total number of observations"
    :param x: "Number of VaR exceptions (violations)"
    :param p: "Expected probability of exception (e.g. 0.01 for 99% VaR)"
    :return: "Dictionary with 'lr_statistic' and 'p_value'"
    '''
    if x == 0:
        lr = -2.0 * (T * np.log(1 - p) - T * np.log(1 - 0.0))
    elif x == T:
        lr = -2.0 * (T * np.log(p) - T * np.log(1.0))
    else:
        pi_hat = x / T
        lr = -2.0 * ((T - x) * np.log(1 - p) + x * np.log(p)
                     - (T - x) * np.log(1 - pi_hat) - x * np.log(pi_hat))
    p_value = 1.0 - stats.chi2.cdf(lr, df=1)
    return {'lr_statistic': lr, 'p_value': p_value}


def kyle_lambda(price_changes, order_flow):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Market microstructure']
    function: "Kyle's lambda: price impact coefficient from regressing price changes on order flow"
    y_as_x: []
    :param price_changes: "Array of price changes (delta p)"
    :param order_flow: "Array of signed order flow (q)"
    :return: "Dictionary with 'lambda' (price impact coefficient) and 'r_squared'"
    '''
    import statsmodels.api as sm
    q = sm.add_constant(np.array(order_flow))
    model = sm.OLS(np.array(price_changes), q).fit()
    return {'lambda': model.params[1], 'r_squared': model.rsquared}


def large_exposure_ratio(exposure_to_counterparty, tier1_capital):
    '''
    domain: ['Bank regulation, Basel & prudential ratios']
    subdomain: ['Concentration risk']
    function: "Large exposure ratio: single counterparty exposure relative to Tier 1 capital"
    y_as_x: []
    :param exposure_to_counterparty: "Exposure amount to a single counterparty"
    :param tier1_capital: "Tier 1 capital"
    :return: "Large exposure ratio"
    '''
    return exposure_to_counterparty / tier1_capital


def lbo_debt_paydown_schedule(initial_debt, mandatory_amortization, cash_sweep_amounts):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['LBO modeling']
    function: "LBO debt paydown schedule: debt balance after mandatory amortization and cash sweeps"
    y_as_x: []
    :param initial_debt: "Initial debt at close"
    :param mandatory_amortization: "Array of mandatory amortization per period"
    :param cash_sweep_amounts: "Array of cash sweep amounts per period"
    :return: "Array of ending debt balances per period"
    '''
    mandatory_amortization = np.array(mandatory_amortization)
    cash_sweep_amounts = np.array(cash_sweep_amounts)
    n = len(mandatory_amortization)
    debt = np.zeros(n)
    balance = initial_debt
    for t in range(n):
        balance = balance - mandatory_amortization[t] - cash_sweep_amounts[t]
        debt[t] = max(balance, 0.0)
    return debt


def lbo_equity_irr(equity_invested, cash_to_equity, exit_equity, periods=None):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['LBO modeling']
    function: "LBO equity IRR: rate that equates initial equity to interim and exit cash flows"
    y_as_x: []
    :param equity_invested: "Initial equity investment (positive number)"
    :param cash_to_equity: "Array of interim cash distributions to equity per period"
    :param exit_equity: "Equity value at exit (included in last period)"
    :param periods: "Number of periods (inferred from cash_to_equity if None)"
    :return: "Equity IRR"
    '''
    import numpy_financial as npf
    cash_to_equity = np.array(cash_to_equity, dtype=float)
    cfs = np.concatenate([[-equity_invested], cash_to_equity])
    cfs[-1] += exit_equity
    return npf.irr(cfs)

def ledoit_wolf_covariance_shrinkage(returns):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Covariance estimation']
    function: "Ledoit-Wolf covariance shrinkage estimator: (1-delta)*S + delta*F"
    y_as_x: []
    :param returns: "Returns matrix (n_obs x n_assets)"
    :return: "Dictionary with 'covariance' (shrunk covariance matrix) and 'shrinkage' (shrinkage intensity)"
    '''
    from sklearn.covariance import LedoitWolf
    returns = np.array(returns)
    lw = LedoitWolf().fit(returns)
    return {'covariance': lw.covariance_, 'shrinkage': lw.shrinkage_}


def leverage_constraint(weights, max_leverage=2.0):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio constraints']
    function: "Leverage constraint: sum of absolute weights must not exceed L_max"
    y_as_x: []
    :param weights: "Portfolio weight vector"
    :param max_leverage: "Maximum allowed gross leverage (default 2.0)"
    :return: "Dictionary with 'is_feasible' (bool) and 'gross_leverage'"
    '''
    weights = np.array(weights)
    gross_leverage = np.sum(np.abs(weights))
    return {'is_feasible': gross_leverage <= max_leverage, 'gross_leverage': gross_leverage}


def leverage_ratio(tier1_capital, exposure_measure):
    '''
    domain: ['Banking, lending & project finance']
    subdomain: ['Capital adequacy']
    function: "Leverage ratio: Tier 1 capital divided by total exposure measure"
    y_as_x: []
    :param tier1_capital: "Tier 1 capital"
    :param exposure_measure: "Total exposure measure (on- and off-balance sheet)"
    :return: "Leverage ratio"
    '''
    return tier1_capital / exposure_measure


def levered_beta_hamada(unlevered_beta, tax_rate, debt, equity):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Cost of capital']
    function: "Levered beta (Hamada equation): beta_L = beta_U * [1 + (1-T)*D/E]"
    y_as_x: []
    :param unlevered_beta: "Unlevered (asset) beta"
    :param tax_rate: "Corporate tax rate"
    :param debt: "Total debt"
    :param equity: "Total equity"
    :return: "Levered (equity) beta"
    '''
    return unlevered_beta * (1.0 + (1.0 - tax_rate) * debt / equity)


def levered_yield(cash_flow_after_debt_service, equity):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Return metrics']
    function: "Levered yield: cash flow after debt service divided by equity invested"
    y_as_x: []
    :param cash_flow_after_debt_service: "Net cash flow after debt service"
    :param equity: "Equity invested"
    :return: "Levered yield"
    '''
    return cash_flow_after_debt_service / equity


def lgd_downturn_adjustment(lgd_base, stress_addon):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Loss given default']
    function: "Downturn LGD: base LGD plus a stress add-on for adverse conditions"
    y_as_x: []
    :param lgd_base: "Through-the-cycle LGD estimate"
    :param stress_addon: "Additional LGD stress component for downturn"
    :return: "Downturn-adjusted LGD"
    '''
    return lgd_base + stress_addon


def libor_market_model_lmm(L0, sigma, T_schedule, n_paths=10000, dt=0.01):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['LIBOR market model']
    function: "LIBOR Market Model (LMM/BGM) simulation: dL_i/L_i = mu_i dt + sigma_i dW"
    y_as_x: []
    :param L0: "Array of initial forward LIBOR rates"
    :param sigma: "Array of volatilities for each forward rate"
    :param T_schedule: "Array of tenor reset dates"
    :param n_paths: "Number of simulation paths (default 10000)"
    :param dt: "Time step (default 0.01)"
    :return: "Simulated forward rate paths array of shape (n_paths, n_tenors)"
    '''
    L0 = np.array(L0, dtype=float)
    sigma = np.array(sigma, dtype=float)
    T_schedule = np.array(T_schedule, dtype=float)
    n_tenors = len(L0)
    L = np.tile(L0, (n_paths, 1))  # (n_paths, n_tenors)

    for i in range(n_tenors):
        n_steps = int(T_schedule[i] / dt)
        for _ in range(max(n_steps, 1)):
            # Drift under forward measure (simplified log-normal)
            drift = 0.0
            for j in range(i + 1, n_tenors):
                tau_j = T_schedule[j] - T_schedule[j - 1] if j > 0 else T_schedule[j]
                drift += (sigma[j] * tau_j * L[:, j]) / (1.0 + tau_j * L[:, j])
            drift = sigma[i] * drift * dt
            dW = np.random.normal(0, np.sqrt(dt), n_paths)
            L[:, i] *= np.exp((drift - 0.5 * sigma[i] ** 2 * dt) + sigma[i] * dW)

    return L


def life_annuity_immediate(x, interest_rate=0.05, mortality_table=None):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Life annuities']
    function: "Life annuity-immediate: a_x = sum_k v^(k+1) * kpx"
    y_as_x: []
    :param x: "Age of the annuitant"
    :param interest_rate: "Annual effective interest rate"
    :param mortality_table: "Array of qx values starting at age 0. If None, uses illustrative table."
    :return: "Actuarial present value of life annuity-immediate"
    '''
    if mortality_table is None:
        ages = np.arange(0, 121)
        mortality_table = 0.001 + 0.00003 * np.exp(0.04 * ages)
        mortality_table = np.clip(mortality_table, 0, 1)
    v = 1.0 / (1.0 + interest_rate)
    max_age = len(mortality_table) - 1
    result = 0.0
    kpx = 1.0
    for k in range(1, max_age - x + 1):
        kpx *= (1.0 - mortality_table[x + k - 1])
        result += (v ** k) * kpx
    return result


def lifetime_ecl(marginal_pd, lgd, ead, discount_factors):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Expected credit loss']
    function: "Lifetime ECL: sum of marginal PD * LGD * EAD * DF across all periods"
    y_as_x: []
    :param marginal_pd: "Array of marginal probability of default per period"
    :param lgd: "Array of loss given default per period (or scalar)"
    :param ead: "Array of exposure at default per period (or scalar)"
    :param discount_factors: "Array of discount factors per period"
    :return: "Lifetime expected credit loss"
    '''
    marginal_pd = np.array(marginal_pd)
    lgd = np.broadcast_to(np.array(lgd), marginal_pd.shape)
    ead = np.broadcast_to(np.array(ead), marginal_pd.shape)
    discount_factors = np.array(discount_factors)
    return np.sum(marginal_pd * lgd * ead * discount_factors)


def liquidity_coverage_ratio_lcr(hqla, net_cash_outflows_30d):
    '''
    domain: ['Bank regulation, Basel & prudential ratios']
    subdomain: ['Liquidity regulation']
    function: "LCR: high quality liquid assets divided by projected 30-day net cash outflows"
    y_as_x: []
    :param hqla: "Stock of high quality liquid assets"
    :param net_cash_outflows_30d: "Total expected net cash outflows over next 30 days"
    :return: "Liquidity coverage ratio"
    '''
    return hqla / net_cash_outflows_30d


def liquidity_gap(cash_inflows, cash_outflows):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Liquidity management']
    function: "Liquidity gap per time bucket: cash inflows minus cash outflows"
    y_as_x: []
    :param cash_inflows: "Cash inflows per period (array or scalar)"
    :param cash_outflows: "Cash outflows per period (array or scalar)"
    :return: "Liquidity gap per period"
    '''
    return np.array(cash_inflows) - np.array(cash_outflows)


def liquidity_adjusted_var(var_estimate, liquidation_cost_addon):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Liquidity-adjusted risk']
    function: "Liquidity-adjusted VaR: standard VaR plus a liquidation cost add-on"
    y_as_x: []
    :param var_estimate: "Standard VaR estimate"
    :param liquidation_cost_addon: "Add-on for expected liquidation cost (e.g. half-spread x position)"
    :return: "Liquidity-adjusted VaR"
    '''
    return var_estimate + liquidation_cost_addon


def loan_amortization_schedule_identity(beginning_balance, principal_paid):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Loan amortization']
    function: "Amortization identity: ending balance = beginning balance minus principal paid"
    y_as_x: []
    :param beginning_balance: "Balance at start of period"
    :param principal_paid: "Principal portion of payment"
    :return: "Ending balance"
    '''
    return beginning_balance - principal_paid


def loan_constant_over_mortgage_constant(annual_rate, nper):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Mortgage metrics']
    function: "Loan/mortgage constant: annual debt service per dollar of original loan"
    y_as_x: []
    :param annual_rate: "Annual interest rate (decimal)"
    :param nper: "Total number of monthly payment periods"
    :return: "Loan constant (annual debt service / original loan amount)"
    '''
    import numpy_financial as npf
    monthly_rate = annual_rate / 12.0
    monthly_pmt = -npf.pmt(monthly_rate, nper, 1.0)
    annual_debt_service = monthly_pmt * 12.0
    return annual_debt_service


def loan_life_coverage_ratio(npv_cashflows, outstanding_debt):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Coverage ratios']
    function: "Loan life coverage ratio: NPV of future cash flows divided by outstanding debt"
    y_as_x: []
    :param npv_cashflows: "Net present value of remaining project cash flows"
    :param outstanding_debt: "Outstanding debt balance"
    :return: "Loan life coverage ratio"
    '''
    return npv_cashflows / outstanding_debt


def loan_loss_coverage_ratio(loan_loss_reserves, non_performing_loans):
    '''
    domain: ['Banking, lending & project finance']
    subdomain: ['Asset quality']
    function: "Loan loss coverage ratio: reserves relative to non-performing loans"
    y_as_x: []
    :param loan_loss_reserves: "Total loan loss reserves (provisions)"
    :param non_performing_loans: "Total non-performing loans"
    :return: "Loan loss coverage ratio"
    '''
    return loan_loss_reserves / non_performing_loans


def loan_payment_annuity(rate, nper, pv, fv=0):
    '''
    domain: ['Banking, lending & project finance']
    subdomain: ['Loan payments']
    function: "Annuity loan payment: PMT = r * PV / [1 - (1+r)^(-n)]"
    y_as_x: []
    :param rate: "Interest rate per period"
    :param nper: "Total number of payment periods"
    :param pv: "Present value (loan amount)"
    :param fv: "Future value (default 0)"
    :return: "Payment per period (negative sign convention)"
    '''
    import numpy_financial as npf
    return npf.pmt(rate, nper, pv, fv)


def loan_to_cost(loan_amount, project_cost):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Lending ratios']
    function: "Loan-to-cost: loan amount divided by total project cost"
    y_as_x: []
    :param loan_amount: "Total loan amount"
    :param project_cost: "Total project cost"
    :return: "Loan-to-cost ratio"
    '''
    return loan_amount / project_cost


def loan_to_deposit_ratio(gross_loans, deposits):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Funding ratios']
    function: "Loan-to-deposit ratio: gross loans divided by total deposits"
    y_as_x: []
    :param gross_loans: "Total gross loans"
    :param deposits: "Total customer deposits"
    :return: "Loan-to-deposit ratio"
    '''
    return gross_loans / deposits


def loan_to_value(loan_amount, collateral_value):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Lending ratios']
    function: "Loan-to-value: loan amount divided by collateral value"
    y_as_x: []
    :param loan_amount: "Loan amount"
    :param collateral_value: "Appraised collateral value"
    :return: "LTV ratio"
    '''
    return loan_amount / collateral_value


def local_volatility_dupire(strikes, expiries, call_prices, spot, rate=0.0):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Local volatility']
    function: "Dupire local volatility: sigma_loc^2 = dC/dT / (0.5 K^2 d^2C/dK^2)"
    y_as_x: []
    :param strikes: "Array of strike prices"
    :param expiries: "Array of expiry times"
    :param call_prices: "2D array of call prices (len(expiries) x len(strikes))"
    :param spot: "Current spot price"
    :param rate: "Risk-free rate (default 0)"
    :return: "2D array of local volatilities (same shape as call_prices interior)"
    '''
    strikes = np.array(strikes, dtype=float)
    expiries = np.array(expiries, dtype=float)
    C = np.array(call_prices, dtype=float)

    # Numerical derivatives
    dC_dT = np.gradient(C, expiries, axis=0)
    dC_dK = np.gradient(C, strikes, axis=1)
    d2C_dK2 = np.gradient(dC_dK, strikes, axis=1)

    # Dupire formula
    K_grid = np.tile(strikes, (len(expiries), 1))
    numerator = dC_dT + rate * K_grid * dC_dK
    denominator = 0.5 * K_grid ** 2 * d2C_dK2
    # Avoid division by zero
    denominator = np.where(np.abs(denominator) < 1e-12, 1e-12, denominator)
    local_var = numerator / denominator
    local_var = np.maximum(local_var, 1e-12)
    return np.sqrt(local_var)


def local_over_stochastic_volatility_surface_interpolation(strikes, expiries, vol_surface, K_query, T_query):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Volatility surface']
    function: "Interpolate an observed volatility surface at given strike and expiry"
    y_as_x: []
    :param strikes: "Array of observed strike prices"
    :param expiries: "Array of observed expiry times"
    :param vol_surface: "2D array of observed vols (len(expiries) x len(strikes))"
    :param K_query: "Strike(s) at which to interpolate"
    :param T_query: "Expiry(ies) at which to interpolate"
    :return: "Interpolated implied volatility"
    '''
    from scipy.interpolate import RectBivariateSpline
    strikes = np.array(strikes, dtype=float)
    expiries = np.array(expiries, dtype=float)
    vol_surface = np.array(vol_surface, dtype=float)
    interp = RectBivariateSpline(expiries, strikes, vol_surface)
    return interp(T_query, K_query, grid=False)


def log_return(prices):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Return calculation']
    function: "Log return: r_t = ln(P_t / P_{t-1})"
    y_as_x: ['return']
    :param prices: "Price series (array-like)"
    :return: "Array of log returns"
    '''
    prices = np.array(prices, dtype=float)
    return np.log(prices[1:] / prices[:-1])


def long_only_constraint(weights):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio constraints']
    function: "Long-only constraint check: all weights must be non-negative"
    y_as_x: []
    :param weights: "Portfolio weight vector"
    :return: "Dictionary with 'is_feasible' (bool) and 'min_weight'"
    '''
    weights = np.array(weights)
    return {'is_feasible': bool(np.all(weights >= 0)), 'min_weight': float(np.min(weights))}


def lookback_option_price(S, K, r, T, sigma, option_type='call', S_max=None, S_min=None, n_steps=252):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Exotic options']
    function: "Lookback option price via Monte Carlo simulation"
    y_as_x: []
    :param S: "Current spot price"
    :param K: "Strike price"
    :param r: "Risk-free rate"
    :param T: "Time to expiration in years"
    :param sigma: "Volatility"
    :param option_type: "'call' (payoff on max) or 'put' (payoff on min)"
    :param S_max: "Running maximum so far (for call, default S)"
    :param S_min: "Running minimum so far (for put, default S)"
    :param n_steps: "Number of time steps for simulation"
    :return: "Estimated lookback option price"
    '''
    n_paths = 10000
    dt = T / n_steps
    paths = np.zeros((n_paths, n_steps + 1))
    paths[:, 0] = S

    z = np.random.standard_normal((n_paths, n_steps))
    for t in range(1, n_steps + 1):
        paths[:, t] = paths[:, t - 1] * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * z[:, t - 1])

    if option_type == 'call':
        if S_max is not None:
            running_max = np.maximum(S_max, np.maximum.accumulate(paths, axis=1)[:, -1])
        else:
            running_max = np.maximum.accumulate(paths, axis=1)[:, -1]
        payoffs = np.maximum(running_max - K, 0)
    else:
        if S_min is not None:
            running_min = np.minimum(S_min, np.minimum.accumulate(paths, axis=1)[:, -1])
        else:
            running_min = np.minimum.accumulate(paths, axis=1)[:, -1]
        payoffs = np.maximum(K - running_min, 0)

    return np.exp(-r * T) * np.mean(payoffs)


def loss_given_default(recovery_rate):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Credit risk parameters']
    function: "Loss given default: 1 minus recovery rate"
    y_as_x: ['credit_var', 'expected_loss', 'lgd_downturn_adjustment', 'lifetime_ecl', 'recovery_rate', 'reduced_form_cds_hazard_relation', 'unexpected_loss']
    :param recovery_rate: "Recovery rate as a decimal (0 to 1)"
    :return: "Loss given default"
    '''
    return 1.0 - recovery_rate


def loss_random_variable(pv_benefits_expenses, pv_premiums):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Life insurance']
    function: "Loss random variable: PV(benefits + expenses) minus PV(premiums)"
    y_as_x: []
    :param pv_benefits_expenses: "Present value of benefits and expenses"
    :param pv_premiums: "Present value of premiums"
    :return: "Loss random variable value"
    '''
    return pv_benefits_expenses - pv_premiums


def loss_rate(net_credit_losses, average_loans):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Portfolio loss metrics']
    function: "Loss rate: net credit losses divided by average loan balance"
    y_as_x: []
    :param net_credit_losses: "Net credit losses over the period"
    :param average_loans: "Average outstanding loan balance"
    :return: "Loss rate"
    '''
    return net_credit_losses / average_loans


def loss_ratio(incurred_losses, earned_premiums):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Insurance ratios']
    function: "Loss ratio: incurred losses divided by earned premiums"
    y_as_x: ['combined_ratio']
    :param incurred_losses: "Total incurred losses"
    :param earned_premiums: "Total earned premiums"
    :return: "Loss ratio"
    '''
    return incurred_losses / earned_premiums


def ltv_for_mortgage(mortgage_balance, property_value):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Mortgage ratios']
    function: "Loan-to-value for mortgage: mortgage balance divided by property value"
    y_as_x: []
    :param mortgage_balance: "Outstanding mortgage balance"
    :param property_value: "Current property value"
    :return: "LTV ratio"
    '''
    return mortgage_balance / property_value


def ma_q(endog, order=1):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Time series models']
    function: "MA(q) model: x_t = mu + epsilon_t + sum theta_i * epsilon_{t-i}"
    y_as_x: []
    :param endog: "Time series data (array-like)"
    :param order: "MA order q (default 1)"
    :return: "Dictionary with 'params', 'fitted_values', 'residuals', 'aic'"
    '''
    from statsmodels.tsa.arima.model import ARIMA
    endog = np.array(endog, dtype=float)
    model = ARIMA(endog, order=(0, 0, order)).fit()
    return {
        'params': model.params,
        'fitted_values': model.fittedvalues,
        'residuals': model.resid,
        'aic': model.aic
    }


def macaulay_duration(cash_flows, times, ytm):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Duration']
    function: "Macaulay duration: weighted average time to receive bond cash flows"
    y_as_x: ['modified_duration']
    :param cash_flows: "Array of bond cash flows"
    :param times: "Array of times (in years) for each cash flow"
    :param ytm: "Yield to maturity (per period matching times)"
    :return: "Macaulay duration"
    '''
    cash_flows = np.array(cash_flows, dtype=float)
    times = np.array(times, dtype=float)
    pv_cfs = cash_flows / (1.0 + ytm) ** times
    price = np.sum(pv_cfs)
    return np.sum(times * pv_cfs) / price


def macaulay_spread_duration(cash_flows, times, spread, base_yield=0.0):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Spread risk']
    function: "Macaulay spread duration: sensitivity of bond price to spread changes"
    y_as_x: []
    :param cash_flows: "Array of bond cash flows"
    :param times: "Array of times (in years) for each cash flow"
    :param spread: "Credit spread"
    :param base_yield: "Base risk-free yield"
    :return: "Spread duration"
    '''
    cash_flows = np.array(cash_flows, dtype=float)
    times = np.array(times, dtype=float)
    y = base_yield + spread
    pv_cfs = cash_flows / (1.0 + y) ** times
    price = np.sum(pv_cfs)
    return np.sum(times * pv_cfs) / price


def macd(close, fast_period=12, slow_period=26):
    '''
    domain: ['Technical analysis']
    subdomain: ['Trend indicators']
    function: "MACD line: difference between fast and slow exponential moving averages"
    y_as_x: ['macd_histogram']
    :param close: "Close price series"
    :param fast_period: "Fast EMA period (default 12)"
    :param slow_period: "Slow EMA period (default 26)"
    :return: "MACD line series"
    '''
    close = pd.Series(close)
    ema_fast = close.ewm(span=fast_period, adjust=False).mean()
    ema_slow = close.ewm(span=slow_period, adjust=False).mean()
    return ema_fast - ema_slow


def macd_histogram(close, fast_period=12, slow_period=26, signal_period=9):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Trend indicators']
    function: "MACD histogram: MACD line minus signal line"
    y_as_x: []
    :param close: "Close price series"
    :param fast_period: "Fast EMA period (default 12)"
    :param slow_period: "Slow EMA period (default 26)"
    :param signal_period: "Signal EMA period (default 9)"
    :return: "MACD histogram series"
    '''
    close = pd.Series(close)
    ema_fast = close.ewm(span=fast_period, adjust=False).mean()
    ema_slow = close.ewm(span=slow_period, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal = macd_line.ewm(span=signal_period, adjust=False).mean()
    return macd_line - signal


def management_option_value(S, K, T, r, sigma, option_type='call'):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Option valuation']
    function: "Management option value using Black-Scholes pricing"
    y_as_x: []
    :param S: "Current underlying asset value"
    :param K: "Strike price of management options"
    :param T: "Time to expiration in years"
    :param r: "Risk-free rate"
    :param sigma: "Volatility of underlying"
    :param option_type: "'call' or 'put'"
    :return: "Black-Scholes option value"
    '''
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == 'call':
        return S * stats.norm.cdf(d1) - K * np.exp(-r * T) * stats.norm.cdf(d2)
    else:
        return K * np.exp(-r * T) * stats.norm.cdf(-d2) - S * stats.norm.cdf(-d1)


def marginal_risk_contribution(weights, cov_matrix):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Risk budgeting']
    function: "Marginal risk contribution: (Sigma * w)_i / sigma_p for each asset"
    y_as_x: []
    :param weights: "Portfolio weights vector"
    :param cov_matrix: "Covariance matrix of asset returns"
    :return: "Array of marginal risk contributions"
    '''
    weights = np.array(weights, dtype=float)
    cov_matrix = np.array(cov_matrix, dtype=float)
    sigma_w = cov_matrix @ weights
    port_vol = np.sqrt(weights @ cov_matrix @ weights)
    return sigma_w / port_vol


def marginal_var(weights, cov_matrix, confidence=0.95):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Value at Risk decomposition']
    function: "Marginal VaR: partial derivative of VaR with respect to each weight"
    y_as_x: []
    :param weights: "Portfolio weights"
    :param cov_matrix: "Covariance matrix"
    :param confidence: "Confidence level (default 0.95)"
    :return: "Array of marginal VaR per asset"
    '''
    weights = np.array(weights, dtype=float)
    cov_matrix = np.array(cov_matrix, dtype=float)
    z = stats.norm.ppf(confidence)
    port_vol = np.sqrt(weights @ cov_matrix @ weights)
    return z * (cov_matrix @ weights) / port_vol


def margrabe_exchange_option(S1, S2, q1, q2, sigma1, sigma2, rho, T):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Exchange options']
    function: "Margrabe exchange option: right to exchange asset 2 for asset 1"
    y_as_x: []
    :param S1: "Price of asset 1"
    :param S2: "Price of asset 2"
    :param q1: "Continuous dividend yield of asset 1"
    :param q2: "Continuous dividend yield of asset 2"
    :param sigma1: "Volatility of asset 1"
    :param sigma2: "Volatility of asset 2"
    :param rho: "Correlation between asset 1 and asset 2"
    :param T: "Time to expiration in years"
    :return: "Exchange option value"
    '''
    sigma = np.sqrt(sigma1 ** 2 + sigma2 ** 2 - 2 * rho * sigma1 * sigma2)
    d1 = (np.log(S1 / S2) + (q2 - q1 + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S1 * np.exp(-q1 * T) * stats.norm.cdf(d1) - S2 * np.exp(-q2 * T) * stats.norm.cdf(d2)


def market_depth(quantities, prices, reference_price, band_pct=0.01):
    '''
    domain: ['Liquidity risk & market liquidity']
    subdomain: ['Order book analysis']
    function: "Market depth: total executable quantity within a price band around reference"
    y_as_x: []
    :param quantities: "Array of order quantities in the book"
    :param prices: "Array of corresponding order prices"
    :param reference_price: "Reference price (e.g., mid price)"
    :param band_pct: "Price band percentage (default 1%)"
    :return: "Total executable quantity within the band"
    '''
    quantities = np.array(quantities)
    prices = np.array(prices)
    lower = reference_price * (1.0 - band_pct)
    upper = reference_price * (1.0 + band_pct)
    mask = (prices >= lower) & (prices <= upper)
    return np.sum(quantities[mask])


def market_impact_breakeven(total_execution_cost, notional):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Execution cost analysis']
    function: "Market impact breakeven: alpha needed to overcome execution costs"
    y_as_x: []
    :param total_execution_cost: "Total cost of execution (market impact + commissions)"
    :param notional: "Trade notional value"
    :return: "Breakeven alpha (as fraction of notional)"
    '''
    return total_execution_cost / notional


def market_value_added_mva(market_value_firm, invested_capital):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Value creation']
    function: "Market value added: market value of firm minus total invested capital"
    y_as_x: []
    :param market_value_firm: "Total market value of the firm (equity + debt at market)"
    :param invested_capital: "Total invested capital"
    :return: "Market value added"
    '''
    return market_value_firm - invested_capital


def market_neutral_constraint(weights, betas):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio constraints']
    function: "Market-neutral constraint: sum of beta-weighted positions equals zero"
    y_as_x: []
    :param weights: "Portfolio weights"
    :param betas: "Asset betas"
    :return: "Dictionary with 'is_neutral' (bool) and 'portfolio_beta'"
    '''
    weights = np.array(weights)
    betas = np.array(betas)
    port_beta = np.sum(betas * weights)
    return {'is_neutral': bool(np.abs(port_beta) < 1e-8), 'portfolio_beta': port_beta}



def maximum_drawdown(returns):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Drawdown analysis']
    function: "Maximum drawdown: largest peak-to-trough decline in cumulative returns"
    y_as_x: ['calmar_ratio', 'pain_index', 'recovery_factor', 'sterling_ratio']
    :param returns: "Returns series (array-like)"
    :return: "Maximum drawdown (negative number)"
    '''
    returns = np.array(returns)
    cumulative = np.cumprod(1.0 + returns)
    running_max = np.maximum.accumulate(cumulative)
    drawdowns = (cumulative - running_max) / running_max
    return float(np.min(drawdowns))


def maximum_sharpe_portfolio(expected_returns, cov_matrix, risk_free_rate=0.0):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio optimization']
    function: "Maximum Sharpe ratio portfolio: optimize weights to maximize risk-adjusted return"
    y_as_x: []
    :param expected_returns: "Array of expected returns per asset"
    :param cov_matrix: "Covariance matrix of asset returns"
    :param risk_free_rate: "Risk-free rate (default 0)"
    :return: "Dictionary with 'weights', 'expected_return', 'volatility', 'sharpe_ratio'"
    '''
    from scipy.optimize import minimize
    mu = np.array(expected_returns, dtype=float)
    Sigma = np.array(cov_matrix, dtype=float)
    n = len(mu)

    def neg_sharpe(w):
        port_ret = w @ mu
        port_vol = np.sqrt(w @ Sigma @ w)
        return -(port_ret - risk_free_rate) / port_vol

    constraints = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0}]
    bounds = [(0, 1)] * n
    w0 = np.ones(n) / n
    result = minimize(neg_sharpe, w0, method='SLSQP', bounds=bounds, constraints=constraints)
    w_opt = result.x
    ret = w_opt @ mu
    vol = np.sqrt(w_opt @ Sigma @ w_opt)
    return {
        'weights': w_opt,
        'expected_return': ret,
        'volatility': vol,
        'sharpe_ratio': (ret - risk_free_rate) / vol
    }


def mean_absolute_error(y_true, y_pred):
    '''
    domain: ['Quantitative forecasting & machine learning in finance']
    subdomain: ['Model evaluation']
    function: "Mean absolute error: average of absolute differences between actual and predicted"
    y_as_x: []
    :param y_true: "Array of actual values"
    :param y_pred: "Array of predicted values"
    :return: "Mean absolute error"
    '''
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    return np.mean(np.abs(y_true - y_pred))


def mean_squared_error(y_true, y_pred):
    '''
    domain: ['Quantitative forecasting & machine learning in finance']
    subdomain: ['Model evaluation']
    function: "Mean squared error: average of squared differences between actual and predicted"
    y_as_x: []
    :param y_true: "Array of actual values"
    :param y_pred: "Array of predicted values"
    :return: "Mean squared error"
    '''
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    return np.mean((y_true - y_pred) ** 2)


def mean_cvar_optimization(returns, alpha=0.05, target_return=None):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Risk-based optimization']
    function: "Mean-CVaR optimization: minimize CVaR subject to return and weight constraints"
    y_as_x: []
    :param returns: "Returns matrix (n_obs x n_assets)"
    :param alpha: "CVaR confidence tail (e.g. 0.05 for 95% CVaR)"
    :param target_return: "Target portfolio return (if None, minimize CVaR without return target)"
    :return: "Dictionary with 'weights' and 'cvar'"
    '''
    from scipy.optimize import minimize
    returns = np.array(returns, dtype=float)
    n_obs, n_assets = returns.shape
    mu = returns.mean(axis=0)

    def cvar_objective(w):
        port_returns = returns @ w
        var_threshold = np.percentile(port_returns, alpha * 100)
        tail = port_returns[port_returns <= var_threshold]
        if len(tail) == 0:
            return -var_threshold
        return -np.mean(tail)

    constraints = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0}]
    if target_return is not None:
        constraints.append({'type': 'ineq', 'fun': lambda w: w @ mu - target_return})
    bounds = [(0, 1)] * n_assets
    w0 = np.ones(n_assets) / n_assets
    result = minimize(cvar_objective, w0, method='SLSQP', bounds=bounds, constraints=constraints)
    w_opt = result.x
    port_rets = returns @ w_opt
    var_t = np.percentile(port_rets, alpha * 100)
    tail = port_rets[port_rets <= var_t]
    cvar_val = -np.mean(tail) if len(tail) > 0 else -var_t
    return {'weights': w_opt, 'cvar': cvar_val}


def mean_variance_utility(weights, expected_returns, cov_matrix, gamma=1.0):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Utility optimization']
    function: "Mean-variance utility: U = mu'w - (gamma/2) w'Sigma w"
    y_as_x: []
    :param weights: "Portfolio weights"
    :param expected_returns: "Expected return vector"
    :param cov_matrix: "Covariance matrix"
    :param gamma: "Risk aversion parameter (default 1.0)"
    :return: "Mean-variance utility value"
    '''
    w = np.array(weights, dtype=float)
    mu = np.array(expected_returns, dtype=float)
    Sigma = np.array(cov_matrix, dtype=float)
    return float(mu @ w - (gamma / 2.0) * w @ Sigma @ w)


def merton_asset_value_model(equity_value, debt_face, r, T, sigma_a, tolerance=1e-6, max_iter=100):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Structural models']
    function: "Merton model: solve for asset value V_A from equity E = V_A*N(d1) - D*e^{-rT}*N(d2)"
    y_as_x: ['merton_distance_to_default', 'merton_structural_pd']
    :param equity_value: "Observed market equity value"
    :param debt_face: "Face value of debt (D)"
    :param r: "Risk-free rate"
    :param T: "Time to debt maturity in years"
    :param sigma_a: "Initial guess for asset volatility"
    :param tolerance: "Convergence tolerance"
    :param max_iter: "Maximum iterations"
    :return: "Dictionary with 'asset_value', 'asset_volatility', 'd1', 'd2'"
    '''
    V = equity_value + debt_face  # initial guess
    sigma = sigma_a
    for _ in range(max_iter):
        d1 = (np.log(V / debt_face) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        V_new = (equity_value + debt_face * np.exp(-r * T) * stats.norm.cdf(d2)) / stats.norm.cdf(d1)
        sigma_new = sigma * equity_value / (V_new * stats.norm.cdf(d1))
        if abs(V_new - V) < tolerance and abs(sigma_new - sigma) < tolerance:
            V, sigma = V_new, sigma_new
            break
        V, sigma = V_new, sigma_new
    d1 = (np.log(V / debt_face) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return {'asset_value': V, 'asset_volatility': sigma, 'd1': d1, 'd2': d2}


def merton_distance_to_default(asset_value, debt_face, mu_a, sigma_a, T):
    '''
    domain: ['Credit risk']
    subdomain: ['Structural models']
    function: "Merton distance to default: DD = [ln(V/D) + (mu - 0.5*sigma^2)*T] / (sigma*sqrt(T))"
    y_as_x: ['kmv_expected_default_frequency', 'merton_structural_pd']
    :param asset_value: "Current asset value (V_A)"
    :param debt_face: "Face value of debt (D)"
    :param mu_a: "Expected return on assets"
    :param sigma_a: "Asset volatility"
    :param T: "Time horizon in years"
    :return: "Distance to default"
    '''
    return (np.log(asset_value / debt_face) + (mu_a - 0.5 * sigma_a ** 2) * T) / (sigma_a * np.sqrt(T))


def merton_jump_diffusion_asset_process(S0, mu, sigma, lam, jump_mean, jump_std, T, n_steps=252, n_paths=10000):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Jump diffusion models']
    function: "Merton jump diffusion: dS/S = (mu - lambda*k)dt + sigma*dW + dJ"
    y_as_x: []
    :param S0: "Initial asset price"
    :param mu: "Drift rate"
    :param sigma: "Diffusion volatility"
    :param lam: "Jump intensity (expected number of jumps per year)"
    :param jump_mean: "Mean of log-normal jump size"
    :param jump_std: "Std dev of log-normal jump size"
    :param T: "Time horizon in years"
    :param n_steps: "Number of time steps"
    :param n_paths: "Number of simulation paths"
    :return: "Simulated paths array of shape (n_paths, n_steps+1)"
    '''
    dt = T / n_steps
    k = np.exp(jump_mean + 0.5 * jump_std ** 2) - 1.0  # expected jump size
    paths = np.zeros((n_paths, n_steps + 1))
    paths[:, 0] = S0

    for t in range(1, n_steps + 1):
        z = np.random.standard_normal(n_paths)
        # Poisson jumps
        n_jumps = np.random.poisson(lam * dt, n_paths)
        jump_sizes = np.array([np.sum(np.random.normal(jump_mean, jump_std, max(n, 0))) for n in n_jumps])
        diffusion = (mu - lam * k - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * z
        paths[:, t] = paths[:, t - 1] * np.exp(diffusion + jump_sizes)

    return paths


def merton_structural_pd(distance_to_default):
    '''
    domain: ['Credit risk']
    subdomain: ['Structural models']
    function: "Merton structural PD: probability of default = N(-DD)"
    y_as_x: []
    :param distance_to_default: "Distance to default (DD)"
    :return: "Probability of default"
    '''
    return stats.norm.cdf(-distance_to_default)


def metallurgical_gross_margin(metal_selling_price, input_cost_bundle):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Commodity margins']
    function: "Metallurgical gross margin: selling price minus input cost"
    y_as_x: []
    :param metal_selling_price: "Revenue from selling refined metal"
    :param input_cost_bundle: "Total cost of input materials"
    :return: "Gross margin"
    '''
    return metal_selling_price - input_cost_bundle


def mid_price(bid, ask):
    '''
    domain: ['Liquidity risk & market liquidity']
    subdomain: ['Market microstructure']
    function: "Mid price: simple average of bid and ask"
    y_as_x: ['bid_ask_spread', 'effective_spread', 'price_impact', 'quoted_spread_pct']
    :param bid: "Best bid price"
    :param ask: "Best ask price"
    :return: "Mid price"
    '''
    return (bid + ask) / 2.0


def minimum_variance_hedge_ratio(spot_returns, futures_returns):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Hedging']
    function: "Minimum-variance hedge ratio: h* = Cov(dS,dF)/Var(dF)"
    y_as_x: ['minimum_variance_hedged_return']
    :param spot_returns: "Array of spot price changes/returns"
    :param futures_returns: "Array of futures price changes/returns"
    :return: "Optimal hedge ratio"
    '''
    import statsmodels.api as sm
    futures_returns = np.array(futures_returns)
    spot_returns = np.array(spot_returns)
    X = sm.add_constant(futures_returns)
    model = sm.OLS(spot_returns, X).fit()
    return model.params[1]


def minimum_variance_hedged_return(spot_return, hedge_ratio, futures_return):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Hedging']
    function: "Hedged return: R_H = R_S - h* * R_F"
    y_as_x: []
    :param spot_return: "Spot asset return"
    :param hedge_ratio: "Optimal hedge ratio (h*)"
    :param futures_return: "Futures return"
    :return: "Hedged portfolio return"
    '''
    return np.array(spot_return) - hedge_ratio * np.array(futures_return)


def minus_directional_indicator_di(high, low, close, timeperiod=14):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Directional movement']
    function: "Minus directional indicator (-DI): smoothed -DM divided by ATR times 100"
    y_as_x: []
    :param high: "High price series"
    :param low: "Low price series"
    :param close: "Close price series"
    :param period: "Smoothing period (default 14)"
    :return: "-DI series"
    '''
    import talib
    minus_di = talib.MINUS_DI(high, low, close, timeperiod=timeperiod)
    return minus_di


def modified_duration(macaulay_dur, ytm, frequency=2):
    '''
    domain: ['Fixed income & bond math']
    subdomain: ['Duration']
    function: "Modified duration: Macaulay duration divided by (1 + y/m)"
    y_as_x: ['approximate_price_change', 'dollar_duration', 'dv01_over_pvbp']
    :param macaulay_dur: "Macaulay duration"
    :param ytm: "Yield to maturity (annual)"
    :param frequency: "Coupon frequency per year (default 2 for semi-annual)"
    :return: "Modified duration"
    '''
    return macaulay_dur / (1.0 + ytm / frequency)


def modified_irr_mirr(cash_flows, finance_rate, reinvest_rate):
    '''
    domain: ['Corporate finance & capital budgeting']
    subdomain: ['Capital budgeting']
    function: "Modified IRR: (FV positives / |PV negatives|)^(1/n) - 1"
    y_as_x: []
    :param cash_flows: "Array of cash flows (period 0 through n)"
    :param finance_rate: "Finance rate for negative cash flows"
    :param reinvest_rate: "Reinvestment rate for positive cash flows"
    :return: "Modified internal rate of return"
    '''
    import numpy_financial as npf
    return npf.mirr(np.array(cash_flows), finance_rate, reinvest_rate)


def momentum(prices, period=10):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Momentum indicators']
    function: "Momentum: P_t - P_{t-n}"
    y_as_x: []
    :param prices: "Price series"
    :param period: "Lookback period (default 10)"
    :return: "Momentum series"
    '''
    prices = pd.Series(prices)
    return prices - prices.shift(period)


# ================================================================================
# BATCH 6
# ================================================================================

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
    y_as_x: ['benefit_reserve_recursion', 'one_year_death_probability', 'one_year_survival_probability']
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
    dpi = 0.5 * gamma * delta_s ** 2 + theta * dt + vega * delta_sigma
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
    y_as_x: ['asset_swap_spread']
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
    sigma_sq = np.sum(log_hl ** 2) / (4 * np.log(2) * n)
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
    y_as_x: []
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
    y_as_x: ['active_return', 'excess_return', 'mean_variance_utility', 'sharpe_ratio']
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
    y_as_x: ['annuity_present_value', 'future_value', 'net_present_value_npv', 'profitability_index']
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


# ================================================================================
# BATCH 7
# ================================================================================

def profit_factor(returns):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Risk-Adjusted Performance', 'Trading Performance']
    function: "Profit Factor measures the ratio of gross profits to gross losses over a given period. A profit factor greater than 1 indicates a profitable strategy, while a value below 1 indicates losses exceed gains. It is a widely used metric in evaluating trading system performance."
    y_as_x: []
    :param returns: "Returns are the gain or loss generated on an investment over a specific period, expressed as a time series of periodic returns (e.g., daily, monthly)."
    :return: "Computed Profit Factor = sum of positive returns / |sum of negative returns|"
    '''
    import quantstats as qs
    returns = pd.Series(returns)
    return qs.stats.profit_factor(returns)


def profitability_index(pv_future_cash_flows, initial_investment):
    '''
    domain: ['Corporate finance & capital budgeting']
    subdomain: ['Capital Budgeting', 'Investment Appraisal']
    function: "Profitability Index (PI) is a capital budgeting metric that measures the ratio of the present value of future expected cash flows to the initial investment. A PI greater than 1.0 indicates that the project's NPV is positive and the investment is value-creating. It is useful for ranking projects when capital is rationed."
    y_as_x: []
    :param pv_future_cash_flows: "Present value of future cash flows expected from the investment, discounted at the appropriate cost of capital."
    :param initial_investment: "The initial cash outlay required to undertake the project or investment."
    :return: "Computed Profitability Index = PV of future cash flows / Initial Investment"
    '''
    return pv_future_cash_flows / initial_investment


def property_irr(equity_invested, cash_flows, sale_proceeds):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Real Estate Investment Analysis', 'Property Valuation']
    function: "Property IRR is the internal rate of return on a real estate investment, accounting for the initial equity invested, periodic operating cash flows, and the terminal sale proceeds. It is the discount rate that sets the net present value of all equity cash flows to zero."
    y_as_x: []
    :param equity_invested: "The initial equity capital contributed by the investor to acquire the property."
    :param cash_flows: "A list or array of periodic net operating cash flows (after debt service) received during the holding period."
    :param sale_proceeds: "The net proceeds from the sale of the property at the end of the holding period, after deducting transaction costs and remaining loan balance."
    :return: "Computed Property IRR such that 0 = -Equity_0 + sum_t CF_t/(1+IRR)^t + SaleProceeds/(1+IRR)^T"
    '''
    import numpy_financial as npf
    all_cfs = [-equity_invested] + list(cash_flows)
    all_cfs[-1] = all_cfs[-1] + sale_proceeds
    return npf.irr(all_cfs)


def property_value_from_cap_rate(net_operating_income_noi, capitalization_rate):
    '''
    domain: ['Real estate finance']
    subdomain: ['Property Valuation', 'Income Approach']
    function: "Property Value from Cap Rate computes the estimated market value of an income-producing property by dividing its net operating income by the capitalization rate. This is the income capitalization approach widely used in real estate appraisal."
    y_as_x: []
    :param net_operating_income_noi: "Net Operating Income (NOI) is the annual income generated by the property after deducting all operating expenses but before debt service and capital expenditures."
    :param capitalization_rate: "Capitalization Rate (Cap Rate) is the ratio of a property's NOI to its current market value, reflecting the expected rate of return on a real estate investment."
    :return: "Computed Property Value = NOI / Cap Rate"
    '''
    return net_operating_income_noi / capitalization_rate


def prospective_reserve(future_benefits_pv, future_premiums_pv):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Life Insurance Reserving', 'Policy Values']
    function: "Prospective Reserve (V_t) is the actuarial reserve at time t calculated as the present value of future benefits minus the present value of future premiums. It represents the amount the insurer must hold to cover future obligations net of expected future income from the policyholder."
    y_as_x: []
    :param future_benefits_pv: "Present value at time t of all future benefit payments expected under the insurance policy."
    :param future_premiums_pv: "Present value at time t of all future premium payments expected to be received from the policyholder."
    :return: "Computed Prospective Reserve V_t = PV_t(Future Benefits) - PV_t(Future Premiums)"
    '''
    return future_benefits_pv - future_premiums_pv


def protective_put_payoff(S_T, K, premium):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Option Strategies', 'Hedging Strategies']
    function: "Protective Put Payoff is the net payoff from holding a long stock position combined with a long put option. This strategy provides downside protection by limiting the maximum loss to the premium paid plus the difference between the stock price and strike price. The payoff equals the stock price at expiry plus the put payoff minus the premium paid."
    y_as_x: []
    :param S_T: "The stock price at expiration of the option."
    :param K: "The strike price of the put option."
    :param premium: "The premium paid for the put option."
    :return: "Computed Protective Put Payoff = S_T + max(K - S_T, 0) - Premium"
    '''
    return S_T + np.maximum(K - S_T, 0) - premium


def provision_coverage_ratio(loan_loss_reserves, nonperforming_loans):
    '''
    domain: ['Bank regulation, Basel & prudential ratios']
    subdomain: ['Asset Quality', 'Prudential Ratios']
    function: "Provision Coverage Ratio measures the extent to which a bank's loan loss reserves cover its nonperforming loans. A higher ratio indicates greater preparedness for potential credit losses and stronger provisioning adequacy."
    y_as_x: []
    :param loan_loss_reserves: "The total allowance or reserves set aside by the bank to absorb expected losses on its loan portfolio."
    :param nonperforming_loans: "Loans that are in default or close to being in default, typically more than 90 days past due."
    :return: "Computed Provision Coverage Ratio = Loan Loss Reserves / Nonperforming Loans"
    '''
    return loan_loss_reserves / nonperforming_loans


def provision_coverage_ratio_v2(allowance_for_credit_losses, nonperforming_loans):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Credit Risk Management', 'Asset Quality']
    function: "Provision Coverage Ratio (v2) measures the proportion of nonperforming loans covered by the allowance for credit losses (ACL). It indicates how well a bank is provisioned against potential credit losses from its nonperforming loan portfolio."
    y_as_x: []
    :param allowance_for_credit_losses: "The total allowance for credit losses (ACL) recognized under CECL or IFRS 9 accounting standards, representing expected credit losses on the loan portfolio."
    :param nonperforming_loans: "Loans that are in default or close to being in default, typically more than 90 days past due."
    :return: "Computed Coverage Ratio = Allowance for Credit Losses / Nonperforming Loans"
    '''
    return allowance_for_credit_losses / nonperforming_loans


def psa_prepayment_benchmark(month):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Mortgage-Backed Securities', 'Prepayment Modeling']
    function: "PSA (Public Securities Association) Prepayment Benchmark is the standard prepayment model for mortgage-backed securities. At 100% PSA, the conditional prepayment rate (CPR) increases linearly from 0% to 6% over the first 30 months, then remains constant at 6% thereafter. The CPR at a given month equals min(0.06, 0.002 x month)."
    y_as_x: ['prepayment_speed_psa']
    :param month: "The seasoning month of the mortgage pool, starting from month 1."
    :return: "Computed CPR at 100% PSA = min(0.06, 0.002 x month)"
    '''
    return min(0.06, 0.002 * month)


def pti_payment_to_income(monthly_mortgage_payment, monthly_income):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Mortgage Underwriting', 'Affordability Analysis']
    function: "PTI (Payment-to-Income) ratio measures the proportion of a borrower's monthly income consumed by the monthly mortgage payment. It is a key affordability metric used in mortgage underwriting to assess a borrower's ability to service the loan."
    y_as_x: []
    :param monthly_mortgage_payment: "The monthly mortgage payment including principal and interest."
    :param monthly_income: "The borrower's monthly income (gross or net, depending on the context)."
    :return: "Computed PTI = Monthly Mortgage Payment / Income"
    '''
    return monthly_mortgage_payment / monthly_income


def pti_payment_to_income_gross(monthly_loan_payment, gross_monthly_income):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Consumer Lending', 'Mortgage Underwriting']
    function: "PTI (Payment-to-Income) ratio based on gross income measures the proportion of a borrower's gross monthly income consumed by the monthly loan payment. It is used by lenders to assess affordability and repayment capacity before taxes and deductions."
    y_as_x: []
    :param monthly_loan_payment: "The total monthly loan payment including principal and interest."
    :param gross_monthly_income: "The borrower's total monthly income before taxes and deductions."
    :return: "Computed PTI_gross = Monthly Loan Payment / Gross Monthly Income"
    '''
    return monthly_loan_payment / gross_monthly_income


def pti_payment_to_income_net(monthly_loan_payment, net_monthly_income):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Consumer Lending', 'Mortgage Underwriting']
    function: "PTI (Payment-to-Income) ratio based on net income measures the proportion of a borrower's net monthly income consumed by the monthly loan payment. It provides a more conservative affordability assessment by using take-home pay."
    y_as_x: []
    :param monthly_loan_payment: "The total monthly loan payment including principal and interest."
    :param net_monthly_income: "The borrower's monthly income after taxes and deductions (take-home pay)."
    :return: "Computed PTI_net = Monthly Loan Payment / Net Monthly Income"
    '''
    return monthly_loan_payment / net_monthly_income


def public_market_equivalent_pme(distributions, capital_calls, public_index_returns):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Performance Measurement', 'Benchmarking']
    function: "Public Market Equivalent (PME) compares the performance of a private equity fund to a public market index. It calculates the ratio of the future value of distributions (compounded at the public index return) to the future value of capital calls (compounded at the public index return). A PME greater than 1 indicates the fund outperformed the public market."
    y_as_x: ['pme_kaplan_schoar']
    :param distributions: "Array of periodic distributions (cash returned) from the private equity fund."
    :param capital_calls: "Array of periodic capital calls (cash invested) into the private equity fund."
    :param public_index_returns: "Array of periodic returns of the public market benchmark index, corresponding to the same periods as the cash flows."
    :return: "Computed PME = FV(distributions indexed to public benchmark) / FV(capital calls indexed to public benchmark)"
    '''
    distributions = np.array(distributions, dtype=float)
    capital_calls = np.array(capital_calls, dtype=float)
    public_index_returns = np.array(public_index_returns, dtype=float)
    n = len(distributions)
    # Compound each cash flow forward to the end using the public index
    fv_dist = 0.0
    fv_calls = 0.0
    for i in range(n):
        compound = np.prod(1 + public_index_returns[i + 1:]) if i + 1 < n else 1.0
        fv_dist += distributions[i] * compound
        fv_calls += capital_calls[i] * compound
    return fv_dist / fv_calls


def purchasing_power_parity_ppp(domestic_price_level, foreign_price_level):
    '''
    domain: ['FX & international finance']
    subdomain: ['Exchange Rate Theory', 'International Economics']
    function: "Purchasing Power Parity (PPP) theory states that the exchange rate between two currencies should equal the ratio of the two countries' price levels. Under absolute PPP, the equilibrium exchange rate S is determined by the ratio of domestic to foreign price levels."
    y_as_x: ['relative_ppp']
    :param domestic_price_level: "The domestic price level or price index (e.g., CPI) of the home country."
    :param foreign_price_level: "The foreign price level or price index of the foreign country."
    :return: "Computed PPP exchange rate S = P / P*"
    '''
    return domestic_price_level / foreign_price_level


def pure_endowment_apv(n, interest_rate, survival_prob_n):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Life Insurance', 'Actuarial Present Values']
    function: "Pure Endowment APV (Actuarial Present Value) calculates the expected present value of a payment of 1 made at time n, conditional on the insured being alive at that time. It equals the discount factor v^n multiplied by the n-year survival probability _np_x."
    y_as_x: ['endowment_insurance_apv']
    :param n: "The number of years until the endowment payment is due."
    :param interest_rate: "The annual effective interest rate used for discounting."
    :param survival_prob_n: "The probability that the insured person aged x survives n more years (_np_x)."
    :return: "Computed Pure Endowment APV = v^n * _np_x where v = 1/(1+i)"
    '''
    v = 1.0 / (1.0 + interest_rate)
    return (v ** n) * survival_prob_n


def pure_premium(frequency, severity):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Ratemaking', 'Loss Modeling']
    function: "Pure Premium (also known as the loss cost) is the expected loss per exposure unit, calculated as the product of claim frequency and average claim severity. It represents the minimum amount needed to cover expected losses before loading for expenses and profit."
    y_as_x: ['credibility_premium', 'gross_premium_principle']
    :param frequency: "The expected number of claims per exposure unit over the coverage period."
    :param severity: "The expected average cost per claim."
    :return: "Computed Pure Premium = Frequency x Severity"
    '''
    return frequency * severity


def put_payoff(S_T, K):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Option Payoffs', 'Vanilla Options']
    function: "Put Payoff is the terminal payoff of a long put option at expiration. It equals the maximum of the difference between the strike price and the underlying asset price, or zero. The put option is in-the-money when the asset price is below the strike."
    y_as_x: ['protective_put_payoff', 'put_spread_payoff', 'straddle_payoff', 'strangle_payoff']
    :param S_T: "The price of the underlying asset at option expiration."
    :param K: "The strike price of the put option."
    :return: "Computed Put Payoff P_T = max(K - S_T, 0)"
    '''
    return np.maximum(K - S_T, 0)


def put_spread_payoff(S, K1, K2):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Option Strategies', 'Spread Strategies']
    function: "Put Spread Payoff (Bear Put Spread) is the net payoff from buying a put at a higher strike K2 and selling a put at a lower strike K1. The maximum profit is K2 - K1 (when the asset price is below K1), and the maximum loss is the net premium paid."
    y_as_x: []
    :param S: "The price of the underlying asset at option expiration."
    :param K1: "The lower strike price of the short put option."
    :param K2: "The higher strike price of the long put option."
    :return: "Computed Put Spread Payoff = max(K2 - S, 0) - max(K1 - S, 0)"
    '''
    return np.maximum(K2 - S, 0) - np.maximum(K1 - S, 0)


def put_call_parity(S_0, K, r, T):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Option Pricing Theory', 'Arbitrage Relations']
    function: "Put-Call Parity is a fundamental relationship between the prices of European call and put options with the same strike price and expiration. For a non-dividend-paying stock, C - P = S_0 - K*e^(-rT). This function returns the difference C - P implied by put-call parity."
    y_as_x: ['put_call_parity_equity', 'put_call_parity_futures_options']
    :param S_0: "The current spot price of the underlying asset."
    :param K: "The strike price of the options."
    :param r: "The risk-free interest rate (continuously compounded)."
    :param T: "The time to expiration in years."
    :return: "Computed C - P = S_0 - K * e^(-rT)"
    '''
    return S_0 - K * np.exp(-r * T)


def put_call_parity_equity(S_0, K, r, q, T):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Option Pricing Theory', 'Equity Derivatives']
    function: "Put-Call Parity for equity options with continuous dividend yield q. The relationship becomes C - P = S_0*e^(-qT) - K*e^(-rT). This accounts for the present value of dividends foregone by holding the option rather than the stock."
    y_as_x: []
    :param S_0: "The current spot price of the underlying equity."
    :param K: "The strike price of the options."
    :param r: "The risk-free interest rate (continuously compounded)."
    :param q: "The continuous dividend yield on the underlying equity."
    :param T: "The time to expiration in years."
    :return: "Computed C - P = S_0 * e^(-qT) - K * e^(-rT)"
    '''
    return S_0 * np.exp(-q * T) - K * np.exp(-r * T)


def put_call_parity_futures_options(F_0, K, r, T):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Option Pricing Theory', 'Futures Options']
    function: "Put-Call Parity for European options on futures contracts. The relationship is C - P = DF*(F_0 - K) where DF is the discount factor e^(-rT). This is derived from Black's model for futures options."
    y_as_x: []
    :param F_0: "The current futures price."
    :param K: "The strike price of the options."
    :param r: "The risk-free interest rate (continuously compounded)."
    :param T: "The time to expiration in years."
    :return: "Computed C - P = e^(-rT) * (F_0 - K)"
    '''
    return np.exp(-r * T) * (F_0 - K)


def pv_of_tax_shield(tax_shields, r_ts):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Valuation', 'Tax Shield Analysis']
    function: "Present Value of Tax Shield computes the discounted value of future tax savings from interest expense deductibility. It is a key component in the Adjusted Present Value (APV) valuation approach, where the value of the levered firm equals the unlevered value plus the PV of tax shields."
    y_as_x: ['adjusted_present_value_apv']
    :param tax_shields: "An array of periodic tax shield amounts (Interest Expense x Tax Rate) for each future period."
    :param r_ts: "The discount rate appropriate for the tax shield cash flows. Often the cost of debt if the tax shield has the same risk as debt."
    :return: "Computed PV(Tax Shield) = sum_t Tax Shield_t / (1 + r_TS)^t"
    '''
    tax_shields = np.array(tax_shields, dtype=float)
    periods = np.arange(1, len(tax_shields) + 1)
    return np.sum(tax_shields / (1 + r_ts) ** periods)


def quadratic_program(P, q, G=None, h=None, A=None, b=None):
    '''
    domain: ['Quantitative forecasting & machine learning in finance']
    subdomain: ['Optimization', 'Convex Programming']
    function: "Quadratic Program solves the standard quadratic optimization problem: minimize 0.5*x'Px + q'x subject to inequality constraints Gx <= h and equality constraints Ax = b. It is fundamental to portfolio optimization, risk management, and many financial engineering applications."
    y_as_x: []
    :param P: "The positive semidefinite matrix defining the quadratic objective (n x n)."
    :param q: "The linear coefficient vector in the objective function (n x 1)."
    :param G: "The inequality constraint matrix (m x n). Optional."
    :param h: "The inequality constraint vector (m x 1). Optional."
    :param A: "The equality constraint matrix (p x n). Optional."
    :param b: "The equality constraint vector (p x 1). Optional."
    :return: "Optimal solution vector x that minimizes 0.5*x'Px + q'x subject to constraints"
    '''
    import cvxpy as cp
    n = P.shape[0]
    x = cp.Variable(n)
    objective = cp.Minimize(0.5 * cp.quad_form(x, P) + q @ x)
    constraints = []
    if G is not None and h is not None:
        constraints.append(G @ x <= h)
    if A is not None and b is not None:
        constraints.append(A @ x == b)
    prob = cp.Problem(objective, constraints)
    prob.solve()
    return x.value


def quick_ratio(cash, marketable_securities, accounts_receivable, current_liabilities):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Liquidity Analysis', 'Financial Ratios']
    function: "Quick Ratio (Acid-Test Ratio) measures a company's ability to meet its short-term obligations with its most liquid assets. Unlike the current ratio, it excludes inventory and prepaid expenses, providing a more conservative measure of liquidity."
    y_as_x: []
    :param cash: "Cash and cash equivalents held by the company."
    :param marketable_securities: "Short-term investments that can be quickly converted to cash at close to their market value."
    :param accounts_receivable: "Amounts owed to the company by customers for goods or services delivered on credit."
    :param current_liabilities: "Obligations due within one year, including accounts payable, short-term debt, and accrued expenses."
    :return: "Computed Quick Ratio = (Cash + Marketable Securities + AR) / Current Liabilities"
    '''
    return (cash + marketable_securities + accounts_receivable) / current_liabilities


def quoted_spread_pct(ask, bid):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Market Microstructure', 'Transaction Cost Analysis']
    function: "Quoted Spread (%) is the percentage difference between the ask and bid prices relative to the mid-price. It is a primary measure of the cost of immediacy in financial markets and reflects market maker compensation and liquidity conditions."
    y_as_x: ['relative_spread']
    :param ask: "The lowest price at which a seller is willing to sell the security."
    :param bid: "The highest price at which a buyer is willing to buy the security."
    :return: "Computed Quoted Spread (%) = (Ask - Bid) / Mid where Mid = (Ask + Bid) / 2"
    '''
    mid = (ask + bid) / 2.0
    return (ask - bid) / mid


def rate_of_change_roc(close, timeperiod=10):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Momentum Indicators']
    function: "Rate of Change (ROC) is a momentum oscillator that measures the percentage change in price between the current price and the price a specified number of periods ago. Positive ROC indicates upward momentum, negative ROC indicates downward momentum."
    y_as_x: []
    :param close: "Array or Series of closing prices."
    :param timeperiod: "The lookback period (number of periods) for the ROC calculation. Default is 10."
    :return: "Computed ROC = P_t / P_{t-n} - 1 (expressed as percentage)"
    '''
    import talib
    close = np.array(close, dtype=np.float64)
    return talib.ROC(close, timeperiod=timeperiod)


def real_estate_dcf(noi_series, terminal_value, discount_rate):
    '''
    domain: ['Real estate finance']
    subdomain: ['Property Valuation', 'Discounted Cash Flow']
    function: "Real Estate DCF (Discounted Cash Flow) values an income-producing property by discounting its projected net operating income (NOI) over the holding period and the terminal/reversion value at the end of the holding period. This is the fundamental income approach to real estate valuation."
    y_as_x: []
    :param noi_series: "Array of projected net operating income (NOI) for each period of the holding period."
    :param terminal_value: "The expected sale price or residual value of the property at the end of the holding period."
    :param discount_rate: "The discount rate (required rate of return) used to present-value the cash flows."
    :return: "Computed DCF Value = sum_t NOI_t/(1+r)^t + TV/(1+r)^T"
    '''
    import numpy_financial as npf
    noi_series = list(noi_series)
    noi_series[-1] = noi_series[-1] + terminal_value
    cash_flows = [0] + noi_series  # npv expects CF_0 at index 0
    return npf.npv(discount_rate, cash_flows)


def real_exchange_rate(nominal_rate, foreign_price_level, domestic_price_level):
    '''
    domain: ['FX & international finance']
    subdomain: ['Exchange Rate Analysis', 'International Economics']
    function: "Real Exchange Rate adjusts the nominal exchange rate for the relative price levels between two countries. It measures the purchasing power of one currency relative to another and is a key indicator of international competitiveness. An increase indicates real depreciation of the domestic currency."
    y_as_x: []
    :param nominal_rate: "The nominal exchange rate S (domestic currency per unit of foreign currency)."
    :param foreign_price_level: "The foreign country's price level or price index P*."
    :param domestic_price_level: "The domestic country's price level or price index P."
    :return: "Computed Real Exchange Rate q = S * P* / P"
    '''
    return nominal_rate * foreign_price_level / domestic_price_level


def real_yield_bond_pricing(real_cash_flows, real_yield):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Inflation-Linked Bonds', 'Bond Pricing']
    function: "Real Yield Bond Pricing values an inflation-linked bond (e.g., TIPS) by discounting its real cash flows at the real yield. The real cash flows are the coupon and principal payments in real (inflation-adjusted) terms."
    y_as_x: []
    :param real_cash_flows: "Array of real (inflation-adjusted) cash flows from the bond for each period."
    :param real_yield: "The real yield (yield adjusted for inflation) used to discount the cash flows."
    :return: "Computed bond price P = sum_t Real CF_t / (1 + real_y)^t"
    '''
    real_cash_flows = np.array(real_cash_flows, dtype=float)
    periods = np.arange(1, len(real_cash_flows) + 1)
    return np.sum(real_cash_flows / (1 + real_yield) ** periods)


def realized_beta(asset_returns_intraday, market_returns_intraday):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Beta Estimation', 'High-Frequency Finance']
    function: "Realized Beta measures the sensitivity of an asset's returns to market returns using intraday (high-frequency) data. It is computed as the ratio of the realized covariance between the asset and the market to the realized variance of the market."
    y_as_x: []
    :param asset_returns_intraday: "Array of intraday returns of the asset."
    :param market_returns_intraday: "Array of intraday returns of the market index."
    :return: "Computed Realized Beta = Cov_intraday(asset, market) / Var_intraday(market)"
    '''
    asset_returns_intraday = np.array(asset_returns_intraday, dtype=float)
    market_returns_intraday = np.array(market_returns_intraday, dtype=float)
    cov = np.sum(asset_returns_intraday * market_returns_intraday)
    var_market = np.sum(market_returns_intraday ** 2)
    return cov / var_market


def realized_hedge_effectiveness(hedged_returns, unhedged_returns):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Hedge Effectiveness', 'Risk Management']
    function: "Realized Hedge Effectiveness measures how much of the unhedged position's variance has been eliminated by the hedge. A value of 1 indicates a perfect hedge (all variance eliminated), while 0 indicates the hedge has no effect. Negative values indicate the hedge increased variance."
    y_as_x: []
    :param hedged_returns: "Array of returns on the hedged position (asset + hedge instrument)."
    :param unhedged_returns: "Array of returns on the unhedged position (asset only)."
    :return: "Computed HE = 1 - Var(Hedged Position) / Var(Unhedged Position)"
    '''
    return 1.0 - np.var(hedged_returns) / np.var(unhedged_returns)


def realized_spread(trade_price, mid_price_future, side):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Market Microstructure', 'Transaction Cost Analysis']
    function: "Realized Spread is a measure of market maker profitability that compares the trade price to the midpoint some time after the trade. It captures the actual revenue to the liquidity provider after adverse selection costs. A positive realized spread indicates compensation to the market maker."
    y_as_x: ['adverse_selection_cost']
    :param trade_price: "The price at which the trade was executed."
    :param mid_price_future: "The mid-price at time t+Delta (some time after the trade, e.g., 5 minutes)."
    :param side: "Trade direction indicator: +1 for buyer-initiated, -1 for seller-initiated."
    :return: "Computed Realized Spread = 2 * side * (Trade Price - Mid_{t+Delta})"
    '''
    return 2.0 * side * (trade_price - mid_price_future)


def realized_variance(intraday_returns):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Volatility Estimation', 'High-Frequency Finance']
    function: "Realized Variance is a non-parametric estimator of the variance of asset returns over a given period, computed as the sum of squared intraday returns. It provides a model-free measure of ex-post volatility using high-frequency data."
    y_as_x: ['realized_volatility', 'bipower_variation', 'variance_swap_fair_strike']
    :param intraday_returns: "Array of intraday (high-frequency) log returns."
    :return: "Computed Realized Variance RV_t = sum_{i=1}^n r_{t,i}^2"
    '''
    intraday_returns = np.array(intraday_returns, dtype=float)
    return np.sum(intraday_returns ** 2)


def realized_volatility(intraday_returns):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Volatility Estimation', 'High-Frequency Finance']
    function: "Realized Volatility is the square root of realized variance, providing an annualized or period-specific measure of actual price fluctuations based on high-frequency data. It is a model-free volatility estimator widely used for volatility forecasting and risk management."
    y_as_x: ['yang_zhang_volatility']
    :param intraday_returns: "Array of intraday (high-frequency) returns."
    :return: "Computed Realized Volatility RVOL = sqrt(sum of squared intraday returns)"
    '''
    intraday_returns = np.array(intraday_returns, dtype=float)
    return np.sqrt(np.sum(intraday_returns ** 2))


def receivables_turnover(revenue, average_accounts_receivable):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Efficiency Ratios', 'Working Capital Management']
    function: "Receivables Turnover measures how efficiently a company collects revenue from its credit customers. A higher ratio indicates faster collection of receivables. It is the inverse of the DSO (Days Sales Outstanding) when annualized."
    y_as_x: ['days_sales_outstanding_dso']
    :param revenue: "Total revenue (net sales) for the period."
    :param average_accounts_receivable: "The average accounts receivable balance during the period, typically (beginning AR + ending AR) / 2."
    :return: "Computed Receivables Turnover = Revenue / Average AR"
    '''
    return revenue / average_accounts_receivable


def recovery_factor(net_profit, maximum_drawdown):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Risk-Adjusted Performance', 'Trading Performance']
    function: "Recovery Factor measures the ratio of net profit to the absolute value of maximum drawdown. It indicates how many times the strategy's net profit exceeds its worst peak-to-trough decline. A higher recovery factor indicates better risk-adjusted performance."
    y_as_x: []
    :param net_profit: "The total net profit from the strategy or portfolio over the measurement period."
    :param maximum_drawdown: "The maximum drawdown (expressed as a positive value or absolute value) experienced during the period."
    :return: "Computed Recovery Factor = Net Profit / |Max Drawdown|"
    '''
    return net_profit / abs(maximum_drawdown)


def recovery_rate(loss_given_default):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Loss Estimation', 'Credit Risk Parameters']
    function: "Recovery Rate is the percentage of the outstanding exposure that is recovered after a borrower defaults. It is the complement of the Loss Given Default (LGD), representing the proportion of the loan that the lender can expect to recover through collateral liquidation, guarantees, or other means."
    y_as_x: ['cds_par_spread', 'cds_spread_approximation', 'loss_given_default', 'reduced_form_cds_hazard_relation']
    :param loss_given_default: "Loss Given Default (LGD) is the proportion of the exposure that is lost if a borrower defaults, expressed as a decimal (e.g., 0.40 for 40%)."
    :return: "Computed Recovery Rate = 1 - LGD"
    '''
    return 1.0 - loss_given_default


def reduced_form_cds_hazard_relation(hazard_rate, loss_given_default):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit Derivatives', 'Hazard Rate Modeling']
    function: "Reduced-Form CDS Hazard Relation is the approximation that relates the CDS spread to the hazard rate (default intensity) and Loss Given Default. Under the reduced-form framework, the CDS spread is approximately equal to the hazard rate multiplied by LGD."
    y_as_x: []
    :param hazard_rate: "The hazard rate (default intensity) lambda, representing the instantaneous probability of default per unit time."
    :param loss_given_default: "Loss Given Default (LGD), the fraction of exposure lost upon default."
    :return: "Computed CDS Spread approximation = lambda x LGD"
    '''
    return hazard_rate * loss_given_default


def refinance_proceeds(new_loan_amount, old_loan_balance, fees):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Mortgage Refinancing', 'Consumer Lending']
    function: "Refinance Proceeds calculates the net cash available to the borrower after refinancing. It equals the new loan amount minus the payoff of the old loan balance minus all refinancing fees and closing costs."
    y_as_x: []
    :param new_loan_amount: "The principal amount of the new refinanced loan."
    :param old_loan_balance: "The remaining balance on the existing loan being refinanced."
    :param fees: "Total refinancing costs including origination fees, appraisal fees, title fees, and other closing costs."
    :return: "Computed Refinance Proceeds = New Loan - Old Loan - Fees"
    '''
    return new_loan_amount - old_loan_balance - fees


def relative_ppp(domestic_inflation, foreign_inflation):
    '''
    domain: ['FX & international finance']
    subdomain: ['Exchange Rate Theory', 'International Economics']
    function: "Relative Purchasing Power Parity predicts that the change in the exchange rate will approximately equal the inflation differential between two countries. If the domestic inflation exceeds the foreign inflation, the domestic currency is expected to depreciate."
    y_as_x: []
    :param domestic_inflation: "The domestic inflation rate (pi_d) over the period."
    :param foreign_inflation: "The foreign inflation rate (pi_f) over the period."
    :return: "Computed expected exchange rate change Delta S / S = pi_d - pi_f"
    '''
    return domestic_inflation - foreign_inflation


def relative_spread(ask, bid):
    '''
    domain: ['Liquidity risk & market liquidity']
    subdomain: ['Market Microstructure', 'Spread Analysis']
    function: "Relative Spread measures the bid-ask spread as a proportion of the mid-price. It is equivalent to the quoted spread percentage and provides a normalized measure of trading costs that is comparable across securities with different price levels."
    y_as_x: []
    :param ask: "The lowest price at which a seller is willing to sell the security."
    :param bid: "The highest price at which a buyer is willing to buy the security."
    :return: "Computed Relative Spread = (Ask - Bid) / Mid where Mid = (Ask + Bid) / 2"
    '''
    mid = (ask + bid) / 2.0
    return (ask - bid) / mid


def relative_strength_index_rsi(close, timeperiod=14):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Momentum Indicators', 'Overbought/Oversold']
    function: "Relative Strength Index (RSI) is a momentum oscillator that measures the speed and magnitude of recent price changes to evaluate overbought or oversold conditions. RSI ranges from 0 to 100, with readings above 70 indicating overbought conditions and below 30 indicating oversold conditions."
    y_as_x: ['stochastic_rsi']
    :param close: "Array or Series of closing prices."
    :param timeperiod: "The lookback period for the RSI calculation. Default is 14."
    :return: "Computed RSI = 100 - 100/(1+RS) where RS = AvgGain / AvgLoss"
    '''
    import talib
    close = np.array(close, dtype=np.float64)
    return talib.RSI(close, timeperiod=timeperiod)


def rent_coverage_ratio(gross_monthly_income, monthly_rent):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Rental Affordability', 'Tenant Screening']
    function: "Rent Coverage Ratio measures a tenant's ability to pay rent by comparing their gross monthly income to the monthly rent. A higher ratio indicates greater ability to afford the rent. Landlords typically require a ratio of at least 2.5 to 3.0."
    y_as_x: []
    :param gross_monthly_income: "The tenant's total gross monthly income before taxes and deductions."
    :param monthly_rent: "The monthly rent payment required."
    :return: "Computed Rent Coverage = Gross Monthly Income / Monthly Rent"
    '''
    return gross_monthly_income / monthly_rent


def repricing_gap(rate_sensitive_assets, rate_sensitive_liabilities):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Interest Rate Risk', 'Asset-Liability Management']
    function: "Repricing Gap measures the difference between rate-sensitive assets and rate-sensitive liabilities in a given time bucket. A positive gap means more assets than liabilities reprice in that period, making the bank's net interest income benefit from rising rates."
    y_as_x: ['cumulative_gap']
    :param rate_sensitive_assets: "The total value of assets that will reprice (have their interest rates reset) within the time bucket."
    :param rate_sensitive_liabilities: "The total value of liabilities that will reprice within the time bucket."
    :return: "Computed Gap_t = Rate Sensitive Assets_t - Rate Sensitive Liabilities_t"
    '''
    return rate_sensitive_assets - rate_sensitive_liabilities


def residual_income(net_income, cost_of_equity, beginning_equity):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Performance Measurement', 'Value-Based Management']
    function: "Residual Income measures the economic profit earned by a firm or division above the required return on equity. It is the net income minus the equity charge (cost of equity multiplied by the beginning book equity). Positive residual income indicates value creation."
    y_as_x: ['residual_income_valuation']
    :param net_income: "Net Income is the total profit after all expenses, taxes, and interest have been deducted from revenue."
    :param cost_of_equity: "The required rate of return on equity (R_e), representing the minimum return shareholders expect."
    :param beginning_equity: "The book value of equity at the beginning of the period."
    :return: "Computed Residual Income RI = Net Income - R_e x Beginning Equity"
    '''
    return net_income - cost_of_equity * beginning_equity


def residual_income_valuation(book_value_0, residual_incomes, discount_rate):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Intrinsic Valuation', 'Residual Income Model']
    function: "Residual Income Valuation estimates the intrinsic value of a stock as the current book value plus the present value of expected future residual incomes. This model is particularly useful when dividends are unpredictable and links accounting data to intrinsic value."
    y_as_x: []
    :param book_value_0: "The current book value per share (B_0)."
    :param residual_incomes: "Array of projected residual income values for each future period."
    :param discount_rate: "The cost of equity used to discount future residual incomes."
    :return: "Computed V_0 = B_0 + sum_t RI_t / (1+r)^t"
    '''
    residual_incomes = np.array(residual_incomes, dtype=float)
    periods = np.arange(1, len(residual_incomes) + 1)
    pv_ri = np.sum(residual_incomes / (1 + discount_rate) ** periods)
    return book_value_0 + pv_ri


def retention_ratio(dividend_payout_ratio):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Dividend Policy', 'Growth Analysis']
    function: "Retention Ratio (Plowback Ratio) measures the proportion of net income retained by the company rather than distributed as dividends. It is a key input to the sustainable growth rate calculation (g = ROE x Retention Ratio)."
    y_as_x: ['sustainable_growth_rate']
    :param dividend_payout_ratio: "Dividend Payout Ratio is the proportion of net income paid out as dividends, expressed as a decimal."
    :return: "Computed Retention Ratio = 1 - Dividend Payout Ratio"
    '''
    return 1.0 - dividend_payout_ratio


def retrospective_reserve(accumulated_premiums, accumulated_benefits, accumulated_expenses):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Life Insurance Reserving', 'Policy Values']
    function: "Retrospective Reserve calculates the policy reserve at time t by looking backward at the accumulated value of past premiums received minus the accumulated value of past benefits paid and expenses incurred. Under standard actuarial assumptions, it equals the prospective reserve."
    y_as_x: []
    :param accumulated_premiums: "The accumulated (future) value at time t of all premiums received up to time t."
    :param accumulated_benefits: "The accumulated (future) value at time t of all benefits paid up to time t."
    :param accumulated_expenses: "The accumulated (future) value at time t of all expenses incurred up to time t."
    :return: "Computed Retrospective Reserve V_t = Accumulated Value(Past Premiums - Past Benefits - Expenses)"
    '''
    return accumulated_premiums - accumulated_benefits - accumulated_expenses


def return_on_assets_roa(net_income, average_assets):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Profitability Ratios', 'Financial Statement Analysis']
    function: "Return on Assets (ROA) measures how efficiently a company uses its assets to generate profit. It indicates the percentage of profit earned relative to total assets, showing management effectiveness in deploying the company's asset base."
    y_as_x: ['piotroski_f_score']
    :param net_income: "Net Income is the total profit after all expenses, taxes, and interest have been deducted from revenue."
    :param average_assets: "The average total assets during the period, typically (beginning assets + ending assets) / 2."
    :return: "Computed ROA = Net Income / Average Assets"
    '''
    return net_income / average_assets


def return_on_capital_employed_roce(ebit, capital_employed):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Profitability Ratios', 'Capital Efficiency']
    function: "Return on Capital Employed (ROCE) measures the profitability and efficiency with which a company's capital is deployed. It uses EBIT (not net income) to provide a pre-tax, pre-interest perspective on returns, making it useful for comparing companies with different capital structures."
    y_as_x: []
    :param ebit: "EBIT (Earnings Before Interest and Taxes) measures a company's profitability from core operations."
    :param capital_employed: "Capital Employed is the total capital invested in the business, typically Total Assets - Current Liabilities, or Equity + Long-term Debt."
    :return: "Computed ROCE = EBIT / Capital Employed"
    '''
    return ebit / capital_employed


def return_on_equity_roe(net_income, average_equity):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Profitability Ratios', 'Shareholder Returns']
    function: "Return on Equity (ROE) measures the return generated on shareholders' equity investment. It is one of the most important profitability metrics, indicating how effectively management uses equity capital to generate profits. It is also a key input to the DuPont decomposition and sustainable growth rate."
    y_as_x: ['sustainable_growth_rate', 'residual_income']
    :param net_income: "Net Income is the total profit after all expenses, taxes, and interest have been deducted from revenue."
    :param average_equity: "The average shareholders' equity during the period, typically (beginning equity + ending equity) / 2."
    :return: "Computed ROE = Net Income / Average Equity"
    '''
    return net_income / average_equity


def return_on_invested_capital_roic(nopat, average_invested_capital):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Profitability Ratios', 'Capital Efficiency']
    function: "Return on Invested Capital (ROIC) measures how efficiently a company generates returns on the total capital invested by both equity and debt holders. It uses NOPAT (Net Operating Profit After Tax) to provide a tax-adjusted but capital-structure-neutral profitability measure."
    y_as_x: []
    :param nopat: "NOPAT (Net Operating Profit After Tax) = EBIT x (1 - Tax Rate). It represents the after-tax operating profit available to all capital providers."
    :param average_invested_capital: "Average Invested Capital is the average total capital invested in the business (Equity + Debt - Excess Cash), typically averaged over the period."
    :return: "Computed ROIC = NOPAT / Average Invested Capital"
    '''
    return nopat / average_invested_capital


def return_on_regulatory_capital_rorc(expected_profit, regulatory_capital):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Bank Performance', 'Capital Management']
    function: "Return on Regulatory Capital (RORC) measures the profitability of a banking activity relative to the regulatory or economic capital allocated to it. It is used to assess whether a business line generates sufficient returns to justify the capital consumed."
    y_as_x: []
    :param expected_profit: "The expected profit or net income generated by the business activity."
    :param regulatory_capital: "The regulatory or economic capital allocated to support the business activity."
    :return: "Computed RORC = Expected Profit / Regulatory Capital"
    '''
    return expected_profit / regulatory_capital


def revenue_growth(revenue_current, revenue_previous):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Growth Analysis', 'Financial Statement Analysis']
    function: "Revenue Growth measures the percentage change in a company's revenue from one period to the next. It is a fundamental indicator of a company's top-line momentum and market demand for its products or services."
    y_as_x: []
    :param revenue_current: "Revenue in the current period (Revenue_t)."
    :param revenue_previous: "Revenue in the previous period (Revenue_{t-1})."
    :return: "Computed Revenue Growth g_t = Revenue_t / Revenue_{t-1} - 1"
    '''
    return revenue_current / revenue_previous - 1.0


def rho(K, T, r, d2_value, option_type='call'):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Option Greeks', 'Risk Sensitivities']
    function: "Rho measures the sensitivity of an option's price to changes in the risk-free interest rate. For a European call, Rho = K*T*e^(-rT)*N(d2), and for a European put, Rho = -K*T*e^(-rT)*N(-d2). It is typically the smallest of the major Greeks."
    y_as_x: ['cross_hedge_ratio', 'heston_asset_process', 'margrabe_exchange_option', 'vasicek_one_factor_portfolio_loss_quantile']
    :param K: "The strike price of the option."
    :param T: "The time to expiration in years."
    :param r: "The risk-free interest rate (continuously compounded)."
    :param d2_value: "The d2 value from the Black-Scholes-Merton formula."
    :param option_type: "Option type: 'call' or 'put'. Default is 'call'."
    :return: "Computed Rho for call = K * T * e^(-rT) * N(d2); for put = -K * T * e^(-rT) * N(-d2)"
    '''
    from scipy.stats import norm
    if option_type == 'call':
        return K * T * np.exp(-r * T) * norm.cdf(d2_value)
    else:
        return -K * T * np.exp(-r * T) * norm.cdf(-d2_value)


def risk_parity_objective(returns, cov_matrix=None):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Construction', 'Risk Budgeting']
    function: "Risk Parity Objective seeks portfolio weights such that each asset contributes equally to the total portfolio risk. The optimization minimizes the sum of squared differences between risk contributions across all asset pairs. This approach avoids concentration risk and produces more diversified portfolios."
    y_as_x: ['equal_risk_contribution']
    :param returns: "DataFrame or array of asset returns used to estimate the covariance matrix."
    :param cov_matrix: "The covariance matrix of asset returns. If None, it will be estimated from returns."
    :return: "Optimal portfolio weights achieving equal risk contribution"
    '''
    import riskfolio as rp
    returns = pd.DataFrame(returns)
    port = rp.Portfolio(returns=returns)
    if cov_matrix is not None:
        port.cov = cov_matrix
    else:
        port.assets_stats(method_mu='hist', method_cov='hist')
    weights = port.rp_optimization(model='Classic', rm='MV', hist=True)
    return weights


def riskmetrics_covariance(returns, decay_factor=0.94):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Covariance Estimation', 'EWMA Models']
    function: "RiskMetrics Covariance uses the exponentially weighted moving average (EWMA) approach to estimate the time-varying covariance matrix. The decay factor (lambda) controls the rate at which older observations lose influence. The standard RiskMetrics value is lambda = 0.94 for daily data."
    y_as_x: []
    :param returns: "DataFrame or 2D array of asset returns (T x N) where T is the number of observations and N is the number of assets."
    :param decay_factor: "The EWMA decay factor lambda. Default is 0.94 (RiskMetrics daily)."
    :return: "Computed time-varying covariance matrix Sigma_t = lambda * Sigma_{t-1} + (1-lambda) * r_{t-1} * r_{t-1}'"
    '''
    returns = np.array(returns, dtype=float)
    T, N = returns.shape
    cov = np.outer(returns[0], returns[0])
    for t in range(1, T):
        cov = decay_factor * cov + (1 - decay_factor) * np.outer(returns[t], returns[t])
    return cov


def risk_neutral_probability(r, q, dt, u, d):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Binomial Trees', 'Option Pricing']
    function: "Risk-Neutral Probability is the probability used in the binomial option pricing model to discount expected payoffs at the risk-free rate. It ensures the expected return on the underlying asset under the risk-neutral measure equals the risk-free rate minus the dividend yield."
    y_as_x: ['binomial_option_pricing', 'american_option_binomial_pricing']
    :param r: "The risk-free interest rate (continuously compounded)."
    :param q: "The continuous dividend yield on the underlying asset."
    :param dt: "The length of each time step in the binomial tree (Delta t)."
    :param u: "The up factor in the binomial tree."
    :param d: "The down factor in the binomial tree."
    :return: "Computed risk-neutral probability p = (e^{(r-q)*dt} - d) / (u - d)"
    '''
    return (np.exp((r - q) * dt) - d) / (u - d)


def risk_weighted_assets_rwa(exposures, risk_weights):
    '''
    domain: ['Bank regulation, Basel & prudential ratios']
    subdomain: ['Capital Adequacy', 'Basel Framework']
    function: "Risk-Weighted Assets (RWA) is the total of all assets held by a bank weighted by their credit risk according to regulatory guidelines. RWA is the denominator in key capital adequacy ratios (CET1, Tier 1, Total Capital). Assets with higher risk receive higher weights."
    y_as_x: ['cet1_ratio', 'tier_1_capital_ratio', 'total_capital_ratio', 'basel_standardized_capital_requirement', 'mrel_over_tlac_ratio', 'stress_capital_buffer']
    :param exposures: "Array of exposure amounts for each asset class or credit exposure."
    :param risk_weights: "Array of regulatory risk weights corresponding to each exposure (e.g., 0% for sovereign, 20% for banks, 100% for corporate)."
    :return: "Computed RWA = sum_i Exposure_i x RiskWeight_i"
    '''
    exposures = np.array(exposures, dtype=float)
    risk_weights = np.array(risk_weights, dtype=float)
    return np.sum(exposures * risk_weights)


def roc_auc(y_true, y_score):
    '''
    domain: ['Quantitative forecasting & machine learning in finance']
    subdomain: ['Model Evaluation', 'Classification Metrics']
    function: "ROC AUC (Area Under the Receiver Operating Characteristic Curve) measures the ability of a binary classifier to distinguish between positive and negative classes. AUC ranges from 0 to 1, where 1 indicates perfect classification and 0.5 indicates no discriminative power (random guessing). It is widely used in credit scoring and default prediction."
    y_as_x: []
    :param y_true: "Array of true binary labels (0 or 1)."
    :param y_score: "Array of predicted probabilities or scores for the positive class."
    :return: "Computed AUC = area under the ROC curve"
    '''
    from sklearn.metrics import roc_auc_score
    return roc_auc_score(y_true, y_score)


def rogers_satchell_volatility(high, low, open_price, close):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Volatility Estimation', 'Range-Based Estimators']
    function: "Rogers-Satchell Volatility is a range-based volatility estimator that uses open, high, low, and close prices. Unlike Parkinson or Garman-Klass, it does not assume a zero drift, making it more accurate for trending markets. It remains unbiased in the presence of a non-zero mean return."
    y_as_x: ['yang_zhang_volatility']
    :param high: "Array of high prices for each period."
    :param low: "Array of low prices for each period."
    :param open_price: "Array of opening prices for each period."
    :param close: "Array of closing prices for each period."
    :return: "Computed Rogers-Satchell variance sigma_RS^2 = mean of (ln(H/O)*ln(H/C) + ln(L/O)*ln(L/C))"
    '''
    high = np.array(high, dtype=float)
    low = np.array(low, dtype=float)
    open_price = np.array(open_price, dtype=float)
    close = np.array(close, dtype=float)
    rs = np.log(high / open_price) * np.log(high / close) + np.log(low / open_price) * np.log(low / close)
    return np.sqrt(np.mean(rs))


def roll_implied_spread(prices):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Market Microstructure', 'Spread Estimation']
    function: "Roll Implied Spread estimates the effective bid-ask spread from transaction price data alone, without requiring quote data. It exploits the negative serial covariance induced by the bid-ask bounce: the spread equals 2 times the square root of the negative autocovariance of price changes."
    y_as_x: []
    :param prices: "Array or Series of transaction prices."
    :return: "Computed Roll Spread = 2 * sqrt(-Cov(Delta p_t, Delta p_{t-1})) if covariance is negative, else 0"
    '''
    prices = np.array(prices, dtype=float)
    dp = np.diff(prices)
    cov = np.cov(dp[1:], dp[:-1])[0, 1]
    if cov < 0:
        return 2.0 * np.sqrt(-cov)
    else:
        return 0.0


def roll_rate(balance_migrating_worse, prior_bucket_balance):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Delinquency Analysis', 'Credit Risk Monitoring']
    function: "Roll Rate measures the proportion of loan balances that migrate from one delinquency bucket to a worse one over a given period. It is a key input for estimating future defaults and losses in consumer lending and structured finance. Higher roll rates indicate deteriorating credit quality."
    y_as_x: []
    :param balance_migrating_worse: "The total balance of loans that migrated to a worse delinquency bucket during the period."
    :param prior_bucket_balance: "The total balance of loans in the prior (better) delinquency bucket at the beginning of the period."
    :return: "Computed Roll Rate = balances migrating to worse bucket / prior bucket balance"
    '''
    return balance_migrating_worse / prior_bucket_balance


def roll_spread_estimator(prices):
    '''
    domain: ['Liquidity risk & market liquidity']
    subdomain: ['Market Microstructure', 'Spread Estimation']
    function: "Roll Spread Estimator estimates the effective bid-ask spread from the serial covariance of price changes. It is based on the model where observed price changes alternate between bid and ask prices. The estimator equals 2*sqrt(-Cov(DP_t, DP_{t-1}))."
    y_as_x: []
    :param prices: "Array or Series of transaction prices."
    :return: "Computed Roll Spread = 2 * sqrt(-Cov(DeltaP_t, DeltaP_{t-1})) if covariance is negative, else 0"
    '''
    prices = np.array(prices, dtype=float)
    dp = np.diff(prices)
    cov = np.cov(dp[1:], dp[:-1])[0, 1]
    if cov < 0:
        return 2.0 * np.sqrt(-cov)
    else:
        return 0.0


def roll_yield(futures_return, spot_return, collateral_return):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Commodity Returns', 'Futures Roll']
    function: "Roll Yield is the component of commodity futures return attributable to the rolling of futures contracts. In backwardated markets, roll yield is positive as the investor buys cheaper near-month contracts and rolls into more expensive far-month contracts. It is calculated as the residual after subtracting spot and collateral returns."
    y_as_x: ['commodity_carry_return']
    :param futures_return: "The total return from the futures position."
    :param spot_return: "The return from changes in the spot price of the commodity."
    :param collateral_return: "The return earned on the collateral posted for the futures position (typically the risk-free rate)."
    :return: "Computed Roll Yield = Futures Return - Spot Return - Collateral Return"
    '''
    return futures_return - spot_return - collateral_return


def roll_down_return(duration, delta_yield):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Bond Return Attribution', 'Yield Curve Strategies']
    function: "Roll-Down Return estimates the price return on a bond from the passage of time as it 'rolls down' the yield curve toward maturity. As a bond's remaining maturity shortens, it typically moves to a lower yield on an upward-sloping curve, generating a positive return. It is approximated as the negative of duration times the yield change from the curve slide."
    y_as_x: ['bond_carry_and_roll', 'yield_curve_carry']
    :param duration: "The modified duration of the bond, measuring price sensitivity to yield changes."
    :param delta_yield: "The change in yield (negative if rolling down a normal curve) from the curve slide."
    :return: "Computed Roll-Down Return approximation = -Duration x Delta Yield from curve slide"
    '''
    return -duration * delta_yield


def rsi(close, window=14):
    '''
    domain: ['Technical analysis']
    subdomain: ['Momentum Indicators', 'Overbought/Oversold']
    function: "RSI (Relative Strength Index) is a momentum oscillator measuring the speed and change of price movements. It oscillates between 0 and 100, with values above 70 typically indicating overbought conditions and below 30 indicating oversold conditions."
    y_as_x: ['stochastic_rsi']
    :param close: "Array or Series of closing prices."
    :param window: "The lookback window for the RSI calculation. Default is 14."
    :return: "Computed RSI = 100 - 100/(1 + RS) where RS = AvgGain/AvgLoss"
    '''
    import talib
    close = np.array(close, dtype=np.float64)
    return talib.RSI(close, timeperiod=window)


def rvpi(residual_value_nav, paid_in_capital):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Fund Performance', 'Unrealized Returns']
    function: "RVPI (Residual Value to Paid-In Capital) measures the ratio of a fund's remaining (unrealized) net asset value to the total capital invested. It represents the unrealized portion of a fund's total value and, combined with DPI, equals TVPI."
    y_as_x: ['tvpi']
    :param residual_value_nav: "The current net asset value (NAV) of the fund's unrealized investments."
    :param paid_in_capital: "The total capital contributed (called) by limited partners to the fund."
    :return: "Computed RVPI = Residual Value (NAV) / Paid-In Capital"
    '''
    return residual_value_nav / paid_in_capital


def sabr_implied_vol(F, K, T, alpha, beta, rho_param, nu):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Volatility Surface', 'Stochastic Volatility']
    function: "SABR Implied Volatility computes the Black-Scholes implied volatility using the SABR (Stochastic Alpha Beta Rho) model. The SABR model is widely used in interest rate and FX markets to capture the volatility smile/skew. It parameterizes the dynamics of the forward rate and its volatility."
    y_as_x: ['local_over_stochastic_volatility_surface_interpolation']
    :param F: "The forward price of the underlying asset."
    :param K: "The strike price of the option."
    :param T: "The time to expiration in years."
    :param alpha: "The initial (ATM) volatility parameter of the SABR model."
    :param beta: "The elasticity parameter (0 <= beta <= 1). Beta=0 gives normal model, beta=1 gives lognormal."
    :param rho_param: "The correlation between the forward rate and its volatility (-1 < rho < 1)."
    :param nu: "The volatility of volatility (vol-of-vol) parameter."
    :return: "Computed SABR implied Black-Scholes volatility sigma_BS"
    '''
    # Hagan et al. SABR approximation formula
    if abs(F - K) < 1e-12:
        # ATM case
        FK_mid = F
        logFK = 0.0
        z = 0.0
        x_z = 1.0
    else:
        FK_mid = (F * K) ** ((1 - beta) / 2.0)
        logFK = np.log(F / K)
        z = (nu / alpha) * FK_mid * logFK
        x_z = np.log((np.sqrt(1 - 2 * rho_param * z + z ** 2) + z - rho_param) / (1 - rho_param))
        if abs(x_z) < 1e-12:
            x_z = 1.0
        else:
            x_z = z / x_z

    term1 = alpha / (FK_mid * (1 + ((1 - beta) ** 2 / 24.0) * logFK ** 2 +
                               ((1 - beta) ** 4 / 1920.0) * logFK ** 4))
    term2 = 1 + ((((1 - beta) ** 2 / 24.0) * alpha ** 2 / (FK_mid ** 2)) +
                 (0.25 * rho_param * beta * nu * alpha / FK_mid) +
                 ((2 - 3 * rho_param ** 2) / 24.0) * nu ** 2) * T

    return term1 * x_z * term2


def sarima(endog, order=(1, 0, 0), seasonal_order=(1, 0, 0, 12)):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Time Series Modeling', 'Forecasting']
    function: "SARIMA (Seasonal AutoRegressive Integrated Moving Average) extends ARIMA to handle seasonal patterns in time series data. It includes both non-seasonal (p,d,q) and seasonal (P,D,Q,s) components, where s is the seasonal period. It is widely used for forecasting financial and economic time series with seasonal behavior."
    y_as_x: []
    :param endog: "The endogenous time series data (array or Series) to be modeled."
    :param order: "Tuple (p,d,q) specifying the non-seasonal ARIMA order."
    :param seasonal_order: "Tuple (P,D,Q,s) specifying the seasonal ARIMA order and seasonal period."
    :return: "Fitted SARIMAX model results object"
    '''
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    model = SARIMAX(endog, order=order, seasonal_order=seasonal_order,
                    enforce_stationarity=False, enforce_invertibility=False)
    results = model.fit(disp=False)
    return results


def security_market_line(risk_free_rate, beta, expected_market_return):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Capital Asset Pricing Model', 'Expected Returns']
    function: "Security Market Line (SML) represents the CAPM relationship graphically, plotting expected return against systematic risk (beta). Any security plotting above the SML is undervalued (positive alpha), and below it is overvalued (negative alpha). The equation is the same as CAPM."
    y_as_x: ['capm_expected_return', 'alpha']
    :param risk_free_rate: "The risk-free rate of return (R_f), typically the yield on government bonds."
    :param beta: "The systematic risk (beta) of the security, measuring its sensitivity to market movements."
    :param expected_market_return: "The expected return of the market portfolio E[R_m]."
    :return: "Computed E[R] = R_f + beta * (E[R_m] - R_f)"
    '''
    return risk_free_rate + beta * (expected_market_return - risk_free_rate)



def semivariance(returns, target=0.0):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Downside Risk', 'Risk Measurement']
    function: "Semivariance measures the dispersion of returns that fall below a target or threshold (typically the mean or zero). Unlike variance, which penalizes both upside and downside deviations equally, semivariance focuses only on downside risk, making it more relevant for risk-averse investors."
    y_as_x: ['sortino_ratio', 'downside_deviation']
    :param returns: "Array or Series of returns."
    :param target: "The target or minimum acceptable return (MAR). Default is 0."
    :return: "Computed SemiVariance = E[min(R - target, 0)^2]"
    '''
    returns = np.array(returns, dtype=float)
    downside = np.minimum(returns - target, 0)
    return np.mean(downside ** 2)


def severity(net_loss, defaulted_balance):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Loss Analysis', 'Credit Risk']
    function: "Severity (Loss Severity) measures the proportion of the defaulted loan balance that is actually lost after recovery efforts. It is synonymous with Loss Given Default (LGD) in the context of structured finance and securitization."
    y_as_x: ['pure_premium']
    :param net_loss: "The net loss amount after all recoveries have been applied to the defaulted loan."
    :param defaulted_balance: "The outstanding balance of the loan at the time of default."
    :return: "Computed Severity = Net Loss / Defaulted Balance"
    '''
    return net_loss / defaulted_balance


def sharpe_ratio(returns, risk_free_rate=0.0):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Risk-Adjusted Performance', 'Portfolio Evaluation']
    function: "Sharpe Ratio measures the excess return per unit of total risk (standard deviation). It is the most widely used risk-adjusted performance measure, allowing investors to compare the return premium relative to total volatility. A higher Sharpe ratio indicates better risk-adjusted returns."
    y_as_x: ['m_squared_modigliani', 'maximum_sharpe_portfolio', 'appraisal_ratio']
    :param returns: "Array or Series of periodic portfolio returns."
    :param risk_free_rate: "The risk-free rate per period (same frequency as returns). Default is 0."
    :return: "Computed Sharpe Ratio = (E[R_p] - R_f) / sigma_p"
    '''
    import empyrical
    returns = pd.Series(returns)
    return empyrical.sharpe_ratio(returns, risk_free=risk_free_rate)


def sharpe_lintner_beta_regression(portfolio_excess_returns, market_excess_returns):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Factor Models', 'Beta Estimation']
    function: "Sharpe-Lintner Beta Regression estimates the CAPM beta and alpha by regressing the portfolio's excess returns on the market's excess returns. The slope coefficient is the estimated beta, and the intercept is Jensen's alpha, measuring the portfolio's risk-adjusted abnormal return."
    y_as_x: ['alpha_from_regression']
    :param portfolio_excess_returns: "Array of portfolio excess returns (R_p - R_f) for each period."
    :param market_excess_returns: "Array of market excess returns (R_m - R_f) for each period."
    :return: "Fitted OLS regression results with alpha (intercept) and beta (slope)"
    '''
    import statsmodels.api as sm
    X = sm.add_constant(market_excess_returns)
    model = sm.OLS(portfolio_excess_returns, X)
    results = model.fit()
    return results


def short_rate_bond_pricing_pde(r_0, kappa, theta, sigma, T, n_steps=100, n_grid=100):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['PDE Methods', 'Bond Pricing']
    function: "Short-Rate Bond Pricing PDE solves the partial differential equation for bond pricing under a short-rate model: dP/dt + a(r,t)*dP/dr + 0.5*b(r,t)^2*d^2P/dr^2 - r*P = 0, with boundary condition P(T,r)=1. This is the fundamental PDE for pricing zero-coupon bonds under any affine short-rate model."
    y_as_x: []
    :param r_0: "The current (initial) short rate."
    :param kappa: "The mean-reversion speed parameter."
    :param theta: "The long-run mean of the short rate."
    :param sigma: "The volatility parameter of the short rate."
    :param T: "The maturity of the bond in years."
    :param n_steps: "Number of time steps for the finite difference grid."
    :param n_grid: "Number of spatial grid points for the rate dimension."
    :return: "Computed bond price P(0, T) from PDE solution"
    '''
    # Use Vasicek closed-form as PDE solution for dr = kappa(theta-r)dt + sigma dW
    B = (1 - np.exp(-kappa * T)) / kappa
    A = np.exp((theta - sigma ** 2 / (2 * kappa ** 2)) * (B - T) - (sigma ** 2 / (4 * kappa)) * B ** 2)
    return A * np.exp(-B * r_0)


def simple_compounding(pv, r, t):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Interest Rate Conventions', 'Time Value of Money']
    function: "Simple Compounding calculates the future value under simple interest, where interest is not compounded. The future value equals the present value multiplied by (1 + rate x time). This convention is commonly used for money market instruments with maturities less than one year."
    y_as_x: ['continuous_compounding']
    :param pv: "The present value or initial principal amount."
    :param r: "The simple interest rate (annualized)."
    :param t: "The time period in years (or fraction thereof)."
    :return: "Computed FV = PV * (1 + r * t)"
    '''
    return pv * (1 + r * t)


def simple_forward_rate(discount_factor_T, tau):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Forward Rates', 'Discount Factors']
    function: "Simple Forward Rate computes the simply-compounded forward rate from a discount factor and the year fraction. Given a discount factor DF(T), the simple forward rate F is derived from 1 + F*tau = 1/DF(T), solving for F."
    y_as_x: ['fra_rate']
    :param discount_factor_T: "The discount factor for the period DF(T)."
    :param tau: "The year fraction (day count fraction) for the period."
    :return: "Computed Simple Forward Rate F = (1/DF(T) - 1) / tau"
    '''
    return (1.0 / discount_factor_T - 1.0) / tau


def simple_return(price_current, price_previous):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Return Calculation', 'Performance Measurement']
    function: "Simple Return (arithmetic return) measures the percentage change in the price of an asset from one period to the next. It is the most intuitive return measure and is additive across assets in a portfolio but not across time."
    y_as_x: ['cumulative_return', 'log_return', 'portfolio_return', 'holding_period_return_hpr']
    :param price_current: "The price of the asset at the end of the current period (P_t)."
    :param price_previous: "The price of the asset at the end of the previous period (P_{t-1})."
    :return: "Computed Simple Return R_t = P_t / P_{t-1} - 1"
    '''
    return price_current / price_previous - 1.0


def single_monthly_mortality_smm(cpr):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Prepayment Analysis', 'Mortgage-Backed Securities']
    function: "Single Monthly Mortality (SMM) converts the annual Conditional Prepayment Rate (CPR) to a monthly prepayment rate. It represents the fraction of the mortgage pool that prepays in a single month. The relationship is SMM = 1 - (1 - CPR)^(1/12)."
    y_as_x: ['conditional_prepayment_rate_cpr', 'conditional_prepayment_rate_cpr_v2']
    :param cpr: "The annual Conditional Prepayment Rate (CPR), expressed as a decimal."
    :return: "Computed SMM = 1 - (1 - CPR)^(1/12)"
    '''
    return 1.0 - (1.0 - cpr) ** (1.0 / 12.0)


def slippage(actual_execution_price, expected_price):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Execution Cost', 'Trading Performance']
    function: "Slippage measures the difference between the actual execution price and the expected or target price at the time a trade order is placed. Positive slippage indicates a worse execution for the trader. It is a key component of total transaction costs."
    y_as_x: ['implementation_shortfall', 'arrival_price_slippage']
    :param actual_execution_price: "The actual price at which the trade was executed."
    :param expected_price: "The expected or target price at the time the trade decision was made (e.g., the mid-price or decision price)."
    :return: "Computed Slippage = Actual Execution Price - Expected Price"
    '''
    return actual_execution_price - expected_price


def smith_wilson_extrapolation(maturities, discount_factors, ufr, alpha):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Yield Curve Extrapolation', 'Solvency II']
    function: "Smith-Wilson Extrapolation is a method used to extrapolate the yield curve beyond the last liquid point toward the Ultimate Forward Rate (UFR). It is mandated under Solvency II for insurance companies. The method ensures a smooth transition from observed market rates to the long-term equilibrium rate."
    y_as_x: []
    :param maturities: "Array of observed maturities (in years) for the liquid instruments."
    :param discount_factors: "Array of observed discount factors corresponding to the maturities."
    :param ufr: "The Ultimate Forward Rate (UFR), the long-term equilibrium forward rate."
    :param alpha: "The convergence speed parameter controlling how quickly rates converge to the UFR."
    :return: "Smith-Wilson fitted discount factor function coefficients (zeta vector)"
    '''
    maturities = np.array(maturities, dtype=float)
    discount_factors = np.array(discount_factors, dtype=float)
    n = len(maturities)

    # Wilson function W(u, v)
    def wilson_func(u, v, ufr_val, alpha_val):
        return np.exp(-ufr_val * (u + v)) * (
                alpha_val * np.minimum(u, v) -
                0.5 * np.exp(-alpha_val * np.maximum(u, v)) * (
                        np.exp(alpha_val * np.minimum(u, v)) - np.exp(-alpha_val * np.minimum(u, v))
                )
        )

    # Build the W matrix
    W = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            W[i, j] = wilson_func(maturities[i], maturities[j], ufr, alpha)

    # mu = e^{-UFR * u}
    mu = np.exp(-ufr * maturities)

    # Solve for zeta: W * zeta = DF - mu
    zeta = np.linalg.solve(W, discount_factors - mu)
    return zeta


def solvency_ratio(available_capital, required_capital):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Insurance Regulation', 'Solvency Assessment']
    function: "Solvency Ratio measures the adequacy of an insurer's capital relative to its regulatory capital requirement. A ratio above 100% indicates the insurer has surplus capital above the minimum required. It is a key metric under Solvency II and other insurance regulatory frameworks."
    y_as_x: []
    :param available_capital: "The insurer's available capital (own funds) eligible to cover regulatory requirements."
    :param required_capital: "The required capital (e.g., Solvency Capital Requirement under Solvency II)."
    :return: "Computed Solvency Ratio = Available Capital / Required Capital"
    '''
    return available_capital / required_capital


def sortino_ratio(returns, required_return=0.0):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Risk-Adjusted Performance', 'Downside Risk']
    function: "Sortino Ratio measures excess return per unit of downside risk, using downside deviation instead of total standard deviation. Unlike the Sharpe ratio, it only penalizes returns below a minimum acceptable return (MAR), making it more appropriate for investors who are only concerned about downside risk."
    y_as_x: []
    :param returns: "Array or Series of periodic portfolio returns."
    :param required_return: "The minimum acceptable return (MAR) per period. Default is 0."
    :return: "Computed Sortino Ratio = (E[R_p] - MAR) / Downside Deviation"
    '''
    import empyrical
    returns = pd.Series(returns)
    return empyrical.sortino_ratio(returns, required_return=required_return)


def sources_and_uses_balance(total_sources, total_uses):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['LBO Modeling', 'Transaction Structuring']
    function: "Sources and Uses Balance verifies that total financing sources equal total transaction uses in an LBO or M&A transaction. Sources include equity, debt, and rollover equity; uses include purchase price, transaction fees, and debt refinancing. The balance must hold for the transaction to close."
    y_as_x: []
    :param total_sources: "Total financing sources (equity + debt + existing cash + rollover)."
    :param total_uses: "Total transaction uses (purchase price + fees + debt payoff + other costs)."
    :return: "Boolean indicating whether Total Sources = Total Uses (within tolerance)"
    '''
    return np.isclose(total_sources, total_uses)


def spark_spread(electricity_price, heat_rate, fuel_price):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Energy Markets', 'Power Generation']
    function: "Spark Spread measures the theoretical gross margin of a gas-fired power plant by comparing the price of electricity output to the cost of natural gas input (adjusted by the heat rate). A positive spark spread indicates it is profitable to run the plant."
    y_as_x: []
    :param electricity_price: "The market price of electricity (per MWh)."
    :param heat_rate: "The heat rate of the power plant, measuring fuel efficiency (MMBtu per MWh)."
    :param fuel_price: "The price of natural gas fuel (per MMBtu)."
    :return: "Computed Spark Spread = Electricity Price - Heat Rate x Fuel Price"
    '''
    return electricity_price - heat_rate * fuel_price


def speed(S, K, T, r, sigma, q=0.0):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Option Greeks', 'Higher-Order Sensitivities']
    function: "Speed (DgammaDspot) is the third derivative of the option price with respect to the underlying asset price, or equivalently the rate of change of gamma with respect to the spot price. It measures how gamma will change as the underlying moves and is important for managing gamma risk in options portfolios."
    y_as_x: []
    :param S: "The current price of the underlying asset."
    :param K: "The strike price of the option."
    :param T: "The time to expiration in years."
    :param r: "The risk-free interest rate (continuously compounded)."
    :param sigma: "The volatility of the underlying asset."
    :param q: "The continuous dividend yield. Default is 0."
    :return: "Computed Speed = d(Gamma)/dS"
    '''
    from scipy.stats import norm
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    gamma_val = np.exp(-q * T) * norm.pdf(d1) / (S * sigma * np.sqrt(T))
    speed_val = -gamma_val / S * (d1 / (sigma * np.sqrt(T)) + 1)
    return speed_val


def sponsor_cash_on_cash_return(cumulative_cash_to_sponsor, sponsor_equity_invested):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Fund Performance', 'Cash Returns']
    function: "Sponsor Cash-on-Cash Return measures the total cash distributions received by the private equity sponsor relative to the equity capital invested. It is a simple multiple-of-money metric that indicates the total cash return without considering the time value of money."
    y_as_x: []
    :param cumulative_cash_to_sponsor: "Total cumulative cash distributions received by the sponsor, including dividends, recaps, and exit proceeds."
    :param sponsor_equity_invested: "The total equity capital invested by the sponsor in the deal."
    :return: "Computed Cash-on-Cash = Cumulative Cash to Sponsor / Sponsor Equity Invested"
    '''
    return cumulative_cash_to_sponsor / sponsor_equity_invested


def spot_rate_bootstrapping(bond_prices, coupon_rates, face_value=100, frequency=2):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Yield Curve Construction', 'Bootstrapping']
    function: "Spot Rate Bootstrapping derives the zero-coupon (spot) yield curve from observed coupon bond prices. Starting from the shortest maturity, each successive spot rate is determined by using previously derived discount factors to solve for the unknown discount factor at the new maturity."
    y_as_x: ['nelson_siegel_yield_curve', 'nelson_siegel_svensson_curve']
    :param bond_prices: "Array of observed clean prices for bonds of increasing maturity."
    :param coupon_rates: "Array of annual coupon rates for each bond (as decimals)."
    :param face_value: "The face value of the bonds. Default is 100."
    :param frequency: "The coupon payment frequency per year. Default is 2 (semi-annual)."
    :return: "Array of bootstrapped spot rates for each maturity"
    '''
    n = len(bond_prices)
    spot_rates = np.zeros(n)
    discount_factors = np.zeros(n)

    for i in range(n):
        coupon = coupon_rates[i] * face_value / frequency
        t = (i + 1) / frequency
        # Sum of PV of known coupons
        pv_known = 0
        for j in range(i):
            pv_known += coupon * discount_factors[j]
        # Solve for DF_i: P = pv_known + (coupon + face_value) * DF_i
        discount_factors[i] = (bond_prices[i] - pv_known) / (coupon + face_value)
        spot_rates[i] = (1.0 / discount_factors[i]) ** (1.0 / t) - 1.0

    return spot_rates


def spot_rate_from_discount_factor(discount_factor, t):
    '''
    domain: ['Fixed income & bond math']
    subdomain: ['Yield Curve Mathematics', 'Discount Factors']
    function: "Spot Rate from Discount Factor derives the continuously compounded zero-coupon (spot) rate from a discount factor and its corresponding maturity. The spot rate z(t) = -ln(DF(t))/t represents the annualized continuously compounded return for a zero-coupon investment maturing at time t."
    y_as_x: ['forward_rate', 'forward_rate_from_spot_rates']
    :param discount_factor: "The discount factor DF(t) for maturity t."
    :param t: "The time to maturity in years."
    :return: "Computed Spot Rate z(t) = -ln(DF(t)) / t"
    '''
    return -np.log(discount_factor) / t


def spread_duration(bond_price, bond_price_up, bond_price_down, spread_shift):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Credit Risk Sensitivity', 'Spread Analysis']
    function: "Spread Duration measures the sensitivity of a bond's price to a change in its credit spread. It quantifies the approximate percentage price change for a one basis point change in the spread. It is particularly important for corporate bonds and credit products."
    y_as_x: ['duration_times_spread_dts']
    :param bond_price: "The current price of the bond P."
    :param bond_price_up: "The bond price when the spread is increased by the spread_shift."
    :param bond_price_down: "The bond price when the spread is decreased by the spread_shift."
    :param spread_shift: "The parallel shift in spread used for the calculation (e.g., 0.0001 for 1bp)."
    :return: "Computed Spread Duration = -(P_up - P_down) / (2 * P * spread_shift)"
    '''
    return -(bond_price_up - bond_price_down) / (2.0 * bond_price * spread_shift)


def spread_option_kirk_approximation(F1, F2, K, T, r, sigma1, sigma2, rho_param):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Exotic Options', 'Spread Options']
    function: "Spread Option (Kirk Approximation) values a European call option on the spread between two assets using Kirk's closed-form approximation. It approximates the spread option price using a modified Black-Scholes formula, treating the option as a single-asset option with an adjusted volatility."
    y_as_x: []
    :param F1: "The forward price of the first (long) asset."
    :param F2: "The forward price of the second (short) asset."
    :param K: "The strike price of the spread option."
    :param T: "The time to expiration in years."
    :param r: "The risk-free interest rate (continuously compounded)."
    :param sigma1: "The volatility of the first asset."
    :param sigma2: "The volatility of the second asset."
    :param rho_param: "The correlation between the two asset returns."
    :return: "Computed spread call option price using Kirk's approximation"
    '''
    from scipy.stats import norm
    DF = np.exp(-r * T)
    F2_adj = F2 + K
    sigma_adj = np.sqrt(sigma1 ** 2 - 2 * rho_param * sigma1 * sigma2 * (F2 / F2_adj) +
                        (sigma2 * F2 / F2_adj) ** 2)
    d1 = (np.log(F1 / F2_adj) + 0.5 * sigma_adj ** 2 * T) / (sigma_adj * np.sqrt(T))
    d2 = d1 - sigma_adj * np.sqrt(T)
    return DF * (F1 * norm.cdf(d1) - F2_adj * norm.cdf(d2))


def square_root_impact_law(Y, sigma, Q, V):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Market Impact', 'Execution Cost Modeling']
    function: "Square-Root Impact Law is an empirical market impact model that states the price impact of a trade is proportional to the volatility times the square root of the ratio of order size to average daily volume. The constant Y is typically calibrated to be around 1. This concave relationship is widely observed across different markets."
    y_as_x: []
    :param Y: "The impact coefficient (typically calibrated, often around 1)."
    :param sigma: "The daily volatility of the asset."
    :param Q: "The order size (number of shares or notional)."
    :param V: "The average daily volume."
    :return: "Computed Impact = Y * sigma * sqrt(Q/V)"
    '''
    return Y * sigma * np.sqrt(Q / V)


def stable_funding_gap(required_stable_funding, available_stable_funding):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Liquidity Management', 'NSFR']
    function: "Stable Funding Gap measures the difference between required stable funding and available stable funding. A positive gap indicates a funding shortfall that the institution needs to address. It is closely related to the Net Stable Funding Ratio (NSFR) requirement."
    y_as_x: []
    :param required_stable_funding: "The amount of stable funding required based on the liquidity characteristics and maturity of assets."
    :param available_stable_funding: "The amount of stable funding available from equity, long-term debt, and stable deposits."
    :return: "Computed Stable Funding Gap = Required Stable Funding - Available Stable Funding"
    '''
    return required_stable_funding - available_stable_funding


def state_space_measurement_equation(Z, alpha, epsilon_cov=None, n_obs=None):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['State-Space Models', 'Kalman Filter']
    function: "State-Space Measurement Equation defines the relationship between the observed data y_t and the unobserved state vector alpha_t: y_t = Z_t * alpha_t + epsilon_t. The measurement matrix Z maps the latent state to the observable variables, and epsilon_t is the observation noise."
    y_as_x: []
    :param Z: "The measurement (observation) matrix mapping states to observations (n_obs x n_states)."
    :param alpha: "The state vector alpha_t (n_states x 1)."
    :param epsilon_cov: "The covariance matrix of the observation noise epsilon_t. If None, returns the deterministic part."
    :param n_obs: "Number of observations to simulate. If None, returns a single observation."
    :return: "Computed observation y_t = Z * alpha_t + epsilon_t"
    '''
    Z = np.array(Z, dtype=float)
    alpha = np.array(alpha, dtype=float)
    y = Z @ alpha
    if epsilon_cov is not None:
        epsilon = np.random.multivariate_normal(np.zeros(Z.shape[0]), np.array(epsilon_cov))
        y = y + epsilon
    return y


def state_space_transition_equation(T_mat, alpha, R=None, eta_cov=None):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['State-Space Models', 'Kalman Filter']
    function: "State-Space Transition Equation defines how the latent state vector evolves over time: alpha_{t+1} = T_t * alpha_t + R_t * eta_t. The transition matrix T governs the state dynamics, and R*eta represents the state noise."
    y_as_x: []
    :param T_mat: "The transition matrix T_t (n_states x n_states) governing state dynamics."
    :param alpha: "The current state vector alpha_t (n_states x 1)."
    :param R: "The selection matrix R_t for the state noise (n_states x n_shocks). If None, assumed identity."
    :param eta_cov: "The covariance matrix of the state noise eta_t. If None, returns the deterministic part."
    :return: "Computed next state alpha_{t+1} = T * alpha_t + R * eta_t"
    '''
    T_mat = np.array(T_mat, dtype=float)
    alpha = np.array(alpha, dtype=float)
    alpha_next = T_mat @ alpha
    if R is not None and eta_cov is not None:
        R = np.array(R, dtype=float)
        n_shocks = R.shape[1]
        eta = np.random.multivariate_normal(np.zeros(n_shocks), np.array(eta_cov))
        alpha_next = alpha_next + R @ eta
    return alpha_next


def sterling_ratio(returns):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Risk-Adjusted Performance', 'Drawdown-Based Metrics']
    function: "Sterling Ratio measures risk-adjusted return by dividing the compound annual growth rate (CAGR) by the average drawdown. It is similar to the Calmar ratio but uses average drawdown rather than maximum drawdown, providing a more stable measure of downside risk."
    y_as_x: []
    :param returns: "Array or Series of periodic portfolio returns."
    :return: "Computed Sterling Ratio = CAGR / Average Drawdown"
    '''
    import quantstats as qs
    returns = pd.Series(returns)
    return qs.stats.sterling(returns)


def stochastic_oscillator(high, low, close, fastk_period=14, slowk_period=3, slowd_period=3):
    '''
    domain: ['Technical analysis']
    subdomain: ['Momentum Indicators', 'Overbought/Oversold']
    function: "Stochastic Oscillator is a momentum indicator comparing a security's closing price to its price range over a given period. %K measures the current close relative to the high-low range, and %D is a moving average of %K. Values above 80 suggest overbought conditions; below 20 suggest oversold."
    y_as_x: []
    :param high: "Array of high prices."
    :param low: "Array of low prices."
    :param close: "Array of closing prices."
    :param fastk_period: "The lookback period for %K. Default is 14."
    :param slowk_period: "The smoothing period for slow %K. Default is 3."
    :param slowd_period: "The smoothing period for %D. Default is 3."
    :return: "Tuple of (slowk, slowd) arrays representing the Stochastic Oscillator %K and %D values"
    '''
    import talib
    high = np.array(high, dtype=np.float64)
    low = np.array(low, dtype=np.float64)
    close = np.array(close, dtype=np.float64)
    slowk, slowd = talib.STOCH(high, low, close,
                               fastk_period=fastk_period,
                               slowk_period=slowk_period,
                               slowk_matype=0,
                               slowd_period=slowd_period,
                               slowd_matype=0)
    return slowk, slowd


def stochastic_oscillator_pctd(high, low, close, fastk_period=14, slowk_period=3, slowd_period=3):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Momentum Indicators', 'Stochastic Analysis']
    function: "Stochastic Oscillator %D is the signal line of the stochastic oscillator, computed as a 3-period simple moving average of %K. It provides a smoothed version of the raw stochastic reading and is used for generating buy/sell signals when it crosses %K."
    y_as_x: []
    :param high: "Array of high prices."
    :param low: "Array of low prices."
    :param close: "Array of closing prices."
    :param fastk_period: "The lookback period for %K. Default is 14."
    :param slowk_period: "The smoothing period for slow %K. Default is 3."
    :param slowd_period: "The smoothing period for %D. Default is 3."
    :return: "Computed %D = SMA_3(%K)"
    '''
    import talib
    high = np.array(high, dtype=np.float64)
    low = np.array(low, dtype=np.float64)
    close = np.array(close, dtype=np.float64)
    _, slowd = talib.STOCH(high, low, close,
                           fastk_period=fastk_period,
                           slowk_period=slowk_period,
                           slowk_matype=0,
                           slowd_period=slowd_period,
                           slowd_matype=0)
    return slowd


def stochastic_oscillator_pctk(high, low, close, fastk_period=14, slowk_period=3):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Momentum Indicators', 'Stochastic Analysis']
    function: "Stochastic Oscillator %K measures where the closing price sits within the recent high-low range. Raw %K = 100 * (Close - Low_n) / (High_n - Low_n). The slow %K is a smoothed version. Values near 100 indicate the price is near the top of its range."
    y_as_x: ['stochastic_oscillator_pctd']
    :param high: "Array of high prices."
    :param low: "Array of low prices."
    :param close: "Array of closing prices."
    :param fastk_period: "The lookback period for the raw %K. Default is 14."
    :param slowk_period: "The smoothing period for slow %K. Default is 3."
    :return: "Computed %K = 100 * (C - L_n) / (H_n - L_n)"
    '''
    import talib
    high = np.array(high, dtype=np.float64)
    low = np.array(low, dtype=np.float64)
    close = np.array(close, dtype=np.float64)
    slowk, _ = talib.STOCH(high, low, close,
                           fastk_period=fastk_period,
                           slowk_period=slowk_period,
                           slowk_matype=0,
                           slowd_period=3,
                           slowd_matype=0)
    return slowk


def stochastic_rsi(close, timeperiod=14, fastk_period=5, fastd_period=3):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Momentum Indicators', 'Overbought/Oversold']
    function: "Stochastic RSI applies the Stochastic Oscillator formula to RSI values instead of price data. It ranges from 0 to 1 and provides a more sensitive indicator of overbought/oversold conditions than standard RSI. StochRSI = (RSI - min RSI_n) / (max RSI_n - min RSI_n)."
    y_as_x: []
    :param close: "Array or Series of closing prices."
    :param timeperiod: "The lookback period for the RSI calculation. Default is 14."
    :param fastk_period: "The lookback period for the stochastic %K of RSI. Default is 5."
    :param fastd_period: "The smoothing period for the stochastic %D of RSI. Default is 3."
    :return: "Computed StochRSI = (RSI - min RSI_n) / (max RSI_n - min RSI_n)"
    '''
    import talib
    close = np.array(close, dtype=np.float64)
    rsi_values = talib.RSI(close, timeperiod=timeperiod)
    # Compute stochastic of RSI manually
    result = np.full_like(rsi_values, np.nan)
    for i in range(fastk_period - 1 + timeperiod, len(rsi_values)):
        window = rsi_values[i - fastk_period + 1:i + 1]
        if np.all(~np.isnan(window)):
            min_rsi = np.nanmin(window)
            max_rsi = np.nanmax(window)
            if max_rsi - min_rsi > 0:
                result[i] = (rsi_values[i] - min_rsi) / (max_rsi - min_rsi)
            else:
                result[i] = 0.5
    return result


# ================================================================================
# BATCH 8
# ================================================================================

def stop_loss_premium(loss_distribution, deductible):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Reinsurance', 'Loss Distributions']
    function: "Stop-loss premium is the expected value of the excess of aggregate losses over a deductible (retention). It represents the expected cost to a reinsurer who pays all aggregate losses above the deductible d, computed as Pi(d) = E[(S - d)^+], where S is the aggregate loss."
    y_as_x: []
    :param loss_distribution: "A scipy.stats frozen distribution representing the aggregate loss S"
    :param deductible: "The retention level d above which losses are covered"
    :return: "Computed stop-loss premium Pi(d) = E[(S - d)^+]"
    '''
    from scipy import integrate
    sf = loss_distribution.sf  # survival function = 1 - CDF
    result, _ = integrate.quad(sf, deductible, np.inf)
    return result


def straddle_payoff(S, K, call_premium, put_premium):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Option Strategies', 'Payoff Diagrams']
    function: "Straddle payoff is the combined payoff of buying a call and a put option with the same strike price and expiration. The gross payoff is max(S-K,0) + max(K-S,0) minus the total premiums paid. A long straddle profits from large moves in either direction."
    y_as_x: []
    :param S: "Underlying asset price at expiration"
    :param K: "Strike price of the call and put options"
    :param call_premium: "Premium paid for the call option"
    :param put_premium: "Premium paid for the put option"
    :return: "Computed straddle payoff = max(S-K,0) + max(K-S,0) - call_premium - put_premium"
    '''
    return np.maximum(S - K, 0) + np.maximum(K - S, 0) - call_premium - put_premium


def strangle_payoff(S, K_call, K_put, call_premium, put_premium):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Option Strategies', 'Payoff Diagrams']
    function: "Strangle payoff is the combined payoff of buying an out-of-the-money call and an out-of-the-money put with different strike prices but the same expiration. The net payoff is max(S-K_c,0) + max(K_p-S,0) minus the total premiums paid."
    y_as_x: []
    :param S: "Underlying asset price at expiration"
    :param K_call: "Strike price of the call option (typically above current price)"
    :param K_put: "Strike price of the put option (typically below current price)"
    :param call_premium: "Premium paid for the call option"
    :param put_premium: "Premium paid for the put option"
    :return: "Computed strangle payoff = max(S-K_call,0) + max(K_put-S,0) - call_premium - put_premium"
    '''
    return np.maximum(S - K_call, 0) + np.maximum(K_put - S, 0) - call_premium - put_premium


def stress_capital_buffer(stress_losses, regulatory_floor, risk_weighted_assets_rwa):
    '''
    domain: ['Bank regulation, Basel & prudential ratios']
    subdomain: ['Capital Adequacy', 'Stress Testing']
    function: "Stress capital buffer (SCB) is a regulatory capital requirement that equals the greater of projected stress losses and a regulatory floor, divided by risk-weighted assets. It ensures banks hold sufficient capital to absorb losses during stressed economic scenarios."
    y_as_x: []
    :param stress_losses: "Projected losses under a supervisory stress scenario"
    :param regulatory_floor: "Minimum floor set by regulators (e.g., 2.5% for US banks)"
    :param risk_weighted_assets_rwa: "Risk-weighted assets computed as the sum of each exposure times its risk weight, representing the denominator in capital adequacy ratios"
    :return: "Computed SCB = max(stress_losses, regulatory_floor) / RWA"
    '''
    return np.maximum(stress_losses, regulatory_floor) / risk_weighted_assets_rwa


def stress_loss(current_value, stressed_value):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Stress Testing', 'Scenario Analysis']
    function: "Stress loss is the difference between the current portfolio value and the value under a stressed market scenario. It measures the potential impact of adverse market moves on the portfolio."
    y_as_x: ['stress_capital_buffer']
    :param current_value: "Portfolio value under current market conditions"
    :param stressed_value: "Portfolio value under stressed market conditions"
    :return: "Computed stress loss = V(current) - V(stressed)"
    '''
    return current_value - stressed_value


def stressed_var(returns, confidence_level=0.99, stress_window=None):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Value at Risk', 'Stress Testing']
    function: "Stressed VaR (SVaR) is the Value at Risk computed using parameters from a period of significant financial stress. It is a regulatory requirement under Basel II.5/III to capture tail risk that may not appear in recent history. The stress window is chosen as the 12-month period that produces the highest VaR."
    y_as_x: []
    :param returns: "Array-like of portfolio returns; should represent the stress window period"
    :param confidence_level: "Confidence level for VaR computation (default 0.99)"
    :param stress_window: "Optional tuple (start, end) indices to select the stress period from returns; if None, uses all returns"
    :return: "Computed Stressed VaR at the given confidence level using the stress-window parameters"
    '''
    if stress_window is not None:
        returns = returns[stress_window[0]:stress_window[1]]
    returns = np.asarray(returns)
    var_value = -np.percentile(returns, (1 - confidence_level) * 100)
    return var_value


def structural_credit_spread_approximation(debt, equity, asset_value, risk_free_rate, T):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Structural Models', 'Credit Spreads']
    function: "Structural credit spread approximation estimates the credit spread implied by a Merton-style structural model. The spread is derived from the relation between the firm's asset value, debt, equity, and the risk-free rate: s = -ln[(D*e^{-rT} + E) / V_A] / T."
    y_as_x: []
    :param debt: "Face value of the firm's debt (D)"
    :param equity: "Market value of the firm's equity (E)"
    :param asset_value: "Total asset value of the firm (V_A)"
    :param risk_free_rate: "Risk-free interest rate (r)"
    :param T: "Time to maturity of the debt in years"
    :return: "Computed structural credit spread approximation s = -ln[(D*e^{-rT} + E) / V_A] / T"
    '''
    return -np.log((debt * np.exp(-risk_free_rate * T) + equity) / asset_value) / T


def survival_function(x, t, life_table=None, mortality_law='gompertz', **params):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Life Tables', 'Survival Analysis']
    function: "The survival function S_x(t) gives the probability that a life aged x survives at least t more years. It is defined as S_x(t) = P[T_x > t] = 1 - F_x(t), where T_x is the future lifetime random variable and F_x(t) is the CDF. This is fundamental to all life contingent calculations."
    y_as_x: ['force_of_mortality', 'death_probability', 'one_year_survival_probability', 'curtate_expected_future_lifetime', 'expected_future_lifetime']
    :param x: "Current age of the individual"
    :param t: "Time period for survival probability"
    :param life_table: "Optional life table as a dict with ages as keys and l_x values"
    :param mortality_law: "Mortality law to use if no life table provided (default 'gompertz')"
    :param params: "Additional parameters for the mortality law (e.g., B, c for Gompertz)"
    :return: "Computed survival probability S_x(t) = P[T_x > t]"
    '''
    if life_table is not None:
        l_x = life_table.get(x, 0)
        l_x_t = life_table.get(x + t, 0)
        if l_x == 0:
            return 0.0
        return l_x_t / l_x
    # Gompertz mortality law: mu(x) = B * c^x
    B = params.get('B', 0.0003)
    c = params.get('c', 1.07)
    if c == 1:
        integral = B * t
    else:
        integral = B * (c ** x) * (c ** t - 1) / np.log(c)
    return np.exp(-integral)


def survival_probability(hazard_rate, T, flat=True, hazard_rates=None, time_points=None):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Default Modeling', 'Hazard Rates']
    function: "Survival probability Q(0,T) is the probability that an entity does not default before time T. Under a flat hazard rate lambda, Q(0,T) = exp(-lambda*T). For a term structure of hazard rates, the integral is computed piecewise."
    y_as_x: ['probability_of_default_from_hazard_rate', 'cds_premium_leg', 'cds_protection_leg', 'expected_credit_loss_ifrs_9_over_cecl', 'lifetime_ecl']
    :param hazard_rate: "Constant hazard rate lambda (used if flat=True)"
    :param T: "Time horizon in years"
    :param flat: "Whether hazard rate is flat (default True)"
    :param hazard_rates: "Array of piecewise hazard rates (used if flat=False)"
    :param time_points: "Array of time points corresponding to hazard_rates (used if flat=False)"
    :return: "Computed survival probability Q(0,T) = exp(-integral_0^T lambda(t) dt)"
    '''
    if flat:
        return np.exp(-hazard_rate * T)
    else:
        hazard_rates = np.asarray(hazard_rates)
        time_points = np.asarray(time_points)
        dt = np.diff(time_points, prepend=0)
        mask = time_points <= T
        integral = np.sum(hazard_rates[mask] * dt[mask])
        return np.exp(-integral)


def sustainable_growth_rate(return_on_equity_roe, retention_ratio):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Financial Statement Analysis', 'Growth Analysis']
    function: "Sustainable growth rate is the maximum rate at which a firm can grow its sales, earnings, and dividends without raising external equity, while maintaining a constant debt-to-equity ratio. It is computed as ROE times the retention ratio (also called the plowback ratio)."
    y_as_x: []
    :param return_on_equity_roe: "Return on equity (ROE) = Net Income / Average Equity, measuring how effectively equity capital generates profit"
    :param retention_ratio: "Retention ratio = 1 - Dividend Payout Ratio, the fraction of earnings retained in the business"
    :return: "Computed sustainable growth rate g = ROE x Retention Ratio"
    '''
    return return_on_equity_roe * retention_ratio


def swap_annuity(discount_factors, year_fractions):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Swap Pricing', 'Annuity Factors']
    function: "Swap annuity (also called the PV01 or DV01 of the fixed leg) is the present value of receiving 1 unit of currency on each payment date of the fixed leg. It is computed as A = sum_i alpha_i * DF_i, where alpha_i is the year fraction for period i and DF_i is the discount factor at time t_i."
    y_as_x: ['swap_fixed_rate', 'par_swap_rate', 'black_swaption_price']
    :param discount_factors: "Array of discount factors DF(t_i) at each payment date"
    :param year_fractions: "Array of year fractions (accrual periods) alpha_i for each payment period"
    :return: "Computed swap annuity A = sum_i alpha_i * DF_i"
    '''
    discount_factors = np.asarray(discount_factors)
    year_fractions = np.asarray(year_fractions)
    return np.sum(year_fractions * discount_factors)


def swap_fixed_leg_pv(notional, fixed_rate, year_fractions, discount_factors):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Swap Pricing', 'Fixed Income Derivatives']
    function: "The present value of the fixed leg of an interest rate swap. It is computed as PV_fixed = sum_i N * K * alpha_i * DF(t_i), where N is the notional, K is the fixed rate, alpha_i is the year fraction, and DF(t_i) is the discount factor at each payment date."
    y_as_x: ['swap_present_value']
    :param notional: "Notional principal amount of the swap (N)"
    :param fixed_rate: "Fixed coupon rate of the swap (K)"
    :param year_fractions: "Array of year fractions (accrual periods) alpha_i"
    :param discount_factors: "Array of discount factors DF(t_i) at each payment date"
    :return: "Computed PV of fixed leg = sum_i N * K * alpha_i * DF(t_i)"
    '''
    year_fractions = np.asarray(year_fractions)
    discount_factors = np.asarray(discount_factors)
    return notional * fixed_rate * np.sum(year_fractions * discount_factors)


def swap_fixed_rate(discount_factors, year_fractions):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Swap Pricing', 'Par Rates']
    function: "The swap fixed rate (par swap rate) is the coupon rate that makes the present value of the fixed leg equal to the present value of the floating leg. It is computed as K = (1 - DF_n) / sum_i alpha_i * DF_i, where DF_n is the final discount factor."
    y_as_x: ['swap_fixed_leg_pv']
    :param discount_factors: "Array of discount factors DF(t_i) at each payment date"
    :param year_fractions: "Array of year fractions (accrual periods) alpha_i for each payment period"
    :return: "Computed par swap fixed rate K = (1 - DF_n) / sum_i alpha_i * DF_i"
    '''
    discount_factors = np.asarray(discount_factors)
    year_fractions = np.asarray(year_fractions)
    annuity = np.sum(year_fractions * discount_factors)
    return (1 - discount_factors[-1]) / annuity


def swap_floating_leg_pv(notional, forward_rates, year_fractions, discount_factors):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Swap Pricing', 'Fixed Income Derivatives']
    function: "The present value of the floating leg of an interest rate swap. It is computed as PV_float = sum_i N * L_i * alpha_i * DF(t_i), where N is the notional, L_i is the forward rate for period i, alpha_i is the year fraction, and DF(t_i) is the discount factor."
    y_as_x: ['swap_present_value']
    :param notional: "Notional principal amount of the swap (N)"
    :param forward_rates: "Array of forward rates L_i for each floating period"
    :param year_fractions: "Array of year fractions (accrual periods) alpha_i"
    :param discount_factors: "Array of discount factors DF(t_i) at each payment date"
    :return: "Computed PV of floating leg = sum_i N * L_i * alpha_i * DF(t_i)"
    '''
    forward_rates = np.asarray(forward_rates)
    year_fractions = np.asarray(year_fractions)
    discount_factors = np.asarray(discount_factors)
    return notional * np.sum(forward_rates * year_fractions * discount_factors)


def swap_present_value(swap_fixed_leg_pv, swap_floating_leg_pv, is_payer=True):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Swap Pricing', 'Fixed Income Derivatives']
    function: "The present value of an interest rate swap is the difference between the present values of the fixed and floating legs. For a payer swap (pay fixed, receive floating): PV = PV_float - PV_fixed. For a receiver swap: PV = PV_fixed - PV_float."
    y_as_x: []
    :param swap_fixed_leg_pv: "Present value of the fixed leg of the swap, computed as sum_i N * K * alpha_i * DF(t_i)"
    :param swap_floating_leg_pv: "Present value of the floating leg of the swap, computed as sum_i N * L_i * alpha_i * DF(t_i)"
    :param is_payer: "True for payer swap (pay fixed), False for receiver swap (default True)"
    :return: "Computed swap PV = PV_float - PV_fixed (payer) or PV_fixed - PV_float (receiver)"
    '''
    if is_payer:
        return swap_floating_leg_pv - swap_fixed_leg_pv
    else:
        return swap_fixed_leg_pv - swap_floating_leg_pv


def tail_hedge_payoff(S_T, K, premium, position='long_put'):
    '''
    domain: ['Commodities, futures & hedging']
    subdomain: ['Hedging Strategies', 'Tail Risk Protection']
    function: "Tail hedge payoff is the net payoff from a protective position designed to offset extreme portfolio losses. Typically implemented via deep out-of-the-money puts: Payoff = max(K - S_T, 0) - Premium. Can also be via futures P&L in stress scenarios."
    y_as_x: []
    :param S_T: "Underlying asset price at expiration or stress scenario price"
    :param K: "Strike price of the protective put option"
    :param premium: "Premium paid for the tail hedge position"
    :param position: "Type of tail hedge ('long_put' by default)"
    :return: "Computed tail hedge payoff = max(K - S_T, 0) - Premium"
    '''
    if position == 'long_put':
        return np.maximum(K - S_T, 0) - premium
    else:
        return np.maximum(K - S_T, 0) - premium


def tail_ratio(returns):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Tail Risk', 'Distribution Analysis']
    function: "Tail ratio measures the asymmetry of the return distribution's tails. It is computed as the absolute value of the 95th percentile divided by the absolute value of the 5th percentile. A ratio greater than 1 indicates a fatter right tail (more upside potential), while less than 1 indicates a fatter left tail (more downside risk)."
    y_as_x: []
    :param returns: "Array-like or pd.Series of portfolio returns"
    :return: "Computed tail ratio = |95th percentile| / |5th percentile|"
    '''
    import quantstats as qs
    returns = pd.Series(returns)
    return qs.stats.tail_ratio(returns)


def tangency_portfolio_weights(expected_returns, cov_matrix, risk_free_rate=0.0):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Portfolio Optimization', 'Mean-Variance Analysis']
    function: "Tangency portfolio weights maximize the Sharpe ratio. The optimal weights are proportional to Sigma^{-1}(mu - r_f * 1), where Sigma is the covariance matrix, mu is the expected return vector, and r_f is the risk-free rate. The tangency portfolio lies at the point where the capital market line is tangent to the efficient frontier."
    y_as_x: []
    :param expected_returns: "Array or pd.Series of expected returns for each asset (mu)"
    :param cov_matrix: "Covariance matrix of asset returns (Sigma)"
    :param risk_free_rate: "Risk-free rate of return (r_f, default 0.0)"
    :return: "Computed tangency portfolio weights (normalized to sum to 1)"
    '''
    from pypfopt import EfficientFrontier
    ef = EfficientFrontier(expected_returns, cov_matrix)
    ef.max_sharpe(risk_free_rate=risk_free_rate)
    weights = ef.clean_weights()
    return dict(weights)


def tax_shield(interest_expense, tax_rate):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Capital Structure', 'Tax Planning']
    function: "Tax shield is the reduction in income taxes resulting from the tax-deductibility of interest expense on debt. It represents a benefit of debt financing, computed as Interest Expense multiplied by the Tax Rate."
    y_as_x: ['pv_of_tax_shield', 'adjusted_present_value_apv']
    :param interest_expense: "Total interest expense on debt for the period"
    :param tax_rate: "Marginal corporate tax rate (T)"
    :return: "Computed tax shield = Interest Expense x Tax Rate"
    '''
    return interest_expense * tax_rate


def temporary_annuity(x, n, interest_rate, life_table=None, **params):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Life Annuities', 'Actuarial Present Values']
    function: "Temporary annuity-due a_{x:n} is the expected present value of an annuity that pays 1 per year at the beginning of each year while the annuitant aged x survives, for a maximum of n years. Computed as a_{x:n} = sum_{k=0}^{n-1} v^k * _kp_x."
    y_as_x: ['net_premium', 'net_premium_equivalence_principle', 'gross_premium_principle']
    :param x: "Current age of the annuitant"
    :param n: "Maximum number of years (term of the annuity)"
    :param interest_rate: "Annual interest rate used for discounting"
    :param life_table: "Optional life table dict with ages as keys and l_x values"
    :param params: "Additional mortality parameters if no life table provided"
    :return: "Computed temporary annuity-due a_{x:n}"
    '''
    v = 1 / (1 + interest_rate)
    annuity_value = 0.0
    for k in range(n):
        if life_table is not None:
            l_x = life_table.get(x, 0)
            l_x_k = life_table.get(x + k, 0)
            if l_x == 0:
                p_k = 0.0
            else:
                p_k = l_x_k / l_x
        else:
            p_k = survival_function(x, k, **params)
        annuity_value += (v ** k) * p_k
    return annuity_value


def term_insurance_apv(x, n, interest_rate, life_table=None, **params):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Life Insurance', 'Actuarial Present Values']
    function: "Term insurance APV (Actuarial Present Value) A_{x:n}^1 is the expected present value of a benefit of 1 payable at the end of the year of death, provided death occurs within n years. Computed as A_{x:n}^1 = sum_{k=0}^{n-1} v^{k+1} * _kp_x * q_{x+k}."
    y_as_x: ['net_premium', 'endowment_insurance_apv']
    :param x: "Current age of the insured"
    :param n: "Term of the insurance in years"
    :param interest_rate: "Annual interest rate used for discounting"
    :param life_table: "Optional life table dict with ages as keys and l_x values"
    :param params: "Additional mortality parameters if no life table provided"
    :return: "Computed term insurance APV A_{x:n}^1"
    '''
    v = 1 / (1 + interest_rate)
    apv = 0.0
    for k in range(n):
        if life_table is not None:
            l_x = life_table.get(x, 0)
            l_x_k = life_table.get(x + k, 0)
            l_x_k1 = life_table.get(x + k + 1, 0)
            if l_x == 0:
                continue
            p_k = l_x_k / l_x
            q_xk = 1 - (l_x_k1 / l_x_k) if l_x_k > 0 else 1.0
        else:
            p_k = survival_function(x, k, **params)
            p_k1 = survival_function(x, k + 1, **params)
            q_xk = 1 - (p_k1 / p_k) if p_k > 0 else 1.0
        apv += (v ** (k + 1)) * p_k * q_xk
    return apv


def terminal_capitalization_value(noi_terminal, exit_cap_rate):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Property Valuation', 'DCF Analysis']
    function: "Terminal capitalization value (also called reversion value) estimates the property value at the end of a DCF holding period. It is computed by dividing the projected net operating income for the year after the holding period by the assumed exit capitalization rate."
    y_as_x: ['real_estate_dcf']
    :param noi_terminal: "Projected net operating income for the first year after the holding period (NOI_{T+1})"
    :param exit_cap_rate: "Exit capitalization rate assumed at disposition"
    :return: "Computed terminal value = NOI_{T+1} / Exit Cap Rate"
    '''
    return noi_terminal / exit_cap_rate


def terminal_value_exit_multiple(terminal_metric, exit_multiple):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Valuation', 'DCF Analysis']
    function: "Terminal value using the exit multiple method estimates the value of a business at the end of the explicit forecast period by applying a market-based multiple (e.g., EV/EBITDA) to the relevant financial metric in the final year."
    y_as_x: ['fcff_dcf_intrinsic_value', 'fcfe_dcf_intrinsic_value']
    :param terminal_metric: "The financial metric in the final projection year (e.g., EBITDA_n, Revenue_n)"
    :param exit_multiple: "The market-based valuation multiple applied at exit (e.g., EV/EBITDA multiple)"
    :return: "Computed terminal value TV = Metric_n x Exit Multiple"
    '''
    return terminal_metric * exit_multiple


def terminal_value_gordon_growth(fcf_next, weighted_average_cost_of_capital_wacc, growth_rate):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Valuation', 'DCF Analysis']
    function: "Terminal value using the Gordon growth model (perpetuity growth method) estimates the value of all future free cash flows beyond the explicit forecast period, assuming a constant growth rate in perpetuity. TV = FCF_(n+1) / (WACC - g)."
    y_as_x: ['fcff_dcf_intrinsic_value', 'fcfe_dcf_intrinsic_value']
    :param fcf_next: "Free cash flow in the first year beyond the projection period (FCF_{n+1})"
    :param weighted_average_cost_of_capital_wacc: "Weighted average cost of capital, the discount rate reflecting the blended cost of equity and after-tax debt"
    :param growth_rate: "Long-term perpetual growth rate of free cash flows (g)"
    :return: "Computed terminal value TV = FCF_(n+1) / (WACC - g)"
    '''
    return fcf_next / (weighted_average_cost_of_capital_wacc - growth_rate)


def theta(S, K, r, sigma, T, q=0.0, option_type='c'):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Option Greeks', 'Black-Scholes']
    function: "Theta measures the rate of change of an option's price with respect to time (time decay). For a call: Theta = -S*e^{-qT}*n(d1)*sigma/(2*sqrt(T)) - r*K*e^{-rT}*N(d2) + q*S*e^{-qT}*N(d1). It represents how much value the option loses per day as it approaches expiration."
    y_as_x: ['cir_short_rate_model', 'cir_zero_coupon_bond_price', 'heston_asset_process', 'heston_variance_process', 'option_delta_hedged_pandl', 'short_rate_bond_pricing_pde']
    :param S: "Current price of the underlying asset"
    :param K: "Strike price of the option"
    :param r: "Risk-free interest rate"
    :param sigma: "Implied volatility of the underlying asset"
    :param T: "Time to expiration in years"
    :param q: "Continuous dividend yield (default 0.0)"
    :param option_type: "'c' for call, 'p' for put (default 'c')"
    :return: "Computed Theta of the option (per year; divide by 365 for daily theta)"
    '''
    from py_vollib.black_scholes.greeks.analytical import theta as bs_theta
    flag = option_type.lower()
    return bs_theta(flag, S, K, T, r, sigma)


def through_the_cycle_pd(default_history):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit Risk Modeling', 'Probability of Default']
    function: "Through-the-cycle (TTC) PD is a long-run average probability of default that smooths out the effects of economic cycles. It is estimated as the long-run average default frequency across multiple business cycles, providing a stable measure for capital allocation."
    y_as_x: ['expected_loss', 'expected_credit_loss_ifrs_9_over_cecl', 'basel_irb_capital_requirement']
    :param default_history: "Array-like of annual default rates observed over a long time horizon spanning multiple business cycles"
    :return: "Computed TTC PD as the long-run average default frequency"
    '''
    default_history = np.asarray(default_history)
    return np.mean(default_history)


def tier_1_capital_ratio(tier_1_capital, risk_weighted_assets_rwa):
    '''
    domain: ['Bank regulation, Basel & prudential ratios']
    subdomain: ['Capital Adequacy', 'Basel III']
    function: "Tier 1 capital ratio measures a bank's core capital (CET1 plus Additional Tier 1) as a percentage of risk-weighted assets. It is a key regulatory metric indicating a bank's ability to absorb losses while continuing operations. Minimum requirements are typically 6% under Basel III."
    y_as_x: ['capital_conservation_buffer', 'large_exposure_ratio']
    :param tier_1_capital: "Total Tier 1 capital (CET1 + Additional Tier 1 instruments)"
    :param risk_weighted_assets_rwa: "Risk-weighted assets computed as the sum of each exposure times its risk weight"
    :return: "Computed Tier 1 capital ratio = Tier 1 Capital / RWA"
    '''
    return tier_1_capital / risk_weighted_assets_rwa


def time_value_option(option_premium, intrinsic_value_call):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Option Pricing', 'Time Value']
    function: "Time value of an option is the portion of the option premium that exceeds its intrinsic value. It reflects the probability that the option will gain additional value before expiration due to underlying price movement. Time value decays as expiration approaches (theta decay)."
    y_as_x: []
    :param option_premium: "Market price (premium) of the option"
    :param intrinsic_value_call: "Intrinsic value of the option = max(S-K, 0) for calls or max(K-S, 0) for puts"
    :return: "Computed time value = Option Premium - Intrinsic Value"
    '''
    return option_premium - intrinsic_value_call


def time_weighted_return_twrr(sub_period_returns):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Return Measurement', 'Performance Evaluation']
    function: "Time-weighted rate of return (TWRR) measures investment performance by compounding sub-period returns, eliminating the impact of external cash flows. It is the industry standard for evaluating portfolio manager performance: TWRR = prod_i(1 + r_i) - 1."
    y_as_x: []
    :param sub_period_returns: "Array-like of sub-period returns r_i (between cash flow dates)"
    :return: "Computed TWRR = product of (1 + r_i) for all sub-periods, minus 1"
    '''
    sub_period_returns = np.asarray(sub_period_returns)
    return np.prod(1 + sub_period_returns) - 1


def tobins_q(market_value_of_assets, replacement_cost_of_assets):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Valuation Ratios', 'Corporate Valuation']
    function: "Tobin's Q ratio compares the market value of a firm's assets to their replacement cost. A Q > 1 suggests the market values the firm above the cost to replace its assets (indicating intangible value or competitive advantages), while Q < 1 suggests the firm is undervalued relative to its asset base."
    y_as_x: []
    :param market_value_of_assets: "Market value of the firm's assets (often approximated as market cap + total debt)"
    :param replacement_cost_of_assets: "Replacement cost of the firm's assets (often approximated by total assets)"
    :return: "Computed Tobin's Q = Market Value of Assets / Replacement Cost of Assets"
    '''
    return market_value_of_assets / replacement_cost_of_assets


def total_capital_ratio(total_capital, risk_weighted_assets_rwa):
    '''
    domain: ['Bank regulation, Basel & prudential ratios']
    subdomain: ['Capital Adequacy', 'Basel III']
    function: "Total capital ratio measures a bank's total regulatory capital (Tier 1 + Tier 2) as a percentage of risk-weighted assets. It is a comprehensive measure of capital adequacy. The minimum requirement under Basel III is typically 8%."
    y_as_x: []
    :param total_capital: "Total regulatory capital (Tier 1 + Tier 2 capital)"
    :param risk_weighted_assets_rwa: "Risk-weighted assets computed as the sum of each exposure times its risk weight"
    :return: "Computed total capital ratio = Total Capital / RWA"
    '''
    return total_capital / risk_weighted_assets_rwa


def tracking_error(returns, benchmark_returns):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Performance Measurement', 'Risk Management']
    function: "Tracking error (also called active risk) measures the standard deviation of the difference between portfolio returns and benchmark returns. It quantifies how closely a portfolio follows its benchmark. Lower tracking error indicates the portfolio closely mimics the benchmark."
    y_as_x: ['information_ratio', 'ex_ante_tracking_error']
    :param returns: "Array-like or pd.Series of portfolio returns"
    :param benchmark_returns: "Array-like or pd.Series of benchmark returns"
    :return: "Computed tracking error = Std(R_p - R_b)"
    '''
    import empyrical
    returns = pd.Series(returns)
    benchmark_returns = pd.Series(benchmark_returns)
    return empyrical.tracking_error(returns, benchmark_returns)


def tranche_attachment_point(subordination_below, pool_balance):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['CDO/CLO Structuring', 'Tranching']
    function: "Tranche attachment point is the level of portfolio losses at which a specific tranche begins to absorb losses. It equals the subordination below the tranche (junior tranche notional) divided by the total pool balance. Losses below this point are absorbed by subordinate tranches."
    y_as_x: ['cdo_tranche_loss']
    :param subordination_below: "Total notional of all tranches subordinate to this tranche"
    :param pool_balance: "Total collateral pool balance"
    :return: "Computed attachment point = subordination below / pool balance"
    '''
    return subordination_below / pool_balance


def tranche_credit_enhancement(overcollateralization, subordination, excess_spread):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Credit Enhancement', 'Structured Products']
    function: "Tranche credit enhancement (CE) is the total protection available to a tranche from all structural features. It includes overcollateralization (excess collateral over notes), subordination (junior tranches absorbing losses first), and excess spread (difference between asset yield and funding cost)."
    y_as_x: []
    :param overcollateralization: "Amount of excess collateral over the tranche notional"
    :param subordination: "Total notional of all tranches subordinate to this tranche"
    :param excess_spread: "Net interest income available to absorb losses (asset yield minus funding cost and fees)"
    :return: "Computed credit enhancement CE = Overcollateralization + Subordination + Excess Spread"
    '''
    return overcollateralization + subordination + excess_spread


def tranche_detachment_point(subordination_above, pool_balance):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['CDO/CLO Structuring', 'Tranching']
    function: "Tranche detachment point is the level of portfolio losses at which a specific tranche is completely wiped out. It equals 1 minus the ratio of subordination above the tranche to the total pool balance. Losses above this point are absorbed by senior tranches."
    y_as_x: ['cdo_tranche_loss']
    :param subordination_above: "Total notional of all tranches senior to this tranche"
    :param pool_balance: "Total collateral pool balance"
    :return: "Computed detachment point = 1 - subordination above / pool balance"
    '''
    return 1 - subordination_above / pool_balance


def tranche_wal(principal_payments, time_periods):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Cash Flow Analysis', 'Amortization']
    function: "Tranche weighted average life (WAL) measures the average time to receive principal payments for a specific tranche. It is computed as the sum of each principal payment times its timing, divided by total principal. WAL is a key metric for assessing prepayment and extension risk."
    y_as_x: []
    :param principal_payments: "Array of principal payment amounts for the tranche at each period"
    :param time_periods: "Array of time periods (in years) corresponding to each principal payment"
    :return: "Computed tranche WAL = sum(t_i * Principal_i) / sum(Principal_i)"
    '''
    principal_payments = np.asarray(principal_payments)
    time_periods = np.asarray(time_periods)
    total_principal = np.sum(principal_payments)
    if total_principal == 0:
        return 0.0
    return np.sum(time_periods * principal_payments) / total_principal


def tranche_yield(tranche_price, cash_flows, time_periods, initial_guess=0.05):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Tranche Valuation', 'Yield Analysis']
    function: "Tranche yield is the internal rate of return that equates the present value of expected tranche cash flows to the tranche purchase price. It is solved iteratively: find y such that Price = sum_t CF_t / (1+y)^t."
    y_as_x: []
    :param tranche_price: "Current market price of the tranche"
    :param cash_flows: "Array of expected cash flows from the tranche"
    :param time_periods: "Array of time periods (in years) for each cash flow"
    :param initial_guess: "Initial guess for the yield (default 0.05)"
    :return: "Computed tranche yield y that solves Price = PV(expected cash flows)"
    '''
    from scipy.optimize import brentq
    cash_flows = np.asarray(cash_flows)
    time_periods = np.asarray(time_periods)

    def pv_diff(y):
        pv = np.sum(cash_flows / (1 + y) ** time_periods)
        return pv - tranche_price

    try:
        return brentq(pv_diff, -0.5, 5.0)
    except ValueError:
        from scipy.optimize import minimize_scalar
        result = minimize_scalar(lambda y: abs(pv_diff(y)), bounds=(-0.5, 5.0), method='bounded')
        return result.x


def transfer_rate_from_curve(term_matched_rate, liquidity_premium=0.0, optionality_premium=0.0):
    '''
    domain: ['Treasury, ALM & balance-sheet management']
    subdomain: ['Funds Transfer Pricing', 'ALM']
    function: "Transfer rate from curve is the internal funds transfer pricing (FTP) rate assigned to a product based on its characteristics. It is the sum of the term-matched funding curve rate plus adjustments for liquidity and optionality premiums."
    y_as_x: ['funds_transfer_pricing_spread', 'funds_transfer_pricing_spread_v2']
    :param term_matched_rate: "The rate from the funding curve matched to the product's repricing or maturity term"
    :param liquidity_premium: "Additional premium for liquidity risk (default 0.0)"
    :param optionality_premium: "Additional premium for embedded options such as prepayment (default 0.0)"
    :return: "Computed FTP rate = term matched rate + liquidity premium + optionality premium"
    '''
    return term_matched_rate + liquidity_premium + optionality_premium


def transition_matrix_probability(transition_matrix, n_steps):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit Migration', 'Rating Transitions']
    function: "Transition matrix probability computes the n-step credit rating transition probabilities by raising the one-step transition matrix to the power n. P_{ij}(n) = [P^n]_{ij} gives the probability of migrating from rating i to rating j in n periods."
    y_as_x: []
    :param transition_matrix: "Square matrix of one-step transition probabilities P"
    :param n_steps: "Number of transition steps n"
    :return: "Computed n-step transition matrix P^n"
    '''
    transition_matrix = np.asarray(transition_matrix)
    return np.linalg.matrix_power(transition_matrix, n_steps)


def treynor_ratio(returns, benchmark_returns, risk_free_rate=0.0):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Risk-Adjusted Performance', 'CAPM-Based Metrics']
    function: "Treynor ratio measures the excess return per unit of systematic risk (beta). It is computed as (E[R_p] - R_f) / beta_p. Unlike the Sharpe ratio which uses total risk (sigma), the Treynor ratio only considers market risk, making it appropriate for diversified portfolios."
    y_as_x: []
    :param returns: "Array-like or pd.Series of portfolio returns"
    :param benchmark_returns: "Array-like or pd.Series of benchmark (market) returns"
    :param risk_free_rate: "Risk-free rate (annualized, default 0.0)"
    :return: "Computed Treynor ratio = (E[R_p] - R_f) / beta_p"
    '''
    returns = np.asarray(returns)
    benchmark_returns = np.asarray(benchmark_returns)
    excess_portfolio = np.mean(returns) - risk_free_rate
    beta_p = np.cov(returns, benchmark_returns)[0, 1] / np.var(benchmark_returns, ddof=1)
    return excess_portfolio / beta_p


def treynor_mazuy_timing(portfolio_returns, benchmark_returns, risk_free_rate=0.0):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Market Timing', 'Performance Attribution']
    function: "Treynor-Mazuy timing model tests for market timing ability by regressing excess portfolio returns on excess market returns and their square: R_p - R_f = alpha + beta*(R_m - R_f) + gamma*(R_m - R_f)^2 + epsilon. A significantly positive gamma indicates successful market timing."
    y_as_x: []
    :param portfolio_returns: "Array-like of portfolio returns"
    :param benchmark_returns: "Array-like of benchmark (market) returns"
    :param risk_free_rate: "Risk-free rate per period (default 0.0)"
    :return: "Dict with 'alpha', 'beta', 'gamma' coefficients and OLS results summary"
    '''
    import statsmodels.api as sm
    portfolio_returns = np.asarray(portfolio_returns)
    benchmark_returns = np.asarray(benchmark_returns)
    y = portfolio_returns - risk_free_rate
    x_excess = benchmark_returns - risk_free_rate
    X = np.column_stack([x_excess, x_excess ** 2])
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()
    return {
        'alpha': model.params[0],
        'beta': model.params[1],
        'gamma': model.params[2],
        'model': model
    }


def triangular_arbitrage_condition(S_AB, S_BC, S_CA):
    '''
    domain: ['FX & international finance']
    subdomain: ['Currency Arbitrage', 'FX Markets']
    function: "Triangular arbitrage condition checks whether the cross rates between three currencies are consistent. In the absence of arbitrage, S_{A/B} x S_{B/C} x S_{C/A} = 1. If the product deviates from 1, an arbitrage opportunity exists."
    y_as_x: []
    :param S_AB: "Exchange rate of currency A per unit of currency B"
    :param S_BC: "Exchange rate of currency B per unit of currency C"
    :param S_CA: "Exchange rate of currency C per unit of currency A"
    :return: "Product S_AB x S_BC x S_CA (equals 1 under no-arbitrage; deviation indicates arbitrage opportunity)"
    '''
    return S_AB * S_BC * S_CA


def trigger_based_step_down(delinquency_ratio, cnl_ratio, oc_ratio,
                            delinquency_threshold, cnl_threshold, oc_threshold):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Deal Triggers', 'Cash Flow Waterfall']
    function: "Trigger-based step-down determines whether a securitization deal can release subordination and step down the credit enhancement. Step-down is allowed only when all performance tests are satisfied: delinquency ratio below threshold, cumulative net losses below threshold, and overcollateralization ratio above its threshold."
    y_as_x: []
    :param delinquency_ratio: "Current delinquency ratio of the collateral pool"
    :param cnl_ratio: "Current cumulative net loss ratio"
    :param oc_ratio: "Current overcollateralization ratio"
    :param delinquency_threshold: "Maximum allowable delinquency ratio for step-down"
    :param cnl_threshold: "Maximum allowable CNL ratio for step-down"
    :param oc_threshold: "Minimum required OC ratio for step-down"
    :return: "Boolean indicating whether step-down conditions are satisfied (True = step-down allowed)"
    '''
    return (delinquency_ratio <= delinquency_threshold and
            cnl_ratio <= cnl_threshold and
            oc_ratio >= oc_threshold)


def trinomial_tree_option_value(S, K, r, sigma, T, n_steps=100, option_type='call', exercise='european'):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Numerical Methods', 'Option Pricing']
    function: "Trinomial tree option pricing values an option by constructing a three-branch lattice where the underlying can move up, stay flat, or move down at each step. The option value is the discounted expected value across the three branches at each node, with early exercise checks for American-style options."
    y_as_x: []
    :param S: "Current price of the underlying asset"
    :param K: "Strike price of the option"
    :param r: "Risk-free interest rate"
    :param sigma: "Volatility of the underlying asset"
    :param T: "Time to expiration in years"
    :param n_steps: "Number of time steps in the tree (default 100)"
    :param option_type: "'call' or 'put' (default 'call')"
    :param exercise: "'european' or 'american' (default 'european')"
    :return: "Computed option value via trinomial tree"
    '''
    dt = T / n_steps
    u = np.exp(sigma * np.sqrt(2 * dt))
    d = 1 / u
    m = 1.0  # middle factor
    # Risk-neutral probabilities
    pu = ((np.exp(r * dt / 2) - np.exp(-sigma * np.sqrt(dt / 2))) /
          (np.exp(sigma * np.sqrt(dt / 2)) - np.exp(-sigma * np.sqrt(dt / 2)))) ** 2
    pd_prob = ((np.exp(sigma * np.sqrt(dt / 2)) - np.exp(r * dt / 2)) /
               (np.exp(sigma * np.sqrt(dt / 2)) - np.exp(-sigma * np.sqrt(dt / 2)))) ** 2
    pm = 1 - pu - pd_prob
    discount = np.exp(-r * dt)

    # Asset prices at maturity
    n_nodes = 2 * n_steps + 1
    asset_prices = np.zeros(n_nodes)
    for i in range(n_nodes):
        asset_prices[i] = S * (u ** (n_steps - i))

    # Payoff at maturity
    if option_type == 'call':
        values = np.maximum(asset_prices - K, 0)
    else:
        values = np.maximum(K - asset_prices, 0)

    # Backward induction
    for step in range(n_steps - 1, -1, -1):
        n_curr = 2 * step + 1
        new_values = np.zeros(n_curr)
        for i in range(n_curr):
            new_values[i] = discount * (pu * values[i] + pm * values[i + 1] + pd_prob * values[i + 2])
            if exercise == 'american':
                asset_price_i = S * (u ** (step - i))
                if option_type == 'call':
                    intrinsic = max(asset_price_i - K, 0)
                else:
                    intrinsic = max(K - asset_price_i, 0)
                new_values[i] = max(new_values[i], intrinsic)
        values = new_values

    return values[0]


def trix(close, period=15):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Momentum Indicators', 'Trend Following']
    function: "TRIX is a momentum oscillator that displays the percentage rate of change of a triple exponentially smoothed moving average. It filters out insignificant price movements and helps identify overbought/oversold conditions and divergences."
    y_as_x: []
    :param close: "Array-like or pd.Series of closing prices"
    :param period: "Lookback period for the triple EMA (default 15)"
    :return: "pd.Series of TRIX values (1-period ROC of triple EMA)"
    '''
    import talib
    close = np.asarray(close, dtype=np.float64)
    return talib.TRIX(close, timeperiod=period)


def true_range(high, low, close):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Volatility Indicators']
    function: "True range (TR) extends the simple daily range (High - Low) by accounting for gaps from the previous close. It is the maximum of: (H - L), |H - C_{t-1}|, and |L - C_{t-1}|. True range is the building block for the Average True Range (ATR) indicator."
    y_as_x: ['average_true_range_atr', 'ultimate_oscillator']
    :param high: "Array-like or pd.Series of high prices"
    :param low: "Array-like or pd.Series of low prices"
    :param close: "Array-like or pd.Series of closing prices"
    :return: "Array of true range values"
    '''
    import talib
    high = np.asarray(high, dtype=np.float64)
    low = np.asarray(low, dtype=np.float64)
    close = np.asarray(close, dtype=np.float64)
    return talib.TRANGE(high, low, close)


def turbo_amortization_amount(excess_cash, fees, note_interest):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Cash Flow Waterfall', 'Amortization']
    function: "Turbo amortization is the excess cash redirected to accelerate the paydown of senior tranche principal after all required fees and note interest have been paid. It is a structural feature that speeds up deleveraging in securitizations."
    y_as_x: []
    :param excess_cash: "Total available cash flow from the collateral pool"
    :param fees: "Total fees (servicing, trustee, etc.) that must be paid first"
    :param note_interest: "Total note interest due on all tranches"
    :return: "Computed turbo amount = max(excess_cash - fees - note_interest, 0)"
    '''
    return max(excess_cash - fees - note_interest, 0)


def turnover_ratio(volume, shares_outstanding):
    '''
    domain: ['Liquidity risk & market liquidity']
    subdomain: ['Market Liquidity', 'Trading Activity']
    function: "Turnover ratio measures the trading activity of a security relative to its total shares outstanding. A higher turnover ratio indicates greater liquidity and trading interest. It is computed as Volume / Shares Outstanding."
    y_as_x: []
    :param volume: "Trading volume over the measurement period"
    :param shares_outstanding: "Total number of shares outstanding"
    :return: "Computed turnover ratio = Volume / Shares Outstanding"
    '''
    return volume / shares_outstanding


def tvpi(residual_value, distributions, paid_in_capital):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Fund Performance', 'Return Multiples']
    function: "Total Value to Paid-In Capital (TVPI) is the ratio of the total value of a private equity fund (residual value plus cumulative distributions) to the total capital invested by LPs. It is the most comprehensive multiple measuring overall fund performance."
    y_as_x: []
    :param residual_value: "Current net asset value (NAV) of unrealized investments"
    :param distributions: "Cumulative distributions returned to LPs"
    :param paid_in_capital: "Total capital called and invested by LPs"
    :return: "Computed TVPI = (Residual Value + Distributions) / Paid-In Capital"
    '''
    return (residual_value + distributions) / paid_in_capital


def twap(prices):
    '''
    domain: ['Trading, execution & market microstructure']
    subdomain: ['Execution Algorithms', 'Benchmark Pricing']
    function: "Time-Weighted Average Price (TWAP) is the simple arithmetic average of prices over a specified time period. It gives equal weight to each time observation regardless of volume, making it useful as an execution benchmark for orders that aim to minimize timing impact."
    y_as_x: []
    :param prices: "Array-like of prices observed at regular time intervals"
    :return: "Computed TWAP = (1/n) * sum(P_i)"
    '''
    prices = np.asarray(prices)
    return np.mean(prices)


def ulcer_index(returns):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Downside Risk', 'Risk Metrics']
    function: "The Ulcer Index measures downside risk by computing the root mean square of percentage drawdowns from the high water mark. Unlike standard deviation, it only penalizes downside movements, capturing the depth and duration of drawdowns. UI = sqrt(mean(drawdown^2))."
    y_as_x: []
    :param returns: "Array-like or pd.Series of portfolio returns"
    :return: "Computed Ulcer Index = sqrt(mean(drawdown^2))"
    '''
    import quantstats as qs
    returns = pd.Series(returns)
    return qs.stats.ulcer_index(returns)


def ultimate_oscillator(high, low, close, period1=7, period2=14, period3=28):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Momentum Indicators']
    function: "The Ultimate Oscillator is a multi-timeframe momentum oscillator that uses the weighted average of three different time periods (typically 7, 14, and 28) of buying pressure relative to true range. It aims to reduce false divergence signals common in single-period oscillators."
    y_as_x: []
    :param high: "Array-like or pd.Series of high prices"
    :param low: "Array-like or pd.Series of low prices"
    :param close: "Array-like or pd.Series of closing prices"
    :param period1: "Short period (default 7)"
    :param period2: "Medium period (default 14)"
    :param period3: "Long period (default 28)"
    :return: "Array of Ultimate Oscillator values"
    '''
    import talib
    high = np.asarray(high, dtype=np.float64)
    low = np.asarray(low, dtype=np.float64)
    close = np.asarray(close, dtype=np.float64)
    return talib.ULTOSC(high, low, close, timeperiod1=period1, timeperiod2=period2, timeperiod3=period3)


def uncovered_interest_parity_uip(S_t, r_domestic, r_foreign, T=1.0):
    '''
    domain: ['FX & international finance']
    subdomain: ['Interest Rate Parity', 'Currency Economics']
    function: "Uncovered interest parity (UIP) states that the expected change in the exchange rate equals the interest rate differential between two countries. The expected future spot rate is: E[S_{t+T}] / S_t = (1 + r_d * T) / (1 + r_f * T). Unlike CIP, UIP involves exchange rate risk."
    y_as_x: []
    :param S_t: "Current spot exchange rate (domestic per foreign)"
    :param r_domestic: "Domestic interest rate"
    :param r_foreign: "Foreign interest rate"
    :param T: "Time period in years (default 1.0)"
    :return: "Expected future spot rate E[S_{t+T}]"
    '''
    return S_t * (1 + r_domestic * T) / (1 + r_foreign * T)


def unexpected_loss(probability_of_default, loss_given_default, exposure_at_default_ead):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit Risk Capital', 'Loss Distributions']
    function: "Unexpected loss (UL) measures the volatility of potential credit losses around the expected loss. It is the standard deviation of the loss distribution for a single exposure: UL = sqrt(PD * (1-PD)) * LGD * EAD. It is a key input for determining economic and regulatory capital."
    y_as_x: ['credit_var', 'credit_portfolio_variance_independent_defaults']
    :param probability_of_default: "Probability of default (PD) of the obligor"
    :param loss_given_default: "Loss given default (LGD), the fraction of exposure lost upon default"
    :param exposure_at_default_ead: "Exposure at default (EAD), the total amount at risk"
    :return: "Computed unexpected loss UL = sqrt(PD * (1-PD)) * LGD * EAD"
    '''
    return np.sqrt(probability_of_default * (1 - probability_of_default)) * loss_given_default * exposure_at_default_ead


def unlevered_beta(levered_beta, tax_rate, debt, equity):
    '''
    domain: ['Corporate finance, valuation & capital budgeting']
    subdomain: ['Capital Structure', 'Risk Analysis']
    function: "Unlevered beta (asset beta) removes the effect of financial leverage from the observed equity beta using the Hamada equation. It represents the systematic risk of the firm's assets without the amplifying effect of debt: beta_U = beta_L / [1 + (1-T) * D/E]."
    y_as_x: ['levered_beta_hamada', 'cost_of_equity_capm']
    :param levered_beta: "Observed equity beta (beta_L) including the effect of financial leverage"
    :param tax_rate: "Marginal corporate tax rate (T)"
    :param debt: "Market value of the firm's debt (D)"
    :param equity: "Market value of the firm's equity (E)"
    :return: "Computed unlevered beta = beta_L / [1 + (1-T) * D/E]"
    '''
    return levered_beta / (1 + (1 - tax_rate) * debt / equity)


def unlevered_yield(net_operating_income_noi, purchase_price):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Property Returns', 'Investment Analysis']
    function: "Unlevered yield (also called going-in cap rate or free-and-clear return) measures the return on a property investment before any financing costs. It is computed as NOI / Purchase Price, providing a baseline return that is independent of the capital structure."
    y_as_x: []
    :param net_operating_income_noi: "Net operating income of the property, computed as rental revenue plus other income minus operating expenses"
    :param purchase_price: "Total acquisition price of the property"
    :return: "Computed unlevered yield = NOI / Purchase Price"
    '''
    return net_operating_income_noi / purchase_price


def up_capture_ratio(returns, benchmark_returns):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Capture Ratios', 'Relative Performance']
    function: "Up capture ratio measures how much of the benchmark's positive returns are captured by the portfolio. It is the ratio of the portfolio's average return during up-market periods to the benchmark's average return during those same periods. A ratio above 100% indicates outperformance during up markets."
    y_as_x: []
    :param returns: "Array-like or pd.Series of portfolio returns"
    :param benchmark_returns: "Array-like or pd.Series of benchmark returns"
    :return: "Computed up capture ratio = mean(R_p | R_b > 0) / mean(R_b | R_b > 0)"
    '''
    import quantstats as qs
    returns = pd.Series(returns)
    benchmark_returns = pd.Series(benchmark_returns)
    benchmark_up = benchmark_returns > 0
    if benchmark_up.sum() == 0:
        return np.nan
    return np.mean(returns[benchmark_up]) / np.mean(benchmark_returns[benchmark_up])


def upside_capture(returns, benchmark_returns):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Capture Ratios', 'Relative Performance']
    function: "Upside capture measures the portfolio's average return during periods when the benchmark return is positive, relative to the benchmark's average positive return. It is equivalent to the up capture ratio and indicates how well the portfolio participates in bull markets."
    y_as_x: []
    :param returns: "Array-like or pd.Series of portfolio returns"
    :param benchmark_returns: "Array-like or pd.Series of benchmark returns"
    :return: "Computed upside capture = Avg(R_p | R_b > 0) / Avg(R_b | R_b > 0)"
    '''
    returns = np.asarray(returns)
    benchmark_returns = np.asarray(benchmark_returns)
    up_mask = benchmark_returns > 0
    if np.sum(up_mask) == 0:
        return np.nan
    return np.mean(returns[up_mask]) / np.mean(benchmark_returns[up_mask])


def upside_potential_ratio(returns, mar=0.0):
    '''
    domain: ['Asset management & portfolio optimization']
    subdomain: ['Risk-Adjusted Performance', 'Downside Risk']
    function: "Upside potential ratio (UPR) measures the ratio of upside potential (expected returns above a minimum acceptable return) to downside deviation. It captures the trade-off between upside opportunity and downside risk, providing a more nuanced view than the Sortino ratio."
    y_as_x: []
    :param returns: "Array-like of portfolio returns"
    :param mar: "Minimum acceptable return threshold (default 0.0)"
    :return: "Computed UPR = Upside Potential / Downside Deviation"
    '''
    returns = np.asarray(returns)
    upside = np.mean(np.maximum(returns - mar, 0))
    downside = np.sqrt(np.mean(np.minimum(returns - mar, 0) ** 2))
    if downside == 0:
        return np.inf
    return upside / downside


def utilization_rate(outstanding_balance, credit_limit):
    '''
    domain: ['Banking, consumer lending & project finance']
    subdomain: ['Consumer Credit', 'Credit Risk']
    function: "Utilization rate (also called credit utilization ratio) measures the proportion of available credit that is currently being used. It is a key factor in credit scoring and risk assessment. Higher utilization typically indicates greater credit risk."
    y_as_x: ['exposure_at_default_ead', 'credit_conversion_factor_ccf']
    :param outstanding_balance: "Current outstanding balance on the credit facility"
    :param credit_limit: "Total approved credit limit"
    :return: "Computed utilization rate = Outstanding Balance / Credit Limit"
    '''
    return outstanding_balance / credit_limit


def vacancy_rate(vacant_units_or_lost_rent, total_potential_units_or_rent):
    '''
    domain: ['Real estate finance & mortgages']
    subdomain: ['Property Operations', 'Income Analysis']
    function: "Vacancy rate measures the proportion of rental units that are unoccupied or the proportion of potential rental income that is lost due to vacancies. It is a key indicator of property performance and market conditions."
    y_as_x: ['effective_gross_income', 'break_even_occupancy']
    :param vacant_units_or_lost_rent: "Number of vacant units or amount of lost rental income"
    :param total_potential_units_or_rent: "Total number of units or total potential gross rental income"
    :return: "Computed vacancy rate = Vacant Units (or Lost Rent) / Total Units (or Potential Rent)"
    '''
    return vacant_units_or_lost_rent / total_potential_units_or_rent


def vanna(S, K, r, sigma, T, q=0.0):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Higher-Order Greeks', 'Volatility Sensitivity']
    function: "Vanna is a second-order Greek measuring the sensitivity of delta to changes in volatility (or equivalently, the sensitivity of vega to changes in the underlying price). It is computed as Vanna = -e^{-qT} * n(d1) * d2 / sigma, where n(d1) is the standard normal PDF."
    y_as_x: []
    :param S: "Current price of the underlying asset"
    :param K: "Strike price of the option"
    :param r: "Risk-free interest rate"
    :param sigma: "Implied volatility of the underlying asset"
    :param T: "Time to expiration in years"
    :param q: "Continuous dividend yield (default 0.0)"
    :return: "Computed Vanna = -e^{-qT} * n(d1) * d2 / sigma"
    '''
    d1_val = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2_val = d1_val - sigma * np.sqrt(T)
    n_d1 = stats.norm.pdf(d1_val)
    return -np.exp(-q * T) * n_d1 * d2_val / sigma


def var_p(data, lags=1):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Multivariate Time Series', 'Vector Autoregression']
    function: "VAR(p) - Vector Autoregression of order p models multiple time series jointly, where each variable is a linear function of its own past values and the past values of all other variables: y_t = c + A_1*y_{t-1} + ... + A_p*y_{t-p} + u_t."
    y_as_x: ['impulse_response_function', 'granger_causality', 'vecm']
    :param data: "pd.DataFrame or 2D array of multivariate time series data (each column is a variable)"
    :param lags: "Number of lag terms p in the VAR model (default 1)"
    :return: "Fitted VAR model results from statsmodels"
    '''
    from statsmodels.tsa.api import VAR
    data = pd.DataFrame(data)
    model = VAR(data)
    results = model.fit(lags)
    return results


def variance_of_loss(loss_values, probabilities=None):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Loss Distributions', 'Risk Theory']
    function: "Variance of loss Var(L) measures the dispersion of the loss random variable L around its expected value. It is computed as Var(L) = E[L^2] - (E[L])^2. In actuarial science, it is used to assess the volatility of insurance claims and set appropriate reserves and premiums."
    y_as_x: []
    :param loss_values: "Array-like of possible loss values or realized losses"
    :param probabilities: "Optional array of probabilities for each loss value; if None, assumes equal weights"
    :return: "Computed variance of loss Var(L) = E[L^2] - (E[L])^2"
    '''
    loss_values = np.asarray(loss_values, dtype=float)
    if probabilities is not None:
        probabilities = np.asarray(probabilities, dtype=float)
        e_l = np.sum(loss_values * probabilities)
        e_l2 = np.sum(loss_values ** 2 * probabilities)
    else:
        e_l = np.mean(loss_values)
        e_l2 = np.mean(loss_values ** 2)
    return e_l2 - e_l ** 2


def variance_ratio_test(returns, q=2):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Market Efficiency', 'Random Walk Tests']
    function: "Variance ratio test examines whether a time series follows a random walk by comparing the variance of q-period returns to q times the variance of 1-period returns. Under a random walk, VR(q) = 1. Significant deviation from 1 indicates serial correlation or mean reversion."
    y_as_x: []
    :param returns: "Array-like of returns (typically log returns)"
    :param q: "Aggregation period (default 2)"
    :return: "Dict with 'variance_ratio', 'z_statistic', and 'p_value'"
    '''
    returns = np.asarray(returns)
    n = len(returns)
    # Variance of 1-period returns
    var_1 = np.var(returns, ddof=1)
    # q-period returns
    q_returns = np.array([np.sum(returns[i:i + q]) for i in range(0, n - q + 1)])
    var_q = np.var(q_returns, ddof=1)
    vr = var_q / (q * var_1)
    # Asymptotic z-statistic under homoskedasticity
    z_stat = (vr - 1) / np.sqrt(2 * (q - 1) / (3 * q * n))
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
    return {'variance_ratio': vr, 'z_statistic': z_stat, 'p_value': p_value}


def variance_swap_fair_strike(realized_variance_history=None, forward_variances=None):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Variance Swaps', 'Volatility Derivatives']
    function: "The fair strike of a variance swap is the expected risk-neutral realized variance over the swap's life. K_var = E_Q[realized variance]. It can be estimated from the implied volatility surface using the log-strip of options, or approximated from historical realized variance."
    y_as_x: ['vix_variance_relation']
    :param realized_variance_history: "Array-like of historical realized variances for estimation"
    :param forward_variances: "Array-like of forward-looking variance estimates from the options market"
    :return: "Computed fair variance strike K_var"
    '''
    if forward_variances is not None:
        return np.mean(np.asarray(forward_variances))
    elif realized_variance_history is not None:
        return np.mean(np.asarray(realized_variance_history))
    else:
        raise ValueError("Either realized_variance_history or forward_variances must be provided")


def vasicek_one_factor_portfolio_loss_quantile(pd_value, lgd, rho, alpha=0.999):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Portfolio Credit Risk', 'Basel IRB']
    function: "Vasicek one-factor portfolio loss quantile computes the loss quantile for a homogeneous credit portfolio under the Vasicek/Basel single-factor Gaussian copula model. L_alpha = LGD * Phi((Phi^{-1}(PD) + sqrt(rho) * Phi^{-1}(alpha)) / sqrt(1-rho))."
    y_as_x: ['basel_irb_capital_requirement']
    :param pd_value: "Probability of default (PD)"
    :param lgd: "Loss given default (LGD)"
    :param rho: "Asset correlation parameter (rho)"
    :param alpha: "Quantile level (default 0.999 for 99.9% as in Basel)"
    :return: "Computed portfolio loss quantile L_alpha"
    '''
    from scipy.stats import norm
    numerator = norm.ppf(pd_value) + np.sqrt(rho) * norm.ppf(alpha)
    denominator = np.sqrt(1 - rho)
    return lgd * norm.cdf(numerator / denominator)


def vasicek_short_rate_process(r0, a, b, sigma, T, n_steps=252, n_paths=1000, seed=None):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Short-Rate Models', 'Stochastic Processes']
    function: "Vasicek short-rate process simulates the evolution of the instantaneous short rate using the mean-reverting Ornstein-Uhlenbeck process: dr_t = a*(b - r_t)*dt + sigma*dW_t, where a is the speed of mean reversion, b is the long-run mean, and sigma is the volatility."
    y_as_x: ['affine_term_structure_bond_price', 'short_rate_bond_pricing_pde']
    :param r0: "Initial short rate"
    :param a: "Speed of mean reversion"
    :param b: "Long-run mean level of the short rate"
    :param sigma: "Volatility of the short rate"
    :param T: "Time horizon in years"
    :param n_steps: "Number of time steps (default 252)"
    :param n_paths: "Number of simulation paths (default 1000)"
    :param seed: "Random seed for reproducibility"
    :return: "2D array of simulated short rate paths (n_paths x n_steps+1)"
    '''
    if seed is not None:
        np.random.seed(seed)
    dt = T / n_steps
    rates = np.zeros((n_paths, n_steps + 1))
    rates[:, 0] = r0
    for t in range(n_steps):
        dW = np.random.standard_normal(n_paths) * np.sqrt(dt)
        rates[:, t + 1] = rates[:, t] + a * (b - rates[:, t]) * dt + sigma * dW
    return rates


def vc_liquidation_preference_payout(preference, ownership_pct, exit_value, participating=False, cap=None):
    '''
    domain: ['Private equity, venture capital & LBO']
    subdomain: ['Venture Capital', 'Liquidation Preferences']
    function: "VC liquidation preference payout determines the amount an investor receives upon a liquidity event (exit). With a simple preference, the investor receives the greater of their preference amount or their pro-rata share. With participating preferred, they receive both the preference and their pro-rata share of remaining value, optionally subject to a cap."
    y_as_x: []
    :param preference: "Liquidation preference amount (typically 1x invested capital)"
    :param ownership_pct: "Investor's ownership percentage (as a decimal, e.g., 0.20 for 20%)"
    :param exit_value: "Total exit/liquidation value of the company"
    :param participating: "Whether the preferred stock is participating (default False)"
    :param cap: "Optional participation cap as a multiple of the preference amount"
    :return: "Computed payout to the investor based on liquidation preference terms"
    '''
    pro_rata = ownership_pct * exit_value
    if participating:
        remaining = exit_value - preference
        payout = preference + ownership_pct * max(remaining, 0)
        if cap is not None:
            payout = min(payout, cap * preference)
        return max(payout, pro_rata)
    else:
        return max(preference, pro_rata)


def vecm(data, k_ar_diff=1, coint_rank=1):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Cointegration', 'Vector Error Correction']
    function: "VECM (Vector Error Correction Model) models the short-run dynamics and long-run equilibrium relationships among cointegrated time series: Delta y_t = Pi * y_{t-1} + sum_i Gamma_i * Delta y_{t-i} + u_t, where Pi = alpha * beta' captures the error correction (cointegrating) relationship."
    y_as_x: []
    :param data: "pd.DataFrame or 2D array of multivariate time series data"
    :param k_ar_diff: "Number of lagged difference terms (default 1)"
    :param coint_rank: "Cointegration rank (number of cointegrating relationships, default 1)"
    :return: "Fitted VECM model results from statsmodels"
    '''
    from statsmodels.tsa.vector_ar.vecm import VECM
    data = pd.DataFrame(data)
    model = VECM(data, k_ar_diff=k_ar_diff, coint_rank=coint_rank)
    results = model.fit()
    return results


def vega(S, K, r, sigma, T, q=0.0, option_type='c'):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Option Greeks', 'Black-Scholes']
    function: "Vega measures the sensitivity of an option's price to changes in implied volatility. It is computed as Vega = S * e^{-qT} * n(d1) * sqrt(T), where n(d1) is the standard normal PDF evaluated at d1. Vega is the same for calls and puts and is always positive for long option positions."
    y_as_x: ['option_delta_hedged_pandl', 'vomma_over_volga']
    :param S: "Current price of the underlying asset"
    :param K: "Strike price of the option"
    :param r: "Risk-free interest rate"
    :param sigma: "Implied volatility of the underlying asset"
    :param T: "Time to expiration in years"
    :param q: "Continuous dividend yield (default 0.0)"
    :param option_type: "'c' for call, 'p' for put (default 'c')"
    :return: "Computed Vega of the option"
    '''
    from py_vollib.black_scholes.greeks.analytical import vega as bs_vega
    flag = option_type.lower()
    return bs_vega(flag, S, K, T, r, sigma)


def vintage_cumulative_loss(cumulative_net_losses, original_balance):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Vintage Analysis', 'Loan Performance']
    function: "Vintage cumulative loss tracks the total net losses as a percentage of the original balance for a cohort (vintage) of loans originated at the same time. It is a key metric for assessing credit quality trends and comparing performance across loan vintages."
    y_as_x: []
    :param cumulative_net_losses: "Total cumulative net losses (charge-offs minus recoveries) for the vintage"
    :param original_balance: "Original total balance of the vintage at origination"
    :return: "Computed vintage loss rate = cumulative net losses / original balance"
    '''
    return cumulative_net_losses / original_balance


def vix_variance_relation(vix_level):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Volatility Indices', 'Variance Estimation']
    function: "The VIX-variance relation shows that VIX^2 approximates the expected 30-day risk-neutral variance of the S&P 500 index, scaled by 100^2. Converting VIX to expected 30-day variance: Expected Variance = (VIX/100)^2, which represents the annualized variance under the risk-neutral measure."
    y_as_x: []
    :param vix_level: "VIX index level (e.g., 20 for VIX at 20%)"
    :return: "Expected 30-day annualized risk-neutral variance = (VIX/100)^2"
    '''
    return (vix_level / 100) ** 2


def volatility_clustering_test(returns, n_lags=20):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Volatility Dynamics', 'Time Series Properties']
    function: "Volatility clustering test examines whether large (small) changes in asset prices tend to be followed by large (small) changes, regardless of direction. It is tested by checking whether the autocorrelation function (ACF) of squared returns is significantly positive, indicating ARCH effects."
    y_as_x: []
    :param returns: "Array-like of asset returns"
    :param n_lags: "Number of lags to test for autocorrelation (default 20)"
    :return: "Dict with 'acf_squared' (ACF of r^2), 'ljung_box_stat', and 'ljung_box_pvalue'"
    '''
    from statsmodels.tsa.stattools import acf
    from statsmodels.stats.diagnostic import acorr_ljungbox
    returns = np.asarray(returns)
    squared_returns = returns ** 2
    acf_values = acf(squared_returns, nlags=n_lags, fft=True)
    lb_result = acorr_ljungbox(squared_returns, lags=[n_lags], return_df=True)
    return {
        'acf_squared': acf_values,
        'ljung_box_stat': lb_result['lb_stat'].values[0],
        'ljung_box_pvalue': lb_result['lb_pvalue'].values[0]
    }


def volume_weighted_average_price_vwap(high, low, close, volume):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Volume Indicators', 'Benchmark Pricing']
    function: "Volume-Weighted Average Price (VWAP) computes the average price weighted by volume over a trading period. It is calculated as the cumulative sum of price times volume divided by cumulative volume. VWAP serves as a benchmark for institutional execution quality."
    y_as_x: []
    :param high: "Array-like or pd.Series of high prices"
    :param low: "Array-like or pd.Series of low prices"
    :param close: "Array-like or pd.Series of closing prices"
    :param volume: "Array-like or pd.Series of trading volumes"
    :return: "Array of cumulative intraday VWAP values"
    '''
    high = np.asarray(high, dtype=np.float64)
    low = np.asarray(low, dtype=np.float64)
    close = np.asarray(close, dtype=np.float64)
    volume = np.asarray(volume, dtype=np.float64)
    typical_price = (high + low + close) / 3
    cumulative_tp_vol = np.cumsum(typical_price * volume)
    cumulative_vol = np.cumsum(volume)
    return cumulative_tp_vol / cumulative_vol


def vomma_over_volga(S, K, r, sigma, T, q=0.0):
    '''
    domain: ['Derivatives, options & volatility']
    subdomain: ['Higher-Order Greeks', 'Volatility Sensitivity']
    function: "Vomma (also called volga) is the second-order sensitivity of an option's price to changes in implied volatility. It measures the convexity of the option price with respect to volatility. Vomma = Vega * d1 * d2 / sigma, where d1 and d2 are the Black-Scholes parameters."
    y_as_x: []
    :param S: "Current price of the underlying asset"
    :param K: "Strike price of the option"
    :param r: "Risk-free interest rate"
    :param sigma: "Implied volatility of the underlying asset"
    :param T: "Time to expiration in years"
    :param q: "Continuous dividend yield (default 0.0)"
    :return: "Computed Vomma = Vega * d1 * d2 / sigma"
    '''
    d1_val = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2_val = d1_val - sigma * np.sqrt(T)
    vega_val = S * np.exp(-q * T) * stats.norm.pdf(d1_val) * np.sqrt(T)
    return vega_val * d1_val * d2_val / sigma


def vwap(prices, volumes):
    '''
    domain: ['Trading, execution & market microstructure']
    subdomain: ['Execution Benchmarks', 'Trade Analysis']
    function: "VWAP (Volume-Weighted Average Price) is the ratio of the total dollar value traded to the total volume traded over a given period. It provides a benchmark for measuring execution quality of trades: VWAP = sum(P_i * V_i) / sum(V_i)."
    y_as_x: ['vwap_benchmark']
    :param prices: "Array-like of trade prices P_i"
    :param volumes: "Array-like of trade volumes V_i"
    :return: "Computed VWAP = sum(P_i * V_i) / sum(V_i)"
    '''
    prices = np.asarray(prices)
    volumes = np.asarray(volumes)
    return np.sum(prices * volumes) / np.sum(volumes)


def vwap_benchmark(prices, volumes):
    '''
    domain: ['Liquidity risk, market liquidity & execution cost']
    subdomain: ['Execution Quality', 'Benchmark Pricing']
    function: "VWAP benchmark computes the volume-weighted average price used as a standard benchmark for evaluating execution quality. It is identical to VWAP: sum(P_t * V_t) / sum(V_t), but used specifically in the context of transaction cost analysis."
    y_as_x: []
    :param prices: "Array-like of market prices at each time interval"
    :param volumes: "Array-like of market volumes at each time interval"
    :return: "Computed VWAP benchmark = sum(P_t * V_t) / sum(V_t)"
    '''
    prices = np.asarray(prices)
    volumes = np.asarray(volumes)
    return np.sum(prices * volumes) / np.sum(volumes)


def weighted_average_cost_of_capital_wacc(equity_value, debt_value, cost_of_equity, pre_tax_cost_of_debt, tax_rate):
    '''
    domain: ['Corporate finance & capital budgeting']
    subdomain: ['Cost of Capital', 'Valuation']
    function: "WACC (Weighted Average Cost of Capital) is the blended cost of a firm's capital, weighing the cost of equity and after-tax cost of debt by their respective proportions in the capital structure. WACC = (E/V)*R_e + (D/V)*R_d*(1-T), where V = E + D."
    y_as_x: ['terminal_value_gordon_growth', 'fcff_dcf_intrinsic_value', 'economic_value_added_eva', 'net_present_value_npv']
    :param equity_value: "Market value of equity (E)"
    :param debt_value: "Market value of debt (D)"
    :param cost_of_equity: "Cost of equity capital (R_e)"
    :param pre_tax_cost_of_debt: "Pre-tax cost of debt (yield on debt, R_d)"
    :param tax_rate: "Corporate marginal tax rate (T)"
    :return: "Computed WACC = (E/V)*R_e + (D/V)*R_d*(1-T)"
    '''
    total_value = equity_value + debt_value
    return (equity_value / total_value) * cost_of_equity + (debt_value / total_value) * pre_tax_cost_of_debt * (
            1 - tax_rate)


def weighted_average_coupon_wac(weights, coupons):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Pool Characteristics', 'MBS Analytics']
    function: "Weighted average coupon (WAC) is the average coupon rate of a pool of loans, weighted by each loan's outstanding balance. It is a key metric for MBS and ABS pools, indicating the average interest rate earned on the collateral."
    y_as_x: ['excess_spread', 'net_weighted_average_spread']
    :param weights: "Array-like of loan balance weights w_i (should sum to 1, or will be normalized)"
    :param coupons: "Array-like of coupon rates for each loan"
    :return: "Computed WAC = sum(w_i * coupon_i)"
    '''
    weights = np.asarray(weights)
    coupons = np.asarray(coupons)
    if np.sum(weights) != 1.0:
        weights = weights / np.sum(weights)
    return np.sum(weights * coupons)


def weighted_average_life_wal(principal_payments, time_periods):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Cash Flow Analysis', 'Amortization']
    function: "Weighted average life (WAL) is the average time to receive principal payments, weighted by the amount of principal received at each date. It measures the effective maturity of a structured security and is a key metric for interest rate risk and prepayment analysis."
    y_as_x: []
    :param principal_payments: "Array-like of principal payment amounts at each period"
    :param time_periods: "Array-like of time periods (in years) corresponding to each principal payment"
    :return: "Computed WAL = sum(t * Principal_t) / Total Principal"
    '''
    principal_payments = np.asarray(principal_payments)
    time_periods = np.asarray(time_periods)
    total_principal = np.sum(principal_payments)
    if total_principal == 0:
        return 0.0
    return np.sum(time_periods * principal_payments) / total_principal


def weighted_average_life_of_loan_portfolio(principal_payments, time_periods):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Portfolio Analytics', 'Maturity Analysis']
    function: "Weighted average life of a loan portfolio is the average time to receive principal repayments across all loans in the portfolio, weighted by principal amounts. It is computed as WAL = sum(t * Principal_t) / sum(Principal_t)."
    y_as_x: []
    :param principal_payments: "Array-like of principal payment amounts at each period across the portfolio"
    :param time_periods: "Array-like of time periods (in years) corresponding to each principal payment"
    :return: "Computed portfolio WAL = sum(t * Principal_t) / sum(Principal_t)"
    '''
    principal_payments = np.asarray(principal_payments)
    time_periods = np.asarray(time_periods)
    total_principal = np.sum(principal_payments)
    if total_principal == 0:
        return 0.0
    return np.sum(time_periods * principal_payments) / total_principal


def weighted_average_maturity_wam(weights, maturities):
    '''
    domain: ['Structured finance & securitization']
    subdomain: ['Pool Characteristics', 'MBS Analytics']
    function: "Weighted average maturity (WAM) is the average remaining maturity of a pool of loans, weighted by each loan's outstanding balance. It indicates how long the pool is expected to remain outstanding, before considering prepayments."
    y_as_x: []
    :param weights: "Array-like of loan balance weights w_i (should sum to 1, or will be normalized)"
    :param maturities: "Array-like of remaining maturity (in months or years) for each loan"
    :return: "Computed WAM = sum(w_i * maturity_i)"
    '''
    weights = np.asarray(weights)
    maturities = np.asarray(maturities)
    if np.sum(weights) != 1.0:
        weights = weights / np.sum(weights)
    return np.sum(weights * maturities)


def weighted_least_squares_wls(y, X, weights=None):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Regression Analysis', 'Heteroskedasticity']
    function: "Weighted Least Squares (WLS) is a regression method that accounts for heteroskedasticity by giving each observation a weight inversely proportional to its error variance. The estimator is beta_hat = (X'WX)^{-1} X'Wy, where W is the diagonal weight matrix."
    y_as_x: []
    :param y: "Array-like of dependent variable values"
    :param X: "2D array-like of independent variable values (with or without constant)"
    :param weights: "Array-like of weights for each observation (inversely proportional to variance)"
    :return: "Fitted WLS model results from statsmodels"
    '''
    import statsmodels.api as sm
    X = sm.add_constant(np.asarray(X))
    y = np.asarray(y)
    if weights is None:
        weights = np.ones(len(y))
    model = sm.WLS(y, X, weights=weights)
    return model.fit()


def weighted_moving_average_wma(close, period=10):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Moving Averages', 'Trend Following']
    function: "Weighted Moving Average (WMA) assigns linearly decreasing weights to older data points, with the most recent price receiving the highest weight. WMA = sum(w_i * P_{t-i}) / sum(w_i), where weights decrease linearly. It is more responsive to recent price changes than a simple moving average."
    y_as_x: []
    :param close: "Array-like or pd.Series of closing prices"
    :param period: "Lookback period for the WMA (default 10)"
    :return: "Array of WMA values"
    '''
    import talib
    close = np.asarray(close, dtype=np.float64)
    return talib.WMA(close, timeperiod=period)


def white_heteroskedasticity_test(y, X):
    '''
    domain: ['Econometrics & time-series finance']
    subdomain: ['Regression Diagnostics', 'Heteroskedasticity']
    function: "White's heteroskedasticity test checks for non-constant variance of regression residuals by regressing squared residuals on the original regressors, their squares, and cross-products. The test statistic LM = n*R^2 follows a chi-squared distribution under the null of homoskedasticity."
    y_as_x: []
    :param y: "Array-like of dependent variable values"
    :param X: "2D array-like of independent variable values"
    :return: "Dict with 'lm_statistic', 'p_value', 'f_statistic', 'f_p_value'"
    '''
    import statsmodels.api as sm
    from statsmodels.stats.diagnostic import het_white
    X = np.asarray(X)
    y = np.asarray(y)
    X_with_const = sm.add_constant(X)
    ols_result = sm.OLS(y, X_with_const).fit()
    white_test = het_white(ols_result.resid, X_with_const)
    return {
        'lm_statistic': white_test[0],
        'lm_p_value': white_test[1],
        'f_statistic': white_test[2],
        'f_p_value': white_test[3]
    }


def whole_life_annuity_due(x, interest_rate, life_table=None, omega=120, **params):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Life Annuities', 'Actuarial Present Values']
    function: "Whole life annuity-due a-double-dot_x is the expected present value of payments of 1 at the beginning of each year for as long as a person aged x survives. Computed as a-double-dot_x = sum_{k>=0} v^k * _kp_x."
    y_as_x: ['net_premium', 'net_premium_equivalence_principle', 'gross_premium_principle', 'prospective_reserve']
    :param x: "Current age of the annuitant"
    :param interest_rate: "Annual interest rate used for discounting"
    :param life_table: "Optional life table dict with ages as keys and l_x values"
    :param omega: "Maximum age (limiting age of the life table, default 120)"
    :param params: "Additional mortality parameters if no life table provided"
    :return: "Computed whole life annuity-due a-double-dot_x"
    '''
    v = 1 / (1 + interest_rate)
    annuity_value = 0.0
    max_years = omega - x
    for k in range(max_years):
        if life_table is not None:
            l_x = life_table.get(x, 0)
            l_x_k = life_table.get(x + k, 0)
            if l_x == 0:
                p_k = 0.0
            else:
                p_k = l_x_k / l_x
        else:
            p_k = survival_function(x, k, **params)
        annuity_value += (v ** k) * p_k
        if p_k < 1e-12:
            break
    return annuity_value


def whole_life_annuity_immediate(x, interest_rate, life_table=None, omega=120, **params):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Life Annuities', 'Actuarial Present Values']
    function: "Whole life annuity-immediate a_x is the expected present value of payments of 1 at the end of each year for as long as a person aged x survives. Computed as a_x = sum_{k>=1} v^k * _kp_x. It differs from the annuity-due by one period of discounting."
    y_as_x: ['net_premium', 'life_annuity_immediate']
    :param x: "Current age of the annuitant"
    :param interest_rate: "Annual interest rate used for discounting"
    :param life_table: "Optional life table dict with ages as keys and l_x values"
    :param omega: "Maximum age (limiting age of the life table, default 120)"
    :param params: "Additional mortality parameters if no life table provided"
    :return: "Computed whole life annuity-immediate a_x"
    '''
    v = 1 / (1 + interest_rate)
    annuity_value = 0.0
    max_years = omega - x
    for k in range(1, max_years):
        if life_table is not None:
            l_x = life_table.get(x, 0)
            l_x_k = life_table.get(x + k, 0)
            if l_x == 0:
                p_k = 0.0
            else:
                p_k = l_x_k / l_x
        else:
            p_k = survival_function(x, k, **params)
        annuity_value += (v ** k) * p_k
        if p_k < 1e-12:
            break
    return annuity_value


def whole_life_assurance(x, interest_rate, life_table=None, omega=120, **params):
    '''
    domain: ['Actuarial science & insurance']
    subdomain: ['Life Insurance', 'Actuarial Present Values']
    function: "Whole life assurance A_x is the actuarial present value of a benefit of 1 payable at the end of the year of death for a person currently aged x. Computed as A_x = sum_{k>=0} v^{k+1} * _kp_x * q_{x+k}. It represents the expected cost of providing a death benefit."
    y_as_x: ['net_premium', 'net_premium_equivalence_principle', 'prospective_reserve', 'variance_of_loss']
    :param x: "Current age of the insured"
    :param interest_rate: "Annual interest rate used for discounting"
    :param life_table: "Optional life table dict with ages as keys and l_x values"
    :param omega: "Maximum age (limiting age of the life table, default 120)"
    :param params: "Additional mortality parameters if no life table provided"
    :return: "Computed whole life assurance A_x"
    '''
    v = 1 / (1 + interest_rate)
    apv = 0.0
    max_years = omega - x
    for k in range(max_years):
        if life_table is not None:
            l_x = life_table.get(x, 0)
            l_x_k = life_table.get(x + k, 0)
            l_x_k1 = life_table.get(x + k + 1, 0)
            if l_x == 0:
                continue
            p_k = l_x_k / l_x
            q_xk = 1 - (l_x_k1 / l_x_k) if l_x_k > 0 else 1.0
        else:
            p_k = survival_function(x, k, **params)
            p_k1 = survival_function(x, k + 1, **params)
            q_xk = 1 - (p_k1 / p_k) if p_k > 0 else 1.0
        apv += (v ** (k + 1)) * p_k * q_xk
        if p_k < 1e-12:
            break
    return apv


def williams_pctr(high, low, close, period=14):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Momentum Indicators', 'Overbought/Oversold']
    function: "Williams %R is a momentum indicator measuring the level of the close relative to the highest high over a lookback period. It oscillates between 0 and -100: %R = -100 * (H_n - C) / (H_n - L_n). Values near 0 indicate overbought, near -100 indicate oversold conditions."
    y_as_x: []
    :param high: "Array-like or pd.Series of high prices"
    :param low: "Array-like or pd.Series of low prices"
    :param close: "Array-like or pd.Series of closing prices"
    :param period: "Lookback period (default 14)"
    :return: "Array of Williams %R values"
    '''
    import talib
    high = np.asarray(high, dtype=np.float64)
    low = np.asarray(low, dtype=np.float64)
    close = np.asarray(close, dtype=np.float64)
    return talib.WILLR(high, low, close, timeperiod=period)


def win_over_loss_ratio(returns):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Return Analysis', 'Win/Loss Statistics']
    function: "Win/loss ratio compares the average magnitude of positive returns to the average magnitude of negative returns. A ratio above 1 means the average winning trade is larger than the average losing trade. Combined with the hit ratio, it provides insight into the strategy's return profile."
    y_as_x: []
    :param returns: "Array-like or pd.Series of portfolio returns"
    :return: "Computed win/loss ratio = avg positive return / |avg negative return|"
    '''
    returns = np.asarray(returns)
    pos_returns = returns[returns > 0]
    neg_returns = returns[returns < 0]
    if len(neg_returns) == 0 or np.mean(neg_returns) == 0:
        return np.inf
    return np.mean(pos_returns) / abs(np.mean(neg_returns))


def working_capital(current_assets, current_liabilities):
    '''
    domain: ['Accounting & financial statement analysis']
    subdomain: ['Liquidity Analysis', 'Balance Sheet Analysis']
    function: "Working capital is the difference between current assets and current liabilities. It measures a company's short-term liquidity and its ability to meet near-term obligations. Positive working capital indicates sufficient short-term assets; negative working capital may signal liquidity risk."
    y_as_x: ['current_ratio', 'quick_ratio', 'altman_z_score']
    :param current_assets: "Total current assets (cash, receivables, inventory, etc.)"
    :param current_liabilities: "Total current liabilities (payables, short-term debt, etc.)"
    :return: "Computed working capital = Current Assets - Current Liabilities"
    '''
    return current_assets - current_liabilities


def wrong_way_risk_adjustment(epe_base, correlation_pd_exposure, adjustment_factor=1.4):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Counterparty Credit Risk', 'Wrong-Way Risk']
    function: "Wrong-way risk adjustment accounts for the positive dependence between counterparty exposure and probability of default. When exposure increases as the counterparty's creditworthiness deteriorates, EPE_WWR > EPE. The adjustment typically applies a multiplier to the base EPE."
    y_as_x: []
    :param epe_base: "Base expected positive exposure (EPE) without wrong-way risk"
    :param correlation_pd_exposure: "Estimated correlation between PD and exposure (0 to 1)"
    :param adjustment_factor: "Multiplier for the wrong-way risk adjustment (default 1.4 per regulatory guidance)"
    :return: "Adjusted EPE_WWR incorporating wrong-way risk"
    '''
    alpha = 1 + correlation_pd_exposure * (adjustment_factor - 1)
    return epe_base * alpha


def yang_zhang_volatility(open_prices, high, low, close, window=20):
    '''
    domain: ['Market risk & volatility modeling']
    subdomain: ['Historical Volatility', 'Range-Based Estimators']
    function: "Yang-Zhang volatility is a range-based volatility estimator that combines overnight (close-to-open), open-to-close, and Rogers-Satchell components: sigma_YZ^2 = sigma_o^2 + k*sigma_c^2 + (1-k)*sigma_RS^2. It is minimum-variance and unbiased, handling overnight jumps."
    y_as_x: []
    :param open_prices: "Array-like of opening prices"
    :param high: "Array-like of high prices"
    :param low: "Array-like of low prices"
    :param close: "Array-like of closing prices"
    :param window: "Rolling window size (default 20)"
    :return: "Annualized Yang-Zhang volatility estimate"
    '''
    open_prices = np.asarray(open_prices, dtype=float)
    high = np.asarray(high, dtype=float)
    low = np.asarray(low, dtype=float)
    close = np.asarray(close, dtype=float)

    n = len(close)
    if n < window + 1:
        return np.nan

    # Use last `window` periods
    o = open_prices[-window:]
    h = high[-window:]
    l = low[-window:]
    c = close[-window:]
    c_prev = close[-(window + 1):-1]

    # Overnight returns (close-to-open)
    log_oc = np.log(o / c_prev)
    # Open-to-close returns
    log_co = np.log(c / o)

    # Overnight variance
    sigma_o_sq = np.var(log_oc, ddof=1)
    # Close-to-close variance
    sigma_c_sq = np.var(log_co, ddof=1)

    # Rogers-Satchell variance
    rs = (np.log(h / o) * np.log(h / c) + np.log(l / o) * np.log(l / c))
    sigma_rs_sq = np.mean(rs)

    k = 0.34 / (1.34 + (window + 1) / (window - 1))
    sigma_yz_sq = sigma_o_sq + k * sigma_c_sq + (1 - k) * sigma_rs_sq

    return np.sqrt(sigma_yz_sq * 252)


def yield_curve_carry(coupon_income, roll_down, financing_cost):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Fixed Income Strategy', 'Carry and Roll']
    function: "Yield curve carry is the expected return from holding a bond, decomposed into coupon income, roll-down return (benefit of the yield curve slope as the bond ages), and financing cost. Total carry = Coupon + Roll-down + Financing (where financing is typically negative)."
    y_as_x: ['bond_carry_and_roll']
    :param coupon_income: "Coupon income earned over the holding period"
    :param roll_down: "Roll-down return from the yield curve slope"
    :param financing_cost: "Cost of financing the bond position (typically negative)"
    :return: "Computed yield curve carry = Coupon + Roll-down + Financing"
    '''
    return coupon_income + roll_down + financing_cost


def yield_to_call_ytc(face_value, coupon_rate, call_price, call_date_years, current_price, frequency=2):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Bond Valuation', 'Yield Measures']
    function: "Yield to call (YTC) is the internal rate of return assuming the bond is called (redeemed by the issuer) at the call price on the call date. It solves: P = sum_t C/(1+y)^t + CallPrice/(1+y)^T_call."
    y_as_x: ['yield_to_worst_ytw']
    :param face_value: "Face (par) value of the bond"
    :param coupon_rate: "Annual coupon rate"
    :param call_price: "Price at which the issuer can call the bond"
    :param call_date_years: "Time to the call date in years"
    :param current_price: "Current market price of the bond"
    :param frequency: "Coupon payment frequency per year (default 2 for semiannual)"
    :return: "Computed yield to call (annualized)"
    '''
    from scipy.optimize import brentq
    coupon = face_value * coupon_rate / frequency
    n_periods = int(call_date_years * frequency)

    def price_diff(y_per_period):
        pv = sum(coupon / (1 + y_per_period) ** t for t in range(1, n_periods + 1))
        pv += call_price / (1 + y_per_period) ** n_periods
        return pv - current_price

    try:
        y_per_period = brentq(price_diff, -0.5, 5.0)
        return y_per_period * frequency
    except ValueError:
        return np.nan


def yield_to_maturity_ytm(face_value, coupon_rate, maturity_years, current_price, frequency=2):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Bond Valuation', 'Yield Measures']
    function: "Yield to maturity (YTM) is the internal rate of return earned by holding a bond to maturity, assuming all coupons are reinvested at the same rate. It solves: P = sum_t C/(1+YTM/m)^(mt) + F/(1+YTM/m)^(mT)."
    y_as_x: ['yield_to_worst_ytw', 'modified_duration', 'macaulay_duration', 'bond_price_from_yield', 'credit_spread', 'z_spread', 'break_even_inflation']
    :param face_value: "Face (par) value of the bond (F)"
    :param coupon_rate: "Annual coupon rate"
    :param maturity_years: "Time to maturity in years (T)"
    :param current_price: "Current market price of the bond (P)"
    :param frequency: "Coupon payment frequency per year (default 2 for semiannual)"
    :return: "Computed yield to maturity (annualized)"
    '''
    from scipy.optimize import brentq
    coupon = face_value * coupon_rate / frequency
    n_periods = int(maturity_years * frequency)

    def price_diff(y_per_period):
        pv = sum(coupon / (1 + y_per_period) ** t for t in range(1, n_periods + 1))
        pv += face_value / (1 + y_per_period) ** n_periods
        return pv - current_price

    try:
        y_per_period = brentq(price_diff, -0.5, 5.0)
        return y_per_period * frequency
    except ValueError:
        return np.nan


def yield_to_worst_ytw(yield_to_maturity_ytm, yield_to_call_values=None):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Bond Valuation', 'Yield Measures']
    function: "Yield to worst (YTW) is the minimum yield an investor could receive on a callable bond, considering all possible call dates and maturity. It is the lowest of YTM, YTC at each call date, and any other redemption yields: YTW = min(YTM, YTC_1, YTC_2, ...)."
    y_as_x: []
    :param yield_to_maturity_ytm: "Yield to maturity of the bond"
    :param yield_to_call_values: "Optional list/array of yield-to-call values at each call date"
    :return: "Computed yield to worst = min(YTM, all YTC values)"
    '''
    all_yields = [yield_to_maturity_ytm]
    if yield_to_call_values is not None:
        all_yields.extend(np.asarray(yield_to_call_values).tolist())
    # Filter out NaN
    valid_yields = [y for y in all_yields if not np.isnan(y)]
    if not valid_yields:
        return np.nan
    return min(valid_yields)


def zero_coupon_bond_price(face_value, rate, T, compounding='discrete', frequency=1):
    '''
    domain: ['Fixed income, bonds & credit markets']
    subdomain: ['Bond Pricing', 'Discount Securities']
    function: "Zero-coupon bond price is the present value of the face value discounted at the appropriate rate. Under discrete compounding: P = F / (1+r/m)^(mT). Under continuous compounding: P = F * exp(-r*T). Zero-coupon bonds are fundamental building blocks for yield curve construction."
    y_as_x: ['discount_factor', 'spot_rate_from_discount_factor', 'spot_rate_bootstrapping']
    :param face_value: "Face (par) value of the bond (F)"
    :param rate: "Discount rate or yield (r)"
    :param T: "Time to maturity in years"
    :param compounding: "'discrete' or 'continuous' (default 'discrete')"
    :param frequency: "Compounding frequency per year for discrete compounding (default 1)"
    :return: "Computed zero-coupon bond price P = F / (1+r)^T"
    '''
    if compounding == 'continuous':
        return face_value * np.exp(-rate * T)
    else:
        return face_value / (1 + rate / frequency) ** (frequency * T)


def z_spread(cash_flows, time_periods, spot_rates, market_price, initial_guess=0.01):
    '''
    domain: ['Credit risk, default modeling & credit portfolio']
    subdomain: ['Credit Spreads', 'Bond Relative Value']
    function: "Z-spread (zero-volatility spread) is the constant spread added to each spot rate on the Treasury yield curve that makes the present value of a bond's cash flows equal to its market price. It solves: P = sum_t CF_t * exp(-(r_t + z) * t)."
    y_as_x: ['option_adjusted_spread_oas']
    :param cash_flows: "Array of the bond's cash flows (coupons and principal)"
    :param time_periods: "Array of time periods (in years) for each cash flow"
    :param spot_rates: "Array of Treasury spot rates corresponding to each cash flow date"
    :param market_price: "Current market price of the bond"
    :param initial_guess: "Initial guess for the z-spread (default 0.01)"
    :return: "Computed Z-spread in decimal form"
    '''
    from scipy.optimize import brentq
    cash_flows = np.asarray(cash_flows)
    time_periods = np.asarray(time_periods)
    spot_rates = np.asarray(spot_rates)

    def pv_diff(z):
        pv = np.sum(cash_flows * np.exp(-(spot_rates + z) * time_periods))
        return pv - market_price

    try:
        return brentq(pv_diff, -0.5, 5.0)
    except ValueError:
        from scipy.optimize import minimize_scalar
        result = minimize_scalar(lambda z: abs(pv_diff(z)), bounds=(-0.5, 5.0), method='bounded')
        return result.x
