def choose_techniques(situation: dict) -> list[str]:
    if not isinstance(situation, dict):
        raise ValueError("Невідома мета: None")
        
    goal = situation.get('goal', None)
    valid_goals = {'order', 'sprint', 'release_date', 'schedule', 'agreement'}
    if goal not in valid_goals:
        raise ValueError(f"Невідома мета: {goal}")
        
    items = situation.get('items', None)
    if isinstance(items, bool) or not isinstance(items, int) or items < 1:
        raise ValueError("Некоректна кількість пунктів")
        
    history_sprints = situation.get('history_sprints', 0)
    has_dependencies = situation.get('has_dependencies', False)
    wants_probability = situation.get('wants_probability', False)
    disputed = situation.get('disputed', False)
    largest = situation.get('largest', None)
    
    result = []
    if goal == 'agreement':
        result = ["Дорожня карта"]
        if history_sprints >= 3:
            result.append("Швидкість із діапазоном")
    elif goal == 'schedule':
        result = ["Три оцінки (PERT)"]
        if has_dependencies:
            result.append("Критичний шлях")
    elif goal == 'release_date':
        if history_sprints < 3:
            result = ["Спершу накопичити швидкість (щонайменше 3 спринти)"]
        else:
            result = ["Швидкість із діапазоном"]
            if wants_probability:
                result.append("Метод Монте-Карло")
    elif goal == 'order':
        if items > 20:
            result = ["Розміри «футболок» (S, M, L)"]
            if disputed:
                result.append("Planning Poker для спірних пунктів")
        else:
            result = ["Planning Poker"]
    elif goal == 'sprint':
        result = ["Planning Poker"]
        if largest is not None and largest >= 13:
            result.append("Розбити історії завбільшки 13 і більше")
            
    return result