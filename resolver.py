import re
import argparse
from tree2 import Tree, get_index
from tree3 import process_string
from algorithm import resolve_anaphor
import json

gold_data = {}
lexicon = {}
head_settings = {}

def compute_corenlp_accuracy():
    pass

def read_gold_data():
    pass

def look_for_PRP(cell):
    if cell is None:
        return []
    unresolved = []
    if cell.tag().startswith('PRP'):
        unresolved.append((cell, lexicon.get(cell.get_string())))
    if cell.is_leaf():
        return unresolved
    return unresolved + look_for_PRP(cell.get_left()) + look_for_PRP(cell.get_right())

def main(args):
    global lexicon
    with open(args.config_file) as c:
        params = json.load(c)
    lexicon = params[args.language]['lexicon']

    with open(args.sentences) as s:
        parser_output = json.load(s)

    for sentence in sorted(parser_output["sentences"], key=lambda x: x["index"]):
        list_hier = process_string(sentence["parse"])
        tree_to_parse = Tree(list_hier[0])
        print tree_to_parse.get_string()
        candidates = look_for_PRP(tree_to_parse)

        for candidate, conf in candidates:
            proposed = resolve_anaphor(candidate)
            print 'Proposed antecedents for', candidate.get_string()

            print 'Are as follows: '
            if proposed is None:
                continue
            for proposal in proposed:
                proposal.pretty_print()
        print '-'*20


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s",
                        "--sentences",
                        default="binding_dataset.deterministic.json",
                        help="CoreNLP output containing sentences")

    parser.add_argument("-g",
                        "--gold_data",
                        default="gold_data.json",
                        help="Gold data for binding using CoreNLP indexing scheme")

    parser.add_argument("-l",
                       "--language",
                        default="eng",
                        help="Specify 'eng' for English, 'ger' for German")

    parser.add_argument("-c",
                        "--config_file",
                        default="config.json",
                        help="json input for parameter settings. Should not need anything other than the default!")

    args = parser.parse_args()
    main(args)
