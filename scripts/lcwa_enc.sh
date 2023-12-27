
#!/bin/bash


TOKEN_FILE='LCWA'
ENC_KEY=$(head -n 1 $1)

#openssl enc -e -base64 -in "/home/pi/git/speedtest/src/${TOKEN_FILE}.txt" -out "/home/pi/git/speedtest/src/${TOKEN_FILE}.enc" -k "$ENC_KEY"
openssl enc -e -base64 -in "/Users/klein/git/speedtest/src/${TOKEN_FILE}.txt" -out "/Users/klein/git/speedtest/src/${TOKEN_FILE}.enc" -k "$ENC_KEY"

