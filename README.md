# DTU-PSN-Investment-Matching-Tools
This repository contains the scripts and instructions to cross-reference investment data with company blacklists

Instructions for using the tool
1) Open LLM_Sub_finder.ipynb using colab.research.google.com
   
   <img width="410" height="281" alt="Screenshot 2026-07-31 153051" src="https://github.com/user-attachments/assets/11d94c86-8ba1-4238-bc30-e3dc85577396" />

2) Click the files tab and then the top folder icon (with two dots next to it) to open up the file directory

   <img width="381" height="325" alt="Screenshot 2026-07-31 153004" src="https://github.com/user-attachments/assets/3b1a15ed-abe6-4bbd-b5ea-eeb8ae93b7b8" />

3) Upload the four function files (corporate_logic.py, fzintegral.py, llm_api.py, run_pipeline.py) to the /content/ folder

   <img width="378" height="282" alt="Screenshot 2026-07-31 153126" src="https://github.com/user-attachments/assets/d053fe99-d22f-4c45-994f-a4bbadd46d5b" />

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
   c) If one determines that the "Portfolio Company" and "Matched Subsidiary" or "Parent Company" are a match, the investment amount must be manually extracted        from the original investment portfolio. Recommended to use Ctrl+F to find the investment as there are often multiple investments in the same firms.
10) Add the matched company along with the amount and asset manager to the tab related to the relevant month in the Investment Template worksheet. The Summary page will autofill as data is entered.
11) If using different asset managers than the ones listed, go to the 'January' tab and change cells N8, N9, N10, etc. to the names of the asset managers. Then edit the formula for cells M8, M9, M10, etc so that the text in the formula between the two asterisks is the same as the text entered into N8, N9, N10, etc. Copy this block of edited cells and paste them in the same location for all the other monthly tabs. If using more than 3 asset managers, format the Summary tab accordingly by cutting and pasting the blacklist summary columns the required amount of columns away and adjusting the formulas for each subsequent asset manager. 
