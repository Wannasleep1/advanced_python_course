from datetime import *

from application.salary import *
from application.db.people import *


if __name__ == '__main__':
    print('Сегодня', date.today().strftime('%d.%m.%Y'))
    get_employees()
    calculate_salary()