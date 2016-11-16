#set up the experimentation between PTRS and iPTRS
import parse_review_yelp as pry
import prod_distribution as pd
import os
import shutil
import iPTRS
import random
from datetime import date
#generate a random set of user_id and product_id for testing
def random_test():
    users = [f[:-4] for f in os.listdir('./users_Yelp')]
    prods = [f[:-4] for f in os.listdir('./products_Yelp')]
    random.seed()
    while (True):
        user_id = users[random.randrange(len(users)-1)]
        prod_id = prods[random.randrange(len(prods)-1)]
        is_valid = True
        with open("products_Yelp/"+prod_id+".txt",'r') as f:
            for line in f:
                if user_id  == line[:len(user_id)]:
                    is_valid = False
                    break;
        if is_valid:
            return user_id, prod_id

#main program for experimentation
print ("...Begin a new experimentation")
check = input("rebuild the file system?[y/n]")
if check == 'y':
    #build the file system
    shutil.rmtree('users_Yelp')
    shutil.rmtree('products_Yelp')
    os.remove('products_distribution_Yelp.txt')
    os.remove('parsed_reviews_Yelp.txt')
    os.mkdir('users_Yelp')
    os.mkdir('products_Yelp')
    pry.build_file_sys()
is_t = input("Consider the time factor?[y/n]")
rate = 0
check_t = False
if is_t == 'y':
    check_t = True
    rate = input("Input how fast will the value discount: ")
    pd.get_prod_distribution(is_t,date.today(),rate, '_Yelp')
else:
    pd.get_prod_distribution(check_t, date.today(), 0, '_Yelp')
while True:
    random_play = input("Random?[y/n]")
    user_id = ''
    random_id = ''
    if random_play == 'y':
        print("...random generate a combination of user_id and prod_id for testing")
        user_id, prod_id = random_test()
    else:
        user_id = input("input user id: ")
        prod_id = input("input product id: ")
    print ('user_id: %s , prod_id: %s' % (user_id,prod_id))
    result = iPTRS.iPTRS_derivation(user_id, prod_id, 'P', 3, 0.001,check_t,date.today(),rate,'_Yelp')
    print ('user_id: %s , prod_id: %s' % (user_id,prod_id))
    print (result)
