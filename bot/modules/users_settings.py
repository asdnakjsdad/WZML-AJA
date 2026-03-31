from asyncio import sleep
from functools import partial
from html import escape
from io import BytesIO
from os import getcwd
from re import sub
from time import time

from aiofiles.os import makedirs, remove
from aiofiles.os import path as aiopath
from langcodes import Language
from pyrogram.filters import create
from pyrogram.handlers import MessageHandler

from bot.helper.ext_utils.status_utils import get_readable_file_size

from .. import auth_chats, excluded_extensions, sudo_users, user_data
from ..core.config_manager import Config
from ..core.tg_client import TgClient
from ..helper.ext_utils.bot_utils import (
    get_size_bytes,
    new_task,
    update_user_ldata,
)
from ..helper.ext_utils.db_handler import database
from ..helper.ext_utils.media_utils import create_thumb
from ..helper.telegram_helper.button_build import ButtonMaker
from ..helper.telegram_helper.message_utils import (
    delete_message,
    edit_message,
    send_file,
    send_message,
)

handler_dict = {}

leech_options = [
    "THUMBNAIL",
    "LEECH_SPLIT_SIZE",
    "LEECH_DUMP_CHAT",
    "LEECH_PREFIX",
    "LEECH_SUFFIX",
    "LEECH_CAPTION",
    "THUMBNAIL_LAYOUT",
]
uphoster_options = [
    "GOFILE_TOKEN",
    "GOFILE_FOLDER_ID",
    "BUZZHEAVIER_TOKEN",
    "BUZZHEAVIER_FOLDER_ID",
    "PIXELDRAIN_KEY",
]
rclone_options = ["RCLONE_CONFIG", "RCLONE_PATH", "RCLONE_FLAGS"]
gdrive_options = ["TOKEN_PICKLE", "GDRIVE_ID", "INDEX_URL"]
ffset_options = [
    "FFMPEG_CMDS",
    "METADATA",
    "AUDIO_METADATA",
    "VIDEO_METADATA",
    "SUBTITLE_METADATA",
]
advanced_options = [
    "EXCLUDED_EXTENSIONS",
    "NAME_SWAP",
    "YT_DLP_OPTIONS",
    "UPLOAD_PATHS",
    "USER_COOKIE_FILE",
]
yt_options = ["YT_DESP", "YT_TAGS", "YT_CATEGORY_ID", "YT_PRIVACY_STATUS"]

user_settings_text = {
    "THUMBNAIL": (
        "Foto atau Dokumen",
        "Thumbnail Kustom digunakan sebagai gambar sampul untuk file yang kamu unggah ke Telegram dalam mode media atau dokumen.",
        "<i>Kirim sebuah foto untuk menyimpannya sebagai thumbnail kustom.</i> \n┖ <b>Sisa Waktu :</b> <code>60 dtk</code>",
    ),
    "RCLONE_CONFIG": (
        "",
        "",
        "<i>Kirim file <code>rclone.conf</code> milikmu untuk digunakan sebagai Tujuan Unggah ke RClone.</i> \n┖ <b>Sisa Waktu :</b> <code>60 dtk</code>",
    ),
    "TOKEN_PICKLE": (
        "",
        "",
        "<i>Kirim file <code>token.pickle</code> milikmu untuk digunakan sebagai Tujuan Unggah ke GDrive.</i> \n┖ <b>Sisa Waktu :</b> <code>60 dtk</code>",
    ),
    "LEECH_SPLIT_SIZE": (
        "",
        "",
        f"Kirim ukuran pecahan Leech dalam bytes atau gunakan gb/mb. Contoh: 40000000 atau 2.5gb atau 1000mb. PENGGUNA_PREMIUM: {TgClient.IS_PREMIUM_USER}.</i> \n┖ <b>Sisa Waktu :</b> <code>60 dtk</code>",
    ),
    "LEECH_DUMP_CHAT": (
        "",
        "",
        """Kirim ID/USERNAME/PM tujuan leech. 
* b:id/@username/pm (b: berarti leech oleh bot) (id atau username obrolan, atau tulis pm yang berarti pesan pribadi agar bot mengirimkan file secara pribadi kepadamu). Kapan harus menggunakan b: (leech oleh bot)? Saat pengaturan default kamu adalah leech oleh pengguna, namun kamu ingin menggunakan bot untuk tugas tertentu.
* u:id/@username (u: berarti leech oleh pengguna) Digunakan jika OWNER menambahkan USER_STRING_SESSION.
* h:id/@username (hybrid leech) h: untuk mengunggah file oleh bot dan pengguna berdasarkan ukuran file.
* id/@username|topic_id (leech di obrolan dan topik tertentu) tambahkan | tanpa spasi dan tulis id topik setelah id atau username obrolan.
┖ <b>Sisa Waktu :</b> <code>60 dtk</code>""",
    ),
    "LEECH_PREFIX": (
        "",
        "",
        "Kirim Awalan (Prefix) Nama File Leech. Kamu bisa menambahkan tag HTML. Contoh: <code>@channelku</code>.</i> \n┖ <b>Sisa Waktu :</b> <code>60 dtk</code>",
    ),
    "LEECH_SUFFIX": (
        "",
        "",
        "Kirim Akhiran (Suffix) Nama File Leech. Kamu bisa menambahkan tag HTML. Contoh: <code>@channelku</code>.</i> \n┖ <b>Sisa Waktu :</b> <code>60 dtk</code>",
    ),
    "LEECH_CAPTION": (
        "",
        "",
        "Kirim Keterangan (Caption) Leech. Kamu bisa menambahkan tag HTML. Contoh: <code>@channelku</code>.</i> \n┖ <b>Sisa Waktu :</b> <code>60 dtk</code>",
    ),
    "THUMBNAIL_LAYOUT": (
        "",
        "",
        "Kirim tata letak thumbnail (lebarxtinggi, 2x2, 3x3, 2x4, 4x4, ...). Contoh: 3x3.</i> \n┖ <b>Sisa Waktu :</b> <code>60 dtk</code>",
    ),
    "RCLONE_PATH": (
        "",
        "",
        "Kirim Path Rclone. Jika ingin menggunakan rclone config, edit menggunakan token owner/user dari usetting atau tambahkan mrcc: sebelum path rclone. Contoh: mrcc:remote:folder. </i> \n┖ <b>Sisa Waktu :</b> <code>60 dtk</code>",
    ),
    "RCLONE_FLAGS": (
        "",
        "",
        "kunci:nilai|kunci|kunci|kunci:nilai. Cek di sini untuk semua <a href='https://rclone.org/flags/'>Bendera (Flags) Rclone</a>\nContoh: --buffer-size:8M|--drive-starred-only",
    ),
    "GDRIVE_ID": (
        "",
        "",
        "Kirim ID Gdrive. Jika ingin menggunakan token.pickle, edit menggunakan token owner/user dari usetting atau tambahkan mtp: sebelum id. Contoh: mtp:F435RGGRDXXXXXX . </i> \n┖ <b>Sisa Waktu :</b> <code>60 dtk</code>",
    ),
    "INDEX_URL": (
        "",
        "",
        "Kirim URL Index untuk opsi gdrive-mu. </i> \n┖ <b>Sisa Waktu :</b> <code>60 dtk</code>",
    ),
    "UPLOAD_PATHS": (
        "",
        "",
        "Kirim Dict berisi kunci yang memiliki nilai path. Contoh: {'jalur 1': 'remote:folder_rclone', 'jalur 2': 'id gdrive1', 'jalur 3': 'id obrolan tg', 'jalur 4': 'mrcc:remote:', 'jalur 5': b:@username} . </i> \n┖ <b>Sisa Waktu :</b> <code>60 dtk</code>",
    ),
    "EXCLUDED_EXTENSIONS": (
        "",
        "",
        "Kirim ekstensi yang dikecualikan, dipisahkan dengan spasi tanpa titik di awal. </i> \n┖ <b>Sisa Waktu :</b> <code>60 dtk</code>",
    ),
    "NAME_SWAP": (
        "",
        "",
        """<i>Kirim format Penukaran Nama (Name Swap) kamu. Kamu bisa menambahkan pola (pattern) alih-alih teks normal sesuai dengan format.</i>
<b>Panduan Dokumentasi Lengkap</b> <a href="https://t.me/WZML_X/77">Klik Di Sini</a>
┖ <b>Sisa Waktu :</b> <code>60 dtk</code>
""",
    ),
    "YT_DLP_OPTIONS": (
        "",
        "",
        """Format: {kunci: nilai, kunci: nilai, kunci: nilai}.
Contoh: {"format": "bv*+mergeall[vcodec=none]", "nocheckcertificate": True, "playliststart": 10, "fragment_retries": float("inf"), "matchtitle": "S13", "writesubtitles": True, "live_from_start": True, "postprocessor_args": {"ffmpeg": ["-threads", "4"]}, "wait_for_video": (5, 100), "download_ranges": [{"start_time": 0, "end_time": 10}]}
Cek semua opsi API yt-dlp dari <a href='https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/YoutubeDL.py#L184'>FILE</a> ini atau gunakan <a href='https://t.me/mltb_official_channel/177'>skrip</a> ini untuk mengonversi argumen CLI ke opsi API.

<i>Kirim dict Opsi YT-DLP sesuai format.</i> \n┖ <b>Sisa Waktu :</b> <code>60 dtk</code>""",
    ),
    "FFMPEG_CMDS": (
        "",
        "",
        """Dict dari nilai daftar perintah ffmpeg. Kamu bisa mengatur beberapa perintah ffmpeg untuk semua file sebelum diunggah. Jangan tulis ffmpeg di awal, langsung mulai dengan argumennya.
Contoh: {"subtitle": ["-i mltb.mkv -c copy -c:s srt mltb.mkv", "-i mltb.video -c copy -c:s srt mltb"], "convert": ["-i mltb.m4a -c:a libmp3lame -q:a 2 mltb.mp3", "-i mltb.audio -c:a libmp3lame -q:a 2 mltb.mp3"], extract: ["-i mltb -map 0:a -c copy mltb.mka -map 0:s -c copy mltb.srt"]}
Catatan:
- Tambahkan `-del` ke daftar perintah jika kamu ingin bot menghapus file asli setelah perintah selesai dijalankan!
- Untuk mengeksekusi salah satu dari daftar tersebut, misalnya, kamu harus menggunakan -ff subtitle (kunci daftar) atau -ff convert (kunci daftar).
Penjelasan penggunaan mltb.* yang mereferensikan file yang ingin dikerjakan:
1. Perintah pertama: input mltb.mkv, jadi perintah ini hanya bekerja pada video mkv dan outputnya juga mltb.mkv. -del akan menghapus media asli setelah selesai.
2. Perintah kedua: input mltb.video, jadi perintah ini bekerja pada semua video dan outputnya hanya mltb (ekstensi sama dengan input).
3. Perintah ketiga: input mltb.m4a, jadi perintah ini hanya bekerja pada audio m4a dan outputnya mltb.mp3.
4. Perintah keempat: input mltb.audio, jadi perintah ini bekerja pada semua audio dan outputnya mltb.mp3.

<i>Kirim dict Opsi FFMPEG_CMDS sesuai format.</i> \n┖ <b>Sisa Waktu :</b> <code>60 dtk</code>
""",
    ),
    "METADATA_CMDS": (
        "",
        "",
        """<i>Kirim Metadata kamu. Kamu bisa menuliskannya sesuai format title="Bergabunglah dengan @WZML_X".</i>
<b>Panduan Dokumentasi Lengkap</b> <a href="https://t.me/WZML_X/">Klik Di Sini</a>
┖ <b>Sisa Waktu :</b> <code>60 dtk</code>
""",
    ),
    "METADATA": (
        "🏷 Metadata Global (kunci=nilai|kunci=nilai)",
        "Terapkan metadata ke semua file media dengan variabel dinamis.",
        """<i>📝 Kirim metadata sebagai</i> <code>kunci=nilai|kunci2=nilai2</code>

<b>🔧 Variabel Dinamis:</b>
• <code>{filename}</code> - Nama file asli
• <code>{basename}</code> - Nama tanpa ekstensi
• <code>{audiolang}</code> - Bahasa audio (Inggris/Indonesia dll.)
• <code>{year}</code> - Tahun dari nama file

<b>📋 Contoh:</b>
<code>title={basename}|artist={audiolang} Version|year={year}</code>

⏱ <b>Sisa Waktu:</b> <code>60 dtk</code>""",
    ),
    "AUDIO_METADATA": (
        "🎵 Metadata Track Audio",
        "Metadata diterapkan pada setiap track audio secara terpisah.",
        """<i>🎧 Metadata track audio dengan dukungan bahasa per-track</i>

<b>📋 Contoh:</b>
<code>language={audiolang}|title=Audio - {audiolang}</code>

⏱ <b>Sisa Waktu:</b> <code>60 dtk</code>""",
    ),
    "VIDEO_METADATA": (
        "🎥 Metadata Stream Video",
        "Metadata diterapkan pada stream video.",
        """<i>📹 Metadata stream video untuk track visual</i>

<b>📋 Contoh:</b>
<code>title={basename}|comment=Video HD</code>

⏱ <b>Sisa Waktu:</b> <code>60 dtk</code>""",
    ),
    "SUBTITLE_METADATA": (
        "💬 Metadata Stream Subtitle",
        "Metadata diterapkan pada setiap track subtitle secara terpisah.",
        """<i>📄 Metadata stream subtitle dengan dukungan bahasa per-track</i>

<b>📋 Contoh:</b>
<code>language={sublang}|title=Subtitle - {sublang}</code>

⏱ <b>Sisa Waktu:</b> <code>60 dtk</code>""",
    ),
    "YT_DESP": (
        "String",
        "Deskripsi kustom untuk unggahan YouTube. Default akan digunakan jika tidak diatur.",
        "<i>Kirim deskripsi YouTube kustom milikmu.</i> \nSisa Waktu : <code>60 dtk</code>",
    ),
    "YT_TAGS": (
        "String yang dipisahkan koma",
        "Tag kustom untuk unggahan YouTube (contoh: tag1,tag2,tag3). Default akan digunakan jika tidak diatur.",
        "<i>Kirim tag YouTube kustom kamu sebagai daftar yang dipisahkan koma.</i> \nSisa Waktu : <code>60 dtk</code>",
    ),
    "YT_CATEGORY_ID": (
        "Angka",
        "ID kategori kustom untuk unggahan YouTube. Default akan digunakan jika tidak diatur.",
        "<i>Kirim ID kategori YouTube kustom kamu (contoh: 22).</i> \nSisa Waktu : <code>60 dtk</code>",
    ),
    "YT_PRIVACY_STATUS": (
        "public, private, atau unlisted",
        "Status privasi kustom untuk unggahan YouTube. Default akan digunakan jika tidak diatur.",
        "<i>Kirim status privasi YouTube kustom kamu (public, private, atau unlisted).</i> \nSisa Waktu : <code>60 dtk</code>",
    ),
