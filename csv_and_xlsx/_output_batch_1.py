"""
Financial Functions - Batch 1 (Equations 0-101)
Auto-generated Python implementations of financial, actuarial, and technical analysis equations.
"""
import numpy as np
import pandas as pd
from scipy import stats


def abnormal_earnings_growth(eps_next, required_return, abnormal_growth_pv):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Equity Valuation', 'Earnings-Based Valuation']
    function: "Computes the intrinsic stock price using the Ohlson-Juettner model: capitalized next-period earnings plus the present value of abnormal earnings growth."
    y_as_x: []
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


def absolute_ppp(domestic_price_level, foreign_price_level):
    '''
    domain: ['FX & international finance']
    subdomain: ['Purchasing Power Parity', 'Exchange Rate Theory']
    function: "Computes the equilibrium exchange rate under Absolute Purchasing Power Parity, where the exchange rate equals the ratio of domestic to foreign price levels."
    y_as_x: ['purchasing_power_parity_ppp']
    :param domestic_price_level: "Aggregate price level in the domestic economy (P)"
    :param foreign_price_level: "Aggregate price level in the foreign economy (P*)"
    :return: "Equilibrium spot exchange rate S = P / P*"
    '''
    return domestic_price_level / foreign_price_level


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
    y_as_x: ['average_directional_index_adx']
    :param high: "Array of high prices"
    :param low: "Array of low prices"
    :param close: "Array of closing prices"
    :param timeperiod: "Lookback period for the ADX calculation (default 14)"
    :return: "ADX values as a numpy array"
    '''
    try:
        import talib
        return talib.ADX(high, low, close, timeperiod=timeperiod)
    except ImportError:
        high = np.asarray(high, dtype=float)
        low = np.asarray(low, dtype=float)
        close = np.asarray(close, dtype=float)
        n = len(close)
        tr = np.zeros(n)
        plus_dm = np.zeros(n)
        minus_dm = np.zeros(n)
        for i in range(1, n):
            hl = high[i] - low[i]
            hc = abs(high[i] - close[i - 1])
            lc = abs(low[i] - close[i - 1])
            tr[i] = max(hl, hc, lc)
            up_move = high[i] - high[i - 1]
            down_move = low[i - 1] - low[i]
            plus_dm[i] = up_move if (up_move > down_move and up_move > 0) else 0.0
            minus_dm[i] = down_move if (down_move > up_move and down_move > 0) else 0.0
        atr = np.zeros(n)
        smoothed_plus = np.zeros(n)
        smoothed_minus = np.zeros(n)
        atr[timeperiod] = np.sum(tr[1:timeperiod + 1])
        smoothed_plus[timeperiod] = np.sum(plus_dm[1:timeperiod + 1])
        smoothed_minus[timeperiod] = np.sum(minus_dm[1:timeperiod + 1])
        for i in range(timeperiod + 1, n):
            atr[i] = atr[i - 1] - atr[i - 1] / timeperiod + tr[i]
            smoothed_plus[i] = smoothed_plus[i - 1] - smoothed_plus[i - 1] / timeperiod + plus_dm[i]
            smoothed_minus[i] = smoothed_minus[i - 1] - smoothed_minus[i - 1] / timeperiod + minus_dm[i]
        plus_di = 100.0 * smoothed_plus / np.where(atr != 0, atr, 1.0)
        minus_di = 100.0 * smoothed_minus / np.where(atr != 0, atr, 1.0)
        di_sum = plus_di + minus_di
        dx = 100.0 * np.abs(plus_di - minus_di) / np.where(di_sum != 0, di_sum, 1.0)
        adx_arr = np.full(n, np.nan)
        start = 2 * timeperiod
        if start < n:
            adx_arr[start] = np.mean(dx[timeperiod:start + 1])
            for i in range(start + 1, n):
                adx_arr[i] = (adx_arr[i - 1] * (timeperiod - 1) + dx[i]) / timeperiod
        return adx_arr


def affine_term_structure_bond_price(a_coeff, b_coeff, state_vector):
    '''
    domain: ['Interest-rate modeling & term structures']
    subdomain: ['Term Structure Models', 'Affine Models']
    function: "Computes the zero-coupon bond price under an affine term structure model: P(t,T) = exp(A(t,T) + B(t,T)' X_t)."
    y_as_x: []
    :param a_coeff: "Scalar A(t,T) coefficient from the affine model solution"
    :param b_coeff: "Vector B(t,T) of factor loadings from the affine model"
    :param state_vector: "Vector X_t of state variables (e.g., short rate factors)"
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
    subdomain: ['Loss Modeling', 'Aggregate Risk']
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


def allocation_effect_brinson_fachler(portfolio_weights, benchmark_weights, benchmark_sector_returns, benchmark_total_return):
    '''
    domain: ['Performance measurement & attribution']
    subdomain: ['Performance Attribution', 'Brinson Model']
    function: "Computes the allocation effect for each sector under the Brinson-Fachler attribution model: Allocation_i = (w_i^P - w_i^B)(r_i^B - r^B)."
    y_as_x: []
    :param portfolio_weights: "Array of portfolio sector weights"
    :param benchmark_weights: "Array of benchmark sector weights"
    :param benchmark_sector_returns: "Array of benchmark returns for each sector"
    :param benchmark_total_return: "Total benchmark return"
    :return: "Array of allocation effects per sector"
    '''
    pw = np.asarray(portfolio_weights, dtype=float)
    bw = np.asarray(benchmark_weights, dtype=float)
    br = np.asarray(benchmark_sector_returns, dtype=float)
    return (pw - bw) * (br - benchmark_total_return)


def alpha(returns, factor_returns, risk_free_rate=0.0):
    '''
    domain: ['Equity valuation & asset pricing']
    subdomain: ['Asset Pricing', 'CAPM']
    function: "Computes Jensen's alpha: the excess return of an asset beyond what is predicted by the CAPM. alpha = E[R_i] - [R_f + beta_i(E[R_m]-R_f)]."
    y_as_x: ['appraisal_ratio', 'alpha_from_regression', 'treynor_ratio']
    :param returns: "Array of asset returns"
    :param factor_returns: "Array of market (benchmark) returns"
    :param risk_free_rate: "Risk-free rate per period (default 0)"
    :return: "Annualized Jensen's alpha"
    '''
    try:
        import empyrical
        return empyrical.alpha(returns, factor_returns, risk_free=risk_free_rate)
    except ImportError:
        returns = np.asarray(returns, dtype=float)
        factor_returns = np.asarray(factor_returns, dtype=float)
        excess_r = returns - risk_free_rate
        excess_m = factor_returns - risk_free_rate
        b = np.cov(excess_r, excess_m)[0, 1] / np.var(excess_m, ddof=1)
        alpha_val = np.mean(excess_r) - b * np.mean(excess_m)
        return alpha_val * 252


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


def american_option_binomial_pricing(spot, strike, rate, volatility, time_to_maturity, steps=100, option_type='call', dividend_yield=0.0):
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
        return {'conditional_power_vol': sigma_delta, 'params': {'omega': omega, 'alpha': alpha_coeff, 'gamma': gamma, 'delta': delta, 'beta': beta_coeff}}


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
    return {'constant': model.params[0] if constant else 0.0, 'phi': model.params[-1], 'residuals': model.resid, 'model': model}


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
    return {'constant': model.params[0] if constant else 0.0, 'phi': model.params[-1], 'residuals': model.resid, 'model': model}


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


def asian_option_price(spot, strike, rate, volatility, time_to_maturity, n_averaging=12, option_type='call', dividend_yield=0.0, n_simulations=50000, seed=42):
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


def average_directional_index_adx(high, low, close, timeperiod=14):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Trend Indicators', 'Directional Movement']
    function: "Computes the Average Directional Index (ADX) using TA-Lib. Measures trend strength."
    y_as_x: []
    :param high: "Array of high prices"
    :param low: "Array of low prices"
    :param close: "Array of closing prices"
    :param timeperiod: "Lookback period (default 14)"
    :return: "ADX values as numpy array"
    '''
    return adx(high, low, close, timeperiod=timeperiod)


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


def barrier_option_price(spot, strike, barrier, rate, volatility, time_to_maturity, option_type='call', barrier_type='down-and-out', dividend_yield=0.0, n_simulations=50000, seed=42):
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
    y_as_x: ['alpha', 'capm_expected_return', 'levered_beta_hamada', 'unlevered_beta', 'security_market_line', 'treynor_ratio']
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


def binomial_option_pricing(spot, strike, rate, volatility, time_to_maturity, steps=100, option_type='call', dividend_yield=0.0):
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
    y_as_x: ['accrued_interest', 'dirty_price', 'clean_price', 'bond_price_from_yield', 'yield_to_maturity_ytm', 'modified_duration', 'convexity', 'macaulay_duration']
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
