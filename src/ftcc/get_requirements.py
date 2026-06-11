import tomllib
from packaging.requirements import Requirement


def get_requirements(compilation_path):
    filename = "src/ftcc/_build_info.toml"
    with open(filename, "rb") as f:
        build_info = tomllib.load(f)
        groups = build_info["dependency-groups"]
        conflicts = build_info["dependency-conflicts"]
        sources = build_info["dependency-sources"]

    print("groups:")
    print(groups)
    print("conflicts:")
    print(conflicts)
    print("sources:")
    print(sources)

    deps = set()

    for node in compilation_path:
        print(groups[node])
        print(deps)
        deps |= {Requirement(dep) for dep in groups[node]}
        # deps.append(groups[node])
        print(deps)

    for conflict in conflicts:
        dep1 = conflict[0]["group"]
        dep2 = conflict[1]["group"]
        if dep1 in deps and dep2 in deps:
            raise RuntimeError(
                f"Dependency conflicts exist in the compilation path. dep1: {dep1}, dep2: {dep2}"
            )

    print("Deps:")
    print(deps)
    with open("compilation_requirements.txt", "w") as f:
        # TODO: actually format this
        for dep in deps:
            if dep in sources.keys():
                f.write(write_requirement(dep, sources[dep]))
            else:
                f.write(str(dep))
            # f.write(dep)
            # f.write(sources[dep])
    print("Wrote compilation_requirements.txt")


# TODO: change to add sources to deps when they are created as Requirement objects
def write_requirement(pkg, src=None):
    if src is not None:
        req_string = pkg + " @ git+" + src
        return req_string
    else:
        return pkg
