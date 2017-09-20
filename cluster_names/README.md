# Clustering Names via Soundex / Levenshtein Distance
This program takes names from an external file, converts them using Soundex, and uses agglomerative clustering to create groups of similar names based on a matrix of their Levenshtein distances. The main file, `name_clusterer.py`, takes two arguments: a text file of names separated by line breaks, and the number of desired clusters.
