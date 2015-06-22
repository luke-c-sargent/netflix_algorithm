#!/usr/bin/env python3

masterlist = []
sublist = []

# ------------
# netflix_read
# ------------

def netflix_read (s) :
    """
    s a string, either the movie ID or the customer ID
    returns nothing. updates global masterlist, which is a list of lists; each
      sublist containing the movie id as the first element, and the customer 
      ids as the following elements.
    """

    global masterlist
    global sublist

    listcopy = sublist[:]

    if ":" in s :
      if len(listcopy) > 0 :
        masterlist.append(listcopy)
      sublist = []
      strnocolon = s.replace(":", "")
      sublist.append(int(strnocolon))
    else :
      sublist.append(int(s))


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

def netflix_print (w, movieid, ratings, i, rmse) :
    """
    print three ints
    w         a writer
    movieid   the movie ID number
    ratings   the array of ratings
    length    the number of ratings in the array
    rmse      the root mean square error
    """
    w.write(str(movieid) + ":")
    count = 0
    length = len(ratings)
    while (count < length) :
#      print("hi");
      w.write(str(ratings[count]) + "\n")
      count += 1

    w.write("RMSE: " + rmse)

# -------------
# netflix_solve
# -------------

def netflix_solve (r, w) :
    """
    r a reader
    w a writer
    """
    global masterlist

    for s in r :
        netflix_read(s)

    length = len(masterlist)
    count = 0

    while (count < length) :
      #do stuff
      arr = masterlist[count]
      movieid = arr[0]
      netflix_print(w, movieid, arr, len(arr), "rmse")
      count += 1
