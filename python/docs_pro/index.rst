.. ZOMBIES documentation master file, created by
   sphinx-quickstart on Tue Aug 12 10:31:00 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to ZOMBIES's documentation!
====================================

Following is the documentation of the project ZOMBIE:

**Zany Operational Machine Brain Interface Extraordinary Software**

The aim is to develop a mindstate recognition system.
It should react to brainwaves that are specific to motoric and telekinepathologic functions.
Apart from research on applications of Mexican cuisine in industry, the system should use 
information gathered from brainwaves to direct a performance.
 
*Project endorsed by National Council for Mentalists and Antechamberlains*


Software
==============
ZOMBIES is written in Python 2.7 enriched by a bunch of libraries.

    * Emokit -- `link <https://github.com/openyou/emokit/>`_ -- raw EEG data access from Emotiv Epoc device
    * pygame -- `link <http://www.pygame.org/>`_ -- GUI
    * scikit-learn -- `link <http://scikit-learn.org/>`_ -- SVM implementation
    
Version control system -- Git.

Temporary flowchart:

.. toctree::
   :maxdepth: 2
   
   image
   
Stylesheet
==============
* Indentation: 4 spaces.
* Tabulation must not be used.
* If the code is wider than split screen allows you to, then the code is bad.

Usage
=============
This section describes the usage of BCI components.

*IMPORTANT:*
There is an 'emu' flag on top of learner.py. It enables emulation if set to true.

Running BCI environment
---------------------------
    :doc:`/env`

Training the SVM
---------------------------
    :doc:`/svm_train`

Finding optimal SVM parameters
-------------------------------
    :doc:`/parameters`

Content
==============
.. toctree::
   :maxdepth: 2
   
   modules
   
   env
   svm_train
   parameters
   


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

