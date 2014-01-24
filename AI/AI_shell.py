import sys

from subprocess import Popen, PIPE, STDOUT

p = Popen(['grep', 'f'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)

grep_stdout = p.communicate(input='one\ntwo\nthree\nfour\nfive\nsix\n')[0]
print grep_stdout

#p = Popen(['python', 'prog.py'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
#p.stdout.readline().rstrip()
#p.communicate('mike')[0].rstrip()
