sudo apt install --force-yes python3-matplotlib
sudo apt install --force-yes python3-dropbox

sudo apt install  --force-yes python3-loguru
sudo apt install  --force-yes python3-pandas
sudo apt install  --force-yes python3-iperf3



sudo rm /usr/lib/python3.11/EXTERNALLY-MANAGED

curl -O  https://install.speedtest.net/app/cli/ookla-speedtest-1.2.0-linux-armel.tgz
tar -zxf ookla-speedtest-1.2.0-linux-armel.tgz
sudo mv speedtest /usr/bin/speedtest
speedtest
