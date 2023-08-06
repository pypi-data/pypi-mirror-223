"""Send greetings"""
import sys

def greet(tz):
    return "Hello! It's " + tz + " now."

def cli(args=None):
    """"Process command line arguments"""
    if not args:
        args = sys.argv[1:]
    tz = args[0]
    print(greet(tz))