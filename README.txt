# Cold Email Generator AI Agent

This prototype demonstrates how to build a minimal AI Agent that:
1. Loads data from a Tamtam-generated Excel file (`output-tamtam-lookalike-2024-11-13T18_42_33.xlsx`).
2. Optionally fetches matching data from HubSpot CRM using HubSpot's API.
3. Merges the data.
4. Uses the OpenAI GPT model to generate personalized cold emails.

## Setup & Usage

1. **Install Python** (3.9+ recommended).
2. **Clone / Download** this folder into your local machine.
3. **Fill out your keys**:
   - In `config.py`, replace `YOUR_OPENAI_API_KEY_HERE` with your real OpenAI API key.
   - (Optional) If you wish to pull data from HubSpot, replace `YOUR_HUBSPOT_API_KEY_HERE` with a valid HubSpot API key.
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt