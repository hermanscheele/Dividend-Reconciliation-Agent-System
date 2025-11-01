

# Call model with agent specific instruction
def call_agent(user_msg: str):
    resp = client.chat.completions.create(
        model="gpt-5-mini",   
        messages=[
            {"role": "system", "content": BASE_SYSTEM_PROMPT},
            {"role": "user", "content": user_msg}
        ]
    )
    return resp.choices[0].message.content





def detect_breaks(internal, custodian):

    user_msg = f"""
        Internal: {internal}
        Custodian: {custodian}
        {BREAK_AGENT_INSTRUCTION}
        """
    
    stop = spinner("Detecting breaks...")

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
    


















# Matches internal and custodian records
def matching_agent():
    return 0














# Spots inconsistencies
def break_detection_agent():
    return 0

# Explains the issue and proposes a fix
def llm_analyst():
    return 0
    
# Automatically checks external sources
def market_aware_agent():
    return 0

# Creates draft accounting adjustments or custodian queries
def remediation_agent():
    return 0

# Escalates unclear cases to humans
def supervisor_agent():
    return 0


# Discussion and conclusion among 2 or more models
def model_think_tank():
    return 0


# Ask for specific feedback to "tune" the other agents
def feedback_agent():
    return 0

# NBIM policies + regulatory rules embedded in the agent
def policy_reasoning_agent():
    return 0



# Super agent that orchesters all other agents
def main_agent():
    return 0