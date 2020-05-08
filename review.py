class Review:
    def __init__(self, date, content,score):
        self.date = date
        self.content = content
        self.score = score



    def create_dictionary(self):
        return {
            'date': self.date,
            'content': self.content,
            'score':self.score

        }
