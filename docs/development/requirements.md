## Development Requirements

General development requirements are fairly simple:

- Python
- Pipenv

For frontend development, a few extra tools are needed:

- NPM
- Gulp
- Chromedriver/geckodriver

### Windows

#### WSL

The [Windows Subsystem for Linux](https://blogs.msdn.microsoft.com/wsl/) is 
probably the easiest way to get started, but Windows-native tools can work
as well. With WSL, it is pretty easy to follow along with the Ubuntu 
instructions below. The one big difference is Google Chrome and Chromedriver.

Download and install the latest version of Google Chrome Beta and Chromedriver.
put the Chromedriver in a reasonable location (perhaps `%LOCALAPPDATA%`). For 
Chromedriver, this simply means copy `chromedriver.exe` into 
`%LOCALAPPDATA%\chromedriver\`.

Open up Bash on Ubuntu on Windows and run the following to make Chromedriver
accessible for tests:

    sudo mkdir -p /usr/local/bin/ && cd /usr/local/bin/
    sudo ln -s /c/mnt/Users/<YOUR USERNAME HERE>/AppData/Local/chromedriver/chromedriver.exe chromedriver

Continue on to the Ubuntu instructions to finish up and ignore the Chrome and
Chromedriver installation there.

#### Native

For native Windows, install:

- [Python for Windows](https://www.python.org/downloads/windows/)
- [Node for Windows](https://nodejs.org/en/download/) (includes NPM)

With these tools and some environment configuration, Windows native development
should be just as smooth as WSL. A suggested method for using Chromedriver:

1. Install [Chrome Beta](https://www.google.com/chrome/browser/beta.html)
1. Download [ChromeDriver for Windows](https://sites.google.com/a/chromium.org/chromedriver/downloads)
1. Create a folder `bin` in `%USERPROFILE%`.
1. Unzip and copy `chromedriver.exe` to `%USERPROFILE%\bin`.
1. Add `%USERPROFILE%\bin` to you `PATH`.

With this configuration, the `chromedriver` command should be available so 
Timestrap's tests will be able to run.

### Ubuntu

You can install everything you need from pip, which is just pipenv:

    pip instal pipenv
    cd /path/to/timestrap
    pipenv install

If you are doing frontend development you also need NPM and Node.js:

    sudo apt install npm
    npm install -g gulp-cli
    cd /path/to/timestrap
    npm install

If you want to run tests you will need to install some additional packages,
these are not required and if you are working on small changes or documentation
you can rely on Travis CI to run tests for you.

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

### OS X

Download and install [Homebrew](https://brew.sh/) for OS X if you don't already
have it.

Install Node and Python:

    brew install node python

Make sure you have pipenv installed after this with:

    pip install pipenv
    cd /path/to/timestrap
    pipenv install

If you want to test with Selenium, install the latest Google Chrome Beta:

    brew install chromedriver
