from openai import OpenAI
import pandas as pd
import json
from utils import load_dividend_events, parse_json_output, summarize_agent_output, spinner, write_json_file
from utils import parse_json_output
from break_checks import detect_breaks
from sub_agents import contextualize_policy_text
from dividend_policy import POLICY_TEXT
from prompts import BASE_SYSTEM_PROMPT, BREAK_DIAGNOSIS_PROMPT, POLICY_AGENT_PROMPT


nbim_books = "data/NBIM_Dividend_Bookings 1 (2).csv"
custody_books = "data/CUSTODY_Dividend_Bookings 1 (2).csv"


break_model = "gpt-4.1-nano"


client = OpenAI()



def break_diagnozer_agent(internal, custodian, model):

    nbim_json = load_dividend_events(nbim_books)
    custody_json = load_dividend_events(custody_books)

    breaks = detect_breaks(internal, custodian)["breaks"]

    user_msg = f"""
        Breaks detected: {breaks}, 

        NBIM: {nbim_json}, 
        CUSTODY: {custody_json},

        {BREAK_DIAGNOSIS_PROMPT}
        """
    

    # API
    stop = spinner("Diagnosing breaks...")
    response = client.chat.completions.create(
        model=model,
        # max_tokens=1000
        messages=[
            {"role":"system","content":BASE_SYSTEM_PROMPT},
            {"role":"user","content":user_msg}
        ]
    ).choices[0].message.content
    stop()


    result = json.loads(response)
    write_json_file(result, "break_agent")
    
    try:
        return result
    except:
        return {"kind":"error", "raw": response}
    





def policy_agent(breaks, break_diagnosis, policy_text, model):

    policy_context = contextualize_policy_text(policy_text)
    print(policy_context)
    payload = {
            "BREAKS": breaks,
            "BREAK_DIAGNOSIS": break_diagnosis,
            "POLICY_CONTEXT": policy_context
        }

    usr_msg = f"""
        {POLICY_AGENT_PROMPT}, 
        Evaluate policy for these inputs (JSON only):
        {json.dumps(payload, default=str)}
        """
    
    stop = spinner("Checking Policy...")
    response = client.chat.completions.create(
        model=model,
        temperature=0.0,
        #max_tokens=600,
        messages=[
            {"role": "system", "content": BASE_SYSTEM_PROMPT},
            {"role": "user", "content": usr_msg}
        ]
    ).choices[0].message.content
    stop()

    
    result = json.loads(response)
    write_json_file(result, "policy_agent")
    
    try:
        return result
    except:
        return {"kind":"error", "raw": response}
    




def tax_and_market_agent():
    return 0








breaks = detect_breaks(nbim_books, custody_books)["breaks"]
diag = break_diagnozer_agent(nbim_books, custody_books, break_model)
p = policy_agent(breaks, diag, POLICY_TEXT, break_model)


