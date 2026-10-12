def pyramid_report(tests: list[dict], target: tuple = (70, 20, 10)) -> dict:
    if not isinstance(tests, list) or len(tests) == 0:
        raise ValueError("Немає тестів")
        
    levels = []
    s = m = l = 0
    
    for test in tests:
        if not isinstance(test, dict):
            raise ValueError("Некоректний тест: ?")
        name = test.get('name')
        name_str = name if isinstance(name, str) else "?"
        
        seconds = test.get('seconds')
        if isinstance(seconds, bool) or not isinstance(seconds, (int, float)) or seconds < 0:
            raise ValueError(f"Некоректний тест: {name_str}")
            
        ui = test.get('ui', False)
        external_network = test.get('external_network', False)
        localhost = test.get('localhost', False)
        database = test.get('database', False)
        filesystem = test.get('filesystem', False)
        
        if ui or external_network or seconds > 300:
            level = "наскрізний"
            l += 1
        elif localhost or database or filesystem or seconds > 60:
            level = "інтеграційний"
            m += 1
        else:
            level = "модульний"
            s += 1
            
        levels.append((name_str, level))
        
    total = s + m + l
    if total > 0:
        s_share = round(s * 100 / total, 1)
        m_share = round(m * 100 / total, 1)
        l_share = round(l * 100 / total, 1)
    else:
        s_share = m_share = l_share = 0.0
        
    shares = (s_share, m_share, l_share)
    counts = (s, m, l)
    
    if l > m and l > s:
        shape = "ріжок морозива"
    elif m > s and m >= l:
        shape = "пісочний годинник"
    elif s >= m:
        shape = "піраміда"
    else:
        shape = "ромб"
        
    far_from_target = []
    level_names = ["модульний", "інтеграційний", "наскрізний"]
    for i, share_val in enumerate(shares):
        if abs(share_val - target[i]) > 10:
            far_from_target.append(level_names[i])
            
    return {
        'levels': levels,
        'counts': counts,
        'shares': shares,
        'shape': shape,
        'far_from_target': far_from_target
    }