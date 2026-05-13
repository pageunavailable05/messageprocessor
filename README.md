## How to run

1. Clone the repository

git clone https://github.com/pageunavailable05/messageprocessor
cd messageprocessor

3. Create virtual environment
   
python3 -m venv venv
source venv/bin/activate

5. Install dependencies
   
pip install -r requirements.txt

7. Add your data
   
Place your messages.json file into the "data" folder

9. Run the script
    
python src/main.py

11. Check results in the "output" folder
    
classified_messages.csv — all messages with category
summary_report.txt — statistics report


## What the script does.

This script takes a JSON file with user messages, removes all invalid entries such as missing user_id, empty messages, duplicates and missing channels, and classifies each message into one of four categories: grant_search, report_request, general_question, or unknown. It logs all skipped messages with reasons so you can see exactly what was filtered out. The cleaned and classified data is saved to a CSV file, and a summary report with statistics by category, channel and user is saved as a TXT file.

## What decisions I made

Since the main goal of the script is data analysis, I removed all messages with missing user_id, message, or channel because, without any of these fields the data is incomplete and meaningless for analysis. I stripped whitespace as required by the task. Additionally I added extra check on my own: duplicate detection based on user_id + message + created_at combination to avoid skewed results in the report.

## What I would improve

1. I would add proper error handling for the JSON file so the script does not crash silently, but instead logs a clear message when the file is missing, empty or corrupted.
2. I would implement the Postgres database integration for a more professional approach, storing cleaned and classified messages with a proper schema and secure connection via environment variables.
3. I would handle edge cases for unexpected user input, for example extremely long messages or messages with special characters that could break the classification or file saving.
4. I would expand the keyword lists for each category to improve classification accuracy and reduce the number of messages falling into the unknown category.


## TIME

I spent approximately 5 hours on this assignment, including reading the task, writing the script, and preparing the written answers.
