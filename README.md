316 Final Project Code for Amazonians ([Bob Qian](https://www.linkedin.com/in/bob-qian/), 
[Eric Xing](https://www.linkedin.com/in/eric-xing/), [Erika Wang](https://www.linkedin.com/in/erikawang2024/), [Havish Malladi](https://www.linkedin.com/in/havish-malladi/), [Jaewon Jung](https://www.linkedin.com/in/jaewon-jung-09b568180/))

The project is a spin-off of Amazon on a website called Nile

Originally created by [Rickard Stureborg](http://www.rickard.stureborg.com) and [Yihao Hu](https://www.linkedin.com/in/yihaoh/) for Fall 2021.
Amended for Fall 2022.

## Goals

Our goal with this project was to create a replica of the famous [Amazon](https://www.amazon.com/) website. Some of our functionalities, include but are not limited to - allowing users to create an account and login; allowing sellers to sell products; allowing users to add products to a cart and checkout; allowing sellers to process and fufill orders; and allowing users to write reviews. We used HTML/CSS to write the front and and used a Python Flask API that accessed a PostgreSQL Database for the backend. 

## Project Structure

All of the database is in the [db](/db/) folder and all of the API and HTML code is in the [app](/app/) folder

## Installing the Current Code

1. Fork this repo by clicking the small 'Fork' button at the very top right on Gitlab.
   Name your forked repo as you prefer.
2. In your newly forked repo, find the blue "Clone" button.
   Copy the "Clone with SSH" text.
   In your terminal on your device, you can now issue the command `git clone THE_TEXT_YOU_JUST_COPIED`.
   Make sure to replace 'THE_TEXT_YOU_JUST_COPIED' with the "Clone with SSH" text.
3. In your VM, change into the repository directory and then run `./install.sh`.
   This will install a bunch of things, set up an important file called `.flashenv`, and creates a simple PostgreSQL database named `amazon`.

## Running/Stopping the Website

To run your website, in your VM, go into the repository directory and issue the following commands:
```
source env/bin/activate
flask run
```
The first command will activate a specialized Python environment for running Flask.
While the environment is activated, you should see a `(env)` prefix in the command prompt in your VM shell.
You should only run Flask while inside this environment; otherwise it will produce an error.

An example website will be avaliable at [http://152.3.65.85:5000/](http://152.3.65.85:5000/)

To stop your website, simply press <kbd>Ctrl</kbd><kbd>C</kbd> in the VM shell where flask is running.
You can then deactivate the environment using
```
deactiviate
```

## Working with the Database

Your Flask server interacts with a PostgreSQL database called `amazon` behind the scene.
As part of the installation procedure above, this database has been created automatically for you.
You can access the database directly by running the command `psql amazon` in your VM.

For debugging, you can access the database while the Flask server is running.
We recommend you open a second shell on your VM to run `psql amazon`.
After you perform some action on the website, you run a query inside `psql` to see the action has the intended effect on the database.

The `db/` subdirectory of this repository contains files useful for (re-)initializing the database if needed.
To (re-)initialize the database, first make sure that you are NOT running your Flask server or any `psql` sessions; then, from your repository directory, run `db/setup.sh`.
* You will see lots of text flying by---make sure you go through them carefully and verify there was no errors.
  Any error in (re-)initializing the database will cause your Flask server to fail, so make sure you fix them.
* If you get `ERROR:  database "amazon" is being accessed by other users`, that means you likely have Flask or another `psql` still running; terminate them and re-run `db/setup.sh`.
  If you cannot seem to find where you are running them, a sure way to get rid of them is to restart your VM.

To change the database schema, modify `db/create.sql` and `db/load.sql` as needed.
Make sure you to run `db/setup.sh` to reflect the changes.

Under `db/data/`, you will find CSV files that `db/load.sql` uses to initialize the database contents when you run `db/setup.sh`.
Under `db/generated/`, you will find alternate CSV files that will be used to initialize a bigger database instance when you run `db/setup.sh generated`; these files are automatically generated by running a script (which you can re-run by going inside `db/data/generated/` and running `python gen.py`.
* Note that PostgreSQL does NOT store data inside these CSV files; it store data on disk files using an efficient, binary format.
  In other words, if you change your database contents through your website or through `psql`, you will NOT see these changes reflected in these CSV files (but you can see them through `psql amazon`).
* For safety, a database should never store password in plain text; instead it stores one-way hash of the password.
  This rule applies to the password value in the CSV files too.
  To see what hashed password value you should put in a CSV file, see `db/data/gen.py` for example of how compute the hashed value.

## Note on Hiding Credentials

Use the file `.flaskenv` for passwords/secret keys---we are talking about passwords used to access your database server, for example (not user passwords for your website in CSV files described earlier).
This file is NOT tracked by git and it was automatically generated when you first ran `./install.sh` (from a template file).
You can change any credentials in this file.
Only share the contents of this file securely with your teammates, but don't check it into git because your credentials would be exposed to everybody on gitlab if you are not careful.
You can generate strong passwords with this tool: https://www.lastpass.com/password-generator

