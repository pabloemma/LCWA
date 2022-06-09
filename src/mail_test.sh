#!/bin/bash
subject="$2"
for I in `cat /home/klein/private/LCWA/recipient_list1.txt`; do cat $3 | mutt  -a $1 -s $2 -- $I < $3; echo $I; sleep 3; done
