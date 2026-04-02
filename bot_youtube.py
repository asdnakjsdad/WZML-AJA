import os
import telebot
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# ================= PENGATURAN =================
BOT_TOKEN = 'MASUKKAN_TELEGRAM_BOT_TOKEN_ANDA_DI_SINI'

# Masukkan data Google Anda dalam bentuk teks langsung, TIDAK PERLU FILE JSON/PICKLE
CLIENT_ID = 'masukkan_client_id_anda_disini.apps.googleusercontent.com'
CLIENT_SECRET = 'masukkan_client_secret_anda_disini'
REFRESH_TOKEN = 'masukkan_refresh_token_yang_didapat_dari_google_disini'
# ==============================================

bot = telebot.TeleBot(BOT_TOKEN)

def get_youtube_service():
    """Fungsi untuk login ke YouTube tanpa file pickle"""
    creds = Credentials(
        token=None,
        refresh_token=REFRESH_TOKEN,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        token_uri="https://oauth2.googleapis.com/token"
    )
    return build('youtube', 'v3', credentials=creds)

@bot.message_handler(content_types=['video', 'document'])
def handle_video(message):
    bot.reply_to(message, "⏳ Video diterima! Sedang mengunduh dari Telegram...")
    
    try:
        # 1. Mengunduh video dari chat Telegram
        if message.content_type == 'video':
            file_id = message.video.file_id
        else:
            file_id = message.document.file_id

        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        video_path = "video_sementara.mp4"
        with open(video_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        bot.reply_to(message, "📤 Unduhan selesai. Mulai proses upload ke YouTube...")
        
        # 2. Upload ke YouTube
        youtube = get_youtube_service()
        request = youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": "Video Upload via Telegram Bot",
                    "description": "Video ini di-upload secara otomatis menggunakan Bot Telegram.",
                    "categoryId": "22" # Kategori Film & Animasi
                },
                "status": {
                    "privacyStatus": "private" # Ubah jadi "public" jika ingin langsung publik
                }
            },
            media_body=MediaFileUpload(video_path, chunksize=-1, resumable=True)
        )
        response = request.execute()
        
        # 3. Berikan link ke user
        video_url = f"https://www.youtube.com/watch?v={response['id']}"
        bot.reply_to(message, f"✅ **Upload Berhasil!**\n\nLink Video: {video_url}", parse_mode="Markdown")
        
        # 4. Bersihkan file sampah di server
        if os.path.exists(video_path):
            os.remove(video_path)
            
    except Exception as e:
        bot.reply_to(message, f"❌ **Gagal melakukan upload:**\n{e}", parse_mode="Markdown")

print("Bot YouTube Uploader sedang berjalan...")
bot.polling(none_stop=True)
