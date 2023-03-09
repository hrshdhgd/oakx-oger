# oakx-oger

This is an [OGER](https://github.com/OntoGene/OGER) plugin for [`oaklib`](https://github.com/INCATools/ontology-access-kit).

**ALPHA**

## Usage

```
pip install oakx-oger
runoak -i oger:sqlite:obo:envo annotate cultured organisms polar ecosystems atmospheric gas exchange
```

## How it works

There are two possible inputs to this plugin:
1. A `.txt` file [`runoak -i oger:sqlite:obo:envo annotate --text-file text.txt`]
2. Words that need to be annotated.[`runoak -i oger:sqlite:obo:envo annotate cultured organisms polar ecosystems atmospheric gas exchange`]

Input ontologies generally used `oaklib` can be used with an `oger:` prefix.
Note: This has been tested only with `oger:sqlite:obo:*` for now.


## Acknowledgements

This [cookiecutter](https://cookiecutter.readthedocs.io/en/stable/README.html) project was developed from the [oakx-plugin-cookiecutter](https://github.com/INCATools/oakx-plugin-cookiecutter) template and will be kept up-to-date using [cruft](https://cruft.github.io/cruft/).
