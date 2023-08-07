# llm-friendly

![MIT Licence](https://img.shields.io/badge/licence-MIT-red)
[![pytest](https://github.com/GovTechSG/llm-friendly/actions/workflows/pytest.yml/badge.svg)](https://github.com/GovTechSG/llm-friendly/actions/workflows/pytest.yml)
![PyPI](https://img.shields.io/pypi/v/llm-friendly)
![PyPI - Downloads](https://img.shields.io/pypi/dm/llm-friendly)


`llm-friendly` converts API responses to LLM-friendly text.

```mermaid
flowchart LR
    APIResponse["API Response \n or \n JSON body"]
    LLMFriendly["llm-friendly"]
    LLM["Large-Language Model \n (e.g. OpenAI or Llama 2"]
    
    APIResponse -- JSON --> LLMFriendly -- string --> LLM
```

## Currently Supported Source APIs

 - Amazon Web Services (AWS)
   - Textract

[//]: # ( - Azure AI)

[//]: # (   - Vision)

[//]: # ( - Google Cloud Platform &#40;GCP&#41;)

[//]: # (   - Vision)

## Installation

### Latest Stable

```shell
pip install llm-friendly
```

### Latest Development Version

```shell
pip install git+https://github.com/GovTechSG/llm-friendly.git
```

## Usage

Convert your tables into CSV, JSON or Markdown formats.

```python
from llm_friendly.aws import textract

textract_response = {...}
text_content = textract.to_llm_output(textract_response, mode=textract.MODE_CSV) # MODE_JSON or MODE_MARKDOWN
print(text_content)
```

## Tests

```shell
pytest
```

## Similar Projects

- [Unstructured](https://github.com/Unstructured-IO/unstructured/): Supports primarily unstructured formats (Word, PDF, Excel, Email etc)
