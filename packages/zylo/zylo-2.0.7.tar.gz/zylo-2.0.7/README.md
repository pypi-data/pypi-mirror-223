# Zylo

Zylo is a lightweight web framework made with love.

## Features

- Simple and intuitive routing
- Template rendering using Jinja2
- Session management with the sessions library
- Static file serving

## Installation

You can install Zylo using pip:


```bash
pip install zylo

```

## Usage

```python

# app.py

from zylo.core.branch import Zylo

app = Zylo()

@app.route('/')
def home(request):
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()
 
```

## changelogs

- Beta version 2.0.7
- Latest update of beta
- Bug fixed with update --> 2.0.7
- Updated Usage Guide 1.2.2
- Newly designed system based on Matrix 1.0.0 Metapolist
- Major Bug fixies in zylo
- No longer support for version 1 beta --> # clearout
- Attractive echosystem in zylo
- Freshly updated Mailer, Blueprint, Sessions, Chiper, JwT, BaseModals, Zylo
- Strict route has been removed in version --> 2.0.7
- Added battries support usign ZyloAdmin 

## Usage Guide

Our team working hard and the usage guide will be avilable within 24hrs on http://zylo.vvfin.in or https://github.com/E491K8/ZyloProject/

## Batteries Support 

Installation of ZyloAdmin v1

```bash
pip install zyloadmin

```

## Create zylo project

```bash
zyloadmin startproject -i {projectName}
```

