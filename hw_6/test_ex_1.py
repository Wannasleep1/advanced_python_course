from copy import deepcopy

import pytest as pt

import app


class TestApp:

    @pt.mark.parametrize("test_input,expected", [("0", False), (1, False), ('10006', True),
                                                 ('-10006', False), ('10006.0', False)])
    def test_check_document_existance(self, test_input, expected):
        assert app.check_document_existance(test_input) == expected

    @pt.mark.parametrize("test_input,expected", [("12345678", None), ("11-2", "Геннадий Покемонов"),
                                                 ("5455 028765", None), (0, None)])
    def test_get_doc_owner_name(self, monkeypatch, test_input, expected):
        monkeypatch.setattr("builtins.input", lambda _: test_input, raising=True)
        result = app.get_doc_owner_name()
        assert result == expected

    def test_get_all_owners_names(self):
        assert app.get_all_doc_owners_names() == {"Василий Гупкин", "Геннадий Покемонов", "Аристарх Павлов"}

    @staticmethod
    @pt.fixture()
    def directories_setup():
        return deepcopy(app.directories)

    @staticmethod
    @pt.fixture()
    def documents_setup():
        return deepcopy(app.documents)

    @pt.mark.parametrize("test_input,expected", [("100500", ("100500", True)), ("3", ("3", False))])
    def test_add_new_shelf(self, monkeypatch, test_input, expected, directories_setup):
        monkeypatch.setattr("app.directories", directories_setup)
        assert app.add_new_shelf(test_input) == expected

    @pt.mark.parametrize("test_input,expected", [("lol kek cheburek", None), ("11-2", ("11-2", True))])
    def test_delete_doc(self, monkeypatch, test_input, expected, documents_setup, directories_setup):
        monkeypatch.setattr("app.documents", documents_setup, raising=True)
        monkeypatch.setattr("builtins.input", lambda _: test_input, raising=True)
        monkeypatch.setattr("app.directories", directories_setup, raising=True)
        assert app.delete_doc() == expected

    @staticmethod
    def helper_func():
        x = -1
        user_command = input('Введите команду - ')
        if user_command == 'p':
            x = app.get_doc_owner_name()
        elif user_command == 'ap':
            x = app.get_all_doc_owners_names()
        elif user_command == 'l':
            x = app.show_all_docs_info()
        elif user_command == 's':
            x = app.get_doc_shelf()
        elif user_command == 'a':
            x = app.add_new_doc()
        elif user_command == 'd':
            x = app.delete_doc()
        elif user_command == 'm':
            x = app.move_doc_to_shelf()
        elif user_command == 'as':
            x = app.add_new_shelf()
        return x

    @pt.mark.parametrize("test_input,expected", [("p", "app.get_doc_owner_name"), ("l", "app.show_all_docs_info"),
                                                 ("ap", "app.get_all_doc_owners_names"), ("s", "app.get_doc_shelf"),
                                                 ("a", "app.add_new_doc"), ("d", "app.delete_doc"),
                                                 ("m", "app.move_doc_to_shelf"), ("as", "app.add_new_shelf")])
    def test_secretary_program_start(self, monkeypatch, test_input, expected):
        def _set():
            return 1

        monkeypatch.setattr("builtins.input", lambda _: test_input, raising=True)
        monkeypatch.setattr(expected, _set, raising=True)
        assert self.helper_func() == 1
