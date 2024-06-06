#========= modules =========#
import json
from prettytable import PrettyTable
from pwinput import pwinput
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from datetime import datetime


#========= dict =========#
data_kios = {
    "user": {
        "admin": {
            "password": "admien90",
            "admin": True
        },
        "jojon": {
            "password": "12345",
            "tgl_lahir": "2005-02-17",
            "gender": "L",
            "saldo":1000000,
            "vip": True,
            "admin": False,
            "keranjang": {}
        },
        "kipli": {
            "password": "kipluy",
            "tgl_lahir": "1988-10-03",
            "gender": "L",
            "saldo": 500000,
            "vip": False,
            "admin": False,
            "keranjang": {}
        },
        "rosa": {
            "password": "11111",
            "tgl_lahir": "2004-04-01",
            "gender": "P",
            "saldo":1000000,
            "vip": True,
            "admin": False,
            "keranjang": {}
        },
    },
    "produk": {
        "tembakau": {
            "gayo aceh": {"harga": 25000, "tipe": "lokal"},
            "esse change grape": {"harga": 20000, "tipe": "lokal"},
            "savinelli aroma": {"harga": 85000, "tipe": "impor"},
            "heritage original": {"harga": 25000, "tipe": "lokal"},
            "captain black": {"harga": 28000, "tipe": "impor"},
            "sillem's red": {"harga": 30000, "tipe": "impor"}
        },
        "kertas": {
            "kertas buffalo 100lbr": {"harga": 5000, "tipe": "tawar"},
            "kertas esse coffee 100lbr": {"harga": 5000, "tipe": "manis"},
            "kertas mascotte zig-zag 100lbr": {"harga": 10000, "tipe": "tawar"}
        },
        "roller": {
            "roller plastik 110mm": {"harga": 15000},
            "roller kain serap 110mm": {"harga": 20000},
            "roller otomatis 80mm": {"harga": 100000},
            "roller raw classic 80mm": {"harga": 18000},
            "roller OCB metal 110mm": {"harga": 25000}
        },
        "filter": {
            "filter menthol 50g": {"harga": 20000},
            "filter reguler 50g": {"harga": 15000},
            "filter esse menthol 50g": {"harga": 25000}
        }
    },
    "voucher": {
        "ngebul5": {"diskon": 5, "dipakai": False},
        "linting9": {"diskon": 9,"dipakai": False}
    },
    "pemasukan": 19000000,
    "pembelian": {
        "kipli": {
            "total pembayaran": 655000,
            "gayo aceh": 10,
            "black cavendish": 6.2,
            "kertas buffalo 100lbr": 15,
            "roller plastik 110mm": 2,
            "filter reguler 50g": 20
        },
        "jojon": {
            "total pembayaran": 395000,
            "barrack lemon": 1.9,
            "kertas buffalo 100lbr": 10,
            "roller plastik 110mm": 1,
            "filter reguler 50g": 15
        }
    }
}


#========= vars =========#
daftar_kategori = list(data_kios["produk"].keys())
current_time = datetime.now().time()
start_time = datetime.strptime("08:00", "%H:%M").time()
end_time = datetime.strptime("23:00", "%H:%M").time()


#========= funcs =========#
# mindahin output jadi ke kiri atas (mirip os.system('cls') tapi gak beneran ngehapus)
def clear():
    print('\n'*40) # kasih ruang 40 baris, kalo kurang malah nabrak output yang sebelumnya
    print('\033[H') # pindahin cursor ke home (kiri atas)


def format_uang(nominal):
    return f"Rp{nominal:,.0f}".replace(',','.')

def inputhandler(prompt, inputtype="str", max=None, min=None):
    while True:
        try:
            if inputtype == "str":
                userinput = input(prompt).strip()
            elif inputtype == "int":
                userinput = int(input(prompt))
                if userinput < 0:
                    print("Input harus lebih dari 0\n")
                    continue
            elif inputtype == "digit":
                userinput = input(prompt)
                if not userinput.isdigit():
                    print("Input hanya bisa berupa angka\n")
                    continue
            elif inputtype == "pw":
                userinput = pwinput(prompt).strip()
            elif inputtype == "nospecial":
                userinput = input(prompt).strip()
                if any(char in "!@#$%^&*()+=[]{};:'\"<>,?/~`" for char in userinput):
                    print("Input tidak boleh mengandung karakter spesial\n")
                    continue
            
            # jika parameter max dipakai (gak kosong) dan panjang input lebih dari max
            if max is not None and len(str(userinput)) > max:
                print(f"Input terlalu panjang. Maksimum panjang adalah {max} karakter.\n")
                continue
            
            if min is not None and len(str(userinput)) < min:
                print(f"Input terlalu pendek. Minimum panjang adalah {min} karakter.\n")
                continue
            
            if '\t' in str(userinput) or '\\' in str(userinput):
                print("Input tidak boleh mengandung tab atau '\\'\n")
                continue

            return userinput
        except KeyboardInterrupt:
            print("Terdeteksi interupsi\n")
        except ValueError:
            print("Input hanya bisa berupa integer\n")
        except:
            print(f"Apa lah dia\n")

def color(text, color_name):
    # ANSI color escape
    color_codes = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'purple': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'orange': '\033[38;5;208m'
    }

    # cek color_name valid atau nggak
    if color_name.lower() not in color_codes:
        raise KeyError(f"Warna {color_name} gak didukung. Cuman ini yang ada: {', '.join(color_codes.keys())}")

    # aplikasikan warna ke teks
    color_code = color_codes[color_name.lower()]
    reset_code = '\033[0m'  # ANSI escape untuk reset ke default
    colored_text = f"{color_code}{text}{reset_code}"

    return colored_text
        
# buat bikin banner (judul) biar serasi
def banner(text):
    # definisikan panjang banner
    banner_length = 65
    text_length = len(text)
    # hitung berapa karakter '=' yang diperlukan
    padding = banner_length - text_length
    # dibagi jadi dua untuk kanan kiri
    left_padding = padding // 2
    right_padding = padding - left_padding
    # tinggal dikalikan pakai jumlah kanan kiri
    return f"{'=' * left_padding} {text} {'=' * right_padding}"

def menu_admin():
    print(banner("Menu Admin"))
    print(f"Total Pemasukan: {format_uang(data_kios['pemasukan'])}")
    print("[1] Data pembelian barang")
    print("[2] Data total pembayaran")
    print("[3] Log out")
    while True:
        pilihan = inputhandler("Masukkan pilihan anda: ", "int")
        if pilihan == 1:
            clear()
            while True:
                clear()
                print(f"{'='*10} Kategori Produk {'='*10}")
                print("[1] Tembakau")
                print("[2] Kertas")
                print("[3] Roller")
                print("[4] Filter")
                print("[5] Semua produk")
                print("[6] Kembali")
                pilihan = inputhandler("Masukkan pilihan anda: ", "int")
                if pilihan <= len(daftar_kategori):
                    kategori = daftar_kategori[pilihan-1]
                    title = f'Data Pembelian {kategori.title()}'
                    daftar_nama_produk = list(data_kios["produk"][kategori].keys())
                    pembelian_produk = {item: 0 for item in daftar_nama_produk}

                elif pilihan == 5:
                    title = f"Data Pembelian Semua Produk"
                    daftar_nama_produk = []
                    for kategori in data_kios["produk"].keys():
                        daftar_nama_produk.extend(list(data_kios["produk"][kategori].keys()))
                    pembelian_produk = {item: 0 for item in daftar_nama_produk}
                
                elif pilihan == 6:
                    clear()
                    menu_admin()

                else:
                    print("Pilihan tidak valid")

                if pilihan <= 5:
                    for users, items in data_kios['pembelian'].items():
                        for item, jumlah in items.items():
                            if item in daftar_nama_produk:
                                pembelian_produk[item] = pembelian_produk.get(item, 0) + jumlah

                    pembelian_produk_urut = dict(sorted(pembelian_produk.items(), key=lambda x: x[1], reverse=True))

                    nama_produk_urut = list(pembelian_produk_urut.keys())
                    daftar_jumlah_pembelian = list(pembelian_produk_urut.values())

                    # hitung warna dari colormap supaya warnanya hijau untuk yang terbanyak dan merah untuk yang paling sedikit
                    normalize = mcolors.Normalize(vmin=min(daftar_jumlah_pembelian), vmax=max(daftar_jumlah_pembelian))
                    colormap = plt.cm.RdYlGn  # Red-Yellow-Green
                    colors = [colormap(normalize(value)) for value in daftar_jumlah_pembelian]

                    # buat graf batang pakai warna yang sudah dihitung
                    plt.figure(figsize=(10, 5))
                    bars = plt.bar(nama_produk_urut, daftar_jumlah_pembelian, color=colors)

                    # bikin teksnya miring
                    plt.xticks(rotation=90)

                    # nampilkan jumlah pembelian di atas tiap batang
                    for i, (bar, jumlah) in enumerate(zip(bars, daftar_jumlah_pembelian)):
                        c = jumlah
                        produk = nama_produk_urut[i]
                        if produk in data_kios["produk"]["tembakau"]:
                            c = f"{jumlah} ({jumlah*50:.0f}g)"
                        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), c, ha='center', va='bottom', fontsize=8)

                    # hilangin angka di kiri
                    plt.gca().yaxis.set_visible(False)

                    plt.title(title)
                    plt.tight_layout()
                    plt.show()
        
        elif pilihan == 2:
            data_user = {}
            for users, items in data_kios["pembelian"].items():
                total_pembayaran = items.get("total pembayaran", 0)
                data_user[users] = int(total_pembayaran)
            data_user = dict(sorted(data_user.items(), key=lambda x: x[1], reverse=True))

            daftar_user = list(data_user.keys())
            daftar_pembayaran = list(data_user.values())

            # hitung warna dari colormap
            normalize = mcolors.Normalize(vmin=min(daftar_pembayaran), vmax=max(daftar_pembayaran))
            colormap = plt.cm.RdYlGn  # Red-Yellow-Green
            colors = [colormap(normalize(value)) for value in daftar_pembayaran]

            # buat graf batang pakai warna yang sudah dihitung
            plt.figure(figsize=(10, 5))
            bars = plt.bar(daftar_user, daftar_pembayaran, color=colors)

            # bikin teksnya miring
            plt.xticks(rotation=90)

            # nampilkan total pembayaran di atas tiap batang
            for i, (bar, jumlah) in enumerate(zip(bars, daftar_pembayaran)):
                user = daftar_user[i]
                plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), jumlah, ha='center', va='bottom', fontsize=8)

            # hilangin angka di kiri
            plt.gca().yaxis.set_visible(False)

            plt.title("Data Total Pembayaran")
            plt.tight_layout()
            plt.show()

        elif pilihan == 3:
            clear()
            menu_awal()
        else:
            print("Pilihan tidak valid")

def menu_akun():
    print(banner("Akun"))
    print(f"{username}")
    if user["gender"] == "L":
        print(f"\nGender: Laki-laki")
    else:
        print(f"\nGender: Perempuan")
    print(f"Usia: {calculate_age(user['tgl_lahir'])} tahun")
    print(f"Saldo: {format_uang(user['saldo'])}")
    
    print("[1] Tambah saldo")
    print("[2] Kembali")
    while True:
        pilihan = inputhandler("Masukkan pilihan anda: ", "int")
        if pilihan == 1:
            jumlah = inputhandler("Masukkan jumlah yang diinginkan: ", "int")
            user["saldo"] += jumlah
            clear()
            print(f"Berhasil menambahkan {format_uang(jumlah)} ke saldo anda")
            menu_akun()
            break
        elif pilihan == 2:
            clear()
            menu_utama()
            break
        else:
            print("Pilihan tidak valid")

def menu_keranjang():
    tabel_keranjang = PrettyTable()
    tabel_keranjang.title = "Keranjang"
    tabel_keranjang.field_names = ["Nama Produk", "Harga", "Jumlah", "Total"]
    harga_total = 0
    jumlah_item = 0
    for nama_item in list(user['keranjang'].keys()):
        item = user["keranjang"][nama_item]
        harga_total += item["jumlah"] * item["harga"]
        if item["kategori"] == "tembakau":
            harga_item = f"{format_uang(item['harga'])}/50g"
            jumlah = f"{item['jumlah'] * 50:.0f}g"
            # Each 50g of tobacco counts as an individual item
            jumlah_item += (item['jumlah'] * 50) // 50
        else:
            jumlah = item['jumlah']
            harga_item = format_uang(item["harga"])
            jumlah_item += 1

        tabel_keranjang.add_row([f"{nama_item}".title(), harga_item, jumlah, format_uang(item["jumlah"] * item["harga"])])

    tabel_keranjang.add_row(['-' * 10, '-' * 10, '-' * 10, '-' * 10])
    tabel_keranjang.add_row(['', "", "Subtotal:", format_uang(harga_total)])
    print(tabel_keranjang)
    print("[1] Bayar")
    print("[2] Kembali")
    pilihan = inputhandler("Masukkan pilihan anda: ", "int")
    if pilihan == 1:
        while True:
            diskon = 0
            kode_voucher = inputhandler("Masukkan kode voucher. Tekan [n] untuk tidak pakai voucher: ")
            if kode_voucher in list(data_kios["voucher"].keys()):
                diskon = data_kios["voucher"][kode_voucher]["diskon"]
                data_kios["voucher"][kode_voucher]["dipakai"] = True

            elif kode_voucher == 'n':
                diskon = 0
            else:
                print("Kode voucher tidak ditemukan")
                diskon = 0

            # diskon 15% kalau total 100000 atau lebih 
            # diskon 25% untuk >=350rb
            # jumlah barang harus lebih dari 1 (untuk tembakau dihitung jadi 1 item tiap 50g)
            if harga_total >= 350000 and jumlah_item > 1:
                diskon += 25
            elif harga_total >= 100000 and jumlah_item > 1:
                diskon += 15
                
            harga_potongan = harga_total - (harga_total * (diskon / 100))
            if user["saldo"] >= harga_potongan:
                for nama_item in list(user['keranjang'].keys()):
                    item = user["keranjang"][nama_item]
                    if not username in data_kios["pembelian"]:
                        data_kios["pembelian"][username] = {}
                        data_kios["pembelian"][username]["total pembayaran"] = 0

                    if nama_item in data_kios["pembelian"][username]:
                        data_kios["pembelian"][username][nama_item] += item["jumlah"]
                    else:
                        data_kios["pembelian"][username][nama_item] = item["jumlah"]
                data_kios["pembelian"][username]["total pembayaran"] += harga_potongan

                tabel_keranjang.add_row(['', "", "Potongan:", f"{diskon}% (-{format_uang(harga_total * (diskon / 100))})"])
                tabel_keranjang.add_row(['', "", "Total:", format_uang(harga_potongan)])
                tabel_keranjang.add_row(['', "", "Saldo:", format_uang(user["saldo"])])
                tabel_keranjang.add_row(['', "", "Kembali:", format_uang(user["saldo"] - harga_potongan)])
                user["saldo"] -= harga_potongan
                user["keranjang"] = {}
                data_kios["pemasukan"] += harga_potongan
                
                clear()
                tabel_keranjang.title = "Kios Tembakau Mbul Mbako"
                print(tabel_keranjang)
                print("Terima kasih telah belanja di kios kami")
                print("[1] Kembali ke menu produk")
                print("[2] Log out")
                pilihan = inputhandler("Masukkan pilihan anda: ", "int")
                if pilihan == 1:
                    clear()
                    menu_produk()
                    break
                elif pilihan == 2:
                    menu_awal()
                    break
            else:
                print(f"Saldo anda tidak mencukupi\n")
    elif pilihan == 2:
        clear()
        menu_produk()

def menu_produk():
    while True:
        print(banner("Kategori Produk"))
        print("[1] Tembakau")
        print("[2] Kertas")
        print("[3] Roller")
        print("[4] Filter")
        print("[5] Kembali")
        pilihan = inputhandler("masukkan pilihan anda: ", "int")
        if pilihan <= len(daftar_kategori):
            clear()
            kategori = daftar_kategori[pilihan-1]

            daftar_nama_produk = list(data_kios["produk"][kategori].keys())
            tabel_produk = PrettyTable()
            tabel_produk.title = kategori.title()
            if kategori == "tembakau":
                tabel_produk.field_names = ["No", "Nama", "Harga/50g", "Tipe"]
                has_type = True
            elif "tipe" in data_kios["produk"][kategori][daftar_nama_produk[0]]:
                tabel_produk.field_names = ["No", "Nama", "Harga", "Tipe"]
                has_type = True
            else:
                has_type = False
                tabel_produk.field_names = ["No", "Nama", "Harga"]

            for i, nama_produk in enumerate(daftar_nama_produk, start=1):
                produk = data_kios["produk"][kategori][nama_produk]
                if has_type:
                    tabel_produk.add_row([i, nama_produk.title(), format_uang(produk["harga"]), produk["tipe"]])
                else:
                    tabel_produk.add_row([i, nama_produk.title(), format_uang(produk["harga"])])
            print(tabel_produk)

            print("[1] Tambah barang ke keranjang")
            print("[2] Kembali ke kategori")
            while True:
                pilihan = inputhandler("masukkan pilihan anda: ", "int")
                if pilihan == 1:
                    while True:
                        no = inputhandler("\nNomor barang: ", "int")
                        
                        ada = False
                        for i, nama_produk in enumerate(daftar_nama_produk, start=1):
                            if i == no:
                                produk = data_kios["produk"][kategori][nama_produk]
                                ada = True
                                if kategori == "tembakau":
                                    while True:
                                        jumlah = inputhandler("Berapa gram?: ", "int") / 50
                                        if jumlah < 1:
                                            print(color("\nMinimal 50 gram\n", "orange"))
                                        else:
                                            break
                                else:
                                    while True:
                                        jumlah = inputhandler("jumlah: ", "int")
                                        if jumlah < 1:
                                            print("\nMinimal 1\n")
                                        else:
                                            break
                                
                                if kategori == "tembakau":
                                    pak = f"{jumlah*50:.0f}g"
                                elif kategori == "kertas":
                                    pak = f"{jumlah} buku"
                                elif kategori == "filter":
                                    pak = f"{jumlah} bungkus"
                                else:
                                    pak = jumlah

                                if nama_produk in list(user["keranjang"].keys()):
                                    user["keranjang"][nama_produk]["jumlah"] += jumlah
                                else:
                                    user["keranjang"].update({nama_produk:{"kategori": kategori, "harga": produk["harga"], "jumlah": jumlah}})
                                
                                clear()
                                print(f"{pak} {nama_produk} telah ditambahkan ke keranjang\n")

                                print("[1] Tambah barang lagi")
                                print("[2] Lihat Keranjang")
                                print("[3] Kembali ke kategori")
                                while True:
                                    pilihan = inputhandler("Masukkan pilihan: ", "int")
                                    if pilihan == 1:
                                        clear()
                                        print(tabel_produk)
                                        break
                                    elif pilihan == 2:
                                        clear()
                                        menu_keranjang()
                                        break
                                    elif pilihan == 3:
                                        clear()
                                        menu_produk()
                                        break
                                    else:
                                        print(color("Pilihan tidak valid", "red"))
                        if not ada:
                            print(color("\nNomor barang tidak valid\n", "red"))

                elif pilihan == 2:
                    clear()
                    menu_produk()
                else:
                    print(color("Pilihan tidak valid", "red"))
        elif pilihan == 5:
            clear()
            menu_utama()
        else:
            print(color("Pilihan tidak valid", "red"))

def calculate_age(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d").date()
    today = datetime.today()
    age = today.year - date.year - ((today.month, today.day) < (date.month, date.day))
    return age

def register():
    print(banner("Register"))
    
    while True:
        global username
        username = inputhandler("Masukkan username anda: ", "nospecial", min=8, max=30)
        if username in data_kios["user"]:
            print("Username sudah dipakai, silahkan pilih username lain\n")
        else:
            break

    while True:
        try:
            birthdate_str = inputhandler("Masukkan tanggal lahir anda (YYYY-MM-DD): ").strip()
            # birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d").date()
            usia = calculate_age(birthdate_str)
            if usia < 18:
                print("Gaboleh ye, usia harus 18 tahun atau lebih")
                return  # Menghentikan registrasi jika usia di bawah 18
            else:
                break
        except ValueError:
            print("Masukkan tanggal yang valid dengan format YYYY-MM-DD")

    while True:
        gender = inputhandler("Masukkan gender anda (L/P): ").strip().upper()
        if gender not in ["L", "P"]:
            print("Gender harus 'L' atau 'P'\n")
        else:
            break

    while True:
        password = inputhandler("Masukkan password anda: ", "pw")
        if len(password) < 4:
            print(color("Password harus memiliki minimal 4 karakter\n", "orange"))
        else:
            break

    global user
    user = data_kios["user"][username] = {
        "password": password,
        "saldo": 500000,
        "vip": False,
        "keranjang": {},
        "tgl_lahir": birthdate_str,
        "gender": gender
    }
    
    clear()

    # Menentukan panggilan
    if usia < 30:
        panggilan = "Bang" if gender == "L" else "Mbak"
    else:
        panggilan = "Pak" if gender == "L" else "Ibu"

    print(color(f"\nRegistrasi berhasil. Selamat datang {panggilan} {username}!", "green"))
    menu_utama()

def login():
    print(banner("Login"))
    
    while True:
        global username
        username = inputhandler("Masukkan username anda: ", "nospecial")
        password = inputhandler("Masukkan password anda: ", "pw")
        
        if username in data_kios["user"] and data_kios["user"][username]["password"] == password:
            global user
            user = data_kios["user"][username]
            
            if user.get("admin", False):
                menu_admin()
            else:
                usia = calculate_age(user["tgl_lahir"])
                gender = user["gender"]

                if usia < 30:
                    panggilan = "Bang" if gender == "L" else "Mbak"
                else:
                    panggilan = "Pak" if gender == "L" else "Ibu"

                clear()

                print(color(f"Login Berhasil. Selamat datang {panggilan} {username}!", "green"))
                menu_utama()
            break
        else:
            print(color("Login gagal", "red"))


def menu_utama():
    print(banner("Menu Utama"))
    print("[1] Lihat produk")
    print("[2] Keranjang")
    print("[3] Akun")
    print("[4] Log out")
    while True:
        pilihan = inputhandler("masukkan pilihan anda: ", "int")
        if pilihan == 1:
            clear()
            menu_produk()
        elif pilihan == 2:
            if user["keranjang"] != {}:
                clear()
                menu_keranjang()
            else:
                clear()
                print("\nKeranjang anda kosong")
                menu_utama()
                break
        elif pilihan == 3:
            clear()
            menu_akun()
        elif pilihan == 4:
            clear()
            menu_awal()
        else:
            print(color("Pilihan tidak valid\n", "red"))

def menu_awal():
    clear()
    if not (start_time <= current_time <= end_time):
        print(color("Kios buka dari jam 08:00 sampai 16:00. Silahkan kembali lagi pas buka yaa", "orange"))
        return
    
    print(banner("Selamat Datang di Kios Tembakau Mbul Mbako"))
    print("[1] Login")
    print("[2] Register")
    while True:
        pilihan = inputhandler("Masukkan pilihan anda: ", "int")
        if pilihan == 1:
            clear()
            login()
            break
        elif pilihan == 2:
            clear()
            register()
            break
        else:
            print("Pilihan tidak valid\n")


#========= main call =========#
menu_awal()
