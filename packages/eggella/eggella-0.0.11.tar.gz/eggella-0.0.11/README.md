# Eggella
[[ENG]](README.md) [[RU]](README_RU.md)
> [Eggella](https://en.wikipedia.org/wiki/Eggella) is a shield volcano in central Kamchatka. 
> The volcano is located on the west axis of the southern Sredinny Range.

----
## About

Eggella is a framework for easy creating REPL applications. 

Design inspired by [vulcano](https://github.com/dgarana/vulcano), [flask](https://github.com/pallets/flask) 
and various chatbots frameworks and built top on [prompt-toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit)

## Features:

- Python 3.8+ support
- Command line arguments auto cast from function annotations
- Cross-platform. [prompt-toolkit guarantees](https://github.com/prompt-toolkit/python-prompt-toolkit#prompt_toolkit-features)
- FSM (finite state machine) to organize a branch interface system
- Error handlers
- Customized events
- Auto create command suggestions
- Auto generate man page and help command
## Install

```shell
pip install eggella
```

## Hello world
```python
from eggella import Eggella


app = Eggella(__name__)


@app.on_command("hello")
def hello():
    """This my first command!"""
    return "Hello, world!"


if __name__ == '__main__':
    app.loop()
```

![quickstart](docs/gifs/quickstart.gif)

See the [documentation](https://eggella.readthedocs.io/en/latest/) and [examples](examples)!