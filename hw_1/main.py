from datetime import date

from application.salary import calculate_salary
from application.db.people import get_employees


if __name__ == '__main__':
    print('Сегодня', date.today().strftime('%d.%m.%Y'))
    get_employees()
    calculate_salary()