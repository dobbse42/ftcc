## Fault-Tolerant Compiler Collection

[![Repository](https://img.shields.io/badge/GitHub-5C5C5C.svg?logo=github)](https://github.com/dobbse42/ftcc)
[![Unitary Foundation](https://img.shields.io/badge/Supported%20By-Unitary%20Foundation-FFFF00.svg)](https://unitary.foundation)



Fault-Tolerant Compiler Collection (ftcc) is a python library which acts as a framework for linking various fault-tolerant compilation tools together in order to perform end-to-end compilation of error-corrected quantum circuits.

For more information, see the docs, the official discord channel, or discussions.

ftcc is primarily for users who wish to perform end-to-end compilations of quantum circuits intended to be run with QEC, generally for the purposes of benchmarking and performing resource estimates on different ftcc techniques. ftcc has also been designed as a standard for implementations of new qec techniques to target. The goal is that any existing software implementation of some step in the fault-tolerant compilation pipeline can be easily adapted to work as a `layer` in ftcc, allowing easy integration with other parts of the compilation pipeline.

Contributions are welcome! If you are interested in contributing, please see the contributor's guide. Feel free to reach out on the project's discord channel if you have any questions or just want to learn more.

ftcc has been patterned after the Unitary Foundation's [ucc](https://github.com/unitaryfoundation/ucc) tool for circuit optimization, and tries to mimic its user experience where possible.
