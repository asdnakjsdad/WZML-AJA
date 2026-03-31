# ruff: noqa: F403, F405
mirror = """<b>Kirim tautan bersama dengan baris perintah atau </b>

/cmd link

<b>Dengan membalas ke tautan/file</b>:

/cmd -n nama_baru -e -up tujuan_unggahan

<b>CATATAN:</b>
1. Perintah yang dimulai dengan <b>qb</b> HANYA untuk torrent."""

yt = """<b>Kirim tautan bersama dengan baris perintah</b>:

/cmd link
<b>Dengan membalas ke tautan</b>:
/cmd -n nama_baru -z kata_sandi -opt x:y|x1:y1

Cek di sini untuk semua <a href='https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md'>SITUS</a> yang didukung
Cek semua opsi api yt-dlp dari <a href='https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/YoutubeDL.py#L212'>FILE</a> ini atau gunakan <a href='https://t.me/mltb_official_channel/177'>skrip</a> ini untuk mengonversi argumen CLI ke opsi API."""

clone = """Kirim tautan Gdrive|Gdot|Filepress|Filebee|Appdrive|Gdflix atau path rclone bersama dengan perintah atau dengan membalas ke tautan/rc_path dengan perintah.
Gunakan -sync untuk menggunakan metode sinkronisasi di rclone. Contoh: /cmd rcl/path_rclone -up rcl/path_rclone/rc -sync"""

new_name = """<b>Nama Baru</b>: -n

/cmd link -n nama baru
Catatan: Tidak berfungsi untuk torrent"""

multi_link = """<b>Multi tautan hanya dengan membalas ke tautan/file pertama</b>: -i

/cmd -i 10 (jumlah tautan/file)"""

same_dir = """<b>Pindahkan file/folder ke folder baru</b>: -m

Kamu juga bisa menggunakan argumen ini untuk memindahkan isi dari beberapa tautan/torrent ke direktori yang sama, jadi semua tautan akan diunggah bersama sebagai satu tugas.

/cmd link -m folder_baru (hanya satu tautan di dalam folder baru)
/cmd -i 10 (jumlah tautan/file) -m nama_folder (semua isi tautan di dalam satu folder)
/cmd -b -m nama_folder (balas ke pesan massal/file (tiap tautan di baris baru))

Saat menggunakan bulk (massal), kamu juga bisa menggunakan argumen ini dengan nama folder yang berbeda bersama tautan di pesan atau file massal.
Contoh:
link1 -m folder1
link2 -m folder1
link3 -m folder2
link4 -m folder2
link5 -m folder3
link6
maka isi dari link1 dan link2 akan diunggah dari folder yang sama yaitu folder1
isi link3 dan link4 akan diunggah dari folder yang sama juga yaitu folder2
link5 akan diunggah sendirian di dalam folder baru bernama folder3
link6 akan diunggah secara normal sendirian
"""

thumb = """<b>Thumbnail untuk tugas saat ini</b>: -t

/cmd link -t link-pesan-tg (dokumen atau foto) atau none (file tanpa thumbnail)"""

split_size = """<b>Ukuran pecahan (split) untuk tugas saat ini</b>: -sp

/cmd link -sp (500mb atau 2gb atau 4000000000)
Catatan: Hanya mb dan gb yang didukung, atau tulis dalam bytes tanpa satuan!"""

upload = """<b>Tujuan Unggahan</b>: -up

/cmd link -up rcl/gdl (rcl: untuk memilih config rclone, remote & path | gdl: untuk memilih token.pickle, id gdrive) menggunakan tombol
Kamu bisa langsung menambahkan path unggahan: -up remote:dir/subdir atau -up Id_Gdrive atau -up id/username (telegram) atau -up id/username|id_topik (telegram)
Jika DEFAULT_UPLOAD adalah `rc` maka kamu bisa memasukkan up: `gd` untuk mengunggah menggunakan alat gdrive ke GDRIVE_ID.
Jika DEFAULT_UPLOAD adalah `gd` maka kamu bisa memasukkan up: `rc` untuk mengunggah ke RCLONE_PATH.

Jika kamu ingin menambahkan path atau gdrive secara manual dari config/token kamu (DIUNGGAH DARI USETTING), tambahkan mrcc: untuk rclone dan mtp: sebelum path/id_gdrive tanpa spasi.
/cmd link -up mrcc:main:dump atau -up mtp:id_gdrive <strong>atau kamu cukup mengedit unggahan menggunakan token/config owner/user dari usetting tanpa menambahkan mtp: atau mrcc: sebelum path/id unggahan</strong>

Untuk menambahkan tujuan leech:
-up id/@username/pm
-up b:id/@username/pm (b: artinya leech oleh bot) (id atau username obrolan, atau tulis pm yang berarti pesan pribadi agar bot mengirimkan file secara pribadi kepadamu)
Kapan harus menggunakan b: (leech oleh bot)? Saat pengaturan default kamu adalah leech oleh pengguna (user) dan kamu ingin melakukan leech menggunakan bot untuk tugas tertentu.
-up u:id/@username (u: artinya leech oleh pengguna) Ini jika OWNER menambahkan USER_STRING_SESSION.
-up h:id/@username (leech campuran/hybrid) h: untuk mengunggah file oleh bot dan pengguna berdasarkan ukuran file.
-up id/@username|id_topik (leech di obrolan dan topik tertentu) tambahkan | tanpa spasi dan tulis id topik setelah id obrolan atau username.

Jika kamu ingin menentukan apakah menggunakan token.pickle atau service accounts, kamu bisa menambahkan tp:id_gdrive (menggunakan token.pickle) atau sa:id_gdrive (menggunakan service accounts) atau mtp:id_gdrive (menggunakan token.pickle pengguna yang diunggah dari usetting).
DEFAULT_UPLOAD tidak berpengaruh pada perintah leech.
"""

user_download = """<b>Unduhan Pengguna</b>: link

/cmd tp:link untuk mengunduh menggunakan token.pickle owner jika service account aktif.
/cmd sa:link untuk mengunduh menggunakan service account jika service account dinonaktifkan.
/cmd tp:id_gdrive untuk mengunduh menggunakan token.pickle dan file_id jika service account aktif.
/cmd sa:id_gdrive untuk mengunduh menggunakan service account dan file_id jika service account dinonaktifkan.
/cmd mtp:id_gdrive atau mtp:link untuk mengunduh menggunakan token.pickle pengguna yang diunggah dari usetting
/cmd mrcc:remote:path untuk mengunduh menggunakan config rclone pengguna yang diunggah dari usetting
kamu cukup mengedit unggahan menggunakan token/config owner/user dari usetting tanpa menambahkan mtp: atau mrcc: sebelum path/id"""

rcf = """<b>Bendera (Flags) Rclone</b>: -rcf

/cmd link|path|rcl -up path|rcl -rcf --buffer-size:8M|--drive-starred-only|kunci|kunci:nilai
Ini akan menimpa semua bendera lain kecuali --exclude
Cek di sini untuk semua <a href='https://rclone.org/flags/'>Bendera Rclone</a>."""

bulk = """<b>Unduhan Massal (Bulk)</b>: -b

Bulk hanya bisa digunakan dengan membalas ke pesan teks atau file teks yang berisi tautan yang dipisahkan oleh baris baru.
Contoh:
link1 -n nama baru -up remote1:path1 -rcf |kunci:nilai|kunci:nilai
link2 -z -n nama baru -up remote2:path2
link3 -e -n nama baru -up remote2:path2
Balas ke contoh ini dengan perintah -> /cmd -b (bulk)

Catatan: Argumen apapun yang menyertai perintah akan diterapkan ke semua tautan
/cmd -b -up remote: -z -m nama_folder (semua isi tautan dalam satu folder berformat zip diunggah ke satu tujuan)
jadi kamu tidak bisa mengatur tujuan unggahan yang berbeda di setiap tautan jika kamu menambahkan -m bersama perintah
Kamu bisa mengatur awal dan akhir tautan dari bulk seperti seed, dengan -b awal:akhir atau hanya akhir dengan -b :akhir atau hanya awal dengan -b awal.
Nilai default awal adalah dari nol (tautan pertama) hingga tak terbatas."""

rlone_dl = """<b>Unduhan Rclone</b>:

Perlakukan path rclone persis seperti tautan
/cmd main:dump/ubuntu.iso atau rcl (Untuk memilih config, remote dan path)
Pengguna bisa menambahkan rclone mereka sendiri dari pengaturan pengguna
Jika kamu ingin menambahkan path secara manual dari config kamu, tambahkan mrcc: sebelum path tanpa spasi
/cmd mrcc:main:dump/ubuntu.iso
Kamu cukup mengedit menggunakan config owner/user dari usetting tanpa menambahkan mrcc: sebelum path"""

extract_zip = """<b>Ekstrak/Zip</b>: -e -z

/cmd link -e kata_sandi (ekstrak dengan perlindungan kata sandi)
/cmd link -z kata_sandi (zip dengan perlindungan kata sandi)
/cmd link -z kata_sandi -e (ekstrak dan zip dengan perlindungan kata sandi)
Catatan: Saat ekstrak dan zip ditambahkan bersama perintah, ia akan mengekstrak dulu lalu men-zip, jadi selalu ekstrak lebih dulu"""

join = """<b>Gabungkan File Terpecah</b>: -j

Opsi ini hanya akan berfungsi sebelum ekstrak dan zip, jadi kebanyakan akan digunakan dengan argumen -m (samedir)
Dengan Balasan:
/cmd -i 3 -j -m nama_folder
/cmd -b -j -m nama_folder
jika kamu punya link (folder) yang berisi file terpecah:
/cmd link -j"""

tg_links = """<b>Tautan TG</b>:

Perlakukan tautan Telegram seperti tautan langsung (direct link) pada umumnya
Beberapa tautan membutuhkan akses pengguna jadi kamu harus menambahkan USER_SESSION_STRING untuk itu.
Tiga jenis tautan:
Publik: https://t.me/nama_channel/id_pesan
Pribadi: tg://openmessage?user_id=xxxxxx&message_id=xxxxx
Super: https://t.me/c/id_channel/id_pesan
Rentang: https://t.me/nama_channel/id_pesan_awal-id_pesan_akhir
Contoh Rentang: tg://openmessage?user_id=xxxxxx&message_id=555-560 atau https://t.me/nama_channel/100-150
Catatan: Tautan rentang (range) hanya akan bekerja dengan membalas perintah ke tautan tersebut"""

sample_video = """<b>Video Sampel</b>: -sv

Buat video sampel untuk satu video atau folder berisi video.
/cmd -sv (akan mengambil nilai default yaitu durasi sampel 60 detik dan durasi tiap bagian 4 detik).
Kamu bisa mengubah nilai tersebut. Contoh: /cmd -sv 70:5 (durasi-sampel:durasi-bagian) atau /cmd -sv :5 atau /cmd -sv 70."""

screenshot = """<b>Tangkapan Layar (ScreenShots)</b>: -ss

Buat tangkapan layar untuk satu video atau folder berisi video.
/cmd -ss (akan mengambil nilai default yaitu 10 foto).
Kamu bisa mengubah nilai ini. Contoh: /cmd -ss 6."""

seed = """<b>Seed Bittorrent</b>: -d

/cmd link -d rasio:waktu_seed atau dengan membalas ke file/tautan
Untuk menentukan rasio dan waktu seed tambahkan -d rasio:waktu.
Contoh: -d 0.7:10 (rasio dan waktu) atau -d 0.7 (hanya rasio) atau -d :10 (hanya waktu) di mana waktu dalam hitungan menit"""

zip_arg = """<b>Zip</b>: -z kata_sandi

/cmd link -z (zip)
/cmd link -z kata_sandi (zip dengan perlindungan kata sandi)"""

qual = """<b>Tombol Kualitas</b>: -s

Jika kualitas default ditambahkan dari opsi yt-dlp menggunakan opsi format dan kamu perlu memilih kualitas untuk tautan tertentu atau multi tautan.
/cmd link -s"""

yt_opt = """<b>Opsi</b>: -opt

/cmd link -opt {"format": "bv*+mergeall[vcodec=none]", "nocheckcertificate": True, "playliststart": 10, "fragment_retries": float("inf"), "matchtitle": "S13", "writesubtitles": True, "live_from_start": True, "postprocessor_args": {"ffmpeg": ["-threads", "4"]}, "wait_for_video": (5, 100), "download_ranges": [{"start_time": 0, "end_time": 10}]}

Cek semua opsi api yt-dlp dari <a href='https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/YoutubeDL.py#L184'>FILE</a> ini atau gunakan <a href='https://t.me/mltb_official_channel/177'>skrip</a> ini untuk mengonversi argumen CLI ke opsi API."""

convert_media = """<b>Konversi Media</b>: -ca -cv
/cmd link -ca mp3 -cv mp4 (konversi semua audio ke mp3 dan semua video ke mp4)
/cmd link -ca mp3 (konversi semua audio ke mp3)
/cmd link -cv mp4 (konversi semua video ke mp4)
/cmd link -ca mp3 + flac ogg (konversi hanya flac dan ogg audio ke mp3)
/cmd link -cv mkv - webm flv (konversi semua video ke mp4 kecuali webm dan flv)"""

force_start = """<b>Mulai Paksa</b>: -f -fd -fu
/cmd link -f (paksa unduh dan unggah)
/cmd link -fd (paksa unduh saja)
/cmd link -fu (paksa unggah langsung setelah unduhan selesai)"""

gdrive = """<b>Gdrive</b>: link
Jika DEFAULT_UPLOAD adalah `rc` maka kamu bisa memasukkan up: `gd` untuk mengunggah menggunakan alat gdrive ke GDRIVE_ID.
/cmd TautanGdrive atau gdl atau IdGdrive -up gdl atau IdGdrive atau gd
/cmd tp:TautanGdrive atau tp:IdGdrive -up tp:IdGdrive atau gdl atau gd (untuk menggunakan token.pickle jika service account aktif)
/cmd sa:TautanGdrive atau sa:IdGdrive -p sa:IdGdrive atau gdl atau gd (untuk menggunakan service account jika service account dinonaktifkan)
/cmd mtp:TautanGdrive atau mtp:IdGdrive -up mtp:IdGdrive atau gdl atau gd(jika kamu menambahkan unggahan IdGdrive dari usetting) (untuk menggunakan token.pickle pengguna dari usetting)
Kamu cukup mengedit menggunakan token owner/user dari usetting tanpa menambahkan mtp: sebelum id"""

rclone_cl = """<b>Rclone</b>: path
Jika DEFAULT_UPLOAD adalah `gd` maka kamu bisa memasukkan up: `rc` untuk mengunggah ke RCLONE_PATH.
/cmd rcl/path_rclone -up rcl/path_rclone/rc -rcf kuncibendera:nilaibendera|kuncibendera|kuncibendera:nilaibendera
/cmd rcl atau path_rclone -up path_rclone atau rc atau rcl
/cmd mrcc:path_rclone -up rcl atau rc (jika kamu menambahkan path rclone dari usetting) (untuk menggunakan config pengguna)
Kamu cukup mengedit menggunakan config owner/user dari usetting tanpa menambahkan mrcc: sebelum path"""

name_swap = r"""<b>Penggantian Nama (Name Swap)</b>: -ns
/cmd link -ns skrip/kode/s | mirror/leech | teh/ /s | clone | cpu/ | \[mltb\]/mltb | \\teks\\/teks/s
Ini akan berdampak pada semua file. Format: kataYangDiganti/kataPengganti/sensitiveCase
Penggantian Kata. Kamu bisa menambahkan pola (pattern) alih-alih teks normal. Waktu Habis: 60 dtk
CATATAN: Kamu harus menambahkan \ sebelum karakter apapun, ini adalah karakternya: \^$.|?*+()[]{}-
1. skrip akan diganti dengan kode dengan sensitive case
2. mirror akan diganti dengan leech
4. teh akan diganti dengan spasi dengan sensitive case
5. clone akan dihapus
6. cpu akan diganti dengan spasi
7. [mltb] akan diganti dengan mltb
8. \teks\ akan diganti dengan teks dengan sensitive case
"""

transmission = """<b>Transmisi TG</b>: -hl -ut -bt
/cmd link -hl (leech oleh pengguna dan sesi bot berdasarkan ukuran file) (Hybrid Leech)
/cmd link -bt (leech oleh sesi bot)
/cmd link -ut (leech oleh pengguna)"""

thumbnail_layout = """Tata Letak Thumbnail: -tl
/cmd link -tl 3x3 (lebarxtinggi) 3 foto di baris dan 3 foto di kolom"""

leech_as = """<b>Leech Sebagai</b>: -doc -med
/cmd link -doc (Leech sebagai dokumen)
/cmd link -med (Leech sebagai media)"""

ffmpeg_cmds = """<b>Perintah FFmpeg</b>: -ff
daftar dari perintah ffmpeg. Kamu bisa mengatur beberapa perintah ffmpeg untuk semua file sebelum diunggah. Jangan tulis ffmpeg di awal, langsung mulai dengan argumennya.
Catatan:
1. Tambahkan <code>-del</code> ke dalam daftar jika kamu ingin bot menghapus file asli setelah perintah selesai dijalankan!
3. Untuk mengeksekusi salah satu daftar yang sudah ditambahkan di bot seperti: ({"subtitle": ["-i mltb.mkv -c copy -c:s srt mltb.mkv"]}), kamu harus menggunakan -ff subtitle (kunci daftar)
Contoh: ["-i mltb.mkv -c copy -c:s srt mltb.mkv", "-i mltb.video -c copy -c:s srt mltb", "-i mltb.m4a -c:a libmp3lame -q:a 2 mltb.mp3", "-i mltb.audio -c:a libmp3lame -q:a 2 mltb.mp3", "-i mltb -map 0:a -c copy mltb.mka -map 0:s -c copy mltb.srt"]
Di sini saya akan menjelaskan bagaimana menggunakan mltb.* yang mereferensikan file yang ingin dikerjakan.
1. Perintah pertama: input mltb.mkv, jadi perintah ini hanya bekerja pada video mkv dan outputnya juga mltb.mkv. -del akan menghapus media asli setelah selesai.
2. Perintah kedua: input mltb.video, jadi perintah ini bekerja pada semua video dan outputnya hanya mltb (ekstensi sama dengan input).
3. Perintah ketiga: input mltb.m4a, jadi perintah ini hanya bekerja pada audio m4a dan outputnya mltb.mp3.
4. Perintah keempat: input mltb.audio, jadi perintah ini bekerja pada semua audio dan outputnya mltb.mp3."""

metadata = """<b>Metadata</b>: -meta

Terapkan metadata kustom ke file media menggunakan pemisah pipa (|).

<b>Format:</b> kunci=nilai|kunci2=nilai2|kunci3=nilai3

<b>Variabel Dinamis:</b>
• <code>{filename}</code> - Nama file asli
• <code>{basename}</code> - Nama file tanpa ekstensi  
• <code>{extension}</code> - Ekstensi file
• <code>{audiolang}</code> - Bahasa audio (terdeteksi otomatis atau bahasa Inggris)
• <code>{sublang}</code> - Bahasa subtitle (terdeteksi otomatis atau tidak ada)
• <code>{year}</code> - Tahun yang diekstrak dari nama file

<b>Metadata Per-Stream:</b>
Atur metadata yang berbeda untuk stream audio/video/subtitle di Pengaturan Pengguna > Pengaturan FFmpeg:
• <b>Metadata Audio:</b> Diterapkan pada setiap stream audio
• <b>Metadata Video:</b> Diterapkan pada stream video  
• <b>Metadata Subtitle:</b> Diterapkan pada stream subtitle

<b>Contoh:</b>
<code>/mirror link -meta title=Film Saya|artist={audiolang} Version</code>
<code>/yt link -meta album={basename}|year={year}|genre=Aksi</code>

<b>Menghindari Pipa:</b> Gunakan <code>\\|</code> untuk menyertakan karakter pipa literal pada nilai:
<code>title=Film \\| Edisi Sutradara</code>

<b>Contoh Pengaturan Pengguna:</b>
• Metadata Audio: <code>language={audiolang}|title=Track Audio</code>
• Metadata Video: <code>title={basename}|year={year}</code>
• Metadata Subtitle: <code>language={sublang}|title=Subtitle</code>"""

YT_HELP_DICT = {
    "main": yt,
    "New-Name": f"{new_name}\nCatatan: Jangan tambahkan ekstensi file",
    "Zip": zip_arg,
    "Quality": qual,
    "Options": yt_opt,
    "Multi-Link": multi_link,
    "Same-Directory": same_dir,
    "Thumb": thumb,
    "Split-Size": split_size,
    "Upload-Destination": upload,
    "Rclone-Flags": rcf,
    "Bulk": bulk,
    "Sample-Video": sample_video,
    "Screenshot": screenshot,
    "Convert-Media": convert_media,
    "Force-Start": force_start,
    "Name-Swap": name_swap,
    "TG-Transmission": transmission,
    "Thumb-Layout": thumbnail_layout,
    "Leech-Type": leech_as,
    "FFmpeg-Cmds": ffmpeg_cmds,
    "Metadata": metadata,
}

MIRROR_HELP_DICT = {
    "main": mirror,
    "New-Name": new_name,
    "DL-Auth": "<b>Otorisasi Tautan Langsung</b>: -au -ap\n\n/cmd link -au username -ap kata_sandi",
    "Headers": "<b>Header kustom tautan langsung</b>: -h\n\n/cmd link -h kunci: nilai kunci1: nilai1",
    "Extract/Zip": extract_zip,
    "Select-Files": "<b>Pemilihan File Bittorrent/JDownloader/Sabnzbd</b>: -s\n\n/cmd link -s atau dengan membalas ke file/tautan",
    "Torrent-Seed": seed,
    "Multi-Link": multi_link,
    "Same-Directory": same_dir,
    "Thumb": thumb,
    "Split-Size": split_size,
    "Upload-Destination": upload,
    "Rclone-Flags": rcf,
    "Bulk": bulk,
    "Join": join,
    "Rclone-DL": rlone_dl,
    "Tg-Links": tg_links,
    "Sample-Video": sample_video,
    "Screenshot": screenshot,
    "Convert-Media": convert_media,
    "Force-Start": force_start,
    "User-Download": user_download,
    "Name-Swap": name_swap,
    "TG-Transmission": transmission,
    "Thumb-Layout": thumbnail_layout,
    "Leech-Type": leech_as,
    "FFmpeg-Cmds": ffmpeg_cmds,
    "Metadata": metadata,
}

CLONE_HELP_DICT = {
    "main": clone,
    "Multi-Link": multi_link,
    "Bulk": bulk,
    "Gdrive": gdrive,
    "Rclone": rclone_cl,
}

RSS_HELP_MESSAGE = """
Gunakan format ini untuk menambahkan url feed:
Judul1 link (wajib)
Judul2 link -c cmd -inf xx -exf xx
Judul3 link -c cmd -d rasio:waktu -z kata_sandi

-c perintah -up mrcc:remote:path/subdir -rcf --buffer-size:8M|kunci|kunci:nilai
-inf Untuk filter kata yang disertakan (included words).
-exf Untuk filter kata yang dikecualikan (excluded words).
-stv true atau false (filter case sensitive)

Contoh: Judul https://www.url-rss.com -inf 1080 atau 720 atau 144p|mkv atau mp4|hevc -exf flv atau web|xxx
Filter ini akan mengambil tautan yang judulnya mengandung `(1080 atau 720 atau 144p) dan (mkv atau mp4) dan hevc` dan tidak mengandung kata (flv atau web) dan xxx. Kamu bisa menambahkan apapun sesukamu.

Contoh lain: -inf  1080  atau 720p|.web. atau .webrip.|hvec atau x264. Ini akan mengambil judul yang mengandung ( 1080  atau 720p) dan (.web. atau .webrip.) dan (hvec atau x264). Saya telah menambahkan spasi sebelum dan sesudah 1080 untuk menghindari pencocokan yang salah. Jika ada angka `10805695` di judul, itu akan cocok dengan 1080 jika ditambahkan 1080 tanpa spasi sesudahnya.

Catatan Filter:
1. | artinya dan.
2. Tambahkan `atau` di antara kunci yang serupa, kamu bisa menambahkannya di antara kualitas atau ekstensi, jadi jangan gunakan filter seperti ini f: 1080|mp4 atau 720|web karena ini akan mengambil 1080 dan (mp4 atau 720) dan web ... bukan (1080 dan mp4) atau (720 dan web).
3. Kamu bisa menambahkan `atau` dan `|` sebanyak yang kamu mau.
4. Perhatikan judul jika memiliki karakter spesial statis sesudah atau sebelum kualitas/ekstensi dan gunakan di filter untuk mencegah pencocokan yang salah.
Waktu Habis: 60 dtk.
"""

PASSWORD_ERROR_MESSAGE = """
<b>Tautan ini membutuhkan kata sandi!</b>
- Sisipkan <b>::</b> setelah tautan dan tulis kata sandi setelah tanda tersebut.

<b>Contoh:</b> link::kata sandi saya
"""


def get_bot_commands():
    from ...core.plugin_manager import get_plugin_manager

    static_commands = {
        "Mirror": "[link/file] Mirror ke Tujuan Unggahan",
        "QbMirror": "[magnet/torrent] Mirror ke Tujuan Unggahan menggunakan qbit",
        "Ytdl": "[link] Mirror YouTube, m3u8, Media Sosial dan url yang didukung yt-dlp",
        "UpHoster": "[link/file] Unggah ke Server DDL",
        "Leech": "[link/file] Leech file untuk Diunggah ke Telegram",
        "QbLeech": "[magnet/torrent] Leech file untuk Diunggah ke Telegram menggunakan qbit",
        "YtdlLeech": "[link] Leech YouTube, m3u8, Media Sosial dan url yang didukung yt-dlp",
        "Clone": "[link] Kloning (Clone) file/folder ke GDrive",
        "UserSet": "Pengaturan pribadi pengguna",
        "ForceStart": "[gid/balasan] Mulai paksa dari tugas dalam antrean",
        "Count": "[link] Hitung jumlah file/folder di GDrive",
        "List": "[kueri] Cari Teks apapun yang tersedia di GDrive",
        "Search": "[kueri] Cari torrent via Plugin Qbit",
        "MediaInfo": "[balasan/link] Dapatkan MediaInfo dari Target Media",
        "Select": "[gid/balasan] Pilih file untuk Tugas NZB, Aria2, Qbit",
        "Ping": "Ping Bot untuk menguji Kecepatan Respons",
        "Status": "[id/me] Status Tugas Bot",
        "Stats": "Statistik lengkap Bot, OS, Repositori & Sistem",
        "Rss": "Pengaturan Manajemen RSS Pengguna",
        "IMDB": "[kueri] atau ttxxxxxx Dapatkan info IMDB",
        "CancelAll": "Batalkan semua Tugas pada Bot",
        "Help": "Panduan penggunaan rinci dari Bot WZ",
        "BotSet": "[SUDO] Pengaturan Manajemen Bot",
        "Log": "[SUDO] Dapatkan Log Bot untuk Pengecekan Internal",
        "Restart": "[SUDO] Muat ulang (Reboot) bot",
        "RestartSessions": "[SUDO] Muat ulang (Reboot) Sesi Pengguna",
    }

    commands = static_commands.copy()

    plugin_manager = get_plugin_manager()
    if plugin_manager:
        for plugin_info in plugin_manager.list_plugins():
            if plugin_info.enabled and plugin_info.commands:
                for cmd in plugin_info.commands:
                    if cmd == "speedtest":
                        commands["SpeedTest"] = "Cek Kecepatan Bot menggunakan Speedtest.com"

    return commands


BOT_COMMANDS = get_bot_commands()


def get_help_string():
    from ..telegram_helper.bot_commands import BotCommands

    help_lines = ["CATATAN: Coba setiap perintah tanpa argumen apapun untuk melihat rincian lebih lanjut."]

    commands = BotCommands.get_commands()

    for key, cmds in commands.items():
        cmd_attr = getattr(BotCommands, f"{key}Command", None)
        if not cmd_attr:
            continue

        if isinstance(cmd_attr, list):
            cmd_str = f"/{' atau /'.join(cmd_attr)}"
        else:
            cmd_str = f"/{cmd_attr}"

        if key == "SpeedTest" and key in BOT_COMMANDS:
            help_lines.append(f"{cmd_str}: Cek Kecepatan Bot menggunakan Speedtest.com")
        elif key == "Mirror":
            help_lines.append(f"{cmd_str}: Mulai mirroring ke cloud.")
        elif key == "QbMirror":
            help_lines.append(f"{cmd_str}: Mulai Mirroring ke cloud menggunakan qBittorrent.")
        elif key == "JdMirror":
            help_lines.append(f"{cmd_str}: Mulai Mirroring ke cloud menggunakan JDownloader.")
        elif key == "NzbMirror":
            help_lines.append(f"{cmd_str}: Mulai Mirroring ke cloud menggunakan Sabnzbd.")
        elif key == "Ytdl":
            help_lines.append(f"{cmd_str}: Mirror tautan yang didukung yt-dlp.")
        elif key == "UpHoster":
            help_lines.append(f"{cmd_str}: Unggah ke Server DDL.")
        elif key == "Leech":
            help_lines.append(f"{cmd_str}: Mulai leeching ke Telegram.")
        elif key == "QbLeech":
            help_lines.append(f"{cmd_str}: Mulai leeching menggunakan qBittorrent.")
        elif key == "JdLeech":
            help_lines.append(f"{cmd_str}: Mulai leeching menggunakan JDownloader.")
        elif key == "NzbLeech":
            help_lines.append(f"{cmd_str}: Mulai leeching menggunakan Sabnzbd.")
        elif key == "YtdlLeech":
            help_lines.append(f"{cmd_str}: Leech tautan yang didukung yt-dlp.")
        elif key == "Clone":
            help_lines.append(
                f"{cmd_str} [url_drive]: Salin file/folder ke Google Drive."
            )
        elif key == "Count":
            help_lines.append(
                f"{cmd_str} [url_drive]: Hitung file/folder dari Google Drive."
            )
        elif key == "Delete":
            help_lines.append(
                f"{cmd_str} [url_drive]: Hapus file/folder dari Google Drive (Hanya Owner & Sudo)."
            )
        elif key == "UserSet":
            help_lines.append(f"{cmd_str} [kueri]: Pengaturan pengguna.")
        elif key == "BotSet":
            help_lines.append(f"{cmd_str} [kueri]: Pengaturan bot.")
        elif key == "Select":
            help_lines.append(
                f"{cmd_str}: Pilih file dari torrent atau nzb dengan gid atau balasan."
            )
        elif key == "CancelTask":
            help_lines.append(f"{cmd_str} [gid]: Batalkan tugas dengan gid atau balasan.")
        elif key == "ForceStart":
            help_lines.append(f"{cmd_str} [gid]: Mulai paksa tugas dengan gid atau balasan.")
        elif key == "CancelAll":
            help_lines.append(f"{cmd_str} [kueri]: Batalkan semua tugas [status].")
        elif key == "List":
            help_lines.append(f"{cmd_str} [kueri]: Cari di Google Drive.")
        elif key == "Search":
            help_lines.append(f"{cmd_str} [kueri]: Cari torrent dengan API.")
        elif key == "MediaInfo":
            help_lines.append(f"{cmd_str} [kueri]: Dapatkan info media.")
        elif key == "Status":
            help_lines.append(f"{cmd_str}: Menampilkan status dari semua unduhan.")
        elif key == "Stats":
            help_lines.append(
                f"{cmd_str}: Tampilkan statistik dari mesin tempat bot dijalankan."
            )
        elif key == "Ping":
            help_lines.append(
                f"{cmd_str}: Cek berapa lama waktu yang dibutuhkan untuk Ping Bot (Hanya Owner & Sudo)."
            )
        elif key == "Authorize":
            help_lines.append(
                f"{cmd_str}: Otorisasi sebuah obrolan atau pengguna untuk memakai bot (Hanya Owner & Sudo)."
            )
        elif key == "UnAuthorize":
            help_lines.append(
                f"{cmd_str}: Cabut otorisasi obrolan atau pengguna untuk memakai bot (Hanya Owner & Sudo)."
            )
        elif key == "Users":
            help_lines.append(f"{cmd_str}: tampilkan pengaturan pengguna (Hanya Owner & Sudo).")
        elif key == "AddSudo":
            help_lines.append(f"{cmd_str}: Tambahkan pengguna sudo (Hanya Owner).")
        elif key == "RmSudo":
            help_lines.append(f"{cmd_str}: Hapus pengguna sudo (Hanya Owner).")
        elif key == "Restart":
            help_lines.append(
                f"{cmd_str}: Mulai ulang dan perbarui bot (Hanya Owner & Sudo)."
            )
        elif key == "Log":
            help_lines.append(
                f"{cmd_str}: Dapatkan file log dari bot. Berguna untuk mendapatkan laporan crash (Hanya Owner & Sudo)."
            )
        elif key == "Shell":
            help_lines.append(f"{cmd_str}: Jalankan perintah shell (Hanya Owner).")
        elif key == "AExec":
            help_lines.append(f"{cmd_str}: Eksekusi fungsi async (Hanya Owner).")
        elif key == "Exec":
            help_lines.append(f"{cmd_str}: Eksekusi fungsi sync (Hanya Owner).")
        elif key == "ClearLocals":
            help_lines.append(
                f"/{BotCommands.ClearLocalsCommand}: Bersihkan lokal {BotCommands.AExecCommand} atau {BotCommands.ExecCommand} (Hanya Owner)."
            )
        elif key == "Rss":
            help_lines.append(f"/{BotCommands.RssCommand}: Menu RSS.")

    return "\n".join(help_lines)


help_string = get_help_string()
