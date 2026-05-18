import pandas as pd
import time
import chardet
import os
from IPython.display import display, clear_output
from corporate_logic import get_company_structure

def load_input_file(path, company_column=None):
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    if path.lower().endswith((".xlsx", ".xls")):
        df = pd.read_excel(path)
    else:
        with open(path, "rb") as f:
            raw_sample = f.read(100000)
        encoding = chardet.detect(raw_sample).get("encoding", "utf-8")
        df = pd.read_csv(path, encoding=encoding, sep=None, engine="python", on_bad_lines="skip")

    return _standardize_company_column(df, company_column)

def _standardize_company_column(df, company_column=None):
    df = df.dropna(axis=1, how="all")
    if df.shape[1] == 0:
        raise ValueError("No usable columns found.")

    if len(df.columns) == 1:
        df.columns = ["Company"] if company_column is None else [company_column]
        return df

    if company_column is not None and company_column in df.columns:
        df.rename(columns={company_column: "Company"}, inplace=True)
        return df

    lower_cols = [c.lower() for c in df.columns]
    if company_column is not None and company_column.lower() in lower_cols:
        actual = df.columns[lower_cols.index(company_column.lower())]
        df.rename(columns={actual: "Company"}, inplace=True)
        return df

    text_scores = {}
    for col in df.columns:
        non_null = df[col].dropna()
        if len(non_null) == 0:
            continue
        text_scores[col] = non_null.astype(str).str.len().mean()

    best = max(text_scores, key=text_scores.get)
    df.rename(columns={best: "Company"}, inplace=True)
    return df

def run_pipeline(csv_path, output_path="companies.csv", instructions=None, model="openai/gpt-5.2", company_column=None, delay=2):
    df = load_input_file(csv_path, company_column)
    company_names = df["Company"].dropna().unique()

    rows = []
    live_df = pd.DataFrame(columns=["Company", "Immediate Parent", "Ultimate Parent", "Subsidiaries", "Error"])
    display(live_df)

    for name in company_names:
        print(f"Retrieving corporate structure for: {name}")
        time.sleep(delay)

        company_instructions = None
        if instructions is not None:
            company_instructions = instructions.format(company_name=name)

        data = get_company_structure(name, instructions=company_instructions, model=model)

        if data is None or "error" in data:
            row = {
                "Company": name,
                "Immediate Parent": None,
                "Ultimate Parent": None,
                "Subsidiaries": None,
                "Error": data.get("error") if isinstance(data, dict) else "No response"
            }
        else:
            immediate = data.get("immediate_parent") or {}
            ultimate = data.get("ultimate_parent") or {}
            subsidiaries = data.get("subsidiaries") or []

            row = {
                "Company": name,
                "Immediate Parent": immediate.get("name"),
                "Ultimate Parent": ultimate.get("name"),
                "Subsidiaries": ", ".join(sub.get("name") for sub in subsidiaries if sub.get("name")),
                "Error": None
            }

        rows.append(row)
        live_df = pd.DataFrame(rows)
        clear_output(wait=True)
        display(live_df)

    df_final = df.merge(live_df, on="Company", how="left")
    df_final.to_csv(output_path, index=False)

    print(f"Saved output to: {output_path}")
    return df_final

if __name__ == "__main__":
    run_pipeline("/content/x.xlsx", output_path="companies.csv", model="openai/gpt-5.2", company_column="Company Standard Name")
