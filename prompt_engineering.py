"""
prompt_engineering.py

Contains the prompt templates and logic to craft instructions
for generating cold emails.
"""

from typing import Dict

def build_cold_email_prompt(company_info: Dict) -> str:
    company_name = company_info.get("Company", "")
    revenu = company_info.get("Revenu", "")
    countries = company_info.get("Countries", "")
    strategy = company_info.get("Strategy", "")
    painpoints = company_info.get("Painpoints", "")
    product_use_cases = company_info.get("Product use cases", "")

    # Here we add a short "few-shot" style example
    # to guide the model to produce a subject + short body.
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

    prompt = f"""
You are an AI sales assistant at Mirakl. 
Your role: write a personalized cold outreach email to {company_name}.
Keep it under 180 words and include a compelling subject line and a short body.

Context for {company_name}:
- Annual online revenue: {revenu}
- Countries/Markets: {countries}
- High-level strategy or areas of focus: {strategy}
- Potential pain points: {painpoints}
- Mirakl product use cases: {product_use_cases}

Guidelines:
1. Write in a friendly, professional tone aligned with Mirakl's brand voice.
2. Provide a subject line first on a separate line, then the email body.
3. You can reference the sample format below, but make it unique to this company.
4. Remain concise and avoid too many bullet points.

Here is an example email for reference:
{example_email}

Now craft YOUR new subject line and email below:
"""
    return prompt.strip()