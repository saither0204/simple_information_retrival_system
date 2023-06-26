import os
import re
import argparse
import sys
import time
from collections import defaultdict
from porterStemmer import PorterStemmer


def second_search(text,str):
  list_1=[m.start() for m in re.finditer(fr'\b{str}\b',text)] #used fr to combine variable in the raw string
  if (str=='The Fisher'):
      return list_1[2]
  else:
    return list_1[1]


def create_file_names_with_underscore(chapter_name, count):
    chapter_name_underscore= chapter_name.replace(" ","_").lower().replace(',','').replace("'",'')  # Lower case as well as with underscore
    file_name = f'{count}_{chapter_name_underscore}.txt'
    return file_name


def cleaning_text(text):
    text = text.replace('"', '')
    text = text.replace('\n', ' ')
    text = text.replace(',', '')
    text = text.replace('.', '')
    text = text.replace(';', '')
    text = text.replace(':', '')
    text = text.replace('?', '')
    text = text.replace('!', '')
    return text



def extract_collection(dict_titles_texts_original, dict_titles_texts_st):
    for title, text in dict_titles_texts_original.items():
        file_name=os.path.abspath(f'collection_original/{title}')
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(text)
            
    for title, text in dict_titles_texts_st.items():
        file_name_ST=os.path.abspath(f'collection_no_stopwords/{title}')
        with open(file_name_ST, 'w', encoding='utf-8') as file_st:
            file_st.write(text)       
            
        
def print_title(chapter_name_underscore, count):
    to_print = f'{count}_{chapter_name_underscore}.txt'
    print(to_print, file=sys.stdout)
        

def linear_search_original(dict_titles_texts_original, query):
    title_list = []
    for title, text in dict_titles_texts_original.items():
        text = cleaning_text(text)
        words = text.split(' ')
        for word in words:
            if query == word.lower():
                title_list.append(title)
                break
    return title_list


def linear_search_no_stopwords(dict_titles_texts_st, query):
    title_list = []
    for title, text in dict_titles_texts_st.items():
        words = text.split(' ')
        for word in words:
            if query == word.lower():
                title_list.append(title)
                break
    return title_list
        

def linear_search_stemmed_form_original(dict_titles_texts_original,  query, obj_word):
    title_list = []
    stemmed_query = obj_word.stem(query)
    for title, text in dict_titles_texts_original.items():
        text = cleaning_text(text)
        words = text.split(' ')
        for word in words:
            stemmed_word = obj_word.stem(word)
            if stemmed_query == stemmed_word.lower():
                title_list.append(title)
                break
    return title_list


def linear_search_stemmed_form_no_stopwords(dict_titles_texts_st, query, obj_word):
    title_list = []
    stemmed_query = obj_word.stem(query)
    for title, text in dict_titles_texts_st.items():
        words = text.split(' ')
        for word in words:
            stemmed_word = obj_word.stem(word)
            if stemmed_query == stemmed_word.lower():
                title_list.append(title)
                break
    return title_list
    

def linear_search_collection(chapter_titles, dict_titles_texts_original, dict_titles_texts_st, query, model, documents, stemming):
    query = query.lower() #changes the query to lower case characters    
    obj_word = PorterStemmer()
    
    
    if query.__contains__('&'):
        query = query.split('&',2) #Now query is a list with 2 items [0,1]
        
        if stemming is True:
            if documents == 'original':
                var1 = set(linear_search_stemmed_form_original(dict_titles_texts_original = dict_titles_texts_original, query = query[0], obj_word = obj_word))
                var2 = set(linear_search_stemmed_form_original(dict_titles_texts_original = dict_titles_texts_original, query = query[1], obj_word = obj_word))
                var3 = var1 & var2
                var3 = list(var3)
                var3.sort()
                for i in var3:
                    print(i, file=sys.stdout)
                
        
            elif documents == 'no_stopwords':        
                var1 = set(linear_search_stemmed_form_no_stopwords(dict_titles_texts_st = dict_titles_texts_st, query = query[0], obj_word = obj_word))
                var2 = set(linear_search_stemmed_form_no_stopwords(dict_titles_texts_st = dict_titles_texts_st, query = query[1], obj_word = obj_word))
                var3 = var1 & var2
                var3 = list(var3)
                var3.sort()
                for i in var3:
                    print(i, file=sys.stdout)
            
        else:    
            if documents == 'original':
                var1 = set(linear_search_original(dict_titles_texts_original = dict_titles_texts_original, query = query[0]))
                var2 = set(linear_search_original(dict_titles_texts_original = dict_titles_texts_original, query = query[1]))
                var3 = var1 & var2
                var3 = list(var3)
                var3.sort()
                for i in var3:
                    print(i, file=sys.stdout)
                    
            elif documents == 'no_stopwords':
                linear_search_no_stopwords(dict_titles_texts_st = dict_titles_texts_st, query = query)
                var1 = set(linear_search_no_stopwords(dict_titles_texts_st = dict_titles_texts_st, query = query[0]))
                var2 = set(linear_search_no_stopwords(dict_titles_texts_st = dict_titles_texts_st, query = query[1]))
                var3 = var1 & var2
                var3 = list(var3)
                var3.sort()
                for i in var3:
                    print(i, file=sys.stdout)
        
    elif query.__contains__('|'):
        query = query.split('|',2) #Now query is a list with 2 items [0,1]
        
        if stemming is True:
            if documents == 'original':
                var1 = linear_search_stemmed_form_original(dict_titles_texts_original = dict_titles_texts_original, query = query[0], obj_word = obj_word)
                var2 = linear_search_stemmed_form_original(dict_titles_texts_original = dict_titles_texts_original, query = query[1], obj_word = obj_word)
                var3 = var1 + var2
                var3 = list(var3)
                var3.sort()
                for i in var3:
                    print(i, file=sys.stdout)
                
        
            elif documents == 'no_stopwords':        
                var1 = linear_search_stemmed_form_no_stopwords(dict_titles_texts_st = dict_titles_texts_st, query = query[0], obj_word = obj_word)
                var2 = linear_search_stemmed_form_no_stopwords(dict_titles_texts_st = dict_titles_texts_st, query = query[1], obj_word = obj_word)
                var3 = var1 + var2
                var3 = list(var3)
                var3.sort()
                for i in var3:
                    print(i, file=sys.stdout)
            
        else:    
            if documents == 'original':
                var1 = linear_search_original(dict_titles_texts_original = dict_titles_texts_original, query = query[0])
                var2 = linear_search_original(dict_titles_texts_original = dict_titles_texts_original, query = query[1])
                var3 = var1 + var2
                var3 = list(var3)
                var3.sort()
                for i in var3:
                    print(i, file=sys.stdout)
                    
            elif documents == 'no_stopwords':
                linear_search_no_stopwords(dict_titles_texts_st = dict_titles_texts_st, query = query)
                var1 = linear_search_no_stopwords(dict_titles_texts_st = dict_titles_texts_st, query = query[0])
                var2 = linear_search_no_stopwords(dict_titles_texts_st = dict_titles_texts_st, query = query[1])
                var3 = var1 + var2
                var3 = list(var3)
                var3.sort()
                for i in var3:
                    print(i, file=sys.stdout)
        
    elif query.__contains__('>'):
        query = query.strip('>') #Now query is a single word without the negation symbol '>'
        var2 = set(chapter_titles)
        if stemming is True:
            if documents == 'original':
                var1 = set(linear_search_stemmed_form_original(dict_titles_texts_original = dict_titles_texts_original, query = query, obj_word = obj_word))
                var3 = var2 ^ var1
                var3 = list(var3)
                var3.sort()
                for i in var3:
                    print(i, file=sys.stdout)
                
        
            elif documents == 'no_stopwords':        
                var1 = set(linear_search_stemmed_form_no_stopwords(dict_titles_texts_st = dict_titles_texts_st, query = query, obj_word = obj_word))
                var3 = var2 ^ var1
                var3 = list(var3)
                var3.sort()
                for i in var3:
                    print(i, file=sys.stdout)
            
        else:    
            if documents == 'original':
                var1 = set(linear_search_original(dict_titles_texts_original = dict_titles_texts_original, query = query))
                var3 = var2 ^ var1
                var3 = list(var3)
                var3.sort()
                for i in var3:
                    print(i, file=sys.stdout)
                    
            elif documents == 'no_stopwords':
                linear_search_no_stopwords(dict_titles_texts_st = dict_titles_texts_st, query = query)
                var1 = set(linear_search_no_stopwords(dict_titles_texts_st = dict_titles_texts_st, query = query))
                var3 = var2 ^ var1
                var3 = list(var3)
                var3.sort()
                for i in var3:
                    print(i, file=sys.stdout)
        
    else:
        if stemming is True:
            #obj_word.stem(query)
            #print(obj_word.stem(query)) #code to test of function works or not.
            if documents == 'original':
                var1 = linear_search_stemmed_form_original(dict_titles_texts_original = dict_titles_texts_original, query = query, obj_word = obj_word)
                for i in var1:
                    print(i, file=sys.stdout)
        
            elif documents == 'no_stopwords':
                var1 = linear_search_stemmed_form_no_stopwords(dict_titles_texts_st = dict_titles_texts_st, query = query, obj_word = obj_word)
                for i in var1:
                    print(i, file=sys.stdout)
            
        else:    
            if documents == 'original':
                var1 = linear_search_original(dict_titles_texts_original = dict_titles_texts_original, query = query)
                for i in var1:
                    print(i, file=sys.stdout)
            elif documents == 'no_stopwords':
                var1 = linear_search_no_stopwords(dict_titles_texts_st = dict_titles_texts_st, query = query)
                for i in var1:
                    print(i, file=sys.stdout)


def inverted_list_search(chapter_keys, inverted_index, query, model, documents, stemming):
    query = query.lower() #changes the query to lower case characters
    obj_inverted = PorterStemmer()
    
    
    if query.__contains__('&'):
        query = query.split('&',2) #Now query is a list with 2 items [0,1]
        if query[0].lower() in inverted_index:
            var1 = set(inverted_index[query[0]])
            #print(var1)
            if query[1].lower() in inverted_index:
                var2 = set(inverted_index[query[1]])
                var3 = var1 & var2
                var3 = list(var3)
                var3.sort()
                for i in var3:
                    print(i, file=sys.stdout)
                
        
    elif query.__contains__('|'):
        query = query.split('|',2) #Now query is a list with 2 items [0,1]
        if query[0].lower() in inverted_index:
            var1 = inverted_index[query[0]]
            #print(var1)
            if query[1].lower() in inverted_index:
                var2 = inverted_index[query[1]]
                var3 = set(var1 + var2)
                var3 = list(var3)
                var3.sort()
                for i in var3:
                    print(i, file=sys.stdout)
        
    elif query.__contains__('>'):
        query = query.strip('>') #Now query is a single word without the negation symbol '>'
        var1 = set(chapter_keys)
        if query.lower() in inverted_index:
            var2 = set(inverted_index[query])
            var3 = var1 ^ var2
            var3 = list(var3)
            var3.sort()
            print(len(var3))
            for i in var3:
                print(i, file=sys.stdout)
    
    else:
        if query.lower() in inverted_index:
            var1 = inverted_index[query]
            var1.sort()
            for i in var1:
                print(i, file=sys.stdout)
        
    
    
    

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-s","--search-mode",dest="search_mode")
    parser.add_argument("-e", "--extract-collection",dest="extract_collection")
    parser.add_argument("-q","--query",dest="query")
    parser.add_argument("-m","--model", dest="model")
    parser.add_argument("-d","--documents", dest="documents")
    parser.add_argument("-r","--stemming", dest="stemming", action='store_true')
    args = parser.parse_args()
    
    try:
        os.mkdir('collection_original')
        os.mkdir('collection_no_stopwords')
    except FileExistsError:
        pass
    
    #to avoid creation of files again during search
    try:
        text_file_name = args.extract_collection
        text_file_path = os.path.abspath(text_file_name)
    except TypeError:
        text_file_path = os.path.abspath('aesopa10.txt')
    
    with open(text_file_path,'r') as f:
        text=f.read()
        pattern = '\n{4}(.+?)\n{3}'
        result = re.findall(pattern, text)
    
    chapters_list_final = []
    
    result = result[1:]
    for i in result:
        i = " ".join(i.split())
        chapters_list_final.append(i)
        
    chapters_text=[]
    
    for i in range(0,len(chapters_list_final)):
        start_index= second_search(text,chapters_list_final[i])+len(chapters_list_final[i])+3 # to remove /n 3 times
        
        if i==len(chapters_list_final)-1:
            chapters_text.append(text[start_index:-1])
            
        elif i<len(chapters_list_final):
            end_index=second_search(text,chapters_list_final[i+1])-6 # to remove 4 time /n + 2 times /s
            chapters_text.append(text[start_index:end_index])
    
    ST_file_path = os.path.abspath("englishST.txt")
    with open(ST_file_path, 'r') as f:
        st_text = f.read()
        stop_words = st_text.split('\n')
        stop_words = stop_words[:-1]#Removing last line of englishST.txt as it is a blank
    
    chapter_list_final_keys = [] # will contain Chapters names in required format
    chapters_text_values = chapters_text
    for i in range(1,len(chapters_list_final)+1):
        chapter_list_final_keys.append(create_file_names_with_underscore(chapters_list_final[i-1],str(i).zfill(2)))
    #print(chapter_list_with_required_titles[0:5])
    
    dict_titles_texts_original = dict(zip(chapter_list_final_keys, chapters_text_values))
    
    dict_titles_texts_st = dict(zip(chapter_list_final_keys, chapters_text_values))
    for key in dict_titles_texts_st.keys():
        dict_titles_texts_st[key] = cleaning_text(dict_titles_texts_st[key])
        words = dict_titles_texts_st[key].split(' ')
        filtered_words = []
        for word in words:    
            if word.lower() not in stop_words:
                filtered_words.append(word)
        s = ' '.join(filtered_words)
        dict_titles_texts_st[key] = s
    
    
    if args.extract_collection is not None:
        extract_collection(dict_titles_texts_original= dict_titles_texts_original, dict_titles_texts_st = dict_titles_texts_st)
    if args.query is not None:
        if args.search_mode == 'linear':
            start = time.time()
            linear_search_collection(chapter_titles = chapter_list_final_keys, dict_titles_texts_original= dict_titles_texts_original, dict_titles_texts_st = dict_titles_texts_st, query=args.query, model=args.model, documents=args.documents, stemming=args.stemming)
            end = time.time()
            print(f'T={(end - start)*1000} ms')
        elif args.search_mode == 'inverted':
            unique = []
            for text in dict_titles_texts_st.values():
                #print(text)
                text = cleaning_text(text)
                words = text.split(" ")
                for word in words:
                #print(word)
                    if word not in unique:
                        unique.append(word)
    
            unique.remove('')
            unique.sort()
            
            
            inverted_index = defaultdict(list)
            for i in range(0,len(unique)):
                for key,value in dict_titles_texts_st.items():
                    words = value.split(" ")
                    for word in words:
                        if unique[i].lower() == word.lower():
                            {inverted_index[unique[i].lower()].append(key)}
                            break
            start = time.time()
            inverted_list_search(chapter_list_final_keys, inverted_index, query=args.query, model=args.model, documents=args.documents, stemming=args.stemming)
            end = time.time()
            print(f'T={(end - start)*1000} ms')