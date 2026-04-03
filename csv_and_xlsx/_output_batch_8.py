"""
Financial Functions - Batch 8 (Equations 714-813)
"""
import numpy as np
import pandas as pd
from scipy import stats


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
    y_as_x: ['option_delta_hedged_pandl']
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


def weighted_average_cost_of_capital_wacc(equity_value, debt_value, cost_of_equity, cost_of_debt, tax_rate):
    '''
    domain: ['Corporate finance & capital budgeting']
    subdomain: ['Cost of Capital', 'Valuation']
    function: "WACC (Weighted Average Cost of Capital) is the blended cost of a firm's capital, weighing the cost of equity and after-tax cost of debt by their respective proportions in the capital structure. WACC = (E/V)*R_e + (D/V)*R_d*(1-T), where V = E + D."
    y_as_x: ['terminal_value_gordon_growth', 'fcff_dcf_intrinsic_value', 'economic_value_added_eva', 'net_present_value_npv']
    :param equity_value: "Market value of equity (E)"
    :param debt_value: "Market value of debt (D)"
    :param cost_of_equity: "Cost of equity capital (R_e)"
    :param cost_of_debt: "Cost of debt capital before tax (R_d)"
    :param tax_rate: "Corporate marginal tax rate (T)"
    :return: "Computed WACC = (E/V)*R_e + (D/V)*R_d*(1-T)"
    '''
    total_value = equity_value + debt_value
    return (equity_value / total_value) * cost_of_equity + (debt_value / total_value) * cost_of_debt * (1 - tax_rate)


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
