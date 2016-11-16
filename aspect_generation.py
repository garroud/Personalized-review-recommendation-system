#The program will generate all the aspects which will be used in our system
import nltk
import re
from fim import apriori, eclat, fpgrowth, fim

def tag_gen_TA(output):
    fo_2 = open('parsed information/reviews_TA.txt', 'w')
    fo = open(output,'w')
    count = 0
    with open('resource/sub_en_tripadvisor_review_details.txt','r',encoding = 'utf-8') as f:
        for line in f:
            content = line[line.find("\"text\": ")+9 : line.find('\", \"author\"')]
            temp = bytes(content,'ascii').decode('unicode_escape')
            results = temp.rstrip('-').split('\\n')
            tokens = []
            tagged = []
            for paragraph in results:
                fo_2.write(paragraph+'\n')
                tokens = nltk.word_tokenize(paragraph)
                tagged += nltk.pos_tag(tokens)
                for item in tagged:
                    if item[1] == 'NN' or item[1] == 'NNP' or item[1] == 'NNS':
                        #temp = ''
                        #try:
                        #    temp = bytes(item[0],'ascii').decode('unicode_escape')
                        #except:
                        #    pass
                        if not (item[0] == '\\' or item[0] == '..' or \
                                item[0] == '%' or item[0] == '*'):
                            result = item[0].rstrip('/').split('/')
                            for words in result:
                                fo.write(words + ',')
                    if item[1] == '.' or item[1] == ';' or item[1]=='?' \
                        or item[1] == '!':
                        count += 1
            fo.write('\n')
    fo.close()
    fo_2.close()
    return count

#asdef get_candidate():
#Use the the association rule miner, CBA (Liu, Hsu and Ma 1998), which is
#based on the Apriori algorithm in (Agrawal and Srikant 1994). It finds all
#frequent itemsets in the transaction set. The result will be our candidate aspects

#designed to handle the validility of a candidate feature set
def valid_two_words(candidate, words):
    indices = [i for i, x in enumerate(words) if x == candidate[0]]
    if len(indices) == 0:
        return False
    for index in indices:
        if words[index-3:index+4].count(candidate[1])!=0:
            return True

def valid_three_words(candidate, words):
    return valid_two_words((candidate[0],candidate[1]),words) and \
            valid_two_words((candidate[0],candidate[2]),words) and \
            valid_two_words((candidate[1],candidate[2]),words)


def gen_freq_set(filename):
    total_list = []
    with open(filename,'r') as f:
        for line in f:
            content = line.split(',')
            total_list.append(content[:-1])
    freq_set = fpgrowth(total_list, supp=1, zmin=1,zmax=3)
    #test for compactness of the candidate set
    count = {}
    for item in freq_set:
        if len(item[0]) >=2 :
            count[item[0]] = 0
    with open('parsed information/reviews_TA.txt','r') as f:
        for review in f:
            for sentence in re.split(r'[?!.;\n]\s*',review):
                words = re.split(r'[,\s\'\"()\[\]\{\}]\s*',sentence)
                for item in freq_set:
                    if len(item[0]) == 2 and valid_two_words(item[0],words):
                        count[item[0]]  += 1
                    if len(item[0]) == 3 and valid_three_words(item[0],words):
                        count[item[0]] += 1
    fo_1 = open('parsed information/freq_set_TA.txt', 'w')
    fo_2 = open('parsed information/freq_set_TA_2.txt','w')
    for item in freq_set:
        fo_1.write(item)
        if len(item[0]) == 1:
            fo_2.write(item)
        else:
            if(count[item[0]] >= 2):
                fo_2.write(item)
    fo_1.close()
    fo_2.close()
    return

#tag_gen_TA('parsed information/tag_gen_TA_2.txt')
gen_freq_set('parsed information/tag_gen_TA_2.txt')
