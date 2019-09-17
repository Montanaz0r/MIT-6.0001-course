#ps1c.py - solution to a 'House Hunting' Part C from MIT_60001 course.

def bisect_search(the_range, annual_salary):
    '''initialize bisect search; parameters:
    the_range - decimal number representing % of salary we are willing to consider, while searching for optimal
    rate of savings, annual_salary - salary level.'''
    step_counter = 0
    def bisect_search_helper(low, high, annual_salary, step_counter):
        '''Given low and high points, calculation the middle one and comparing result with conditions,
        step counter is initialized as 0, with each recursion counter is being incremented by 1'''
        step_counter += 1
        print(f'Step number: {step_counter}')
        middle = (low + high)//2
        if low == middle:   # condition that is checking if the program did not exhaust range of possibilities.
            print('It is not possible to pay the down payment in three years!')
            return None
        middle_as_decimal = middle/10000
        print(f'low: {low}, high: {high}, middle as decimal: {middle_as_decimal}')
        result = house_hunting(annual_salary=annual_salary, portion_down_payment=0.25, r=0.04, semi_annual_raise=0.07,
                      total_cost=1000000, m_time_limit=36, portion_saved=middle_as_decimal)
        if result == 36:   # prints portions of savings that met all the conditions.
            print(f'You reached your goal by saving {middle_as_decimal} of your salary per month.')
        elif result == 0:   # checking level deeper, since with previous try we exceeded time condition.
            bisect_search_helper(middle, high, annual_salary, step_counter)
        else:  # checking level deeper, since with previous try we reached goal with less time than we are allowed to use.
            bisect_search_helper(low, middle, annual_salary, step_counter)
    if the_range == 0:
        return False
    else:
        return bisect_search_helper(0, the_range, annual_salary, step_counter)


def house_hunting(annual_salary, portion_down_payment, r, semi_annual_raise, total_cost, m_time_limit,
                  portion_saved, current_savings = 0):
    '''given annual salary, portion down payment, r as annual rate, semi annual raise, total cost, function will
    count number of months needed to reach the goal considering portion saved, which is a variable that will
    be declared by function bisect_search_helper. total cost is set up to 1 000 000 and m time limit is set up to 36
    in respect of task constraints.'''
    monthly_salary = annual_salary / 12
    annual_raise_counter = 0
    months_counter = 0
    goal = total_cost * portion_down_payment
    while current_savings < goal:
        if months_counter >= m_time_limit:   # when functions exceeded the time limit, there is no point in checking further.
            print('You have exceeded given time, while you have not reached your goal!')
            months_counter = 0
            break
        if annual_raise_counter == 6:
            monthly_salary += monthly_salary * semi_annual_raise
            annual_raise_counter = 1
        else:
            annual_raise_counter += 1
        current_savings += current_savings * r/12
        current_savings += monthly_salary * portion_saved
        months_counter += 1
    print(f'Number of months: {months_counter}')
    return months_counter


print('Enter your annual salary: ')
annual_salary = int(input())
the_range = 10000
bisect_search(the_range, annual_salary)