"""
main.py

Entry point for running the Cold Emails Generator AI Agent for a single selected company.
"""

import pandas as pd
from data_loader import load_tamtam_data, load_hubspot_data, merge_data
from email_generator import generate_cold_email
from config import OUTPUT_FILE
import logging

def main(batch_mode: bool = False):
    tamtam_df = load_tamtam_data()
    hubspot_df = load_hubspot_data()
    merged_df = merge_data(tamtam_df, hubspot_df)

    if merged_df.empty:
        print("No companies found in the data.")
        return

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    print("Available companies:")
    for idx, row in merged_df.iterrows():
        print(f"{idx}: {row.get('Name', 'Unnamed Company')}")
    logging.info("Available companies printed to terminal.")

    if not batch_mode:
        # -- Interactive single-company mode --
        logging.info("Available companies:")
        for idx, row in merged_df.iterrows():
            logging.info(f"{idx}: {row.get('Name', 'Unnamed Company')}")

        try:
            selected_index = int(input("Enter the index of the company for which you want to generate the email: "))
        except ValueError:
            logging.error("Invalid input. Please enter a valid number.")
            return

        if selected_index not in merged_df.index:
            print("Invalid index selected.")
            return

        selected_row = merged_df.loc[selected_index]
        company_info = {
            "Company": selected_row.get("Name", ""),
            "Revenu": selected_row.get("Revenue", ""),
            "Countries": selected_row.get("Countries", ""),
            "Strategy": selected_row.get("Strategy", ""),
            "Painpoints": selected_row.get("Pain Points", ""),
            "Product use cases": selected_row.get("Products & use cases", "")
        }
        logging.info("Validated Input Data: %s", company_info)

        result = generate_cold_email(company_info)
        email_text = result.get("GeneratedEmail", "")

        print("\nGenerated Email:")
        print("-" * 80)
        print(email_text)
        print("-" * 80)

        # Save result to CSV
        result_item = {
            "Company": company_info["Company"],
            "GeneratedEmail": email_text,
            "ResponseTime_sec": result.get("ResponseTime", ""),
            "TokensUsed": result.get("TokensUsed", ""),
            "EstimatedCost_$": result.get("EstimatedCost", "")
        }
        results_df = pd.DataFrame([result_item])
        results_df.to_csv(OUTPUT_FILE, index=False)
        print(f"Email and metrics saved to {OUTPUT_FILE}")

    else:
        # -- Batch mode: interactive selection of companies --
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
                "Company": row.get("Name", ""),
                "Revenu": row.get("Revenue", ""),
                "Countries": row.get("Countries", ""),
                "Strategy": row.get("Strategy", ""),
                "Painpoints": row.get("Pain Points", ""),
                "Product use cases": row.get("Products & use cases", "")
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
    # You can toggle batch_mode to True/False here or 
    # parse from command line arguments for flexibility
    # e.g., python main.py --batch
    main(batch_mode=True)