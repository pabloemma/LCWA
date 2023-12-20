#!/bin/bash
subject="$2"
for I in `cat /home/klein/private/LCWA/recipient_list.txt`; do cat $3 | mutt  -a $1 -s $2 -- $I < $3; echo $I; sleep 3; done
#for I in `cat /Users/klein/private/LCWA/recipient_list_short.txt`; do cat $3 | /usr/local/bin/mutt  -a $1 -s $2 -- $I < $3; echo $I; sleep 3; done
