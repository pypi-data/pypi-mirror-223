from looqbox.render.abstract_render import BaseRender
from looqbox.objects.looq_object import LooqObject


class ObjForm(LooqObject):
    """
    Creates a Looqbox form.

    Attributes:
    --------
        :param dict *fields: Form parameters.
        :param str title: Form title.
        :param str method: Form method ("GET" or "POST").
        :param str action: Form action.
        :param str filepath: Form input file path.
        :param str tab_label: Set the name of the tab in the frame.

    Example:
    --------
    >>> form = ObjForm({"type": "input", "label": "Loja", "value": "3",
    ...                 "name": "loja", "readonly": TRUE, "style": {"text-align": "center"}},
    ...                {"type": "input", "label": "Produto", "value": "Suco",
    ...                 "name": "plu", "readonly": TRUE, "style": {"text-align": "center"}},
    ...                title="Suco de laranja 350mL")

    Properties:
    --------
        to_json_structure()
            :return: A JSON string.
    """

    def __init__(self, *fields, title=None, method="GET", action=None, filepath=None, tab_label=None, value=None):
        """
        Creates a view to drag and drop a file that will be read and used in other script of the response.

        Parameters:
        --------
            :param dict *fields: Form parameters.
            :param str title: Form title.
            :param str method: Form method ("GET" or "POST").
            :param str action: Form action.
            :param str filepath: Form input file path.
            :param str tab_label: Set the name of the tab in the frame.

        Example:
        --------
        >>> form = ObjForm({"type": "input", "label": "Loja", "value": "3",
        ...                 "name": "loja", "readonly": TRUE, "style": {"text-align": "center"}},
        ...                {"type": "input", "label": "Produto", "value": "Suco",
        ...                 "name": "plu", "readonly": TRUE, "style": {"text-align": "center"}},
        ...                title="Suco de laranja 350mL")
        """
        super().__init__()
        if action is None:
            action = ""
        self.title = title
        self.method = method
        self.action = action
        self.filepath = filepath
        self.fields = fields
        self.tab_label = tab_label
        self.value = value

    def to_json_structure(self, visitor: BaseRender):
        return visitor.obj_form_render(self)
