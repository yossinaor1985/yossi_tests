"""
Financial Functions - Batch 5 (Equations 408-509)
"""
import numpy as np
import pandas as pd
from scipy import stats


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
    y_as_x: []
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
    y_as_x: []
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
    y_as_x: ['lifetime_ecl', 'expected_loss', 'lgd_downturn_adjustment', 'credit_var']
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
    y_as_x: ['calmar_ratio', 'sterling_ratio', 'pain_index']
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
    y_as_x: ['bid_ask_spread', 'quoted_spread_pct', 'effective_spread']
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


def minus_directional_indicator_di(high, low, close, period=14):
    '''
    domain: ['Technical analysis & chart-based indicators']
    subdomain: ['Directional movement']
    function: "Minus directional indicator (-DI): smoothed -DM divided by ATR times 100"
    y_as_x: ['adx', 'average_directional_index_adx']
    :param high: "High price series"
    :param low: "Low price series"
    :param close: "Close price series"
    :param period: "Smoothing period (default 14)"
    :return: "-DI series"
    '''
    high = pd.Series(high, dtype=float)
    low = pd.Series(low, dtype=float)
    close = pd.Series(close, dtype=float)

    # Directional movement
    up_move = high.diff()
    down_move = -low.diff()
    minus_dm = pd.Series(np.where((down_move > up_move) & (down_move > 0), down_move, 0.0), index=high.index)

    # True range
    tr = pd.concat([
        high - low,
        (high - close.shift(1)).abs(),
        (low - close.shift(1)).abs()
    ], axis=1).max(axis=1)

    atr = tr.rolling(window=period).sum()
    smoothed_minus_dm = minus_dm.rolling(window=period).sum()

    return 100.0 * smoothed_minus_dm / atr


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
