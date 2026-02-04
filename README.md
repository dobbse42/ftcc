## Fault-Tolerant Compiler Collection

[![Repository](https://img.shields.io/badge/GitHub-5C5C5C.svg?logo=github)](https://github.com/dobbse42/ftcc)
[![Unitary Foundation](https://img.shields.io/badge/Supported%20By-Unitary%20Foundation-FFFF00.svg)](https://unitary.foundation)
[![Discord Chat](https://img.shields.io/badge/dynamic/json?color=blue&label=Discord&query=approximate_presence_count&suffix=%20online.&url=https%3A%2F%2Fdiscord.com%2Fapi%2Finvites%2FJqVGmpkP96%3Fwith_counts%3Dtrue)](http://discord.unitary.foundation)


Fault-Tolerant Compiler Collection (ftcc) is a python library which acts as a framework for linking various fault-tolerant compilation tools together in order to perform end-to-end compilation of error-corrected quantum circuits.

For more information, see the docs or the official [ftcc discord channel](https://discord.gg/unitary-fund-764231928676089909) in the Unitary Foundation discord server.

ftcc is primarily for users who wish to perform end-to-end compilations of quantum circuits intended to be run with QEC, generally for the purposes of benchmarking and performing resource estimates on different ftcc techniques. ftcc has also been designed as a standard for implementations of new qec techniques to target. The goal is that any existing software implementation of some step in the fault-tolerant compilation pipeline can be easily adapted to work as a `layer` in ftcc, allowing easy integration with other parts of the compilation pipeline.

### Getting Started
We are holding off on publishing to PyPI until more of the core functionality is complete. However, if you would like to play around with the tool while it is still being developed, feel free to clone this repo!
We use `uv` for dependency management, and while you can use any package manager you like we would highly encourage users to use `uv` as well.

First, clone the repo:
```
git clone https://github.com/dobbse42/ftcc.git
```
then simply run `uv sync` and you should be able to use the library.
Feel free to test that everything's working by running the tests:
```
uv run pytest -s
```

Tutorials and example notebooks will be added around the same time that we implement packaging, but for now a good place to start understanding the library is by looking at the end-to-end tests.

### Contributing
Contributions are welcome! If you are interested in contributing, please see the contributor's guide. Feel free to reach out on the project's discord channel if you have any questions or just want to learn more.
If there is particular functionality missing which you would either like implemented or want to implement yourself, opening a feature request issue is a great place to start.

ftcc has been patterned after the Unitary Foundation's [ucc](https://github.com/unitaryfoundation/ucc) tool for circuit optimization, and tries to mimic its user experience where possible.
