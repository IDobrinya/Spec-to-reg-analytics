from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def preprocess_text(text):
    # Приведение к нижнему регистру
    text = text.lower()
    text = text.replace(",", "")
    text = text.replace(".", "")
    # Разбиение на слова
    words = text.split()
    # Удаление стоп-слов
    stop_words = set(stopwords.words('russian'))
    words = [word for word in words if word not in stop_words]
    # Лемматизация
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    # Объединение обратно в строку
    return ' '.join(words)