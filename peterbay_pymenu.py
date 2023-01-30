# SPDX-FileCopyrightText: 2023 Petr Vavrin <pvavrin@gmail.com>
# SPDX-FileCopyrightText: Copyright (c) 2023 Petr Vavrin
#
# SPDX-License-Identifier: MIT
"""
`peterbay_pymenu`
================================================================================

Universal python library for creating menus for console and GUI applications.


* Author(s): Petr Vavrin

Implementation Notes
--------------------

It's universal without any dependencies.

"""

# imports

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/peterbay/Peterbay_CircuitPython_PyMenu.git"


class MenuItem:
    parent = None
    prev = None
    next = None
    child = None
    uid = None

    label = ""
    hotkey = None
    data = None
    disabled = None
    enter_cb = None
    leave_cb = None
    value_cb = None
    dynamic_cb = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def drop_reference(self):
        self.prev = None
        self.next = None
        self.child = None


class MenuCore:
    __item_counter = 1
    __root_item = None
    __main_item = None
    __active_item = None

    ACTION_PREV = 1
    ACTION_NEXT = 2
    ACTION_BACK = 3
    ACTION_ENTER = 4

    auto_render = True
    show_previous_items = True
    circular = False
    menu_exit = None
    pre_render = None
    post_render = None
    render_scroll_up = None
    render_scroll_down = None
    render_title = None
    render_item = None
    rows_limit = 255

    def __init__(self):
        self.__root_item = MenuItem()
        self.__root_item.uid = 0

    def add_item(self, menu_item, parent=None):
        self.check_item(menu_item)

        menu_item.uid = self.__item_counter
        self.__item_counter += 1

        if parent:
            self.check_item(parent)
        else:
            parent = self.__root_item

        menu_item.parent = parent

        if parent.child:
            child_item = parent.child
            while child_item.next:
                child_item = child_item.next
            child_item.next = menu_item
            menu_item.prev = child_item

        else:
            parent.child = menu_item

    def init(self, initial_item):
        self.check_item(initial_item)
        self.__main_item = initial_item
        self.__active_item = initial_item

    def check_item(self, item):
        if not isinstance(item, MenuItem):
            raise ValueError("WRONG_MENU_ITEM_INSTANCE")

    def reset(self):
        self.check_item(self.__active_item)
        self.__active_item = self.__main_item

    def clear_childs(self, child_item):
        while True:
            next_item = child_item.next
            child_item.drop_reference()
            if next_item:
                child_item = next_item
            else:
                break

    def action(self, key):
        active_item = self.__active_item
        self.check_item(active_item)

        if key == self.ACTION_PREV:
            if active_item.prev:
                self.__active_item = active_item.prev

            elif self.circular:
                while active_item.next:
                    self.__active_item = active_item.next

        elif key == self.ACTION_NEXT:
            if active_item.next:
                self.__active_item = active_item.next

            elif self.circular:
                while active_item.prev:
                    self.__active_item = active_item.prev

        elif key == self.ACTION_ENTER and not active_item.disabled:
            if callable(active_item.dynamic_cb):
                active_item.dynamic_cb(self, self.__active_item)

            if callable(active_item.enter_cb):
                active_item.enter_cb(self.__active_item)

            if active_item.child:
                self.__active_item = active_item.child

        elif key == self.ACTION_BACK:
            parent = active_item.parent
            if callable(parent.dynamic_cb):
                self.clear_childs(parent.child)
                parent.child = None

            if callable(parent.leave_cb):
                parent.leave_cb()

            if not parent.uid == 0:
                self.__active_item = parent

            elif callable(self.menu_exit):
                self.menu_exit()
                return

        if self.auto_render:
            self.render()

    def action_hotkey(self, hotkey):
        self.check_item(self.__active_item)
        item = self.__active_item
        while item.prev:
            item = item.prev

        while True:
            if item.hotkey == hotkey:
                self.__active_item = item
                self.action(self.ACTION_ENTER)
                break

            if not item.next:
                break

            item = item.next

    def set_active(self, item, enter=False):
        self.check_item(item)
        self.__active_item = item
        if enter:
            self.action(self.ACTION_ENTER)

        elif self.auto_render:
            self.render()

    def render(self):
        if not callable(self.render_item):
            raise RuntimeError("MISSING_RENDER_ITEM_FUNCTION")

        self.check_item(self.__active_item)
        parent = self.__active_item.parent

        if callable(self.pre_render):
            self.pre_render((parent.uid == 0))

        show_item = self.__active_item
        rows_counter = self.rows_limit
        render_index = 0

        if callable(self.render_title):
            parent_value = None
            if callable(parent.value_cb):
                parent_value = parent.value_cb(parent)

            self.render_title(parent, parent_value)
            rows_counter -= 1

        if self.show_previous_items:
            while show_item.prev:
                show_item = show_item.prev

        if show_item.prev and callable(self.render_scroll_up):
            self.render_scroll_up()

        while True:
            is_active = show_item.uid == self.__active_item.uid
            self.render_item(show_item, render_index, is_active)
            render_index += 1
            rows_counter -= 1

            if rows_counter <= 0 or not show_item.next:
                break

            show_item = show_item.next

        if show_item.next and callable(self.render_scroll_down):
            self.render_scroll_down()

        if callable(self.post_render):
            self.post_render((parent.uid == 0))
