# Site connectivity checker (scc) (windonws only)

> A shell aplication that checks or monitors website availability

If a website is unavailable you can tell scc to monitor it <br>
When it becomes available scc will send a notification

## Installation

* navigate to your directory

```
> cd path\to\your\directory
```

* make a python virtual environment

```
> python -m venv venv
```

* activate the virtual environment

```
> venv\Scripts\activate.bat
```

* install app dependencies

```
(venv) > pip install click click-shell win10toast requests
```

* in setup.py you can specify what you want your shell command to be by changing
`scc=scc:cli` to `yourCommandName=scc:cli`

```
entry_points='''
        [console_scripts]
        scc=scc:cli
    ''',
```

* setup shell command

```
(venv) > pip install --editable .
```

* finally add your directory to windows enviroment variables (PATH)
