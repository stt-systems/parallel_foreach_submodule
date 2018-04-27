# Parallel Foreach Submodule

Parallel Foreach Submodule (PFS) is a tool for "git submodule foreach" execution in parallel.


### What can I do with PFS?

* Execute git submodule foreach in parallel
* Use it from terminal when it is installed
* Multiplatform execution (it is developed in Python)


### Installation

You can install or upgrade PFS with:

`$ pip install pfs --upgrade`

Or you can install from source with:

```bash
$ git clone https://github.com/RDCH106/parallel_foreach_submodule.git --recursive
$ cd parallel_foreach_submodule
$ pip install .
```


### Quick example

```bash
$ pfs -p "D:\project" -c "git pull origin" -j 8
```

The example executes command `git pull origin` for each submdoule in `D:\project` using 8 threads.
