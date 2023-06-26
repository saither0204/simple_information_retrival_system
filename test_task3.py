import os
#from ir_pr2_grp08 import inverted_index


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
    print(precision_result)
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
    tot_relevant_docs = list(tot_relevant_docs)
    
    numer = len(relevant_retrieved_docs)
    denom = len(tot_relevant_docs)
    
    recall_result = numer / denom
    print(recall_result)
    return recall_result
        



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

dict_gt = dict(zip(gt_keys,gt_values))
print(dict_gt)



