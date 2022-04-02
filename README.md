# Export and import data for Excel and PDF

###### Description: The utility allows to get data from Excel or PDF and export data to Excel or PDF.

## Contents:
- [Usage guide](#usage-guide)
    - [Import from PDF to database](#import-from-pdf-to-database)
    - [Import from Excel to database](#import-from-excel-to-database)
    - [Export users from database to PDF](#export-users-from-database-to-pdf)
    - [Export users from database to Excel](#export-users-from-database-to-excel)

## Usage guide:

* Pull or copy all the files and directories to your computer
* Install all neccessery libruaries by `pip install -r requirements.txt`
* Run main.py by `python main.py`
    * If there isn't `server.sqlite3` file in the root directory - it will be created automatically
    * The database is going to be filled by initial data
    * If there aren't `results/Excel` and `results/PDF` directories - they will be created automatically too
![python main.py](https://i.imgur.com/0HRhisS.png "python main.py")

* `Do you want to import (i) or export (e) data:` - if you want to import data input `i` if to export `e`

### Import from PDF to database:
* `Do you want to import data from excel (e) or pdf (p):` - input `p` to import data from PDF (CV from https://hh.ru ) to database. PDF has to be in the ***/sources*** directory and be named as ***Source.pdf***: `/sources/Source.pdf`
![import from pdf](https://i.imgur.com/hrhlBw6.png "import from pdf")

### Import from Excel to database:
* `Do you want to import data from excel (e) or pdf (p):` - input `e` to import data from Excel to database. Excel has to be in the ***/sources*** directory and be named as ***Source.xlsx***: `/sources/Source.xlsx`. Excel file has to have sheets ***regions***, ***cities***, ***users*** and data, you would like to upload to database
![import from excel](https://i.imgur.com/Xv7Zou6.png "import from excel")

### Export users from database to PDF:
* `Do you want to export data to excel (e) or pdf (p):` - input `p` to export data from database to PDF. PDF-file will be created in `/results/PDF/2022-04-02_11-49-19 Result.pdf` (with current date and time in name)
![export to pdf](https://i.imgur.com/ieiGEko.png "export to pdf")

### Export users from database to Excel:
* `Do you want to export data to excel (e) or pdf (p):` - input `e` to export data from database to Excel. Excel-file will be createdn in `/results/PDF/2022-04-02_11-49-19 Result.pdf` (with current date and time in name)
![export to excel](https://i.imgur.com/B7UpUSE.png "export to excel")
