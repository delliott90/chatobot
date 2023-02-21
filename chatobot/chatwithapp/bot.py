# bot.py

# Test from CLI with 
# python manage.py shell
# from chatwithapp.bot import Bot
# THE_BOT = Bot()
# THE_BOT.query_bot('my sampel query')
# test with some chat for example:
# >>> THE_BOT.query_bot('do you like plants?')
# {'bot_q': 'do you like plants?', 'bot_r': <Statement text:Oh that's great!>}
# exit() to leave CLI

# Note how the chat bot added it's own tables to the existing sqlite database under the chatobot project

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from ast import literal_eval as make_tuple
import os


class Bot():
    def __init__(self) -> None:
        self.chatbot = ChatBot("Chatpot")
        self.exit_conditions = (":q", "quit", "exit")
        self.trainer = ListTrainer(self.chatbot)

    def train_bot(self, training_tuppel):
        training_tuppel = training_tuppel.split(":")
        self.trainer.train(training_tuppel)

    # Takes in a corpus text file which contains a tuple of chat strings
    def train_bot_with_corpus(self, corpus):
        file_path = os.path.join(os.path.dirname(__file__), corpus)
        with open(file_path, "r") as corpus_file:
            content = corpus_file.read()
        content = make_tuple(content)
        self.trainer.train(content)
        corpus_file.close()


    def query_bot(self, query):
        return {"bot_q": query, "bot_r": self.chatbot.get_response(query)}