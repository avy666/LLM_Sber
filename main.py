
import streamlit as st
from bert_utils import BertEmbeddingExtractor
from visualization import create_vector_plot, create_attention_heatmap
from styles import get_styles

# Инициализация состояния сессии
# Создаем экстрактор BERT только один раз при запуске приложения
if 'bert_extractor' not in st.session_state:
    st.session_state.bert_extractor = BertEmbeddingExtractor()

# Получение стилей для оформления
styles = get_styles()

# Конфигурация страницы
st.set_page_config(
    page_title="Визуализация BERT Эмбеддингов",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Применение пользовательских стилей CSS
st.markdown("""
    <style>
    /* Градиентный фон для всего приложения */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    /* Стилизация кнопок */
    .stButton>button {
        width: 100%;
        margin-top: 1rem;
        background: linear-gradient(45deg, #2193b0, #6dd5ed);
        color: white;
        border-radius: 10px;
        padding: 0.8rem 1.5rem;
        border: none;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    /* Эффект при наведении на кнопку */
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    /* Стилизация текстового поля */
    .stTextArea>div>div>textarea {
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Заголовок и описание с пользовательским стилем
st.markdown("""
    <div style='background: linear-gradient(45deg, #2193b0, #6dd5ed); padding: 2rem; border-radius: 15px; color: white; text-align: center; margin-bottom: 2rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
        <h1>Визуализация BERT Эмбеддингов</h1>
        <p style='font-size: 1.2rem; margin-top: 1rem;'>
            Исследуйте различные типы BERT эмбеддингов для вашего текста.
            Просто введите текст ниже и нажмите кнопку анализа.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Секция ввода с улучшенным стилем
with st.container():
    # Поле для ввода текста
    text_input = st.text_area(
        "✍️ Введите текст для анализа:",
        "Привет мир!",
        help="Введите любой текст для анализа его эмбеддингов"
    )

    # Кнопка анализа
    if st.button("Анализировать текст"):
        if text_input.strip():
            # Получение токенизации и эмбеддингов
            tokenization = st.session_state.bert_extractor.get_tokenization(text_input)
            embeddings = st.session_state.bert_extractor.get_embeddings(text_input)

            # Отображение результатов токенизации
            st.subheader("Результаты токенизации")
            st.write("Токены:", embeddings['tokens'])

            # Создание вкладок для разных визуализаций
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "Эмбеддинги токенов",
                "Позиционные эмбеддинги",
                "Эмбеддинги типов токенов",
                "CLS вектор",
                "Карта внимания"
            ])

            # Вкладка с эмбеддингами токенов
            with tab1:
                for idx, token in enumerate(embeddings['tokens']):
                    st.subheader(f"Токен: {token}")
                    st.plotly_chart(
                        create_vector_plot(
                            embeddings['token_embeddings'][idx],
                            f"Вектор эмбеддинга для токена '{token}'"
                        ),
                        use_container_width=True,
                        key=f"token_emb_{idx}"
                    )

            # Вкладка с позиционными эмбеддингами
            with tab2:
                for idx, token in enumerate(embeddings['tokens']):
                    st.subheader(f"Позиция {idx} (токен: {token})")
                    st.plotly_chart(
                        create_vector_plot(
                            embeddings['position_embeddings'][idx],
                            f"Позиционный эмбеддинг для позиции {idx}"
                        ),
                        use_container_width=True,
                        key=f"pos_emb_{idx}"
                    )

            # Вкладка с эмбеддингами типов токенов
            with tab3:
                for idx, token in enumerate(embeddings['tokens']):
                    st.subheader(f"Токен: {token}")
                    st.plotly_chart(
                        create_vector_plot(
                            embeddings['token_type_embeddings'][idx],
                            f"Эмбеддинг типа токена для '{token}'"
                        ),
                        use_container_width=True,
                        key=f"type_emb_{idx}"
                    )

            # Вкладка с CLS вектором
            with tab4:
                st.subheader("CLS вектор")
                st.plotly_chart(
                    create_vector_plot(
                        embeddings['cls_vector'],
                        "Значения CLS вектора"
                    ),
                    use_container_width=True,
                    key="cls_vector"
                )
                
            # Вкладка с картой внимания
            with tab5:
                st.subheader("Визуализация внимания между токенами")
                st.plotly_chart(
                    create_attention_heatmap(
                        embeddings['attention_weights'],
                        embeddings['tokens']
                    ),
                    use_container_width=True
                )
        else:
            st.error("Пожалуйста, введите текст для анализа.")

# Добавление информационной секции внизу
st.markdown("""
---
### О BERT эмбеддингах

- **Эмбеддинги токенов**: Контекстные представления каждого токена во входном тексте
- **Позиционные эмбеддинги**: Кодируют позицию каждого токена в последовательности
- **Эмбеддинги типов токенов**: Используются для различения разных сегментов во входных данных
- **CLS вектор**: Специальный классификационный токен, представляющий всю последовательность
""")
