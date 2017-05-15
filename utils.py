from _ast import List


def build_menu(buttons: List, n_cols: int):  # builds an inline menu which has n_cols columns
    menu = [buttons[i:i+n_cols] for i in range(0, len(buttons), n_cols)]
    return menu
