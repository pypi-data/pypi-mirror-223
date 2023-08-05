from looqbox.objects.container.positional.abstract_positional_container import AbstractPositionalContainer
from looqbox.render.abstract_render import BaseRender


class ObjRow(AbstractPositionalContainer):

    def __init__(self, *children, **properties):
        super().__init__(*children, **properties)

    def to_json_structure(self, visitor: BaseRender):
        return visitor.row_render(self)
