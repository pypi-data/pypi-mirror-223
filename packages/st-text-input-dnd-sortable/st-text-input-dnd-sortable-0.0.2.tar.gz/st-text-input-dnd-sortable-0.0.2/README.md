# streamlit-custom-component

Streamlit component which include row(s) of text input field with DnD property.

## Installation instructions

```sh
pip install st-text-input-dnd-sortable
```

## Usage instructions

```python
import streamlit as st

from st_text_input_dnd_sortable import st_text_input_dnd_sortable

output = st_text_input_dnd_sortable(
    textInputElement=[{"label": 'What is the name of your favourite person?', "default_value": "", "placeholder": "Joey"},
                      {"label": 'What is the name of your favourite dog?', "default_value": "", "placeholder": "Miyu"},
                      {"label": 'What is your favourite color?', "default_value": "", "placeholder": "Green"}])
```