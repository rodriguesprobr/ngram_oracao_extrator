# Baseado em: https://gist.github.com/omri374/ec1c243a5a94a657dae40078d47977b6

import re
from typing import List

import spacy
from spacy.tokens import Doc
from tqdm import tqdm


class PreProcessamento:
    def __init__(
        self,
        spacy_model=None,
        remove_numbers=False,
        remove_special=True,
        remove_hyperlinks=True,
        pos_to_remove=None,
        remove_stopwords=False,
        lemmatize=False
    ):
        """
        Preprocesses text using spaCy
        :param remove_numbers: Whether to remove numbers from text
        :param remove_stopwords: Whether to remove stopwords from text
        :param remove_special: Whether to remove special characters (including numbers)
        :param remove_hyperlinks: Whether to remove hyperlinks
        :param pos_to_remove: list of PoS tags to remove
        :param lemmatize:  Whether to apply lemmatization
        """

        self._remove_numbers = remove_numbers
        self._pos_to_remove = pos_to_remove
        self._remove_stopwords = remove_stopwords
        self._remove_special = remove_special
        self._remove_hyperlinks = remove_hyperlinks
        self._lemmatize = lemmatize

        if not spacy_model:
            self.model = spacy.load("pt_core_news_lg")
        else:
            self.model = spacy_model

    @staticmethod
    def load_model(model="pt_core_news_lg"):
        return spacy.load(model, disable=["ner", "parser"])

    def tokenize(self, text) -> List[str]:
        """
        Tokenize text using a spaCy pipeline
        :param text: Text to tokenize
        :return: list of str
        """
        doc = self.model(text)
        return [token.text for token in doc]

    def preprocess_text(self, text) -> str:
        """
        Runs a spaCy pipeline and removes unwanted parts from text
        :param text: text string to clean
        :return: str, clean text
        """
        if self._remove_hyperlinks is True:
            text = re.sub(
                r'(https?:\/\/)(\s)*(www\.)?(\s)*((\w|\s)+\.)*([\w\-\s]+\/)*([\w\-]+)((\?)?[\w\s]*=\s*[\w\%&]*)*',
                "",
                text,
                flags=re.MULTILINE)
        doc = self.model(text)
        return self.__clean(doc)

    def preprocess_text_list(self, texts=List[str]) -> List[str]:
        """
        Runs a spaCy pipeline and removes unwantes parts from a list of text.
        Leverages spaCy's `pipe` for faster batch processing.
        :param texts: List of texts to clean
        :return: List of clean texts
        """
        clean_texts = []
        for doc in tqdm(self.model.pipe(texts)):
            clean_texts.append(self.__clean(doc))

        return clean_texts

    def __clean(self, doc: Doc) -> str:

        tokens = []
        # POS Tags removal
        if self._pos_to_remove:
            for token in doc:
                if token.pos_ not in self._pos_to_remove:
                    tokens.append(token)
        else:
            tokens = doc

        # Remove Numbers
        if self._remove_numbers:
            tokens = [
                token for token in tokens if not (token.like_num or token.is_currency)
            ]

        # Remove Stopwords
        if self._remove_stopwords:
            tokens = [token for token in tokens if not token.is_stop]
        # remove unwanted tokens
        tokens = [
            token
            for token in tokens
            if not (
                token.is_punct or token.is_space or token.is_quote or token.is_bracket
            )
        ]

        # Remove empty tokens
        tokens = [token for token in tokens if token.text.strip() != ""]

        # Lemmatize
        if self._lemmatize:
            text = " ".join([token.lemma_ for token in tokens])
        else:
            text = " ".join([token.text for token in tokens])

        if self._remove_special:
            # Remove non alphabetic characters
            text = re.sub(r"[^a-zA-ZÀ-ÿ\']", " ", text)
        # remove non-Unicode characters
        # text = re.sub(r"[^\x00-\x7F]+", "", text)

        text = text.lower()

        return text
