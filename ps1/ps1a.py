#ps1a.py - solution to a 'House Hunting' Part A from MIT_60001 course.

def house_hunting(portion_down_payment, r, current_savings = 0):
    '''portion_down_payment - portion of the cost needed for a down payment,
    r - annual rate of savings, current_savings - by default are 0, you can explicitly change them by calling
    function with additional parameter'''
    print('Enter  your annual salary: ')
    annual_salary = int(input())
    print('Enter the percent of your salary to save, as a decimal: ')
    portion_saved = float(input())
    print('Enter the cost of your dream home: ')
    total_cost = int(input())
    monthly_salary = annual_salary / 12
    months_counter = 0
    goal = total_cost * portion_down_payment
    while current_savings < goal:
       current_savings += current_savings * r/12
       current_savings += monthly_salary * portion_saved
       months_counter += 1
    print(f'Number of months: {months_counter}')
    return months_counter

portion_down_payment = 0.25
current_savings = 0
r = 0.04
house_hunting(portion_down_payment, r)