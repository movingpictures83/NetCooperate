# NetCooperate
# Language: Python
# Input: Prefix (two metabolite network files)
# Output: TXT (cooperation statistics)
# Tested with: PluMA 1.0, Python 3.6

This is a PluMA plugin that takes two metabolic networks and runs 
NetCooperate (Levy et al, 2015) to compute the likelihood of cooperation
between the two corresponding entities.  These entities can be microbial
or the host.

The plugin accepts network files in a tabular format (.tab).  This is a simple
format where metabolic interactions are rows in a table, and the interacting metabolites the 
columns (separated by tabs), i.e.:

A	B
A	C

The plugin requires two of these files as input and therefore accepts a prefix.
It will then automatically concatenated "1.tab" and "2.tab" for the files.

The output TXT file contains statistics as to the likelihood of entities 1 and 2 cooperating,
plus key metabolites that could be involved in their cooperation.

Note: The plugin wraps the source code of NetCooperate, developed by the Borenstein lab
at University of Washington and available here:
http://elbo.gs.washington.edu/software_netcooperate.html

The version in this plugin was downloaded on October 5, 2018.  It is available under the lesser
GNU Public License, as is this plugin.  You can find a copy of this license inside this same
folder.

The example is also the basic example provided with their software.

