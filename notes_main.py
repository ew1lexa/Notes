from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QListWidget, QWidget, QTextEdit, QLabel, QInputDialog
from PyQt5.QtGui import QIcon
import json

# Добавить замтеку
def add_note():
    note_name, ok = QInputDialog.getText(
        window, "Добавить заметку", "Название заметки:"
    )
    notes[note_name] = {"текст": "", "теги": []}
    notes_list.addItem(note_name)

# Удалить заметку 
def del_note():
    if notes_list.selectedItems():
        note_name = notes_list.selectedItems()[0].text()
        del notes[note_name]  # Удаляем заметку из словаря
        notes_list.takeItem(notes_list.row(notes_list.selectedItems()[0]))  # Удаляем заметку из списка
        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(notes, file, ensure_ascii=False, indent=4)  # Сохраняем изменения в файл
        print(f"Заметка '{note_name}' удалена.")
    else:
        print("Заметка для удаления не выбрана!")

# Сохранить заметку
def save_note():
    if notes_list.selectedItems():
        note_name = notes_list.selectedItems()[0].text()
        note_text = note_edit.toPlainText()
        notes[note_name]["текст"] = note_text
        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(notes, file, ensure_ascii=False, indent=4)
        print(f"Заметка '{note_name}' сохранена.")
    else:
        print("Заметка для сохранения не выбрана!")

# Добавление тега
def add_tag():
    if notes_list.selectedItems():
        key = notes_list.selectedItems()[0].text()
        tag = tag_input.text()
        if tag and tag not in notes[key]["теги"]:
            notes[key]["теги"].append(tag)
            tags_list.addItem(tag)
            tag_input.clear()
        with open("notes_data.json", "w", encoding = 'utf-8') as file:
            json.dump(notes, file, ensure_ascii=False, sort_keys=True)
    else:
        print("Заметка для добавления тега не выбрана!")

# Удаление тега
def del_tag():
    if notes_list.selectedItems():
        key = notes_list.selectedItems()[0].text()
        if tags_list.selectedItems():
            tag = tags_list.selectedItems()[0].text()
            if tag in notes[key]["теги"]:
                notes[key]["теги"].remove(tag)
                tags_list.takeItem(tags_list.row(tags_list.selectedItems()[0]))
                with open("notes_data.json", "w", encoding = 'utf-8') as file:
                    json.dump(notes, file, sort_keys=True)
        else:
            print("Тег для удаления не выбран!")
    else:
        print("Заметка для удаления тега не выбрана!") 

# Искать тег
def search_tag():
    tag = tag_input.text()
    if search_by_tag_button.text() == "Искать заметки по тегу" and tag:
        notes_filtered = {}  # Словарь для заметок с выбранным тегом
        for note_name, note_data in notes.items():
            if tag in note_data["теги"]:
                notes_filtered[note_name] = note_data
        search_by_tag_button.setText("Сбросить поиск")
        notes_list.clear()
        tags_list.clear()
        notes_list.addItems(notes_filtered.keys())
    elif search_by_tag_button.text() == "Сбросить поиск":
        tag_input.clear()
        notes_list.clear()
        tags_list.clear()
        notes_list.addItems(notes.keys())
        search_by_tag_button.setText("Искать заметки по тегу")
    else:
        pass
    
# Обработка нажатия на название
def show_note():
    if notes_list.selectedItems():
        name = notes_list.selectedItems()[0].text()
        note_edit.setText(notes[name]['текст'])
        tags_list.clear()
        tags_list.addItems(notes[name]['теги'])

app = QApplication([])
window = QMainWindow()
window.setWindowTitle("Умные заметки")
window.setGeometry(100, 100, 800, 600)  # Устанавливаем размер окна

# Создание центрального виджета и основного горизонтального лэйаута
central_widget = QWidget()
window.setCentralWidget(central_widget)
main_layout = QHBoxLayout(central_widget)  # Основной лэйаут (горизонтальный)

# Левая часть: поле для редактирования заметки
left_layout = QVBoxLayout()  # Вертикальный лэйаут для левой части
note_edit = QTextEdit()  # Поле для редактирования заметки
note_edit.setPlaceholderText("Редактируйте заметку здесь...")
note_edit.setStyleSheet("font-size: 14px; padding: 10px;")
left_layout.addWidget(note_edit)

# Правая часть: все остальные элементы
right_layout = QVBoxLayout()  # Вертикальный лэйаут для правой части
right_layout.setSpacing(15)  # Устанавливаем отступы между элементами

# Заголовок "Список заметок"
notes_label = QLabel("Список заметок")
notes_label.setStyleSheet("font-weight: bold; font-size: 16px; margin-bottom: 10px;")
right_layout.addWidget(notes_label)

# Список заметок
notes_list = QListWidget()
notes_list.setStyleSheet("font-size: 14px; padding: 5px;")
right_layout.addWidget(notes_list)

# Кнопки для управления заметками (с иконками)
button_layout = QHBoxLayout()
create_note_button = QPushButton(QIcon("path_to_create_icon.png"), "Создать заметку")
delete_note_button = QPushButton(QIcon("path_to_delete_icon.png"), "Удалить заметку")
create_note_button.setStyleSheet("""
    font-size: 12px; 
    padding: 6px; 
    border-radius: 8px; 
    background-color: #4CAF50; 
    color: white; 
    border: none;
""")
delete_note_button.setStyleSheet("""
    font-size: 12px; 
    padding: 6px; 
    border-radius: 8px; 
    background-color: #F44336; 
    color: white; 
    border: none;
""")
button_layout.addWidget(create_note_button)
button_layout.addWidget(delete_note_button)
right_layout.addLayout(button_layout)

# кнопка "Сохранить заметку" 
save_note_button = QPushButton("Сохранить заметку")
save_note_button.setStyleSheet("""
    font-size: 14px; 
    padding: 10px; 
    border-radius: 8px; 
    background-color: #4CAF50; 
    color: white; 
    border: none;
""")
right_layout.addWidget(save_note_button)

# Заголовок "Список тегов"
tags_label = QLabel("Список тегов")
tags_label.setStyleSheet("font-weight: bold; font-size: 16px; margin-top: 20px; margin-bottom: 10px;")
right_layout.addWidget(tags_label)

# Поле для ввода тега
tag_input = QLineEdit()
tag_input.setPlaceholderText("Введите тег...")
tag_input.setStyleSheet("font-size: 14px; padding: 8px; border-radius: 8px;")
right_layout.addWidget(tag_input)

# Список тегов
tags_list = QListWidget()
tags_list.setStyleSheet("font-size: 14px; padding: 5px;")
right_layout.addWidget(tags_list)

# Кнопки для управления тегами (с иконками)
tag_button_layout = QHBoxLayout()
add_tag_button = QPushButton(QIcon("path_to_add_icon.png"), "Добавить к заметке")
remove_tag_button = QPushButton(QIcon("path_to_remove_icon.png"), "Открепить от заметки")
add_tag_button.setStyleSheet("""
    font-size: 12px; 
    padding: 6px; 
    border-radius: 8px; 
    background-color: #2196F3; 
    color: white; 
    border: none;
""")
remove_tag_button.setStyleSheet("""
    font-size: 12px; 
    padding: 6px; 
    border-radius: 8px; 
    background-color: #FF9800; 
    color: white; 
    border: none;
""")
tag_button_layout.addWidget(add_tag_button)
tag_button_layout.addWidget(remove_tag_button)
right_layout.addLayout(tag_button_layout)


# Кнопка "Искать заметки по тегу" 
search_by_tag_button = QPushButton("Искать заметки по тегу")
search_by_tag_button.setStyleSheet("""
    font-size: 14px; 
    padding: 10px; 
    border-radius: 8px; 
    background-color: #2196F3; 
    color: white; 
    border: none;
""")
right_layout.addWidget(search_by_tag_button)

# Привязка функций к кнопкам
notes_list.clicked.connect(show_note)
create_note_button.clicked.connect(add_note)
delete_note_button.clicked.connect(del_note)
save_note_button.clicked.connect(save_note)
add_tag_button.clicked.connect(add_tag)
remove_tag_button.clicked.connect(del_tag)
search_by_tag_button.clicked.connect(search_tag)

# Добавляем левую и правую части в основной лэйаут
main_layout.addLayout(left_layout, 70)  # 70% ширины для левой части
main_layout.addLayout(right_layout, 30)  # 30% ширины для правой части

# Загрузка json
with open('notes_data.json', 'r', encoding='utf-8') as file:
    notes = json.load(file)
notes_list.addItems(notes)

# Отображение окна приложения и запуск приложения
window.show()
app.exec_()