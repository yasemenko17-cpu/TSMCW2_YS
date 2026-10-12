import re

def check_ready(story: dict) -> dict:
    if not isinstance(story, dict):
        raise ValueError("Некоректна історія")
    
    problems = []
    
    # 1. Шаблон: Як <роль>, я хочу <дія>, щоб <мета>
    text = story.get('text')
    pattern = r"^Як\s+(\S.*?),\s+я\s+хочу\s+(\S.*?),\s+щоб\s+(\S.*?)$"
    if not isinstance(text, str) or not re.match(pattern, text.strip()):
        problems.append("немає шаблону «Як..., я хочу..., щоб...»")
        
    # 2. Критерії
    criteria = story.get('criteria')
    if not isinstance(criteria, list):
        count = 0
    else:
        count = sum(1 for c in criteria if isinstance(c, str) and c.strip())
    if count < 3:
        problems.append(f"критеріїв прийняття менше трьох: {count}")
        
    # 3. Оцінка
    points = story.get('points', None)
    fibonacci = (1, 2, 3, 5, 8, 13, 21)
    if points is None or 'points' not in story:
        problems.append("немає оцінки")
    elif isinstance(points, bool) or not isinstance(points, int) or points not in fibonacci:
        problems.append(f"оцінка {points} не зі шкали Фібоначчі")
    else:
        if points in (13, 21):
            problems.append(f"історія завелика ({points}): розбийте її")
            
    # 4. Залежності
    deps = story.get('dependencies')
    if deps is None:
        deps = []
    if isinstance(deps, list):
        for dep in deps:
            if isinstance(dep, dict):
                if dep.get('resolved') is not True:
                    problems.append(f"залежність {dep.get('name')} не вирішена")
                    
    ready = len(problems) == 0
    verdict = "Готова до планування" if ready else "Повернути власнику продукту"
    
    return {
        'ready': ready,
        'problems': problems,
        'verdict': verdict
    }