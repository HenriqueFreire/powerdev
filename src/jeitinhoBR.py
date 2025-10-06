import sys
from PyQt6.QtWidgets import QApplication, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor
import time

def main():
    app = QApplication(sys.argv)
    
    # --- INÍCIO DA MODIFICAÇÃO POWER-DEV ---
    # Define um nome de classe único para o nosso aplicativo.
    # Isso será usado como nosso "sinal secreto".
    app.setApplicationName("powerdev_secret")
    # --- FIM DA MODIFICAÇÃO POWER-DEV ---

    label = QLabel("Isso é um Overlay PyQt6!\nInvisível para captura?")
    
    label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    # --- INÍCIO DA MODIFICAÇÃO DE DEPURAÇÃO ---
    # Remove as flags que fazem a janela ser ignorada pelo WM/compositor.
    # A janela agora aparecerá com bordas normais.
    label.setWindowFlags(
        Qt.WindowType.WindowStaysOnTopHint
    )
    # --- FIM DA MODIFICAÇÃO DE DEPURAÇÃO ---
    
    palette = label.palette()
    palette.setColor(QPalette.ColorRole.WindowText, QColor("white"))
    label.setPalette(palette)
    
    label.setGeometry(300, 400, 800, 200)
    label.show()

    win_id = int(label.winId())
    print(f"Janela criada com WM_CLASS='powerdev_secret'. ID: {hex(win_id)}")
    print("Este script continuará rodando.")

    sys.exit(app.exec())

if __name__ == "__main__":
    main()