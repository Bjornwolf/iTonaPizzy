#!/usr/bin/python
# -*- coding: utf-8 -*-

"""A simple non-deterministic grammar framework class."""

import random

class Grammar(object):
    def __init__(self, starting_word, nonterminals, productions):
        """Constructs the grammar.
        
        **Keyword arguments:**
            * starting word -- a string consisting of terminals and nonterminals
            * nonterminals -- list of nonterminal characters
            * productions -- a dictionary of grammatic productions in {nonterminal: [(result, weight)]}; A -> aA | bA translates to {'A': [("aA",1), ("bA,1)]}
            
        """
        self.nonterminals = nonterminals
        self.productions = productions
        self.word = starting_word
        self.nonterminals_in_word = []
        nonts = []
        ctr = 0
        for l in self.word:
            if l in nonterminals:
                nonts.append(ctr)
                ctr = 0
            else:
                ctr += 1
        self.nonterminals_in_word = nonts
            
        
    def swap_productions(self, productions):
        """Inserts a new production set into the grammar. Returns nothing.
        
        **Keyword arguments:**
            * productions -- defined as in the constructor"""
        self.productions = productions
        
    def make_production(self):
        """Does one step for the left-most nonterminal. Returns nothing."""
    
        if self.nonterminals_in_word == []:
            return
        first = self.nonterminals_in_word[0]
        self.nonterminals_in_word = self.nonterminals_in_word[1:]
        nont = self.word[first]
        prod = self.choose(nont)
        self.word = self.word[:first] + prod + self.word[first+1:]
        new_nonterminals = []
        ctr = first
        for i in prod:
            if i in self.nonterminals:
                new_nonterminals.append(ctr)
                ctr = 0
            else:
                ctr += 1
        if ctr == len(self.word):
            self.nonterminals_in_word = []
        elif self.nonterminals_in_word == []:
            self.nonterminals_in_word = new_nonterminals + [ctr]
        else:
            self.nonterminals_in_word[0] += ctr
            self.nonterminals_in_word = new_nonterminals + self.nonterminals_in_word
            
    def choose(self, nonterminal):
        """Selects the appropriate production.
        
        **Keyword arguments:**
            * nonterminal -- the nonterminal from which to produce.
            
        Returns the chosen production."""
    
        choice = self.productions[nonterminal]
        weight_sum = reduce(lambda (a,b), (c,d): (a,b+d), choice)[1]
        rand = random.randint(1, weight_sum)
        for (p, w) in choice:
            if rand <= w:
                return p
            rand -= w
            
    def show_word(self):
        """Substracts the longest terminal prefix from the word and returns it."""
    
        if self.nonterminals_in_word == []:
            word = self.word
            self.word = ""
            return word
        word = self.word[:self.nonterminals_in_word[0]]
        self.word = self.word[self.nonterminals_in_word[0]:]
        self.nonterminals_in_word[0] = 0
        return word