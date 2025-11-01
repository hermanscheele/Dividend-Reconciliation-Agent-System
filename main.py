from openai import OpenAI
import pandas as pd
import json
from utils import load_dividend_events, parse_json_output, summarize_agent_output, spinner
from break_checks import detect_breaks
from prompts import BASE_SYSTEM_PROMPT, BREAK_DIAGNOSIS_PROMPT



nbim_books = "data/NBIM_Dividend_Bookings 1 (2).csv"
custody_books = "data/CUSTODY_Dividend_Bookings 1 (2).csv"


break_model = "gpt-4.1-nano"


client = OpenAI()


def diagnose_breaks(internal, custodian):

    nbim_json = load_dividend_events(nbim_books)
    custody_json = load_dividend_events(custody_books)

    breaks = detect_breaks(internal, custodian)["breaks"]

    user_msg = f"""
        Breaks detected: {breaks}, 

        NBIM: {nbim_json}, 
        CUSTODY: {custody_json},

        {BREAK_DIAGNOSIS_PROMPT}
        """
    
    stop = spinner("Diagnosing breaks...")

    response = client.chat.completions.create(
        model=break_model,
        messages=[
            {"role":"system","content":BASE_SYSTEM_PROMPT},
            {"role":"user","content":user_msg}
        ]
    ).choices[0].message.content

    stop()

    try:
        return json.loads(response)
    except:
        return {"kind":"error", "raw": response}
    






diag = diagnose_breaks(nbim_books, custody_books)
