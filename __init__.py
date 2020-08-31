# """Setup database."""
#
# from pymongo import MongoClient
# import os
# import glob
#
# from .modules import data_provider
#
# # MONGO SETUP
# host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/tweetgen')
# client = MongoClient(host=f'{host}?retryWrites=false')
# db = client.get_default_database()
# tweets = db['tweets']
# text_sources = db['text_sources']
#
# # Clean text_sources collection
# text_sources.delete_many({})
#
# # Add documents into text sources
# global_home_path = os.getcwd() + "/static/text/"
#
# print("Setting up chains")
# print("Global path: {}".format(global_home_path))
#
# for file in glob.glob(global_home_path + "*.txt"):
#     filename = os.path.basename(file)
#     raw_name = filename.split(".txt")[0]
#
#     print("Examaning file: {}".format(filename))
#
#     if text_sources.count_documents({'name': raw_name}) == 0:
#         new_text = {
#             'name': raw_name,
#             'path': os.path.join(global_home_path, filename),
#             'sentence_list': data_provider.get_sentence_list_from_corpus(os.path.join(global_home_path, filename))}
#
#         text_sources.insert_one(new_text)
#         print("Inserted {} into text_sources".format(new_text['name']))
#
#         print("-----------------------------------------------")
