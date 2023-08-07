from __future__ import annotations

from collections.abc import Sequence
import dataclasses
import logging

from typing import Any, Literal

from mknodes.basenodes import mkcontainer, mkimage, mknode
from mknodes.utils import helpers


# ![Static Badge](https://img.shields.io/badge/built_with-mknodes-yellow?link=www.pypa.org)

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Shield:
    identifier: str
    title: str
    image_url: str
    url: str

    def get_image_url(self, user, project, branch):
        return self.image_url.format(user=user, project=project, branch=branch)

    def get_url(self, user, project):
        return self.url.format(user=user, project=project)


build_shield = Shield(
    identifier="build",
    title="Github Build",
    image_url="https://github.com/{user}/{project}/workflows/Build/badge.svg",
    url="https://github.com/{user}/{project}/actions/",
)

latest_version_shield = Shield(
    identifier="version",
    title="PyPI Latest Version",
    image_url="https://img.shields.io/pypi/v/{project}.svg",
    url="https://pypi.org/project/{project}/",
)

license_shield = Shield(
    identifier="license",
    title="PyPI License",
    image_url="https://img.shields.io/pypi/l/{project}.svg",
    url="https://pypi.org/project/{project}/",
)

package_status_shield = Shield(
    identifier="status",
    title="Package status",
    image_url="https://img.shields.io/pypi/status/{project}.svg",
    url="https://pypi.org/project/{project}/",
)

code_cov_shield = Shield(
    identifier="codecov",
    title="Package status",
    image_url="https://codecov.io/gh/{user}/{project}/branch/{branch}/graph/badge.svg",
    url="https://codecov.io/gh/{user}/{project}/",
)

black_shield = Shield(
    identifier="black",
    title="Code style: black",
    image_url=r"https://img.shields.io/badge/code%20style-black-000000.svg",
    url="https://github.com/psf/black",
)

pyup_shield = Shield(
    identifier="pyup",
    title="PyUp",
    image_url="https://pyup.io/repos/github/{user}/{project}/shield.svg",
    url="https://pyup.io/repos/github/{user}/{project}/",
)

codetriage_shield = Shield(
    identifier="code_triage",
    title="Open Source Helpers",
    image_url="https://www.codetriage.com/{user}/{project}/users.svg",
    url="https://www.codetriage.com/{user}/{project}/",
)

SHIELDS = [
    build_shield,
    latest_version_shield,
    package_status_shield,
    code_cov_shield,
    black_shield,
    pyup_shield,
    codetriage_shield,
    license_shield,
]

ShieldTypeStr = Literal[
    "build",
    "version",
    "status",
    "codecov",
    "black",
    "pyup",
    "code_triage",
    "license",
]


class MkShields(mkcontainer.MkContainer):
    """MkCritic block."""

    ICON = "simple/shieldsdotio"

    def __init__(
        self,
        shields: Sequence[ShieldTypeStr],
        user: str,
        project: str,
        branch: str = "main",
        **kwargs: Any,
    ):
        """Constructor.

        Arguments:
            shields: Shields to include
            user: Github username for shields
            project: project name for shields
            branch: branch name for shields
            kwargs: Keyword arguments passed to parent
        """
        super().__init__(**kwargs)
        self.block_separator = "\n"
        self.user = user
        self.project = project
        self.branch = branch
        self.shields = shields

    def __repr__(self):
        kwargs = dict(
            shields=self.shields,
            user=self.user,
            project=self.project,
        )
        if self.branch != "main":
            kwargs["branch"] = self.branch
        return helpers.get_repr(self, **kwargs)

    @property
    def items(self) -> list[mknode.MkNode]:
        return [
            mkimage.MkImage(
                s.get_image_url(user=self.user, project=self.project, branch=self.branch),
                link=s.get_url(user=self.user, project=self.project),
                title=s.title,
                parent=self,
            )
            for s in SHIELDS
            if s.identifier in self.shields
        ]

    @items.setter
    def items(self, value):
        pass

    @staticmethod
    def create_example_page(page):
        import mknodes

        node = MkShields(
            shields=["version", "status", "codecov"],
            user="phil65",
            project="mknodes",
        )
        page += mknodes.MkReprRawRendered(node)


if __name__ == "__main__":
    shields = MkShields(
        shields=["version", "status", "codecov"],
        user="phil65",
        project="prettyqt",
    )
    print(shields)
