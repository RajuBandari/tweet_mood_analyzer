import re
import csv
import nltk.classify


#STEP1) PREPROCESSING TEXT
#-----------------------------------------------------
# Method: for preprocessing the text
# Input:  any text as string
#-----------------------------------------------------
def process_text(text):
    text = text.lower()                                                 # step1: converting text to lower case
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',text)       # step2: converting links to URL
    text = re.sub('@[^\s]+','AT_USER',text)                             # step3: removing user names to AT_USER   
    text = re.sub('[\s]+', ' ', text)                                   # step4: removing extra spaces
    text = re.sub(r'#([^\s]+)', r'\1', text)                            # step5: replacing hashtags with tag text
    text = text.strip('\'"')                                            # step6: trimming the text- removing traling spaces
    return text

#STEP2) BUILDING FEATURE VECTOR
#-----------------------------------------------------
# Method: For building feature vector
# Input:  any text as string, stop words
#-----------------------------------------------------
def build_feature_vector(text, stop_words):
    #intializing the variables
    feature_vector = []  
    words = text.split()
    for word in words:
        pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
        word = pattern.sub(r"\1\1", word)                                                     # step 1) Removing repeating characters 
        word = word.strip('\'"?,.')                                                           # step 2) Removing punctuation marks
        validation = re.search(r"^[a-zA-Z][a-zA-Z0-9]*[a-zA-Z]+[a-zA-Z0-9]*$", word)          # step 3) validating if it consits only words
        if(word in stop_words or validation is None):                                         # step 4) ignroing stop words and words that fail in above validation
            continue
        else:
            feature_vector.append(word.lower())                                               # if it is the valid word adding to feature vector
    return feature_vector    


#STEP3) FOR EXTRATING FEATURES FROM TEXT
#-----------------------------------------------------
# Method: for exact featured from the input text
# Input:  any text as string
#-----------------------------------------------------
def extract_features(text):
    words_list = set(text)                                                                  # step 1) Splitting the sentence into words
    # intializing dictionary of features
    features = {}                   
    for word in feature_list:
        features['contains(%s)' % word] = 1 if (word in words_list) else 0                  # step 2) Building features dictionary by checking if the word in featuresList 
    return features


#-----------------------------------------------------
# Method: Internal method for reading stop words from file
# Input:  stopwords containing file name
#-----------------------------------------------------
def read_stop_words(file_name):
    # initializing
    stop_words = []
    stop_words.append('AT_USER')
    stop_words.append('URL')
    # reading line by line - each line contains only one word
    fp = open(file_name, 'r')
    line = fp.readline()
    while line:
        word = line.strip() # removing trailing spaces
        stop_words.append(word) # adding to array
        line = fp.readline()
    fp.close()
    return stop_words


# Main method for processing and training a classifier 
#-----------------------------------------------------
# Method: Method takes the input text and gives its *sentiment*
# Input:  input text
#-----------------------------------------------------
def classify(tweetText):
    # intializing varaibles
    global feature_list
    global tweets
    global NBClassifier

    feature_list = []
    tweets = []
    
    traing_tweets = csv.reader(open('training_set.csv', 'rb'), delimiter=',')           # step 1) Reading training set data from csv file
    stop_words = read_stop_words('stop_words.txt')  # for reading stop words
    for row in traing_tweets:
        sentiment = row[2]                          # manually annotated sentiment
        tweet = row[1]                              # tweet for training
        processed_tweet = process_text(tweet)                                           # step 2) Processing tweet
        feature_vector = build_feature_vector(processed_tweet, stop_words)              # step 3) building feature vector
        feature_list.extend(feature_vector)
        tweets.append((feature_vector, sentiment));
    feature_list = list(set(feature_list)) # Removing duplicates in feature list
    training_set = nltk.classify.util.apply_features(extract_features, tweets)          # step 4) generating training set using NLTK
    train_set = training_set[0:112]
    test_set = training_set[112:]
    NBClassifier = nltk.NaiveBayesClassifier.train(train_set)                        # step 5) training the Naive Bayes classifier
    print("Classifier accuracy percent:",(nltk.classify.accuracy(NBClassifier, test_set))*100)
 
    
    #-------------------------------------------------------------------------
    # actual real time tweet processing
    #-------------------------------------------------------------------------
    # processing user inut tweet
    processed_tweet = process_text(tweetText)
    # classifying tweet using our classifier
    sentiment = NBClassifier.classify(extract_features(build_feature_vector(processed_tweet, stop_words)))
    # returning output(sentiment) of the classfier
    return sentiment


         
print classify('happy today')


