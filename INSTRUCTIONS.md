## Setup

The first thing to do is to clone this repository on our computer:

```
$ git clone https://github.com/rocammo/scopus-search-api.git
```

> Note: It is necessary to have `git` installed.

After cloning, a folder will be created. Inside it, you need to install virtualenv using the Python (pip) package installer:

```
# macOS
$ pip3 install virtualenv

# Debian, Ubuntu, Fedora
$ sudo pip install virtualenv
```

> Note: It is necessary to have `python3` installed.

To create the virtual environment, simply run the `virtualenv` command as follows:

```
$ virtualenv env --python=python3
```

To activate the virtual environment, run the virtualenv `activate` script installed in the `bin/` directory:

```
$ cd env
$ source bin/activate
(env)$
```

After activating it, all that is missing is to install the necessary packages (requirements.txt) using the pip packages installer:

```
(env)$ pip install -r requirements.txt
```

## Usage

To execute the project, run:

```
$ python main.py
```

The queries are set in code (ref: `main.py`). The filtering is done by means of a quality indicator (criterion) stored in the `quality-indicator.json` file. The results will be saved in JSON format, inside the `results/` folder.
