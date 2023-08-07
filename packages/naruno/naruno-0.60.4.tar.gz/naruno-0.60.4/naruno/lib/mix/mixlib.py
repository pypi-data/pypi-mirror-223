#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2021 Naruno Developers
Copyright (c) 2021 Onur Atakan ULUSOY

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


def starting_text_centered() -> str:
    """
    Prints the STARTING message between space.
    """

    print(" ")
    print(" STARTING")
    print(" ")

    return "\nSTARTING\n"


def ended_text_centered() -> str:
    """
    Prints the ENDED message between space.
    """
    print(" ")
    print(" ENDED")
    print(" ")

    return "\nENDED\n"


def printcentertext(text) -> str:
    """
    Prints the text between spaces.

    Inputs:
      * text: A string.
    """

    print(" ")
    print(text)
    print(" ")

    return "\n" + text + "\n"


def banner_maker(sc_name, description, author):
    """
    Returns a string in the form of a banner.

    Inputs:
      * sc_name: Name of the script.
      * description: Description of the script.
      * author: Author of the script.
    """

    return (((((f"""Script Name    : {sc_name}""" + """\n""" +
                """Description    : """) + description) + """\n""") +
             """Author         : """) + author) + """\n"""


def question_maker(question_text=None, mode=None):
    """
    Returns a string in the form of a question.

    Inputs:
      * mode: A string ("main" or "sub")
    """

    if question_text is None:
        if mode == "main":
            question_text = "Please enter main option: "
        elif mode == "sub":
            question_text = "Please enter sub option: "
        elif mode == "anykeytocontinue":
            question_text = "Press any key to continue..."
        else:
            question_text = "Please enter main option: "

    return input(question_text)


def menu_maker(menu_number, menu_text) -> str:
    """
    Returns a string in the form of a menu.

    Inputs:
      * menu_number: A data for menu defination (ex. 1, "sc")
    """

    return f"{str(menu_number)}) {menu_text}" + "\n"


def quit_menu_maker(mode) -> str:
    """
    Returns a quit string by mode.

    Inputs:
      * mode: A string ("main" or "sub")
    """

    if mode == "main":
        quit_menu_maker_result = "\n0) Quit \n"
    elif mode == "sub":
        quit_menu_maker_result = "\n0) Quit sub menu \n"
    else:
        quit_menu_maker_result = "\n0) Quit \n"

    return quit_menu_maker_result


def menu_space() -> str:
    """
    Returns a string in the form of a space.
    """

    return "\n"


def menu_seperator() -> str:
    """
    Returns a string in the form of a seperator.
    """

    return "\n" + "*** \n" + "\n"


def menu_title(menu_title_text) -> str:
    """
    Returns a string in the form of a title.

    Inputs:
      * menu_title_text: A string.
    """

    return "\n" + "*** " + menu_title_text + " ***" + " \n" + "\n"
