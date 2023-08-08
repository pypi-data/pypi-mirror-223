# streamlit-selectable-gallery

Streamlit component that allows you to do X

## Installation instructions

```sh
pip install streamlit-selectable-gallery
```

## Usage instructions

```python
import streamlit as st
import base64

from streamlit_selectable_image_gallery import image_gallery

images = []
for file in ['documents/image1.png', 'documents/image2.png']:
    with open(file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
        images.append(f"data:image/jpeg;base64,{encoded}")

selected_index = image_gallery(images, 300)


st.write(selected_index)
```