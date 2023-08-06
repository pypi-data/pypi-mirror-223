from streamlit_render.core.frame import new_element
import streamlit as st
import json
class Render:  
    def Object(self, data, callback, **props):       
        file = fileExtension = None
        if data is not None:
            file = data.getvalue().decode("utf-8")
            fileExtension = data.name.split(".")[-1]

        new_element("renderObject", "Object")(
            file=file, 
            fileExtension=fileExtension,
            callback=callback,           
            **props
        )