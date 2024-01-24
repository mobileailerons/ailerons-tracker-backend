""" Article Model """

class Article:
    """ Model for a news article. """

    def __init__(self, data):
        self.title = data["title"]
        self.content = data["content"]
        self.image_url = data["image_url"]
        self.published = data["published"]
        self.archived = data["archived"]
        self.publication_date = data["publication_date"]
        