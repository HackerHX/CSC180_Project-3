'''
CSC180 
Project #3

'''

import math,os,timeit




def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''
    
    sum_of_squares = 0.0  
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    
    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    
    sum = 0.0
    
    for i in vec1:
        if i in vec2:
            sum += vec1[i] * vec2[i]
    
    vec1sqrt = norm(vec1)
    vec2sqrt = norm(vec2)
    
    return sum/(vec1sqrt*vec2sqrt)
    
def euclid_similarity(vec1, vec2):
    
    vec3 = {}

    
    for i in vec2:
        if i in vec1:
            vec3[i] = vec1[i] - vec2[i]
    
    return -norm(vec3)
    
def euclidnorm_similarity(vec1, vec2):
    vec3 = {}
    
    for i in vec1:
        if i in vec2:
            vec3[i] = vec1[i] / norm(vec1) - vec2[i] / norm(vec2)
            
    return -norm(vec3)
    
    
            

def build_semantic_descriptors(sentences):
    d = {}
    for i in sentences:
        for j in i:
            if len(i) != 1:
                if j not in d:
                    d[ j ] = {}
                for k in i:
                    if k != j:
                        if k not in d[j]:
                            d[j][k] = 1.0
                        else:
                            d[j][k] += 1.0
    
    return d
                    
            
    

def update_dict(d1, d2):
    for i in d2:
        if i in d1:
            for j in d2[i]:
                if j in d1[i]:
                    d1[i][j] += d2[i][j]
                else:
                    d1[i][j] = d2[i][j]
        else:
            d1[i] = d2[i]
    
    return d1

    

def build_semantic_descriptors_from_files(filenames):
    punctuation = [',', '-', '--', ':', ';', '"', "'"]
    
    total_d = {}
    
    for i in filenames:
        
        file = open(i, "r", encoding="utf-8")
        
        s = str.lower(file.read())

        file.close()
        
        for j in punctuation:
            s = s.replace(j,'')
            
        s = s.replace('!','.')
        s = s.replace('?','.')
        s = s.replace('\n',' ')
        s = s.strip('.')
        sentences = s.split('.')
       
        
        for g in range(len(sentences)):
            sentences[g] = sentences[g].strip(' ').split(' ')
        
        new_d = build_semantic_descriptors(sentences)
        total_d = update_dict(total_d, new_d)
        
    
    
    return total_d



def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    if word not in semantic_descriptors:
        return  None
    d1 = semantic_descriptors[word]

    lsim = []
    
    for i in choices:
        if i not in semantic_descriptors:
            lsim.append(-1)
        else:
            lsim.append(similarity_fn(d1, semantic_descriptors[i]))
            
        
    return choices[lsim.index(max(lsim) )]
        


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    
    right_question = 0.0
    
    file = open(filename, "r", encoding="utf-8")
    questions = file.read()
    file.close()
    
    questions = questions.split('\n')
    for i in questions:
        q = i.split(' ')
        ans = most_similar_word(q[0], q[2:], semantic_descriptors, similarity_fn)
        if ans == q[1]:
            right_question += 1.0
            
    return  str(right_question / len(questions) * 100) +"%"
 
 
if __name__ == '__main__':
    
    os.chdir("F:\Study\CSC180")
    start = timeit.default_timer()
    l = ["pg2600.txt","pg7178.txt"]
    main_dict = build_semantic_descriptors_from_files(l)
    print("The correction rate is",run_similarity_test("test.txt",main_dict, cosine_similarity))


    stop = timeit.default_timer()

    print("The program takes",stop - start," seconds to run") 
   




