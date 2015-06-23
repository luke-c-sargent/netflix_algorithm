#!/usr/bin/env python3

import json
rmsAccumulator=0
rmsCounter=0

# ------------
# netflix_read
# ------------

def netflix_read (r) :
    """
    s a string, either the movie ID or the customer ID
    returns nothing. updates global masterlist, which is a list of lists; each
      sublist containing the movie id as the first element, and the customer
      ids as the following elements.
    """

    global rmsAccumulator # add to this the squared diff of values
    global rmsCounter #increment this by one after calc'ing above
    sublist = []
    masterlist = []
    s1 = r.readline()
    s2 = s1.replace(":\n", "")
    sublist.append(int(s2))

    for s in r :
      if ":" in s or s == "\n":
        masterlist.append(sublist)
        sublist = []
        strnocolon = s.replace(":", "")
        sublist.append(int(strnocolon))
      else :
        sublist.append(int(s))
   
    masterlist.append(sublist)

    return masterlist

# ------------
# netflix_eval
# ------------

def netflix_eval (masterlist) :
    """
    """
    movieavg = open('/u/ebanner/netflix-tests/BRG564-Average_Movie_Rating_Cache.json')
    movied = json.load(movieavg, object_pairs_hook = dict)
    movieavg.close()
    
    solutions = open('/u/klt713/CS373/p2/cs373-netflix/solutions-trial.json')
    solutionsd = json.load(solutions, object_pairs_hook = dict)
    solutions.close()

    print(solutionsd)
    return 1

# -------------
# netflix_print
# -------------

def netflix_print (w, movieid, ratings, i) :
    """
    print three ints
    w         a writer
    movieid   the movie ID number
    ratings   the array of ratings
    length    the number of ratings in the array
    rmse      the root mean square error
    """
    w.write(str(movieid) + ":\n")
    count = 1
    length = len(ratings)
    while (count < length) :
      w.write(str(ratings[count]) + "\n")
      count += 1

# -------------
# netflix_solve
# -------------

def netflix_solve (r, w) :
    """
    r a reader
    w a writer
    """
    masterlist = netflix_read(r)
    
    length = len(masterlist)

    count = 0
    while (count < length) :
      #do stuff
      arr = masterlist[count]
      movieid = arr[0]
      netflix_print(w, movieid, arr, len(arr))
      count += 1
  
    netflix_eval(masterlist)

    rmse = netflix_rmse()
    w.write("rmse = " + str(rmse) + "\n")

# ----------------------
# netflix_rmse
# ----------------------
def netflix_rmse ():
    """
    globals that have been accumulating values
    have final calculations performed on them
    """
    global rmsAccumulator
    global rmsCounter
#    r = rmsAccumulator/rmsCounter
#    return sqrt(r)
    return 1
