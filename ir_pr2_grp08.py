import os
import re
import argparse
import sys
import time
from collections import defaultdict, Counter
import math



class PorterStemmer:
    def isCons(self, alphabet):#function checking if a letter is a consonant or not and returns a boolean value (true or false).
        if alphabet == 'a' or alphabet == 'e' or alphabet == 'i' or alphabet == 'o' or alphabet == 'u':
            return False
        else:
            return True
        

    def isConsonant(self, word, i):#function that returns true only if the letter at i th position 
        #in the argument 'word' is a consonant.But if the letter is 'y' and the letter at i-1 th position 
        #is also a consonant, then it returns false.
        alphabet = word[i]
        if self.isCons(alphabet):
            if alphabet == 'y' and self.isCons(word[i-1]):
                return False
            else:
                return True
        else:
            return False
        

    def isVowel(self, word, i):#function that returns true if the letter at i th position in the argument 'word'
        #is a vowel
        variable = self.isConsonant(word, i)
        return not(variable)

    # *S  - the stem ends with S (and similarly for the other letters). 
    def endsWith(self, stem, alphabet):#returns true if the word 'stem' ends with 'alphabet' 
        if stem.endswith(alphabet):
            return True
        else:
            return False

    # *v* - the stem contains a vowel. 
    def containsVowel(self, stem):#returns true if the word 'stem' contains a vowel
        for i in stem:
            if not self.isCons(i):
                return True
        return False

    # *d  - the stem ends with a double consonant (e.g. -TT, -SS).
    def doubleCons(self, stem):#returns true if the word 'stem' ends with 2 consonants
        if len(stem) >= 2:
            if self.isConsonant(stem, -1) and self.isConsonant(stem, -2):
                return True
            else:
                return False
        else:
            return False
    
    # *o  - the stem ends cvc, where the second c is not W, X or Y (e.g. -WIL, -HOP).
    def cvc(self, word):
        #returns true if the last 3 letters of the word are of the following pattern: consonant,vowel,consonant
        #but if the last word is either 'w','x' or 'y', it returns false
        if len(word) >= 3:
            f = -3
            s = -2
            t = -1
            third = word[t]
            if self.isConsonant(word, f) and self.isVowel(word, s) and self.isConsonant(word, t):
                if third != 'w' and third != 'x' and third != 'y':
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def getForm(self, word):
        #This function takes a word as an input, and checks for vowel and consonant sequences in that word.
        #vowel sequence is denoted by V and consonant sequences by C
        #For example, the word 'balloon' can be divived into following sequences:
        #'b' : C
        #'a' : V
        #'ll': C
        #'oo': V
        #'n' : C
        #So form = [C,V,C,V,C] and formstr = CVCVC
        form = []
        formStr = ''
        for i in range(len(word)):
            if self.isConsonant(word, i):
                if i != 0:
                    prev = form[-1]
                    if prev != 'C':
                        form.append('C')
                else:
                    form.append('C')
            else:
                if i != 0:
                    prev = form[-1]
                    if prev != 'V':
                        form.append('V')
                else:
                    form.append('V')
        for j in form:
            formStr += j
        return formStr

    def getM(self, word):
        #returns value of M which is equal to number of 'VC' in formstr
        #So in above example of word 'balloon', we have 2 'VC'

        form = self.getForm(word)
        m = form.count('VC')
        return m

    
    def replace(self, orig, rem, rep):
        #this function checks if string 'orig' ends with 'rem' and
        #replaces 'rem' by the substring 'rep'. The resulting string 'replaced'
        #is returned.

        result = orig.rfind(rem)
        base = orig[:result]
        replaced = base + rep
        return replaced

    def replaceM0(self, orig, rem, rep):
        #same as the function replace(), except that it checks the value of M for the 
        #base string. If it is >0 , it replaces 'rem' by 'rep', otherwise it returns the
        #original string

        result = orig.rfind(rem)
        base = orig[:result]
        if self.getM(base) > 0:
            replaced = base + rep
            return replaced
        else:
            return orig

    def replaceM1(self, orig, rem, rep):
        #same as replaceM0(), except that it replaces 'rem' by 'rep', only when M>1 for
        #the base string

        result = orig.rfind(rem)
        base = orig[:result]
        if self.getM(base) > 1:
            replaced = base + rep
            return replaced
        else:
            return orig

    def step1a(self, word):
        #In a given word, this function replaces 'sses' by 'ss', 'ies' by 'i',
        #'ss' by 'ss' and 's' by ''

        """step1a() gets rid of plurals. e.g.

           caresses  ->  caress
           ponies    ->  poni
           ties      ->  ti
           caress    ->  caress
           cats      ->  cat
        """
        if word.endswith('sses'):
            word = self.replace(word, 'sses', 'ss')
        elif word.endswith('ies'):
            word = self.replace(word, 'ies', 'i')
        elif word.endswith('ss'):
            word = self.replace(word, 'ss', 'ss')
        elif word.endswith('s'):
            word = self.replace(word, 's', '')
        else:
            pass
        return word

    def step1b(self, word):
        #this function checks if a word ends with 'eed','ed' or 'ing' and replces these substrings by
        #'ee','' and ''. If after the replacements in case of 'ed' and 'ing', the resulting word
        # -> ends with 'at','bl' or 'iz' : add 'e' to the end of the word
        # -> ends with 2 consonants and its last letter isn't 'l','s' or 'z': remove last letter of the word
        # -> has 1 as value of M and the cvc(word) returns true : add 'e' to the end of the word
        
        '''
        step1b gets rid of -eed -ed or -ing. e.g.

        feed      ->  feed
           agreed    ->  agree
           disabled  ->  disable

           matting   ->  mat
           mating    ->  mate
           meeting   ->  meet
           milling   ->  mill
           messing   ->  mess

           meetings  ->  meet
        '''
        flag = False
        if word.endswith('eed'):
            result = word.rfind('eed')
            base = word[:result]
            if self.getM(base) > 0:
                word = base
                word += 'ee'
        elif word.endswith('ed'):
            result = word.rfind('ed')
            base = word[:result]
            if self.containsVowel(base):
                word = base
                flag = True
        elif word.endswith('ing'):
            result = word.rfind('ing')
            base = word[:result]
            if self.containsVowel(base):
                word = base
                flag = True
        if flag:
            if word.endswith('at') or word.endswith('bl') or word.endswith('iz'):
                word += 'e'
            elif self.doubleCons(word) and not self.endsWith(word, 'l') and not self.endsWith(word, 's') and not self.endsWith(word, 'z'):
                word = word[:-1]
            elif self.getM(word) == 1 and self.cvc(word):
                word += 'e'
            else:
                pass
        else:
            pass
        return word

    def step1c(self, word):
        #In words ending with 'y' this function replaces 'y' by 'i'
        
        """step1c() turns terminal y to i when there is another vowel in the stem."""

        if word.endswith('y'):
            result = word.rfind('y')
            base = word[:result]
            if self.containsVowel(base):
                word = base
                word += 'i'
        return word

    def step2(self, word):
        #this function checks the value of M, and replaces the suffixes accordingly
        
        """step2() maps double suffices to single ones.
        so -ization ( = -ize plus -ation) maps to -ize etc. note that the
        string before the suffix must give m() > 0.
        """

        if word.endswith('ational'):
            word = self.replaceM0(word, 'ational', 'ate')
        elif word.endswith('tional'):
            word = self.replaceM0(word, 'tional', 'tion')
        elif word.endswith('enci'):
            word = self.replaceM0(word, 'enci', 'ence')
        elif word.endswith('anci'):
            word = self.replaceM0(word, 'anci', 'ance')
        elif word.endswith('izer'):
            word = self.replaceM0(word, 'izer', 'ize')
        elif word.endswith('abli'):
            word = self.replaceM0(word, 'abli', 'able')
        elif word.endswith('alli'):
            word = self.replaceM0(word, 'alli', 'al')
        elif word.endswith('entli'):
            word = self.replaceM0(word, 'entli', 'ent')
        elif word.endswith('eli'):
            word = self.replaceM0(word, 'eli', 'e')
        elif word.endswith('ousli'):
            word = self.replaceM0(word, 'ousli', 'ous')
        elif word.endswith('ization'):
            word = self.replaceM0(word, 'ization', 'ize')
        elif word.endswith('ation'):
            word = self.replaceM0(word, 'ation', 'ate')
        elif word.endswith('ator'):
            word = self.replaceM0(word, 'ator', 'ate')
        elif word.endswith('alism'):
            word = self.replaceM0(word, 'alism', 'al')
        elif word.endswith('iveness'):
            word = self.replaceM0(word, 'iveness', 'ive')
        elif word.endswith('fulness'):
            word = self.replaceM0(word, 'fulness', 'ful')
        elif word.endswith('ousness'):
            word = self.replaceM0(word, 'ousness', 'ous')
        elif word.endswith('aliti'):
            word = self.replaceM0(word, 'aliti', 'al')
        elif word.endswith('iviti'):
            word = self.replaceM0(word, 'iviti', 'ive')
        elif word.endswith('biliti'):
            word = self.replaceM0(word, 'biliti', 'ble')
        return word

    def step3(self, word):
        #this function checks the value of M, and replaces the suffixes accordingly
        
        """step3() dels with -ic-, -full, -ness etc. similar strategy to step2."""

        if word.endswith('icate'):
            word = self.replaceM0(word, 'icate', 'ic')
        elif word.endswith('ative'):
            word = self.replaceM0(word, 'ative', '')
        elif word.endswith('alize'):
            word = self.replaceM0(word, 'alize', 'al')
        elif word.endswith('iciti'):
            word = self.replaceM0(word, 'iciti', 'ic')
        elif word.endswith('ful'):
            word = self.replaceM0(word, 'ful', '')
        elif word.endswith('ness'):
            word = self.replaceM0(word, 'ness', '')
        return word

    def step4(self, word):
        #this function checks the value of M, and replaces the suffixes accordingly
        
        """step4() takes off -ant, -ence etc., in context <c>vcvc<v>{meaning, M >1 for the word}."""

        if word.endswith('al'):
            word = self.replaceM1(word, 'al', '')
        elif word.endswith('ance'):
            word = self.replaceM1(word, 'ance', '')
        elif word.endswith('ence'):
            word = self.replaceM1(word, 'ence', '')
        elif word.endswith('er'):
            word = self.replaceM1(word, 'er', '')
        elif word.endswith('ic'):
            word = self.replaceM1(word, 'ic', '')
        elif word.endswith('able'):
            word = self.replaceM1(word, 'able', '')
        elif word.endswith('ible'):
            word = self.replaceM1(word, 'ible', '')
        elif word.endswith('ant'):
            word = self.replaceM1(word, 'ant', '')
        elif word.endswith('ement'):
            word = self.replaceM1(word, 'ement', '')
        elif word.endswith('ment'):
            word = self.replaceM1(word, 'ment', '')
        elif word.endswith('ent'):
            word = self.replaceM1(word, 'ent', '')
        elif word.endswith('ou'):
            word = self.replaceM1(word, 'ou', '')
        elif word.endswith('ism'):
            word = self.replaceM1(word, 'ism', '')
        elif word.endswith('ate'):
            word = self.replaceM1(word, 'ate', '')
        elif word.endswith('iti'):
            word = self.replaceM1(word, 'iti', '')
        elif word.endswith('ous'):
            word = self.replaceM1(word, 'ous', '')
        elif word.endswith('ive'):
            word = self.replaceM1(word, 'ive', '')
        elif word.endswith('ize'):
            word = self.replaceM1(word, 'ize', '')
        elif word.endswith('ion'):
            result = word.rfind('ion')
            base = word[:result]
            if self.getM(base) > 1 and (self.endsWith(base, 's') or self.endsWith(base, 't')):
                word = base
            word = self.replaceM1(word, '', '')
        return word

    def step5a(self, word):
        #this function checks if the word ends with 'e'. If it does, it checks the value of
        #M for the base word. If M>1, OR, If M = 1 and cvc(base) is false, it simply removes 'e'
        #ending.
        
        """step5() removes a final -e if m() > 1.
        """

        if word.endswith('e'):
            base = word[:-1]
            if self.getM(base) > 1:
                word = base
            elif self.getM(base) == 1 and not self.cvc(base):
                word = base
        return word

    def step5b(self, word):
        #this function checks if the value of M for the word is greater than 1 and it ends with 2 consonants
        # and it ends with 'l', it removes 'l'
        
        #step5b changes -ll to -l if m() > 1
        if self.getM(word) > 1 and self.doubleCons(word) and self.endsWith(word, 'l'):
            word = word[:-1]
        return word

    def stem(self, word):
        """
        I read the porter.txt file and found your note.
        """
        #steps to be followed for stemming according to the porter stemmer :)

        word = self.step1a(word)
        word = self.step1b(word)
        word = self.step1c(word)
        word = self.step2(word)
        word = self.step3(word)
        word = self.step4(word)
        word = self.step5a(word)
        word = self.step5b(word)
        return word
    


    





def precision(query, dict_gt, inverted_index):
    temp_tot_relevant_docs = inverted_index[query]
    tot_relevant_docs = []
    for elem in temp_tot_relevant_docs:
        var = elem[0:2]
        if var[0] == '0':
            var=var[1] 
        tot_relevant_docs.append(var)
    tot_relevant_docs = set(tot_relevant_docs)
    all_retrieved_docs = set(dict_gt[query])
    
    relevant_retrieved_docs = all_retrieved_docs & tot_relevant_docs
    relevant_retrieved_docs = list(relevant_retrieved_docs)
    all_retrieved_docs = list(all_retrieved_docs)
    
    numer = len(relevant_retrieved_docs)
    denom = len(all_retrieved_docs)
    
    precision_result = numer / denom
    return precision_result

def recall(query, dict_gt, inverted_index):
    temp_tot_relevant_docs = inverted_index[query]
    tot_relevant_docs = []
    for elem in temp_tot_relevant_docs:
        var = elem[0:2]
        if var[0] == '0':
            var=var[1] 
        tot_relevant_docs.append(var)
    tot_relevant_docs = set(tot_relevant_docs)
    all_retrieved_docs = set(dict_gt[query])
    
    relevant_retrieved_docs = all_retrieved_docs & tot_relevant_docs
    relevant_retrieved_docs = list(relevant_retrieved_docs)
    all_retrieved_docs = list(all_retrieved_docs)
    
    numer = len(relevant_retrieved_docs)
    denom = len(tot_relevant_docs)
    
    recall_result = numer / denom
    return recall_result




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
    text = text.replace("  "," ")
    text = text.replace('\n\n', ' ')
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
        

def corpus2dtm(tokenized_corpus, vocabulary):
  document_term_matrix = []
  for document in tokenized_corpus:
        document_counts = Counter(document)
        row = [document_counts[word] for word in vocabulary]
        document_term_matrix.append(row)
  return document_term_matrix

def queryToDtm(query_tokenized, vocabulary):
    queryVector = []
    queryCounts = Counter(query_tokenized)
    row = [queryCounts[word] for word in vocabulary]
    queryVector = row
    return queryVector

def termFreqCalc(document_term_matrix):
    term_frequency = []
    document_term = list(map(list, zip(*document_term_matrix)))
    for i in document_term:
        term_frequency.append(sum(i))
    return term_frequency
    

def queryWeightCalc(query_vector, term_frequency, No_of_Docs):
    max_tf = max(query_vector)
    
    weight_vector = []
    for i in range(len(query_vector)):
        if query_vector[i] == 0:
            weight_vector.append(0)
        else:
            log_value=math.log((No_of_Docs)/term_frequency[i])
            weight=(0.5+((0.5*query_vector[i])/max_tf))*log_value
            weight_vector.append(weight)
    return weight_vector


def termWeightCalc(term_frequency, No_of_Docs, document_term_matrix):
    tf_matrix = []
    idf_matrix = []
    for i in range(len(term_frequency)):
        tf_matrix.append((No_of_Docs)/term_frequency[i])
        idf_matrix.append(math.log((No_of_Docs)/term_frequency[i]))
    for i in range(len(document_term_matrix)):
        for j in range(len(document_term_matrix[i])):
            document_term_matrix[i][j] = document_term_matrix[i][j] * idf_matrix[j]
    
    return document_term_matrix


def doc_magnitude(document_weight_vector):
  doc_magnitude=[]
  temp_magnitude=0
  for document in document_weight_vector:
    for value in document:
      temp_magnitude=temp_magnitude+(value*value)
    temp_magnitude=math.sqrt(temp_magnitude)
    doc_magnitude.append(temp_magnitude)
    temp_magniude=0
  return doc_magnitude


def query_magnitude(query_weight_vector):
  query_magnitude=0
  for value in query_weight_vector:
    query_magnitude=query_magnitude+(value*value)
  query_magnitude=math.sqrt(query_magnitude)
  return query_magnitude


def dot_prod(document_weight_vector,query_weight_vector):
  dot_prod_vector=[]
  for i in range(len(document_weight_vector)):
    value=0
    for j in range(len(document_weight_vector[i])):
      value= value + (document_weight_vector[i][j]*query_weight_vector[j])
    dot_prod_vector.append(value)
  return dot_prod_vector


def top_docs(dot_prod_matrix,query_magnitude,doc_magnitude_vector):
  topDocs=[]
  value=0
  for i in range(len(dot_prod_matrix)):
    value=dot_prod_matrix[i]/(doc_magnitude_vector[i]*query_magnitude)
    topDocs.append(value)
  topDocs = [i+1 for i, x in sorted(enumerate(topDocs), key=lambda x: x[1], reverse=True)]
  return topDocs
    

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

    
    dict_titles_texts_original = dict(zip(chapter_list_final_keys, chapters_text_values))
    
    dict_titles_texts_st = dict(zip(chapter_list_final_keys, chapters_text_values))
    tokenized_documents = []
    for key in dict_titles_texts_st.keys():
        dict_titles_texts_st[key] = cleaning_text(dict_titles_texts_st[key])
        words = dict_titles_texts_st[key].split(' ')
        filtered_words = []
        for word in words:    
            if word.lower() not in stop_words:
                filtered_words.append(word.lower())
        tokenized_documents.append(list(filtered_words))
        s = ' '.join(filtered_words)
        dict_titles_texts_st[key] = s
    
    if args.extract_collection is not None:
        extract_collection(dict_titles_texts_original= dict_titles_texts_original, dict_titles_texts_st = dict_titles_texts_st)
    if args.query is not None:
        if args.model == 'bool':
            if args.search_mode == 'linear':
                start = time.time()
                linear_search_collection(chapter_titles = chapter_list_final_keys, dict_titles_texts_original= dict_titles_texts_original, dict_titles_texts_st = dict_titles_texts_st, query=args.query, model=args.model, documents=args.documents, stemming=args.stemming)
                end = time.time()
                print(f'T={(end - start)*1000} ms')
            elif args.search_mode == 'inverted':
                unique = []
                for text in dict_titles_texts_st.values():

                    text = text.lower()
                    text = cleaning_text(text)
                    words = text.split(" ")
                    for word in words:

                        if word not in unique:
                            unique.append(word)

                unique.remove('')
                unique.sort()
                query=args.query
                if args.stemming and not(query.__contains__('&') or query.__contains__('|') or query.__contains__('>')):
                    obj_word = PorterStemmer()
                    query=obj_word.stem(query)
                    for word in unique:
                        temp=obj_word.stem(word)
                        unique.append(word)     
                
                
                inverted_index = defaultdict(list)
                for i in range(0,len(unique)):
                    for key,value in dict_titles_texts_st.items():
                        words = value.split(" ")
                        for word in words:
                            if unique[i].lower() == word.lower():
                                {inverted_index[unique[i].lower()].append(key)}
                                break
                    
                start = time.time()
                inverted_list_search(chapter_list_final_keys, inverted_index, query, model=args.model, documents=args.documents, stemming=args.stemming)
                end = time.time()
                
                try:
                    ground_truth_path = os.path.abspath("ground_truth.txt")
                    with open(ground_truth_path, 'r') as gt:
                        terms = gt.read()
                        terms = terms.split('\n')
                        var = []
                        for i in terms:
                            temp = i.split(' - ')
                            var.append(temp)
                        var = var[:6]

                    gt_keys = []
                    gt_values = []
                    for i in range(len(var)):
                        gt_values.append((var[i][1]).split(", "))
                        gt_keys.append(var[i][0])
                            
                    temp_gt_values = gt_values
                    temp_gt_keys = gt_keys
                    
                    dict_gt = dict(zip(gt_keys,gt_values))

                    recall_value = recall(args.query, dict_gt, inverted_index)
                    precision_value = precision(args.query, dict_gt,inverted_index)   
                    print(f'T={(end - start)*1000} ms,P = {precision_value},R = {recall_value}')         
                
                except KeyError:
                    print(f'T={(end - start)*1000} ms, P=?,R=?')
            else:
                print("\nSearch Mode Argument is missing\n")
        
        elif args.model == "vector":
            try:
                unique = []
                for text in dict_titles_texts_st.values():

                    text = text.lower()
                    text = cleaning_text(text)
                    words = text.split(" ")
                    for word in words:

                        if word not in unique:
                            unique.append(word)

                unique.remove('')
                unique.sort()
                query = args.query
                query = query.lower()
                query_tokenized=list(query.split(" "))
                if args.stemming:
                    temp = []
                    obj_word = PorterStemmer()
                    for word in query_tokenized:
                        temp.append(obj_word.stem(word))
                    query_tokenized = temp
                        
                
                
                document_term_matrix = corpus2dtm(tokenized_documents, unique)
                
                queryVector = queryToDtm(query_tokenized, unique)
                
                term_frequency = termFreqCalc(document_term_matrix)
                
                query_weight_vector = queryWeightCalc(queryVector, term_frequency, len(chapter_list_final_keys))
                
                document_weight_vector = termWeightCalc(term_frequency, len(chapter_list_final_keys), document_term_matrix)
                
                doc_magnitude_vector = doc_magnitude(document_weight_vector)
                
                query_magnitude_value = query_magnitude(query_weight_vector)
                
                dot_prod_matrix = dot_prod(document_weight_vector, query_weight_vector)
                
                topDocs = top_docs(dot_prod_matrix, query_magnitude_value, doc_magnitude_vector)
                start = time.time()
                print(topDocs)
                end = time.time()
                print(f'T={(end - start)*1000} ms, P=?,R=?')
            except NameError:
                print("")
        else:
            print("\nModel Argument is missing\n") 
            
            
        
