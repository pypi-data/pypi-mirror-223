#!/usr/bin/env python3

from prody import parsePDB
import sys


pdb_file = sys.argv[1]
molecule = parsePDB(pdb_file)

selection = molecule.select("within 5 of (chain A and resnum 9 or chain C and resnum 9) and surface")
for a in selection:
    print(f"{a.getChid()}.{a.getResname()}.{a.getResnum()} {a.getName()}")
