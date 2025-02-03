
def get_styles():
    """
    Возвращает словарь с пользовательскими стилями для приложения.
    Включает стили для основных компонентов интерфейса:
    - Главный контейнер
    - Заголовок
    - Контейнер для ввода
    - Текстовая область
    - Кнопки
    - Вкладки
    
    Returns:
        dict: Словарь стилей CSS
    """
    return {
        'main_container': {
            'max-width': '1200px',
            'margin': '0 auto',
            'padding': '2rem',
        },
        'title': {
            # Градиентный фон для заголовка
            'background': 'linear-gradient(45deg, #2193b0, #6dd5ed)',
            'padding': '2rem',
            'border-radius': '15px',
            'color': 'white',
            'text-align': 'center',
            'margin-bottom': '2rem',
            'box-shadow': '0 4px 6px rgba(0,0,0,0.1)',
        },
        'input_container': {
            # Стили для контейнера ввода текста
            'background-color': '#ffffff',
            'padding': '2rem',
            'border-radius': '15px',
            'margin-bottom': '2rem',
            'box-shadow': '0 2px 12px rgba(0,0,0,0.1)',
            'border': '1px solid #e0e0e0',
        },
        'text_area': {
            # Стили для текстового поля
            'border': '2px solid #e0e0e0',
            'border-radius': '10px',
            'padding': '1rem',
            'font-size': '16px',
        },
        'button': {
            # Стили для кнопок с эффектом при наведении
            'background': 'linear-gradient(45deg, #2193b0, #6dd5ed)',
            'color': 'white',
            'padding': '0.8rem 1.5rem',
            'border-radius': '10px',
            'border': 'none',
            'box-shadow': '0 2px 4px rgba(0,0,0,0.1)',
            'transition': 'transform 0.2s ease',
            'hover': {
                'transform': 'translateY(-2px)',
                'box-shadow': '0 4px 8px rgba(0,0,0,0.2)',
            }
        },
        'tabs': {
            # Стили для вкладок
            'background-color': '#ffffff',
            'border-radius': '10px',
            'padding': '1rem',
            'margin-top': '2rem',
            'box-shadow': '0 2px 12px rgba(0,0,0,0.1)',
        }
    }
