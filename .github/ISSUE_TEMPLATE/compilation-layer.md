---
name: Compilation layer
about: Describe this issue template's purpose here.
title: 'New compilation layer: [insert name here]'
labels: Compilation layer
assignees: ''

---

## Compilation step
What fault-tolerant compilation step does this layer implement?

## Tool/library to be used
What external tool/library is performing this compilation? Is this the express purpose of this tool, or are you only using some subset of the tool's functionality?

## Necessary translation layers
What translation layers will need to be written to integrate this compilation layer with the existing compilation graph? Briefly outline the work you expect these layers to need to perform as well if possible.

## Testing and verification
What unit tests will you write to verify the correctness of this integration? Remember that we do not want to test the correctness of the tool being integrated, but rather the correctness of your use of the tool.
