import pandas

# Read in a dataframe of the full consolidated data, hard coding dates and IDs
df = pandas.read_csv("../Data/test_data.txt",  dtype={"Detection_date": int,
                                                      "Session_date": int,
                                                      "Bird_ID": str})
# Headings are: Detection_date,Detection_time,Tag_ID,Signal_strength,Connection,
# Unit,Session_date,Session_time,Session_loc,Bird_ID,Home_Location,Sex,Status

# Question 1: How often is each individual associated with each location?
# Complications:
    # 1: Each individual has a minimum and maximum detection date (tag start, lost tag)
    # 2: Over the tagged interval (min date to max date), there are variable sessions and session lengths
    # 3: Individuals can have a value of 0 detections for each session - date combo
# Task 1: Pull number of detections for each individual for each location for each session

byBirdID = df.groupby("Bird_ID")["Session_date"] # group by bird ID, looking at detection dates only
for bird in df["Bird_ID"].unique(): # for each unique bird ID
    first_detect = byBirdID.get_group(bird).min() # bird first detected
    last_detect = byBirdID.get_group(bird).max() # bird last detected
    days_on = last_detect - first_detect + 2
    #print(bird, first_detect, last_detect, days_on)
    # create a dataframe of only that timeframe
    df_new = df[(df["Session_date"] >= first_detect) & (df["Session_date"] <= last_detect)]
    df_bird = df_new.loc[df_new["Bird_ID"] == bird]
    # Count time-bounded df by unique session
    bySessionID = df_bird.groupby(["Session_date","Session_loc"])["Detection_time"].count()
    print(bySessionID)






#counts = df.groupby(["Bird_ID","Session_date","Session_loc"]).count()
#print(counts)