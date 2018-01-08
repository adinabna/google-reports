# Google Reports

An introductory application on how to generate Google Spreadsheets using Google Service Accounts.

## Synopsis

_**For the following commands to work, do the Requirements section first if it's your first time running this.**_

Before running this application, you will need to create a Service Account (an account that belongs to your application instead of to an individual end user) and enable the Google Drive API and the Sheets API for your project. You can do this via the following page [Google Developers Console](https://console.developers.google.com/projectselector/apis/api?organizationId=590846829574). Follow the steps explained [defined for _CONSOLE_](https://cloud.google.com/iam/docs/creating-managing-service-accounts).
**REMARKS:**
  Make sure to save the JSON secret key file for the Service Account created.

Run this application like this:

  ```
  python generate_reports.py
  ```

**REMARKS**:
    If you are only running this via a **virtualenv** , make sure to run the **generate_reports.py** script as follows:

    ```
    venv/bin/python generate_reports.py
    ```

## Requirements

For managing dependencies this project uses a _requirements.txt_ file, the _pom_ file of Python.

- Install _pip_ using the following command:

```
sudo easy_install pip
```

- Use the _requirements.txt_ file **to install all dependencies** by calling the following command **from within the root of the project**:

```
pip install -r requirements.txt
```

This will install among others, these main dependencies:
http://pyyaml.org/ <br />
https://www.pylint.org/ <br />

If you run into any errors, try installing the following:

```
sudo apt-get install python-setuptools
```

**REMARKS**: Make sure to check the _Development Setup_ section of the document if you encounter any issues with the above. And please make sure you follow the steps mentioned in the _Synopsis_ part of this document to finalise the setup for the app and learn how to run it.

## Description

An introductory application on how to generate Google Spreadsheets using Google Service Accounts.

## Errors

All logs will be printed to *stderr*, and thus all the errors will be found there.

## Development Setup

Please install the following in order to run the project and the analysis tool against it:

- [Install pyenv-virtualenv plugin](https://github.com/pyenv/pyenv-virtualenv)

```
  brew install pyenv-virtualenv
```
Please follow all the steps in the Github project link above.

- The analysis tool will run in a virtual environment https://github.com/pyenv/pyenv
Install using the below:

```
  pyenv install 3.4.2
  pyenv virtualenv 3.4.2 google-reports
  pyenv activate google-reports
```

_**This is an extra step before first installing Pylint.**_ <br />
  Change to the root of the project and generate the initial settings file for Pylint using:

  ```
    pylint --generate-rcfile > .pylintrc
  ```

  Disable some of the warnings (e.g. _missing-docstring, bare-except_) by adding _missing-docstring,bare-except_ to the end of the line which starts _disable=_ if you wish to turn that off.

- Install Pylint https://www.pylint.org/:

```
  pip install pylint
```

- Now, while in the root of the project opened from the last used command line, evaluate the code using:

```
  pylint *.py
```
You will see something like this:
`Your code has been rated at 8.60/10`

- For managing dependencies use a _requirements.txt_ file, the _pom_ file of Python.

```
  pip install -r google-reports/requirements.txt
```

- See all dependencies using the following command:

```
  pip freeze
```

Pipe directly all dependencies into the _requirements.txt_ file in a sorted manner using the following command line:

```
  pip freeze | sort > requirements.txt
```

- When inside the virtual env, you need to install dependencies again, otherwise Pylint will complain it cannot import them. Use the _requirements.txt_ file to install all dependencies by calling the following from within the root of the project:

```
pip install -r requirements.txt
```

**REMARKS**:

If you are only running this via a **virtualenv** (which implies also that you are using the global Python installation on that environment), you specify the directory it is installed into: e.g. `virtualenv --python python3 venv` would create a folder called **venv**, which has a **venv/bin/python** in it (plus other stuff too).

You activate this by calling:

```
source venv/bin/activate
```

but if you call `venv/bin/python` directly you don’t need to activate first._
