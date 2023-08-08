# import streamlit as st
# import os
# import streamlit.components.v1 as components

# # Create a _RELEASE constant. We'll set this to False while we're developing
# # the component, and True when we're ready to package and distribute it.
# # (This is, of course, optional - there are innumerable ways to manage your
# # release process.)
# _RELEASE = True

# # Declare a Streamlit component. `declare_component` returns a function
# # that is used to create instances of the component. We're naming this
# # function "_component_func", with an underscore prefix, because we don't want
# # to expose it directly to users. Instead, we will create a custom wrapper
# # function, below, that will serve as our component's public API.

# # It's worth noting that this call to `declare_component` is the
# # *only thing* you need to do to create the binding between Streamlit and
# # your component frontend. Everything else we do in this file is simply a
# # best practice.

# if not _RELEASE:
#     _component_func = components.declare_component(
#         # We give the component a simple, descriptive name ("st_text_input_dnd_sortable"
#         # does not fit this bill, so please choose something better for your
#         # own component :)
#         "st_text_input_dnd_sortable",
#         # Pass `url` here to tell Streamlit that the component will be served
#         # by the local dev server that you run via `npm run start`.
#         # (This is useful while your component is in development.)
#         url="http://localhost:3001",
#     )
# else:
#     # When we're distributing a production version of the component, we'll
#     # replace the `url` param with `path`, and point it to to the component's
#     # build directory:
#     parent_dir = os.path.dirname(os.path.abspath(__file__))
#     build_dir = os.path.join(parent_dir, "frontend/build")
#     _component_func = components.declare_component(
#         "st_text_input_dnd_sortable", path=build_dir)


# # Create a wrapper function for the component. This is an optional
# # best practice - we could simply expose the component function returned by
# # `declare_component` and call it done. The wrapper allows us to customize
# # our component's API: we can pre-process its input args, post-process its
# # output value, and add a docstring for users.
# def st_text_input_dnd_sortable(textInputElement):
#     """Create a new instance of "st_text_input_dnd_sortable".

#     Parameters
#     ----------
#     textInputElement: list of obj where each obj contains keys of "label", "default_value",
#          and "placeholder"

#     Returns
#     -------
#     list
#         list of obj where each obj contains keys of "label", "default_value",
#         "placeholder", and "output"

#     """
#     # Call through to our private component function. Arguments we pass here
#     # will be sent to the frontend, where they'll be available in an "args"
#     # dictionary.
#     #
#     # "default" is a special argument that specifies the initial return
#     # value of the component before the user has interacted with it.
#     component_value = _component_func(
#         textInputElement=textInputElement)
#     if component_value is not None:
#         component_value = component_value['updatedOutput']
#     else:
#         component_value = textInputElement
#         for iItem in range(len(textInputElement)):
#             component_value[iItem]['output'] = component_value[iItem]['default_value']
#     # We could modify the value returned from the component if we wanted.
#     # There's no need to do this in our simple example - but it's an option.
#     return component_value


# # Add some test code to play with the component while it's in development.
# # During development, we can run this just as we would any other Streamlit
# # app: `$ streamlit run st_text_input_dnd_sortable/__init__.py`

# output = st_text_input_dnd_sortable(
#     textInputElement=[{"label": 'ชื่อที่แสดงเวร "เช้า 1"', "default_value": "ช", "placeholder": "ช"},
#                       {"label": 'ชื่อที่แสดงเวร "บ่าย 1"',
#                        "default_value": "บ", "placeholder": "บ"},
#                       {"label": 'ชื่อที่แสดงเวร "ดึก 1"', "default_value": "ด", "placeholder": "ด"}])

# st.write(output)

from st_text_input_dnd_sortable import st_text_input_dnd_sortable

output = st_text_input_dnd_sortable(
    textInputElement=[{"label": 'What is the name of your favourite person?', "default_value": "", "placeholder": "Joey"},
                      {"label": 'What is the name of your favourite dog?', "default_value": "", "placeholder": "Miyu"},
                      {"label": 'What is your favourite color?', "default_value": "", "placeholder": "Green"}])
