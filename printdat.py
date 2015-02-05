import sys

#takes a list and prints hex + text
def printdat(data):
  for d in data:
     sys.stdout.write('%02X' % d)
     sys.stdout.write(' ')
  sys.stdout.write('    ')
  for d in data:
    if (d >= 32) and (d <= 126):
      sys.stdout.write(chr(d))
    else:
      sys.stdout.write('.')
  sys.stdout.write('\n')
