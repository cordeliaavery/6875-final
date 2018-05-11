from tree import Tree
from tree2 import Tree as Tree2
from algorithm import resolve_anaphor
import json

vals = {"S": 
        (
            {"NP": "the child"},
            {"VP":
             (
                 {"VBar": 
                  (
                      {"V": "ran"},
                      {"PP": 
                       (
                           {"P": "to"},
                           {"NP": "her"}
                       )
                      }
                  )
                 }
                 ,)
            }
        )
       }

vals2 = ("S",
         (
             ("NP", "the child"),
             (
                 "VP",
                 (
                     (
                         "VBar",
                         (
                             ("V", "ran"),
                             (
                                 "PP",
                                 (
                                     ("P", "to"),
                                     ("NP", "her")
                                 )
                             )
                         )
                     ),
                 )
             )
         )
       )

x = Tree(vals)

print ("Tree 1:")
x.pretty_print()

x2 = Tree2(vals2)
print ("Tree 2:")
x2.pretty_print()

print x.get_left().pretty_print()
print x.get_right().pretty_print()

#resolve_anaphor(x)

with open("binding_dataset.neural.json") as f:
    parser_output = json.load(f)

for elem in sorted(parser_output["sentences"], key=lambda x: x["index"]):
    print elem["parse"]
