#!/usr/bin/env python3
"""
Control the number of motions in the corpus.

.. include:: docs/N-motions.md
"""
from pyriksdagen.args import (
    fetch_parser,
    impute_args,
)
from tqdm import tqdm
import json
import pandas as pd
import re




def main(args):
    d = {}
    for motion in tqdm(args.motions):
        motion = motion.replace("riksdagen-motions/", "")
        data, py, mot_basename = motion.split("/")
        if py not in d:
            d[py] = {"total":0}
        d[py]["total"] += 1
        mot_spl = mot_basename.split("-")
        committee = mot_spl[2]
        if len(mot_spl) == 6:
            chamber = mot_spl[3]
            if chamber == "fk":
                chamber = "första_kammaren"
            elif chamber == "ak":
                chamber = "andra_kammaren"
            else:
                raise ValueError(f"What chamber is {chamber}?")
        else:
            chamber = None
        if committee == '':
            commitee = "general"
        if committee not in d[py]:
            d[py][committee] = 0
        d[py][committee] += 1
        if chamber is not None:
            if chamber not in d[py]:
                d[py][chamber] = 0
            d[py][chamber] += 1
    with open(f"quality/estimates/N-motions/raw-results_{args.version}.json", "w+") as out:
        json.dump(d, out, ensure_ascii=False, indent=4)



if __name__ == '__main__':
    parser = fetch_parser("motions", docstring=__doc__)
    parser.add_argument("-v", "--version", type=str, required=True)
    args = parser.parse_args()
    print(args)
    pat = re.compile(r"v([0-9]+)([.])([0-9]+)([.])([0-9]+)(b|rc)?([0-9]+)?")
    if pat.match(args.version) is None:
        raise ValueError(f"{args.version} is not a valid version number.")
    main(impute_args(args))
