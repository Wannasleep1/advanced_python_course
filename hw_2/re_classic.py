from pprint import pprint
import csv
import re


def convert_phone_numbers(lst):
    phone_num_pattern = (
        r"^([+]?[7]{1}|[8]{1})\s*\(?([1-9]{1}\d{2}){1}\)?-?\s*(\d{3}){1}-?\s*(\d{2}){1}-?\s*(\d{2}){1}"
        r"\s*(\(?(доб.\s*\d{4})\)?)?$"
    )
    addition = re.search(r"доб.\s*\d{4}", lst[5])
    lst[5] = re.sub(phone_num_pattern, r"+7(\2)-\3-\4-\5", lst[5])
    lst[5] += " (" + addition.group(0) + ")" if addition else ""


def convert_fio(lst):
    words_in_lastname = re.findall(r"\w[^\s]+", lst[0])
    if len(words_in_lastname) == 3:
        lst[0] = words_in_lastname[0]
        lst[1] = words_in_lastname[1]
        lst[2] = words_in_lastname[2]
    elif len(words_in_lastname) == 2:
        lst[0] = words_in_lastname[0]
        lst[1] = words_in_lastname[1]
    elif type(lst[1]) == str:
        words_in_firstname = re.findall(r"\w[^\s]+", lst[1])
        if len(words_in_firstname) == 2:
            lst[1] = words_in_firstname[0]
            lst[2] = words_in_firstname[1]


def process_lst(lst):
    convert_fio(lst)
    convert_phone_numbers(lst)


# Получилось громоздко, но смысла декомпозировать вроде как не было
def drop_duplicates():
    ready_lst = [contacts_list[0]]
    # Перебираем контакты в искомом списке
    for lst in contacts_list[1:]:
        # Перебираем контакты в формируемом списке
        for elem in ready_lst:
            # Проверяем наличие дубликата по совпадению имени и фамилии
            if (lst[0] == elem[0]) and (lst[1] == elem[1]):
                # Перебираем данные контакта для заполнения пустых значений
                for i in range(2, len(lst)):
                    # Один из списков в искомом файле длиннее остальных, поэтому предотвращаем
                    # появление ошибки выхода за границы списка.
                    try:
                        if not elem[i] and lst[i]:
                            elem[i] = lst[i]
                    except IndexError:
                        break
                break
        else:
            ready_lst.append(lst)

    return ready_lst


def main():
    for lst in contacts_list:
        process_lst(lst)

    return drop_duplicates()


if __name__ == "__main__":
    with open("phonebook_raw.csv", encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    # Выполняем преобразования непосредственно в прочитанном списке.
    processed_data = main()

    with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
        data_writer = csv.writer(f, delimiter=',')
        data_writer.writerows(processed_data)
