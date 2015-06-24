#!/usr/bin/env python3

# using modified:
# -------------------------------
# projects/collatz/TestCollatz.py
# Copyright (C) 2015
# Glenn P. Downing
# -------------------------------

# https://docs.python.org/3.4/reference/simple_stmts.html#grammar-token-assert_stmt

# -------
# imports
# -------

from io       import StringIO
from unittest import main, TestCase

from Netflix import netflix_read, netflix_eval, netflix_print, netflix_solve,netflix_rmse

import Netflix

# -----------
# TestCollatz
# -----------

class TestNetflix (TestCase) :
    # ----
    # read
    # ----

    def test_read (self) :
        s=StringIO("1:\n19\n"+"20\n")
        i = netflix_read(s)
        j= [[1,19,20]]
        self.assertEqual(i,  j)
        
    def test_read_2 (self) :
        s=StringIO("10:\n19\n"+"20\n"+"11:\n"+"20\n21\n")
        i = netflix_read(s)
        j= [[10,19,20],[11,20,21]]
        self.assertEqual(i,  j)
        
    def test_read_3 (self) :
        s=StringIO("99:\n19\n"+"22\n"+"101:\n"+"666\n666\n"+"666:\n999\n"+"20\n")
        i = netflix_read(s)
        j= [[99,19,22],[101,666,666],[666,999,20]]
        self.assertEqual(i,  j)

    # ----
    # eval
    # ----

    def test_eval_1 (self) :
        i=[[1,30878]]
        v = netflix_eval(i)
        self.assertEqual(v, [[1, 3.7196613523550819]])
        
    def test_eval_2 (self) :
        i=[[1,30878],[10,1952305]]
        v = netflix_eval(i)
        self.assertEqual(v, [[1, 3.7196613523550819], [10, 3.3260588580871548]])
        
    def test_eval_3 (self) :
        i=[[1,2647871],[10,1952305],[1000,97460]]
        v = netflix_eval(i)
        self.assertEqual(v, [[1, 3.5016072515479428], [10, 3.3260588580871548], [1000, 3.8824355945848912]])

    # -----
    # print
    # -----

    def test_print (self) :
        w = StringIO()
        netflix_print(w, 1, [1,10,11])
        self.assertEqual(w.getvalue(), "1:\n10.0\n11.0\n")

    def test_print_2 (self) :
        w = StringIO()
        netflix_print(w, 2, [1,5,6,6])
        self.assertEqual(w.getvalue(), "2:\n5.0\n6.0\n6.0\n")
      
    def test_print_3 (self) :
        w = StringIO()
        netflix_print(w, 3, [1,7,666])
        self.assertEqual(w.getvalue(), "3:\n7.0\n666.0\n")

    # -----
    # solve
    # -----

    def test_solve_1 (self) :
        i="1:\n30878\n"
        r=StringIO(i)
        w=StringIO()
        
        netflix_solve(r,w)
        self.assertEqual(w.getvalue(), '1:\n3.7\nRMSE: 0.28\n')
        
    def test_solve_2 (self) :
        i="1:\n30878\n10:\n1952305\n"
        r=StringIO(i)
        w=StringIO()
        
        netflix_solve(r,w)
        self.assertEqual(w.getvalue(), '1:\n3.7\n10:\n3.3\nRMSE: 0.29\n')
        
    def test_solve_3 (self) :
        i="1:\n2647871\n10:\n1952305\n1000:\n97460\n"
        r=StringIO(i)
        w=StringIO()
        
        netflix_solve(r,w)
        self.assertEqual(w.getvalue(), '1:\n3.5\n10:\n3.3\n1000:\n3.9\nRMSE: 0.55\n')

# ----
# netflix_rmse
# ----
    def test_rmse(self):
      Netflix.rmsAccumulator = 15
      Netflix.rmsCounter= 5
      self.assertEqual(netflix_rmse(),'1.73')
      Netflix.rmsAccumulator=0
      Netflix.rmsCounter=0
        
    def test_rmse_2(self):
      Netflix.rmsAccumulator = 25
      Netflix.rmsCounter= 5
      self.assertEqual(netflix_rmse(),'2.23')
      Netflix.rmsAccumulator=0
      Netflix.rmsCounter=0
    
    def test_rmse_3(self):
      Netflix.rmsAccumulator = 10
      Netflix.rmsCounter= 5
      self.assertEqual(netflix_rmse(),'1.41')
      Netflix.rmsAccumulator=0
      Netflix.rmsCounter=0
# ----
# main
# ----

if __name__ == "__main__" :
    main()
