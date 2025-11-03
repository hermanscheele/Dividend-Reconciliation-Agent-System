
POLICY_TEXT = """
═══════════════════════════════════════════════════════════════════════════════
NBIM DIVIDEND PROCESSING POLICY
Version 2.1 | Effective Date: 2025-01-01
═══════════════════════════════════════════════════════════════════════════════

SECTION 1: WITHHOLDING TAX POLICY

1.1 Treaty Rate Application
- PRIMARY RULE: Always apply bilateral tax treaty rate when Norway has a Double Taxation Treaty (DTT) with the source country
- Treaty rates take precedence over statutory domestic rates
- Valid tax residency certificate must be on file with custodian
- If treaty relief cannot be obtained at source, standard rate applies with subsequent reclaim

1.2 Country-Specific Tax Treatment

SOUTH KOREA (Article 10 - Norway-Korea Tax Treaty 2004):
- Treaty rate: 15% on dividends to institutional investors
- Statutory rate: 22% (15% national tax + 7% local income tax)
- POLICY: NBIM must apply 15% treaty rate when approved status documented
- Custodian must withhold at treaty rate if NBIM provides valid certificate
- VIOLATION: Any withholding above 15% when treaty status is valid

SWITZERLAND (Article 10 - Norway-Switzerland Tax Treaty 1987):
- Treaty rate: 15% on dividends to institutional investors  
- Statutory rate: 35% (Swiss federal withholding tax)
- POLICY: NBIM applies 15% for calculation; 35% withheld at source with 20% reclaim
- Quick refund procedure available for eligible institutions
- VIOLATION: Failure to calculate at 15% treaty rate for NBIM books

UNITED STATES (Article 10 - Norway-US Tax Treaty 1971):
- Treaty rate: 15% on dividends
- Statutory rate: 30% for non-residents
- POLICY: W-8BEN-E form must be on file; apply 15% rate
- VIOLATION: 30% withholding indicates missing treaty documentation

1.3 Tolerance and Rounding
- Acceptable variance: ±0.5% due to rounding and calculation methodology
- Material deviation: >1% difference requires investigation
- Local taxes and surtaxes must be included in total withholding calculation

═══════════════════════════════════════════════════════════════════════════════
SECTION 2: POSITION DATA INTEGRITY

2.1 Nominal Basis Requirements
- NBIM position data must reconcile to custodian holdings on record date
- Zero tolerance for position mismatches on dividend events
- POLICY: Any nominal basis discrepancy is a CRITICAL violation requiring immediate correction
- Root cause: System sync errors, failed trades not properly recorded, or manual entry mistakes

2.2 Position Reconciliation Timing
- Daily reconciliation required for all holdings
- T+2 settlement positions must be reflected by record date
- Corporate actions (splits, mergers) must update positions before ex-date

2.3 Violation Consequences
- Position mismatch = incorrect dividend entitlement = financial loss
- MANDATORY: Daily position break resolution before market close

═══════════════════════════════════════════════════════════════════════════════
SECTION 3: FOREIGN EXCHANGE POLICY

3.1 FX Rate Source Hierarchy (in order of priority):
1. NBIM Treasury official closing rate (Bloomberg NBIM composite)
2. WM/Reuters 4pm London Fix
3. ECB Daily Reference Rate
4. Central Bank of source country official rate

3.2 FX Rate Timing
- Rate must be captured as of PAYMENT DATE (not ex-date or record date)
- For non-standard settlement: use actual cash receipt date
- Cross-currency transactions: document FX rate source and timestamp

3.3 Tolerance Bands
- Normal variance: ±0.20% acceptable due to timing/feed differences
- Material variance: >0.50% requires investigation and documentation
- Market disruption (>2% move on payment date): escalate to Treasury

═══════════════════════════════════════════════════════════════════════════════
SECTION 4: DIVIDEND PAYMENT DATES

4.1 Standard Settlement Rules
- Payment date must match custodian notification unless:
  a) Source market holiday → next business day per market convention
  b) Custodian processing delay → documented in custodian SLA
  c) ADR programs → may differ from underlying security schedule

4.2 Date Tolerance
- Acceptable variance: ±1 business day for operational timing
- Material variance: >3 business days indicates custodian error or communication breakdown
- POLICY: Payment date differences >5 business days require escalation

4.3 South Korea Specific
- Typical payment timing: 30-60 days after ex-date (longer than most markets)
- Extended timeline is normal market practice
- VIOLATION: Only if payment date contradicts official company announcement

4.4 Switzerland Specific  
- Typical payment timing: 2-4 days after ex-date (very short cycle)
- Swiss francs settle T+2 
- VIOLATION: Payment date >7 days after ex-date without documented reason

═══════════════════════════════════════════════════════════════════════════════
SECTION 5: AMOUNT CALCULATION METHODOLOGY

5.1 Standard Dividend Calculation
Gross Amount = Dividend Per Share × Nominal Basis (shares held on record date)
Withholding Tax = Gross Amount × Applicable WHT Rate
Net Amount = Gross Amount − Withholding Tax − Other Deductions

5.2 Calculation Tolerance
- Rounding: Amounts may differ by up to 0.01 due to decimal precision
- Material threshold: >0.10% variance indicates calculation error
- Currency precision: Minimum 2 decimal places for all currencies

5.3 Cross-Validation Requirements
- Net amount must mathematically derive from gross and tax
- If Net amount breaks but Tax is correct → investigate gross amount or FX
- If Net and Tax both break → likely upstream position or rate issue

═══════════════════════════════════════════════════════════════════════════════
SECTION 6: CUSTODIAN DATA QUALITY STANDARDS

6.1 Data Accuracy Requirements
- Custodian must provide accurate ISIN, dates, rates, and amounts
- NBIM reserves right to reject custodian data that contradicts market sources
- Custodian errors must be corrected within 2 business days of notification

6.2 Escalation Procedures
- Tax rate errors: Escalate to custodian tax team + NBIM tax compliance
- Amount errors: Escalate to custodian operations + NBIM reconciliation
- Position errors: Escalate to custodian relationship manager + NBIM portfolio ops

6.3 Service Level Agreements (SLA)
- Custodian response time: 24 hours for acknowledgment
- Custodian correction time: 48 hours for data corrections
- NBIM internal correction: Same business day for critical breaks

═══════════════════════════════════════════════════════════════════════════════
SECTION 7: DOCUMENTATION AND COMPLIANCE

7.1 Required Documentation
- Tax treaty certificates: Must be current and on file before payment date
- Withholding tax forms: W-8BEN-E (US), Certificate of Residence (EU), etc.
- Custodian agreements: Must specify data quality standards and SLAs

7.2 Audit Trail Requirements
- All policy deviations must be documented with reason code
- Manual overrides require approval from supervisor + compliance review
- Policy violations must be logged in break management system

7.3 Reporting
- Daily break report: All breaks >$10K or >0.10% 
- Weekly summary: Break trends and custodian performance
- Monthly review: Policy violations and corrective actions

═══════════════════════════════════════════════════════════════════════════════
SECTION 8: POLICY VIOLATION DEFINITIONS

8.1 Critical Violations (Immediate Action Required)
- Position mismatch causing incorrect dividend calculation
- Treaty rate not applied when valid documentation exists
- Payment date >10 business days from market standard without explanation

8.2 Material Violations (Resolve Within 2 Business Days)
- Tax rate variance >1% from policy
- Amount variance >$50K or >1% of expected value
- Missing FX documentation for cross-currency events

8.3 Minor Variances (Acceptable Within Tolerance)
- Tax rate difference ≤0.5%
- Amount difference ≤0.10%
- Date difference ≤1 business day

═══════════════════════════════════════════════════════════════════════════════
SECTION 9: EXCEPTION HANDLING

9.1 When Policy Does Not Apply
- New markets without established treaty
- Special corporate actions (mergers, spin-offs, returns of capital)
- Market disruptions or regulatory changes

9.2 Uncertain Cases
- If policy is unclear: Mark as "uncertain" and escalate to compliance
- If data is missing: Request required documentation before processing
- If systems conflict: Prioritize most recent official source

9.3 Override Authority
- Tax treatment overrides: Tax Compliance Officer only
- Position overrides: Portfolio Operations Manager only
- Amount overrides: Reconciliation Team Lead with documentation

═══════════════════════════════════════════════════════════════════════════════
END OF POLICY DOCUMENT
═══════════════════════════════════════════════════════════════════════════════
"""