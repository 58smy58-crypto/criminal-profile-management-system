# 📊 1 Milyon Kayıtlı Suçlu Profili Detaylı Yönetim Sistemi (CRUD)


Bu proje; **Büyük Veri (Big Data)** mimarilerinde veri tabanı indeksleme, normalizasyon ve performans optimizasyonu süreçleri ile gelişmiş masaüstü arayüz yönetimini bir araya getirmek amacıyla geliştirilmiştir. 
**1 milyondan fazla** benzersiz zanlı kaydı barındıran ilişkisel bir SQL Server veritabanını, Python (PyQt6) tabanlı dinamik filtreleme paneliyle milisaniyeler seviyesinde yönetir.

---

## 📐 Veritabanı Normalizasyonu (Database Normalization)

Projenin ilk aşamalarında tüm verilerin tek bir devasa tabloda tutulması; hem ciddi bir veri tekrarına (redundancy) sebep oluyor, 
hem de 1 milyon kayıt altındaki arama ve güncelleme performansını olumsuz etkiliyordu. Bu sorunu çözmek için veritabanı mimarisi normalize edilerek ilişkisel (Relational) hale getirilmiştir:

### ❌ Normalizasyon Öncesi (Veri Tekrarı Riski)
Normalizasyon yapılmadan önce, her zanlı kaydının yanına tekrar tekrar `"Cinayet"`, `"Uyuşturucu Ticareti"`, `"Gasp"` gibi uzun metinler veya `"Adana"`, `"Afyonkarahisar"` 
gibi şehir isimleri string (metin) olarak yazılıyordu. Bu durum diskte gereksiz devasa bir yer kaplıyor ve indekslemeyi yavaşlatıyordu.
<img width="434" height="420" alt="Eski_Kayıt_Tasarım" src="https://github.com/user-attachments/assets/28b4dfa4-e80b-41b7-a309-bf12f2c638be" />
<img width="1439" height="884" alt="Eski_Kayıtlar" src="https://github.com/user-attachments/assets/d43b8396-efa2-4b77-9572-c48e2e86ecdf" />



###  Normalizasyon Sonrası (Modüler ve Performanslı Yapı)
Sistem optimize edilerek metinsel veriler kendi sözlük (dictionary) tablolarına taşınmış ve ana tabloya sadece `int` veya `varchar(10)` tipinde hafif ID'ler (Foreign Key) bağlanmıştır. 
<img width="1388" height="858" alt="KayıtÖrnek" src="https://github.com/user-attachments/assets/95bf15e5-247e-4f84-985e-13548bf64cc9" />
<img width="399" height="415" alt="Kayıt_Tasarım" src="https://github.com/user-attachments/assets/324e1826-8d73-4594-80d9-18f602a25b20" />

* **Veritabanı Ağaç Şeması:** Normalizasyon sonrası ana tablo ile sözlük tablolarının (`dbo.Sehirler`, `dbo.Suc_Kayitlari`) SQL Server üzerindeki modüler dizilimi:
<img width="633" height="899" alt="Nesne_Gezgini" src="https://github.com/user-attachments/assets/d456efe3-6ac7-44a1-ab53-bdbaf1d9d7d6" />


* **Suç Türleri Sözlüğü (`dbo.Suc_Kayitlari`):** Metinsel suç tanımları tek bir yerde toplanarak ID'ye indirgendi. Ana tabloda sadece bu ID'ler (C, D, ES vb.) tutularak bellek optimizasyonu sağlandı:
<img width="688" height="323" alt="SuçKayıtları" src="https://github.com/user-attachments/assets/3bec8d46-0712-422f-bafb-a99a79d8506f" />


* **Şehir Verileri Sözlüğü (`dbo.Sehirler`):** Şehir isimlerinin kaplayacağı alan, 1'den 81'e kadar olan `int` plaka kodlarıyla optimize edildi:
<img width="671" height="599" alt="Şehirler" src="https://github.com/user-attachments/assets/fb473b6f-0309-4115-b2a9-be240a6c1eea" />


Bu sayede 1 milyon kayıtlık ana tablo (`Zanli_Profil`) inanılmaz derecede hafifletilmiş, disk alanından maksimum tasarruf sağlanmış ve indekslerin RAM üzerinde çok daha hızlı çalışması tetiklenmiştir.

---

## ⚡ Öne Çıkan Teknik Mühendislik (Milisaniyelik Sorgular)

Büyük veri setlerinde en büyük problem veri ararken yaşanan gecikmeler ve yeni veri eklenirken veritabanının kilitlenmesidir. Projede bu iki problem mimari düzeyde çözülmüştür:

* **🎯 Stratejik Kümelenmemiş Dizinler (Non-Clustered Indexes):** T.C. Kimlik No, Ad-Soyad, Parmak İzi ve DNA Kodu gibi sık sorgulanan alanlar için `Index_1`'den `Index_8`'e kadar özel dizin ağaçları oluşturulmuştur.
* **🚀 %70 Fill Factor (Doluluk Oranı) Optimizasyonu:** Dizin yaprak sayfalarında (Leaf Nodes) **%30 boşluk** bırakılmıştır. Bu sayede, uygulamadan **yeni suçlu kaydı eklendiğinde** veya
* güncellemeler yapıldığında SQL Server sayfa bölünmesi (Page Split) yaşamaz. Sistem, yeni kayıtlarda hata vermeden ve yazma performansından ödün vermeden kararlı şekilde çalışmaya devam eder.

---

## 🎨 Gelişmiş PyQt6 Kullanıcı Arayüzü

### 1. Uygulama Genel Arayüzü (Boş Durum)
Uygulama ilk açıldığında kullanıcıyı karşılayan temiz, modern ve kullanıcı dostu arayüz. Sol tarafta çoklu varyasyonlara izin veren gelişmiş filtreleme alanları, 
sağ tarafta ise CRUD (Ekle/Güncelle/Sil) operasyonlarının yönetildiği işlem paneli yer alır.

<img width="1919" height="1031" alt="Uygulama" src="https://github.com/user-attachments/assets/59a3b7d5-f3bc-4699-bb33-7b9657a077c3" />


### 🔍 2. 1 Milyon Veri Arasından Canlı Filtreleme & CRUD Dinamiği
Çoklu kriterler (Doğum yılı aralığı, boy-kilo limitleri, fiziksel özellikler ve lokasyon) girilerek 1 milyon veri arasından yapılan milisaniyelik filtreleme sonucu ve sağ taraftaki veri işlem panelinin aktif kullanımı:

<img width="1919" height="1027" alt="Örnek" src="https://github.com/user-attachments/assets/1bd0a036-0621-4057-9679-23b587bcb14e" />


---

## 💾 Veri Besleme (Data Seeding) & BULK INSERT Operasyonları

Milyonlarca veriyi lokal ortamda sıfırdan ve en hızlı şekilde ayağa kaldırmak için yazılan optimize SQL betikleri:

* **Şehir Verilerinin Text Dosyasından Aktarılması:**
<img width="934" height="206" alt="Sehir_Ekleme_Text_Dosayasından" src="https://github.com/user-attachments/assets/f628c106-c64a-42d4-88d1-48ceae81b36f" />


* **1 Milyon Kaydın CSV'den Performanslı Aktarımı:**
    Büyük veri aktarımında Türkçe karakter kaybı yaşanmaması için `CODEPAGE = '65001'` (UTF-8) kullanılmış; satır sonlarının kararlı ayrıştırılması için `ROWTERMINATOR = '0x0a'` (hex kodu) tercih edilmiştir.
<img width="872" height="254" alt="1_Mliyon_Veri_Ekleme_Kodu" src="https://github.com/user-attachments/assets/8689ba28-194b-4646-80e6-88cc094a76fb" />


---

## 🛠️ Kurulum, Veri Üretimi ve Çalıştırma (Adım Adım)

Uygulamayı lokal ortamınızda 1 milyon kayıtla birlikte eksiksiz çalıştırmak için aşağıdaki adımları sırasıyla takip edin:
Txt dosyasındaki 1 milyon kayıt oluşturma kodunu çalıştır oluşan cvs dosyasını sql e resimdeki gibi yazdır sonra Python proje uygulamasını çalıştır.
### 1. Depoyu Klonlayın ve Bağımlılıkları Kurun
```bash
# Projeyi bilgisayarınıza indirin
git clone [https://github.com/kullanici_adi/criminal-profile-management-system.git](https://github.com/kullanici_adi/criminal-profile-management-system.git)
cd criminal-profile-management-system

# Gerekli Python kütüphanelerini yükleyin
pip install PyQt6 pyodbc
