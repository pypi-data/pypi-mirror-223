# Ontocop

[![coverage report](https://gitlab.com/lukasmu/ontocop/badges/master/coverage.svg?style=flat-square)](https://gitlab.com/lukasmu/ontocop/-/commits/master)
[![pipeline status](https://gitlab.com/lukasmu/ontocop/badges/master/pipeline.svg?style=flat-square)](https://gitlab.com/lukasmu/ontocop/-/commits/master)

A toolbox (and a [pre-commit](https://pre-commit.com) hook) for checking ontologies. Currently, this tool can perform two types of checks:
- It can evaluate ontologies using the [OntOlogy Pitfall Scanner](https://oops.linkeddata.es/aboutus.jsp)
- It can find inconsistent classes in OWL ontologies using [owlready2](https://owlready2.readthedocs.io)

## Installation

You can install Ontocop using [pip](https://packaging.python.org/en/latest/tutorials/installing-packages/):

```pip install ontocop```

Alternatively, you can also install Ontocop as a [pre-commit](https://pre-commit.com) hook. Here's a sample `.pre-commit-config.yaml`:

```yaml
-   repo: https://gitlab.com/lukasmu/ontocop
    rev: 0.2.0
    hooks:
    -   id: ontocop
```

## Changelog

Please see [CHANGELOG](CHANGELOG.md) for more information what has changed recently.

## License

This tool is open-sourced software licensed under the MIT license. Please see [LICENSE](LICENSE.md) for details.
