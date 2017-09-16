import argparse
import re
import os
import csv
import math
import collections as coll
import numpy as np


def parse_argument():
    """
    Code for parsing arguments
    """
    parser = argparse.ArgumentParser(description='Parsing a file.')
    parser.add_argument('--train', nargs=1, required=True)
    parser.add_argument('--test', nargs=1, required=True)
    args = vars(parser.parse_args())
    return args

def parse_file(filename):
    """
    Given a filename outputs user_ratings and movie_ratings dictionaries

    Input: filename

    Output: user_ratings, movie_ratings
        where:
            user_ratings[user_id] = {movie_id: rating}
            movie_ratings[movie_id] = {user_id: rating}
    """
    user_ratings = coll.defaultdict(dict)
    movie_ratings = coll.defaultdict(dict)
    f = open(filename, 'rb')
    f = csv.reader(f)
    for row in f:
        user_ratings[int(row[1])][int(row[0])] = float(row[2])
        movie_ratings[int(row[0])][int(row[1])] = float(row[2])
    return user_ratings, movie_ratings

def compute_average_user_ratings(user_ratings):
    """ Given a the user_rating dict compute average user ratings

    Input: user_ratings (dictionary of user, movies, ratings)
    Output: ave_ratings (dictionary of user and ave_ratings)
    """
    ave_ratings = coll.defaultdict(float)
    for key in user_ratings:
        ave_ratings[key] = np.mean(user_ratings[key].values())
    return ave_ratings

def compute_user_similarity(d1, d2, ave_rat1, ave_rat2):
    """ Computes similarity between two users

        Input: d1, d2, (dictionary of user ratings per user) 
            ave_rat1, ave_rat2 average rating per user (float)
        Ouput: user similarity (float)
    """
    i_set = set(d1) & set(d2)
    if not i_set:
        return 0.0
    num = 0
    den1 = 0
    den2 = 0
    for i in i_set:
        num += (d1[i]-ave_rat1)*(d2[i]-ave_rat2)
        den1 += (d1[i]-ave_rat1)**2
        den2 += (d2[i]-ave_rat2)**2
    if den1 == 0 or den2 == 0:
        return 0.0
    w_ij = num / math.sqrt(den1 * den2)
    return w_ij

# optional, since the parser doesn't count lines?
# faster than counting # of elements in all sub-dicts?
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def main():
    """
    This function is called from the command line via
    
    python cf.py --train [path to filename] --test [path to filename]
    """
    args = parse_argument()
    train_file = args['train'][0]
    test_file = args['test'][0]
    print train_file, test_file

    train_ur,  train_mr = parse_file(train_file)
    test_ur, test_mr = parse_file(test_file)

    pred_dict = coll.defaultdict(dict)
    diff_list = []

    avg_u = compute_average_user_ratings(train_ur)

    output = open("predictions.txt", "w")
    writer = csv.writer(output)

    for user_i in test_ur:
        avg_ui = avg_u[user_i]
        for movie_k in test_ur[user_i]:
            j_users = train_mr[movie_k]

            avg_j_users = [avg_u[j] for j in j_users]
            rating_j_users = [train_ur[j][movie_k] for j in j_users]
            ws = [compute_user_similarity(
                train_ur[user_i], train_ur[j], avg_u[user_i], avg_u[j])
                  for j in j_users]

            if not ws or sum(map(abs, ws)) == 0:
                pred_dict[user_i][movie_k] = avg_ui
            else:
                secondsum = [ws[x] * (rating_j_users[x] - avg_j_users[x]) for x in range(len(j_users))]
                pred_dict[user_i][movie_k] = avg_ui + ((1 / sum(map(abs, ws))) * sum(secondsum))

            writer.writerow([movie_k, user_i, test_ur[user_i][movie_k], pred_dict[user_i][movie_k]])
            diff_list.append(test_ur[user_i][movie_k] - pred_dict[user_i][movie_k])


    n = len(diff_list)
    rmse = math.sqrt(sum(map(lambda x: x**2, diff_list))/n)
    mae = (1/float(n)) * sum(map(abs, diff_list))
    print 'RMSE: ', rmse
    print 'MAE: ', mae

    output.close()

if __name__ == '__main__':
    main()

