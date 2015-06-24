#!/usr/bin/env python3

import json
from numpy import square, sqrt, subtract, clip, mean
from urllib.request import urlopen

rmsAccumulator=0
rmsCounter=0

# ------------
# netflix_read
# ------------

def netflix_read (r) :
    """
    r - a reader, reads in all movie IDs or customer IDs
    returns masterlist, which is a list of lists; each sublist containing the 
      movie id as the first element, and the customer ids as the following 
      elements.
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
    masterlist - the list of sublists. Each sublist contains a movie ID as the
      first element, and the customer IDs as the following elements.
    returns the modified masterlist, containing predictions for each movie
      rating, based on a combination of the average rating per movie, the
      average rating per user, and the variance of the user's rating history.
    """

    assert type(masterlist) is list

    global rmsAccumulator # add to this the squared diff of values
    global rmsCounter #increment this by one after calc'ing above

    movieavgfile = urlopen("http://www.cs.utexas.edu/~ebanner/netflix-tests/BRG564-Average_Movie_Rating_Cache.json")
    movied = json.loads(movieavgfile.read().decode(movieavgfile.info().get_param('charset') or 'utf-8'), object_pairs_hook = dict)
    movieavgfile.close()
    
    useravgfile = urlopen("http://www.cs.utexas.edu/~ebanner/netflix-tests/ezo55-Average_Viewer_Rating_And_Variance_Cache.json")
    useravgd = json.loads(useravgfile.read().decode(useravgfile.info().get_param('charset') or 'utf-8'), object_pairs_hook = dict)
    useravgfile.close()

    maxVariance=max([int(j) for i,j in useravgd.values()])
    avgRating=mean([int(i) for i in movied.values()])
    solutions = urlopen("http://www.cs.utexas.edu/~ebanner/netflix-tests/pam2599-probe_solutions.json")
    solutionsd = json.loads(solutions.read().decode(solutions.info().get_param('charset') or 'utf-8'), object_pairs_hook = dict)
    solutions.close()

    predictionlist = []
    predictionsublist = []

    #each sublist in masterlist is a movie that we want to predict the rating of
    for sublist in masterlist :

      #key is the movie number
      key = sublist[0]

      #movieavg is the average rating of this movie
      movieavg = movied[str(key)]
      assert type(movieavg) is float

      #solutiondd is the "customer: correct rating" pair list for this movie
      solutionsdd = solutionsd[str(key)]
      itersublist = iter(sublist)
      next(itersublist)

      for index, i in enumerate(itersublist, start = 1) :
        customer = i
        useravgdd = useravgd[str(customer)]
        userrating = useravgdd[0]
        uservar = useravgdd[1]

        assert type(uservar) is float

        solution = solutionsdd[str(customer)]
        if uservar != 0 :
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
          prediction = clip(kernel,0,5)

        sublist[index] = prediction
        diffsquared = square(subtract(prediction, solution))
        rmsAccumulator += diffsquared
        rmsCounter += 1

    assert rmsAccumulator is not None
    assert rmsCounter > 0

    return masterlist

# -------------
# netflix_print
# -------------

def netflix_print (w, movieid, ratings) :
    """
    print three ints
    w         a writer
    movieid   the movie ID number
    ratings   the list of ratings
    returns nothing, but prints the movie ID and predicted customer rating
    """

    assert type(movieid) is int
    assert movieid > 0
    assert type(ratings) is list


    w.write(str(movieid) + ":\n")
    count = 1
    length = len(ratings)
    while (count < length) :
      formattedfloat = "{0:.1f}".format(ratings[count])
      w.write(str(formattedfloat) + "\n")
      count += 1

# -------------
# netflix_solve
# -------------

def netflix_solve (r, w) :
    """
    r a reader
    w a writer
    performs the netflix prediction calculations, writes out the RMSE.
    """
    masterlist = netflix_read(r)
    length = len(masterlist)
    predictionlist = netflix_eval(masterlist)

    count = 0
    while (count < length) :
      #do stuff
      arr = predictionlist[count]
      movieid = arr[0]
      netflix_print(w, movieid, arr)
      count += 1

    assert count > 0

    rmse = netflix_rmse()

    assert float(rmse) > 0
    assert type(rmse) is str
    w.write("RMSE: " + str(rmse) + "\n")

# ----------------------
# netflix_rmse
# ----------------------
def netflix_rmse ():
    """
    returns the RMSE. function performs final calculations on globals that have
      been accumulating values.
    """
    global rmsAccumulator
    global rmsCounter

    assert rmsCounter > 0
    assert rmsAccumulator > 0

    r = rmsAccumulator/rmsCounter

    assert r > 0

    root = sqrt(r)
    root=int(root*100)/100.0
    formattedroot = "{0:.2f}".format(root)
    return formattedroot
