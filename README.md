# Paper Translator

Components:

- marker-pdf: [VikParuchuri/marker: Convert PDF to markdown quickly with high accuracy](https://github.com/VikParuchuri/marker)
- langgraph: [jasonwei/langgraph: A tool for detecting language in text](https://github.com/jasonwei/langgraph)
- langchain: for knownledge graph.

## Installation

Please refer to `requirements.txt` for installation instructions.

## Usage

Put the PDFs in the `pdf/` folder and run:

```shell
marker_single pdf/[file].pdf markdown --batch_multiplier 2 --langs English
```

Example:

```shell
marker_single pdf/2211.09119v2.pdf markdown --batch_multiplier 2 --langs English
```

Revise the generated markdown files in `markdown/` folder. Then copy the revised files as `ragtest/input/[file].txt`.

Run GraphRAG to generate the knowledge graph:

```shell
python -m graphrag.index --init --root ./ragtest
```

This will create two files: `.env` and `settings.yaml` in the `ragtest` directory.

Modify the `settings.yaml` file same as `graphrag_settings.yaml`.

Edit the grapgrag source code `graphrag/llm/openai/openai_embeddings_llm.py` same as [GraphRAG local setup via vLLM and Ollama : A detailed integration guide. | by Saurabh Rajaram Yadav | Jul, 2024 | Medium](https://medium.com/@ysaurabh059/graphrag-local-setup-via-vllm-and-ollama-a-detailed-integration-guide-5d85f18f7fec).

Auto prompt tuning(After I run it, the indexing was failed):

```shell
python -m graphrag.prompt_tune --config ragtest\settings.yaml --root ragtest --no-entity-types
```

Run indexing:

```shell
python -m graphrag.index --root ./ragtest
```
