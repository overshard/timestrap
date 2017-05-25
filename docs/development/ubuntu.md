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
