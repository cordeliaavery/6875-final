# 6.863-final

Our algorithm requires a .json file containing sentences as parsed by CoreNLP. Our algorithm can be run as follows:

```
usage: ./resolver [-h] [-s SENTENCES] [-g GOLD_DATA] [-l LANGUAGE]
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


