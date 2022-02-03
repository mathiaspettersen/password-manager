# Introduction

##### The password manager is a simple CLI program which connects to several databases to serve and fetch data. Here, you can add entries, delete entries and modify entries, as well as search for password entries within the database. The manager uses SQLite for the database structure.

## Functionality
##### - View all entries
##### - Search for entries
##### - Add new entry
##### - Update entry
##### - Delete entry
##### - Extra
- Password generator
- Secure notes
- Password strength checker
##### - Log
- View/search/modify logs

## Usage

To download program, use:
`git clone https://github.com/mathiaspettersen/password-manager`

Enter the folder, and run:
`python3 main.py`

Default password is `passman`, and can be changed once logged in (`6. Extra -> 4. Change master password`) 

## Miscellaneous

`pass.db` contains the password entries.

`secnot.db` contains the secure notes.

`log.db` contains the logs.

`welcome.db` contains the initial login password.

To open one of the databases, run `sqlite3` and then `.open <dbnamme.db>`. Type `.tables` to view tables and `select * from <table name>;` to view contents.

## Screenshots

Initial launch of `main.py` which shows the login:

![image](https://user-images.githubusercontent.com/70077872/150974794-98faf3a1-3bdd-443e-9552-a775158b9af1.png)

Searching for entries:

![image](https://user-images.githubusercontent.com/70077872/150975384-abcdfacf-e376-4857-ad21-6c434000ba53.png)

Automatic logger output:

![image](https://user-images.githubusercontent.com/70077872/150975516-eb744b8e-7471-49f4-9eae-37bc0e1b7b1b.png)

Password generator:

![image](https://user-images.githubusercontent.com/70077872/150975779-6b2b5707-b15f-479f-8f14-ba77673a0389.png)


