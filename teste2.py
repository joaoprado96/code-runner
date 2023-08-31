from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from gensim import corpora, models
from collections import Counter

# Certifique-se de baixar o conjunto de palavras irrelevantes (stopwords) do NLTK antes de rodar o código.
# Você pode fazer isso com o seguinte comando: nltk.download('stopwords')

def analyze_comments(comments_list):
    # Tokenizar e remover stopwords de cada comentário
    texts = [[word for word in word_tokenize(comment.lower()) if word not in stopwords.words('english')]
             for comment in comments_list]

    # Criar um dicionário e corpus com base nos textos processados
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    # Aplicar o modelo LDA
    lda_model = models.LdaModel(corpus, num_topics=3, id2word=dictionary, passes=15)

    # Coletar palavras-chave dos tópicos mais relevantes
    keywords = []
    for idx, topic in lda_model.print_topics(-1):
        # Coleta apenas as palavras, ignorando os pesos
        words = topic.split("+")
        for word in words:
            keywords.append(word.split("*")[1].replace('"', '').replace(' ', ''))

    # Contar a frequência das palavras-chave e pegar as mais comuns
    keyword_frequencies = Counter(keywords)
    most_common_keywords = keyword_frequencies.most_common(5)

    # Criar uma descrição baseada nas palavras-chave mais frequentes
    description = "Este código parece lidar com: " + ', '.join([keyword[0] for keyword in most_common_keywords])

    return description

# Exemplo de uso
comments = [
    "# Initialize variables",
    "# Compute the factorial",
    "# This function checks for prime numbers",
    "# Loop through the array",
    "# Handle exceptions"
]

print(analyze_comments(comments))
