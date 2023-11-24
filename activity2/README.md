# Guided Local Search

A implementation of Guided Local Search (GLS) for the University Course Timetabling Problem (UCTP) proposed by ITC2007 format.

Made for the course of Topics on Optimization at the Federal University of Espírito Santo (UFES), 2023/2.

## Requirements

- Python 3.12 or higher.
- Latest [Poetry](https://python-poetry.org/).

## Installation

```sh
poetry install
```

## Usage/test

```sh
poetry run pytest
```

## Repository

- [src/](src/): Source code
- [instances](instances/): Instances of the UCTP, provided by the ITC2007. Also includes a tester for your hardware, to even the playing field and make older results comparable to newer ones.
- [presentation](presentation/): Source code for the presentation slides.
- [report](report/): Source code for the report, in an article format.
