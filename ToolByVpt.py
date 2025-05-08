import discord
from discord.ext import commands
import os

TOKEN = 'MTM2NzA2NjU4MTg4ODEzOTI4NA.GlvgB4.lB0fIGANlI43TMiqnFCTFp1dbODvy_XaFTrA0A'  # Thay YOUR_BOT_TOKEN bằng token bot của bạn
CHANNEL_ID = 1364890863410352180  # ID kênh Discord của bạn
FILE_PATH = 'text.txt'  # Đường dẫn tới file .txt

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    channel = bot.get_channel(CHANNEL_ID)

    if not channel:
        print("Không thể tìm thấy kênh.")
        await bot.close()
        return

    if not os.path.exists(FILE_PATH):
        print(f"Không tìm thấy file: {FILE_PATH}")
        await bot.close()
        return

    while True:
        try:
            # Đọc tất cả các dòng trong file
            with open(FILE_PATH, 'r', encoding='utf-8') as f:
                content = f.read()  # Đọc toàn bộ nội dung của file

            if not content:
                print("File trống.")
                continue

            # Định dạng lại nội dung theo yêu cầu, mỗi dòng với ' > # '
            formatted_content = "\n".join([f"> # {line.strip()}" for line in content.splitlines()])

            # Gửi tất cả nội dung vào kênh Discord mà không đợi
            await channel.send(formatted_content)
            print(f"Đã gửi toàn bộ nội dung trong file.")

        except discord.errors.HTTPException as e:
            if e.code == 429:
                retry_after = int(e.retry_after)
                print(f"Rate limit gặp phải, chờ {retry_after} giây.")
                await asyncio.sleep(retry_after)  # Nghỉ sau khi gặp rate limit và thử lại
                continue
            else:
                print(f"Lỗi HTTPException khác: {e}")
                await bot.close()
                break

        except Exception as e:
            print(f"Lỗi khác: {e}")
            await bot.close()
            break

bot.run(TOKEN)
