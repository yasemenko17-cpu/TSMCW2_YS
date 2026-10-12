def decide_change(cr: dict, state: dict) -> dict:
    if not isinstance(cr, dict):
        raise ValueError("Некоректний запит: ?")
    cr_id = cr.get('id', '?')
    
    cr_type = cr.get('type')
    valid_types = {'problem', 'extension', 'external', 'standards', 'management'}
    if cr_type not in valid_types:
        raise ValueError(f"Некоректний запит: {cr_id}")
        
    impact_days = cr.get('impact_days')
    if isinstance(impact_days, bool) or not isinstance(impact_days, int) or impact_days < 0:
        raise ValueError(f"Некоректний запит: {cr_id}")
        
    value = cr.get('value')
    if isinstance(value, bool) or not isinstance(value, int) or not (1 <= value <= 10):
        raise ValueError(f"Некоректний запит: {cr_id}")
        
    if not isinstance(state, dict):
        raise ValueError("Некоректний стан")
    reserve_days = state.get('reserve_days')
    if isinstance(reserve_days, bool) or not isinstance(reserve_days, int) or reserve_days < 0:
        raise ValueError("Некоректний стан")
        
    goal_at_risk = state.get('goal_at_risk', False)
    emergency = cr.get('emergency', False)
    mandatory = cr.get('mandatory', False) or cr_type in ('standards', 'management')
    
    left = max(0, reserve_days - impact_days)
    exceeds_reserve = impact_days > reserve_days
    
    if emergency:
        decision = "Затвердити"
        reserve_after = left
        rebaseline = exceeds_reserve
        next_step = "Ретроспективний розгляд радою"
    elif mandatory:
        decision = "Затвердити"
        reserve_after = left
        rebaseline = exceeds_reserve
        next_step = "Оновити базову лінію" if exceeds_reserve else "Виконати в межах резерву"
    elif goal_at_risk:
        decision = "Відкласти"
        reserve_after = reserve_days
        rebaseline = False
        next_step = "Розглянути на наступному плануванні"
    elif not exceeds_reserve:
        if value >= 5:
            decision = "Затвердити"
            reserve_after = left
            rebaseline = False
            next_step = "Виконати в межах резерву"
        else:
            decision = "Відкласти"
            reserve_after = reserve_days
            rebaseline = False
            next_step = "Повернути в беклог"
    else:
        if value >= 8:
            decision = "Відкласти"
            reserve_after = reserve_days
            rebaseline = False
            next_step = "Узгодити з замовником нову базову лінію"
        else:
            decision = "Відхилити"
            reserve_after = reserve_days
            rebaseline = False
            next_step = "Повідомити замовника"
            
    return {
        'id': cr_id,
        'decision': decision,
        'reserve_after': reserve_after,
        'rebaseline': rebaseline,
        'next_step': next_step
    }