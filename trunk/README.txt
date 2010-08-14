TELFORCE--

This package contains a set of python modules that can be imported or run as
stand-alone scripts.

telforce.py:
This script uses generator.py to generate random passwords.  It attempts
to login using random passwords and a predefined set of usernames.  The user
may define the host to connect to, the file with usernames, the length of
guessed passwords, the number of threads, and the number of times each thread
should attempt to guess the usr/passwd.

generator.py:
This module implements functions for generating random strings containing 
upper and lower case letters, numbers, and symbols.  The random strings are 
of variable length.  The user may specify what types of characters to include.



RUNNING:

    $ python telforce.py -h
Shows the help message.

    $ python telforce.py -o 10.0.1.1 -u usr.txt
Spawns the default 3 threads that try to connect to 10.0.1.1 using the usernames
found in 'usr.txt'.  Each thread tries to guess the default number of times (15)
for every username in 'usr.txt'.
