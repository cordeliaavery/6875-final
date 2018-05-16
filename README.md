# 6.863-final

Our algorithm requires a .json file containing sentences as parsed by CoreNLP. Our algorithm can be run as follows:

```
./resolver [-h] [-s SENTENCES] [-g GOLD_DATA] [-l LANGUAGE]
                [-c CONFIG_FILE] [-v] [-o OUTPUT_FILE]

optional arguments:
  -h, --help            show this help message and exit
  -s SENTENCES, --sentences SENTENCES
                        CoreNLP output containing parses for input sentences
  -g GOLD_DATA, --gold_data GOLD_DATA
                        Gold data for binding using CoreNLP indexing scheme
  -l LANGUAGE, --language LANGUAGE
                        Specify 'eng' for English, 'ger' for German
  -c CONFIG_FILE, --config_file CONFIG_FILE
                        json input for parameter settings. Should not need
                        anything other than the default!
  -v, --verbose         set to true to output mismatched coreference sets
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
```

The code for the main algorithm can be found in `algorithm_cls.py`, while the code for the tree construction can be found in `tree2.py`. English and German raw data can be found in `binding_dataset.txt` and `auf_deutsch.txt`, and their respective parses are found in `binding_dataset.deterministic.json` and `auf_deutsch.json`. Gold data is found in `gold_data.json` and `gold_data_ger.json`, and all other output from `CoreNLP` is found in `dataset/`. All code can be found at 
https://github.com/cordeliaavery/6875-final.

