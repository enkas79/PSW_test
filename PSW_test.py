import sys
import re
import math
import secrets
import string
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QLabel, QProgressBar, 
                             QPushButton, QSpinBox, QCheckBox, QGroupBox, 
                             QGridLayout, QMessageBox, QMenuBar)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

# ==========================================
# Metadati e Configurazione
# ==========================================
VERSION = "1.0.0"  
REPO_OWNER = "enkas79"
REPO_NAME = "PSW_test"
AUTHOR = "Enrico Martini"

class PasswordCyberDashboard(QMainWindow):
    def __init__(self):
        super().__init__()

        # Scenari Hardware (Hashes al secondo - HPS)
        self.scenari = {
            "💻 Vecchio Laptop (Intel i3/i5)": 1_000_000,
            "🖥️ Desktop Pro (i9-14900K)": 100_000_000,
            "🚀 GPU High-End (RTX 4090)": 100_000_000_000,
            "🌌 Cluster / Attacco Quantistico": 1_000_000_000_000_000
        }

        self.common_passwords = {"123456", "password", "12345678", "qwerty", "admin123"}
        self.labels_tempo = {}
        
        self.init_ui()
        self.apply_adaptive_geometry()
        self.apply_light_styles()
        self.crea_menu()

    def init_ui(self):
        # Titolo dinamico usando i metadati
        self.setWindowTitle(f"Password Stress Test v.{VERSION}")
        
        # Widget centrale necessario per QMainWindow
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setSpacing(15)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        # --- 1. ANALISI ---
        input_group = QGroupBox("ANALISI SICUREZZA")
        input_vbox = QVBoxLayout()
        
        h_input_layout = QHBoxLayout()
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Inserisci la password...")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.textChanged.connect(self.analizza_tutto)
        h_input_layout.addWidget(self.password_input)

        self.btn_toggle_vis = QPushButton("👁️")
        self.btn_toggle_vis.setFixedWidth(40)
        self.btn_toggle_vis.setCheckable(True)
        self.btn_toggle_vis.clicked.connect(self.toggle_visibility)
        h_input_layout.addWidget(self.btn_toggle_vis)

        self.btn_copy = QPushButton("COPIA")
        self.btn_copy.clicked.connect(self.copia_password)
        h_input_layout.addWidget(self.btn_copy)
        input_vbox.addLayout(h_input_layout)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(10)
        self.progress_bar.setTextVisible(False)
        input_vbox.addWidget(self.progress_bar)
        
        self.info_label = QLabel("In attesa di input...")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        input_vbox.addWidget(self.info_label)
        input_group.setLayout(input_vbox)
        self.main_layout.addWidget(input_group)

        # --- 2. DASHBOARD ---
        scenari_group = QGroupBox("RESISTENZA STIMATA")
        grid_layout = QGridLayout()
        grid_layout.setVerticalSpacing(12)

        for i, (nome, hps) in enumerate(self.scenari.items()):
            lbl_nome = QLabel(nome)
            lbl_risultato = QLabel("-")
            lbl_risultato.setAlignment(Qt.AlignmentFlag.AlignRight)
            lbl_risultato.setObjectName("risultato_label")
            grid_layout.addWidget(lbl_nome, i, 0)
            grid_layout.addWidget(lbl_risultato, i, 1)
            self.labels_tempo[nome] = lbl_risultato

        scenari_group.setLayout(grid_layout)
        self.main_layout.addWidget(scenari_group)

        # --- 3. GENERATORE ---
        gen_group = QGroupBox("GENERATORE AUTOMATICO")
        gen_vbox = QVBoxLayout()

        l_layout = QHBoxLayout()
        l_layout.addWidget(QLabel("Lunghezza:"))
        self.spin_length = QSpinBox()
        self.spin_length.setRange(4, 128); self.spin_length.setValue(16)
        l_layout.addWidget(self.spin_length)
        gen_vbox.addLayout(l_layout)

        check_grid = QGridLayout()
        self.check_upper = QCheckBox("A-Z (Maiuscole)"); self.check_upper.setChecked(True)
        self.check_lower = QCheckBox("a-z (Minuscole)"); self.check_lower.setChecked(True)
        self.check_numbers = QCheckBox("0-9 (Numeri)"); self.check_numbers.setChecked(True)
        self.check_special = QCheckBox("!@# (Speciali)"); self.check_special.setChecked(True)
        
        check_grid.addWidget(self.check_upper, 0, 0); check_grid.addWidget(self.check_lower, 0, 1)
        check_grid.addWidget(self.check_numbers, 1, 0); check_grid.addWidget(self.check_special, 1, 1)
        gen_vbox.addLayout(check_grid)

        self.btn_genera = QPushButton("GENERA PASSWORD")
        self.btn_genera.setObjectName("btn_genera")
        self.btn_genera.clicked.connect(self.genera_sicura)
        gen_vbox.addWidget(self.btn_genera)
        gen_group.setLayout(gen_vbox)
        self.main_layout.addWidget(gen_group)

        # --- 4. ESCI ---
        self.btn_exit = QPushButton("ESCI DAL PROGRAMMA")
        self.btn_exit.setObjectName("btn_exit")
        self.btn_exit.clicked.connect(self.close)
        self.main_layout.addWidget(self.btn_exit)

    def crea_menu(self):
        """Crea la barra dei menu con le informazioni dinamiche."""
        bar_menu = self.menuBar()
        
        # Menu Aiuto
        menu_aiuto = bar_menu.addMenu("&Aiuto")
        
        # Azione Info
        azione_info = QAction("Informazioni", self)
        azione_info.triggered.connect(self.mostra_info)
        menu_aiuto.addAction(azione_info)

    def mostra_info(self):
        """Mostra il popup con i metadati dinamici."""
        messaggio = (
            #f"Software: {REPO_NAME}\n"
            f"Autore: {AUTHOR}\n"
            f"Versione: {VERSION}\n\n"
            #f"Repository: github.com/{REPO_OWNER}/{REPO_NAME}"
        )
        QMessageBox.information(self, "Info Software", messaggio)

    def apply_adaptive_geometry(self):
        screen = QApplication.primaryScreen().availableGeometry()
        f_width = max(int(screen.width() * 0.3), 600)
        f_height = max(int(screen.height() * 0.3), 600)
        self.resize(f_width, f_height)
        c = screen.center()
        self.move(c.x() - f_width // 2, c.y() - f_height // 2)

    def apply_light_styles(self):
        self.setStyleSheet("""
            QWidget { background-color: #ffffff; color: #2c3e50; font-family: 'Segoe UI', sans-serif; }
            QGroupBox { border: 1px solid #dcdde1; border-radius: 8px; margin-top: 20px; font-weight: bold; background-color: #fcfcfc; }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; color: #3498db; }
            QLineEdit { background-color: white; border: 1px solid #ced4da; border-radius: 4px; padding: 8px; }
            QPushButton { background-color: #f1f2f6; border: 1px solid #ced4da; border-radius: 4px; padding: 6px; font-weight: 500; }
            QPushButton:hover { background-color: #dfe4ea; }
            #btn_genera { background-color: #2ecc71; color: white; border: none; font-weight: bold; padding: 10px; }
            #btn_genera:hover { background-color: #27ae60; }
            #btn_exit { background-color: #e74c3c; color: white; border: none; font-weight: bold; }
            #btn_exit:hover { background-color: #c0392b; }
            QProgressBar { background-color: #f1f2f6; border-radius: 5px; }
            #risultato_label { color: #2980b9; font-family: 'Consolas', monospace; }
            QMenuBar { background-color: #f1f2f6; border-bottom: 1px solid #dcdde1; }
            QMenuBar::item:selected { background-color: #dfe4ea; }
        """)

    # --- LOGICA (Toggle, Copia, Genera, Analisi, Formattazione) ---
    def toggle_visibility(self):
        mode = QLineEdit.EchoMode.Normal if self.btn_toggle_vis.isChecked() else QLineEdit.EchoMode.Password
        self.password_input.setEchoMode(mode)
        self.btn_toggle_vis.setText("🔒" if self.btn_toggle_vis.isChecked() else "👁️")

    def copia_password(self):
        QApplication.clipboard().setText(self.password_input.text())
        self.info_label.setText("✅ Copiata!")

    def genera_sicura(self):
        pool = ""
        if self.check_upper.isChecked(): pool += string.ascii_uppercase
        if self.check_lower.isChecked(): pool += string.ascii_lowercase
        if self.check_numbers.isChecked(): pool += string.digits
        if self.check_special.isChecked(): pool += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if not pool: pool = string.ascii_lowercase 
        pwd = ''.join(secrets.choice(pool) for _ in range(self.spin_length.value()))
        self.password_input.setText(pwd)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        self.btn_toggle_vis.setChecked(True)

    def formatta_tempo_ibrido(self, secondi):
        if secondi < 1: return "Istantaneo"
        if secondi < 3600: return f"{int(secondi/60)} min"
        if secondi < 86400: return f"{int(secondi/3600)} ore"
        anni = secondi / 86400 / 365
        if anni < 1: return f"{int(secondi/86400)} giorni"
        if anni < 1_000_000: return f"{anni:,.0f} anni".replace(",", ".")
        if anni < 1_000_000_000: return f"Circa {anni/1_000_000:.1f} mln anni"
        return "Eternità 🌌"

    def analizza_tutto(self, password):
        if not password:
            self.progress_bar.setValue(0)
            for lbl in self.labels_tempo.values(): lbl.setText("-")
            return
        is_common = password.lower() in self.common_passwords
        pool = 0
        if re.search(r"[a-z]", password): pool += 26
        if re.search(r"[A-Z]", password): pool += 26
        if re.search(r"\d", password): pool += 10
        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): pool += 32
        if pool == 0: return
        combinazioni = pool ** len(password)
        entropia = len(password) * math.log2(pool)
        for nome, hps in self.scenari.items():
            if is_common:
                self.labels_tempo[nome].setText("Istantaneo (Comune)")
                self.labels_tempo[nome].setStyleSheet("color: #e74c3c; font-weight: bold;")
            else:
                tempo = self.formatta_tempo_ibrido(combinazioni / hps)
                self.labels_tempo[nome].setText(tempo)
                self.labels_tempo[nome].setStyleSheet("color: #2980b9; font-weight: bold;")
        punteggio = min(100, int((entropia / 80) * 100))
        self.progress_bar.setValue(punteggio)
        color = "#e74c3c" if punteggio < 40 else "#f1c40f" if punteggio < 75 else "#2ecc71"
        self.progress_bar.setStyleSheet(f"QProgressBar::chunk {{ background-color: {color}; }}")
        self.info_label.setText(f"Entropia: {int(entropia)} bit")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordCyberDashboard()
    window.show()
    sys.exit(app.exec())
