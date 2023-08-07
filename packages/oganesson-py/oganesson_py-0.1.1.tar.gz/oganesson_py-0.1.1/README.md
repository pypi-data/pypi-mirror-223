# Oganesson

A simple python code quality checked built on top of [Radon](https://pypi.org/project/radon/).

## Why Oganesson?

Whereas radon provides a rich reporting CLI, it does not support CI out of the box.  [Xenon](https://pypi.org/project/radon/) provides a CLI for using cyclomatic complexity metrics for a CI pipeline, however it doesn't offer other metrics. 

Oganesson provides a minimal CLI to generate a simple Cyclomatic Complexity and Maintainability Index report for a codebase.  It also provides a flag for CI use `--trigger` which raises an exception when any components of a codebase fall outside of the determined range.

In short, Oganesson makes a number of compromises to produce a very simple tool to get key metrics about a codebase, and use in a CI.

## Installation

Oganesson can be installed from pypi:

```sh
pip install oganesson-py
```

This installs the `oganesson` CLI tool.

## Usage

Currently oganesson intends only to provide the oganesson CLI tool:

```
$ oganesson --help
Usage: oganesson [OPTIONS] [PATHS]...

  # Oganesson

  A CLI for running quality metrics on Python code.  Currently a wrapper
  around Radon, with intent to add a few extra metrics in time.

  Whereas radon has flake8 support, and xenon is designed to work in a CI for
  cyclometric complexity, the maintainability index isn't supported in CI out
  of the box.  This tool produces a report to the stdout of all instances
  which don't satisfy the thresholds set.  If the trigger flag is set, the
  tool will raise an exception (for CI, or in future commit hooks).

Options:
  -a, --analysers [cc|mi]         Choice of analysers  [default: cc, mi]
  --max-cc INTEGER                Threshold for cyclomatic complexity
                                  reporting.  [default: 0]
  --min-mi FLOAT                  Threshold for maintainability index
                                  reporting in range [0, 100].  [default:
                                  100.0]
  --mi-multiline-comments BOOLEAN
                                  Treat multi-line strings as comments for
                                  maintainability reporting.  [default: True]
  -t, --trigger                   Raise an exception if quality thesholds are
                                  breached.
  --ignore TEXT                   Directories to ignore  [default: venv,
                                  .venv, .git]
  --help                          Show this message and exit.
```

### Simple Case - All Metrics

In the most simple case, to analyse all python files in the current directory, run `oganesson`.  An analysis report will be sent the the stdout, listing all python files and the analysis metrics associated with each component of the file.

### Choosing Analysers

To choose which analysers to use, use the `analysers` options, this can be `cc` or `mi`.

### Filtered Metrics

By default, oganesson captures **all** components and outputs their cyclomatic complexity and maintainability index.  To report only "poor" metrics, change the `min-mi` or `max-cc`.

For example `oganesson --analysers cc --max-ci 5` will only report the cyclomatic complexity of components with a cyclomatic complexity greater than 5.

### CI Usage

When used in a CI pipeline, use the `--trigger` flag to raise an exception if any of the thresholds are breached.

Note that by default the `max-ci` and `min-mi` thresholds will capture **all** possible values, so the job will fail in all cases.  For this to be useful it should be used alongside the `max-ci` and `min-mi` options.

A good starting point would be `oganesson --max-cc 10 --min-mi 20 --trigger`

