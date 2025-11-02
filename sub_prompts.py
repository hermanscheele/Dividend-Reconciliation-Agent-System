POLICY_CONTEXTUALIZER_PROMPT = """
Convert the following dividend policy text into a small JSON rule set.

Return ONLY JSON:
{
  "rules": [
    {
      "domain": "WHT | FX | DATES | ADR | NET_FORMULA | EXCEPTIONS",
      "jurisdiction": "<country or 'global'>",
      "name": "<short name>",
      "clause": "<section id if any, else null>",
      "rule": "<one sentence rule>",
      "tolerance": "<e.g., ±0.5pp, ±0.20%> or null",
      "examples": ["<very short example>"]
    }
  ]
}

Keep it brief and actionable. Do not invent rates. If unknown, set null.
"""
