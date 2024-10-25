# -*- coding: utf-8 -*-
"""Home_IOAI_Biased_Embeddings.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/16G0GBBwEqot0xoDBV30ftguN9yWCyzk_

# Word Vectors Gone Wrong: Fixing Gender Stereotypes in Language Models

## Problem Description


Language models process words as arrays of  numbers, called word vectors (or word embeddings). These vectors are created based on the usage of the words in context, so they capture the distributional properties of words. Word vectors can be conceptualized as unique coordinates in a multi-dimensional space, with the distance between them capturing the semantic and syntactic relations between words.

In a seminal [article](https://aclanthology.org/P16-1158/) Ekaterina Vylomova and colleagues show that word vectors trained on English data exhibit a curious property: the spatial difference between the vectors of 'king' and 'queen' is the same as the difference between the vectors of 'man' and 'woman'. This difference essentially captures **gender**. Similarly, the difference between 'king' and 'man' is the same as that between 'queen' and 'woman', capturing the notion of royalty.

The way gender is reflected in word vectors has received special attention in NLP, because while sometimes word vectors capture true gender roles (e.g. a king is by definition male), other times they capture undesirable societal biases, e.g. they place 'engineer' and 'man' in the same relationship as 'housekeeper' and 'woman'. This does not seem fair, given that professions such as engineer or housekeeper should be non-gender specific.

![](https://i.ibb.co/RNjF8MH/Screenshot-2023-11-22-at-16-01-27.png)

We don't want to have models that promote stereotypes about which jobs are suitable for men or women, so we should find a way to fix this problem. The tasks presented in this notebook will guide you to one possible solution.

## Technical Specifications

All team solutions should be submitted as a modified and compiled copy of this base notebook. You also need to provide a file of the word vectors you created.

The notebook contains specific tasks you need to accomplish and provides code when necessary. Some cells, marked with the `###DO NOT CHANGE THIS CELL###` comment, have to remain as they are. Other cells can be changed, especially the ones saying `###YOUR CODE GOES HERE###` should be changed to complete the tasks.


Your goal is to get familiar with word vectors and the problem of bias which is a common issue in Artificial Intelligence applications.

## Resources

You can read more on gender bias in word vectors in the paper [Man is to Computer Programmer as Woman is to Homemaker? Debiasing Word Embeddings](https://proceedings.neurips.cc/paper_files/paper/2016/file/a486cd07e4ac3d270571622f4f316ec5-Paper.pdf) by Tolga Bolukbasi, Kai-Wei Chang, James Zou, Venkatesh Saligrama, and Adam Kalai. Proceedings of NIPS 2016.

There are some articles/tutorials online that explain the main concepts of the paper (neutralization and equalization of word vectors) such as [Debiasing Word Embeddings with Geometry](https://medium.com/@mihird97/debiasing-word-embeddings-with-geometry-d2c471ab4ae6).

##Task 1: Creating word Vectors for words

One popular method for obtaining word vectors is to use a pre-trained model such as Word2Vec or GloVe (Global Vectors for Word Representation).

🎯 The goal of is to get familiar with GloVe (Global Vectors for Word Representation), a pre-trained model used to create word vectors.

Deliverables: Extract vectors for the example words provided below and then save them in a txt file. You should deliver (1) the txt file with the words and their corresponding vectors (2) a read_glove_vecs python function that reads the words and vectors from your .txt file like:

```
words, word_to_vec_map = read_glove_vecs('w2v_gnews_small.txt')
```
"""

import numpy as np
from scipy import spatial
import gensim.downloader as api

# Download pre-trained GloVe word vectors
glove_vectors = api.load("glove-wiki-gigaword-100")

# Get the word vectors
man_vector = glove_vectors['man']
woman_vector = glove_vectors['woman']
engineer_vector = glove_vectors['engineer']
housekeeper_vector = glove_vectors['housekeeper']

# Calculate cosine similarities
man_woman_sim = 1 - spatial.distance.cosine(man_vector, woman_vector)
woman_engineer_sim = 1 - spatial.distance.cosine(woman_vector, engineer_vector)
man_engineer_sim = 1 - spatial.distance.cosine(man_vector, engineer_vector)
woman_housekeeper = 1 - spatial.distance.cosine(woman_vector, housekeeper_vector)
man_housekeeper = 1 - spatial.distance.cosine(man_vector, housekeeper_vector)

print("Similarity between man and woman", man_woman_sim)
print("Similarity between man and engineer", man_engineer_sim)
print("Similarity between woman and engineer", woman_engineer_sim)
print("Similarity between man and housekeeper", man_housekeeper)
print("Similarity between woman and housekeeper", woman_housekeeper)

glove_vectors['roofer']

# Get the word vectors
man_vector = glove_vectors['man']
woman_vector = glove_vectors['woman']
bricklayer_vector = glove_vectors['sniper']
nurse_vector = glove_vectors['nurse']

# Calculate cosine similarities
man_woman_sim = 1 - spatial.distance.cosine(man_vector, woman_vector)
woman_bricklayer_sim = 1 - spatial.distance.cosine(woman_vector, bricklayer_vector)
man_bricklayer_sim = 1 - spatial.distance.cosine(man_vector, bricklayer_vector)
woman_nurse = 1 - spatial.distance.cosine(woman_vector, nurse_vector)
man_nurse = 1 - spatial.distance.cosine(man_vector, nurse_vector)

print("Similarity between man and woman", man_woman_sim)
print("Similarity between man and bricklayer", man_bricklayer_sim)
print("Similarity between woman and bricklayer", woman_bricklayer_sim)
print("Similarity between man and nurse", man_nurse)
print("Similarity between woman and nurse", woman_nurse)

"""You should extract word vectors from the following lists. Make sure you save

---

them in a .txt file with a name of your choice. The file should just contain a words and their corresponding vector seperated by space. The next word should start from a new line.
"""

# prompt: generate vectors for names

names = ['john', 'mary', 'alice', 'bob']
vectors = []

for name in names:
    vectors.append(glove_vectors[name])

# # Save the vectors to a file
with open('name_vectors.txt', 'w') as f:
   for i, name in enumerate(names):
    if i < len(vectors):
       vector_str = ' '.join([str(x) for x in vectors[i]])
       f.write(f"{name} {vector_str}\n")

print (vectors)

# Here are the lists of words you should extract word vectors from GloVe, combine all lists in one file

sample = ["father", "mother", "man", "woman"]

professions = ["doctor", "lawyer", "engineer", "nurse", "teacher", "accountant", "architect", "artist", "writer", "chef", "designer", "dentist", "entrepreneur", "firefighter", "journalist", "mechanic", "musician", "paramedic", "photographer", "psychologist", "scientist", "soldier", "surgeon", "vet", "receptionist"]
activities = ["reading", "writing", "painting", "singing", "cooking", "traveling", "volunteering", "meditating", "shopping"]
items = ["phone", "computer", "car", "house", "job", "school", "family", "friends", "food", "drink", "toys", "books", "movies", "concerts", "sports", "electronics", "furniture", "clothing"]
names = ["Alex", "Charlotte", "David", "Emma", "Ethan", "Isabella", "Lily", "Oliver", "Sophia", "William", 'john', 'anna', 'sophie', 'ronaldo', 'shakira', 'mario', 'maria', 'tom', 'katy']

words = sample + professions + activities + items
print(words)
with open('words.txt', 'w') as f:
  for w in words:
    f.write(w + " ")
    try:
      f.write(" ".join(map(str, list(glove_vectors[w]))))
    except Exception as e:
      print(e)
      pass
    f.write('\n')

def read_glove_vecs(glove_file):
    with open(glove_file, 'r') as f:
        words = set()
        word_to_vec_map = {}
        for line in f:
            line = line.strip().split()
            curr_word = line[0]
            words.add(curr_word)
            word_to_vec_map[curr_word] = np.array(line[1:], dtype=np.float64)

    return words, word_to_vec_map

words, word_to_vec_map = read_glove_vecs('words.txt')
print(word_to_vec_map.keys())
print(words)

"""*斜体文本*[link text](https://)It is common practice to save the word embeddings into a .txt format file and then load them with a function like:

`words, word_to_vec_map = read_glove_vecs('w2v_gnews_small.txt')`

You should create a function named 'read_glove_vecs' to open and read the .txt file with the word vectors.

## Task 2 - Implement Cosine Similarity

We can measure how similar are two words using cosine similarity. We would expect non-gender specific words to be equally distant from gender specific words.

🎯 The goal is to get familiar with calculating cosince similarity using python and try to find similar words that are an example of bias and unbiased vectors. We can measure how similar two words are using cosine similarity!

Deliverables: Provide code for implementing cosine distance in Python. Run the example words, and try measuring the distance of different words. Can you find a biased and an unbiased example?

To calculate cosine similarity, we need to take the cosine of the angle between these two vectors. Here are the steps:

1. Calculate the dot product of A and B
   - Multiply each element in A with the corresponding element in B
   - Sum all those products
   - Call this dot_product

2. Calculate the magnitudes (or lengths) of A and B
   - Square each element in A, sum them, and take the square root. Let's call this mag_A.
   - Do the same for B. Let's call this mag_B.

3. Compute cosine similarity:
   cosine_similarity = dot_product / (mag_A * mag_B)

The closer this value is to 1, the smaller the angle and the more similar document A is to document B.

Thanks to Python, you do not need to do these time-consuming calculations manually! Especially for step 1 and step 2, there is a library called 'numpy' with functions that can help you implement cosine distance in Python!
"""

def cosine_similarity(u, v):
    """
    Cosine similarity reflects the degree of similariy between u and v

    Arguments:
        u -- a word vector of shape (n,)
        v -- a word vector of shape (n,)

    Returns:
        cosine_similarity -- the cosine similarity between u and v defined by the formula above.
    """

    distance = 0.0

    ### START CODE HERE ###

    D = np.dot(u, v)
    normv = np.linalg.norm(v)
    # Compute the dot product between u and v (≈1 line)
    dot = np.dot(u,v)
    # Compute th1e L2 norm of u (≈1 line)
    norm_u = np.linalg.norm(u)

    # Compute the L2 norm of v (≈1 line)
    norm_v = np.linalg.norm(v)
    # Compute the cosine similarity defined by formula (1) (≈1 line)
    cosine_similarity = dot/(norm_u * norm_v)
    ### END CODE HERE ###

    return cosine_similarity

father = word_to_vec_map["father"]
mother = word_to_vec_map["mother"]
woman = word_to_vec_map["woman"]
man = word_to_vec_map["man"]

print(father)
print("cosine_similarity(father, mother) = ", cosine_similarity(father, mother))
print("cosine_similarity(woman, man) = ",cosine_similarity(woman, man))
print("cosine_similarity(mother - woman, father - man) = ",cosine_similarity(mother - woman, father - man))

father = word_to_vec_map["father"]
mother = word_to_vec_map["mother"]
doctor = word_to_vec_map["doctor"]
lawyer = word_to_vec_map["lawyer"]


print("cosine_similarity(father, lawyer) = ", cosine_similarity(father, lawyer))
print("cosine_similarity(mother, doctor) = ",cosine_similarity(mother, doctor))

man = word_to_vec_map["man"]
woman = word_to_vec_map["woman"]
nurse = word_to_vec_map["nurse"]
doctor = word_to_vec_map["doctor"]


print("cosine_similarity(man, doctor) = ", cosine_similarity(man, doctor))
print("cosine_similarity(woman, doctor) = ", cosine_similarity(woman, doctor))
print("cosine_similarity(woman, nurse) = ",cosine_similarity(woman, nurse))
print("cosine_similarity(man, nurse) = ",cosine_similarity(woman, nurse))
print("cosine_similarity(nurse, doctor) = ",cosine_similarity(nurse, doctor))

"""This is the code for computing word analogy given three words (word_a, word_b, word_c), or for example ('man', 'father', 'woman'), the following code find the word vector of a word that completes the analogy. In this example the word vector we expect is 'mother'."""

print("cosine_similarity(mother - woman, father - man) = ",cosine_similarity(woman - mother, man - father))

"""## Task 3: Remove bias from word vectors

1.   List item
2.   List item




*   List item



After getting familiar with all the tools we need, now it's time to actually solve the problem of bias in word vectors.

🎯 The goal is to implement a neutralize and equalize Python functions to remove the bias from the word vectors.

Deliverables: (1) Complete the python code for the neutralize and equalize python functions following [Man is to Computer Programmer as Woman is to Homemaker? Debiasing Word Embeddings](https://proceedings.neurips.cc/paper_files/paper/2016/file/a486cd07e4ac3d270571622f4f316ec5-Paper.pdf) by Tolga Bolukbasi, Kai-Wei Chang, James Zou, Venkatesh Saligrama, and Adam Kalai. Proceedings of NIPS 2016. The code should run without any errors. (2) Provide examples before and after removing bias.

To remove the gender bias from non-gender specific word vectors, we need represent the semantic concept of gender as a vector. We can approximate that vector by subtracting female and male word vectors. This means we can compute a vector 'vgender = v1 - v2', where 'v1' represents the word vector corresponding to the word woman, and 'v2' corresponds to the word vector corresponding to the word man. The resulting vector roughly encodes the concept of "gender".
"""

vgender = word_to_vec_map['woman'] - word_to_vec_map['man']
print(vgender.shape)

"""*Now*, you will consider the cosine similarity of different words with vgender. A positive value of similarity means that the words are closer to 'woman' and a negative cosine similarity means the words are closer to 'man'."""

print ('List of names and their similarities with constructed vector:')

# girls and boys name
name_list = ['john', 'anna', 'sophie', 'ronaldo', 'shakira', 'mario', 'maria', 'tom', 'katy']

for w in name_list:
    print (w, cosine_similarity(glove_vectors[w], vgender))

"""As you can see, female first names tend to have a positive cosine similarity with our constructed vector
, while male first names tend to have a negative cosine similarity. This is not suprising, and the result seems acceptable.

But let's try with some other words.
"""

print('Other words and their similarities:')
word_list = ['lipstick', 'guns', 'science', 'arts', 'literature', 'warrior','doctor', 'tree', 'receptionist',
             'technology',  'fashion', 'teacher', 'engineer', 'pilot', 'computer', 'singer']
for w in word_list:
    print (w, cosine_similarity(glove_vectors[w], vgender))

cosine_similarity(neutralize("computer", vgender, word_to_vec_map), vgender)

"""Do you notice anything surprising? It is astonishing how these results reflect certain unhealthy gender stereotypes. For example, "computer" is closer to "man" while "literature" is closer to "woman". Ouch!

We'll see below how to reduce the bias of these vectors, using an algorithm due to Boliukbasi et al., 2016. Note that some word pairs such as "actor"/"actress" or "grandmother"/"grandfather" should remain gender specific, while other words such as "receptionist" or "technology" should be neutralized, i.e. not be gender-related. You will have to treat these two type of words differently when debiasing.

An approach to remove the bias would be to neutralize and equalize the bias for non-gender specific words, following Bolukbasi et al, 2016.

> Tolga Bolukbasi, Kai-Wei Chang, James Zou, Venkatesh Saligrama, and Adam Kalai. 2016. Man is to computer programmer as woman is to homemaker? debiasing word embeddings. In Proceedings of the 30th International Conference on Neural Information Processing Systems (NIPS'16). Curran Associates Inc., Red Hook, NY, USA, 4356-4364.
"""

def neutralize(word, g, word_to_vec_map):
    """
    Removes the bias of "word" by projecting it on the space orthogonal to the bias axis.
    This function ensures that gender neutral words are zero in the gender subspace.

    Arguments:
        word -- string indicating the word to debias
        g -- numpy-array of shape (100,), corresponding to the bias axis (such as gender)
        word_to_vec_map -- dictionary mapping words to their corresponding vectors. ok
    Returns:
        e_debiased -- neutralized word vector representation of the input "word"
    """

    ### START CODE HERE ###
    # Select word vector representation of "word". Use word_to_vec_map. (≈ 1 line)
    e = word_to_vec_map[word]

    # Compute e_biascomponent using the formula give above. (≈ 1 line)
    e_biascomponent = np.dot(e,g) / (np.linalg.norm(g))**2 * g

    # Neutralize e by substracting e_biascomponent from it
    # e_debiased should be equal to its orthogonal projection. (≈ 1 line)
    e_debiased = e - e_biascomponent
    ### END CODE HERE ###

    return e_debiased

e = "receptionist"
print("cosine similarity between " + e + " and vgender, before neutralizing: ", cosine_similarity(word_to_vec_map["receptionist"], vgender))

e_debiased = neutralize("receptionist", vgender, word_to_vec_map)
print("cosine similarity between " + e + " and vgender, after neutralizing: ", cosine_similarity(e_debiased, vgender))

"""Next, lets see how debiasing can also be applied to word pairs such as "actress" and "actor." Equalization is applied to pairs of words that you might want to have differ only through the gender property. As a concrete example, suppose that "actress" is closer to "babysit" than "actor." By applying neutralizing to "babysit" we can reduce the gender-stereotype associated with babysitting. But this still does not guarantee that "actor" and "actress" are equidistant from "babysit." The equalization algorithm takes care of this.

The key idea behind equalization is to make sure that a particular pair of words are equally distant.
"""

def equalize(pair, bias_axis, word_to_vec_map):
    """
    Debias gender specific words by following the equalize method described in the figure above.

    Arguments:
    pair -- pair of strings of gender specific words to debias, e.g. ("actress", "actor")
    bias_axis -- numpy-array of shape (100,), vector corresponding to the bias axis, e.g. gender
    word_to_vec_map -- dictionary mapping words to their corresponding vectors

    Returns
    e_1 -- word vector corresponding to the first word
    e_2 -- word vector corresponding to the second word
    """

    ### START CODE HERE ###
    # Step 1: Select word vector representation of "word". Use word_to_vec_map. (≈ 2 lines)
    w1, w2 = pair
    e_w1, e_w2 = word_to_vec_map[w1], word_to_vec_map[w2]

    # Step 2: Compute the mean of e_w1 and e_w2 (≈ 1 line)
    mu = (e_w1 + e_w2) / 2

    # Step 3: Compute the projections of mu over the bias axis and the orthogonal axis (≈ 2 lines)
    mu_B = np.dot(mu,bias_axis) / (np.linalg.norm(bias_axis))**2 * bias_axis
    mu_orth = mu - mu_B

    # Step 4: Use equations (7) and (8) to compute e_w1B and e_w2B (≈2 lines)
    e_w1B = np.dot(e_w1,bias_axis) / (np.linalg.norm(bias_axis))**2 * bias_axis
    e_w2B = np.dot(e_w2,bias_axis) / (np.linalg.norm(bias_axis))**2 * bias_axis

    # Step 5: Adjust the Bias part of e_w1B and e_w2B using the formulas (9) and (10) given above (≈2 lines)
    corrected_e_w1B = (np.sqrt(np.linalg.norm(1-np.linalg.norm(mu_orth)**2)) * (e_w1B - mu_B) /
    np.linalg.norm(e_w1 - mu_orth - mu_B))
    corrected_e_w2B = (np.sqrt(np.linalg.norm(1-np.linalg.norm(mu_orth)**2)) * (e_w2B - mu_B) /
    np.linalg.norm(e_w2 - mu_orth - mu_B))

    # Step 6: Debias by equalizing e1 and e2 to the sum of their corrected projections (≈2 lines)
    e1 = corrected_e_w1B + mu_orth
    e2 = corrected_e_w2B + mu_orth

    ### END CODE HERE ###

    return e1, e2

print("cosine similarities before equalizing:")
print("cosine_similarity(word_to_vec_map[\"man\"], gender) = ", cosine_similarity(word_to_vec_map["man"], vgender))
print("cosine_similarity(word_to_vec_map[\"woman\"], gender) = ", cosine_similarity(word_to_vec_map["woman"], vgender))
print()
e1, e2 = equalize(("man", "woman"), vgender, word_to_vec_map)
print("cosine similarities after equalizing:")
print("cosine_similarity(e1, gender) = ", cosine_similarity(e1, vgender))
print("cosine_similarity(e2, gender) = ", cosine_similarity(e2, vgender))
