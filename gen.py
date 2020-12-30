#!/usr/bin/env python

"""
matrix:
 include:
 - name: 1.2-apache
   os: ubuntu-latest
   tags:
   - 1.2
   - 1.2-apache
   context: apache/1.2
 - name: 1.3-apache
   os: ubuntu-latest
   tags:
   - 1.3
   - 1.3-apache
   - latest
   context: apache/1.3
"""

import glob
import json
from distutils.version import StrictVersion
from pprint import pprint

dockerfiles = glob.glob("*/*/Dockerfile")
l = []
for df in dockerfiles:
  variant,version,_ = df.split('/')
  l.append({
    'version': version,
    'variant': variant,
    'file': df,
    })

l.sort(key=lambda f: StrictVersion(f['version']))
latest = l[-1]['version']
print("latest is %s" % (latest,))
pprint(l)
strategy = {
  "max-parallel": 1,
  "fail-fast": False,
  "matrix": {
    "include": [],
    }}
for im in l[:2]:
  tags = []
  if im['variant'] == "apache":
    tags.append(im['version'])
    if im['version'] == latest:
      tags.append("latest")
      tags.append("apache")
  else:
    tags.append("%s-%s" % (im['version'], im['variant']))
    if im['version'] == latest:
      tags.append(im['variant'])

  strategy['matrix']['include'].append(
    {
      "name": "%s-%s" % (im['version'], im['variant']),
      "os": "ubuntu-latest",
      "tags:": ",".join(map(lambda x: "darknao/dotclear:%s" % (x,), tags)),
      "context": "%s/%s" % (im['variant'], im['version']),
      "dockerfile": im['file'],
      })

pprint(strategy)
print("::set-output name=strategy::%s" % (json.dumps(strategy),))
