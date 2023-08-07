from __future__ import annotations

from importlib import metadata
import pathlib

from packaging.markers import Marker
from packaging.requirements import Requirement

from mknodes.utils import helpers


CLASSIFIERS = [
    "Development Status",
    "Environment",
    "Framework",
    "Intended Audience",
    "License",
    "Natural Language",
    "Operating System",
    "Programming Language",
    "Topic",
    "Typing",
]


def get_extras(markers):
    extras = []
    for marker in markers:
        match marker:
            case list():
                extras.extend(get_extras(marker))
            case tuple():
                if str(marker[0]) == "extra":
                    extras.append(str(marker[2]))
    return extras


class Dependency:
    def __init__(self, name):
        self.req = Requirement(name)
        self.name = self.req.name
        self.marker = Marker(name.split(";", maxsplit=1)[-1]) if ";" in name else None
        self.extras = get_extras(self.marker._markers) if self.marker else []

    def __repr__(self):
        return f"{type(self).__name__}(name={self.name!r})"


class PackageInfo:
    def __init__(self, pkg_name: str):
        self.package_name = pkg_name
        self.distribution = metadata.distribution(pkg_name)
        self.metadata = self.distribution.metadata
        self.urls = {
            v.split(",")[0]: v.split(",")[1]
            for k, v in self.metadata.items()
            if k == "Project-URL"
        }
        requires = self.distribution.requires
        self.requirements = [Dependency(i) for i in requires] if requires else []
        self.classifiers = [v for h, v in self.metadata.items() if h == "Classifier"]
        self.version = self.metadata["Version"]
        self.metadata_version = self.metadata["Metadata-Version"]
        self.name = self.metadata["Name"]

    def __repr__(self):
        return helpers.get_repr(self, pkg_name=self.package_name)

    def get_license(self) -> str:
        if license_name := self.metadata.get("License-Expression", "").strip():
            return license_name
        return next(
            (
                value.rsplit("::", 1)[1].strip()
                for header, value in self.metadata.items()
                if header == "Classifier" and value.startswith("License ::")
            ),
            "Unknown",
        )

    def get_keywords(self) -> list[str]:
        return self.metadata.get("Keywords", "").split(",")

    def get_required_package_names(self) -> list[str]:
        return [i.name for i in self.requirements]

    def get_extras(self):
        return {extra for dep in self.requirements for extra in dep.extras}

    def get_license_file_path(self) -> pathlib.Path | None:
        file = self.metadata.get("License-File")
        return pathlib.Path(file) if file else None


if __name__ == "__main__":
    info = PackageInfo("mknodes")
    print(info.get_license_file_path())
