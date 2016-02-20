#!/usr/bin/python

import csv
import sys
import os
import requests


def send_email_message(to_address, url, student_name):
    html = ""
    if url is None:
        html = "<html><h3>Hello %s</h3>" \
               "<p>Error in creating a git repo.</p>" \
               "<p>Your public key did not meet the requirements." \
               " Please fill the form again or reply to this email.</p>" \
               "</html>" % (student_name)
    else:
        html = "<html><h3>Hello %s</h3>" \
               "<p>We have created a git repo for you.</p>" \
               "<p>You can clone your repo from the following URL: %s</p>" \
               "<p>Tweet @nag_kumar if you have any questions.</p></html>" % (student_name, url)
    return requests.post(
            "https://api.mailgun.net/v3/mailgun.nagkumar.com/messages",
            auth=("api", "<api key from mailgun>"),
            data={"from": "CMPE 273 TA <nagkumar.arkalgud@sjsu.edu>",
                  "to": to_address,
                  "subject": "Important information about assignment/lab submission CMPE 273",
                  "text": "Information about assignment/lab submission CMPE 273",
                  "html": html})


def write(filename, content):
    with open(filename, 'w') as g:
        g.write(content)


with open(sys.argv[1], 'r') as csvfile:
    r = csv.DictReader(csvfile)
    for row in r:
        print type(row)
        student_name = row['Your full name']
        student_id = row['SJSU ID']
        student_key = row['Public key']
        student_email = row['Email ID']
        if student_key.startswith("ssh"):
            git_repo_name = "%s_%s" % (student_name.strip().replace(" ", "_").lower(), student_id)
            move_to_git_folder = "cd gitolite-admin"
            try:
                os.chdir("gitolite-admin")
            except OSError:
                pass
            os.system("pwd")
            file_name = "keydir/%s.pub" % git_repo_name
            write(file_name, student_key)
            os.system("ls -l keydir")
            git_add_repo_line1 = "repo    %s" % git_repo_name
            git_add_repo_line2 = "    RW    =    %s" % git_repo_name
            with open("conf/gitolite.conf", "a") as git_file:
                git_file.write(git_add_repo_line1)
                git_file.write("\n")
                git_file.close()
            with open("conf/gitolite.conf", "a") as git_file:
                git_file.write(git_add_repo_line2)
                git_file.write("\n")
                git_file.write("\n")
                git_file.close()

            git_add_command = "git add ."
            git_add_repo_command = 'git commit -am "Created %s repo."' % student_name
            git_push_command = "git push"

            os.system(git_add_command)
            os.system(git_add_repo_command)
            os.system(git_push_command)
            git_repo_url = "git@git.nagkumar.com:%s" % git_repo_name

            send_email_message(student_email, git_repo_url, student_name)
        else:
            send_email_message(student_email, None, student_name)

            # cmd = "ls -l " + sys.argv[1]
            # os.system(cmd)
