
def apply_safeguards(resolutions, breaks, diagnosis):
    
    override_count = 0
    
    for resolution in resolutions:
        break_id = resolution.get("break_id")
        
        # Get corresponding data
        break_data = breaks[break_id - 1] if break_id <= len(breaks) else {}
        diag_data = next((d for d in diagnosis if d.get("break_id") == break_id), {})
        
        # Store original decision
        resolution["original_auto_fixable"] = resolution.get("auto_fixable")
        resolution["safeguard_applied"] = False
        
        # Only check if LLM said auto-fixable
        if not resolution.get("auto_fixable"):
            continue
        
        # RULE 1: Position errors
        if break_data.get("type") in ["NOMINAL_MISMATCH", "ISIN_MISMATCH"]:
            resolution["auto_fixable"] = False
            resolution["safeguard_applied"] = True
            resolution["human_reason"] = "Position data errors require investigation"
            print(f"     Break {break_id}: Blocked - Position error")
            override_count += 1
            continue
        
        # RULE 2: Large amounts (raised to $200K for demo)
        amount = abs(break_data.get("difference", 0))
        if amount > 200000:
            resolution["auto_fixable"] = False
            resolution["safeguard_applied"] = True
            resolution["human_reason"] = f"Amount ${amount:,} exceeds $200K threshold"
            print(f"     Break {break_id}: Blocked - Amount ${amount:,} > $200K")
            override_count += 1
            continue
        
        # RULE 3: Custodian errors
        if diag_data.get("source") == "external_custodian_error":
            resolution["auto_fixable"] = False
            resolution["safeguard_applied"] = True
            resolution["human_reason"] = "Custodian errors require escalation"
            print(f"     Break {break_id}: Blocked - Custodian error")
            override_count += 1
            continue
        
        # RULE 4: Uncertain cases
        if diag_data.get("source") == "unclear" or resolution.get("fix_confidence") == "low":
            resolution["auto_fixable"] = False
            resolution["safeguard_applied"] = True
            resolution["human_reason"] = "Uncertain classification requires review"
            print(f"     Break {break_id}: Blocked - Uncertain")
            override_count += 1
            continue
    
    return override_count
