from haystack import indexes
from .models import Book


class BookIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    isbn  = indexes.CharField(model_attr='isbn')

    def prepare(self, object):
        self.prepared_data = super(BookIndex, self).prepare(object)
        try:
            if object.author:
                self.prepared_data['author'] = object.author.name

            if object.author.bio:
                self.prepared_data['bio'] = object.author.bio

            if object.genre:
                self.prepared_data['genre'] = object.genre.name

            if object.summary:
                self.prepared_data['summary'] = object.summary.text
        except:
            pass

        return self.prepared_data

    def get_model(self):
        return Book
