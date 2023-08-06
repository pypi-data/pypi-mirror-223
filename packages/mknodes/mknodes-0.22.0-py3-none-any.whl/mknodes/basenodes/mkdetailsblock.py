from __future__ import annotations

import logging

from typing import Any, Literal

from mknodes.basenodes import mkblock, mknode
from mknodes.utils import helpers


logger = logging.getLogger(__name__)

AdmonitionTypeStr = Literal[
    "node",
    "abstract",
    "info",
    "tip",
    "success",
    "question",
    "warning",
    "failure",
    "danger",
    "bug",
    "example",
    "quote",
]


class MkDetailsBlock(mkblock.MkBlock):
    """Pymdownx-based details box."""

    ICON = "octicons/info-16"
    REQUIRED_EXTENSIONS = ["pymdownx.blocks.details"]

    def __init__(
        self,
        content: str | list | mknode.MkNode,
        *,
        typ: AdmonitionTypeStr = "info",
        expand: bool | None = None,
        title: str | None = None,
        **kwargs: Any,
    ):
        """Constructor.

        Arguments:
            content: Admonition content
            typ: Admonition type
            expand: Whether the details block should be expanded initially
            title: Optional Admonition title
            kwargs: Keyword arguments passed to parent
        """
        super().__init__(
            "details",
            content=content,
            argument=title or "",
            attributes=dict(type=typ, open=expand),
            **kwargs,
        )

    def __repr__(self):
        from mknodes.basenodes import mktext

        if len(self.items) == 1 and isinstance(self.items[0], mktext.MkText):
            content = str(self.items[0])
        elif len(self.items) == 1:
            content = self.items[0]
        else:
            content = [str(i) if isinstance(i, mktext.MkText) else i for i in self.items]
        return helpers.get_repr(
            self,
            content=content,
            typ=self.typ,
            title=self.argument,
            expand=self.expand,
            _filter_empty=True,
        )

    @property
    def typ(self) -> AdmonitionTypeStr:
        return self.attributes["type"]

    @typ.setter
    def typ(self, value: AdmonitionTypeStr):
        self.attributes["type"] = value

    @property
    def expand(self) -> bool:
        return self.attributes["open"]

    @expand.setter
    def expand(self, value: bool):
        self.attributes["open"] = value

    @staticmethod
    def create_example_page(page):
        import mknodes

        page.status = "new"  # for the small icon in the left menu
        page += "MkDetailsBlock is a markdown extension based on pymdownx block syntax."
        url = "https://facelessuser.github.io/pymdown-extensions/extensions/blocks/api/"
        page += mknodes.MkLink(url, "More info", as_button=True)
        # AdmonitionTypeStr is a Literal containing all Admonition types
        for typ in AdmonitionTypeStr.__args__:
            node = mknodes.MkDetailsBlock(
                typ=typ,
                content=f"This is type **{typ}**",
                title=f"Details block with type {typ!r}",
                header=f"Type '{typ}'",
            )
            page += mknodes.MkReprRawRendered(node)


if __name__ == "__main__":
    tab = MkDetailsBlock(content="test", title="test")
    print(tab)
