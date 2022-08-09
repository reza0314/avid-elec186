echo 'downloding dependencies...'
sudo apt install ffmpeg fswebcam
pip install opencv-contrib-python
sleep 3
echo 'Downloding and installing files'
wget -q -O robot.zip https://github.com/reza0314/avid-elec186/archive/refs/heads/main.zip
unzip -q robot.zip
cd avid-elec186-main/
sudo cp Robot.desktop /usr/share/applications/
sudo mkdir /usr/share/Robot
sudo cp -r . /usr/share/Robot
sudo rm -rf ../avid-elec186-main
sudo rm ../robot.zip
cd /usr/share/Robot
sudo rm -rf ./.git ./.vscode Robot.desktop
sleep 3
echo 'Done rebooting the raspberry pi ...'
sleep 5
sudo reboot now