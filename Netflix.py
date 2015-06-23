#!/usr/bin/env python3

import json
from numpy import square, sqrt, subtract

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

    global rmsAccumulator # add to this the squared diff of values
    global rmsCounter #increment this by one after calc'ing above

    movieavgfile = open('/u/ebanner/netflix-tests/BRG564-Average_Movie_Rating_Cache.json')
    movied = json.load(movieavgfile, object_pairs_hook = dict)
    movieavgfile.close()
    
    solutions = open('/u/klt713/CS373/p2/cs373-netflix/solutions-trial.json')
    solutionsd = json.load(solutions, object_pairs_hook = dict)
    solutions.close()

    #each sublist in masterlist is a movie that we want to predict the rating of
    for sublist in masterlist :
      #key is the movie number
      key = sublist[0]
#      print("Key = " + str(key))

      #movieavg is the average rating of this movie
      movieavg = movied[str(key)]
      assert type(movieavg) is float
#      print("movied = " + str(movied))
      print("key = " + str(key) + ", movie average = " + str(movieavg))

      #solutiondd is the "customer: correct rating" pair list for this movie
      solutionsdd = solutionsd[str(key)]
      print("solutionsdd = " + str(solutionsdd))
      itersublist = iter(sublist)
      
      #next(itersublist) is the same thing as key (it's the movie ID)
      next(itersublist)

#          print("solution = " + str(solutiondd))
      for i in itersublist :
        customer = i
        print("Customer = " + str(customer))
        solution = solutionsdd[str(customer)]
        print("solution = " + str(solution))
        prediction = movieavg 
#        print("prediction = " + str(prediction))
        diffsquared = square(subtract(prediction, solution))
#        print("diffsquared = " + str(diffsquared))
        rmsAccumulator += diffsquared
        rmsCounter += 1

#    print(solutionsd)
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
    print("rmsAccumulator = " + str(rmsAccumulator))
    r = rmsAccumulator/rmsCounter
    return sqrt(r)
