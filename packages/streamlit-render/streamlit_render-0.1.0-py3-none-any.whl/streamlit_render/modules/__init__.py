from streamlit_render.modules.render import Render
from streamlit_render.modules.media import Media
from streamlit_render.modules.html import HTML

__all__ = [
    "html",
    "render",
    "media",
]

render = Render()
html = HTML()
media = Media()