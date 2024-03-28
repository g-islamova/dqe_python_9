### Prerequisites
Before running the main script (task10_main.py), ensure you have the following:

- Required dependencies installed (pyodbc).
- Database is initialized and tables are created (run the script named "task10_db.py")

### Usage
Run the main script (task10_main.py) and follow the on-screen instructions to interact with 
the News Feed tool. 

You can choose from the following options:

- Add Records from File (TXT): The source TXT file containing records should be named **"news_file"** 
and placed in the same folder as the script.
- Add Records from File (JSON): The folder containing JSON files with records should be named **"json_files"**
and placed in the same folder as the script
- Add Records from File (XML): The folder containing XML files with records should be named **"xml_files"** 
and placed in the same folder as the script
- Add Records Manually: Input records manually.
- Quit: Exit the application.

You can find sample files with sample records in the branch. Feel free to add our own data.


### Information about database
The script uses an SQLite database. Check for duplicates is performed on database side.

### Notes
Make sure to provide valid paths when prompted for file or folder paths.
Word and letter counts are saved to CSV files (word_counts.csv, letter_counts.csv).

