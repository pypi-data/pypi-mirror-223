class frequenciesOfItems:
    def __init__(self, transactional_db, separator='\t'):
        self.transactional_db = transactional_db
        self.separator = separator
        self.items_freq_dict = {}

    def getFrequencies(self):
        # Initialize the frequency dictionary
        self.items_freq_dict = {}

        # Split the transactional database into individual transactions
        transactions = self.transactional_db.split('\n')

        # Iterate through each transaction to calculate frequencies
        for transaction in transactions:
            items = transaction.split(self.separator)
            for item in items:
                if item.strip():  # Check if the item is not an empty string after stripping leading/trailing whitespaces
                    if item in self.items_freq_dict:
                        self.items_freq_dict[item] += 1
                    else:
                        self.items_freq_dict[item] = 1

        return self.items_freq_dict

