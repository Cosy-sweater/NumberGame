from tkinter import *
import time
from random import choice, sample

root = Tk()
root.geometry("1000x458")

action_symbols = ["+", "-", "*", "/"]
button_list = []
radiobutton_list = []
selected_task = IntVar()
expression = ""
expression_elements = 0

statistics = {}
correct = 0
current_time = time.time()


def get_numbers(len1=25, len2=2, range1=(3, 50)):  # len2 = 5
    result1 = list(map(str, sample(range(*range1), len1)))
    result2 = []
    while len(result2) < len2:
        temp = eval(str(choice(result1)) + choice(action_symbols[:-2]) + str(choice(result1)))
        if temp not in result2 and temp == int(temp) and temp != 0:
            result2.append(int(temp))

    return result1, result2


def reset_expression():
    global expression, expression_elements
    expression = ""
    expression_elements = 0
    expression_label["text"] = ""
    for button in button_list:
        button.switch_activity(reset=True)


def select_task():
    global current_task_result
    current_task_result = int(radiobutton_list[selected_task.get()]["text"])
    print(current_task_result)


def confirm():
    global current_time, correct
    to_statistics = [round(time.time() - current_time, 1), selected_task.get()]
    if current_task_result == eval(expression):
        radiobutton_list[selected_task.get()]["bg"] = "#1dc320"
        correct += 1
    else:
        radiobutton_list[selected_task.get()]["bg"] = "#e0293e"
    radiobutton_list[selected_task.get()]["state"] = "disabled"

    to_statistics.append(current_task_result)
    to_statistics.append(eval(expression))
    statistics[radiobutton_list[selected_task.get()]["text"]] = to_statistics
    current_time = time.time()

    del possible_selections[selected_task.get() - (len(radiobutton_list) - len(possible_selections))]
    # (len(radiobutton_list) - len(possible_selections)) сдвиг индексов возможных выборов

    if len(possible_selections) == 0:
        show_endscreen()
        return
    selected_task.set(possible_selections[0])
    reset_expression()
    select_task()


def show_endscreen():
    reset_button["state"] = "disabled"
    confirm_button["state"] = "disabled"
    popup = Toplevel()
    popup.protocol("WM_DELETE_WINDOW", root.destroy)

    for key in statistics:  # дичь, индексы и форматирование сток
        values = statistics[key]
        text = f'Пример №{values[1] + 1}:\nВремя:{values[0]}\nОтвет:{values[3]}\nПравильный ответ:{values[2]}'
        Label(popup, text=text, font="Calibri 24", anchor='n').pack(side=TOP, padx=20, pady=25)

    Label(popup, text=f'Всего {correct}/{len(radiobutton_list)}', font="Calibri 24", anchor='n').pack(side=TOP, padx=20,
                                                                                                      pady=25)

    popup.mainloop()


buttons_numbers, task_numbers = get_numbers()


class CustomButton:
    def __init__(self, symbol="#", is_active=True, x=0, y=0):
        self.activity = {True: "active", False: "disabled"}
        self.is_active = is_active

        self.button = Button(root, text=symbol, font="Calibri 24", width=4, command=self.on_click)
        self.button["state"] = self.activity[self.is_active]
        self.button.place(x=x, y=y)

    def on_click(self):
        global expression, expression_elements
        expression += self.button["text"]
        expression_elements += 1

        for button in button_list:
            button.switch_activity(set_to=False if expression_elements == 3 else None)

        if expression_elements < 3:
            confirm_button["state"] = "disabled"
        else:
            confirm_button["state"] = "active"

        expression_label["text"] = expression

    def switch_activity(self, set_to=None, reset=False):
        if set_to is None:
            self.is_active = not self.is_active
        else:
            self.is_active = set_to

        if reset is True:
            self.is_active = self.button["text"].isdigit()  # if num True else False

        self.button["state"] = self.activity[self.is_active]

        if self.button["text"] in expression.replace("-", "+").replace("*", "+").replace("/", "+").split("+"):
            self.button["state"] = "disabled"


for row in range(5):
    for column in range(5):
        x = row * 75 + 5
        y = column * 70 + 5
        index = column * 5 + row
        button_list.append(CustomButton(symbol=buttons_numbers[index], x=x, y=y))

for i in action_symbols:
    x = action_symbols.index(i) * 75 + 695
    button_list.append(CustomButton(symbol=i, x=x, y=5, is_active=False))

# reset button
reset_button = Button(root, text="Сброс", font="Calibri 24", command=reset_expression)
reset_button.place(x=888, y=75)

# confirm button
confirm_button = Button(root, text="Проверить", font="Calibri 24", command=confirm, state="disabled")
confirm_button.place(x=717, y=75)

expression_label = Label(root, text="", bg="#777777", font="Calibri 24", width=17)
expression_label.place(x=400, y=15)

for index, number in enumerate(task_numbers):
    new_button = Radiobutton(root, text=str(number), variable=selected_task, value=index, font="Calibri 24",
                             bg="#DDDDDD", width=10, command=select_task)
    new_button.place(x=index * 201, y=400)
    radiobutton_list.append(new_button)
current_task_result = int(radiobutton_list[selected_task.get()]["text"])
possible_selections = [i for i in range(len(radiobutton_list))]

mainloop()