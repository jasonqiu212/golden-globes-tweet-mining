class Tweet:
    """A class representing a tweet."""

    def __init__(self, text, user):
        self.text = text
        self.user = user
    
    def applyTextPreprocessing(self, f):
        """
        Apply text processing function onto the text of this tweet.

        Args:
            f: Text processing function to apply.
        """
        self.text = f(self.text)
