# Python project stub

This repo contains stub files that can be used to create a Python project
that is able to be packaged and uploaded to the Python Package Index and
hence can be installed with `pip install my-project-name`.
This README describes how to modify the stubs and use them as the base of
a new Python project.
(The requirements in order to follow the steps below
are a recent installation of Python 3 [>= 3.8] on Linux.)

## Contents

* <a href='#choose-a-project-name'>Choose a project name</a>

* <a href='#create-a-github-repo'>Create a GitHub repo</a>

* <a href='#build-the-package'>Build the package</a>

* <a href='#upload-the-package-to-pypi-test'>Upload the package to PyPI test</a>

* <a href='#upload-the-package-to-the-real-pypi'>Upload the package to the real PyPI</a>

* <a href='#further-reading'>Further reading</a>

<h2 id='choose-a-project-name'>Choose a project name</h2>

First, clone this repository by typing the following at a Linux shell
```sh
$ git clone git@github.com:striebel/python-project-stub.git
```
This creates the directory `python-project-stub` in the current
working directory.
Rename this directory to the name of your project with
```sh
$ mv python-project-stub my-project-name
```
Before choosing a project name, check if the name has been taken
yet by visiting
```
https://pypi.org/project/my-project-name
```
If you get a 404 error, then the name you want hasn't been taken.
Also search your project name from the PyPI search bar on the homepage,
because if there is another project with a name that is only a character or two
different from your desired name, your name will likely be rejected
when you try to upload your package.

After you choose a project name,
`cd` into the repo root dir and remove the existing git repo itself,
since you are going to create a new repo for your project:
```sh
$ cd my-project-name
$ rm -rf .git
```
Next open `pyproject.toml` in a text editor:
change the project name field value
from `python-project-stub` to `my-project-name`.
Also update the author name, the project description, and homepage fields.

After saving `pyproject.toml` with these changes,
rename the adjacent source code directory (`python_project_stub`)
to agree with the new project's name.
For example, execute
```sh
$ mv python_project_stub my_project_name
```

With `my-project-name` still as your working dir, now execute
```sh
$ python -m my_project_name
```
This will produce some output on the terminal.
Open `my_project_name/__main__.py` with a text editor to check
if what was printed on the terminal agrees with what you see
in that file.

<h2 id='create-a-github-repo'>Create a GitHub repo</h2>

Create a GitHub repo corresponding to your new Python project using
GitHub's web interface, and name the new repo `my-project-name`.
In order to use the rest of the instructions below, do not choose any
of the options to automatically add a README,
.gitignore, or license file when creating the repo
(you can add these later).

Now, either rename the existing `README.md` file so that you can continue
to read it locally, or just continue to read it in a web browser at
`https://github.com/striebel/python-project-stub`
(if that's what you have been doing),
because the next step will intentionally replace the current README file.

In the `my-project-name` directory, which should still be the current
working directory, execute
```sh
$ git init
$ git branch --move trunk
$ echo "# My project name" > README.md
$ git add --all
$ git commit --message "initial commit"
```

Now set the new GitHub repo as the remote/origin of the local repo that you just created,
and push your initial commit:
```sh
$ git remote add origin git@github.com:my-github-username/my-project-name.git
$ git push --set-upstream origin trunk
```

In a web browser navigate to
```
https://github.com/my-github-username/my-project-name
```
to see GitHub's web interface to your repo with the initial files
now uploaded.

<h2 id='build-the-package'>Build the package</h2>

First create a Python virtual environment in your local repo dir
```sh
$ python -m venv venv-my-project-name
```

You do not want the virtual environment that you create on any given machine
to be included in your repo's version tracking system,
so in your repo's root dir, create a file named `.gitignore`, and add the line
```
venv*/
```
to the file. Then push this file to your remote repo:
```sh
$ git add .gitignore
$ git commit -m "added .gitignore file"
$ git push origin
```

Next activate the newly created Python virtual environment:
```sh
$ source activate venv-my-project-name/bin/activate
```

Execute the following sequence of commands to build the package
```sh
$ pip install --upgrade pip
$ pip install --upgrade setuptools wheel
$ pip install --upgrade build
$ python -m build
```

Confirm that the package file
`dist/my-project-name-0.0.0.tar.gz` was generated:
```sh
$ ls -l dist
```

<h2 id='upload-the-package-to-pypi-test'>Upload the package to PyPI test</h2>

### Upload the package

First visit
```
https://test.pypi.org
```
and create an account.

Then execute
```sh
$ pip install --upgrade twine
```

Next create a PyPI Test API token
[here](https://test.pypi.org/manage/account/#api-tokens).

Since this is a pure Python package, just upload the source package
(`dist/my-project-name-0.0.0.tar.gz`) -
no need to upload the pre-built wheel
(`dist/my-project-name-0.0.0-py3-none-any.whl`):
```sh
$ python -m twine upload --repository testpypi dist/my-project-name-0.0.0.tar.gz
```
For username enter `__token__` and for the password enter the token value
including the `pypi-` prefix.

### Download and install the package

To confirm that the package was properly uploaded, first
`cd` out of the repo root into, say, your home directory.
Confirm that the package is not installed in the current
virtual environment by executing:
```sh
python -m my_project_name
```
which should produce an error.

Now install the package from the test PyPI with
```sh
$ pip install \
>     --index-url https://test.pypi.org/simple/ \
>     --extra-index-url https://pypi.org/simple/ \
>     my-project-name
```

Then execute
```sh
$ python -m my_project_name
```
and the output should be
```
outside guard
inside guard
```

Now uninstall the package:
```sh
$ pip uninstall my-project-name
```
and confirm again that running
```sh
$ python -m my_project_name
```
now is unsuccessful.

<h2 id='upload-the-package-to-the-real-pypi'>Upload the package to the real PyPI</h2>

### Upload the package

Create an account at `https://pypi.org`.
Then follow the steps in the previous section again, except when doing
the "twine upload," omit `--repository testpypi` so that by default the
real PyPI will be used, i.e.:
```sh
python -m twine upload dist/my-project-name-0.0.0.tar.gz
```

The address to get the API token is exactly the same except omit the
`test` subdomain, like [here](https://pypi.org/manage/account/#api-tokens)

### Download and install the package

Then test by downloading and installing from the real PyPI using `pip`:
```sh
pip install --no-cache-dir my-project-name
```

Confirm that the install worked by executing
```sh
python -m my_project_name
```

<h2 id='further-reading'>Further reading</h2>

* [Python packaging user guide](https://packaging.python.org/en/latest/)
  - [Packaging python projects tutorial](
        https://packaging.python.org/en/latest/tutorials/packaging-projects/
    )
