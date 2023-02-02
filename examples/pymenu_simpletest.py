# SPDX-FileCopyrightText: 2023 Petr Vavrin <pvavrin@gmail.com>
# SPDX-FileCopyrightText: Copyright (c) 2023 Petr Vavrin
#
# SPDX-License-Identifier: MIT

# pylint: disable=unused-argument, wrong-import-position
import sys

sys.path.insert(0, "..")

from peterbay_pymenu import MenuCore, MenuItem

# -- menu rendering -------------------------------------------------


def print_menu_line(line, delimiter=False):
    if delimiter:
        print("+{0: <50}+".format("-" * 50))
    else:
        print("|{0: <50}|".format(line))


def render_pre(is_main_menu):
    print("")
    print_menu_line(None, True)


def render_post(is_main_menu):
    if is_main_menu:
        pass
    else:
        print_menu_line(" [ 0] Back")
    print_menu_line(None, True)


def render_menu_title(item, value):
    if item.uid == 0:
        print_menu_line(" MAIN MENU")
    else:
        label = [item.label]
        while item.parent:
            item = item.parent
            if item.uid != 0:
                label.insert(0, item.label)

        if value:
            print_menu_line(" {0}, value: {1}".format(" / ".join(label), value))
        else:
            print_menu_line(" {0}".format(" / ".join(label)))
    print_menu_line(None, True)


def render_menu_item(item, render_index, is_active):
    item_row = []

    # if is_active:
    #     item_row.append("> ")
    # else:
    #     item_row.append("  ")

    hotkey = ""
    if item.hotkey:
        hotkey = str(item.hotkey)

    item_row.append(" [{0: >2}] {1: <20} ".format(hotkey, item.label))

    if item.disabled:
        item_row.append(" (disabled)")

    if item.value_fn:
        value = item.value_fn(item)
        item_row.append("val: %s" % str(value))

    if item.child or callable(item.dynamic_fn):
        item_row.append(" ->")

    print_menu_line("".join(item_row))


# --- functions called from menu ------------------------------------

global_data = {"volume": 50}


def get_value(item):
    if item.data == "temp":
        return "451 °F"

    return item.data


def show_about(item):
    print("Example - Petr Vavrin (c) 2023")


def exit_menu(item):
    sys.exit(0)


def print_message(item):
    print("*" * 30)
    print(item.data)
    print("*" * 30)


def dynamic_menu(menux, parent):
    menu_a = MenuItem(
        label="item a", hotkey="1", enter_fn=print_message, data="Message for item a"
    )
    menu_b = MenuItem(
        label="item b", hotkey="2", enter_fn=print_message, data="Message for item b"
    )
    menu_c = MenuItem(
        label="item c", hotkey="3", enter_fn=print_message, data="Message for item c"
    )

    menux.add_item(menu_a, parent)
    menux.add_item(menu_b, parent)
    menux.add_item(menu_c, parent)


def get_volume(item):
    return global_data["volume"]


def increase_volume(item):
    global_data["volume"] += 1
    print("increase volume: %d" % global_data["volume"])


def decrease_volume(item):
    global_data["volume"] -= 1
    print("decrease volume: %d" % global_data["volume"])


# --- menu definition -----------------------------------------------

menu = MenuCore()

menu_i1 = MenuItem(label="Item 1", hotkey="1")
menu.add_item(menu_i1)

menu_i1_s1 = MenuItem(label="Item 1 - about", hotkey="1", enter_fn=show_about)
menu.add_item(menu_i1_s1, menu_i1)

menu_i1_s2 = MenuItem(
    label="Item 1 - get value", hotkey="2", data="temp", value_fn=get_value
)
menu.add_item(menu_i1_s2, menu_i1)

menu_i1_s3 = MenuItem(label="Item 1 - disabled", hotkey="3")
menu_i1_s3.disabled = True
menu.add_item(menu_i1_s3, menu_i1)


menu_i2 = MenuItem(label="Item 2", hotkey="2")
menu.add_item(menu_i2)

menu_i2_s1 = MenuItem(label="Item 2 - dynamic", hotkey="1", dynamic_fn=dynamic_menu)
menu.add_item(menu_i2_s1, menu_i2)


menu_i3 = MenuItem(label="Volume", hotkey="3", value_fn=get_volume)
menu.add_item(menu_i3)

menu_i3_s1 = MenuItem(label="Increase volume", hotkey="1", enter_fn=increase_volume)
menu.add_item(menu_i3_s1, menu_i3)

menu_i3_s2 = MenuItem(label="Decrease volume", hotkey="2", enter_fn=decrease_volume)
menu.add_item(menu_i3_s2, menu_i3)


menu_i9 = MenuItem(label="Exit", hotkey="9", enter_fn=exit_menu)
menu.add_item(menu_i9)

menu.init(menu_i1)

menu.circular = False
menu.render_title_fn = render_menu_title
menu.render_item_fn = render_menu_item
menu.pre_render_fn = render_pre
menu.post_render_fn = render_post

menu.render()

while True:
    try:
        print("User input: ", end="")
        user_input = input()

        if user_input == "0":
            menu.action(menu.ACTION_BACK)

        elif user_input == "reset":
            menu.reset()
            menu.render()

        elif user_input == "menu":
            menu.render()

        else:
            menu.action_hotkey(user_input)

    except KeyboardInterrupt:
        break
