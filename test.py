from subprocess import Popen, PIPE, STDOUT

p = Popen(['th', 'gameStateQ.lua'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)    
grep_stdout = p.communicate(input='one\ntwo\nthree\nfour\nfive\nsix\n')[0]
print(grep_stdout.decode())