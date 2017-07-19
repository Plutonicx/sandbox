import os
import SampleModule as sm
import distance
import pickle
import boto3

def lambda_handler(event, context):
    word_1 = os.environ.get("word_1")
    word_2 = os.environ.get("word_2")

    lev_dist = distance.levenshtein(str(word_1),str(word_2))

    builder = "the distance between word 1 and word 2 is: " + str(lev_dist)

    print(builder)

    val = sm.square_root_it(4)

    print(str(val))

    return(lev_dist)
