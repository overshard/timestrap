### Windows

The easiest way to develop on Windows now days is using the WSL. We'll let you
figure out how to get that setup for your machine however once it is installed
most of the instructions are the exact same as the Ubuntu install instructions
after that with the exception of Google Chrome and Chromedriver.

Download and install the latest version of Google Chrome Beta and Chromedriver.
put the Chromedriver in a reasonable location, I tend to put apps that don't
come with an installer in `%LOCALAPPDATA%`. For Chromedriver I copied
`chromedriver.exe` into `%LOCALAPPDATA%\chromedriver\`.

Open up Bash on Ubuntu on Windows and run the following to make chromedriver
accessible to our tests:

    sudo mkdir -p /usr/local/bin/ && cd /usr/local/bin/
    sudo ln -s /c/mnt/Users/<YOUR USERNAME HERE>/AppData/Local/chromedriver/chromedriver.exe chromedriver

Continue on to the Ubuntu instructions to finish up and ignore the Chrome and
Chromedriver installation there.
