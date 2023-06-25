import os
import re
import argparse
import sys
from porterStemmer import PorterStemmer


def second_search(text,str):
  list_1=[m.start() for m in re.finditer(fr'\b{str}\b',text)] #used fr to combine variable in the raw string
  if (str=='The Fisher'):
      return list_1[2]
  else:
    return list_1[1]


def cleaning_text(file_name):
    with open(file_name, 'r', encoding = 'utf-8') as file_text:
        text = file_text.read()
        text = text.replace('"', '')
        text = text.replace('\n', ' ')
        text = text.replace(',', '')
        text = text.replace('.', '')
        text = text.replace(';', '')
        text = text.replace(':', '')
        text = text.replace('?', '')
        text = text.replace('!', '')
    return text


def create_file(data, chapter_name,count):
    ST_file_path = os.path.abspath("englishST.txt")
    
    chapter_name_underscore= chapter_name.replace(" ","_").lower().replace(',','').replace("'",'')  # Lower case as well as with underscore
    file_name=os.path.abspath(f'collection_original/{count}_{chapter_name_underscore}.txt')
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(data)
    
    file_name_ST=os.path.abspath(f'collection_no_stopwords/{count}_{chapter_name_underscore}.txt')
    with open(ST_file_path, 'r') as f:
        st_text = f.read()
        stop_words = st_text.split('\n')
        stop_words = stop_words[:-1]#Removing last line of englishST.txt as it is a blank
        
        
        with open(file_name, 'r', encoding = 'utf-8') as file_text:
            text = cleaning_text(file_name_ST)
            words = text.split(' ')
            filtered_words = []
            for word in words:    
                if word.lower() not in stop_words:
                    filtered_words.append(word)
            s = ' '.join(filtered_words)
            with open(file_name_ST, 'w', encoding='utf-8') as file_st:
                file_st.write(s)
        
        
def extract_collection(chapters_text, chapters_list_final):
    for i in range(1,len(chapters_text)+1):
        create_file(chapters_text[i-1],chapters_list_final[i-1],str(i).zfill(2))
        
        
def print_title(chapter_name_underscore, count):
    to_print = f'{count}_{chapter_name_underscore}.txt'
    print(to_print, file=sys.stdout)
        

def linear_search_original(chapter_name_underscore, count, query):
    file_name=os.path.abspath(f'collection_original/{count}_{chapter_name_underscore}.txt')
    text = cleaning_text(file_name)
    words = text.split(' ')
    flag = 0
    for word in words:
        if query == word.lower():
            flag += 1
    if flag > 0:
        print_title(chapter_name_underscore, count)


def linear_search_no_stopwords(chapter_name_underscore, count, query):
    file_name_ST=os.path.abspath(f'collection_no_stopwords/{count}_{chapter_name_underscore}.txt')
    with open(file_name_ST, 'r', encoding='utf-8') as file_st:
        text = file_st.read()
        words = text.split(' ')
    flag = 0
    for word in words:
        if query == word.lower():
            flag += 1
    if flag > 0:
        print_title(chapter_name_underscore, count)
        

def linear_search_stemmed_form_original(chapter_name_underscore, count, query, obj_word):
    file_name=os.path.abspath(f'collection_original/{count}_{chapter_name_underscore}.txt')
    text = cleaning_text(file_name)
    words = text.split(' ')
    flag = 0
    for word in words:
        stemmed_word = obj_word.stem(word)
        if query == stemmed_word.lower():
            flag+=1
    if flag > 0:
        print_title(chapter_name_underscore, count)


def linear_search_stemmed_form_no_stopwords(chapter_name_underscore, count, query, obj_word):
    file_name_ST=os.path.abspath(f'collection_no_stopwords/{count}_{chapter_name_underscore}.txt')
    with open(file_name_ST, 'r', encoding='utf-8') as file_st:
        text = file_st.read()
        words = text.split(' ')
    flag = 0
    for word in words:
        stemmed_word = obj_word.stem(word)
        if query == stemmed_word.lower():
            flag += 1
    if flag > 0:
        print_title(chapter_name_underscore, count)
    

def linear_search_collection(chapter_name,count,query, model, documents, stemming):
    query = query.lower() #changes the query to lower case characters    
    chapter_name_underscore = chapter_name.replace(" ","_").lower().replace(',','').replace("'",'')  # Lower case as well as with underscore
    
    
    if stemming is True:
        obj_word = PorterStemmer()
        #obj_word.stem(query)
        #print(obj_word.stem(query)) #code to test of function works or not.
        if documents == 'original':
            stemmed_query = obj_word.stem(query)
            #print(stemmed_query)
            linear_search_stemmed_form_original(chapter_name_underscore, count, stemmed_query, obj_word)
    
        elif documents == 'no_stopwords':
            linear_search_stemmed_form_no_stopwords(chapter_name_underscore, count, stemmed_query, obj_word)
        
    else:    
        if documents == 'original':
            linear_search_original(chapter_name_underscore, count, query)
    
        elif documents == 'no_stopwords':
            linear_search_no_stopwords(chapter_name_underscore, count, query)
    

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
    
    if args.extract_collection is not None:
        extract_collection(chapters_text, chapters_list_final)
    if args.query is not None:
        if args.search_mode == 'linear':
            for i in range(1,len(chapters_list_final)+1):
                linear_search_collection(chapters_list_final[i-1],str(i).zfill(2), query=args.query, model=args.model, documents=args.documents, stemming=args.stemming)
        elif args.search_mode == 'inverted':
            for i in range(1,len(chapters_list_final)+1):
                inverted_list_search(chapters_list_final[i-1],str(i).zfill(2), query=args.query, model=args.model, documents=args.documents, stemming=args.stemming)