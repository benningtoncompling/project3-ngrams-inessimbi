#!/usr/bin/python3
#
# build_ngram_model.py,.py - building n gram model
# Author: <Ines Simbi>(inessimbi@bennington.edu)
# Date: <03.30.2019>


import math

file_name = "shakespeare.txt"
out_file_name = "output_generated.txt"

with open(file_name, 'r', encoding="utf-8") as in_file:  # open file
    with open(out_file_name, 'w', encoding="utf-8") as out_file:  # writes to file
        text = in_file.readlines()  # read what's in file
        the_list = []
        for line in text:
            line = line.lower().strip()
            the_list.append("<s> " + line + " </s>")
        unigram_text=(" ". join(the_list))
        unigrams_list = unigram_text.split(" ")
        #print(unigrams_list)
        #print(len(unigrams_list))
        bigrams_list = []
        for i in range(len(unigrams_list) - 1):
            bigrams_list.append(unigrams_list[i] + " " + unigrams_list[i+1])
        #print(bigrams_list)
        #bigram_text = (" ".join(bigrams_list))
        trigrams_list = []
        for j in range(len(unigrams_list) - 2):
            trigrams_list.append(unigrams_list[j] + " " + unigrams_list[j + 1] + " ," + unigrams_list[j+2])
        #print(trigrams_list[:20])

        unigram_counts = {}
        for word in unigrams_list:
            if word not in unigram_counts:
                unigram_counts[word] = 1
            else:
                unigram_counts[word] += 1
        #print(unigram_counts)

        bigram_counts = {}
        count_bigram_tokens = 0
        count_bigram_types = 0
        for i in range(len(unigrams_list)-1):
            first_word = unigrams_list[i]
            second_word = unigrams_list[i+1]
            if (first_word in bigram_counts) and (second_word in bigram_counts[first_word]):
                bigram_counts[first_word][second_word] += 1
                count_bigram_tokens = count_bigram_tokens + 1

            elif first_word in bigram_counts:
                bigram_counts[first_word][second_word] = 1
                count_bigram_tokens = count_bigram_tokens + 1
                count_bigram_types = count_bigram_types + 1
            else:
                bigram_counts[first_word] = {second_word: 1}
                count_bigram_tokens = count_bigram_tokens + 1
                count_bigram_types = count_bigram_types + 1
        #print("number of types in bigram: ", count_bigram_types)
        #print("number of types in bigram: ", count_bigram_tokens)

        #print(bigram_counts)

        trigram_counts = {}
        count_trigram_tokens = 0
        count_trigram_types = 0
        for i in range(len(unigrams_list)-2):
            first_set = unigrams_list[i] + " " + unigrams_list[i+1]
            second_word = unigrams_list[i+2]
            if first_set in trigram_counts:
                if second_word in trigram_counts:
                    trigram_counts[first_set][second_word] += 1
                    count_trigram_tokens = count_trigram_tokens + 1

                else:
                    trigram_counts[first_set][second_word] = 1
                    count_trigram_tokens = count_trigram_tokens + 1
                    count_trigram_types = count_trigram_types + 1
            else:
                trigram_counts[first_set] = {second_word: 1}
                count_trigram_tokens = count_trigram_tokens + 1
                count_trigram_types = count_trigram_types + 1

        #print(trigram_counts)
        #print("number of types in trigram: ", count_trigram_types)
        #print("number of types in trigram: ", count_trigram_tokens)

        #number of types in ngrams
        the_string= ""
        ngram1= " \data\ ngram 1: type= " + str(len(unigram_counts)) + " token= " + str(len(unigrams_list))
        ngram2= " ngram 2: type= " + str(count_bigram_types) + " token= " + str(count_bigram_tokens)
        ngram3= " ngram 3: type= " + str(count_trigram_types) + " token= " + str(count_trigram_tokens)
        the_string = ngram1 + ngram2 + ngram3
        out_file.write(the_string)

        out_file.write("\1-grams ")
        the_1_gram_string = " "
        for key in unigram_counts.keys(): #gets key in dictionary
            count_1_gram =unigram_counts[key]
            prob_1_gram = count_1_gram / len(unigrams_list)
            log_1_gram = math.log(prob_1_gram, 10)
            the_1_gram_string=(str(count_1_gram) + " " + str(prob_1_gram) + " " + str(log_1_gram) + " " + key + " ")
            #print(the_1_gram_list[4000])
            #the_1_gram_list_text =(" ". join(the_1_gram_list))
            out_file.write(the_1_gram_string)

        out_file.write("\2-grams ")
        the_2_gram_string = ""
        for key in bigram_counts.keys(): #gets key in dictionary ex:
            for value in bigram_counts[key].keys(): # gets value of key in key in dictionary
                count_2_gram = bigram_counts[key][value]
                prob_2_gram = count_2_gram / unigram_counts[key]
                log_2_gram = math.log(prob_2_gram, 10)
                the_2_gram_string = (str(count_2_gram) + " " + str(prob_2_gram) + " " + str(log_2_gram) + " =" + key + " "+ value + " ")
                #print(unigram_counts["ripe-red"])
                #print(the_2_gram_list[-20:])
                #the_2_gram_list_text =(" ". join(the_2_gram_list))
                out_file.write(the_2_gram_string)

        out_file.write("\3-grams ")
        the_3_gram_string = ""
        for key in trigram_counts.keys():
            for value in trigram_counts[key].keys():  # gets value of key in key in dictionary
                count_3_gram = trigram_counts[key][value]
                key_words = key.split()
                #if key_words[0] not in bigram_counts:
                 #   print("can't find " + key)
                prob_3_gram = count_3_gram / bigram_counts[key_words[0]][key_words[1]]
                log_3_gram = math.log(prob_3_gram, 10)
                the_3_gram_string = str(count_3_gram) + " " + str(prob_3_gram) + " " + str(log_3_gram) + " =" + key + " " + value + " "
                #print(the_3_gram_list[:5])
                out_file.write(the_3_gram_string)