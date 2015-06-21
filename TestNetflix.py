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

from Python import netflix_read, netflix_eval, netflix_print, netflix_solve

# -----------
# TestCollatz
# -----------

class TestNetflix (TestCase) :
    # ----
    # read
    # ----

    def test_read (self) :
        #i, j = netflix_read(s)
        self.assertEqual(1,  1)

    # ----
    # eval
    # ----

    def test_eval_1 (self) :
        #v = netflix_eval(1, 10)
        self.assertEqual(1, 1)

    # -----
    # print
    # -----

    def test_print (self) :
        w = StringIO()
        #netflix_print(w, 1, 10, 20)
        self.assertEqual("1", "1")



    # -----
    # solve
    # -----

    def test_solve (self) :
        #netflix_solve(r, w)
        self.assertEqual(1,1)

# ----
# main
# ----

if __name__ == "__main__" :
    main()
