import os
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "image_gallery",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("streamlit_selectable_image_gallery", path=build_dir)


def image_gallery(images, height, key=None):
    """Create a new instance of "image_gallery".

    Parameters
    ----------
    images: list
        The list of images to display in the gallery. Each image can be an HTTP URL or a Base64 image.
    height: int
        The height of an image in the gallery.
    key: str or None
        An optional key that uniquely identifies this component.

    Returns
    -------
    int
        The index of the selected image in the gallery.

    """
    component_value = _component_func(images=images, height=height, key=key, default=-1)

    return component_value


if not _RELEASE:
    import streamlit as st

    st.subheader("Image Gallery Component")

    # A list of image URLs for testing
    images = [
        "https://images.unsplash.com/photo-1575936123452-b67c3203c357?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80",
        "https://images.unsplash.com/photo-1488372759477-a7f4aa078cb6?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80",
        "https://images.unsplash.com/photo-1574169208507-84376144848b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=879&q=80"
    ]

    # The height of an image
    height = 200

    selected_index = image_gallery(images, height)
    if selected_index >= 0:
        st.markdown(f"You've selected image {selected_index}!")