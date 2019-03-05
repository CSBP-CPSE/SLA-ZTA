# SLA-ZTA 
# Self-contained labour areas / Zones de travail autonomes

## Self-contained labour areas (SLA)
A self-contained labour area is a territorial unit where most of the residents with jobs are working in the area and most of the jobs in the area are filled by workers residing in the area.


## Zones de travail autonomes (ZTA)
Une zone de travail  autonome est une unité territoriale où la plupart des résidents employés  travaillent dans la zone délimitée et où la plupart des emplois sont occupés  par des résidents de cette zone.

## 2016 Self-contained labour areas (SLA)

For the newest iteration of the SLA project using 2016 Census of Population data, it was decided to use only rural flows in order to both better align the SLA system with other standard geographies and provide more information on labour markets outside of Census Metropolitan Areas (CMAs) and Census Agglomerations (CAs). The graphic below shows the final result.

<p align="center">
  <img src="./img/SLA_2016_Rural Only.png" alt="SLA example"
       width="654" height="540">
</p>

## Documentation and Prior Use
* https://www150.statcan.gc.ca/n1/pub/21-006-x/21-006-x2008008-eng.htm
* http://guelph2016.crrf.ca/wp-content/uploads/2016/10/BVRF2016Alasia.pdf

## How It Works

Self-Contained Labour Areas is a tool to create self-contained areas.
It is designed to take a set of commuting flows between areas of any type
and group them into clusters meeting a users definition for self-containment.

This is a experimental Python port of the original code implemented in SAS
to create self-contined labour areas for the municipalities of Canada.

## Usage

First, install `SLA-ZTA`:

```
$ pip install https://github.com/CSBP-CPSE/SLA-ZTA
```

Import the package into your program and call the clustering function as in the following example, using the default values for each variable:  

```
from SLA-ZTA import SLA

SLA.main(test.csv, 4574, 0, 2500, 0.75, 0.90)
```

The variables required to run the program are, in this order:
* inputFile - a CSV file with three columns: RES, POW, and TotalFlow. Original RES and POW codes should be mapped to numbers from 1 to the total number of areas.
* numberOfAreas - integer value of highest area present in input file
* lowestPopulation - smallest population eligible to be a successful cluster, and value associated with highest required self-containment. Default 0.
* highestPopulation - largest population, used only for setting highest self-containment endpoint. Default 25,000.
* lowestSelfContainment - the lowest level of self-containment required for a cluster to be considered viable. Applies to the area with the highest population by default. Default 0.75.
* highestSelfContainment - the highest level of self-containment required for a cluster to be considered viable. Applies to the area with the lowest population by default. Default 0.90.

This code is created and maintained by the Centre for Special Business Projects, Statistics Canada.

