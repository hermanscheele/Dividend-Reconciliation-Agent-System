from openai import OpenAI
import json
from utils import spinner
from prompts import POLICY_CONTEXTUALIZER_PROMPT


client = OpenAI()

def contextualize_policy_text(policy_text, model="gpt-4.1-nano"):

    msg = [
        {"role":"system","content":"JSON only."},
        {"role":"user","content": POLICY_CONTEXTUALIZER_PROMPT + "\n\nPOLICY TEXT:\n" + policy_text}
    ]

    stop = spinner("Contextualizing Policy Text...")
    out = client.chat.completions.create(
        model=model, 
        temperature=0.0, 
        messages=msg).choices[0].message.content
    stop()
    
    try:
        data = json.loads(out)
        return data if isinstance(data, dict) and "rules" in data else {"rules": []}
    except:
        # fallback: pass through raw text as one rule
        return {"rules":[{"domain":"EXCEPTIONS","jurisdiction":"global","name":"raw_text",
                          "clause":None,"rule":"See raw text","tolerance":None,"examples":[policy_text[:300]]}]}
