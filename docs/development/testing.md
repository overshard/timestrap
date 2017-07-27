## Testing

Timestrap uses Selenium (usually with Chromedriver) for frontend testing. See 
[Development Requirements](../development/requirements) for more details on
how to install Chromedriver.

100% coverage is the goal, so any new code should include relevant tests and
pass existing tests. The following command can be used to run all tests:

    python manage.py test
    
Individual package tests can also be run by specifying the path to package:

    python manage.py test api.tests
    
The above command will only run the tests in `api/tests.py`.

Also, a single tests can be run by specifying the full package path, including
the test case class name:

    python manage.py test core.tests.tests_selenium.SeleniumTestCase.test_clients_change
    
The above command will only run the `test_clients_change` in 
`core/tests/tests_selenium`.
    
### Gulp

Gulp is a useful (but *optional*) tool to assist with development. See 
[Development Installation](../installation/development) and 
[Gulp Command Reference](../development/gulp) for more information on using 
Gulp.

To run all tests and produce a coverage report, run:

    gulp test

### Linting

Python, SASS and JavScript (ES6) should also be linted for any code changes. 
Linting requires Gulp and can be run using the following command:

    gulp lint
    
Tests **and** linting must pass in CI for all pull requests!

### Sauce Labs

In order to run Selenium tests in a consistent environment, this project makes
use of [SauceLabs](https://saucelabs.com/) for browser testing. To run tests on
SauceLabs, you will need to first create an account. Once you have your 
username and access key, follow the steps below:

Install the [Sauce Connect Proxy](https://wiki.saucelabs.com/display/DOCS/Sauce+Connect+Proxy):

    wget https://saucelabs.com/downloads/sc-4.4.8-linux.tar.gz
    tar zxf sc-4.4.8-linux.tar.gz
    mv sc-4.4.8-linux/bin/sc /usr/local/bin

From within the virtual environment:

    pip install sauceclient
    export SAUCE_USERNAME=[YOUR USERNAME]
    export SAUCE_ACCESS_KEY=[YOUR ACCESS KEY]
    sc &

After "Sauce Connect is up, you may start your tests."

    python manage.py test
