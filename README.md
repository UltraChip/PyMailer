# PyMailer

## A simple command-line utility to send emails through an SMTP server (such as Gmail).
PyMailer was created to allow an easy way to add email-sending functionality to scripts and programs running on your Linux system. It's designed to work with SMTP email servers and comes pre-configured to work with GMail's SMTP service.

---
## Example use case
Say you have a script to check the status of your server's RAID running at regular intervals via a cron job. The script can pipe its output to PyMailer to automatically send you a warning email when it detects the RAID is degraded.

---
## How To Use
PyMailer can be called with the "pymailer" command and supports the following command line arguments:

-m : The main message content of your email. The message content can be supplied using -m or it can be piped in over stdin:

    pymailer -m "This is an email message."
or

    echo "This is an email message." | pymailer

-s --subject : Specify the subject line for your email. This argument is OPTIONAL; if you don't provide a subject then PyMailer will use the default subject line specified in /etc/pymailer.conf

    pymailer -s "Critical Server Message" -m "RAID-5 is degraded"

-t --to : Specify the recipient for your email. This argument is OPTIONAL; if you don't provide a subject then PyMailer will use the default recipient specified in /etc/pymailer.conf

    cat /var/log/backupscript.log | pymailer -t "sysadmin@example.com"

---
## How To Configure
Configuration of PyMailer is achieved by editing /etc/pymailer.conf. The file is in a JSON-esque format (essentially just JSON + comments). The installer will walk you through building an initial configuration pre-set to work with Gmail, but this can easily be changed by editing the file directly in your text editor of choice.

---
## How To Install
If you're running an APT-based Linux distribution (Debian, Ubuntu, Mint, etc.) then you should be able to just clone this repository and then run ./install.sh (note: script must be run as root or with sudo). The install script will copy files to their appropriate locations and then walk you through several prompts to help you set up an initial configuration file. 

If you are running a distribution that doesn't use APT then you may need to lightly modify the install script so that it works with your package manager.

PyMailer is not supported on Windows at this time. 

---
## Dependencies
- The only hard dependency is Python3. PyMailer is written with only standard libraries so you should not need to install any other modules.

- OPTIONAL: If you have git installed it will make download and installation slightly easier, but it isn't strictly neccessary. 

---
## Security Considerations
BE AWARE that in order for PyMailer to work it must store the password to its email account inside /etc/pymailer.conf. It is **HIGHLY RECOMMENDED** that the email account you choose be dedicated solely to automated service messages and that the password you choose for it be strong and 100% unique. If the email service you are using supports app-specific passwords then it's extremely recommended that you use it!

---
## Known Issues
- If the password to your sending email account happens to contain an ampersand (&) then the install script will not write it to the config file correctly. This can be worked around by opening up /etc/pymailer.conf with a text editor and updating the password manually.