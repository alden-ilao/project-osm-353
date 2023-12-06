# Project-OSM-353
CMPT 373 data analysis project integrating OpenSourceMap data, exploring restaurant emeneties in the Metro Vancouver area.
Find out report [here](https://docs.google.com/document/d/1smrJh-KzrwZYtFqh73VDUU6BtP1ffGA-mlO0C4Erc8c/edit?usp=sharing)


## Creating New Environment from environment.yml
```
conda env create -f environment.yml
```

## Updating Environment Packages
Note: Make sure you activated the environment

Use this when new dependencies have been added so that the environment.yml file gets updated
```
conda env export --from-history > environment.yml
```

## Updating Environment
Note: Make sure you activated the environment

Use this when you the .yml file has updated packages and the environment needs to be updated
```
conda env update --file environment.yml  --prune
```
