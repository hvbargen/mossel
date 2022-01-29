# mossel
Experimental command line shell

## Meaning and Pronounciation

I thought about a different word for shell and thought of German "Muschel", but thought that might be difficult to pronounce and write for others.
Then the Dutch word "mossel" came to my mind. Only later I found that the English word "mussle" has the same meaning (I only knew the words "shell" and "conch" with a similar meaning.
Often, the word means a particular kind of shell: A black, edible clam that can be found all along the coast of the North Sea.

The proncounciation is similar to "mussle", just with an "o" instead of "u".

## Goals

### Special goals

* Secure password caching
* Security by explicit listing of supported commands

### Other goals

* Scriptable, just like other shells (Bash, CMD, PowerShell)
* Should work on Windows and Linux
* Expects a concole with suppport for ANSI colors and cursor movement and makes use of these features
* Support for Unicode symbols including those from beyond the BMP, e.g. emojis.
* Support for auto-completion, for commands as well as for parameters.
* History

## Why not use ...?

### PowerShell

Well, it is just for fun.
And while I like some ideas of the PowerShell, I'm just not used to it, and I don't like those long command and parameter names.

### Extensions to CMD

I tried some of them, but was not satisfied.
If just CMD supported auto-completion for commands as well, then maybe I hadn't even thought about writing a custom shell.

## Why not create a GUI or a GUI-like TUI?

TUI = Text-based user-interface

Some newer TUI projects are very impressive.
The main reason is that I want everything to be scriptable.

## Background

For daily work in my company, I created a shell called "LISH". This was written in a mixture of CMD scripts and Python scripts.
Often, a CMD script was just a super-thin wrapper for a Python script with the same name.
I also developed a command-line utility for password caching.
I am quite happy with that solution, as it saves me a lot of work very day. However, it had some drawbacks:

* No auto-completion (except for file name arguments, as usual in CMD).
* The password caching mechanism is not as secure as it should be.
* I used .cmd scripts with SET commands for storing project-specific configuration. This is not as secure as it should be.
* Long-running scripts need extra-care if they use the password caching mechanism.

## Secure password caching

Shells are made for developers.
Developers often need credentials to access resources like databases, source repositories, wikis, you name it.
And of course developers are writing and using scripts or other command-line programs to do their work,
so these scripts/programs need to know the credentials.

This led to the bad situation that some lazy developers used to *store credentials directly in scripts or in configuration files*.

**This must be strictly avoided.**

But is should still be easy to write a script which e.g. connects to a database with username/password.
However, if you call that script several times, you don't want to enter the same data again and again.

Of course there are credential stores like KeyPass etc and other programs for storing passwords (GUI based or CLI).
However, I have not found any program that seems to support scripting.

So what we want is a program (let's call it cred-cache) with the following features:

* It does not store credentials anywhere in the file system (not even in a "wallet" or "key-cloak" file which is itself encrypted and needs a password).
* A shell script can ask for the credentials for a named resource.
* The cred-cache prompts the user for the credentials on the command line, if the credentials are not yet cached.
* If the credentials are cached, the user will not be prompted.
* The cache expires automatically after some time.
* The cache-expiring properties of credentials are configurable.
* The whole cache can be purged if the display is locked.
* Depending on the technical possibilities, the credentials shall not be visible on the command-line or the environment.
