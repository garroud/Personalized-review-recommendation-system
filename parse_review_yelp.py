#This program is used to generate the dsitribution of
#all the features of restuants listed in Yelp.com
import numpy as np
import os
import basic_info
import re

#Parse the reviews to aspect importance distribution
def parse_text(topics,text):
    aspect_importance_dist =np.zeros(len(topics))
    text_split = re.split(r'[?!.;\n]\s*',text)
    for sentence in text_split:
        temp = np.zeros(len(topics))
        words = re.split(r'[,\s\'\"()\[\]\{\}]\s*',sentence)
        total = 0
        for word in words:
            if topics.count(word) != 0:
                total += 1
                temp[topics.index(word)] += len(words)
        if total != 0:
            temp = 1/float(total) * temp
            aspect_importance_dist += temp
    #normalize the result so that the sum  = 1
    if (sum(aspect_importance_dist) != 0):
        aspect_importance_dist = [float(result)/sum(aspect_importance_dist) \
                                  for result in aspect_importance_dist]
    return aspect_importance_dist

def build_file_sys():
    print("...Parse the raw data from internet\n")
    #file_name = raw_input("\nInput the name of source file: ")

    #Store aggregated result of parsing in parsed_reviews.txt
    fo = open("parsed information/parsed_reviews_Yelp.txt",'w+')
    with open('parsed information/yelp_r_review_details.txt','r') as f:
        for line in f:
            user_id = line[line.find("user_id")+11 : line.find("\"",line.find("user_id")+11)]
            prod_id = line[line.find("business_id")+15 : -3]
            review_id = line[line.find("review_id")+13: line.find("\"",line.find("review_id")+13)]
            quality = 1 + int(line[line.find("useful")+9 : line.find(",",line.find("useful")+9)])
            date = line[line.find("\"date\"")+9 : line.find("\"date\"")+19]
            text = line[line.find("text")+8 : line.find('", "type"')]
            aspect_importance_dist = parse_text(basic_info.topics_Y, text)
            # Classify the reviews by users
            if not os.path.exists("users_Yelp/"+user_id+".txt"):
                fo_u = open("users_Yelp/"+user_id+".txt", 'w+')
            else:
                fo_u = open("users_Yelp/"+user_id+".txt", 'a')
            # Classify the reviews by products
            if not os.path.exists("products_Yelp/"+prod_id+".txt"):
                    fo_p = open("products_Yelp/"+prod_id+".txt", 'w+')
            else:
                fo_p = open("products_Yelp/"+prod_id+".txt", 'a')
            fo.write(user_id + ' ' + prod_id +' '+ review_id +' '+ date + ' '+ str(quality))
            fo_u.write(prod_id +' '+ review_id +' ' + date + ' ' + str(quality))
            fo_p.write(user_id +' '+ review_id +' ' + date + ' ' +str(quality))
            for number in aspect_importance_dist:
                fo.write(' ' + str(number))
                fo_u.write(' ' + str(number))
                fo_p.write(' ' + str(number))
            fo.write('\n')
            fo_u.write('\n')
            fo_p.write('\n')
            fo_u.close()
            fo_p.close()
        fo.close()
        print("...Parsing completes\n")
