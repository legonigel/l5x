'''
Created on Nov 3, 2015

@author: "hutcheb"
'''

import unittest, os
import subprocess

print(os.curdir)
filepath=r"E:\Documents\workspace\l5x\l5x\doc\make.bat html"
cwd=r"E:\Documents\workspace\l5x\l5x\doc"
p = subprocess.Popen(filepath, cwd=cwd)
stdout, stderr = p.communicate()
print(filepath)
p = subprocess.Popen(filepath, shell=True, stdout = subprocess.PIPE)
stdout, stderr = p.communicate()

loader = unittest.TestLoader()
ts = loader.discover('./tests', pattern='*test.py')
tr = unittest.runner.TextTestRunner(verbosity=10)
tr.run(ts)
