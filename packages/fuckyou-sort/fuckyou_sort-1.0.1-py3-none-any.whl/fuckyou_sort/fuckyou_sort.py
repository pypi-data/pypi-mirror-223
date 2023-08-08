def sort(array):

    n = len(array)

    for i in range(n):

        array[i] = i


    return array

def step(array):

    n = len(array)

    step_count = 0
    
    for i in range(n):

        if array[i] == step_count:
            step_count += 1

        else:
            break

    if n > step_count:
        array[step_count] = step_count
        
    return array