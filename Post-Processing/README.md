# Post-Processing for Contiguity and Coverage

The SLA system attempts to group all municipalities in Canada into an SLA. However, there are some cases in which this can't be done. Municipalities in Canada can be suppressed for data quality or confidentality reasons, or they may have no population that commutes outside that municipality, or they may simply have no population at all. 

The result of this is that the initial output of the SLA system does not cover the entirety of Canada. This issue can be seen on the map below, where all the white areas represent municipalities that were excluded from the SLA system for one reason or another.

<p align="center">
  <img src="./img/example.png" alt="SLA example"
       width="654" height="540">
</p>

In addition, the SLA system itself does not require contiguity. Municipalities in the same SLA may be separated from each other by some distance, creating areas that are hard to visualize and difficult for users.

## Types of Issues

There are three main types of delineation issues presented by the SLA geography that have to be dealt with by post-processing:

The first type of issue occurs when an SLA cannot be surrounded by a single contiguous border. This can occur in a number of situations and is most closely analogous to the ‘holes’ concept seen in CMA/CA delineation rules. In these cases, modifications are made to the SLA either by adding or subtracting a CSD for the purpose of creating a cohesive group.

The second type of issue occurs when the areas delineated by the SLA geography intersect with the borders created by the statistical geographic classification. In the past, these cases were most closely related to the interaction between the CMA/CA delineation and the provincial borders. With the new form of the geography the issue of CMA/CA interaction has been eliminated, so only provincial reconciliation is needed.

The third type of issue occurs when a CSD has not been assigned to any SLA, either because it has no outside commuting flows or because it has been suppressed for the relevant year. These types of cases are unique to the SLA geography, as the CMA/CA geography is not intended to include every CSD of Canada, and so a custom solution had to be devised. 

## End Result

The end result of the post-processing program is a set of SLA that cover all municipalities in Canada and are, insofar as poissble, contiguous. For 2016, this included the creation of 98 pseudo-SLAs that cover the geographically large unpopulated areas of Canada.
