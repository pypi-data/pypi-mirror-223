# statistics/frequenciesOfItems.py

class FrequenciesOfItems:
    def __init__(self, transactional_db, separator='\t'):
        self.transactional_db = transactional_db
        self.separator = separator
        self.items_freq_dict = {}

    def calculate_frequencies(self):
        with open(self.transactional_db, 'r') as file:
            for line in file:
                items = line.strip().split(self.separator)
                for item in items:
                    if item not in self.items_freq_dict:
                        self.items_freq_dict[item] = 1
                    else:
                        self.items_freq_dict[item] += 1

    def get_frequencies(self):
        return self.items_freq_dict
