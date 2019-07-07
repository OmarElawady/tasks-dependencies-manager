Tasks dependencies manager
==========================

This is a project that maintains a list of tasks along with their dependencies.

This is the [documentation](https://omarelawady.github.io/tasksdependenciesmanager/doc/) of the project code.

Usage
=====

```python
b = Make()
b.add_task("publish", ["build-release"], "print publish")
b.add_task("build-release", ["nim-installed"], "print exec command to build release mode")
b.add_task("nim-installed", ["curl-installed"], "print curl LINK | bash")
b.add_task("curl-installed", ["apt-installed"], "apt-get install curl")
b.add_task("apt-installed", [], "code to install apt...")
b.run_task("publish")
```
