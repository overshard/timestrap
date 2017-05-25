## Testing

We use selenium with the chromedriver for testing. If you wish to run tests you
will need to make sure you have Chrome installed. For installation instructions
on those see the above documentation

I'm trying to push for 100% code coverage on this project! If you want to add
or change something and test that everything still works you can do so easily
with:

    python manage.py test

If you push code to our primary repository we test for style adherence and code
coverage. If you get a failed build to either of these we won't accept your
code till it's fixed.

### Sauce Labs

In order to run Selenium tests in a consistent environment, this project makes
use of [SauceLabs](https://saucelabs.com/) for browser testing. To run tests on
SauceLabs, you will need to first create an account. Once you have your 
username and access key, follow the steps below:

Install the sc proxy client

    wget https://saucelabs.com/downloads/sc-4.4.6-linux.tar.gz
    tar zxf sc-4.4.6-linux.tar.gz
    mv sc-4.4.6-linux/bin/sc /usr/local/bin

From within the virtual environment

    pip install sauceclient
    export SAUCE_USERNAME=[YOUR USERNAME]
    export SAUCE_ACCESS_KEY=[YOUR ACCESS KEY]
    sc &

After "Sauce Connect is up, you may start your tests."

    python manage.py test
