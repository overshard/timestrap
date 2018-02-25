## Development Requirements

General development requirements are fairly simple:

- Python
- pipenv

For frontend development, a few extra tools are needed:

- npm
- gulp
- geckodriver


### Windows

#### WSL

The [Windows Subsystem for Linux](https://blogs.msdn.microsoft.com/wsl/) is
probably the easiest way to get started, but Windows-native tools can work
as well. With WSL, it is pretty easy to follow along with the Ubuntu
instructions below. The one big difference is Firefox and geckodriver.

Download and install the latest version of Firefox and geckodriver.
put the geckodriver in a reasonable location (perhaps `%LOCALAPPDATA%`). For
geckodriver, this simply means copy `geckodriver.exe` into
`%LOCALAPPDATA%\geckodriver\`.

Open up Bash on Ubuntu on Windows and run the following to make Chromedriver
accessible for tests:

    sudo mkdir -p /usr/local/bin/ && cd /usr/local/bin/
    sudo ln -s /c/mnt/Users/<YOUR USERNAME HERE>/AppData/Local/geckodriver/geckodriver.exe geckodriver

Continue on to the Ubuntu instructions to finish up and ignore the Chrome and
Chromedriver installation there.

#### Native

For native Windows, install:

- [Python for Windows](https://www.python.org/downloads/windows/)
- [Node for Windows](https://nodejs.org/en/download/) (includes NPM)

With these tools and some environment configuration, Windows native development
should be just as smooth as WSL. A suggested method for using geckodriver:

1. Install [Firefox](https://www.mozilla.org/en-US/firefox/)
1. Download [geckodriver for Windows](https://github.com/mozilla/geckodriver/releases)
1. Create a folder `bin` in `%USERPROFILE%`.
1. Uncompress and copy `geckodriver.exe` to `%USERPROFILE%\bin`.
1. Add `%USERPROFILE%\bin` to your `PATH`.

With this configuration, the `geckodriver` command should be available so
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

We've found that Firefox is best for testing since they have added a ton of
improvements that allow for things like headless testing.

    sudo apt update
    sudo apt install firefox
    curl -L https://github.com/mozilla/geckodriver/releases/download/v0.19.1/geckodriver-v0.19.1-linux64.tar.gz -o geckodriver.tar.gz
    sudo mkdir -p /usr/local/bin/
    sudo tar zxvf geckodriver.tar.gz -C /usr/local/bin/
    sudo chmod +x /usr/local/bin/geckodriver


### OS X

Download and install [Homebrew](https://brew.sh/) for OS X if you don't already
have it.

Install Node and Python:

    brew install node python

Make sure you have pipenv installed after this with:

    pip install pipenv
    cd /path/to/timestrap
    pipenv install

If you want to test with Selenium, install the latest Firefox and geckodriver:

    brew install geckodriver
