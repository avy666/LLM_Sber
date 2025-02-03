
import plotly.graph_objects as go
import numpy as np


def create_vector_plot(vector, title):
    """
    Создание табличного представления для одного вектора эмбеддингов.
    
    Args:
        vector (numpy.ndarray): Вектор эмбеддингов для визуализации
        title (str): Заголовок для графика
        
    Returns:
        plotly.graph_objects.Figure: Объект графика Plotly
    """
    # Округление значений вектора до 4 знаков после запятой для читаемости
    vector_rounded = np.round(vector, 4)

    # Создание таблицы с двумя столбцами: размерность и значение
    fig = go.Figure(data=[
        go.Table(
            header=dict(values=['Размерность', 'Значение'], align='left'),
            cells=dict(
                values=[list(range(len(vector))), vector_rounded],
                align='left',
                format=[None, '.4f']  # Форматирование чисел до 4 знаков
            )
        )
    ])

    # Настройка внешнего вида таблицы
    fig.update_layout(
        title=title,
        height=400,  # Фиксированная высота таблицы
        margin=dict(l=50, r=50, t=50, b=50)  # Отступы по краям
    )
    return fig


def create_token_selector(tokens):
    """
    Создание интерфейса выбора токенов.
    
    Args:
        tokens (list): Список токенов
        
    Returns:
        tuple: Индексы и сами токены
    """
    return list(range(len(tokens))), tokens
def create_attention_heatmap(attention_weights, tokens):
    """
    Создание тепловой карты для визуализации внимания между токенами.
    
    Args:
        attention_weights (list): Веса внимания из модели BERT
        tokens (list): Список токенов
    """
    # Получаем веса внимания для первой головы первого слоя
    attention_matrix = attention_weights[0][0][0].numpy()
    
    # Создаем тепловую карту
    fig = go.Figure(data=go.Heatmap(
        z=attention_matrix,
        x=tokens,
        y=tokens,
        colorscale='Viridis'
    ))

    # Настройка внешнего вида
    fig.update_layout(
        title='Тепловая карта внимания между токенами',
        xaxis_title='Целевые токены',
        yaxis_title='Исходные токены',
        height=600,
        width=800
    )
    return fig
