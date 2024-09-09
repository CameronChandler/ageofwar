minion_stats = {
    f'minion{i}': {} for i in range(1, 13)
}

for i in range(1, 13):
    evolution = 1 + (i-1) // 3 # {1, 2, 3, 4}
    stage = 1 + (i-1) % 3 # {1, 2, 3}
    minion_stats[f'minion{i}']['max_health'] = 5
# "minion1" : {"max_health":    5, "damage":  1, "cost":   3, "reward_xp":   1}
# "minion2" : {"max_health":   15, "damage":  4, "cost":  10, "reward_xp":   5}
# "minion3" : {"max_health":   20, "damage":  5, "cost":  50, "reward_xp":  10}
# "minion4" : {"max_health":   50, "damage": 19, "cost": 150, "reward_xp": 150}
# "minion5" : {"max_health":   50, "damage": 19, "cost": 100, "reward_xp":  25}
# "minion6" : {"max_health":   80, "damage":  7, "cost":  25, "reward_xp":  50}
# "minion7" : {"max_health":  120, "damage": 10, "cost":  30, "reward_xp":  80}
# "minion8" : {"max_health":  150, "damage": 12, "cost":  50, "reward_xp": 120}
# "minion9" : {"max_health":  250, "damage": 20, "cost":  80, "reward_xp": 180}
# "minion10": {"max_health":  300, "damage": 30, "cost": 100, "reward_xp": 250}
# "minion11": {"max_health":  500, "damage": 50, "cost": 150, "reward_xp": 350}
# "minion12": {"max_health": 1000, "damage": 80, "cost": 250, "reward_xp": 500}

last_stat = 'max_health'

for name, stats in minion_stats.items():
    space = ' ' * (int(name.lstrip('minion')) <= 9)
    print(f'\"{name}\"{space}: {{', end='')
    for key, value in stats.items():
        end = ', ' * (key != last_stat)
        print(f'"{key}": {str(value).rjust(6)}{end}', end='')
    print('}')
