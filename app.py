from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import random
import glob
from datetime import datetime
import os

try:
    from .modules.markov import Markov
    from .modules import data_provider
except:
    from modules.markov import Markov
    from modules import data_provider

# MONGO SETUP
host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/tweetgen')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
tweets = db['tweets']
text_sources = db['text_sources']

# GLOBAL VARIABLES
DEFAULT_SENTENCE_SIZE = 2
DEFAULT_MARKOV_ORDER = 2
app = Flask(__name__)

# Dict to store markov chains. Key=filename Value=Markov object
markov_chains = {}

# Routes
@app.route("/")
def redirect_to_welcome():
    """Setup Database and Markov Chains for all the text sources."""

    # Add documents into text sources
    global_home_path = os.getcwd() + "/static/text/"

    print("Setting up chains")
    print("Global path: {}".format(global_home_path))

    for file in glob.glob(global_home_path + "*.txt"):
        filename = os.path.basename(file)
        raw_name = filename.split(".txt")[0]

        print("Examaning file: {}".format(filename))

        if text_sources.count_documents({'name': raw_name}) == 0:
            new_text = {
                'name': raw_name,
                'path': os.path.join(global_home_path, filename),
                'sentence_list': data_provider.get_sentence_list_from_corpus(os.path.join(global_home_path, filename))}

            text_sources.insert_one(new_text)
            print("Inserted {} into text_sources".format(new_text['name']))

            print("-----------------------------------------------")

    # Build markov chains for all text-sources
    for item in text_sources.find({}):
        print("I am in file: {}".format(item['name']))
        filename = item['name']
        if filename not in markov_chains.keys():
            markov_chains[filename] = Markov()
            markov_chains[filename].build_chain_n_order(item['sentence_list'], DEFAULT_MARKOV_ORDER)

            print("Built chain for source -> {}".format(filename))

    print("Markov chain keys from setup database: {}".format(markov_chains.keys()))

    return redirect(url_for('show_welcome'))


@app.route("/welcome")
def show_welcome():
    """Show welcome page where you can pick the books that you want to base the tweet generator off of."""

    print("Markov chain keys from welcome: {}".format(markov_chains.keys()))

    name_list = []
    for text_source in text_sources.find({}):
        source_name = text_source['name']
        if source_name not in name_list:
            name_list.append(source_name)

    return render_template("welcome.html", text_sources=name_list)


@app.route("/setup/<source_name>", methods=['POST'])
def setup_for_source(source_name):
    """Setups program for source_name and shows dashboard."""

    # Generate first tweet for this source
    print("Markov chain keys from setup source: {}".format(markov_chains.keys()))

    # Avoiding wierd error that sometimes happens
    if source_name not in markov_chains:
        markov_chains[source_name] = Markov()
        markov_chains[source_name].build_chain_n_order(text_sources.find_one({'name': source_name})['sentence_list'], DEFAULT_MARKOV_ORDER)
        print("built chain because source name wasnt in markov chains")

    tweet = []
    for i in range(0, DEFAULT_SENTENCE_SIZE):
        tweet.append(markov_chains[source_name].generate_sentence_n_order(DEFAULT_MARKOV_ORDER))
    tweet = " ".join(tweet)

    return redirect(url_for(
        "show_dashboard",
        source_id=str(text_sources.find_one({'name': source_name})['_id']),
        tweet=tweet,
        num_sentences=DEFAULT_SENTENCE_SIZE,
        from_save=False))

@app.route("/setup/random")
def setup_random():
    """Setups program using a random text-source."""

    source_name = None

    random_index = random.randint(0, text_sources.count_documents({}) - 1)
    print("Random index: {}".format(random_index))
    counter = 0
    for source in text_sources.find():
        if random_index == counter:
            source_name = source['name']
            break
        counter += 1

    # Avoiding wierd error that sometimes happens
    if source_name not in markov_chains:
        markov_chains[source_name] = Markov()
        markov_chains[source_name].build_chain_n_order(text_sources.find_one({'name': source_name})['sentence_list'], DEFAULT_MARKOV_ORDER)
        print("built chain because source name wasnt in markov chains")

    tweet = []
    for i in range(0, DEFAULT_SENTENCE_SIZE):
        tweet.append(markov_chains[source_name].generate_sentence_n_order(DEFAULT_MARKOV_ORDER))
    tweet = " ".join(tweet)

    return redirect(url_for(
        "show_dashboard",
        source_id=str(text_sources.find_one({'name': source_name})['_id']),
        tweet=tweet,
        num_sentences=DEFAULT_SENTENCE_SIZE,
        from_save=False))


@app.route("/dashboard/<source_id>/<from_save>/<num_sentences>/<tweet>")
def show_dashboard(source_id, num_sentences, tweet, from_save):
    """Show dashboard."""

    if not from_save:
        from_save = request.form.get('from_save')

    return render_template(
        "index.html",
        source_name=str(text_sources.find_one({'_id': ObjectId(source_id)})['name']),
        source_id=source_id,
        tweet=tweet,
        num_sentences=num_sentences,
        from_save=from_save)


@app.route("/generate/<source_id>", methods=['POST'])
def generate_tweet(source_id):
    """Generate tweet with an input number of words."""

    print("Markov chain keys from generate_tweet: {}".format(markov_chains.keys()))

    num_sentences = int(request.form.get("num_sentences"))
    from_save = request.form.get("from_save")

    source_name = text_sources.find_one({'_id': ObjectId(source_id)})['name']

    # Avoiding wierd error that sometimes happens
    if source_name not in markov_chains:
        markov_chains[source_name] = Markov()
        markov_chains[source_name].build_chain_n_order(text_sources.find_one({'name': source_name})['sentence_list'], DEFAULT_MARKOV_ORDER)
        print("built chain because source name wasnt in markov chains")

    tweet = []
    for i in range(0, num_sentences):
        tweet.append(markov_chains[source_name].generate_sentence_n_order(DEFAULT_MARKOV_ORDER))
    tweet = " ".join(tweet)

    return redirect(url_for(
        "show_dashboard",
        source_id=source_id,
        tweet=tweet,
        num_sentences=num_sentences,
        from_save=from_save))

@app.route("/save/<source_id>/<tweet>/<num_sentences>")
def save_tweet(source_id, num_sentences, tweet):
    """Save tweet to database."""
    tweet = {
        'data': tweet,
        'author': text_sources.find_one({'_id': ObjectId(source_id)})['name'],
        'liked_date': datetime.now()
    }
    tweets.insert_one(tweet)

    return redirect(url_for(
        'show_dashboard',
        source_id=source_id,
        tweet=tweet['data'],
        num_sentences=num_sentences,
        from_save=True))

@app.route("/favorites", methods=['POST'])
def show_favorites():
    """Show the 5 most recent favorite tweets."""

    source_id = request.form.get('source_id')
    num_sentences = request.form.get('num_sentences')
    tweet = request.form.get('tweet')

    recent_fav_tweets = list(tweets.find().sort([('liked_date', -1)]).limit(4))

    return render_template(
        "favorites.html",
        favorite_tweets=recent_fav_tweets,
        current_tweet=tweet,
        source_id=source_id,
        num_sentences=num_sentences,
        from_save=True)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
