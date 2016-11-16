# The program will implement our iPTRS algorithm and generate the set with
# size k
import basic_info
import numpy as np
from scipy.stats import pearsonr
from scipy.stats import spearmanr
from sklearn.metrics.pairwise import cosine_similarity
import discount as dis
import warnings

# Build the score function of a candidate set
def f(set, aspect, predict_distribution, delta, is_t,present,rate):
    marks = 0
    for review in set:
        if review[3][aspect] != 0:
            quality = 0
            if is_t :
                quality = review[1] * dis.discount(rate,dis.time_diff(review[2],present))
            else:
                quality = review[1]
            if(quality > marks):
                marks = quality
    return (predict_distribution[aspect]+delta)*marks

def F(top_set, predict_distribution,delta,is_t,present, rate,type):
    topics = []
    if type == "_Yelp":
        topics = basic_info.topics_Y
    else:
        topics = basic_info.topics_TA
    if top_set == []:
        return 0
    score = 0
    for aspect in range(len(topics)):
        score += f(top_set, aspect, predict_distribution,delta,is_t,present,rate)
    return score

#Define the aggreation function to predict the aspect importance distribution
def similarity(vector_1, vector_2 , mode):
    warnings.filterwarnings('error')
    result = 0
    if mode == 'P':
        try:
            result = pearsonr(vector_1,vector_2)[0]
        except:
            pass
    elif mode == 'C':
        try:
            cosine_similarity(vector_1,vector_2)[0]
        except:
            pass
    else:
        try:
            spearmanr(vector_1,vector_2)[0]
        except:
            pass
    return result

def g(x):
    if x <= 20:
        return x/20.0;
    return 1;

def aggregate_PTRS(user_id , prod_id, mode, is_t,present,rate,type):
    #build a dictionary to store the vectors of products in memory
    users = {}
    topics = []
    if type == "_Yelp":
        topics = basic_info.topics_Y
    else:
        topics = basic_info.topics_TA
    with open("users_distribution" + type + ".txt",'r') as f:
        for line in f:
            content = line.rstrip('\n').split(' ')
            users[content[0]] = np.array([float(number) for number in content[2:]])
    #Initial the result
    result = np.zeros(len(topics))
    #count the number of reviews the user wrote before,meanwhile update adjustment
    total_weight = 0.0
    with open("products" +type+'/'+prod_id+".txt") as f:
        for line in f:
            content = line.rstrip('\n').split(" ")
            weight = 0
            if(is_t):
                time = content[2]
                weight = similarity(users[content[0]],users[user_id],mode) + \
                         dis.discount(rate,dis.time_diff(time,present))
            else:
                weight = similarity(users[content[0]],users[user_id],mode)
            result += weight * users[content[0]]
            total_weight += weight
    result = (1.0/total_weight) * result
    return result

def aggregate_iPTRS(user_id , prod_id, mode, is_t,present,rate,type):
    #build a dictionary to store the vectors of products in memory
    products = {}
    topics = []
    if type == "_Yelp":
        topics = basic_info.topics_Y
    else:
        topics = basic_info.topics_TA
    with open("parsed information/products_distribution" + type + ".txt",'r') as f:
        for line in f:
            content = line.rstrip('\n').split(' ')
            products[content[0]] = np.array([float(number) for number in content[2:]])
    #Update the result to be the baseline vector of the product
    result = np.array(products[prod_id])
    adjustment = np.zeros(len(topics))
    #count the number of reviews the user wrote before,meanwhile update adjustment
    count = 0
    total_weight = 0.0
    with open("users" +type+'/'+user_id+".txt") as f:
        for line in f:
            content = line.rstrip('\n').split(" ")
            weight = 0
            if(is_t):
                time = content[2]
                weight = similarity(products[content[0]],products[prod_id],mode) + \
                         dis.discount(rate,dis.time_diff(time,present))
            else:
                weight = similarity(products[content[0]],products[prod_id],mode)
            adjustment += (np.array([float(x) for x in content[4:]]) - \
                          weight * products[content[0]])
            total_weight += weight
            count += 1
    result += g(count) * (1.0/total_weight) * adjustment
    #set it to zero if the value is small than 0
    result = [(lambda x :  0 if x < 0 else x )(x)for x in result]
    return result
# Suppoese the user did not write reviews to the product before
def iPTRS_derivation(user_id, prod_id, mode, size,delta, is_t, present,rate,type,base):
    predict_distribution = []
    if base == 'i':
        print("...Start do build the iPTRS")
        predict_distribution = aggregate_iPTRS(user_id, prod_id, mode,is_t,present,rate,type)
    else:
        print("...Start do build the PTRS")
        predict_distribution = aggregate_PTRS(user_id, prod_id, mode,is_t,present,rate,type)
    #print (predict_distribution)
    #Extract the info of reviews related to the product
    reviews = []
    with open("products"+ type +'/' + prod_id+".txt", 'r') as f:
        for line in f:
            content = line.strip('\n').split(' ')
            reviews.append((content[1],int(content[3]), content[2] , \
                    [float(x) for x in content[4:]]))
    iPTRS = []
    iPTRS_id = []
    #applying the greedy algorithm
    for i in range(size):
        delta_score = 0
        candidate = ()
        for r in reviews:
            #check whether the candidate is already in the set
            score = F(iPTRS + [r],predict_distribution,delta,is_t,present,rate,type)\
                    - F(iPTRS,predict_distribution,delta,is_t, present,rate,type)
            if score > delta_score :
                candidate = r
                delta_score = score
        if(candidate != ()):
            iPTRS.append(candidate)
            iPTRS_id.append(candidate[0])
    return iPTRS
