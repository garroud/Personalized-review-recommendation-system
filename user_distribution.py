import os
import numpy as np
import basic_info
import discount as dis
def get_user_distribution(is_t, present, rate, type):
    topics = []
    if type == "_Yelp":
        topics = basic_info.topics_Y
    else:
        topics = basic_info.topics_TA
    file_list = os.listdir('users'+type)
    with open("paserd information/users_distribution"+type+".txt","w+") as f:
        for the_file in file_list:
            f.write(the_file[:-4])
            size = 0
            distribution = np.zeros(len(topics))
            with open("users" + type + '/'+ the_file, 'r') as finput:
                for line in finput:
                    time   = line.split(' ')[2]
                    vector = np.array([float(number) for number in line.split(' ')[4:]])
                    if(is_t):
                        factor = dis.discount(rate,dis.time_diff(time,present))
                        distribution += factor * vector
                        size += factor
                    else:
                        distribution += vector
                        size += 1
            distribution /= size
            f.write(" " + str(size))
            for number in distribution:
                f.write(" " + str(number))
            f.write('\n')
