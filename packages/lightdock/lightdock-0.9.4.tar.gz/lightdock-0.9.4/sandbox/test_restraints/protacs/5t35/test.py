#!/usr/bin/env python3

from prody import parsePDB
import sys


pdb_file = sys.argv[1]
molecule = parsePDB(pdb_file)

selection = molecule.select("within 10 of (chain D and resnum 301 or chain D and resnum 69) and surface or (chain D and resnum 301 or chain D and resnum 69)")
for a in selection:
    print(f"{a.getChid()}.{a.getResname()}.{a.getResnum()} {a.getName()}")
