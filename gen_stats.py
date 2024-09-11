from math import exp

base_evolution_cost = 200
a = 1.8
b = base_evolution_cost / exp(a*1)
evolution_costs = [int(100*(b*exp(a*e)//100)) for e in [1, 2, 3]]
print(f'"evolution_cost": {evolution_costs}')

minion_stats = {
    f'minion{i}': {} for i in range(1, 13)
}

health_ratios = [23.0, 33.0, 56.0] # Minions 1, 2, 3
damage_ratios = [ 8.1, 11.1, 17.1] # Minions 1, 2, 3

max_health_bases = [30, 120, 450, 1500]
cost_bases = [2*i for i in [3, 35, 500, 6500]]
damage_bases = [int(h) + 1 for h in max_health_bases]
print(f'damage_bases: {damage_bases}')

for i in range(1, 13):
    evolution = (i-1) // 3 # {0, 1, 2, 3}
    stage = (i-1) % 3 # {0, 1, 2}

    base_health = max_health_bases[evolution] / health_ratios[0]
    if stage == 0:
        cost = cost_bases[evolution]
        max_health = base_health * health_ratios[stage]
        damage     = base_health * damage_ratios[stage]
    elif stage == 1:
        cost *= 1.7
        max_health = base_health * health_ratios[stage]
        damage     = base_health * damage_ratios[stage]
    else:
        cost *= 4
        max_health = base_health * health_ratios[stage]
        damage     = base_health * damage_ratios[stage]

    minion_stats[f'minion{i}']['max_health'] = int(max_health)
    minion_stats[f'minion{i}']['damage']     = int(damage)
    minion_stats[f'minion{i}']['cost']       = int(cost)
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

last_stat = 'cost'

for name, stats in minion_stats.items():
    space = ' ' * (int(name.lstrip('minion')) <= 9)
    print(f'\"{name}\"{space}: {{', end='')
    for key, value in stats.items():
        end = ', ' * (key != last_stat)
        print(f'"{key}": {str(value).rjust(6)}{end}', end='')
    print('}')