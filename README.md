# 6.863-final

Overleaf document:
[Final writeup](https://www.overleaf.com/15495036jntwcxndwsts)

Need pyStatParser:
`pip install pyStatParser`

Must setup CoreNLP server. Download CoreNLP (https://stanfordnlp.github.io/CoreNLP/download.html).

`cd stanford-corenlp-full-2018-02-27`

`java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer`

And then just run `python get_parse_tree.py`
