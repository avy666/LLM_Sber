import torch
from transformers import BertTokenizer, BertModel


class BertEmbeddingExtractor:
    """
    Класс для извлечения различных типов эмбеддингов из BERT модели.
    Поддерживает работу с многоязычной версией BERT.
    """

    def __init__(self):
        # Инициализация токенизатора и модели BERT
        # Используется многоязычная версия BERT для поддержки разных языков
        self.tokenizer = BertTokenizer.from_pretrained(
            'google-bert/bert-base-multilingual-uncased')
        self.model = BertModel.from_pretrained(
            'google-bert/bert-base-multilingual-uncased', output_attentions=True) # Added output_attentions=True
        # Переключение модели в режим оценки (отключение dropout и т.д.)
        self.model.eval()

    def get_tokenization(self, text):
        """
        Получение результатов токенизации для входного текста.

        Args:
            text (str): Входной текст для токенизации

        Returns:
            dict: Словарь с ID токенов и их текстовыми представлениями
        """
        tokens = self.tokenizer(text, return_tensors='pt')
        return {
            'input_ids': tokens['input_ids'],
            'tokens': self.tokenizer.convert_ids_to_tokens(tokens['input_ids'][0])
        }

    def get_embeddings(self, text):
        """
        Извлечение различных типов эмбеддингов из текста.

        Args:
            text (str): Входной текст для анализа

        Returns:
            dict: Словарь с различными типами эмбеддингов:
                - token_embeddings: эмбеддинги для каждого токена
                - position_embeddings: позиционные эмбеддинги
                - token_type_embeddings: эмбеддинги типов токенов
                - cls_vector: вектор специального токена [CLS]
                - tokens: список токенов
                - attention_weights: attention weights
        """
        # Токенизация входного текста
        tokens = self.tokenizer(text, return_tensors='pt')

        # Получение эмбеддингов с отключенным расчетом градиентов
        with torch.no_grad():
            outputs = self.model(**tokens, output_hidden_states=True)

        # Извлечение различных типов эмбеддингов
        # Эмбеддинги слов для каждого токена
        token_embeddings = self.model.embeddings.word_embeddings(
            tokens['input_ids'])[0]
        # Позиционные эмбеддинги для каждой позиции в последовательности
        position_embeddings = self.model.embeddings.position_embeddings(
            torch.arange(tokens['input_ids'].shape[1]).unsqueeze(0))[0]
        # Эмбеддинги типов токенов (для различения разных сегментов текста)
        token_type_embeddings = self.model.embeddings.token_type_embeddings(
            torch.zeros_like(tokens['input_ids']))[0]

        # Получение вектора [CLS] - агрегированного представления всего предложения
        cls_vector = outputs.last_hidden_state[0][0]

        # Формирование результирующего словаря
        return {
            'token_embeddings': token_embeddings.detach().numpy(),
            'position_embeddings': position_embeddings.detach().numpy(),
            'token_type_embeddings': token_type_embeddings.detach().numpy(),
            'cls_vector': cls_vector.detach().numpy(),
            'tokens': self.tokenizer.convert_ids_to_tokens(tokens['input_ids'][0]),
            'attention_weights': outputs.attentions
        }