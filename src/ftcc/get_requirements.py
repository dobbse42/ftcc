import tomllib
from packaging.requirements import Requirement


def get_requirements(compilation_path, requirements_filename):
    filename = "src/ftcc/_build_info.toml"
    with open(filename, "rb") as f:
        build_info = tomllib.load(f)
        groups = build_info["dependency-groups"]
        conflicts = build_info["dependency-conflicts"]
        sources = build_info["dependency-sources"]

    # print("groups:")
    # print(groups)
    # print("conflicts:")
    # print(conflicts)
    # print("sources:")
    # print(sources)

    deps = set()

    for node in compilation_path:
        # print(groups[node])
        # print(deps)
        deps |= {Requirement(dep) for dep in groups[node]}
        # deps.append(groups[node])
        # print(deps)

    for conflict in conflicts:
        dep1 = conflict[0]["group"]
        dep2 = conflict[1]["group"]
        # print(f"dep1: {dep1}, dep2: {dep2}")
        # print(f"compilation path: {compilation_path}")
        if dep1 in compilation_path and dep2 in compilation_path:
            raise RuntimeError(
                f"Dependency conflicts exist in the compilation path. dep1: {dep1}, dep2: {dep2}"
            )

    # print("Deps:")
    # print(deps)
    with open(requirements_filename, "w") as f:
        # TODO: actually format this
        for dep in deps:
            if dep.name in sources.keys():
                # print(f"dep {dep} has source {sources[dep.name]}")
                # print(str(sources[dep.name]))
                f.write(write_requirement(str(dep), sources[dep.name]))
            else:
                f.write(str(dep))
            # f.write(dep)
            # f.write(sources[dep])
            f.write("\n")
    print("Wrote compilation_requirements.txt")


# TODO: change to add sources to deps when they are created as Requirement objects
def write_requirement(pkg, src=None):
    if src is not None:  # for now only accepts git sources
        src_string = src["git"]
        if "rev" in src.keys():
            src_string = src_string + "@" + src["rev"]
        req_string = pkg + " @ git+" + src_string
        print(req_string)
        return req_string
    else:
        return pkg
