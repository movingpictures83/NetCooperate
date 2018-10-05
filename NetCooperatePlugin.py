#from __future__ import outfile.write_function
import sys
import SeedSet
import NetCooperate

#if len(sys.argv) != 3:
#    outfile.write(sys.argv[0], 'graph1 graph2');
#    exit();

# Our graph reading script
#  Reads a tab-separated file of edges
def readGraph(graphFile):
    
    graph={}
    for line in open(graphFile):
        
        vals = line.strip().split("\t");
        
        if len(vals[0])==0 or vals[0][0] == '#':
            continue     
        elif len(vals) != 2:
            outfile.write("Bad line: " + line)
            continue
        
        graph.setdefault(vals[0],[]).append(vals[1])
        
    return graph

class NetCooperatePlugin:
   def input(self, filename):
      self.graphFileOne=filename+"1.tab";
      self.graphFileTwo=filename+"2.tab";

      self.graphOne = readGraph(self.graphFileOne);
      self.graphTwo = readGraph(self.graphFileTwo);     

   def run(self):
      # Choose what we find important
      onlyGiant=False
      minComponentSize=0

      # Calculate the seed sets
      SeedsOne, self.SeedGroupsOne, self.nonSeedsOne, PrunedOne, self.NodesOne = SeedSet.calculate_seeds(self.graphOne,onlyGiant,minComponentSize)
      SeedsTwo, self.SeedGroupsTwo, self.nonSeedsTwo, PrunedTwo, self.NodesTwo = SeedSet.calculate_seeds(self.graphTwo,onlyGiant,minComponentSize)

      # Calculate the biosynthetic support
      #  The biosynthetic support compares the SeedGroups to All nodes in the other network
      self.bssOneOne, self.bssOneOneSupport = NetCooperate.compute_single_interaction_score(self.SeedGroupsOne,self.NodesOne)
      self.bssOneTwo, self.bssOneTwoSupport = NetCooperate.compute_single_interaction_score(self.SeedGroupsOne,self.NodesTwo)
      self.bssTwoOne, self.bssTwoOneSupport = NetCooperate.compute_single_interaction_score(self.SeedGroupsTwo,self.NodesOne)
      self.bssTwoTwo, self.bssTwoTwoSupport = NetCooperate.compute_single_interaction_score(self.SeedGroupsTwo,self.NodesTwo)

      # Calculate the metabolic complementarity
      #  The metabolic complementarity compares the SeedGroups to Non-Seed nodes in the other network
      self.mcOneOne, self.mcOneOneSupport = NetCooperate.compute_single_interaction_score(self.SeedGroupsOne,self.nonSeedsOne)
      self.mcOneTwo, self.mcOneTwoSupport = NetCooperate.compute_single_interaction_score(self.SeedGroupsOne,self.nonSeedsTwo)
      self.mcTwoOne, self.mcTwoOneSupport = NetCooperate.compute_single_interaction_score(self.SeedGroupsTwo,self.nonSeedsOne)
      self.mcTwoTwo, self.mcTwoTwoSupport = NetCooperate.compute_single_interaction_score(self.SeedGroupsTwo,self.nonSeedsTwo)

   def output(self, filename):
      outfile = open(filename, 'w')
      outfile.write("Example one: computing single interaction scores individually & reporting supported compounds.\n")
      outfile.write("biosynthetic support:\n")
      outfile.write("%s being supported by %s:\t%g\t%s\n" % (self.graphFileOne, self.graphFileOne, self.bssOneOne, ','.join(self.bssOneOneSupport)))
      outfile.write("%s being supported by %s:\t%g\t%s\n" % (self.graphFileOne, self.graphFileTwo, self.bssOneTwo, ','.join(self.bssOneTwoSupport)))
      outfile.write("%s being supported by %s:\t%g\t%s\n" % (self.graphFileTwo, self.graphFileOne, self.bssTwoOne, ','.join(self.bssTwoOneSupport)))
      outfile.write("%s being supported by %s:\t%g\t%s\n" % (self.graphFileTwo, self.graphFileTwo, self.bssTwoTwo, ','.join(self.bssTwoTwoSupport)))
      outfile.write("\n")
      outfile.write("metabolic complementarity:\n")
      outfile.write("%s being complemented by %s:\t%g\t%s\n" % (self.graphFileOne, self.graphFileOne, self.mcOneOne, ','.join(self.mcOneOneSupport)))
      outfile.write("%s being complemented by %s:\t%g\t%s\n" % (self.graphFileOne, self.graphFileTwo, self.mcOneTwo, ','.join(self.mcOneTwoSupport)))
      outfile.write("%s being complemented by %s:\t%g\t%s\n" % (self.graphFileTwo, self.graphFileOne, self.mcTwoOne, ','.join(self.mcTwoOneSupport)))
      outfile.write("%s being complemented by %s:\t%g\t%s\n" % (self.graphFileTwo, self.graphFileTwo, self.mcTwoTwo, ','.join(self.mcTwoTwoSupport)))

      ### Or use this all-in-one function call

      # This returns a two-tuple for each argument. tupple[0] is the support score, tupple[1] is the list of supported seeds
      BSSOneOnTwo, BSSTwoOnOne, MCOneOnTwo, MCTwoOnOne = NetCooperate.compute_all_interaction_scores(self.SeedGroupsOne,self.NodesOne,self.nonSeedsOne,self.SeedGroupsTwo,self.NodesTwo,self.nonSeedsTwo)

      outfile.write("\n---------------------------------------------------\n")
      outfile.write("Example two: computing all interaction scores in one call but not reporting supported compounds.\n")
      outfile.write("biosynthetic support:\n")
      outfile.write("%s being supported by %s:\t%g\n" % (self.graphFileOne, self.graphFileOne, BSSOneOnTwo[0]))
      outfile.write("%s being supported by %s:\t%g\n" % (self.graphFileOne, self.graphFileTwo, BSSTwoOnOne[0]))
      outfile.write("\n")
      outfile.write("metabolic complementarity:\n")
      outfile.write("%s being complemented by %s:\t%g\n" % (self.graphFileTwo, self.graphFileOne,  MCOneOnTwo[0]))
      outfile.write("%s being complemented by %s:\t%g\n" % (self.graphFileTwo, self.graphFileTwo,  MCTwoOnOne[0]))

