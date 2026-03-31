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
    "USER_COOKIE_FILE": (
        "File",
        "File Cookie YT-DLP pengguna untuk mengautentikasi akses ke situs web dan YouTube.",
        "<i>Kirim file cookie kamu (contoh: cookies.txt atau abc.txt).</i> \n┖ <b>Sisa Waktu :</b> <code>60 dtk</code>",
    ),
    "GOFILE_TOKEN": (
        "String",
        "Token API Gofile",
        "<i>Kirim Token API Gofile kamu.</i> \n┖ <b>Sisa Waktu :</b> <code>60 dtk</code>",
    ),
    "GOFILE_FOLDER_ID": (
        "String",
        "ID Folder Gofile",
        "<i>Kirim ID Folder Gofile kamu. Jika kosong, akan diunggah ke Root.</i> \n┖ <b>Sisa Waktu :</b> <code>60 dtk</code>",
    ),
    "BUZZHEAVIER_TOKEN": (
        "String",
        "Token API BuzzHeavier",
        "<i>Kirim Token API BuzzHeavier (ID Akun) kamu.</i> \n┖ <b>Sisa Waktu :</b> <code>60 dtk</code>",
    ),
    "BUZZHEAVIER_FOLDER_ID": (
        "String",
        "ID Folder BuzzHeavier",
        "<i>Kirim ID Folder BuzzHeavier kamu.</i> \n┖ <b>Sisa Waktu :</b> <code>60 dtk</code>",
    ),
    "PIXELDRAIN_KEY": (
        "String",
        "Kunci API PixelDrain",
        "<i>Kirim Kunci API PixelDrain kamu.</i> \n┖ <b>Sisa Waktu :</b> <code>60 dtk</code>",
    ),
}


async def get_user_settings(from_user, stype="main"):
    user_id = from_user.id
    user_name = from_user.mention(style="html") if hasattr(from_user, 'mention') else f"<b>{from_user.title}</b>"
    buttons = ButtonMaker()
    rclone_conf = f"rclone/{user_id}.conf"
    token_pickle = f"tokens/{user_id}.pickle"
    user_dict = user_data.get(user_id, {})

    if stype == "main":
        buttons.data_button(
            "Pengaturan Umum", f"userset {user_id} general", position="header"
        )
        buttons.data_button("Pengaturan Mirror", f"userset {user_id} mirror")
        buttons.data_button("Pengaturan Leech", f"userset {user_id} leech")
        buttons.data_button("Pengaturan Uphoster", f"userset {user_id} uphoster")
        buttons.data_button("Pengaturan Media FF", f"userset {user_id} ffset")
        buttons.data_button(
            "Pengaturan Lanjutan", f"userset {user_id} advanced", position="l_body"
        )

        if user_dict and any(
            key in user_dict
            for key in list(user_settings_text.keys())
            + [
                "USER_TOKENS",
                "AS_DOCUMENT",
                "EQUAL_SPLITS",
                "MEDIA_GROUP",
                "USER_TRANSMISSION",
                "HYBRID_LEECH",
                "STOP_DUPLICATE",
                "DEFAULT_UPLOAD",
            ]
        ):
            buttons.data_button(
                "Reset Semua", f"userset {user_id} confirm_reset_all", position="footer"
            )
        buttons.data_button("Tutup", f"userset {user_id} close", position="footer")

        text = f"""⌬ <b>Pengaturan Pengguna :</b>
│
┟ <b>Nama</b> → {user_name}
┠ <b>UserID</b> → #ID{user_id}
┠ <b>Username</b> → @{from_user.username}
┠ <b>Telegram DC</b> → {from_user.dc_id}
┖ <b>Bahasa Telegram</b> → {Language.get(lc).display_name() if (lc := getattr(from_user, 'language_code', None)) else "Tidak Ada"}"""

        btns = buttons.build_menu(2)

    elif stype == "general":
        if user_dict.get("DEFAULT_UPLOAD", ""):
            default_upload = user_dict["DEFAULT_UPLOAD"]
        elif "DEFAULT_UPLOAD" not in user_dict:
            default_upload = Config.DEFAULT_UPLOAD
        du = "API GDRIVE" if default_upload == "gd" else "RCLONE"
        dur = "API GDRIVE" if default_upload != "gd" else "RCLONE"
        buttons.data_button(
            f"Ganti Mode ke {dur}", f"userset {user_id} {default_upload}"
        )

        user_tokens = user_dict.get("USER_TOKENS", False)
        tr = "USER" if user_tokens else "OWNER"
        trr = "OWNER" if user_tokens else "USER"
        buttons.data_button(
            f"Ganti ke token/config {trr}",
            f"userset {user_id} tog USER_TOKENS {'f' if user_tokens else 't'}",
        )

        buttons.data_button("Kembali", f"userset {user_id} back", "footer")
        buttons.data_button("Tutup", f"userset {user_id} close", "footer")

        def_cookies = user_dict.get("USE_DEFAULT_COOKIE", False)
        cookie_mode = "Cookie Owner" if def_cookies else "Cookie Pengguna"
        buttons.data_button(
            f"Ganti ke File Cookie {'OWNER' if not def_cookies else 'USER'}",
            f"userset {user_id} tog USE_DEFAULT_COOKIE {'f' if def_cookies else 't'}",
        )
        btns = buttons.build_menu(1)

        text = f"""⌬ <b>Pengaturan Umum :</b>
┟ <b>Nama</b> → {user_name}
┃
┠ <b>Paket Unggah Default</b> → <b>{du}</b>
┠ <b>Mode Penggunaan Default</b> → token/config milik <b>{tr}</b>
┖ <b>Mode Cookies YT</b> → <b>{cookie_mode}</b>
"""

    elif stype == "leech":
        thumbpath = f"thumbnails/{user_id}.jpg"
        buttons.data_button("Thumbnail", f"userset {user_id} menu THUMBNAIL")
        thumbmsg = "Ada" if await aiopath.exists(thumbpath) else "Tidak Ada"
        buttons.data_button(
            "Ukuran Pecah Leech", f"userset {user_id} menu LEECH_SPLIT_SIZE"
        )
        if user_dict.get("LEECH_SPLIT_SIZE", False):
            split_size = user_dict["LEECH_SPLIT_SIZE"]
        else:
            split_size = Config.LEECH_SPLIT_SIZE
        buttons.data_button(
            "Tujuan Leech", f"userset {user_id} menu LEECH_DUMP_CHAT"
        )
        if user_dict.get("LEECH_DUMP_CHAT", False):
            leech_dest = user_dict["LEECH_DUMP_CHAT"]
        elif "LEECH_DUMP_CHAT" not in user_dict and Config.LEECH_DUMP_CHAT:
            leech_dest = Config.LEECH_DUMP_CHAT
        else:
            leech_dest = "Tidak Ada"
        buttons.data_button("Awalan (Prefix) Leech", f"userset {user_id} menu LEECH_PREFIX")
        if user_dict.get("LEECH_PREFIX", False):
            lprefix = user_dict["LEECH_PREFIX"]
        elif "LEECH_PREFIX" not in user_dict and Config.LEECH_PREFIX:
            lprefix = Config.LEECH_PREFIX
        else:
            lprefix = "Tidak Ada"
        buttons.data_button("Akhiran (Suffix) Leech", f"userset {user_id} menu LEECH_SUFFIX")
        if user_dict.get("LEECH_SUFFIX", False):
            lsuffix = user_dict["LEECH_SUFFIX"]
        elif "LEECH_SUFFIX" not in user_dict and Config.LEECH_SUFFIX:
            lsuffix = Config.LEECH_SUFFIX
        else:
            lsuffix = "Tidak Ada"

        buttons.data_button("Keterangan (Caption) Leech", f"userset {user_id} menu LEECH_CAPTION")
        if user_dict.get("LEECH_CAPTION", False):
            lcap = user_dict["LEECH_CAPTION"]
        elif "LEECH_CAPTION" not in user_dict and Config.LEECH_CAPTION:
            lcap = Config.LEECH_CAPTION
        else:
            lcap = "Tidak Ada"

        if (
            user_dict.get("AS_DOCUMENT", False)
            or "AS_DOCUMENT" not in user_dict
            and Config.AS_DOCUMENT
        ):
            ltype = "DOKUMEN"
            buttons.data_button("Kirim Sebagai Media", f"userset {user_id} tog AS_DOCUMENT f")
        else:
            ltype = "MEDIA"
            buttons.data_button(
                "Kirim Sebagai Dokumen", f"userset {user_id} tog AS_DOCUMENT t"
            )
        if (
            user_dict.get("EQUAL_SPLITS", False)
            or "EQUAL_SPLITS" not in user_dict
            and Config.EQUAL_SPLITS
        ):
            buttons.data_button(
                "Matikan Pecahan Setara", f"userset {user_id} tog EQUAL_SPLITS f"
            )
            equal_splits = "Aktif"
        else:
            buttons.data_button(
                "Nyalakan Pecahan Setara", f"userset {user_id} tog EQUAL_SPLITS t"
            )
            equal_splits = "Nonaktif"
        if (
            user_dict.get("MEDIA_GROUP", False)
            or "MEDIA_GROUP" not in user_dict
            and Config.MEDIA_GROUP
        ):
            buttons.data_button(
                "Matikan Grup Media", f"userset {user_id} tog MEDIA_GROUP f"
            )
            media_group = "Aktif"
        else:
            buttons.data_button(
                "Nyalakan Grup Media", f"userset {user_id} tog MEDIA_GROUP t"
            )
            media_group = "Nonaktif"
        if (
            TgClient.IS_PREMIUM_USER
            and user_dict.get("USER_TRANSMISSION", False)
            or "USER_TRANSMISSION" not in user_dict
            and Config.USER_TRANSMISSION
        ):
            buttons.data_button(
                "Leech dengan Bot", f"userset {user_id} tog USER_TRANSMISSION f"
            )
            leech_method = "pengguna"
        elif TgClient.IS_PREMIUM_USER:
            leech_method = "bot"
            buttons.data_button(
                "Leech dengan Pengguna", f"userset {user_id} tog USER_TRANSMISSION t"
            )
        else:
            leech_method = "bot"

        if (
            TgClient.IS_PREMIUM_USER
            and user_dict.get("HYBRID_LEECH", False)
            or "HYBRID_LEECH" not in user_dict
            and Config.HYBRID_LEECH
        ):
            hybrid_leech = "Aktif"
            buttons.data_button(
                "Matikan Hybride Leech", f"userset {user_id} tog HYBRID_LEECH f"
            )
        elif TgClient.IS_PREMIUM_USER:
            hybrid_leech = "Nonaktif"
            buttons.data_button(
                "Nyalakan HYBRID Leech", f"userset {user_id} tog HYBRID_LEECH t"
            )
        else:
            hybrid_leech = "Nonaktif"

        buttons.data_button(
            "Tata Letak Thumbnail", f"userset {user_id} menu THUMBNAIL_LAYOUT"
        )
        if user_dict.get("THUMBNAIL_LAYOUT", False):
            thumb_layout = user_dict["THUMBNAIL_LAYOUT"]
        elif "THUMBNAIL_LAYOUT" not in user_dict and Config.THUMBNAIL_LAYOUT:
            thumb_layout = Config.THUMBNAIL_LAYOUT
        else:
            thumb_layout = "Tidak Ada"

        buttons.data_button("Kembali", f"userset {user_id} back", "footer")
        buttons.data_button("Tutup", f"userset {user_id} close", "footer")
        btns = buttons.build_menu(2)

        text = f"""⌬ <b>Pengaturan Leech :</b>
┟ <b>Nama</b> → {user_name}
┃
┠ Tipe Leech → <b>{ltype}</b>
┠ Thumbnail Kustom → <b>{thumbmsg}</b>
┠ Ukuran Pecah Leech → <b>{get_readable_file_size(split_size)}</b>
┠ Pecahan Setara → <b>{equal_splits}</b>
┠ Grup Media → <b>{media_group}</b>
┠ Awalan (Prefix) Leech → <code>{escape(lprefix)}</code>
┠ Akhiran (Suffix) Leech → <code>{escape(lsuffix)}</code>
┠ Keterangan (Caption) Leech → <code>{escape(lcap)}</code>
┠ Tujuan Leech → <code>{leech_dest}</code>
┠ Leech menggunakan sesi <b>{leech_method}</b>
┠ Leech Campuran → <b>{hybrid_leech}</b>
┖ Tata Letak Thumbnail → <b>{thumb_layout}</b>
"""

    elif stype == "uphoster":
        uphoster_service = user_dict.get("UPHOSTER_SERVICE", "gofile")
        buttons.data_button(
            "Ubah Tujuan ⇋",
            f"userset {user_id} uphoster_destinations",
        )
        buttons.data_button("Alat Gofile", f"userset {user_id} gofile")
        buttons.data_button("Alat BuzzHeavier", f"userset {user_id} buzzheavier")
        buttons.data_button("Alat PixelDrain", f"userset {user_id} pixeldrain")
        buttons.data_button("Kembali", f"userset {user_id} back", "footer")
        buttons.data_button("Tutup", f"userset {user_id} close", "footer")
        btns = buttons.build_menu(1)

        destinations = [s.capitalize() for s in uphoster_service.split(",")]
        text = f"""⌬ <b>Pengaturan Uphoster :</b>
┟ <b>Nama</b> → {user_name}
┃
┖ <b>Tujuan Saat Ini</b> → {', '.join(destinations)}"""

    elif stype == "pixeldrain":
        buttons.data_button("Kunci PixelDrain", f"userset {user_id} menu PIXELDRAIN_KEY")
        buttons.data_button("Kembali", f"userset {user_id} back uphoster", "footer")
        buttons.data_button("Tutup", f"userset {user_id} close", "footer")
        btns = buttons.build_menu(1)

        if user_dict.get("PIXELDRAIN_KEY", False):
            pdtoken = user_dict["PIXELDRAIN_KEY"]
        elif Config.PIXELDRAIN_KEY:
            pdtoken = Config.PIXELDRAIN_KEY
        else:
            pdtoken = "Tidak Ada"

        text = f"""⌬ <b>Pengaturan PixelDrain :</b>
┟ <b>Nama</b> → {user_name}
┃
┖ <b>Kunci PixelDrain</b> → <code>{pdtoken}</code>"""

    elif stype == "buzzheavier":
        buttons.data_button(
            "Token BuzzHeavier", f"userset {user_id} menu BUZZHEAVIER_TOKEN"
        )
        buttons.data_button(
            "ID Folder BuzzHeavier", f"userset {user_id} menu BUZZHEAVIER_FOLDER_ID"
        )
        buttons.data_button("Kembali", f"userset {user_id} back uphoster", "footer")
        buttons.data_button("Tutup", f"userset {user_id} close", "footer")
        btns = buttons.build_menu(1)

        if user_dict.get("BUZZHEAVIER_TOKEN", False):
            bztoken = user_dict["BUZZHEAVIER_TOKEN"]
        elif Config.BUZZHEAVIER_API:
            bztoken = Config.BUZZHEAVIER_API
        else:
            bztoken = "Tidak Ada"

        if user_dict.get("BUZZHEAVIER_FOLDER_ID", False):
            bzfolder = user_dict["BUZZHEAVIER_FOLDER_ID"]
        else:
            bzfolder = "Tidak Ada"

        text = f"""⌬ <b>Pengaturan BuzzHeavier :</b>
┟ <b>Nama</b> → {user_name}
┃
┠ <b>Token BuzzHeavier</b> → <code>{bztoken}</code>
┖ <b>ID Folder BuzzHeavier</b> → <code>{bzfolder}</code>"""

    elif stype == "gofile":
        buttons.data_button("Token Gofile", f"userset {user_id} menu GOFILE_TOKEN")
        buttons.data_button(
            "ID Folder Gofile", f"userset {user_id} menu GOFILE_FOLDER_ID"
        )
        buttons.data_button("Kembali", f"userset {user_id} back uphoster", "footer")
        buttons.data_button("Tutup", f"userset {user_id} close", "footer")
        btns = buttons.build_menu(1)

        if user_dict.get("GOFILE_TOKEN", False):
            gftoken = user_dict["GOFILE_TOKEN"]
        elif Config.GOFILE_API:
            gftoken = Config.GOFILE_API
        else:
            gftoken = "Tidak Ada"

        if user_dict.get("GOFILE_FOLDER_ID", False):
            gffolder = user_dict["GOFILE_FOLDER_ID"]
        elif Config.GOFILE_FOLDER_ID:
            gffolder = Config.GOFILE_FOLDER_ID
        else:
            gffolder = "Tidak Ada (Unggah ke Root)"

        text = f"""⌬ <b>Pengaturan Gofile :</b>
┟ <b>Nama</b> → {user_name}
┃
┠ <b>Token Gofile</b> → <code>{gftoken}</code>
┖ <b>ID Folder Gofile</b> → <code>{gffolder}</code>"""

    elif stype == "rclone":
        buttons.data_button("Konfigurasi Rclone", f"userset {user_id} menu RCLONE_CONFIG")
        buttons.data_button(
            "Path Rclone Default", f"userset {user_id} menu RCLONE_PATH"
        )
        buttons.data_button("Bendera (Flags) Rclone", f"userset {user_id} menu RCLONE_FLAGS")

        buttons.data_button("Kembali", f"userset {user_id} back mirror", "footer")
        buttons.data_button("Tutup", f"userset {user_id} close", "footer")

        rccmsg = "Ada" if await aiopath.exists(rclone_conf) else "Tidak Ada"
        if user_dict.get("RCLONE_PATH", False):
            rccpath = user_dict["RCLONE_PATH"]
        elif Config.RCLONE_PATH:
            rccpath = Config.RCLONE_PATH
        else:
            rccpath = "Tidak Ada"
        btns = buttons.build_menu(1)

        if user_dict.get("RCLONE_FLAGS", False):
            rcflags = user_dict["RCLONE_FLAGS"]
        elif "RCLONE_FLAGS" not in user_dict and Config.RCLONE_FLAGS:
            rcflags = Config.RCLONE_FLAGS
        else:
            rcflags = "Tidak Ada"

        text = f"""⌬ <b>Pengaturan RClone :</b>
┟ <b>Nama</b> → {user_name}
┃
┠ <b>Konfigurasi Rclone</b> → <b>{rccmsg}</b>
┠ <b>Bendera Rclone</b> → <code>{rcflags}</code>
┖ <b>Path Rclone</b> → <code>{rccpath}</code>"""

    elif stype == "gdrive":
        buttons.data_button("token.pickle", f"userset {user_id} menu TOKEN_PICKLE")
        buttons.data_button("ID Gdrive Default", f"userset {user_id} menu GDRIVE_ID")
        buttons.data_button("URL Index", f"userset {user_id} menu INDEX_URL")
        if (
            user_dict.get("STOP_DUPLICATE", False)
            or "STOP_DUPLICATE" not in user_dict
            and Config.STOP_DUPLICATE
        ):
            buttons.data_button(
                "Matikan Blokir Duplikat", f"userset {user_id} tog STOP_DUPLICATE f"
            )
            sd_msg = "Aktif"
        else:
            buttons.data_button(
                "Nyalakan Blokir Duplikat",
                f"userset {user_id} tog STOP_DUPLICATE t",
                "l_body",
            )
            sd_msg = "Nonaktif"
        buttons.data_button("Kembali", f"userset {user_id} back mirror", "footer")
        buttons.data_button("Tutup", f"userset {user_id} close", "footer")

        tokenmsg = "Ada" if await aiopath.exists(token_pickle) else "Tidak Ada"
        if user_dict.get("GDRIVE_ID", False):
            gdrive_id = user_dict["GDRIVE_ID"]
        elif GDID := Config.GDRIVE_ID:
            gdrive_id = GDID
        else:
            gdrive_id = "Tidak Ada"
        index = user_dict["INDEX_URL"] if user_dict.get("INDEX_URL", False) else "Tidak Ada"
        btns = buttons.build_menu(2)

        text = f"""⌬ <b>Pengaturan Alat GDrive :</b>
┟ <b>Nama</b> → {user_name}
┃
┠ <b>Token Gdrive</b> → <b>{tokenmsg}</b>
┠ <b>ID Gdrive</b> → <code>{gdrive_id}</code>
┠ <b>URL Index</b> → <code>{index}</code>
┖ <b>Blokir Duplikat</b> → <b>{sd_msg}</b>"""
    elif stype == "mirror":
        buttons.data_button("Alat RClone", f"userset {user_id} rclone")
        rccmsg = "Ada" if await aiopath.exists(rclone_conf) else "Tidak Ada"
        if user_dict.get("RCLONE_PATH", False):
            rccpath = user_dict["RCLONE_PATH"]
        elif RP := Config.RCLONE_PATH:
            rccpath = RP
        else:
            rccpath = "Tidak Ada"

        buttons.data_button("Alat GDrive", f"userset {user_id} gdrive")
        tokenmsg = "Ada" if await aiopath.exists(token_pickle) else "Tidak Ada"
        if user_dict.get("GDRIVE_ID", False):
            gdrive_id = user_dict["GDRIVE_ID"]
        elif GI := Config.GDRIVE_ID:
            gdrive_id = GI
        else:
            gdrive_id = "Tidak Ada"

        index = user_dict["INDEX_URL"] if user_dict.get("INDEX_URL", False) else "Tidak Ada"
        if (
            user_dict.get("STOP_DUPLICATE", False)
            or "STOP_DUPLICATE" not in user_dict
            and Config.STOP_DUPLICATE
        ):
            sd_msg = "Aktif"
        else:
            sd_msg = "Nonaktif"

        buttons.data_button("Alat Unggah YT", f"userset {user_id} yttools")
        buttons.data_button("Kembali", f"userset {user_id} back", "footer")
        buttons.data_button("Tutup", f"userset {user_id} close", "footer")
        btns = buttons.build_menu(1)

        text = f"""⌬ <b>Pengaturan Mirror :</b>
┟ <b>Nama</b> → {user_name}
┃
┠ <b>Konfigurasi Rclone</b> → <b>{rccmsg}</b>
┠ <b>Path Rclone</b> → <code>{rccpath}</code>
┠ <b>Token Gdrive</b> → <b>{tokenmsg}</b>
┠ <b>ID Gdrive</b> → <code>{gdrive_id}</code>
┠ <b>Tautan Index</b> → <code>{index}</code>
┖ <b>Blokir Duplikat</b> → <b>{sd_msg}</b>
"""

    elif stype == "ffset":
        buttons.data_button(
            "Perintah FFmpeg", f"userset {user_id} menu FFMPEG_CMDS", "header"
        )
        if user_dict.get("FFMPEG_CMDS", False):
            ffc = user_dict["FFMPEG_CMDS"]
        elif "FFMPEG_CMDS" not in user_dict and Config.FFMPEG_CMDS:
            ffc = Config.FFMPEG_CMDS
        else:
            ffc = "<b>Tidak Ada</b>"

        if isinstance(ffc, dict):
            ffc = "\n" + "\n".join(
                [
                    f"{no}. <b>{key}</b>: <code>{escape(str(value[0]))}</code>"
                    for no, (key, value) in enumerate(ffc.items(), start=1)
                ]
            )

        buttons.data_button("Metadata", f"userset {user_id} menu METADATA")
        metadata_setting = user_dict.get("METADATA")
        display_meta_val = "<b>Belum Diatur</b>"
        if isinstance(metadata_setting, dict) and metadata_setting:
            display_meta_val = ", ".join(
                f"{k}={escape(str(v))}" for k, v in metadata_setting.items()
            )
            display_meta_val = f"<code>{display_meta_val}</code>"
        elif isinstance(metadata_setting, str) and metadata_setting:  # Legacy
            display_meta_val = (
                f"<code>{escape(metadata_setting)}</code> [<i>Versi lama, perlu diatur ulang</i>]"
            )

        buttons.data_button("Metadata Audio", f"userset {user_id} menu AUDIO_METADATA")
        audio_meta_setting = user_dict.get("AUDIO_METADATA")
        display_audio_meta = "<b>Belum Diatur</b>"
        if isinstance(audio_meta_setting, dict) and audio_meta_setting:
            display_audio_meta = ", ".join(
                f"{k}={escape(str(v))}" for k, v in audio_meta_setting.items()
            )
            display_audio_meta = f"<code>{display_audio_meta}</code>"

        buttons.data_button("Metadata Video", f"userset {user_id} menu VIDEO_METADATA")
        video_meta_setting = user_dict.get("VIDEO_METADATA")
        display_video_meta = "<b>Belum Diatur</b>"
        if isinstance(video_meta_setting, dict) and video_meta_setting:
            display_video_meta = ", ".join(
                f"{k}={escape(str(v))}" for k, v in video_meta_setting.items()
            )
            display_video_meta = f"<code>{display_video_meta}</code>"

        buttons.data_button(
            "Metadata Subtitle", f"userset {user_id} menu SUBTITLE_METADATA"
        )
        subtitle_meta_setting = user_dict.get("SUBTITLE_METADATA")
        display_subtitle_meta = "<b>Belum Diatur</b>"
        if isinstance(subtitle_meta_setting, dict) and subtitle_meta_setting:
            display_subtitle_meta = ", ".join(
                f"{k}={escape(str(v))}" for k, v in subtitle_meta_setting.items()
            )
            display_subtitle_meta = f"<code>{display_subtitle_meta}</code>"

        buttons.data_button("Kembali", f"userset {user_id} back", "footer")
        buttons.data_button("Tutup", f"userset {user_id} close", "footer")
        btns = buttons.build_menu(2)

        text = f"""⌬ <b>Pengaturan FF :</b>
┟ <b>Nama</b> → {user_name}
┃
┠ <b>Perintah CLI FFmpeg</b> → {ffc}
┃
┠ <b>Metadata Default</b> → {display_meta_val}
┠ <b>Metadata Audio</b> → {display_audio_meta}
┠ <b>Metadata Video</b> → {display_video_meta}
┖ <b>Metadata Subtitle</b> → {display_subtitle_meta}"""

    elif stype == "advanced":
        buttons.data_button(
            "Pengecualian Ekstensi", f"userset {user_id} menu EXCLUDED_EXTENSIONS"
        )
        if user_dict.get("EXCLUDED_EXTENSIONS", False):
            ex_ex = user_dict["EXCLUDED_EXTENSIONS"]
        elif "EXCLUDED_EXTENSIONS" not in user_dict:
            ex_ex = excluded_extensions
        else:
            ex_ex = "Tidak Ada"

        if ex_ex != "Tidak Ada":
            ex_ex = ", ".join(ex_ex)

        ns_msg = (
            f"<code>{swap}</code>"
            if (swap := user_dict.get("NAME_SWAP", False))
            else "<b>Tidak Ada</b>"
        )
        buttons.data_button("Tukar Nama", f"userset {user_id} menu NAME_SWAP")

        buttons.data_button("Opsi YT-DLP", f"userset {user_id} menu YT_DLP_OPTIONS")
        if user_dict.get("YT_DLP_OPTIONS", False):
            ytopt = user_dict["YT_DLP_OPTIONS"]
        elif "YT_DLP_OPTIONS" not in user_dict and Config.YT_DLP_OPTIONS:
            ytopt = Config.YT_DLP_OPTIONS
        else:
            ytopt = "Tidak Ada"

        upload_paths = user_dict.get("UPLOAD_PATHS", {})
        if not upload_paths and "UPLOAD_PATHS" not in user_dict and Config.UPLOAD_PATHS:
            upload_paths = Config.UPLOAD_PATHS
        else:
            upload_paths = "Tidak Ada"
        buttons.data_button("Path Unggah", f"userset {user_id} menu UPLOAD_PATHS")

        yt_cookie_path = f"cookies/{user_id}/cookies.txt"
        user_cookie_msg = (
            "Ada" if await aiopath.exists(yt_cookie_path) else "Tidak Ada"
        )
        buttons.data_button(
            "File Cookie YT", f"userset {user_id} menu USER_COOKIE_FILE"
        )

        buttons.data_button("Kembali", f"userset {user_id} back", "footer")
        buttons.data_button("Tutup", f"userset {user_id} close", "footer")
        btns = buttons.build_menu(1)

        text = f"""⌬ <b>Pengaturan Lanjutan :</b>
┟ <b>Nama</b> → {user_name}
┃
┠ <b>Tukar Nama</b> → {ns_msg}
┠ <b>Ekstensi Dikecualikan</b> → <code>{ex_ex}</code>
┠ <b>Path Unggah</b> → <b>{upload_paths}</b>
┠ <b>Opsi YT-DLP</b> → <code>{ytopt}</code>
┖ <b>File Cookie YT Pengguna</b> → <b>{user_cookie_msg}</b>"""
    elif stype == "yttools":
        buttons.data_button("Deskripsi YT", f"userset {user_id} menu YT_DESP")
        yt_desp_val = user_dict.get(
            "YT_DESP",
            Config.YT_DESP if hasattr(Config, "YT_DESP") else "Belum Diatur (Pakai Default)",
        )

        buttons.data_button("Tag YT", f"userset {user_id} menu YT_TAGS")
        yt_tags_val = user_dict.get(
            "YT_TAGS",
            Config.YT_TAGS if hasattr(Config, "YT_TAGS") else "Belum Diatur (Pakai Default)",
        )
        if isinstance(yt_tags_val, list):
            yt_tags_val = ",".join(yt_tags_val)

        buttons.data_button("ID Kategori YT", f"userset {user_id} menu YT_CATEGORY_ID")
        yt_cat_id_val = user_dict.get(
            "YT_CATEGORY_ID",
            (
                Config.YT_CATEGORY_ID
                if hasattr(Config, "YT_CATEGORY_ID")
                else "Belum Diatur (Pakai Default)"
            ),
        )

        buttons.data_button(
            "Status Privasi YT", f"userset {user_id} menu YT_PRIVACY_STATUS"
        )
        yt_privacy_val = user_dict.get(
            "YT_PRIVACY_STATUS",
            (
                Config.YT_PRIVACY_STATUS
                if hasattr(Config, "YT_PRIVACY_STATUS")
                else "Belum Diatur (Pakai Default)"
            ),
        )

        buttons.data_button("Kembali", f"userset {user_id} back mirror", "footer")
        buttons.data_button("Tutup", f"userset {user_id} close", "footer")
        btns = buttons.build_menu(2)

        text = f"""⌬ <b>Pengaturan Alat YouTube:</b>
┟ <b>Nama</b> → {user_name}
┃
┠ <b>Deskripsi YT</b> → <code>{escape(str(yt_desp_val))}</code>
┠ <b>Tag YT</b> → <code>{escape(str(yt_tags_val))}</code>
┠ <b>ID Kategori YT</b> → <code>{escape(str(yt_cat_id_val))}</code>
┖ <b>Status Privasi YT</b> → <code>{escape(str(yt_privacy_val))}</code>"""

    return text, btns


async def update_user_settings(query, stype="main"):
    handler_dict[query.from_user.id] = False
    msg, button = await get_user_settings(query.from_user, stype)
    await edit_message(query.message, msg, button)


@new_task
async def send_user_settings(_, message):
    from_user = message.from_user if message.from_user else message.sender_chat
    user_id = message.from_user.id if message.from_user else message.sender_chat.id
    handler_dict[user_id] = False
    msg, button = await get_user_settings(from_user)
    await send_message(message, msg, button)


@new_task
async def add_file(_, message, ftype, rfunc):
    user_id = message.from_user.id
    handler_dict[user_id] = False
    if ftype == "THUMBNAIL":
        des_dir = await create_thumb(message, user_id)
    elif ftype == "RCLONE_CONFIG":
        rpath = f"{getcwd()}/rclone/"
        await makedirs(rpath, exist_ok=True)
        des_dir = f"{rpath}{user_id}.conf"
        await message.download(file_name=des_dir)
    elif ftype == "TOKEN_PICKLE":
        tpath = f"{getcwd()}/tokens/"
        await makedirs(tpath, exist_ok=True)
        des_dir = f"{tpath}{user_id}.pickle"
        await message.download(file_name=des_dir)
    elif ftype == "USER_COOKIE_FILE":
        cpath = f"{getcwd()}/cookies/{user_id}"
        await makedirs(cpath, exist_ok=True)
        des_dir = f"{cpath}/cookies.txt"
        await message.download(file_name=des_dir)
    await delete_message(message)
    update_user_ldata(user_id, ftype, des_dir)
    await rfunc()
    await database.update_user_doc(user_id, ftype, des_dir)


@new_task
async def add_one(_, message, option, rfunc):
    user_id = message.from_user.id
    handler_dict[user_id] = False
    user_dict = user_data.get(user_id, {})
    value = message.text
    if value.startswith("{") and value.endswith("}"):
        try:
            value = eval(value)
            if user_dict[option]:
                user_dict[option].update(value)
            else:
                update_user_ldata(user_id, option, value)
        except Exception as e:
            await send_message(message, str(e))
            return
    else:
        await send_message(message, "Harus berupa Dict (Kamus)!")
        return
    await delete_message(message)
    await rfunc()
    await database.update_user_data(user_id)


@new_task
async def remove_one(_, message, option, rfunc):
    user_id = message.from_user.id
    handler_dict[user_id] = False
    user_dict = user_data.get(user_id, {})
    names = message.text.split("/")
    for name in names:
        if name in user_dict[option]:
            del user_dict[option][name]
    await delete_message(message)
    await rfunc()
    await database.update_user_data(user_id)


@new_task
async def set_option(_, message, option, rfunc):
    user_id = message.from_user.id
    handler_dict[user_id] = False
    value = message.text
    if option == "LEECH_SPLIT_SIZE":
        if not value.isdigit():
            value = get_size_bytes(value)
        value = min(int(value), TgClient.MAX_SPLIT_SIZE)
    # elif option == "LEECH_DUMP_CHAT": # TODO: Add
    elif option == "EXCLUDED_EXTENSIONS":
        fx = value.split()
        value = ["aria2", "!qB"]
        for x in fx:
            x = x.lstrip(".")
            value.append(x.strip().lower())
    elif option == "YT_TAGS":
        if isinstance(value, str):
            value = [tag.strip() for tag in value.split(",") if tag.strip()]
        elif not isinstance(value, list):
            await send_message(message, "Tag YT harus berupa string yang dipisahkan oleh koma.")
            return
    elif option == "YT_CATEGORY_ID":
        if isinstance(value, str) and value.isdigit():
            value = int(value)
        elif not isinstance(value, int):
            await send_message(message, "ID Kategori YT harus berupa angka bulat.")
            return
    elif option == "YT_PRIVACY_STATUS":
        allowed_statuses = ["public", "private", "unlisted"]
        if not isinstance(value, str) or value.lower() not in allowed_statuses:
            await send_message(
                message,
                f"Status Privasi YT harus salah satu dari: {', '.join(allowed_statuses)}.",
            )
            return
        value = value.lower()
    elif option in [
        "METADATA",
        "AUDIO_METADATA",
        "VIDEO_METADATA",
        "SUBTITLE_METADATA",
    ]:
        parsed_metadata_dict = {}
        if value and isinstance(value, str):
            if value.strip() == "":
                value = {}
            else:
                parts = []
                current = ""
                i = 0
                while i < len(value):
                    if value[i] == "\\" and i + 1 < len(value) and value[i + 1] == "|":
                        current += "|"
                        i += 2
                    elif value[i] == "|":
                        parts.append(current)
                        current = ""
                        i += 1
                    else:
                        current += value[i]
                        i += 1
                if current:
                    parts.append(current)

                for part in parts:
                    if "=" in part:
                        key, val_str = part.split("=", 1)
                        parsed_metadata_dict[key.strip()] = val_str.strip()
                if not parsed_metadata_dict and value.strip() != "":
                    await send_message(
                        message,
                        "Format string metadata salah. Format: kunci1=nilai1|kunci2=nilai2. Gunakan \\| untuk meniadakan karakter garis vertikal (pipe).",
                    )
                    return
                value = parsed_metadata_dict
        else:
            value = {}

    elif option in ["UPLOAD_PATHS", "FFMPEG_CMDS", "YT_DLP_OPTIONS"]:
        if value.startswith("{") and value.endswith("}"):
            try:
                value = eval(sub(r"\s+", " ", value))
            except Exception as e:
                await send_message(message, str(e))
                return
        else:
            await send_message(message, "Harus berupa dict (kamus)!")
            return
    update_user_ldata(user_id, option, value)
    await delete_message(message)
    await rfunc()
    await database.update_user_data(user_id)


async def get_menu(option, message, user_id):
    handler_dict[user_id] = False
    user_dict = user_data.get(user_id, {})

    file_dict = {
        "THUMBNAIL": f"thumbnails/{user_id}.jpg",
        "RCLONE_CONFIG": f"rclone/{user_id}.conf",
        "TOKEN_PICKLE": f"tokens/{user_id}.pickle",
        "USER_COOKIE_FILE": f"cookies/{user_id}/cookies.txt",
    }

    buttons = ButtonMaker()
    if option in ["THUMBNAIL", "RCLONE_CONFIG", "TOKEN_PICKLE", "USER_COOKIE_FILE"]:
        key = "file"
    else:
        key = "set"
    buttons.data_button(
        "Ubah" if user_dict.get(option, False) else "Atur",
        f"userset {user_id} {key} {option}",
    )
    if user_dict.get(option, False):
        if option == "THUMBNAIL":
            buttons.data_button(
                "Lihat Thumb", f"userset {user_id} view THUMBNAIL", "header"
            )
        elif option in ["YT_DLP_OPTIONS", "FFMPEG_CMDS", "UPLOAD_PATHS"]:
            buttons.data_button(
                "Tambah Satu", f"userset {user_id} addone {option}", "header"
            )
            buttons.data_button(
                "Hapus Satu", f"userset {user_id} rmone {option}", "header"
            )

        if key != "file":  # TODO: option default val check
            buttons.data_button("Reset", f"userset {user_id} reset {option}")
        elif await aiopath.exists(file_dict[option]):
            buttons.data_button("Hapus", f"userset {user_id} remove {option}")
    if option in leech_options:
        back_to = "leech"
    elif option in rclone_options:
        back_to = "rclone"
    elif option in gdrive_options:
        back_to = "gdrive"
    elif option in yt_options:
        back_to = "yttools"
    elif option in ffset_options:
        back_to = "ffset"
    elif option in advanced_options:
        back_to = "advanced"
    else:
        back_to = "back"
    buttons.data_button("Kembali", f"userset {user_id} {back_to}", "footer")
    buttons.data_button("Tutup", f"userset {user_id} close", "footer")
    val = user_dict.get(option)
    if option in file_dict and await aiopath.exists(file_dict[option]):
        val = "<b>Ada</b>"
    elif option == "LEECH_SPLIT_SIZE":
        val = get_readable_file_size(val)
    elif option == "METADATA":
        current_meta_val = user_dict.get(option)
        if isinstance(current_meta_val, dict) and current_meta_val:
            val = ", ".join(
                f"{k}={escape(str(v))}" for k, v in current_meta_val.items()
            )
            val = f"<code>{val}</code>"
        elif isinstance(current_meta_val, str) and current_meta_val:
            val = (
                f"<code>{escape(current_meta_val)}</code> [<i>Versi lama, perlu diatur ulang</i>]"
            )
        elif not current_meta_val:
            val = "<b>Belum Diatur</b>"

        if val is None:
            val = "<b>Tidak Ada</b>"

    if option == "METADATA":
        text = f"""⌬ <b><u>Pengaturan Menu :</u></b>
│
┟ <b>Opsi</b> → {option}
┃
┠ <b>Nilai Opsi</b> → {val if val else "<b>Tidak Ada</b>"}
┃
┠ <b>Tipe Input Default</b> → {user_settings_text[option][0]}
┠ <b>Deskripsi</b> → {user_settings_text[option][1]}
┃
┠ <b>Variabel Dinamis:</b>
┠ • <code>{{filename}}</code> - Nama file lengkap
┠ • <code>{{basename}}</code> - Nama file tanpa ekstensi  
┠ • <code>{{extension}}</code> - Ekstensi file
┃
┠ • <code>{{audiolang}}</code> - Bahasa audio
┖ • <code>{{sublang}}</code> - Bahasa subtitle
"""
    else:
        text = f"""⌬ <b><u>Pengaturan Menu :</u></b>
│
┟ <b>Opsi</b> → {option}
┃
┠ <b>Nilai Opsi</b> → {val if val else "<b>Tidak Ada</b>"}
┃
┠ <b>Tipe Input Default</b> → {user_settings_text[option][0]}
┖ <b>Deskripsi</b> → {user_settings_text[option][1]}
"""
    await edit_message(message, text, buttons.build_menu(2))


async def event_handler(client, query, pfunc, rfunc, photo=False, document=False):
    user_id = query.from_user.id
    handler_dict[user_id] = True
    start_time = update_time = time()

    async def event_filter(_, __, event):
        if photo:
            mtype = event.photo or event.document
        elif document:
            mtype = event.document
        else:
            mtype = event.text
        user = event.from_user or event.sender_chat
        return bool(
            user.id == user_id and event.chat.id == query.message.chat.id and mtype
        )

    handler = client.add_handler(
        MessageHandler(pfunc, filters=create(event_filter)), group=-1
    )

    while handler_dict[user_id]:
        await sleep(0.5)
        if time() - start_time > 60:
            handler_dict[user_id] = False
            await rfunc()
        elif time() - update_time > 8 and handler_dict[user_id]:
            update_time = time()
            msg = await client.get_messages(query.message.chat.id, query.message.id)
            text = msg.text.split("\n")
            text[-1] = (
                f"┖ <b>Sisa Waktu :</b> <code>{round(60 - (time() - start_time), 2)} dtk</code>"
            )
            await edit_message(msg, "\n".join(text), msg.reply_markup)
    client.remove_handler(*handler)


@new_task
async def edit_user_settings(client, query):
    from_user = query.from_user
    user_id = from_user.id
    name = from_user.mention
    message = query.message
    data = query.data.split()

    handler_dict[user_id] = False
    thumb_path = f"thumbnails/{user_id}.jpg"
    rclone_conf = f"rclone/{user_id}.conf"
    token_pickle = f"tokens/{user_id}.pickle"
    yt_cookie_path = f"cookies/{user_id}/cookies.txt"

    user_dict = user_data.get(user_id, {})
    if user_id != int(data[1]):
        return await query.answer("Bukan milikmu!", show_alert=True)
    elif data[2] == "setevent":
        await query.answer()
    elif data[2] in [
        "general",
        "mirror",
        "leech",
        "uphoster",
        "gofile",
        "buzzheavier",
        "pixeldrain",
        "ffset",
        "advanced",
        "gdrive",
        "rclone",
    ]:
        await query.answer()
        await update_user_settings(query, data[2])
    elif data[2] == "yttools":
        await query.answer()
        await update_user_settings(query, data[2])
    elif data[2] == "uphoster_destinations":
        await query.answer()
        user_dict = user_data.get(user_id, {})
        uphoster_service = user_dict.get("UPHOSTER_SERVICE", "gofile")
        selected_services = uphoster_service.split(",") if uphoster_service else []

        if len(data) > 3:
            service = data[3]
            if service in selected_services:
                if len(selected_services) > 1:
                    selected_services.remove(service)
                else:
                    await query.answer(
                        "Setidaknya satu tujuan harus dipilih!", show_alert=True
                    )
            else:
                selected_services.append(service)
            new_services = ",".join(selected_services)
            update_user_ldata(user_id, "UPHOSTER_SERVICE", new_services)
            await database.update_user_data(user_id)
            selected_services = new_services.split(",")
        else:
            selected_services = (
                uphoster_service.split(",") if uphoster_service else ["gofile"]
            )

        buttons = ButtonMaker()
        for service in ["gofile", "buzzheavier", "pixeldrain"]:
            state = "✓" if service in selected_services else ""
            buttons.data_button(
                f"{service.capitalize()} {state}",
                f"userset {user_id} uphoster_destinations {service}",
            )

        buttons.data_button("Kembali", f"userset {user_id} back uphoster", "footer")
        buttons.data_button("Tutup", f"userset {user_id} close", "footer")

        text = f"""⌬ <b>Pilih Tujuan Uphoster :</b>"""
        await edit_message(message, text, buttons.build_menu(1))
    elif data[2] == "menu":
        await query.answer()
        await get_menu(data[3], message, user_id)
    elif data[2] == "tog":
        await query.answer()
        update_user_ldata(user_id, data[3], data[4] == "t")
        if data[3] == "STOP_DUPLICATE":
            back_to = "gdrive"
        elif data[3] in ["USER_TOKENS", "USE_DEFAULT_COOKIE"]:
            back_to = "general"
        else:
            back_to = "leech"
        await update_user_settings(query, stype=back_to)
        await database.update_user_data(user_id)
    elif data[2] == "file":
        await query.answer()
        buttons = ButtonMaker()
        text = user_settings_text[data[3]][2]
        buttons.data_button("Berhenti", f"userset {user_id} menu {data[3]} stop")
        buttons.data_button("Kembali", f"userset {user_id} menu {data[3]}", "footer")
        buttons.data_button("Tutup", f"userset {user_id} close", "footer")
        prompt_title = data[3].replace("_", " ").title()
        new_message_text = f"⌬ <b>Atur {prompt_title}</b>\n\n{text}"
        await edit_message(message, new_message_text, buttons.build_menu(1))
        rfunc = partial(get_menu, data[3], message, user_id)
        pfunc = partial(add_file, ftype=data[3], rfunc=rfunc)
        await event_handler(
            client,
            query,
            pfunc,
            rfunc,
            photo=data[3] == "THUMBNAIL",
            document=data[3] != "THUMBNAIL",
        )
    elif data[2] in ["set", "addone", "rmone"]:
        await query.answer()
        buttons = ButtonMaker()
        if data[2] == "set":
            text = user_settings_text[data[3]][2]
            func = set_option
        elif data[2] == "addone":
            text = f"Tambahkan satu atau lebih kunci string dan nilai ke {data[3]}. Contoh: {{'kunci 1': 62625261, 'kunci 2': 'nilai 2'}}. Waktu Habis: 60 dtk"
            func = add_one
        elif data[2] == "rmone":
            text = f"Hapus satu atau lebih kunci dari {data[3]}. Contoh: kunci 1/kunci 2/kunci 3. Waktu Habis: 60 dtk"
            func = remove_one
        buttons.data_button("Berhenti", f"userset {user_id} menu {data[3]} stop")
        buttons.data_button("Kembali", f"userset {user_id} menu {data[3]}", "footer")
        buttons.data_button("Tutup", f"userset {user_id} close", "footer")
        await edit_message(
            message, message.text.html + "\n\n" + text, buttons.build_menu(1)
        )
        rfunc = partial(get_menu, data[3], message, user_id)
        pfunc = partial(func, option=data[3], rfunc=rfunc)
        await event_handler(client, query, pfunc, rfunc)
    elif data[2] == "remove":
        await query.answer("Dihapus!", show_alert=True)
        if data[3] in [
            "THUMBNAIL",
            "RCLONE_CONFIG",
            "TOKEN_PICKLE",
            "USER_COOKIE_FILE",
        ]:
            if data[3] == "THUMBNAIL":
                fpath = thumb_path
            elif data[3] == "RCLONE_CONFIG":
                fpath = rclone_conf
            elif data[3] == "USER_COOKIE_FILE":
                fpath = yt_cookie_path
            else:
                fpath = token_pickle
            if await aiopath.exists(fpath):
                await remove(fpath)
            del user_dict[data[3]]
            await database.update_user_doc(user_id, data[3])
        else:
            update_user_ldata(user_id, data[3], "")
            await database.update_user_data(user_id)
        await get_menu(data[3], message, user_id)
    elif data[2] == "reset":
        await query.answer("Reset Berhasil!", show_alert=True)
        user_dict.pop(data[3], None)
        await database.update_user_data(user_id)
        await get_menu(data[3], message, user_id)
    elif data[2] == "confirm_reset_all":
        await query.answer()
        buttons = ButtonMaker()
        buttons.data_button("Ya", f"userset {user_id} do_reset_all yes")
        buttons.data_button("Tidak", f"userset {user_id} do_reset_all no")
        buttons.data_button("Tutup", f"userset {user_id} close", "footer")
        text = "<i>Apakah kamu yakin ingin mereset semua pengaturan penggunamu?</i>"
        await edit_message(query.message, text, buttons.build_menu(2))
    elif data[2] == "do_reset_all":
        if data[3] == "yes":
            await query.answer("Reset Berhasil!", show_alert=True)
            user_dict = user_data.get(user_id, {})
            for k in list(user_dict.keys()):
                if k not in ("SUDO", "AUTH", "VERIFY_TOKEN", "VERIFY_TIME"):
                    del user_dict[k]
            for fpath in [thumb_path, rclone_conf, token_pickle, yt_cookie_path]:
                if await aiopath.exists(fpath):
                    await remove(fpath)
            await update_user_settings(query)
            await database.update_user_data(user_id)
        else:
            await query.answer("Reset Dibatalkan.", show_alert=True)
            await update_user_settings(query)
    elif data[2] == "view":
        await query.answer()
        await send_file(message, thumb_path, name)
    elif data[2] in ["gd", "rc"]:
        await query.answer()
        du = "rc" if data[2] == "gd" else "gd"
        update_user_ldata(user_id, "DEFAULT_UPLOAD", du)
        await update_user_settings(query, stype="general")
        await database.update_user_data(user_id)
    elif data[2] == "back":
        await query.answer()
        stype = data[3] if len(data) == 4 else "main"
        await update_user_settings(query, stype)
    else:
        await query.answer()
        await delete_message(message, message.reply_to_message)


@new_task
async def get_users_settings(_, message):
    msg = ""
    if auth_chats:
        msg += f"AUTHORIZED_CHATS: {auth_chats}\n"
    if sudo_users:
        msg += f"SUDO_USERS: {sudo_users}\n\n"
    if user_data:
        for u, d in user_data.items():
            kmsg = f"\n<b>{u}:</b>\n"
            if vmsg := "".join(
                f"{k}: <code>{v or None}</code>\n" for k, v in d.items()
            ):
                msg += kmsg + vmsg
        if not msg:
            await send_message(message, "Tidak ada data pengguna!")
            return
        msg_ecd = msg.encode()
        if len(msg_ecd) > 4000:
            with BytesIO(msg_ecd) as ofile:
                ofile.name = "users_settings.txt"
                await send_file(message, ofile)
        else:
            await send_message(message, msg)
    else:
        await send_message(message, "Tidak ada data pengguna!")
