# DTU-PSN-Investment-Matching-Tools
This repository contains the scripts and instructions to cross-reference investment data with company blacklists

Instructions for using the tool
1) Open LLM_Sub_finder.ipynb using colab.research.google.com
2) Click the files tab and then the top folder icon (with two dots next to it) to open up the file directory
3) Upload the four function files (corporate_logic.py, fzintegral.py, llm_api.py, run_pipeline.py) to the /content/ folder
4) Upload company_cross_reference.xlsx and the investment lists which are of interest to the /sample_data/ folder
   a) Investment data should be in a .csv or .xlsx file, can use .pdf stripping tools if necessary (one is native to excel) 
   b) The column with the company names needs to be titled "Company"
5) Scroll through the cells and update the file paths where necessary; for example the path to requirements should read /content/requirements.txt
6) Run Cell 1 to install necessary packages
7) Run Cell 2 to update directory
8) IF ONE WISHES TO CREATE A NEW COMPANY BLACKLIST: Run Cells 3 and 4, otherwise skip this step
   a) Requires an openai_api_key
   b) The LLM will attempt to find parent companies and subsidiaries of the companies supplied
9) Run Cell 5 to match investment data to the blacklisted company list
   a) The matches will output as a .csv file with four columns: Portfolio Company, Matched Subsidiary, Parent Company, Match Score
   b) The next steps are manual. Match score indicates how good the string matching is between "Portfolio Company" and either "Matched Subsidiary" or "Parent          Company". Results less than 0.8 are omitted. Generally results below 0.9 are not a match but this must be determined manually.
   c) If one determines that the "Portfolio Company" and "Matched Subsidiary" or "Parent Company" are a match, the investment amount must me manually extracted        from the original investment portfolio. Recommended to use Ctrl+F to find the investment as there are often multiple investments in the same firms.
