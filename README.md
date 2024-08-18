# Paper Translator

Components:

- marker-pdf: [VikParuchuri/marker: Convert PDF to markdown quickly with high accuracy](https://github.com/VikParuchuri/marker)
- langgraph: [jasonwei/langgraph: A tool for detecting language in text](https://github.com/jasonwei/langgraph)
- langchain: for knownledge graph.

## Installation

Please refer to `requirements.txt` for installation instructions.

## Usage

### marker-pdf

Put the PDFs in the `pdf/` folder and run:

```shell
marker_single pdf/[file].pdf markdown --batch_multiplier 2 --langs English
```

Example:

```shell
marker_single pdf/2211.09119v2.pdf markdown --batch_multiplier 2 --langs English
```

Revise the generated markdown files in `markdown/` folder. Then copy the revised files as `ragtest/input/[file].txt`.

### Dify

Import `src/paper-translator.yml` to your Dify. The paste the content of the revised markdown file as the input.
