import time
import sys

# Warna ANSI
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
BOLD = "\033[1m"

# Fungsi delay (dalam milidetik)
def delay(ms):
    time.sleep(ms / 1000)

# Fungsi efek mesin ketik
def typewriter(text, color=YELLOW, speed=0.09):
    for c in text:
        sys.stdout.write(color + c)
        sys.stdout.flush()
        time.sleep(speed)
    print(RESET)

def main():
    print(BOLD + CYAN + "=== TAANTEEEEEEE... ===\n" + RESET)

    # Lirik lengkap
    lirik = [
        "",
        "Temanku semua pada jahat tante",
        "Aku lagi susah mereka gak ada",
        "Coba kalo lagi jayaaa",
        "Aku dipuja puja tante",
        "",
        "Sudah terbiasa terjadi tante",
        "Teman datang ketika lagi butuh saja",
        "Coba kalo lagi susahhhh",
        "Mereka semua menghilaaaaanggggg...",
        "",
        "Taanteeeee..."
    ]

    # Variasi warna per bait
    warna = [YELLOW, GREEN, BLUE, CYAN]

    # Baris yang jedanya lebih cepat
    short_delay_lines = {
        "Teman datang ketika lagi butuh saja",
        "Coba kalo lagi susahhhh"
    }

    # Tampilkan lirik dengan efek mesin ketik
    for i, line in enumerate(lirik):
        typewriter(line, warna[i % len(warna)], 0.09)
        # Atur jeda sesuai kondisi
        if line in short_delay_lines:
            delay(1000)  # jeda 1 detik
        else:
            delay(1400)  # jeda 1,4 detik

    print(BOLD + RED + "\n-- Tamat --" + RESET)

if __name__ == "__main__":
    main()
