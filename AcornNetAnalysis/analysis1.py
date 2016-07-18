import pandas
import numpy
import networkx as nx
import matplotlib.pyplot as plt

# Read in a dataframe of the full consolidated data, hard coding dates and IDs
df = pandas.read_csv("../Data/cons_data.txt",  dtype={"Detection_date": int,
                                                      "Session_date": int,
                                                      "Session_loc": str,
                                                      "Bird_ID": str,
                                                      "Home_Location": str})
# Headings are: Detection_date, Detection_time, Tag_ID, Signal_strength, Connection,
# Unit, Session_date, Session_time, Session_loc, Bird_ID, Home_Location, Sex, Status

# Read in the base station locations
bs = pandas.read_csv("../Data/BS_locations_edit.csv", dtype={"Unit1": str,
                                                             "Unit2": str,
                                                             "Unit3": str,
                                                             "Unit6": str})

# Headings are: Date, Unit1, Unit2, Unit3, Unit6

# Question 1: How often is each individual associated with each location?
# Complications:
    # 1: Each individual has a minimum and maximum detection date (tag start, lost tag)
    # 2: Over the tagged interval (min date to max date), there are variable sessions and session lengths
    # 3: Individuals can have a value of 0 detections for each session - date combo
# Task 1: Pull number of detections for each individual for each location for each session

#Make a dictionary to hold the sorted info
#bird_to_loc = {}

#Make the network graph
#Gloc = nx.Graph()
Gbird = nx.Graph()

#Make a list of nodes to show
#loclist = [] #locations
#birdlist = [] #birds

#Make a temporal listing for all birds
timespan = {}

byBirdID = df.groupby("Bird_ID")["Session_date"] # group by bird ID, looking at detection dates only
for bird in df["Bird_ID"].unique(): # for each unique bird ID
    first_detect = byBirdID.get_group(bird).min() # bird first detected
    last_detect = byBirdID.get_group(bird).max() # bird last detected
    timespan[bird] = [first_detect,last_detect]
    print(bird + " part 1")

    # create a dataframe of only that timeframe for this bird
    #df_bird = df[(df["Session_date"] >= first_detect) & (df["Session_date"] <= last_detect)].loc[df["Bird_ID"] == bird]
    #bs_bird = bs[(bs["Date"] >= first_detect) & (bs["Date"] <= last_detect)].drop("Date", 1)

    # Count time-bounded df by location
    #df_byloc = df_bird.groupby(["Session_loc"])["Detection_time"].count()
    #bs_byloc = bs_bird.stack().value_counts()

    # Create the full graph + dictionary
    #birdlist.append(bird)
    #for loc in numpy.unique(bs_bird[['Unit1', 'Unit2', 'Unit3', 'Unit6']]):
        #if loc != "bad":
            #bird_to_loc[bird] = {}
            #bird_to_loc[bird][loc] = 0
            #Gloc.add_edge(bird,loc,weight=0) # Full graph
            #loclist.append(loc)

    #for loc, detects in df_byloc.iteritems():
        #if loc != "bad":
            #samples = bs_byloc[loc]
            #count = detects / samples
            #bird_to_loc[bird][loc] = count
            #Gloc.add_edge(bird,loc,weight=count) # Full graph

# Create a time-location dataframe
# bs_uniq = pandas.melt(bs, id_vars=['Date'], value_vars=['Unit1', 'Unit2', 'Unit3', 'Unit6'])

done_birds = []
for bird in timespan:
    comparison = {i:timespan[i] for i in timespan if i!=bird}
    df_time = df[(df["Session_date"] >= timespan[bird][0]) & (df["Session_date"] <= timespan[bird][1])]
    for bird2 in comparison:
        if bird2 in done_birds:
            pass
        else:
            df_both = df_time[(df_time["Session_date"] >= comparison[bird2][0]) &
                              (df_time["Session_date"] <= comparison[bird2][1])]
            IDs = df_both["Bird_ID"].unique()
            df2 = df_both.groupby(["Bird_ID","Session_date","Session_loc"])["Detection_time"].count()
            pos_overlap = df_both.groupby(["Bird_ID"])["Detection_time"].count()
            if bird in IDs and bird2 in IDs:
                Gbird.add_edge(bird,bird2,weight=0)
            try:
                print("..." + bird + " " + bird2)
                for (ID,date,loc), detects in df2.iteritems():
                    if (bird,date,loc) and (bird2,date,loc) in df2:
                        weight = (detects + df2[(bird2,date,loc)])/(pos_overlap[bird] + pos_overlap[bird2])
                        Gbird[bird][bird2]["weight"] = Gbird[bird][bird2]["weight"] + weight
            except KeyError:
                pass
    done_birds.append(bird)
    print(bird)

#edgelist = []
#for loc in loclist:
    #edgelist.append((loc,"5700"))

# Use the full graph, draw only the edges & nodes for 1 bird
#pos = nx.spring_layout(Gloc)
#nx.draw_networkx_nodes(Gloc,pos,node_size=200,nodelist=loclist)
#nx.draw_networkx_edges(Gloc,pos,alpha=0.1,edgelist)

# Write the graph to a file
nx.write_edgelist(Gbird, "../Data/Gbird_edgelist.gz")

# Draw the full bird network
pos = nx.spring_layout(Gbird)
nx.draw_networkx_nodes(Gbird,pos,node_size=200)
nx.draw_networkx_edges(Gbird,pos,alpha=0.1)

#Draw out the image
plt.draw()
plt.show()