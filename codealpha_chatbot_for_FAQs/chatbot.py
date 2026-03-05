import json
import nltk
import string
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# nltk.download('punkt')
# nltk.download('stopwords')

stop_words = set(stopwords.words("english"))

def preprocess(text):
    text = text.lower()
    tokens = nltk.word_tokenize(text)
    tokens = [
        word for word in tokens
        if word not in stop_words and word not in string.punctuation
    ]
    return " ".join(tokens)

class FAQChatbot:
    def __init__(self, faq_file):
        with open(faq_file, "r") as f:
            self.faqs = json.load(f)

        self.questions = [preprocess(faq["question"]) for faq in self.faqs]

        self.vectorizer = TfidfVectorizer()
        self.question_vectors = self.vectorizer.fit_transform(self.questions)

    def get_response(self, user_input):
        user_input = preprocess(user_input)
        user_vector = self.vectorizer.transform([user_input])

        similarities = cosine_similarity(user_vector, self.question_vectors)
        best_match = similarities.argmax()
        score = similarities[0][best_match]

        if score < 0.3:
            return "Sorry, I couldn't understand your question."

        return self.faqs[best_match]["answer"]