import math
import re

class Bayes_Classifier:

    def __init__(self):
        pass

    def remove_capitalization(self, text: list):
        """
        Function to remove the capitalization from the data.\n
        Args:\n
            text: list = list of sentimnet data.\n
        Returns:\n
            text in lower case.\n
        """
        # Removing capitalization from the data
        for i in range(len(text)):
            text[i] = text[i].lower()

        return text

    def remove_punctuation(self, text: list):
        """
        Function to remove punctutation from the data.\n
        Args:\n
            text: list = list of sentiment data.\n
        Returns:\n
            text without punctuation.\n
        """
        # Removing the punctuation using regular expression (ie re.sub)
        regex = re.compile('[%s]' % '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')
        for i in range(len(text)):
            text[i] = regex.sub('',text[i])

        return text
    
    def get_counter(self, text: list, labels: list):
        """
        Function to create counter of words in text corpus.\n
        Args:\n
            text: list = list of sentiment data.\n
        Returns:\n
            counter dictionary which has the information about the occurence of words in text corpus.\n
        """
        dict_counter_label_1 = {}
        dict_counter_label_5 = {}
        for i in range(len(labels)):
            words = text[i].split()
            if labels[i] == "1":
                for word in words:
                    try:
                        dict_counter_label_1[word] += 1
                    except:
                        dict_counter_label_1[word] = 1

            else:
                for word in words:
                    try:
                        dict_counter_label_5[word] += 1
                    except:
                        dict_counter_label_5[word] = 1

        return dict_counter_label_1, dict_counter_label_5

    
    def remove_stop_words(self, text: list):
        """
        Function to remove stop from the data.\n
        Args:\n
            text: list = list of sentiment data.\n
        Returns:\n
            text without stop words.\n
        """
        # Removing stop words from the text
        # list of stop words, got the list from nltk
        stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", 
                     "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 
                     'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 
                     'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 
                     'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 
                     'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 
                     'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 
                     'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 
                     'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', 
                     "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
        
        for i in range(len(text)):
            words = text[i].split() # Splitting the text into words, this would result into a list
            filtered_words = [word for word in words if word not in stopwords]
            text[i] = " ".join(filtered_words)

        return text
    
    def get_class_dist(self, labels):
        """
        Function to get the class dist.\n
        Args:
            labels = labels of the training data.\n
        return:
            number of 1 class and number of 5 class.\n
        """

        # Class distribution
        class_1 = [1 for l in labels if l=="1"]
        class_5 = [1 for l in labels if l=="5"]

        return sum(class_1), sum(class_5)

    def preprocess_text(self, data: list):
        """
        Function to preprocess the data.\n
        This function  will also extract the labels.\n
        Args:
            data: list of strings
        """

        labels = []
        text = []
        for i in data:
            # removing the new line character
            line = i.replace('\n', '')
            # Splitting the line into three components (ie label, wid, text)
            fields = line.split('|')
            text.append(fields[-1])
            labels.append(fields[0])

        # As a preprocessing step we will remove the capitalization from the text corpus
        text = self.remove_capitalization(text)
        # Removal of punctuation
        text = self.remove_punctuation(text)
        # Removal of stop words
        text = self.remove_stop_words(text)

        return text, labels


    def train(self, lines):
        text, labels = self.preprocess_text(lines)
        # Getting the class distribution
        self.class_1, self.class_5 = self.get_class_dist(labels)
        # Getting the counter for the whole text corpus
        self.dict_counter_label_1, self.dict_counter_label_5 = self.get_counter(text, labels)
        self.vocab_size = len(set(self.dict_counter_label_1.keys()).union(set(self.dict_counter_label_5.keys())))
        self.number_words_label_5 = sum(self.dict_counter_label_1.values())
        self.number_words_label_1 = sum(self.dict_counter_label_1.values())

    def get_prob(self,word, dict_counter, number_words_label):
        """
        Function to get the probability with the laplace smoothing
        Args:
            word: the word in which we need the probability of.\n
            dict_counter: dictionary counter of that class.\n
            number_of_words: number of words for that particular class.\n
        Returns:
            probability of that word in conditioned to that class.\n
        """
        
        if word in dict_counter.keys():
            occurence = dict_counter[word]
        else:
            occurence = 0
        prob = (occurence + 1)/(number_words_label + self.vocab_size)
        return prob

    
    def classify(self, lines):
        prediction = []
        text_preprocessed = self.preprocess_text(lines)[0] # This function will handle all the preprocessing
        for i in range(len(text_preprocessed)):
            label_1_prob = 1
            label_5_prob = 1
            words = text_preprocessed[i].split()
            for word in words:
                label_1_prob *= self.get_prob(word, self.dict_counter_label_1, self.number_words_label_1)
                label_5_prob *= self.get_prob(word, self.dict_counter_label_5, self.number_words_label_5)

            label_1_prob = label_1_prob*(self.class_1/(self.class_1 + self.class_5))
            label_5_prob = label_5_prob*(self.class_5/(self.class_1 + self.class_5))

            if label_1_prob >= label_5_prob:
                prediction.append("1")
            else:
                prediction.append("5")

        return prediction                

                

        
