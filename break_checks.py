import pandas as pd


def detect_breaks(nbim_file, custody_file, tolerance=0.01):
    """
    Detect breaks between custody and NBIM CSV files.
    
    Returns: dict with breaks
    """
    
    # Load files
    custody = pd.read_csv(custody_file, delimiter=';', encoding='utf-8-sig')
    nbim = pd.read_csv(nbim_file, delimiter=';', encoding='utf-8-sig')
    
    # Create keys
    custody['key'] = custody['COAC_EVENT_KEY'].astype(str) + '_' + custody['CUSTODY'].astype(str)
    nbim['key'] = nbim['COAC_EVENT_KEY'].astype(str) + '_' + nbim['BANK_ACCOUNT'].astype(str)
    
    # Merge
    merged = custody.merge(nbim, on='key', how='outer', indicator=True, suffixes=('_c', '_n'))
    
    breaks = []
    
    # Missing records
    for _, row in merged[merged['_merge'] == 'left_only'].iterrows():
        breaks.append({
            'type': 'MISSING_IN_NBIM',
            'event': row['COAC_EVENT_KEY_c'],
            'account': row['CUSTODY'],
            'isin': row['ISIN_c'],
            'custody_amount': row['GROSS_AMOUNT'],
            'nbim_amount': None
        })
    
    for _, row in merged[merged['_merge'] == 'right_only'].iterrows():
        breaks.append({
            'type': 'MISSING_IN_CUSTODY',
            'event': row['COAC_EVENT_KEY_n'],
            'account': row['BANK_ACCOUNT'],
            'isin': row['ISIN_n'],
            'custody_amount': None,
            'nbim_amount': row['GROSS_AMOUNT_QUOTATION']
        })
    
    # Check matched records
    matched = merged[merged['_merge'] == 'both']
    
    for _, row in matched.iterrows():
        event = row['COAC_EVENT_KEY_c']
        account = row['CUSTODY']
        isin = row['ISIN_c']
        
        # ISIN mismatch
        if row['ISIN_c'] != row['ISIN_n']:
            breaks.append({
                'type': 'ISIN_MISMATCH',
                'event': event,
                'account': account,
                'isin': isin,
                'custody_value': row['ISIN_c'],
                'nbim_value': row['ISIN_n']
            })
        
        # Nominal basis
        if row['NOMINAL_BASIS_c'] != row['NOMINAL_BASIS_n']:
            breaks.append({
                'type': 'NOMINAL_MISMATCH',
                'event': event,
                'account': account,
                'isin': isin,
                'custody_value': row['NOMINAL_BASIS_c'],
                'nbim_value': row['NOMINAL_BASIS_n'],
                'difference': abs(row['NOMINAL_BASIS_c'] - row['NOMINAL_BASIS_n'])
            })
        
        # Gross amount
        gross_diff = abs(row['GROSS_AMOUNT'] - row['GROSS_AMOUNT_QUOTATION'])
        if gross_diff > tolerance:
            breaks.append({
                'type': 'GROSS_AMOUNT',
                'event': event,
                'account': account,
                'isin': isin,
                'custody_amount': row['GROSS_AMOUNT'],
                'nbim_amount': row['GROSS_AMOUNT_QUOTATION'],
                'difference': gross_diff
            })
        
        # Net amount
        net_diff = abs(row['NET_AMOUNT_QC'] - row['NET_AMOUNT_QUOTATION'])
        if net_diff > tolerance:
            breaks.append({
                'type': 'NET_AMOUNT',
                'event': event,
                'account': account,
                'isin': isin,
                'custody_amount': row['NET_AMOUNT_QC'],
                'nbim_amount': row['NET_AMOUNT_QUOTATION'],
                'difference': net_diff
            })
        
        # Tax
        tax_diff = abs(row['TAX'] - row['WTHTAX_COST_QUOTATION'])
        if tax_diff > tolerance:
            breaks.append({
                'type': 'TAX',
                'event': event,
                'account': account,
                'isin': isin,
                'custody_tax': row['TAX'],
                'custody_rate': row['TAX_RATE'],
                'nbim_tax': row['WTHTAX_COST_QUOTATION'],
                'nbim_rate': row['WTHTAX_RATE'],
                'difference': tax_diff
            })
        
        # Dates
        custody_ex = pd.to_datetime(row['EX_DATE'], format='%d.%m.%Y', errors='coerce')
        nbim_ex = pd.to_datetime(row['EXDATE'], format='%d.%m.%Y', errors='coerce')
        if pd.notna(custody_ex) and pd.notna(nbim_ex) and custody_ex != nbim_ex:
            breaks.append({
                'type': 'EX_DATE',
                'event': event,
                'account': account,
                'isin': isin,
                'custody_date': str(custody_ex.date()),
                'nbim_date': str(nbim_ex.date())
            })
        
        custody_pay = pd.to_datetime(row['PAY_DATE'], format='%d.%m.%Y', errors='coerce')
        nbim_pay = pd.to_datetime(row['PAYMENT_DATE'], format='%d.%m.%Y', errors='coerce')
        if pd.notna(custody_pay) and pd.notna(nbim_pay) and custody_pay != nbim_pay:
            breaks.append({
                'type': 'PAY_DATE',
                'event': event,
                'account': account,
                'isin': isin,
                'custody_date': str(custody_pay.date()),
                'nbim_date': str(nbim_pay.date())
            })
    
    return {
        'total': len(breaks),
        'breaks': breaks
    }

