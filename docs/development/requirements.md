## Development Requirements

Some extra stuff is needed...

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

### Ubuntu

You can install everything you need from apt, which is just virtualenv:

    sudo apt install python-virtualenv

If you are doing front-end development you also need NPM and Node.js:

    sudo apt install npm

If you want to run tests you will need to install some additional packages,
these are not required though and if you are working on small changes or
documentation then you can rely on Travis CI to run tests for you.

We've found that google-chrome-beta (Chrome 59+) is best for testing since they
have added a ton of improvements that allow for things like headless testing. We
originally used geckodriver and Firefox but Chrome finished all our tests in a
fraction of the time. So to install Chrome on Ubuntu follow the steps below.

    curl -L https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main"
    sudo apt update
    sudo apt install google-chrome-beta
    curl -L https://chromedriver.storage.googleapis.com/2.29/chromedriver_linux64.zip -o chromedriver.zip
    sudo mkdir -p /usr/local/bin/
    sudo unzip chromedriver.zip -d /usr/local/bin/
    sudo chmod +x /usr/local/bin/chromedriver
    echo "GOOGLE_CHROME_BINARY=/usr/bin/google-chrome-beta" >> ~/.bashrc

Go to the top of Installation and make sure you have virtualenv and npm all set
then continue to running and testing.

### OS X

Homebrew, get it if you don't have it and run:

    brew install node python

Make sure you have virtualenv installed after this with:

    pip install virtualenv

If you want to test with selenium install the latest Google Chrome Beta and run:

    brew install chromedriver

Go to the top of Installation and make sure you have virtualenv and npm all set
then continue to running and testing.
