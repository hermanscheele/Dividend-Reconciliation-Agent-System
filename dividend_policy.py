POLICY_TEXT = """ 
NBIM Dividend Processing Policy (Simplified Dev Version)

1) Withholding Tax
- Default: Apply treaty WHT rate where eligible.
- If no treaty rate is known, apply statutory domestic WHT rate.
- Expected accuracy: +/- 0.5 percentage points tolerance due to rounding rules.
- Local surtaxes must be included when applicable.

Examples:
- Switzerland dividends: expected treaty WHT = 15% (if eligible).
- South Korea dividends: WHT ≈ 22% (includes local surtax).

2) FX Conversion
- FX rate source hierarchy (highest priority first):
  1. NBIM Treasury feed official closing rate
  2. WM/Refinitiv closing rate
  3. ECB official daily rate
- FX must be taken as-of payment date.
- Tolerance: +/- 0.20% deviation allowed due to timing/time-zone effects.

3) Key Dates
- Ex-date, record date, payment date must match custodian unless:
  - Market holiday → use next business day
  - ADR program date differs → ADR calendar rules apply
- Tolerance: +/- 1 business day outside holiday scenarios.

4) Corporate Action Type
- Cash dividends follow standard rules.
- ADR programs may adjust event dates and FX timing.

5) Net Amount Calculation
NBIM Net = Gross − Withholding Tax − Local Tax (if applicable)

6) Exceptions
- If policy data unavailable, mark as "uncertain" and request treaty reference or FX source.
- Manual override allowed only with supporting documentation.

End of simplified policy.
"""