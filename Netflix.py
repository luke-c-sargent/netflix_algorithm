#!/usr/bin/env python3

import json
from numpy import square, sqrt, subtract, clip, mean

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

    useravgfile = open('/u/ebanner/netflix-tests/ezo55-Average_Viewer_Rating_And_True_Variance_Cache.json')
    useravgd = json.load(useravgfile, object_pairs_hook = dict)
    useravgfile.close()

    maxVariance=max([int(j) for i,j in useravgd.values()])
    avgRating=mean([int(i) for i in movied.values()])
    solutions = open('/u/ebanner/netflix-tests/pam2599-probe_solutions.json')
    solutionsd = json.load(solutions, object_pairs_hook = dict)
    solutions.close()

    predictionlist = []
    predictionsublist = []

    #each sublist in masterlist is a movie that we want to predict the rating of
    for sublist in masterlist :

      #key is the movie number
      key = sublist[0]
#      predictionsublist.append(key)

      #movieavg is the average rating of this movie
      movieavg = movied[str(key)]
      assert type(movieavg) is float
#      print("movied = " + str(movied))
#      print("key = " + str(key) + ", movie average = " + str(movieavg))

      #solutiondd is the "customer: correct rating" pair list for this movie
      solutionsdd = solutionsd[str(key)]
#      print("solutionsdd = " + str(solutionsdd))
      itersublist = iter(sublist)
      next(itersublist)

      #listsublist = list(itersublist)
      #next(itersublist) is the same thing as key (it's the movie ID)

      for index, i in enumerate(itersublist, start = 1) :
        customer = i
        useravgdd = useravgd[str(customer)]
        userrating = useravgdd[0]
        uservar = useravgdd[1]
#        print("User average rating: " + str(userrating) + "user variance: " + str(uservar))
        solution = solutionsdd[str(customer)]
#        print("Customer = " + str(customer) + "solution = " + str(solution))
        if uservar == 0 :
          prediction = userrating
        else :
          modStrength=.6
          userweight=modStrength *((maxVariance-uservar)/maxVariance)
          movieweight=1-userweight

          #how does the user generally vote?
          attitude=1
          upper=avgRating
          lower=upper
          tudeMod=.05
          attitude=1+((userrating-avgRating)/5)*tudeMod

          kernel=attitude*(movieweight*movieavg + userweight*userrating)
          #kernel=0.5*movieavg+0.3*userrating+0.2*avgRating
          prediction = clip(kernel,0,5)


          #print("mAvg:"+str(movieavg)+" uRating:"+str(userrating)+" uw:"+str(userweight)+" mw:"+str(movieweight))
          #print("pred:"+str(prediction)+" actual:"+str(solution)+ " var:"+str(uservar)+" a:"+str(attitude))

        sublist[index] = prediction
#        print("prediction = " + str(prediction))
        diffsquared = square(subtract(prediction, solution))
#        print("diffsquared = " + str(diffsquared))
        rmsAccumulator += diffsquared
        rmsCounter += 1

#    print(solutionsd)
    return masterlist

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
      formattedfloat = "{0:.1f}".format(ratings[count])
#      w.write(str(ratings[count]) + "\n")
      w.write(str(formattedfloat) + "\n")
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

    predictionlist = netflix_eval(masterlist)

    count = 0
    while (count < length) :
      #do stuff
      arr = predictionlist[count]
      movieid = arr[0]
      #netflix_print(w, movieid, arr, len(arr))
      count += 1


    rmse = netflix_rmse()
    #w.write("RMSE: " + str(rmse) + "\n")
    print("RMSE: " + str(rmse) + "\n")

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
#    print("rmsAccumulator = " + str(rmsAccumulator))
    r = rmsAccumulator/rmsCounter

    root = sqrt(r)
    #formattedroot = "{0:.2f}".format(root)
    root=int(root*100)/100.0
    formattedroot = "{0:.2f}".format(root)
    return formattedroot
