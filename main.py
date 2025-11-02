from openai import OpenAI
import pandas as pd
import json
from utils import load_dividend_events, parse_json_output, summarize_agent_output, spinner, write_json_file
from utils import parse_json_output
from break_checks import detect_breaks
from sub_agents import contextualize_policy_text
from dividend_policy import POLICY_TEXT
from prompts import BASE_SYSTEM_PROMPT, BREAK_DIAGNOSIS_PROMPT, POLICY_AGENT_PROMPT





client = OpenAI()


# ============================================================================
# STEP 1: MARKET VALIDATION (Get external facts FIRST)
# ============================================================================


def market_validation_agent(breaks, model):

    results = []
    
    for i, brk in enumerate(breaks, 1):
        
        # Get country from ISIN
        isin = brk.get('isin', '')
        country_map = {
            'KR': 'South Korea', 'CH': 'Switzerland', 'US': 'United States',
            'GB': 'United Kingdom', 'JP': 'Japan', 'DE': 'Germany', 'FR': 'France'
        }
        country = country_map.get(isin[:2], isin[:2]) if len(isin) >= 2 else 'Unknown'
        
        # Simple query
        query = f"""
            Search public sources for market standards regarding:

            ISIN: {isin}
            Country: {country}
            Custodian: {brk.get('custodian')}
            Break type: {brk.get('type')}
            Ex-date: {brk.get('ex_date')}
            Pay-date: {brk.get('pay_date')}

            Find official dividend details, tax rates, and payment dates.

            Determine: Is this break due to "internal" (NBIM error) or "external" (standard market practice)?

            IMPORTANT: In the "sources" field, include the actual HTTPS URLs of the websites you found, not search references.

            Return ONLY this JSON (no markdown, no explanations):
            {{
                "break_id": {i},
                "issuer_country": "{country}",
                "custodian": "{brk.get('custodian')}",
                "public_info_summary": "<short summary of market standard>",
                "likely_source": "internal|external|uncertain",
                "reason": "<one sentence why>",
                "sources": ["https://example.com/page1", "https://example.com/page2"]
            }}
            """
        
        stop = spinner(f"Market research for break: {i}/{len(breaks)}...")
        response = client.responses.create(
            model=model,
            tools=[{"type": "web_search"}],
            input=query
        )
        stop()
        
        # Parse response
        try:
            parsed = json.loads(response.output_text)
        except:
            parsed = {"break_id": i, "error": "parse_error", "raw": response.output_text}
        
        results.append(parsed)
    
    write_json_file(results, "market_agent")
    return results




# ============================================================================
# STEP 3: DIAGNOSIS (Using market facts)
# ============================================================================

def break_diagnosis_agent(breaks, market_validation, model):
  
    
    user_msg = f"""
        You are diagnosing dividend reconciliation breaks.

        BREAKS DETECTED:
        {json.dumps(breaks, indent=2)}

        MARKET VALIDATION RESULTS (verified external facts):
        {json.dumps(market_validation, indent=2)}

        {BREAK_DIAGNOSIS_PROMPT}
        """
    
    stop = spinner(f"🔬 Diagnosing {len(breaks)} breaks with market facts...")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a financial reconciliation expert."},
            {"role": "user", "content": user_msg}
        ],
        response_format={"type": "json_object"}
    )
    stop()

    result = json.loads(response.choices[0].message.content)
    
    diagnosed_count = len(result.get('diagnosis', []))
    print(f"✓ Diagnosed {diagnosed_count}/{len(breaks)} breaks")
    
    if diagnosed_count != len(breaks):
        print(f"⚠️  Warning: Missing {len(breaks) - diagnosed_count} diagnoses")
    
    write_json_file(result, "break")
    return result



# ============================================================================
# STEP 4: POLICY CHECK
# ============================================================================

def policy_agent(breaks, diagnosis, policy_text, model):

    user_msg = f"""
        Check if these breaks and their diagnoses violate any policies:

        BREAKS: {json.dumps(breaks, indent=2)}
        DIAGNOSIS: {json.dumps(diagnosis, indent=2)}
        POLICY: {policy_text}

        Return JSON with policy violations.
        """
    
    stop = spinner("📋 Checking policy compliance...")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a policy compliance expert."},
            {"role": "user", "content": user_msg}
        ],
        response_format={"type": "json_object"}
    )
    stop()

    result = json.loads(response.choices[0].message.content)
    print("✓ Policy check complete")
    
    write_json_file(result, "policy")

    return result















nbim_file = "data/NBIM_Dividend_Bookings 1 (2).csv"
custody_file = "data/CUSTODY_Dividend_Bookings 1 (2).csv"




breaks = detect_breaks(nbim_file, custody_file)["breaks"]
print(breaks)
market_facts = market_validation_agent(breaks, model="gpt-4o")
diagnosis = break_diagnosis_agent(breaks, market_facts, model="gpt-4.1-nano")
policy_result = policy_agent(breaks, diagnosis, POLICY_TEXT, model="gpt-4.1-nano")


