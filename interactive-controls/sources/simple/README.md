# Simple User Interaction Chaos Toolkit Extension

This module adds a control that can be used as a simple "Press And Key to Continue" 
Chaos Toolkit control to prompt for user interaction during an experiment's 
execution.

### Development

If you wish to develop this project, make sure to install the development
dependencies. But first, [create a virtual environment][venv] and then install
those dependencies.

[venv]: http://chaostoolkit.org/reference/usage/install/#create-a-virtual-environment

```bash
$ pip install -e . 
```

Then, point your environment to this directory:

```bash
$ python setup.py develop
```

Now, you can edit the files and they will be automatically be seen by your
environment, even when running from the `chaos` command locally.

### Test

To run the tests for the project execute the following:

```
$ python setup.py test
```