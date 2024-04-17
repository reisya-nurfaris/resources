#!/bin/bash

# fungsi untuk ngecek modul udah diinstal atau belum
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# install wget otomatis kalo belum
if ! command_exists wget; then
    echo "wget is required but not installed. Installing wget..."
    sudo apt update
    sudo apt install -y wget
fi

# install xdg-utils otomatis kalo belum
if ! command_exists xdg-open; then
    echo "xdg-utils is required but not installed. Installing xdg-utils..."
    sudo apt update
    sudo apt install -y xdg-utils
fi

# cek apakah link gambar dimasukkan
if [ -z "$1" ]; then
    echo "Usage: $0 [image_link]"
    exit 1
fi

# download gambar pake wget
wget -O /tmp/display_image.jpg "$1"

# cek download berhasil atau nggak
if [ $? -ne 0 ]; then
    echo "Failed to download the image."
    exit 1
fi

# tampilin gambar 
xdg-open /tmp/display_image.jpg

# hapus file temporary
rm /tmp/display_image.jpg
