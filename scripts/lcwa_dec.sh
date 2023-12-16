
#!/bin/bash


TOKEN_FILE='LCWA'
ENC_KEY=$(head -n 1 $1)

openssl enc -d -base64 -in "/home/pi/git/speedtest/src/${TOKEN_FILE}.enc" -out "/home/pi/git/speedtest/src/${TOKEN_FILE}_a.txt" -k "$ENC_KEY"
#openssl enc -d -base64 -in "/home/klein/git/speedtest/src/${TOKEN_FILE}.enc" -out "/home/klein/git/speedtest/src/${TOKEN_FILE}_a.txt" -k "$ENC_KEY"
#openssl enc -d -base64 -in "/Users/klein/git/speedtest/src/${TOKEN_FILE}.enc" -out "/Users/klein/git/speedtest/src/${TOKEN_FILE}_a.txt" -k "$ENC_KEY"

