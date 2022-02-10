import re
import pandas as pd
from pandas.core.series import Series


def process_row(row: Series) -> Series:
    words_in_lastname = re.findall(r"\w[^\s]+", row[0])
    if len(words_in_lastname) == 3:
        row[0] = words_in_lastname[0]
        row[1] = words_in_lastname[1]
        row[2] = words_in_lastname[2]
    elif len(words_in_lastname) == 2:
        row[0] = words_in_lastname[0]
        row[1] = words_in_lastname[1]
    elif type(row[1]) == str:
        words_in_firstname = re.findall(r"\w[^\s]+", row[1])
        if len(words_in_firstname) == 2:
            row[1] = words_in_firstname[0]
            row[2] = words_in_firstname[1]

    if type(row[5]) == str:
        phone_num_pattern = (
            r"^([+]?[7]{1}|[8]{1})\s*\(?([1-9]{1}\d{2}){1}\)?-?\s*(\d{3}){1}-?\s*(\d{2}){1}-?\s*(\d{2}){1}"
            r"\s*(\(?(доб.\s*\d{4})\)?)?$"
        )
        addition = re.search(r"доб.\s*\d{4}", row[5])
        row[5] = re.sub(phone_num_pattern, r"+7(\2)-\3-\4-\5", row[5])
        row[5] += " (" + addition.group(0) + ")" if addition else ""

    return row


if __name__ == "__main__":
    contacts_data = pd.read_csv("phonebook_raw.csv", sep=",", on_bad_lines='skip')
    processed_data = contacts_data.apply(process_row, axis=1).groupby(by=["lastname", "firstname"]).first()
    processed_data.to_csv("phonebook.csv", encoding="utf-8")
