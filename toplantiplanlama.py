import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import json
from PIL import Image, ImageTk
import datetime


class ToplantiUygulamasi:
    def __init__(self, master):
        self.master = master
        self.master.title("Toplanti Uygulamasi")
        self.master.geometry("1000x750")
        self.master.configure(bg='#F5DEB3')  

        self.label_isim = tk.Label(master, text="İsim:", bg='#F5DEB3', font=("Arial", 12), fg='black')  
        self.label_tarih = tk.Label(master, text="Toplantı Tarihi:", bg='#F5DEB3', font=("Arial", 12), fg='black')  
        self.label_aciklama = tk.Label(master, text="Açıklama:", bg='#F5DEB3', font=("Arial", 12), fg='black')  

        self.entry_isim = tk.Entry(master)
        self.entry_tarih = DateEntry(master, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.entry_aciklama = tk.Entry(master)

        self.button_toplanti_olustur = tk.Button(master, text="TOPLANTIYI OLUŞTUR", command=self.toplantiyi_olustur, bg='green', fg='white', font=("Arial", 12))
        # Toplantiya katilma
        self.label_katilma_kodu = tk.Label(master, text="Toplanti Kodu:", bg='#F5DEB3', font=("Arial", 12), fg='black')  
        self.label_katilma_isim = tk.Label(master, text="İsim:", bg='#F5DEB3', font=("Arial", 12), fg='black')  
        self.label_katilma_tarih = tk.Label(master, text="Uygun Tarih:", bg='#F5DEB3', font=("Arial", 12), fg='black')  

        self.entry_katilma_kodu = tk.Entry(master)
        self.entry_katilma_isim = tk.Entry(master)
        self.entry_katilma_tarih = DateEntry(master, width=12, background='darkblue', foreground='white', borderwidth=2)

        self.button_toplantiya_katil = tk.Button(master, text="TOPLANTIYA KATIL", command=self.toplantiya_katil, bg='green', fg='white', font=("Arial", 12))  # Yeşil renk

        # Grid
        self.grid_label = tk.Label(master, text="TOPLANTILAR:", bg='#F5DEB3', font=("Arial", 12, "bold"))  
        self.grid_tree = ttk.Treeview(master, columns=("Toplanti Kodu", "Isim", "Tarih", "Aciklama", "Katilimci"), show="headings")


        self.label_isim.grid(row=0, column=0, padx=10, pady=10)
        self.label_tarih.grid(row=1, column=0, padx=10, pady=10)
        self.label_aciklama.grid(row=2, column=0, padx=10, pady=10)

        self.entry_isim.grid(row=0, column=1, padx=10, pady=10)
        self.entry_tarih.grid(row=1, column=1, padx=10, pady=10)
        self.entry_aciklama.grid(row=2, column=1, padx=10, pady=10)

        self.button_toplanti_olustur.grid(row=4, column=0, columnspan=2, pady=10)

        self.label_katilma_kodu.grid(row=0, column=2, padx=10, pady=10)
        self.label_katilma_isim.grid(row=1, column=2, padx=10, pady=10)
        self.label_katilma_tarih.grid(row=2, column=2, padx=10, pady=10)

        self.entry_katilma_kodu.grid(row=0, column=3, padx=10, pady=10)
        self.entry_katilma_isim.grid(row=1, column=3, padx=10, pady=10)
        self.entry_katilma_tarih.grid(row=2, column=3, padx=10, pady=10)

        self.button_toplantiya_katil.grid(row=4, column=2, columnspan=2, pady=10)

        self.grid_label.grid(row=5, column=0, padx=10, pady=10, columnspan=5)
        self.grid_tree.grid(row=6, column=0, columnspan=5)

        #kolon başlıkları
        self.grid_tree.heading("Toplanti Kodu", text="Toplanti Kodu")
        self.grid_tree.heading("Isim", text="Isim")
        self.grid_tree.heading("Tarih", text="Tarih")
        self.grid_tree.heading("Aciklama", text="Aciklama")
        self.grid_tree.heading("Katilimci", text="Katilimci")
        # Çift tıklandığı zaman tplantı detay bilgisi
        self.grid_tree.bind("<Double-1>", self.detay_goster)

        # JSON dosyası için dosya adı
        self.json_filename = "toplanti_verileri.json"
        self.json_filename_fifth = "json_filename_fifth.json"

        # JSON dosyasından daha önce olusturulan toplantı bilgilerini yükle
        self.load_data()
        self.load_data_kolon()

        self.grid_tree_katilanlar = ttk.Treeview(master, columns=("Toplanti Kodu", "Isim", "Tarih"), show="headings")

        self.grid_label_katilanlar = tk.Label(master, text="TOPLANTI TARİHİNDE UYGUN OLMAYAN KATILIMCILAR VE UYGUN ZAMANLARI:", bg='#F5DEB3', font=("Arial", 12, "bold"))  

        self.grid_label_katilanlar.grid(row=7, column=0, padx=10, pady=10, columnspan=4)
        self.grid_tree_katilanlar.grid(row=8, column=0, columnspan=4)

        #katılımcı başlıkları
        self.grid_tree_katilanlar.heading("Toplanti Kodu", text="Toplanti Kodu")
        self.grid_tree_katilanlar.heading("Isim", text="Isim")
        self.grid_tree_katilanlar.heading("Tarih", text="Tarih")
        self.grid_tree_katilanlar.bind("<Double-1>", self.detay_goster_katilanlar)

        self.json_filename_katilimci = "katilimci.json"
        self.load_data_katilimci()

    def toplantiyi_olustur(self):
        toplanti_kodu = self.toplanti_kodu_olusturma()
        isim = self.entry_isim.get()
        tarih = self.entry_tarih.get_date()
        aciklama = self.entry_aciklama.get()

        if toplanti_kodu and isim and tarih and aciklama:
            messagebox.showinfo("Toplanti Oluşturuldu", f"Toplanti Kodu: {toplanti_kodu}\nIsim: {isim}\nTarih: {tarih}\nAciklama: {aciklama}")
            self.toplanti_satirlari_ekle((toplanti_kodu, isim, tarih, aciklama))
            # Verileri JSON dosyasına kaydet
            self.save_data()
        else:
            messagebox.showerror("Hata", "Eksik bilgi girdiniz. Lütfen gerekli tüm bilgileri girin.")

    def toplanti_kodu_olusturma(self):
        # Şu anki tarihi ve rastgele karakterleri kullanarak bir toplantı kodu oluşturma
        current_date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{current_date}"


    def toplantiya_katil(self):
        toplanti_kodu = self.entry_katilma_kodu.get()
        isim = self.entry_katilma_isim.get()
        uygun_tarih = self.entry_katilma_tarih.get_date()

        found = False
        for item in self.grid_tree.get_children():
            values = self.grid_tree.item(item, "values")
            if values[0] == toplanti_kodu:
                found = True
                toplanti_index = item
                break

        if found:
            # Toplantıyı bulduk, şimdi uygun tarih kontrolü yapalım
            toplanti_tarihi_str = values[2]
            toplanti_tarihi = datetime.datetime.strptime(toplanti_tarihi_str, "%Y-%m-%d").date()

            if uygun_tarih == toplanti_tarihi:
                existing_attendees = values[4] if len(values) > 4 else ""  # Daha önce katılanları al

                # Yeni katılımcının uygun olduğu saatte daha önce katılan var mı kontrol et
                if isim in existing_attendees:
                    messagebox.showinfo("Toplantiya Katilma", f"{isim} zaten toplantıda.")
                else:
                    messagebox.showinfo("Toplantiya Katilma", f"Toplanti Kodu: {toplanti_kodu}, Isim: {isim}, Uygun Tarih: {uygun_tarih}")

                    # Verilen toplantının katılımcıları sütununa yeni katılımcının ismini ve daha önce katılanın ismini ekleyelim
                    new_attendees = f"{existing_attendees}, {isim}" if existing_attendees else isim
                    self.grid_tree.set(toplanti_index, column="Katilimci", value=new_attendees)

                    # JSON dosyasına katılımcı bilgisini kaydet
                    self.save_data()
                    self.save_data_kolon()
            else:
                self.farkli_tarihte_katilanlar_satirlari_ekle((toplanti_kodu, f"{isim}", f"{uygun_tarih}"))
                # Verileri JSON dosyasına kaydet
                self.save_data_katilimci()
        else:
            messagebox.showerror("Hata", "Böyle bir toplantı bulunmamaktadır! Toplantı kodunu yanlış veya eksik girdiniz.")


    def detay_goster(self, event):
        selected_item = self.grid_tree.selection()
        values = self.grid_tree.item(selected_item, "values")
        if values and len(values) == 4:
            toplanti_kodu, isim, tarih, aciklama = values
            messagebox.showinfo("Toplanti Detaylari", f"Toplanti Kodu: {toplanti_kodu}\nIsim: {isim}\nTarih: {tarih}\nAciklama: {aciklama}")
        elif values and len(values) == 5:
            toplanti_kodu, isim, tarih, aciklama, Katilimci = values
            messagebox.showinfo("Toplanti Detaylari", f"Toplanti Kodu: {toplanti_kodu}\nIsim: {isim}\nTarih: {tarih}\nAciklama: {aciklama}\nKatilimci: {Katilimci}")            
   
    def detay_goster_katilanlar(self, event):
        selected_item = self.grid_tree_katilanlar.selection()
        values = self.grid_tree_katilanlar.item(selected_item, "values")
        if values:
            toplanti_kodu, isim, tarih = values
            messagebox.showinfo("Toplanti Detaylari", f"Toplanti Kodu: {toplanti_kodu}\nIsim: {isim}\nTarih: {tarih}")          

    def toplanti_satirlari_ekle(self, values):
        # Uzun aciklama kontrolu
        aciklama = values[3]
        if len(aciklama) > 28:
            aciklama = aciklama[:28] + "..."
        values = (values[0], values[1], values[2], aciklama)
        
        self.grid_tree.insert("", "end", values=values)
        
    def farkli_tarihte_katilanlar_satirlari_ekle(self, values):
        self.grid_tree_katilanlar.insert("", "end", values=values)
        
    def katilanlar_satirlari_ekle(self, row_index, value):
        item_id = self.grid_tree.get_children()[row_index]  # İlgili satırın ID'sini alır
        if len(value) > 28:  # Eğer değer 28 karakterden uzunsa
            truncated_value = value[:28] + "..."  # İlk 28 karakteri al ve sonuna ... ekle
            self.grid_tree.set(item_id, column=4, value=truncated_value)
        else:
            self.grid_tree.set(item_id, column=4, value=value)

        
    def load_data(self):
        try:
            with open(self.json_filename, "r") as file:
                data = json.load(file)
                for values in data:
                    self.toplanti_satirlari_ekle(values)
        except FileNotFoundError:
            pass  # dosya henüz oluşturulmamış 
        
    def load_data_kolon(self):
        try:
            with open(self.json_filename_fifth, "r") as file:
                data = json.load(file)
                for idx, value in enumerate(data):
                    self.katilanlar_satirlari_ekle(idx, value)
        except FileNotFoundError:
            pass  # dosya henüz oluşturulmamış 
        
    def load_data_katilimci(self):
        try:
            with open(self.json_filename_katilimci, "r") as file:
                data = json.load(file)
                for values in data:
                    self.farkli_tarihte_katilanlar_satirlari_ekle(values)
        except FileNotFoundError:
            pass  # dosya henüz oluşturulmamış 

    def save_data(self):
        # Grid'deki tüm verileri al
        all_data = []
        for item in self.grid_tree.get_children():
            values = self.grid_tree.item(item, "values")
            all_data.append(values)

        # Verileri JSON dosyasına kaydet
        with open(self.json_filename, "w") as file:
            json.dump(all_data, file)
            
    def save_data_katilimci(self):
        # Grid'deki tüm verileri al
        all_data = []
        for item in self.grid_tree_katilanlar.get_children():
            values = self.grid_tree_katilanlar.item(item, "values")
            all_data.append(values)

        # Verileri JSON dosyasına kaydet
        with open(self.json_filename_katilimci, "w") as file:
            json.dump(all_data, file)
            
    def save_data_kolon(self):
        # Grid'deki 5. sütundaki tüm verileri al
        all_data = []
        for item in self.grid_tree.get_children():
            values = self.grid_tree.item(item, "values")
            # Eğer 5. sütun varsa, onu al; yoksa boşluk ekle
            fifth_column_data = values[4] if len(values) > 4 else ""
            all_data.append(fifth_column_data)
        with open(self.json_filename_fifth, "w") as file:
            json.dump(all_data, file)

 
if __name__ == "__main__":
    root = tk.Tk()
    uygulama = ToplantiUygulamasi(root)
    root.mainloop()
