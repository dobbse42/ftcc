from pathlib import Path
import tomllib
import tomli_w

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        root = Path(self.root)

        pyproject_path = root / "pyproject.toml"

        with pyproject_path.open("rb") as f:
            pyproject = tomllib.load(f)

        project = pyproject["project"]
        uv_conflicts = pyproject["tool"]["uv"]["conflicts"]
        dep_groups = pyproject["dependency-groups"]
        dep_sources = pyproject["tool"]["uv"]["sources"]

        output = {
            "version": project["version"],
            "dependency-groups": dep_groups,
            "dependency-conflicts": uv_conflicts,
            "dependency-sources": dep_sources,
        }

        output_path = root / "src" / "ftcc" / "_build_info.toml"

        with output_path.open("wb") as f:
            tomli_w.dump(output, f)

        print(f"Generated {output_path}")
