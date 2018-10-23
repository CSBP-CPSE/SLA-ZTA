# Quick Documentation

## Rationale

Current geographical and analytical constructions of labour markets in Canada often focus attention on large urban centers of population and employment due to the fact that these centers represent a large percentage of the overall employed Canadian labour force.   The main way to delineate labour markets in Canada are the Census Metropolitan Areas (CMAs) and Census Agglomerations (CAs), whose delineation is predicated on the initial identification of an urban core and the subsequent grouping of all areas strongly related to that core. Thus, each CMA and CA can be said to represent a self-contained labour market centered on an urban core.   

Efforts have been made to add definition to the non-urban areas of Canada, particularly through the Metropolitan Influence Zone (MIZ) classification system.  This system divides all areas in Canada into a stratum depending on the percentage of the working population that commutes to work in any CMA or CA, which acts to differentiate and the areas to some degree. However, what was lacking is any delineation of self-contained labour markets outside of CMAs and CAs.

The Self-Contained Labour Areas (SLAs) were created to provide more information on labour markets outside of CMA/CAs, and specifically to identify whether areas outside of CMA/CAs formed independent groupings.

## Data Source

The commuting data sets used to create the labour market areas were derived from the Canadian Census of Population.  These data sets are created using information from the place of work questions on the long questionnaire delivered to 20% of the Canadian population; data on the other 80% of the population is generated from these responses using multi-variable imputation. Each commuting flow used in this analysis contained three elements:  an origin location derived from the place of residence of each respondent, a destination location derived from the place of work of each respondent, and a rounded count of the number of commuters who travel from the origin to the destination for the purpose of work.

There are several criteria that must be met before a respondent will be included in a flow count produced by the census.   These criteria are that the respondent:  
•	Be above or equal to 15 years of age;
•	Be in the employed labour force in that they;
•	Worked some amount of hours in the week prior to the census or
•	Worked at some point between January 1, 2005 and census day; and .
•	Respond that they have a usual place of work and entered a locatable response into one or more of the place of work address fields  

## Methodology

The methodology used is to start from the census subdivision with the least self-containment, defined as the average of the percentage of their residents working outside the area and the percentage of their workers coming from outside the area. That area is then joined with the area with which it has the strongest reciprocal commuting relationship, as follows:

```
 (Fa,b) * (Fa,b) + (Fb,a) *  (Fb,a)
   Ra       Wb       Rb        Wa                            

Fa,b is the number of journeys to work from area A to area B; 
Fb,a is the number of journeys to work from area B to area A; 
Ra is the number of workers who live in area A; 
Wa is the number of people who work in area A;
Rb is the number of workers who live in area B; 
Wb is the number of people who work in area B;
```
This grouping then restarts, continuing until every eligible area has been grouped into a cluster that meets the minimum standard for self-containment. In order to prevent larger areas from drawing in huge agglomerations of surrounding CSDs, the required standard of self-containment decreases as the areas increase in population. 

For all current iterations of the SLA system, the thresholds have been a sliding scale where a hypothetical area with zero population would require 90% self-containment and a hypothetical area with 25,000 population would require 75%.




