from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout,
    QLabel, QPushButton, QHBoxLayout, QFrame, QSizePolicy, QTextEdit
)
from PyQt5.QtGui import QIcon, QPixmap, QMovie, QFont, QTextCharFormat, QTextBlockFormat, QPainter, QColor
from PyQt5.QtCore import Qt, QSize, QTimer
import sys
import os
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")
Assistantname = env_vars.get("Assistantname")

# Define directories
current_dir = os.getcwd()
def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what's", "where's", "how's"]

    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."

    return new_query.capitalize()
# --- CONFIRMED PATH ---
TempDirPath = rf"{current_dir}\Frontend\Files" 
GraphicsDirPath = rf"{current_dir}\Frontend\Graphics"


# --- FILE I/O AND STATUS FUNCTIONS (WITH STABILITY FIXES) ---

def SetMicrophoneStatus(Command):
    os.makedirs(TempDirPath, exist_ok=True) 
    with open(rf"{TempDirPath}\Mic.data", "w", encoding='utf-8') as file:
        file.write(Command)

def GetMicrophoneStatus():
    try:
        with open(rf"{TempDirPath}\Mic.data", "r", encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        SetMicrophoneStatus("False") 
        return "False"

def SetAssistantStatus(Status):
    os.makedirs(TempDirPath, exist_ok=True)
    with open(rf"{TempDirPath}\Status.data", "w", encoding='utf-8') as file:
        file.write(Status)

def GetAssistantStatus():
    try:
        with open(rf"{TempDirPath}\Status.data", "r", encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        SetAssistantStatus(f"Ready, I'm {Assistantname}.")
        return f"Ready, I'm {Assistantname}."

def MicButtonInitialed(): 
    SetMicrophoneStatus("False")

def MicButtonClosed(): 
    SetMicrophoneStatus("True")

def GraphicsDirectoryPath(Filename):
    return rf"{GraphicsDirPath}\{Filename}"

def TempDirectoryPath(Filename):
    return rf"{TempDirPath}\{Filename}"

def ShowTextToScreen(Text):
    os.makedirs(TempDirPath, exist_ok=True)
    with open(TempDirectoryPath("Responses.data"), "w", encoding='utf-8') as file:
        file.write(Text)

# -------------------------------------------------------------------------


class ChatSection(QWidget):
    def __init__(self):
        super(ChatSection, self).__init__()
        self.old_chat_message = "" 
        self.toggled = False 
        self.icon_label = QLabel() 
        self.gif_label = QLabel() 

        layout = QVBoxLayout(self)
        layout.setContentsMargins(-10, 40, 40, 100)
        layout.setSpacing(-100)

        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
        self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
        layout.addWidget(self.chat_text_edit)

        self.setStyleSheet("background-color: black;")
        layout.setSizeConstraint(QVBoxLayout.SetDefaultConstraint)
        layout.setStretch(1, 1)

        self.label = QLabel("")
        self.label.setStyleSheet("color: white; font-size:16px; margin-right: 195px; border: none; margin-top: -30px;")
        self.label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.label)
        layout.setSpacing(-10)
        layout.addWidget(self.gif_label)

        font = QFont()
        font.setPointSize(13)
        self.chat_text_edit.setFont(font)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loadMessages)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(100) # Performance fix

        self.setStyleSheet("""
             QScrollBar:vertical { border: none; background: black; width: 10px; margin: 0px; }
             QScrollBar::handle:vertical { background: white; min-height: 20px; } 
             QScrollBar::add-line:vertical { background: black; height: 10px; subcontrol-position: bottom; subcontrol-origin: margin; }
             QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical { border: none; background: none; color: none; }
             QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }
        """)

    def loadMessages(self):
        try:
            with open(TempDirectoryPath('Responses.data'), "r", encoding='utf-8') as file:
                messages = file.read()
        except FileNotFoundError:
            ShowTextToScreen("")
            messages = ""

        if not messages or len(messages.strip()) <= 1 or self.old_chat_message == messages:
            pass
        else:
            self.addMessage(message=messages, color='White')
            self.old_chat_message = messages 

    def SpeechRecogText(self):
        try:
            with open(TempDirectoryPath('Status.data'), "r", encoding='utf-8') as file:
                self.label.setText(file.read().strip())
        except FileNotFoundError:
            status = f"Ready, I'm {Assistantname}."
            SetAssistantStatus(status)
            self.label.setText(status)

    def addMessage(self, message, color):
        cursor = self.chat_text_edit.textCursor()
        text_format = QTextCharFormat()
        block_format = QTextBlockFormat()
        block_format.setTopMargin(10)
        block_format.setLeftMargin(10)
        text_format.setForeground(QColor(color))
        cursor.setCharFormat(text_format)
        cursor.setBlockFormat(block_format)
        cursor.insertText(message + "\n")
        self.chat_text_edit.setTextCursor(cursor)
        
class InitialScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        screen = QApplication.primaryScreen()
        geometry = screen.geometry()
        screen_width = geometry.width()
        screen_height = geometry.height()

        content_layout = QVBoxLayout(self)
        content_layout.setContentsMargins(0, 0, 0, 0)

        gif_label = QLabel()
        movie = QMovie(GraphicsDirectoryPath('Jarvis.gif'))
        gif_label.setMovie(movie)
        
        # --- FIX: START THE GIF ANIMATION ---
        movie.start()
        
        gif_label.setAlignment(Qt.AlignCenter)
        gif_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.icon_label = QLabel()
        self.icon_label.setFixedSize(150, 150)
        self.icon_label.setAlignment(Qt.AlignCenter)

        self.toggled = True
        self.toggle_icon()
        self.icon_label.mousePressEvent = self.toggle_icon

        self.label = QLabel("")
        self.label.setStyleSheet("color: white; font-size:16px; margin-bottom:0;")

        content_layout.addWidget(gif_label, alignment=Qt.AlignCenter)
        content_layout.addWidget(self.label, alignment=Qt.AlignCenter)
        content_layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)
        content_layout.setContentsMargins(0, 0, 0, 150)

        self.setLayout(content_layout)
        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)
        self.setStyleSheet("background-color: black;")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(100) # Performance fix

    def SpeechRecogText(self):
        try:
            with open(TempDirectoryPath('Status.data'), "r", encoding='utf-8') as file:
                self.label.setText(file.read().strip())
        except FileNotFoundError:
            status = f"Ready, I'm {Assistantname}."
            SetAssistantStatus(status)
            self.label.setText(status)

    def load_icon(self, path, width=60, height=60):
        pixmap = QPixmap(path)
        self.icon_label.setPixmap(pixmap.scaled(width, height))

    def toggle_icon(self, event=None):
        if self.toggled:
            self.load_icon(GraphicsDirectoryPath('Mic_on.png'), 60, 60)
            MicButtonInitialed()
        else:
            self.load_icon(GraphicsDirectoryPath('Mic_off.png'), 60, 60)
            MicButtonClosed()
        self.toggled = not self.toggled


class MessageScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        screen = QApplication.primaryScreen()
        geometry = screen.geometry()
        layout = QVBoxLayout(self)
        layout.addWidget(ChatSection())
        self.setStyleSheet("background-color: black;")
        self.setFixedHeight(geometry.height())
        self.setFixedWidth(geometry.width())

class CustomTopBar(QWidget):
    def __init__(self, parent, stacked_widget):
        super().__init__(parent)
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        self.setFixedHeight(50)
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignRight)

        home_button = QPushButton(" Home ")
        home_button.setIcon(QIcon(GraphicsDirectoryPath("Home.png")))
        home_button.setStyleSheet("height:40px; background-color:white; color: black;")

        message_button = QPushButton(" Chat ")
        message_button.setIcon(QIcon(GraphicsDirectoryPath("Chats.png")))
        message_button.setStyleSheet("height:40px; background-color:white; color: black;")

        self.minimize_button = QPushButton()
        self.minimize_button.setIcon(QIcon(GraphicsDirectoryPath("Minimize2.png")))
        self.minimize_button.setStyleSheet("background-color:white;")
        self.minimize_button.clicked.connect(self.minimizeWindow)

        self.maximize_button = QPushButton()
        self.maximize_icon = QIcon(GraphicsDirectoryPath("Maximize.png"))
        self.restore_icon = QIcon(GraphicsDirectoryPath("Minimize.png"))
        self.maximize_button.setIcon(self.maximize_icon)
        self.maximize_button.setFlat(True)
        self.maximize_button.setStyleSheet("background-color:white;")
        self.maximize_button.clicked.connect(self.maximizeWindow)

        close_button = QPushButton()
        close_button.setIcon(QIcon(GraphicsDirectoryPath("Close.png")))
        close_button.setStyleSheet("background-color:white;")
        close_button.clicked.connect(self.closeWindow)

        title_label = QLabel(f"{str(Assistantname).capitalize()} AI")
        title_label.setStyleSheet("color: black; font-size: 18px; background-color:white;")

        layout.addWidget(title_label)
        layout.addStretch(1)
        layout.addWidget(home_button)
        layout.addWidget(message_button)
        layout.addStretch(1)
        layout.addWidget(self.minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(close_button)

        home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        message_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        self.draggable = True
        self.offset = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.white)
        super().paintEvent(event)

    def minimizeWindow(self):
        self.parent().showMinimized()

    def maximizeWindow(self):
        if self.parent().isMaximized():
            self.parent().showNormal()
            self.maximize_button.setIcon(self.maximize_icon)
        else:
            self.parent().showMaximized()
            self.maximize_button.setIcon(self.restore_icon)

    def closeWindow(self):
        self.parent().close()

    def mousePressEvent(self, event):
        if self.draggable:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.draggable and self.offset:
            self.parent().move(event.globalPos() - self.offset)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.initUI()

    def initUI(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()

        self.stacked_widget = QStackedWidget(self)

        # Ensure default status files exist on startup
        SetMicrophoneStatus("False")
        SetAssistantStatus(f"Ready, I'm {Assistantname}.")
        ShowTextToScreen("Hello! I am ready to assist you.")

        self.stacked_widget.addWidget(InitialScreen())
        self.stacked_widget.addWidget(MessageScreen())

        self.setGeometry(0, 0, screen_geometry.width(), screen_geometry.height())
        self.setStyleSheet("background-color: black;")

        top_bar = CustomTopBar(self, self.stacked_widget)
        self.setMenuWidget(top_bar)
        self.setCentralWidget(self.stacked_widget)

def GraphicalUserInterface():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    GraphicalUserInterface()