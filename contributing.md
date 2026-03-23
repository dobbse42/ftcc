Contribution Guide

The primary kinds of contributions we are looking for are the integration of new FTQC compilation tools. Contributions of this sort can be as small as opening an issue to make us aware of a tool not yet included in the library, or as large as the full implementation of a new compilation layer and associated translation layers. One of the primary goals of `ftcc` is to bring together tools which the community already uses, so your contributions are invaluable!

Adding new tools to `ftcc` is mostly a matter of familiarity with the tool and some tedious work writing a generalized translation function. In an ideal world, developers and/or power-users of existing tools would take the lead on writing associated compilation layers in `ftcc`. By design, most of the time required for such contributions is in gaining familiarity with the tool to be integrated; somebody already intimately familiar with the tool should be able to write an associated compilation layer in a matter of hours.

Please be sure to write unit tests for any translation functions and compile functions you write; as a rule we trust compilation libraries to sufficiently test their own correctness, so most of our testing focuses on making sure any integrated libraries are being called correctly and that translation functions are not modifying the logic of the circuit. Remember: translation functions only serve to translate IRs and set up succeeding layers to perform their compilation steps. If the output of one tools needs to be further compiled before it can be used as input for another tool, then such compilation should be done in a new compilation layer.

## Setting up the development environment
We rely heavily on `uv`. If you do not have `uv` installed already, see [the uv installation guide](https://docs.astral.sh/uv/getting-started/installation/) and associated tutorials.

You can clone the repo with the following:
```
git clone https://github.com/dobbse42/ftcc.git
cd ftcc
uv sync --all-extras --all-groups
```


## Linting
At the moment, we follow the exact same linting workflow and requirements as `ucc`. I have some personal preferences that may vary slightly from the `ucc` workflow, but in the spirit of making contribution as easy as possible I choose not to enforce them.

Use `pre-commit`.
This can be set up easily with `uv add pre-commit`, followed by `uv run pre-commit install`. Now `pre-commit` should run automatically on every commit.

`pre-commit` should now automatically lint all commits using `ruff` according to the rules specified in `.pre-commit-config.yaml` and `ruff.toml`.

## Compilation layers
Compilation layers are where compilation tools are actually called. Every compilation layer has a `self.metadata` dictionary, which is passed between layers in order to store metadata about a compilation pipeline (e.g. the precise code being used, the device architecture being compiled to, the name of the circuit being compiled, etc.).
Every compilation layer also has a `self.compile()` function, which is where the actual compilation takes place. This is where the tool is called and the resulting circuit after compilation is stored, typically as `self.circuit`. Some compilation layers also have a `self.output()` function to export the compiled IR in some way, but this is not necessary. All other functions in a compilation layer are internally accessible helper functions to be called during `self.__init__()` and `self.compile()`. Only the `__init__()`, `compile()`, and `output()` functions should ever be called outside of the compilation layer.

## Translation layers
When contributing a translation function, please be careful to follow the [[Translation Layers|guidelines]] on what should and should not be included in a translation function. Separating compilation from translation is important for both maintaining the modularity of the tool and making contributions easier. If you find that there is some missing link between two compilation layers which you could quickly implement, feel free to write this as a separate tool and integrate it as a new compilation layer!
The metadata dictionary from one compilation layer should always be passed to any succeeding compilation layers in its entirety. At the moment, our policy is to only ever add information to the metadata dictionary, though this may change as compilation pipelines become longer and we see more how the dictionary is used throughout the tool.

## Testing
You can run all unit tests with `uv run pytest ftcc`. Note that this can take a while, as this will involve installing *all* libraries used in any of the layers. If you want to check the installation and verify that the tool works, it is instead better to run `uv run pytest ftcc-samples`. This will test some sample compilation pipelines using common libraries.
A good rule to remember when writing tests is that the goal is to test the code written as a part of `ftcc`, not some external tool. For compilation layers we generally try to replicate some of the unit tests present in the tool being called, checking that the tool functions the same when we call it through ftcc as it does when the developers themselves call it in their tests. When testing translation layers we generally try to replicate some unit test on the succeeding layer which uses random circuits as input, just with the random circuit acting as input for the *preceding* layer, thereby testing that the use of the translation function between the two layers does not change the correctness of the circuit. We also write some end-to-end tests for full compilation pipelines, but these are mostly 1) to test the functionality of internal `ftcc` code, and 2) to act as examples of how one might use `ftcc` for a full compilation.

## Dependencies
Not all tools in `ftcc` have compatible dependencies. For example, conflicting requirements on qiskit versions (espec around 1.0) and python versions (especially around 3.10-3.12) are quite common. This has been a problem in the community for some time, so of course it is also present in a tool such as `ftcc`which seeks to bring together tools from across the community.
We currently handle this with `uv` dependency groups. Every compilation layer gets its own dependency group, and any conflicts are recorded manually in `pyproject.toml`. At runtime, we only use the dependency groups associate with tools involved in the specified compilation pipeline.
At the moment we do not handle conflicts between non-adjacent tools in a single compilation pipeline, nor do we handle conflicts between adjacent tools, as this has not yet been an issue. In principle, both of these situations could occur and there should be a way to handle them, but as it is not yet urgent we leave this problem for later


All contributions and discussions are welcome. If you have further questions which you believe are not suited to a github issue, feel free to ask on the `fault-tolerant-compiler-collection` [channel](https://discord.gg/unitary-fund-764231928676089909) in the Unitary Foundation discord. If you would rather ask in a more private forum, feel free to dm dobbse42#5400 on discord (@Evan on the UnitaryFoundation discord).
