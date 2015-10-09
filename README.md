# Ircbot

In this repository, you will find:

* Updates to Joel Rosdahl's work
* Simple implementation of ircbots.

## Updates:

* Portability for python 3
* Portability for Windows and Mac OS
* New functionalities:
    - prompt commands



To add functionalities:

You need to add new functions in Irclib in the class `SimpleIRCClient`

in this class, there is a method named dispatcher that parse all events.
```
def _dispatcher(self, c, e):
    """[Internal]"""
    m = "on_" + e.eventtype()
```

there is also a list of events a little bit further:

`protocol_events` so you can add any protocol you want.

Next step, on_prompt command.

## On_prompt:

    This command will listen on the launching terminal any command or message given by the user.


# chanbot
