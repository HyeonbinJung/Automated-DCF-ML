def fcff_from_forecast(
    revenue_prev,
    revenue_growth,
    ebit_margin,
    tax_rate,
    da_ratio,
    capex_ratio,
    nwc_ratio,
    nwc_prev,
):
    revenue = revenue_prev * (1 + revenue_growth)
    ebit = revenue * ebit_margin
    nopat = ebit * (1 - tax_rate)
    da = revenue * da_ratio
    capex = revenue * capex_ratio
    nwc = revenue * nwc_ratio
    delta_nwc = nwc - nwc_prev
    fcff = nopat + da - capex - delta_nwc

    return {
        "revenue": revenue,
        "ebit": ebit,
        "nopat": nopat,
        "da": da,
        "capex": capex,
        "nwc": nwc,
        "delta_nwc": delta_nwc,
        "fcff": fcff,
    }

def dcf_value(fcff_list, wacc, terminal_growth, cash, debt, diluted_shares):
    pv_fcff = sum(
        fcff / ((1 + wacc) ** i)
        for i, fcff in enumerate(fcff_list, start=1)
    )
    terminal = fcff_list[-1] * (1 + terminal_growth) / (wacc - terminal_growth)
    pv_terminal = terminal / ((1 + wacc) ** len(fcff_list))
    enterprise_value = pv_fcff + pv_terminal
    equity_value = enterprise_value + cash - debt
    fair_value_per_share = equity_value / diluted_shares

    return {
        "pv_fcff": pv_fcff,
        "terminal_value": terminal,
        "pv_terminal": pv_terminal,
        "enterprise_value": enterprise_value,
        "equity_value": equity_value,
        "fair_value_per_share": fair_value_per_share,
    }
