def check_bets(bets: list[dict], week: int) -> dict:
    if not isinstance(bets, list) or len(bets) == 0:
        raise ValueError("Немає ставок")
    if isinstance(week, bool) or not isinstance(week, int) or week < 1:
        raise ValueError("Некоректний тиждень")
        
    seen_names = set()
    rows = []
    breaker = []
    overspend_weeks = 0
    
    for bet in bets:
        name = bet.get('name') if isinstance(bet, dict) else None
        name_str = name if isinstance(name, str) and name else "?"
        
        if not isinstance(bet, dict) or not isinstance(name, str) or not name:
            raise ValueError(f"Некоректна ставка: {name_str}")
            
        appetite = bet.get('appetite')
        if isinstance(appetite, bool) or not isinstance(appetite, int) or not (1 <= appetite <= 6):
            raise ValueError(f"Некоректна ставка: {name_str}")
            
        started = bet.get('started')
        if isinstance(started, bool) or not isinstance(started, int) or not (1 <= started <= week):
            raise ValueError(f"Некоректна ставка: {name_str}")
            
        finished = bet.get('finished', None)
        if finished is not None:
            if isinstance(finished, bool) or not isinstance(finished, int) or not (started <= finished <= week):
                raise ValueError(f"Некоректна ставка: {name_str}")
                
        if name in seen_names:
            raise ValueError(f"Дубль ставки: {name}")
        seen_names.add(name)
        
        spent = (finished if finished is not None else week) - started + 1
        left = max(0, appetite - spent)
        
        if finished is not None:
            status = "завершено вчасно" if spent <= appetite else "завершено із запізненням"
        else:
            status = "триває" if spent <= appetite else "запобіжник"
                
        if status == "запобіжник":
            breaker.append(name)
            
        overspend_weeks += max(0, spent - appetite)
        rows.append((name, status, spent, left))
        
    next_step = "Повернути на шейпінг: " + ", ".join(breaker) if breaker else "Продовжувати цикл"
    
    return {
        'rows': rows,
        'breaker': breaker,
        'overspend_weeks': overspend_weeks,
        'next_step': next_step
    }