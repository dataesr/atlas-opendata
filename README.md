# Repository for Processing Data of French Studiants

In this repository, we process Data of French Studiants by aggregating at differents geographical levels and correct some features.

## Setup Instructions

To use it, first:

- create a `INPUT` folder in the root directory with the raw data in it, in .parquet format for each year.
- create an empty `POST_GENTAB` folder in the root directory.
- adding new formats of this year in the `format` page of the ATLAS googlesheet here:
  - `https://docs.google.com/spreadsheet/ccc?key=11NFXSIg6gQMCsMa8zWQQyypvvYBEmfyJfF2yytXqgMk`
- adding new EPE of this year in the `D_EPE` page of the ESR googlesheet here:
  - `https://docs.google.com/spreadsheet/ccc?key=11NFXSIg6gQMCsMa8zWQQyypvvYBEmfyJfF2yytXqgMk`

## 1. Run the notebook `1_opendata_altlas_features_to_correct.ipynb`

- Run the notebook with all the details of the code, step by step. When using the Jupyter notebook, select the `rentree` parameter that means the year of the scholarship (ex: 2024 for the year 2024-2025) at the beginning, and then execute each cell to obtain a standardized format of data for each year.

This notebook enable to change the incorrect features and complete the missing ones. At the end of the process, when each year is done: The `POST_GENTAB` folder must have the same number of file as the folder `INPUT`. With these new files, we produce the 'état du supérieur' map.

## 2. Run the notebook `2_opendata_atlas_total_communes.ipynb`

- Run the notebook with all the details of the code, step by step for the level "communal".

## 3. Run the notebook `3_opendata_atlas_total_etablissements.ipynb`

- Run the notebook step by step, including all code details, using the 'établissement' level, which is much more granular.
