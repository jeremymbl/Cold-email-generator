"""
main.py
"""

import pandas as pd
from data_loader import load_tamtam_data, load_hubspot_data, merge_data
from email_generator import generate_cold_email
from config import OUTPUT_FILE
import logging

def main(batch_mode):
    tamtam_df = load_tamtam_data()
    hubspot_df = load_hubspot_data()
    merged_df = merge_data(tamtam_df, hubspot_df)

    if merged_df.empty:
        print("No companies found in the data.")
        return

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    print("Available companies:")
    for idx, row in merged_df.iterrows():
        print(f"{idx}: {row.get('Company', 'Unnamed Company')}")

    if not batch_mode: # generate mail for a single company
        try:
            selected_index = int(input("Enter the index of the company for which you want to generate the email: "))
        except ValueError:
            logging.error("Invalid input. Please enter a valid number.")
            return

        if selected_index not in merged_df.index:
            print("Invalid index selected.")
            return

        selected_row = merged_df.loc[selected_index]

        company_info_tamtam = {
            "Company": selected_row.get("Company", ""),
            "Revenue": selected_row.get("Revenue", ""),
            "Countries": selected_row.get("Countries", ""),
            "Strategy": selected_row.get("Strategy", ""),
            "Pain Points": selected_row.get("Pain Points", ""),
            "Products & use cases": selected_row.get("Products & use cases", "")
        }

        company_info_crm = {
            "Company": selected_row.get("Company", ""),
            "Revenue": selected_row.get("Revenue", ""),
            "Countries": selected_row.get("Countries", ""),
            "Strategy": selected_row.get("Strategy", ""),
            "Pain Points": selected_row.get("Pain Points", ""),
            "Products & use cases": selected_row.get("Products & use cases", ""),
            "ContactName": selected_row.get("ContactName", ""),
            "Email": selected_row.get("Email", ""),
            "Domain": selected_row.get("Domain", ""),
            "HS_Contact_ID": selected_row.get("HS_Contact_ID", ""),
            "LastInteraction": selected_row.get("LastInteraction", ""),
            "EmailHistory": selected_row.get("EmailHistory", ""),
            "CallSummary": selected_row.get("CallSummary", ""),
            "AdditionalNotes": selected_row.get("AdditionalNotes", "")
        }

        """"
        logging.info("Validated TamTam Data: %s", company_info_tamtam)
        logging.info("Validated CRM Data: %s", company_info_crm)
        """

        # Generate email using only Tamtam data
        result_tamtam = generate_cold_email(company_info_tamtam)
        email_text_tamtam = result_tamtam.get("GeneratedEmail", "")

        # Generate email using CRM data + Tamtam data
        from email_generator import generate_crm_email
        result_crm = generate_crm_email(company_info_crm)
        email_text_crm = result_crm.get("GeneratedEmail", "")

        """
        print("\nGenerated Email using Tamtam Data:")
        print("-" * 80)
        print(email_text_tamtam)
        print("-" * 80)

        print("\nGenerated Email using CRM Data:")
        print("-" * 80)
        print(email_text_crm)
        print("-" * 80)"
        """
        prompt_tamtam = result_tamtam.get("Prompt", "No prompt available for Tamtam email.")
        prompt_crm = result_crm.get("Prompt", "No prompt available for CRM email.")

        print("\nPrompt for Tamtam Data Email:")
        print("-" * 80)
        print(prompt_tamtam)
        print("-" * 80)

        print("\nPrompt for CRM Data Email:")
        print("-" * 80)
        print(prompt_crm)
        print("-" * 80)

        results = [
            {
                "Version": "Tamtam Data",
                "Company": company_info_tamtam["Company"],
                "GeneratedEmail": email_text_tamtam,
                "ResponseTime_sec": result_tamtam.get("ResponseTime", ""),
                "TokensUsed": result_tamtam.get("TokensUsed", ""),
                "EstimatedCost_$": result_tamtam.get("EstimatedCost", "")
            },
            {
                "Version": "Tamtam + Mirakl CRM Data",
                "Company": company_info_crm["Company"],
                "GeneratedEmail": email_text_crm,
                "ResponseTime_sec": result_crm.get("ResponseTime", ""),
                "TokensUsed": result_crm.get("TokensUsed", ""),
                "EstimatedCost_$": result_crm.get("EstimatedCost", "")
            }
        ]
        results_df = pd.DataFrame(results)
        results_df.to_csv(OUTPUT_FILE, index=False)
        print(f"Emails and metrics saved to {OUTPUT_FILE}")

    else:
        # send mails to multiple companies
        selected_indices = []
        print("Enter the indices of the companies you want to generate emails for.")
        print("Type 'STOP' when you are finished.")
        while True:
            user_input = input("Enter company index (or 'STOP'): ").strip()
            if user_input.lower() == "stop":
                break
            try:
                index = int(user_input)
                if index not in merged_df.index:
                    print("Invalid index. Please enter a valid company index.")
                else:
                    if index in selected_indices:
                        print("Index already selected.")
                    else:
                        selected_indices.append(index)
            except ValueError:
                print("Invalid input. Please enter a number or 'STOP'.")

        if not selected_indices:
            print("No valid indices selected. Exiting.")
            return

        all_results = []
        cost_tracker = {"TotalTokens": 0, "TotalCost": 0.0}  # optional aggregator
        for idx in selected_indices:
            row = merged_df.loc[idx]
            company_info = {
                "Company": row.get("Company", ""),
                "Revenue": row.get("Revenue", ""),
                "Countries": row.get("Countries", ""),
                "Strategy": row.get("Strategy", ""),
                "Pain Points": row.get("Pain Points", ""),
                "Products & use cases": row.get("Products & use cases", "")
            }
            result = generate_cold_email(company_info, cost_tracker=cost_tracker)
            all_results.append({
                "Index": idx,
                "Company": company_info["Company"],
                "GeneratedEmail": result.get("GeneratedEmail", ""),
                "ResponseTime_sec": result.get("ResponseTime", ""),
                "TokensUsed": result.get("TokensUsed", ""),
                "EstimatedCost_$": result.get("EstimatedCost", "")
            })

        batch_df = pd.DataFrame(all_results)
        batch_df.to_csv(OUTPUT_FILE, index=False)
        print(f"Batch run complete. Emails saved to {OUTPUT_FILE}")
        logging.info("Total tokens used: %d, Total estimated cost: $%.5f",
                     cost_tracker["TotalTokens"], cost_tracker["TotalCost"])

if __name__ == "__main__":
    main(batch_mode = False)
