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
    
    def __repr__(self) -> str:
        return "(User: {0}, Text: {1})".format(self.user, self.text)
