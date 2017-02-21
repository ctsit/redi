# So you didn't get the report? #

## Steps to debug ##

#### 1 check config.ini ####
If the email setting is False then it wont have emailed, the run may have worked.

#### 2 check for reports ####
Go to the project root. Run `ls -alh`. See when things were modified. Check to see if there are new files added or changed a little after the run should have run.

#### 3 Check the cron.d ####
Go and look at the files in `/etc/cron.d`. See if the command is scheduled to run at the time you think. 

#### 4 Check mail ####
When cron jobs error they send a local mail to the root user. I believe that this is forwarded to the redi user. If you have mail then you have information about runs that ran. Check your mails

