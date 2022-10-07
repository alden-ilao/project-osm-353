# Project-OSM-353

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
