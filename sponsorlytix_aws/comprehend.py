import boto3


class Comprehend:

    def __init__(self, text, language='en'):
        self.language = language
        self.text = text
        self.comprehend = boto3.client('comprehend', 'us-east-2')

    def get_comprehend_data(self):
        comprehend_data = {
            'entity': self.__get_entities(),
            'key_phrases': self.__get_key_phrases(),
            'sentiment': self.__get_sentiment()
        }
        return comprehend_data

    def __get_entities(self):
        entities = self.comprehend.detect_entities(Text=self.text, LanguageCode=self.language)
        return entities.get('Entities')

    def __get_key_phrases(self):
        phrases = self.comprehend.detect_key_phrases(Text=self.text, LanguageCode=self.language)
        return phrases.get('KeyPhrases')

    def __get_sentiment(self):
        sentiment = self.comprehend.detect_sentiment(Text=self.text, LanguageCode=self.language)
        return {
            'score': sentiment.get('SentimentScore'),
            'sentiment': sentiment.get('Sentiment')
        }
