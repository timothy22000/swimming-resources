---
license: cc-by-4.0
pretty_name: Swimming Resources Database
language:
  - en
task_categories:
  - text-retrieval
  - question-answering
  - text-classification
tags:
  - swimming
  - sports
  - open-data
  - coaching
  - water-safety
size_categories:
  - n<1K
configs:
  - config_name: default
    data_files:
      - split: train
        path: swimming_resources.parquet
---

# Swimming Resources Database

[![GitHub source](https://img.shields.io/badge/GitHub-timothy22000%2Fswimming--resources-181717?logo=github&logoColor=white)](https://github.com/timothy22000/swimming-resources)
[![License: CC BY 4.0](https://img.shields.io/badge/license-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Entries](https://img.shields.io/badge/entries-410-brightgreen.svg)](https://github.com/timothy22000/swimming-resources/blob/main/data/swimming_resources.json)
[![Categories](https://img.shields.io/badge/categories-20-blue.svg)](https://github.com/timothy22000/swimming-resources#categories)
[![Version](https://img.shields.io/badge/version-1.0.0-orange.svg)](https://github.com/timothy22000/swimming-resources/blob/main/CHANGELOG.md)

> Source repository: **[github.com/timothy22000/swimming-resources](https://github.com/timothy22000/swimming-resources)** - the GitHub repo is the canonical source. Corrections, additions, and dead-link reports go through GitHub issues or pull requests; the Parquet here is regenerated from those changes.

The Swimming Resources Database is an open dataset of 410 verified swimming
resources across 20 categories, covering governance, learn-to-swim programs,
technique, training, apps, books, coaching education, sports science, news,
gear, open water, triathlon, masters swimming, para swimming, drowning
prevention, records, college programs, recruiting services, and camps.

The dataset is intended for retrieval-augmented generation, recommendation
systems, knowledge bases, directory websites, and research workflows that need
structured information about the swimming ecosystem.

## Background

I started collecting these resources while learning to swim as an adult. The
useful material was scattered across forums, blogs, and outdated directories,
with frequent rebrands and dead links. This dataset is the index I wish had
existed when I started, cleaned up and released so other swimmers, coaches,
researchers, and ML systems can build on it instead of re-doing the search.

## Dataset Files

This Hugging Face dataset repo contains:

| File | Description |
| --- | --- |
| `swimming_resources.parquet` | Primary Hugging Face dataset file. |
| `README.md` | This dataset card. |

## Source Data

The canonical source of truth for this dataset is the GitHub repository:

**[github.com/timothy22000/swimming-resources](https://github.com/timothy22000/swimming-resources)**

Each entry is hand-curated as a Python literal in
[`scripts/data_part1.py`](https://github.com/timothy22000/swimming-resources/blob/main/scripts/data_part1.py)
through `data_part9.py`. The build pipeline at
[`scripts/build_dataset.py`](https://github.com/timothy22000/swimming-resources/blob/main/scripts/build_dataset.py)
validates every record against
[`data/schema.json`](https://github.com/timothy22000/swimming-resources/blob/main/data/schema.json)
and emits four formats: pretty-printed JSON, JSONL, CSV, and the Parquet file
shipped here. The GitHub repository keeps all four output formats checked in
alongside the schema, so the same dataset is available without going through
`datasets`.

Two scheduled workflows in the source repository keep the dataset honest:

- [`validate.yml`](https://github.com/timothy22000/swimming-resources/blob/main/.github/workflows/validate.yml)
  re-runs the build and schema validation on every pull request and push to
  `main`.
- [`link-check.yml`](https://github.com/timothy22000/swimming-resources/blob/main/.github/workflows/link-check.yml)
  runs weekly, fetches every URL in the dataset, and opens an issue listing any
  that no longer resolve.

Corrections, additions, and dead-link reports should go through GitHub
([issues](https://github.com/timothy22000/swimming-resources/issues) or
[pull requests](https://github.com/timothy22000/swimming-resources/pulls))
rather than the Hugging Face discussions tab, so that fixes flow through the
validation pipeline before the Parquet here is updated. The contributor
workflow is documented in
[`CONTRIBUTING.md`](https://github.com/timothy22000/swimming-resources/blob/main/CONTRIBUTING.md).

## Loading

```python
from datasets import load_dataset

dataset = load_dataset("t22000t/swimming-resources")
print(dataset["train"][0])
```

## Schema

Each row represents one resource.

| Field | Type | Description |
| --- | --- | --- |
| `id` | string | Stable identifier formatted as `<prefix>-NNN` or `<prefix>-NNNN`. |
| `category` | string | One of the 20 category identifiers listed below. |
| `subcategory` | string | Optional finer grouping within a category. |
| `name` | string | Official or commonly used display name. |
| `type` | string | Resource type, such as federation, app, book, curriculum, or database. |
| `audience` | string | Main audience served by the resource. |
| `description` | string | Concise one-sentence summary. |
| `url` | string | Canonical HTTP or HTTPS URL. |
| `pricing` | string | One of `free`, `paid`, `freemium`, `mixed`, or `varies`. |
| `region` | string | `global`, a continent, a country, or another practical region label. |
| `language` | string | ISO 639-1 language code, optionally with a region suffix. |
| `year_founded` | int64 or null | Known founding year, when available. |
| `status` | string | One of `active`, `rebranded`, or `defunct`. |
| `notes` | string | Caveats, rebrand details, ISBNs, replacement products, or context. |
| `tags` | list[string] | Search and retrieval tags. |
| `verified` | string | Month when the URL was last verified, formatted `YYYY-MM`. |

## Categories

| Category ID | Label |
| --- | --- |
| `governing_bodies` | Governing Bodies & Federations |
| `learn_to_swim` | Learn-to-Swim & Water Safety Programs |
| `technique` | Technique & Stroke Resources |
| `youtube` | YouTube Channels |
| `training_plans` | Training Plans & Workout Repositories |
| `apps` | Apps & Swim Technology |
| `books` | Books on Swimming |
| `certifications` | Coaching Certifications & Education |
| `science` | Sports Science, Biomechanics & Research |
| `news` | News, Communities & Magazines |
| `podcasts` | Podcasts |
| `gear` | Gear, Equipment & Reviews |
| `open_water` | Open Water & Marathon Swimming |
| `triathlon` | Triathlon Swimming |
| `masters` | Masters Swimming |
| `para` | Para Swimming & Adaptive Resources |
| `drowning_prevention` | Drowning Prevention & Public Health |
| `records` | Records, Rankings & Results Databases |
| `college` | College / NCAA Programs & Conferences |
| `recruiting` | Recruiting Services & Swim Camps |

## Data Quality

All entries are validated against the project JSON Schema before release. URLs
are stored with a `verified` month and are checked by scheduled automation in
the source repository.

The dataset includes historical `rebranded` and `defunct` entries when they are
useful for search, citation, or migration from older names and products.

## Licensing

The database content is released under Creative Commons Attribution 4.0
International (CC BY 4.0). Build scripts in the source repository are released
under the MIT License.

Please attribute the dataset to Timothy Sum and link to the source repository
and this Hugging Face dataset page.

## Citation

```bibtex
@misc{swimming_resources_db_2026,
  title  = {Swimming Resources Database},
  author = {Timothy Sum},
  year   = {2026},
  url    = {https://github.com/timothy22000/swimming-resources},
  note   = {Open-source index of swimming resources, v1.0.0}
}
```
