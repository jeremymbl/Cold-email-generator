"""
prompt_engineering.py

Contains the prompt templates and logic to craft instructions
for generating cold emails.
"""

example_email = """
Example of a successful cold email:

SUBJECT: Driving Growth for ACME Inc.'s Global Expansion

BODY:
Hi Mark,

I noticed ACME Inc. is expanding into new markets this year. At Mirakl, we've helped companies like X and Y streamline their global e-commerce operations, so you can onboard new sellers faster while keeping operational costs low.

Given your strategy to expand to 3 new countries, I'd love to share how our technology could address typical expansion pain points, from cross-border compliance to payment solutions.

If that sounds relevant, I'd be happy to schedule a brief 15-minute chat next week. Looking forward to hearing from you!

Best,
[Your Name]
"""

from typing import Dict

def build_cold_email_prompt(company_info: Dict) -> str:
    company_name = company_info.get("Company", "")
    revenue = company_info.get("Revenue", "")
    countries = company_info.get("Countries", "")
    strategy = company_info.get("Strategy", "")
    painpoints = company_info.get("Pain Points", "")
    product_use_cases = company_info.get("Products & use cases", "")
    
    prompt = f"""
You are an AI sales assistant at Mirakl. 
Your role: write a personalized cold outreach email to {company_name}.
Keep it under 180 words and include a compelling subject line and a short body.

Context for {company_name}:
- Annual online revenue: {revenue}
- Countries/Markets: {countries}
- High-level strategy or areas of focus: {strategy}
- Potential pain points: {painpoints}
- Mirakl products & use cases: {product_use_cases}

Guidelines:
1. Write in a friendly, professional tone aligned with Mirakl's brand voice.
2. Provide a subject line first on a separate line, then the email body.
3. You can reference the sample format below, but make it unique to this company.
4. Remain concise and avoid bullet points.

Here is an example email for reference:
{example_email}

Now craft YOUR new subject line and email below:
"""
    return prompt.strip()

def build_crm_email_prompt(company_info: Dict) -> str:
    """
    Constructs a prompt for generating a personalized email based on combined CRM and TamTam data.
    This prompt uses both the CRM fields and the TamTam fields.
    """
    company = company_info.get("Company", "")
    # TamTam context
    revenue = company_info.get("Revenue", "")
    countries = company_info.get("Countries", "")
    strategy = company_info.get("Strategy", "")
    painpoints = company_info.get("Pain Points", "")
    product_use_cases = company_info.get("Products & use cases", "")
    # CRM context
    contact_name = company_info.get("ContactName", "")
    last_interaction = company_info.get("LastInteraction", "")
    email_history = company_info.get("EmailHistory", "")
    call_summary = company_info.get("CallSummary", "")
    additional_notes = company_info.get("AdditionalNotes", "")

    prompt = f"""
You are an AI sales assistant at Mirakl.
Your role: write a personalized follow-up email for {company} using both our market data and CRM insights.
Context from TamTam:
- Annual online revenue: {revenue}
- Countries/Markets: {countries}
- High-level strategy: {strategy}
- Key pain points: {painpoints}
- Products & use cases: {product_use_cases}

Additional CRM context:
- Contact Name: {contact_name}
- Last Interaction: {last_interaction}
- Email History: {email_history}
- Call Summary: {call_summary}
- Additional Notes: {additional_notes}

Guidelines:
1. Write in a friendly, professional tone aligned with Mirakl's brand voice.
2. Provide a subject line first on a separate line, then the email body.
3. You can reference the sample format below, but make it unique to this company.
4. Remain concise and avoid bullet points.
Keep the email under 180 words.

Here is an example email for reference:
{example_email}

Now craft YOUR new email below:
"""
    return prompt.strip()