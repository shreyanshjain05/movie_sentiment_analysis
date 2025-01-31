from flask import Flask, request, render_template
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
import pandas as pd

# Initialize Flask app
app = Flask(__name__, template_folder='templates')
app.secret_key = 'your_secret_key'

# Load the pre-trained model
model = tf.keras.models.load_model('sentiment_analysis.h5')

# Load the dataset and initialize Tokenizer
dataset = 'IMDB Dataset.csv'
df = pd.read_csv(dataset)
tokenizer = Tokenizer(num_words=5000)
tokenizer.fit_on_texts(df['review'])

# Function to predict sentiment
def predict_sentiment(review):
    # Tokenize and pad the review
    sequence = tokenizer.texts_to_sequences([review])
    padded_sequence = pad_sequences(sequence, maxlen=200)
    prediction = model.predict(padded_sequence)
    sentiment = "positive" if prediction[0][0] > 0.5 else "negative"
    return sentiment

# Home route
@app.route('/')
def home():
    return render_template('review.html')

# Review analysis route (to match form action)
@app.route('/analyze', methods=['POST'])
def analyze():
    if request.method == 'POST':
        # Getting review from the form
        review = request.form['review']
        sentiment = predict_sentiment(review)
        # Returning the result to the template
        return render_template('review.html', sentiment=sentiment)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
