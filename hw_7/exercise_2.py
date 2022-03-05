from exercise_1 import Stack


def is_balanced(hooks_str: str) -> bool:
    stack = Stack()
    left_hooks = "([{"
    for hook in hooks_str:
        if hook in left_hooks:
            stack.push(hook)
        elif not stack.isEmpty():
            last_elem = stack.pop()
            if (last_elem == "(" and hook != ")" or
                    last_elem == "{" and hook != "}" or
                    last_elem == "[" and hook != "]"):
                return False
        else:  # Stack is empty and first hook in the string is closing one.
            return False
    return True


if __name__ == '__main__':
    test_dict = {"(((([{}]))))": True, "[([])((([[[]]])))]{()}": True,
                 "{{[()]}}": True, "}{}": False, "{{[(])]}}": False,
                 "[[{())}]": False}

    for hooks, balanced in test_dict.items():
        assert is_balanced(hooks) == balanced
    print("Ok.")
