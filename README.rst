Introduction
============


.. image:: https://readthedocs.org/projects/peterbay-circuitpython-pymenu/badge/?version=latest
    :target: https://circuitpython-pymenu.readthedocs.io/
    :alt: Documentation Status


.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord


.. image:: https://github.com/peterbay/Peterbay_CircuitPython_PyMenu/workflows/Build%20CI/badge.svg
    :target: https://github.com/peterbay/Peterbay_CircuitPython_PyMenu/actions
    :alt: Build Status


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

Universal python library for creating menus for console and GUI applications.

The menu supports 2 main methods of navigation: hotkeys and index selection.
Hotkeys are characters entered by the user via ```input()```. Index selection
can be used with buttons, rotary encoder, or other hardware to input
up and down commands to move the selection index and then enter to execute
the selected menu item.

Menu Core
--------------------

The menu is adaptable by setting these properties:

```auto_render```: Auto render menu after each call of action or action_key.
Default is True.

```show_previous_items```: Show previous items in menu. If true, the menu
will show the items previous to the active item.
Default is True.

```circular```: Enable circular navigation. If enabled and first menu item
is active and user send action ACTION_PREV, the last item is selected.
If enabled and last menu item is active and user send action ACTION_NEXT,
the first item is selected. Default is False.

```rows_limit```: Limit of rows showed in menu. Useful for long menus.
For showing if previous or next items are available, use render_scroll_up_fn
and render_scroll_down_fn. Default is 255.

The menu is adaptable by overriding these functions:

```pre_render_fn```: Called at the beginning of the render operation.
See simpletest example for an implementation that prints side
boundaries with ASCII characters.

```render_title_fn```: Responsible for rendering the title of the menu. See
simpletest example for an implementation that prints title with ASCII
characters.

```render_item_fn```: Responsible for rendering an item within the menu.
and if desired, the selection indicator. See simpletest example
for an implementation that prints the items with ASCII characters.

```render_scroll_up_fn```: Responsible for rendering the symbol for showing
that previous items are available. Useful for long menus with limited rows.

```render_scroll_down_fn```: Responsible for rendering the symbol for showing
that next items are available. Useful for long menus with limited rows.

```post_render_fn```: Called at the end of the render operation.
See simpletest example for an implementation that prints side
boundaries with ASCII characters.

```menu_exit_fn```: Called when menu is in top level and ACTION_BACK is called.

Menu Item
--------------------

The menu item is adaptable by setting these parameters:

```label```: Label of menu item.

```hotkey```: Hotkey defined for menu item.

```data```: Object, string, int, etc. for storing custom data.

```disabled```: Disabled menu item (not active).

The menu item is adaptable by overriding these functions:

```dynamic_fn```: Function called to dynamically create submenu items.
Called before enter_fn.

```enter_fn```: Function called when menu item is selected.

```leave_fn```: Function called before parent menu item is selected. When action
ACTION_BACK is called.

```value_fn```: Function called for obtaining item value. Called before
render_title_fn.


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.Installing from PyPI
=====================
XXnoteXX This library is not available on PyPI yet. Install documentation is included
as a standard element. Stay tuned for PyPI availability!

XXtodoXX Remove the above note if PyPI version is/will be available at time of release.

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/PeterBay-circuitpython-pymenu/>`_.
To install for current user:

.. code-block:: shell

    pip3 install PeterBay-circuitpython-pymenu

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install PeterBay-circuitpython-pymenu

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .venv
    source .env/bin/activate
    pip3 install PeterBay-circuitpython-pymenu

Installing to a Connected CircuitPython Device with Circup
==========================================================

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip3 install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install peterbay_pymenu

Or the following command to update an existing version:

.. code-block:: shell

    circup update

Usage Example
=============

XXtodoXX Add a quick, simple example. It and other examples should live in the
examples folder and be included in docs/examples.rst.

Documentation
=============
API documentation for this library can be found on `Read the Docs <https://circuitpython-pymenu.readthedocs.io/>`_.

For information on building library documentation, please check out
`this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/peterbay/Peterbay_CircuitPython_PyMenu/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
