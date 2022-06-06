# ExpiredHumans

**How to build the app**

1. open CMD prompt as administrator

2. type "wsl --install -d ubuntu"

3. restart computer

4. open wsl (search wsl in taskbar)

5. type "sudo apu update"

6. type "sudo apt install python3.8"

7. type "sudo apt install python3-pip"

8. type "pip3 install --user --upgrade buildozer"

9. type "sudo apt install -y git zip unzip openjdk-13-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev"

10. type "pip3 install --user --upgrade Cython==0.29.19 virtualenv"

11. type "export PATH=$PATH:~/.local/bin/"

12. type "cd" to change to main directory

13. type "explorer.exe ." to open file explorer in this location

14. copy expired folder and buildozer.spec file downloaded from github to location

15. type "buildozer -v android debug" to begin the building process

**First build may take some time to install dependencies, the built apk can be found in the bin folder. For subsequent builds do the following:**

1. open wsl

2. type "cd"

3. type "buildozer -v android debug"
