import pandas as pd
import re
from rapidfuzz import fuzz

# Text cleaning
suffix_pattern = re.compile(r'\b(inc|llc|ltd|corporation|corp|co|plc|gmbh|sa|pte)\b', re.IGNORECASE)
punct_pattern = re.compile(r'[^\w\s]')
space_pattern = re.compile(r'\s+')

def clean_text(s):
    if pd.isna(s):
        return ''
    s = str(s).lower().strip()
    s = suffix_pattern.sub('', s)
    s = punct_pattern.sub('', s)
    s = space_pattern.sub(' ', s)
    return s.strip()

# Prepare subsidiaries
def prepare_subsidiaries(df):
    df['Company_clean'] = df['Company'].apply(clean_text)
    df['Subsidiaries'] = df['Subsidiaries'].fillna("")
    df['Subsidiaries_List'] = df['Subsidiaries'].apply(
        lambda x: [clean_text(s) for s in re.split(r',|\n', x) if s.strip() != '']
    )
    subs_df = df.explode('Subsidiaries_List')[['Company_clean', 'Subsidiaries_List']]
    subs_df = subs_df.rename(columns={'Company_clean':'Parent_Company_clean', 'Subsidiaries_List':'Subsidiary_clean'})
    subs_dict = dict(zip(subs_df['Subsidiary_clean'], subs_df['Parent_Company_clean']))
    subs_names = list(subs_dict.keys())
    top_level_companies = df['Company_clean'].tolist()
    return subs_dict, subs_names, top_level_companies

# Fuzzy similarity and Choquet
def compute_similarities(a, b):
    return {
        'token_set_ratio': fuzz.token_set_ratio(a, b),
        'token_sort_ratio': fuzz.token_sort_ratio(a, b),
        'partial_ratio': fuzz.partial_ratio(a, b)
    }

def choquet_score(sim_dict, weights=None):
    if weights is None:
        weights = {'token_set_ratio':0.5, 'token_sort_ratio':0.3, 'partial_ratio':0.2}
    sorted_values = sorted(sim_dict.values(), reverse=True)
    sorted_weights = sorted(weights.values(), reverse=True)
    return sum(v*w for v,w in zip(sorted_values, sorted_weights))

def fuzzy_match_company_choquet(company_clean, subs_dict, subs_names, top_level_companies, threshold=75, limit=5):
    matches = []

    # Check subsidiaries
    for sub in subs_names:
        sim_dict = compute_similarities(company_clean, sub)
        score = choquet_score(sim_dict)
        if score >= threshold:
            matches.append((sub, subs_dict[sub], score))

    # Check top-level companies
    for top_company in top_level_companies:
        sim_dict = compute_similarities(company_clean, top_company)
        score = choquet_score(sim_dict)
        if score >= threshold:
            matches.append((None, top_company, score))

    matches = sorted(matches, key=lambda x: x[2], reverse=True)[:limit]
    return matches

# Main portfolio matching
def match_portfolio_to_subsidiaries(portfolio_path, companies_path, output_path="portfolio_matches.csv", threshold=75):
    if portfolio_path.lower().endswith((".xlsx", ".xls")):
        portfolio = pd.read_excel(portfolio_path)
    else:
        portfolio = pd.read_csv(portfolio_path, sep="\t")
    portfolio['Company_clean'] = portfolio['Company'].apply(clean_text)

    if companies_path.lower().endswith((".xlsx", ".xls")):
        companies = pd.read_excel(companies_path)
    else:
        companies = pd.read_csv(companies_path)

    companies = companies[['Company','Subsidiaries']].fillna("")
    companies['Company_clean'] = companies['Company'].apply(clean_text)

    subs_dict, subs_names, top_level_companies = prepare_subsidiaries(companies)

    results = []
    for _, row in portfolio.iterrows():
        company = row['Company']
        company_clean = row['Company_clean']
        matches = fuzzy_match_company_choquet(company_clean, subs_dict, subs_names, top_level_companies, threshold=threshold)
        if matches:
            for sub_name, parent_company, score in matches:
                results.append({
                    'Portfolio_Company': company,
                    'Matched_Subsidiary': sub_name,
                    'Parent_Company': parent_company,
                    'Match_Score': score
                })
        else:
            results.append({
                'Portfolio_Company': company,
                'Matched_Subsidiary': None,
                'Parent_Company': None,
                'Match_Score': None
            })

    matched_df = pd.DataFrame(results)
    matched_df.to_csv(output_path, index=False)
    print(f"Fuzzy matching complete. Output saved to {output_path}")
    return matched_df
