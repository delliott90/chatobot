# cleaner.py

# Test from CLI with 
# Make sure training txt file is included in scripts folder
# python manage.py shell
# from chatwithapp.scripts.cleaner import Clenaer
# THE_CLEANER = Cleaner()
# THE_CLEANER.remove_chat_metadata('training_chat.txt', 'cleaned_corpus.txt')
# cleaned_corpus.txt should be created in chatwithapp directory
# exit() to leave CLI

import re, os, csv

class Cleaner():

    def __init__(self) -> None:
        self.root_path = os.path.dirname(__file__)
        

    def clean_csv_data(self, chat_export_file, clean_data_file) -> None:
        chat_export_file = os.path.join(self.root_path, chat_export_file)
        csv_reader = csv.reader(open(chat_export_file), delimiter=',')
        csv_rows = []
        cleaned_corpus_tuple = tuple()
        tuple_list = []
        for row in csv_reader:
            csv_rows.append(row)
        for index, row in enumerate(csv_rows):
            if index < 1:
                continue
            chat_element = self._remove_twitter_handles(row[4])
            chat_element = self._remove_urls(chat_element)
            tuple_list.append(chat_element)
        cleaned_corpus_tuple = tuple(tuple_list)
        self._write_cleaned_corpus(clean_data_file, cleaned_corpus_tuple)

        
    def clean_wechat_data(self, chat_export_file, clean_data_file) -> None:
        self._remove_wechat_metadata(chat_export_file, clean_data_file)

    def _remove_twitter_handles(self, chat_string):
        handle_regex = r'@\w+'
        return re.sub(handle_regex, "", chat_string)

    def _remove_urls(self, chat_string):
        url_regex = r'https?[^,\'\s]+'
        return re.sub(url_regex, "", chat_string)


    # Takes a raw data file and a clean file
    # Removes date, time, whitespace, and metadata end from WeChat log file
    def _remove_wechat_metadata(self, chat_export_file, clean_data_file) -> None:
        chat_export_file = os.path.join(self.root_path, chat_export_file)
        date_time = r"(\d+\/\d+\/\d+,\s\d+:\d+)"  # e.g. "9/16/22, 06:34"
        dash_whitespace = r"\s-\s"  # " - "
        username = r"([\w\s]+)"  # e.g. "Martin"
        metadata_end = r":\s"  # ": "
        pattern = date_time + dash_whitespace + username + metadata_end

        with open(chat_export_file, "r") as corpus_file:
            content = corpus_file.read()
        cleaned_corpus = re.sub(pattern, "", content)
        corpus_file.close()
        cleaned_corpus_tuple = self._remove_non_message_text(tuple(cleaned_corpus.split("\n")))
        self._write_cleaned_corpus(clean_data_file, cleaned_corpus_tuple)
        # return tuple(cleaned_corpus.split("\n"))

    # Removes media lines from a tuple of WeChat logs
    def _remove_non_message_text(self, export_text_lines):
        messages = export_text_lines[1:-1]
        filter_out_msgs = ("<Media omitted>",)
        return tuple((msg for msg in messages if msg not in filter_out_msgs))

    # Write the cleaned data to a file as a stringified tuple of dialog
    # ex. ('Hi Martin, Philipp here!', 'I’m ready to talk about plants!', ...)
    def _write_cleaned_corpus(self, cleaned_file, cleaned_corpus_tuple):
        with open(cleaned_file, "w") as cleaned_corpus_file:
            cleaned_corpus_file.write(str(cleaned_corpus_tuple))
            # for tup in cleaned_corpus_tuple:
            #     cleaned_corpus_file.write(tup + "\n")
        cleaned_corpus_file.close()
