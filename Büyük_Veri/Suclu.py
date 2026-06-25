import sys
import pyodbc
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QSpinBox, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QScrollArea, QGridLayout, QComboBox
)
from PyQt6.QtCore import Qt


class TumZanliAramaUygulamasi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zanlı Profil Detaylı Yönetim Sistemi (CRUD)")
        self.setGeometry(50, 50, 1300, 800)

        # Yeni Veri Tiplerine Uygun Dönüşüm Sözlükleri (char/varchar tabanlı)
        self.goz_rengi_sozlugu = {"Seçiniz...": ""}
        self.sehir_sozlugu = {"Seçiniz...": ""}
        self.suc_sozlugu = {"Seçiniz...": ""}
        self.kan_sozlugu = {"Seçiniz...": ""}

        # Veritabanı Bağlantısı
        self.db_connect()

        # Arayüz Bileşenleri
        self.init_ui()

        # Veritabanından tüm ComboBox verilerini yükle
        self.combobox_verilerini_yukle()

    def db_connect(self):
        try:
            self.conn = pyodbc.connect(
                'DRIVER={SQL Server};'
                'SERVER=.\\SQLEXPRESS;'
                'DATABASE=Suclu_Veritabanı;'
                'Trusted_Connection=yes;'
            )
            self.cursor = self.conn.cursor()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Veritabanı Hatası",
                f"Veritabanına bağlanılamadı!\n\nTeknik Hata:\n{e}"
            )
            sys.exit()

    def combobox_verilerini_yukle(self):
        try:
            # 1. Göz Renklerini Yükle (Göz_Rengi_Id artık char(1))
            self.cursor.execute("SELECT Göz_Rengi_Id, Göz_Rengi FROM Goz_Renkleri")
            for row in self.cursor.fetchall():
                r_id, r_ad = str(row[0]).strip(), str(row[1]).strip()
                self.goz_rengi_sozlugu[r_ad] = r_id
                self.cmb_goz_rengi.addItem(r_ad)
                self.cmb_ekle_goz_rengi.addItem(r_ad)

            # 2. Şehirleri (Plaka) Yükle (Plaka artık varchar(2))
            self.cursor.execute("SELECT Plaka, Sehir_Adi FROM dbo.Sehirler ORDER BY Plaka")
            for row in self.cursor.fetchall():
                p_id, s_ad = str(row[0]).strip(), str(row[1]).strip()
                gosterim_adi = f"{p_id} - {s_ad}"
                self.sehir_sozlugu[gosterim_adi] = p_id
                self.cmb_plaka.addItem(gosterim_adi)
                self.cmb_ekle_plaka.addItem(gosterim_adi)

            # 3. Suç Kayıtlarını Yükle (Suç_Kaydı_Id artık varchar(3))
            self.cursor.execute("SELECT Suc_Kaydi_Id, Suc_Kaydi FROM Suc_Kayitlari WHERE Suc_Kaydi_Id IS NOT NULL")
            for row in self.cursor.fetchall():
                s_id, s_ad = str(row[0]).strip(), str(row[1]).strip()
                self.suc_sozlugu[s_ad] = s_id
                self.cmb_suc_id.addItem(s_ad)
                self.cmb_ekle_suc_id.addItem(s_ad)

            # 4. Kan Gruplarını Yükle (Kan_Grubu_Id artık varchar(1))
            self.cursor.execute("SELECT Kan_Grubu_Id, Kan_Grubu FROM Kan_Gruplari WHERE Kan_Grubu_Id IS NOT NULL")
            for row in self.cursor.fetchall():
                k_id, k_ad = str(row[0]).strip(), str(row[1]).strip()
                self.kan_sozlugu[k_ad] = k_id
                self.cmb_kan_id.addItem(k_ad)
                self.cmb_ekle_kan_id.addItem(k_ad)

        except Exception as e:
            print("ComboBox verileri yüklenirken teknik hata oluştu:", e)

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout_yatay = QHBoxLayout(main_widget)

        # --- SOL TARAF (ARAMA VE TABLO) ---
        sol_panel = QWidget()
        sol_layout = QVBoxLayout(sol_panel)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        grid_layout = QGridLayout(scroll_widget)

        grid_layout.addWidget(QLabel("TC Kimlik:"), 0, 0)
        self.txt_tc = QLineEdit()
        grid_layout.addWidget(self.txt_tc, 0, 1)

        grid_layout.addWidget(QLabel("Ad:"), 0, 2)
        self.txt_ad = QLineEdit()
        grid_layout.addWidget(self.txt_ad, 0, 3)

        grid_layout.addWidget(QLabel("Soyad:"), 0, 4)
        self.txt_soyad = QLineEdit()
        grid_layout.addWidget(self.txt_soyad, 0, 5)

        grid_layout.addWidget(QLabel("Göz Rengi:"), 1, 0)
        self.cmb_goz_rengi = QComboBox()
        self.cmb_goz_rengi.addItem("Seçiniz...")
        grid_layout.addWidget(self.cmb_goz_rengi, 1, 1)

        grid_layout.addWidget(QLabel("Doğum Yılı (Min-Max):"), 1, 2)
        range_yıl_layout = QHBoxLayout()
        self.sb_yil_min = QSpinBox()
        self.sb_yil_min.setRange(1900, 2026)
        self.sb_yil_min.setValue(1900)
        self.sb_yil_max = QSpinBox()
        self.sb_yil_max.setRange(1900, 2026)
        self.sb_yil_max.setValue(2026)
        range_yıl_layout.addWidget(self.sb_yil_min)
        range_yıl_layout.addWidget(self.sb_yil_max)
        grid_layout.addLayout(range_yıl_layout, 1, 3)

        grid_layout.addWidget(QLabel("Boy (Min-Max):"), 1, 4)
        range_boy_layout = QHBoxLayout()
        self.sb_boy_min = QSpinBox()
        self.sb_boy_min.setRange(0, 250)
        self.sb_boy_min.setValue(0)
        self.sb_boy_max = QSpinBox()
        self.sb_boy_max.setRange(0, 250)
        self.sb_boy_max.setValue(250)
        range_boy_layout.addWidget(self.sb_boy_min)
        range_boy_layout.addWidget(self.sb_boy_max)
        grid_layout.addLayout(range_boy_layout, 1, 5)

        grid_layout.addWidget(QLabel("Parmak İzi Kodu:"), 2, 0)
        self.txt_parmak_izi = QLineEdit()
        grid_layout.addWidget(self.txt_parmak_izi, 2, 1)

        grid_layout.addWidget(QLabel("Belirgin Özellik:"), 2, 2)
        self.txt_ozellik = QLineEdit()
        grid_layout.addWidget(self.txt_ozellik, 2, 3)

        grid_layout.addWidget(QLabel("DNA Kodu:"), 2, 4)
        self.txt_dna = QLineEdit()
        grid_layout.addWidget(self.txt_dna, 2, 5)

        grid_layout.addWidget(QLabel("Ayak (Min-Max):"), 3, 0)
        range_ayak_layout = QHBoxLayout()
        self.txt_ayak_min = QSpinBox()
        self.txt_ayak_min.setRange(0, 60)
        self.txt_ayak_min.setValue(0)
        self.txt_ayak_max = QSpinBox()
        self.txt_ayak_max.setRange(0, 60)
        self.txt_ayak_max.setValue(60)
        range_ayak_layout.addWidget(self.txt_ayak_min)
        range_ayak_layout.addWidget(self.txt_ayak_max)
        grid_layout.addLayout(range_ayak_layout, 3, 1)

        grid_layout.addWidget(QLabel("Kilo (Min-Max):"), 3, 2)
        range_kilo_layout = QHBoxLayout()
        self.sb_kilo_min = QSpinBox()
        self.sb_kilo_min.setRange(0, 300)
        self.sb_kilo_min.setValue(0)
        self.sb_kilo_max = QSpinBox()
        self.sb_kilo_max.setRange(0, 300)
        self.sb_kilo_max.setValue(300)
        range_kilo_layout.addWidget(self.sb_kilo_min)
        range_kilo_layout.addWidget(self.sb_kilo_max)
        grid_layout.addLayout(range_kilo_layout, 3, 3)

        grid_layout.addWidget(QLabel("Suç Kaydı:"), 3, 4)
        self.cmb_suc_id = QComboBox()
        self.cmb_suc_id.addItem("Seçiniz...")
        grid_layout.addWidget(self.cmb_suc_id, 3, 5)

        grid_layout.addWidget(QLabel("Bulunduğu Şehir (Plaka):"), 4, 0)
        self.cmb_plaka = QComboBox()
        self.cmb_plaka.addItem("Seçiniz...")
        grid_layout.addWidget(self.cmb_plaka, 4, 1)

        grid_layout.addWidget(QLabel("Kan Grubu:"), 4, 2)
        self.cmb_kan_id = QComboBox()
        self.cmb_kan_id.addItem("Seçiniz...")
        grid_layout.addWidget(self.cmb_kan_id, 4, 3)

        scroll.setWidget(scroll_widget)
        sol_layout.addWidget(scroll)

        # --- ARAMA BUTONLARI (YAN YANA) ---
        buton_layout = QHBoxLayout()

        self.btn_ara = QPushButton("Tüm Kriterlere Göre Zanlı Ara")
        self.btn_ara.setStyleSheet("background-color: #2b5797; color: white; font-weight: bold; padding: 8px;")
        self.btn_ara.clicked.connect(self.arama_yap)
        buton_layout.addWidget(self.btn_ara, stretch=3)

        self.btn_ara_temizle = QPushButton("Arama Filtrelerini Temizle")
        self.btn_ara_temizle.setStyleSheet("background-color: #555555; color: white; font-weight: bold; padding: 8px;")
        self.btn_ara_temizle.clicked.connect(self.arama_formunu_temizle)
        buton_layout.addWidget(self.btn_ara_temizle, stretch=1)

        sol_layout.addLayout(buton_layout)

        self.table = QTableWidget()
        self.headers = [
            "Tc_Kimlik", "Ad", "Soyad", "Göz_Rengi_Id", "Dogum_Yılı",
            "Boy", "Parmak_İzi", "Belirgin_Özellik", "Dna", "Ayak_Numarası",
            "Kilo", "Suç_Kaydı_Id", "Plaka", "Kan_Grubu_Id"
        ]
        self.table.setColumnCount(len(self.headers))
        self.table.setHorizontalHeaderLabels(self.headers)
        self.table.itemDoubleClicked.connect(self.tablodan_forma_tasina)
        sol_layout.addWidget(self.table)

        layout_yatay.addWidget(sol_panel, stretch=3)

        # --- SAĞ TARAF (ZANLI VERİ YÖNETİM PANELİ) ---
        sag_panel = QWidget()
        sag_panel.setStyleSheet("background-color: #f3f3f3; border-left: 2px solid #ccc; padding: 5px;")
        sag_layout = QVBoxLayout(sag_panel)

        baslik_ekle = QLabel("ZANLI VERİ İŞLEM PANELİ")
        baslik_ekle.setStyleSheet("font-weight: bold; font-size: 14px; color: #1e3a8a; margin-bottom: 10px;")
        baslik_ekle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sag_layout.addWidget(baslik_ekle)

        ekle_scroll = QScrollArea()
        ekle_scroll.setWidgetResizable(True)
        ekle_scroll_widget = QWidget()
        ekle_grid = QGridLayout(ekle_scroll_widget)

        ekle_grid.addWidget(QLabel("TC Kimlik NO (*):"), 0, 0)
        self.txt_ekle_tc = QLineEdit()
        self.txt_ekle_tc.setMaxLength(11)
        ekle_grid.addWidget(self.txt_ekle_tc, 0, 1)

        ekle_grid.addWidget(QLabel("Adı (*):"), 1, 0)
        self.txt_ekle_ad = QLineEdit()
        ekle_grid.addWidget(self.txt_ekle_ad, 1, 1)

        ekle_grid.addWidget(QLabel("Soyadı (*):"), 2, 0)
        self.txt_ekle_soyad = QLineEdit()
        ekle_grid.addWidget(self.txt_ekle_soyad, 2, 1)

        ekle_grid.addWidget(QLabel("Doğum Yılı:"), 3, 0)
        self.sb_ekle_yil = QSpinBox()
        self.sb_ekle_yil.setRange(1900, 2026)
        self.sb_ekle_yil.setValue(1990)
        ekle_grid.addWidget(self.sb_ekle_yil, 3, 1)

        ekle_grid.addWidget(QLabel("Boy (cm):"), 4, 0)
        self.sb_ekle_boy = QSpinBox()
        self.sb_ekle_boy.setRange(0, 250)
        self.sb_ekle_boy.setValue(170)
        ekle_grid.addWidget(self.sb_ekle_boy, 4, 1)

        ekle_grid.addWidget(QLabel("Kilo (kg):"), 5, 0)
        self.sb_ekle_kilo = QSpinBox()
        self.sb_ekle_kilo.setRange(0, 300)
        self.sb_ekle_kilo.setValue(70)
        ekle_grid.addWidget(self.sb_ekle_kilo, 5, 1)

        ekle_grid.addWidget(QLabel("Ayak Numarası:"), 6, 0)
        self.sb_ekle_ayak = QSpinBox()
        self.sb_ekle_ayak.setRange(0, 60)
        self.sb_ekle_ayak.setValue(42)
        ekle_grid.addWidget(self.sb_ekle_ayak, 6, 1)

        ekle_grid.addWidget(QLabel("Göz Rengi:"), 7, 0)
        self.cmb_ekle_goz_rengi = QComboBox()
        self.cmb_ekle_goz_rengi.addItem("Seçiniz...")
        ekle_grid.addWidget(self.cmb_ekle_goz_rengi, 7, 1)

        ekle_grid.addWidget(QLabel("Bulunduğu Şehir:"), 8, 0)
        self.cmb_ekle_plaka = QComboBox()
        self.cmb_ekle_plaka.addItem("Seçiniz...")
        ekle_grid.addWidget(self.cmb_ekle_plaka, 8, 1)

        ekle_grid.addWidget(QLabel("Suç Kaydı:"), 9, 0)
        self.cmb_ekle_suc_id = QComboBox()
        self.cmb_ekle_suc_id.addItem("Seçiniz...")
        ekle_grid.addWidget(self.cmb_ekle_suc_id, 9, 1)

        ekle_grid.addWidget(QLabel("Kan Grubu:"), 10, 0)
        self.cmb_ekle_kan_id = QComboBox()
        self.cmb_ekle_kan_id.addItem("Seçiniz...")
        ekle_grid.addWidget(self.cmb_ekle_kan_id, 10, 1)

        ekle_grid.addWidget(QLabel("Parmak İzi Kodu:"), 11, 0)
        self.txt_ekle_parmak = QLineEdit()
        ekle_grid.addWidget(self.txt_ekle_parmak, 11, 1)

        ekle_grid.addWidget(QLabel("DNA Kodu:"), 12, 0)
        self.txt_ekle_dna = QLineEdit()
        ekle_grid.addWidget(self.txt_ekle_dna, 12, 1)

        ekle_grid.addWidget(QLabel("Belirgin Özellik:"), 13, 0)
        self.txt_ekle_ozellik = QLineEdit()
        ekle_grid.addWidget(self.txt_ekle_ozellik, 13, 1)

        ekle_scroll.setWidget(ekle_scroll_widget)
        sag_layout.addWidget(ekle_scroll)

        # --- BUTONLAR (CRUD İŞLEMLERİ) ---
        self.btn_ekle = QPushButton("Yeni Zanlı Kaydı Ekle")
        self.btn_ekle.setStyleSheet("background-color: #107c41; color: white; font-weight: bold; padding: 8px;")
        self.btn_ekle.clicked.connect(self.kayit_ekle)
        sag_layout.addWidget(self.btn_ekle)

        self.btn_guncelle = QPushButton("Seçili Kaydı Güncelle")
        self.btn_guncelle.setStyleSheet("background-color: #d83b01; color: white; font-weight: bold; padding: 8px;")
        self.btn_guncelle.clicked.connect(self.kayit_guncelle)
        sag_layout.addWidget(self.btn_guncelle)

        self.btn_sil = QPushButton("Seçili Kaydı SİL")
        self.btn_sil.setStyleSheet("background-color: #a80000; color: white; font-weight: bold; padding: 8px;")
        self.btn_sil.clicked.connect(self.kayit_sil)
        sag_layout.addWidget(self.btn_sil)

        layout_yatay.addWidget(sag_panel, stretch=1)

    def arama_yap(self):
        try:
            # Yeni tasarımda char/varchar olan sayısal alanlar için TRY_CAST dönüşümleri eklendi
            query = """
                SELECT Tc_Kimlik, Ad, Soyad, Göz_Rengi_Id, Dogum_Yılı, 
                       Boy, Parmak_İzi, Belirgin_Özellik, Dna, Ayak_Numarası, 
                       Kilo, Suç_Kaydı_Id, Plaka, Kan_Grubu_Id 
                FROM dbo.Zanli_Profil 
                WHERE (TRY_CAST(REPLACE(Dogum_Yılı, CHAR(13), '') AS INT) BETWEEN ? AND ?)
                  AND (TRY_CAST(REPLACE(Boy, CHAR(13), '') AS INT) BETWEEN ? AND ?)
                  AND (TRY_CAST(REPLACE(Kilo, CHAR(13), '') AS INT) BETWEEN ? AND ?)
                  AND (TRY_CAST(REPLACE(Ayak_Numarası, CHAR(13), '') AS INT) BETWEEN ? AND ?)
            """
            params = [
                self.sb_yil_min.value(), self.sb_yil_max.value(),
                self.sb_boy_min.value(), self.sb_boy_max.value(),
                self.sb_kilo_min.value(), self.sb_kilo_max.value(),
                self.txt_ayak_min.value(), self.txt_ayak_max.value()
            ]

            text_filters = [
                ("Tc_Kimlik", self.txt_tc.text().strip()),
                ("Ad", self.txt_ad.text().strip()),
                ("Soyad", self.txt_soyad.text().strip()),
                ("Parmak_İzi", self.txt_parmak_izi.text().strip()),
                ("Belirgin_Özellik", self.txt_ozellik.text().strip()),
                ("Dna", self.txt_dna.text().strip())
            ]

            for column, value in text_filters:
                if value:
                    query += f" AND {column} LIKE ?"
                    params.append(f"%{value}%")

            goz_id = self.goz_rengi_sozlugu.get(self.cmb_goz_rengi.currentText(), "")
            if goz_id != "":
                query += " AND REPLACE(Göz_Rengi_Id, CHAR(13), '') = ?"
                params.append(goz_id)

            sehir_id = self.sehir_sozlugu.get(self.cmb_plaka.currentText(), "")
            if sehir_id != "":
                query += " AND REPLACE(Plaka, CHAR(13), '') = ?"
                params.append(sehir_id)

            suc_id = self.suc_sozlugu.get(self.cmb_suc_id.currentText(), "")
            if suc_id != "":
                query += " AND REPLACE(Suç_Kaydı_Id, CHAR(13), '') = ?"
                params.append(suc_id)

            kan_id = self.kan_sozlugu.get(self.cmb_kan_id.currentText(), "")
            if kan_id != "":
                query += " AND REPLACE(Kan_Grubu_Id, CHAR(13), '') = ?"
                params.append(kan_id)

            self.cursor.execute(query, params)
            rows = self.cursor.fetchall()

            self.table.setRowCount(0)
            for row_idx, row_data in enumerate(rows):
                self.table.insertRow(row_idx)
                for col_idx, value in enumerate(row_data):
                    val_str = str(value).replace('\r', '').strip() if value is not None else ""
                    item = QTableWidgetItem(val_str)
                    item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)
                    self.table.setItem(row_idx, col_idx, item)

            if not rows:
                QMessageBox.information(self, "Bilgi", "Aranan kriterlere uyan hiçbir kayıt bulunamadı.")

        except Exception as e:
            QMessageBox.critical(self, "Sorgu Hatası", f"Veritabanı araması esnasında teknik hata meydana geldi:\n{e}")

    def tablodan_forma_tasina(self, item):
        row = item.row()

        self.txt_ekle_tc.setText(self.table.item(row, 0).text())
        self.txt_ekle_ad.setText(self.table.item(row, 1).text())
        self.txt_ekle_soyad.setText(self.table.item(row, 2).text())

        # Karakter tabanlı verileri güvenle sayısal SpinBox'lara aktarma
        self.sb_ekle_yil.setValue(
            int(self.table.item(row, 4).text()) if self.table.item(row, 4).text().isdigit() else 1990)
        self.sb_ekle_boy.setValue(
            int(self.table.item(row, 5).text()) if self.table.item(row, 5).text().isdigit() else 0)
        self.sb_ekle_kilo.setValue(
            int(self.table.item(row, 10).text()) if self.table.item(row, 10).text().isdigit() else 0)
        self.sb_ekle_ayak.setValue(
            int(self.table.item(row, 9).text()) if self.table.item(row, 9).text().isdigit() else 0)

        self.txt_ekle_parmak.setText(self.table.item(row, 6).text())
        self.txt_ekle_ozellik.setText(self.table.item(row, 7).text())
        self.txt_ekle_dna.setText(self.table.item(row, 8).text())

        # ComboBox'ları metinsel ID'lere (char/varchar) göre eşitleme
        self.cmb_ekle_goz_rengi.setCurrentText(
            next((k for k, v in self.goz_rengi_sozlugu.items() if v == self.table.item(row, 3).text()), "Seçiniz..."))

        self.cmb_ekle_plaka.setCurrentText(
            next((k for k, v in self.sehir_sozlugu.items() if v == self.table.item(row, 12).text()), "Seçiniz..."))

        self.cmb_ekle_suc_id.setCurrentText(
            next((k for k, v in self.suc_sozlugu.items() if v == self.table.item(row, 11).text()), "Seçiniz..."))

        self.cmb_ekle_kan_id.setCurrentText(
            next((k for k, v in self.kan_sozlugu.items() if v == self.table.item(row, 13).text()), "Seçiniz..."))

    def form_verilerini_topla(self):
        tc = self.txt_ekle_tc.text().strip()
        ad = self.txt_ekle_ad.text().strip()
        soyad = self.txt_ekle_soyad.text().strip()

        if not tc or not ad or not soyad:
            return None

        goz_id = self.goz_rengi_sozlugu.get(self.cmb_ekle_goz_rengi.currentText(), "")
        sehir_id = self.sehir_sozlugu.get(self.cmb_ekle_plaka.currentText(), "")
        suc_id = self.suc_sozlugu.get(self.cmb_ekle_suc_id.currentText(), "")
        kan_id = self.kan_sozlugu.get(self.cmb_ekle_kan_id.currentText(), "")

        # Veritabanının yeni char boyut sınırlarına ve türlerine göre string dönüşümleri
        return {
            "tc": tc, "ad": ad, "soyad": soyad,
            "yil": str(self.sb_ekle_yil.value()),  # char(4)
            "boy": str(self.sb_ekle_boy.value()),  # char(3)
            "kilo": str(self.sb_ekle_kilo.value()),  # char(2)
            "ayak": str(self.sb_ekle_ayak.value()),  # char(2)
            "goz_id": goz_id if goz_id != "" else None,
            "sehir_id": sehir_id if sehir_id != "" else None,
            "suc_id": suc_id if suc_id != "" else None,
            "kan_id": kan_id if kan_id != "" else None,
            "parmak": self.txt_ekle_parmak.text().strip() or None,
            "dna": self.txt_ekle_dna.text().strip() or None,
            "ozellik": self.txt_ekle_ozellik.text().strip() or None
        }

    def kayit_ekle(self):
        try:
            data = self.form_verilerini_topla()
            if not data:
                QMessageBox.warning(self, "Eksik Bilgi", "Lütfen TC, Ad ve Soyad alanlarını doldurun.")
                return

            query = """
                INSERT INTO dbo.Zanli_Profil 
                (Tc_Kimlik, Ad, Soyad, Göz_Rengi_Id, Dogum_Yılı, Boy, Parmak_İzi, Belirgin_Özellik, Dna, Ayak_Numarası, Kilo, Suç_Kaydı_Id, Plaka, Kan_Grubu_Id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            self.cursor.execute(query, [
                data["tc"], data["ad"], data["soyad"], data["goz_id"], data["yil"], data["boy"],
                data["parmak"], data["ozellik"], data["dna"], data["ayak"], data["kilo"], data["suc_id"],
                data["sehir_id"], data["kan_id"]
            ])
            self.conn.commit()
            QMessageBox.information(self, "Başarılı", f"{data['ad']} {data['soyad']} başarıyla eklendi.")
            self.formu_temizle()
            self.arama_yap()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Kayıt eklenemedi:\n{e}")

    def kayit_guncelle(self):
        try:
            data = self.form_verilerini_topla()
            if not data:
                QMessageBox.warning(self, "Seçim Yok", "Lütfen güncellemek istediğiniz kayda tablodan çift tıklayın.")
                return

            onay = QMessageBox.question(self, "Güncelleme Onayı",
                                        f"{data['tc']} kimlik numaralı zanlının verilerini güncellemek istediğinize emin misiniz?",
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if onay == QMessageBox.StandardButton.No:
                return

            query = """
                UPDATE dbo.Zanli_Profil SET 
                    Ad = ?, Soyad = ?, Göz_Rengi_Id = ?, Dogum_Yılı = ?, Boy = ?, 
                    Parmak_İzi = ?, Belirgin_Özellik = ?, Dna = ?, Ayak_Numarası = ?, 
                    Kilo = ?, Suç_Kaydı_Id = ?, Plaka = ?, Kan_Grubu_Id = ?
                WHERE Tc_Kimlik = ?
            """
            self.cursor.execute(query, [
                data["ad"], data["soyad"], data["goz_id"], data["yil"], data["boy"],
                data["parmak"], data["ozellik"], data["dna"], data["ayak"], data["kilo"],
                data["suc_id"], data["sehir_id"], data["kan_id"], data["tc"]
            ])
            self.conn.commit()
            QMessageBox.information(self, "Başarılı", "Zanlı bilgileri başarıyla güncellendi.")
            self.formu_temizle()
            self.arama_yap()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Güncelleme başarısız:\n{e}")

    def kayit_sil(self):
        tc = self.txt_ekle_tc.text().strip()
        if not tc:
            QMessageBox.warning(self, "Seçim Yok", "Lütfen silmek istediğiniz kayda tablodan çift tıklayın.")
            return

        onay = QMessageBox.question(self, "SİLME ONAYI",
                                    f"TC: {tc} olan zanlıyı veritabanından KALICI olarak silmek istiyor musunuz?\nBu işlem geri alınamaz!",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if onay == QMessageBox.StandardButton.No:
            return

        try:
            self.cursor.execute("DELETE FROM dbo.Zanli_Profil WHERE Tc_Kimlik = ?", (tc,))
            self.conn.commit()
            QMessageBox.information(self, "Silindi", "Zanlı kaydı sistemden kalıcı olarak silindi.")
            self.formu_temizle()
            self.arama_yap()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Silme işlemi başarısız:\n{e}")

    def arama_formunu_temizle(self):
        self.txt_tc.clear()
        self.txt_ad.clear()
        self.txt_soyad.clear()
        self.txt_parmak_izi.clear()
        self.txt_ozellik.clear()
        self.txt_dna.clear()

        self.sb_yil_min.setValue(1900)
        self.sb_yil_max.setValue(2026)
        self.sb_boy_min.setValue(0)
        self.sb_boy_max.setValue(250)
        self.sb_kilo_min.setValue(0)
        self.sb_kilo_max.setValue(300)
        self.txt_ayak_min.setValue(0)
        self.txt_ayak_max.setValue(60)

        self.cmb_goz_rengi.setCurrentIndex(0)
        self.cmb_plaka.setCurrentIndex(0)
        self.cmb_suc_id.setCurrentIndex(0)
        self.cmb_kan_id.setCurrentIndex(0)

    def formu_temizle(self):
        self.txt_ekle_tc.clear()
        self.txt_ekle_ad.clear()
        self.txt_ekle_soyad.clear()
        self.txt_ekle_parmak.clear()
        self.txt_ekle_dna.clear()
        self.txt_ekle_ozellik.clear()
        self.cmb_ekle_goz_rengi.setCurrentIndex(0)
        self.cmb_ekle_plaka.setCurrentIndex(0)
        self.cmb_ekle_suc_id.setCurrentIndex(0)
        self.cmb_ekle_kan_id.setCurrentIndex(0)

    def closeEvent(self, event):
        try:
            self.conn.close()
        except:
            pass
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = TumZanliAramaUygulamasi()
    pencere.show()
    sys.exit(app.exec()) 