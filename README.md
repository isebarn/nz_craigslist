# Bot to crawl craigslist

# Prerequisite for running the bot

### Libraries
Run
`pip install -r requirements.txt`

### Postgres
[Instructions here](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04)

Can also be set up with docker

### crontab
crontab runs scripts automatically on set times
So if you have a script `script.py`

you can run
`crontab -e`

That will open an editor (or ask you what editor to use) and it will have instructions

The complete crontab for the system would be
`0 0 * * * root /usr/bin/python run.py GetAdList False`
`0 1 * * * root /usr/bin/python run.py GetAdData False YOUR_EMAIL YOUR_EMAIL_PASSWORD`
`0 22 * * * root /usr/bin/python run.py SendEmails False YOUR_EMAIL YOUR_EMAIL_PASSWORD`

# Email sender

### Prerequisite
The email account that will be used must be enabled 
[Here are the instructions](https://stackoverflow.com/a/27515883/4551168)

### Send emails

To send emails to all saved ads, go to the directory of the `run.py` script and run the following command:

`python3 run.py SendEmails False YOUR_EMAIL YOUR_EMAIL_PASSWORD`

To send a test email for a random ad from yourself to yourself run

`python3 run.py SendEmails True YOUR_EMAIL YOUR_EMAIL_PASSWORD`

# Search for ads
To scan for ads on all sub-craigslist sites, go to the directory of the `run.py` script and run the following command

`python3 run.py GetAdList False`
Note that this script may run for **HOURS**, or at least several minutes

### Testing
To do a trial run, run **inside postgres**
`select count(*) from ads;`
To view the count of ads

Then run from the usual place
`python3 run.py GetAdList True`
This wont take long, and you can run the following command a few times. Running the script with the `True` parameter will run a random keyword on a random sub-craigslist page

Then again, run
`select count(*) from ads;`
To see if the count of ads has increased. 
**Note**: You might need to run the `run.py` script a few times because sometimes ads that fulfill the conditions so it wont find any ads.


# Read ads
To read all unread ads, go to the directory of the `run.py` script and run the following command
`python3 run.py GetAdData False`
**Note**: This will definetally run for hours or maybe even **DAYS**

### Testing
Run the following `postgres` command

`select count(*) from ads where Email is null;`
That will return some number, fx 200

Then run

`python3 run.py GetAdData True`
It will take a few moments

Then run again
`select count(*) from ads where Email is null;`
That will return a number 1 smaller than before, 199