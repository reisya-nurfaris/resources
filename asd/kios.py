#========= modules =========#
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
            "saldo":1000000,
            "e-money": 90000,
            "vip": True,
            "admin": False,
            "keranjang": {}
        },
        "kipli": {
            "password": "kipluy",
            "saldo": 500000,
            "e-money": 0,
            "vip": False,
            "admin": False,
            "keranjang": {}
        }
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
end_time = datetime.strptime("16:00", "%H:%M").time()


#========= funcs =========#
# mindahin output jadi ke kiri atas (mirip os.system('cls') tapi gak beneran ngehapus)
def clear():
    print('\n'*40)
    print('\033[H')

def intinput(prompt):
    while True:
        try:
            parsed_input = int(input(prompt))
            if parsed_input > 0:
                return parsed_input
            elif parsed_input <= 0:
                print("Input harus lebih dari 0\n")
        except:
            print("Input hanya bisa berupa angka\n")

def format_uang(nominal):
    return f"Rp{nominal:,.0f}".replace(',','.')

def menu_admin():
    print(f"{'='*10} Menu Admin {'='*10}")
    print(f"Total Pemasukan: {format_uang(data_kios['pemasukan'])}")
    print("[1] Data pembelian barang")
    print("[2] Data total pembayaran")
    print("[3] Log out")
    while True:
        pilihan = intinput("Masukkan pilihan anda: ")
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
                pilihan = intinput("Masukkan pilihan anda: ")
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
    print(f"\n{'='*10} Akun {'='*10}")
    print(f"{username}")
    print(f"\nSaldo: {user['saldo']}")
    print(f"e-money: {user['e-money']}")
    
    print("[1] Tambah e-money")
    print("[2] Kembali")
    while True:
        pilihan = intinput("Masukkan pilihan anda: ")
        if pilihan == 1:
            jumlah = intinput("Masukkan jumlah yang diinginkan: ")
            if jumlah <= user["saldo"]:
                user["saldo"] -= jumlah
                user["e-money"] += jumlah
                clear()
                print(f"Berhasil menambahkan {format_uang(jumlah)} ke e-money anda")
                menu_akun()
                break
            else:
                print("Saldo anda tidak mencukupi")
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
    pilihan = intinput("Masukkan pilihan anda: ")
    if pilihan == 1:
        while True:
            print("\nPilih metode pembayaran")
            print("[1] Cash")
            print("[2] e-money")
            pilihan = intinput("Masukkan pilihan anda: ")

            if pilihan == 1:
                metode = "saldo"
            elif pilihan == 2:
                metode = "e-money"
            
            diskon = 0
            kode_voucher = input("Masukkan kode voucher. Tekan [n] untuk tidak pakai voucher: ")
            if kode_voucher in list(data_kios["voucher"].keys()):
                diskon = data_kios["voucher"][kode_voucher]["diskon"]
                data_kios["voucher"][kode_voucher]["dipakai"] = True

            elif kode_voucher == 'n':
                diskon = 0
            else:
                print("Kode voucher tidak ditemukan")
                diskon = 0

            # diskon 10% kalau total 100000 atau lebih dan jumlah barang lebih dari 1 (untuk tembakau dihitung jadi 1 item tiap 50g)
            
            if harga_total >= 100000 and jumlah_item > 1:
                diskon += 10

            harga_potongan = harga_total - (harga_total * (diskon / 100))
            if user[metode] >= harga_potongan:
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
                tabel_keranjang.add_row(['', "", f"{metode.replace('saldo', 'Cash')}:", format_uang(user[metode])])
                tabel_keranjang.add_row(['', "", "Kembali:", format_uang(user[metode] - harga_potongan)])
                user[metode] -= harga_potongan
                user["keranjang"] = {}
                
                clear()
                tabel_keranjang.title = "Kios Tembakau Kretek Bacco"
                print(tabel_keranjang)
                print("Terima kasih telah belanja di kios kami")
                print("[1] Kembali ke menu produk")
                print("[2] Log out")
                pilihan = intinput("Masukkan pilihan anda: ")
                if pilihan == 1:
                    clear()
                    menu_produk()
                    break
                elif pilihan == 2:
                    menu_awal()
                    break
            else:
                print(f"\n{metode.title()} anda tidak mencukupi\n")
    elif pilihan == 2:
        clear()
        menu_produk()

def menu_produk():
    while True:
        print(f"{'='*10} Kategori Produk {'='*10}")
        print("[1] Tembakau")
        print("[2] Kertas")
        print("[3] Roller")
        print("[4] Filter")
        print("[5] Kembali")
        pilihan = intinput("masukkan pilihan anda: ")
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
                pilihan = intinput("masukkan pilihan anda: ")
                if pilihan == 1:
                    while True:
                        no = intinput("\nNomor barang: ")
                        
                        ada = False
                        for i, nama_produk in enumerate(daftar_nama_produk, start=1):
                            if i == no:
                                produk = data_kios["produk"][kategori][nama_produk]
                                ada = True
                                if kategori == "tembakau":
                                    while True:
                                        jumlah = intinput("Berapa gram?: ") / 50
                                        if jumlah < 1:
                                            print("\nMinimal 50 gram\n")
                                        else:
                                            break
                                else:
                                    while True:
                                        jumlah = intinput("jumlah: ")
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
                                    pilihan = intinput("Masukkan pilihan: ")
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
                                        print("Pilihan tidak valid")
                        if not ada:
                            print("\nNomor barang tidak valid\n")

                elif pilihan == 2:
                    clear()
                    menu_produk()
                else:
                    print("Pilihan tidak valid")
        elif pilihan == 5:
            clear()
            menu_utama()
        else:
            print("Pilihan tidak valid")

def register():
    print(f"{'='*10} Register {'='*10}")
    while True:
        global username
        username = input("Masukkan username anda: ").strip()
        if username in data_kios["user"]:
            print("Username sudah dipakai, silahkan pilih username lain\n")
        elif len(username) < 4:
            print("Username harus memiliki minimal 4 karakter\n")
        else:
            break

    while True:
        password = pwinput("Masukkan password anda: ").strip()
        if len(password) < 4:
            print("Password harus memiliki minimal 4 karakter\n")
        else:
            break
    
    global user
    user = data_kios["user"][username] = {
        "password": password,
        "saldo": 500000,
        "e-money": 0,
        "vip": False,
        "keranjang": {}
    }
    clear()
    print(f"\nRegistrasi berhasil. Selamat datang {username}!")
    menu_utama()
    
def login():
    print(f"{'='*10} Login {'='*10}")
    while True:
        global username
        username = input("Masukkan username anda: ")
        password = pwinput("Masukkan password anda: ")
        if username in data_kios["user"] and data_kios["user"][username]["password"] == password:
            global user
            user = data_kios["user"][username]
            if user["admin"]:
                clear()
                print("Berhasil login sebagai admin.")
                menu_admin()
            else:
                clear()
                print("Login Berhasil. Selamat datang " + username + "!")
                menu_utama()
        else:
            print("Login gagal")

def menu_utama():
    print(f"{'='*10} Menu Utama {'='*10}")
    print("[1] Lihat produk")
    print("[2] Keranjang")
    print("[3] Akun")
    print("[4] Log out")
    while True:
        pilihan = intinput("masukkan pilihan anda: ")
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
            print("Pilihan tidak valid\n")

def menu_awal():
    clear()
    if not (start_time <= current_time <= end_time):
        print("Kios buka dari jam 08:00 sampai 16:00. Silahkan kembali lagi pas buka yaa")
        return
    
    print(f"{'='*5} Selamat Datang di Kios Tembakau Kretek Bacco {'='*5}")
    print("[1] Login")
    print("[2] Register")
    while True:
        pilihan = intinput("Masukkan pilihan anda: ")
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
