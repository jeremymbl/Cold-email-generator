"""
email_generator.py

Contains the function that calls OpenAI's API to generate the emails
using the prompt. 
"""

import openai
from typing import Dict
from config import OPENAI_API_KEY
from prompt_engineering import build_cold_email_prompt
import time
import logging

# We'll add a global or module-level variable to track cumulative cost
TOTAL_API_COST = 0.0

def generate_cold_email(company_info: Dict, cost_tracker: Dict = None) -> dict:
    """
    Calls OpenAI to generate a cold email. 
    Optionally updates a shared cost_tracker dict with aggregated usage/cost.
    """
    global TOTAL_API_COST

    openai.api_key = OPENAI_API_KEY
    prompt = build_cold_email_prompt(company_info)
    start_time = time.time()

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI sales assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=300
        )
        end_time = time.time()
        response_time = end_time - start_time

        generated_text = response["choices"][0]["message"]["content"].strip()
        usage = response.get("usage", {})
        total_tokens = usage.get("total_tokens", 0)
        estimated_cost = (total_tokens / 1000) * 0.002

        # Update global and optional dictionary
        TOTAL_API_COST += estimated_cost
        if cost_tracker is not None:
            cost_tracker["TotalTokens"] += total_tokens
            cost_tracker["TotalCost"] += estimated_cost

        logging.info("API Response Time: %.2f seconds", response_time)
        logging.info("Tokens used: %d, Estimated cost: $%.5f", total_tokens, estimated_cost)
        logging.info("Running total cost (global): $%.5f", TOTAL_API_COST)

        return {
            "GeneratedEmail": generated_text,
            "ResponseTime": response_time,
            "TokensUsed": total_tokens,
            "EstimatedCost": estimated_cost
        }

    except Exception as e:
        logging.error("Error generating email for %s: %s", company_info.get("Company", "Unknown"), e)
        return {
            "GeneratedEmail": "",
            "ResponseTime": None,
            "TokensUsed": None,
            "EstimatedCost": None
        }