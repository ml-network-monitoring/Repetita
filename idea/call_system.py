import subprocess as sp
import sys

args = ['cat', 'call_system.py']

p = sp.run(args=args,
           stdout=sp.PIPE,
           stderr=sp.PIPE)

print(p.stdout.decode('utf-8'))
