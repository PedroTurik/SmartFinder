a = [state]

def gerar_novos_states(states):
    return

seen = set()


while True:
    cur = a.pop()
    if cur.isTerminou():
        print(cur)
        break 
    s = gerar_novos_states(state)
    for st in s:
        if st in seen:
            continue

        else:
            seen.add(st)    
            a.append(st)