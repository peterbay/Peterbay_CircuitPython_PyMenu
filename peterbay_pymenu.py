# SPDX-FileCopyrightText: 2023 Petr Vavrin <pvavrin@gmail.com>
# SPDX-FileCopyrightText: Copyright (c) 2023 Petr Vavrin
#
# SPDX-License-Identifier: MIT
# pylint: disable=no-self-use, not-callable, too-many-branches
"""
`peterbay_pymenu`
================================================================================

Universal python library for creating menus for console and GUI applications.

The menu supports 2 main methods of navigation: hotkeys and index selection.
Hotkeys are characters entered by the user via ```input()```. Index selection
can be used with buttons, rotary encoder, or other hardware to input
up and down commands to move the selection index and then enter to execute
the selected menu item.

The menu is adaptable by overriding these functions:

```render_title```: Responsible for rendering the title of the menu. See
simpletest example for an implementation that prints title with ASCII
characters.

```render_item```: Responsible for rendering an item within the menu.
and if desired, the selection indicator. See simpletest example
for an implementation that prints the items with ASCII characters

```pre_render```: Called at the beginning of the render operation.
See simpletest example for an implementation that prints side
boundaries with ASCII characters

```post_render```: Called at the end of the render operation.
See simpletest example for an implementation that prints side
boundaries with ASCII characters


* Author(s): Petr Vavrin

Implementation Notes
--------------------


"""

# imports

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/peterbay/Peterbay_CircuitPython_PyMenu.git"


class MenuItem:
    """Menu item class

    :param int uid: Unique item ID (automatically set in menu core)
    :param str label: Label of menu item
    :param str hotkey: Hotkey defined for menu item
    :param object data: Object, string, int, etc. for storing custom data
    :param bool disabled: Disabled menu item (not selectable)

    :param function enter_cb: Callback function for enter action
    :param function leave_cb: Callback function for leave action
    :param function value_cb: Callback function for value action
    :param function dynamic_cb: Callback function for dynamic action

    :param MenuItem parent: Parent menu item (set in menu core)
    :param MenuItem prev: Previous menu item (set in menu core)
    :param MenuItem next: Next menu item (set in menu core)
    :param MenuItem child: Child menu item (set in menu core)
    """

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
        """Create menu item instance"""
        for key, value in kwargs.items():
            setattr(self, key, value)

    def drop_reference(self):
        """Drop menu item reference"""
        self.prev = None
        self.next = None
        self.child = None


class MenuCore:
    """Menu core class

    :param bool auto_render: Auto render menu after action
    :param bool show_previous_items: Show previous items in menu
    :param bool circular: Enable circular navigation
    :param int rows_limit: Limit of rows in menu

    :param function menu_exit: Callback function for menu exit
    :param function pre_render: Callback function for pre-render
    :param function post_render: Callback function for post-render
    :param function render_scroll_up: Callback function for scroll up
    :param function render_scroll_down: Callback function for scroll down
    :param function render_title: Callback function for render title
    :param function render_item: Callback function for render item
    """

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
        """Create menu core instance"""
        self.__root_item = MenuItem()
        self.__root_item.uid = 0

    def add_item(self, menu_item, parent=None):
        """Add menu item to the menu

        :param MenuItem menu_item: Menu item to add
        :param MenuItem parent: Parent menu item
        """
        self.__check_item(menu_item)

        menu_item.uid = self.__item_counter
        self.__item_counter += 1

        if parent:
            self.__check_item(parent)
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
        """Set initial menu item

        :param MenuItem initial_item: Initial menu item
        """
        self.__check_item(initial_item)
        self.__main_item = initial_item
        self.__active_item = initial_item

    def __check_item(self, item):
        if not isinstance(item, MenuItem):
            raise ValueError("WRONG_MENU_ITEM_INSTANCE")

    def reset(self):
        """Reset menu to the initial menu item"""
        self.__check_item(self.__active_item)
        self.__active_item = self.__main_item

    def __clear_childs(self, child_item):
        while True:
            next_item = child_item.next
            child_item.drop_reference()
            if next_item:
                child_item = next_item
            else:
                break

    def action(self, key):
        """Perform menu action

        :param int key: Action key
        """
        active_item = self.__active_item
        self.__check_item(active_item)

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
                self.__clear_childs(parent.child)
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
        """Perform menu action by hotkey

        :param str hotkey: Hotkey
        """
        self.__check_item(self.__active_item)
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
        """Set active menu item
        :param MenuItem item: Menu item to set as active
        :param bool enter: Perform enter action
        """
        self.__check_item(item)
        self.__active_item = item
        if enter:
            self.action(self.ACTION_ENTER)

        elif self.auto_render:
            self.render()

    def render(self):
        """Render menu"""
        if not callable(self.render_item):
            raise RuntimeError("MISSING_RENDER_ITEM_FUNCTION")

        self.__check_item(self.__active_item)
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
