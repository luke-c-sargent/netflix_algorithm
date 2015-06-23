#!/usr/bin/env python3

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

def netflix_eval (i, j) :
    """
    i the ???
    j the ???
    return ???
    """
    # <your code>
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
    
    rmse = netflix_rmse(1, 2)
    w.write("rmse = " + str(rmse) + "\n")

# ----------------------
# netflix_rmse
# ----------------------
def netflix_rmse (ours,theirs):
    """
    ours is our calculated movie rating value
    theirs is the given value
    returns rmse
    """
    return 1

