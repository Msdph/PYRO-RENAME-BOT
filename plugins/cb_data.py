from helper.utils import progress_for_pyrogram, convert
from pyrogram import Client, filters
from pyrogram.types import (  InlineKeyboardButton, InlineKeyboardMarkup,ForceReply)
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from helper.database import find
import os 
import humanize
from PIL import Image
import time
import ftplib

FTP_HOST = "130.185.79.155"
FTP_USER = "pz14205"
FTP_PASS = "12345678"
# connect to the FTP server

#ftp.cwd('./domains/pz14205.parspack.net/public_html/')
#ftp.retrlines('LIST')
def handle(sizeWritten,totalSize):
    #global sizeWritten
    sizeWritten += 1024
    percentComplete = sizeWritten / totalSize
    print ("%s percent complete" %str(sizeWritten / totalSize))

def upftp(path,folder,filename):
    ftp = ftplib.FTP("130.185.79.155")
    ftp.login("pz14205", "12345678")
    f = open(f"{path}", "rb")
    ftp.cwd(f'/domains/pz14205.parspack.net/public_html/{folder}')
    ftp.storbinary(f"STOR {filename}", f ,1024 ,handle)
    f.close()

    """ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)
    # force UTF-8 encoding
    ftp.encoding = "utf-8"
    #ftp.cwd('./domains/pz14205.parspack.net/public_html/')
    with open(path, "rb") as file:
        ftp.storbinary(f"STOR ./{one}/{two}", file)

    ftp.quit()"""

def checkftp(text):
    ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)
    # force UTF-8 encoding
    ftp.encoding = "utf-8"
    ftp.cwd('./domains/pz14205.parspack.net/public_html/')
    files = []
    try:
        files = ftp.nlst()
    except ftplib.error_perm as resp:
        if str(resp) == "550 No files found":
            print ("No files in this directory")
        else:
            raise
    if text in files:
        return "exist"
    else:
        ftp.mkd(text)
        return "make"

@Client.on_callback_query(filters.regex('cancel'))
async def cancel(bot,update):
    try:
        await update.message.delete()
    except:
        return

@Client.on_callback_query(filters.regex('rename'))
async def rename(bot,update):
	user_id = update.message.chat.id
	date = update.message.date
	await update.message.delete()
	await update.message.reply_text("__𝙿𝚕𝚎𝚊𝚜𝚎 𝙴𝚗𝚝𝚎𝚛 𝙽𝚎𝚠 𝙵𝚒𝚕𝚎𝙽𝚊𝚖𝚎...__",	
	reply_to_message_id=update.message.reply_to_message.id,  
	reply_markup=ForceReply(True))

@Client.on_callback_query(filters.regex('sftp'))
async def ftp(bot,update):
	user_id = update.message.chat.id
	date = update.message.date
	await update.message.delete()
	await update.message.reply_text("__𝙿𝚕𝚎𝚊𝚜𝚎 𝙴𝚗𝚝𝚎𝚛 PATH 𝙽𝚊𝚖𝚎...__",	
	reply_to_message_id=update.message.reply_to_message.id,  
	reply_markup=ForceReply(True))	

@Client.on_callback_query(filters.regex("upload"))
async def doc(bot,update):
    type = update.data.split('_')[1]
    new_name = update.message.text
    new_filename = new_name.split(":-")[1]
    print(new_filename)
    if not "." in new_filename:
        new_filename = new_filename + ".mkv"
    else:
        new_filename = new_filename + ".mkv"
    file_path = f"downloads/{new_filename}"
    file = update.message.reply_to_message
    print(file_path)
    ms = await update.message.edit("𝚃𝚁𝚈𝙸𝙽𝙶 𝚃𝙾 𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳...")
    c_time = time.time()
    try:
        path = await bot.download_media(message = file, progress=progress_for_pyrogram,progress_args=( "𝚃𝚁𝚈𝙸𝙽𝙶 𝚃𝙾 𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳....",  ms, c_time   ))
    except Exception as e:
        await ms.edit(e)
        return 
    splitpath = path.split("/downloads/")
    dow_file_name = splitpath[1]
    old_file_name =f"downloads/{dow_file_name}"
    os.rename(old_file_name,file_path)
    duration = 0
    try:
        metadata = extractMetadata(createParser(file_path))
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds
    except:
        pass
    user_id = int(update.message.chat.id) 
    ph_path = None
    data = find(user_id) 
    media = getattr(file, file.media.value)
    c_caption = data[1] 
    c_thumb = data[0]
    if c_caption:
        caption = c_caption.format(filename=new_filename, filesize=humanize.naturalsize(media.file_size), duration=convert(duration))
    else:
        caption = f"**{new_name}**"
    if (media.thumbs or c_thumb):
        if c_thumb:
            ph_path = await bot.download_media(c_thumb) 
        else:
            ph_path = await bot.download_media(media.thumbs[0].file_id)
        Image.open(ph_path).convert("RGB").save(ph_path)
        img = Image.open(ph_path)
        img.resize((1080, 720))
        img.save(ph_path, "JPEG")
    await ms.edit("𝚃𝚁𝚈𝙸𝙽𝙶 𝚃𝙾 𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶....")
    c_time = time.time() 
    try:
        if type == "document":
            await bot.send_document(
		    update.message.chat.id,
                document=file_path,
                thumb=ph_path, 
                caption=caption, 
                progress=progress_for_pyrogram,
                progress_args=( "𝚃𝚁𝚈𝙸𝙽𝙶 𝚃𝙾 𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶....",  ms, c_time   ))
        elif type == "video": 
            await bot.send_video(
                update.message.chat.id,
                video=file_path,
                caption=caption,
                thumb=ph_path,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=( "𝚃𝚁𝚈𝙸𝙽𝙶 𝚃𝙾 𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶...."+file_path,  ms, c_time))
        elif type == "audio": 
            await bot.send_audio(
                update.message.chat.id,
                audio=file_path,
                caption=caption,
                thumb=ph_path,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=( "𝚃𝚁𝚈𝙸𝙽𝙶 𝚃𝙾 𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶....",  ms, c_time   ))
    except Exception as e: 
        await ms.edit(e) 
        os.remove(file_path)
        if ph_path:
           os.remove(ph_path)
    await ms.delete() 
    os.remove(file_path) 
    if ph_path:
        os.remove(ph_path) 

@Client.on_callback_query(filters.regex("ftp"))
async def doc2(bot,update):
    type = update.data.split('_')[1]
    new_name = update.message.text
    new_filename = new_name.split(":-")[1]
    print(new_filename)
    
    file_path = f"downloads/{new_filename}"
    file = update.message.reply_to_message
	#hjk
    media = file.document or file.video or file.audio or file.photo
    fileeeeeeeeeeeeeeename = media.file_name
    #print(media.file_size)
	#hjk
    ms = await update.message.edit("𝚃𝚁𝚈𝙸𝙽𝙶 𝚃𝙾 𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳...")
    c_time = time.time()
    try:
        path = await bot.download_media(message = file, progress=progress_for_pyrogram,progress_args=( "𝚃𝚁𝚈𝙸𝙽𝙶 𝚃𝙾 𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳....",  ms, c_time   ))
    except Exception as e:
        await ms.edit(e)
        return 
    #splitpath = path.split("/downloads/")
    #dow_file_name = splitpath[1]
    #old_file_name =f"downloads/{dow_file_name}"
    #os.rename(old_file_name,file_path)
    duration = 0
    try:
        metadata = extractMetadata(createParser(file_path))
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds
    except:
        pass
    user_id = int(update.message.chat.id) 
    ph_path = None
    data = find(user_id) 
    media = getattr(file, file.media.value)
    c_caption = data[1] 
    c_thumb = data[0]
    sixe = humanize.naturalsize(media.file_size)
    if c_caption:
        caption = c_caption.format(filename=new_filename, filesize=humanize.naturalsize(media.file_size), duration=convert(duration))
    else:
        caption = f"**{new_name}**"
    if (media.thumbs or c_thumb):
        if c_thumb:
            ph_path = await bot.download_media(c_thumb) 
        else:
            ph_path = await bot.download_media(media.thumbs[0].file_id)
        Image.open(ph_path).convert("RGB").save(ph_path)
        img = Image.open(ph_path)
        img.resize((1080, 720))
        img.save(ph_path, "JPEG")
    await ms.edit("𝚃𝚁𝚈𝙸𝙽𝙶 𝚃𝙾 𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶....")
    c_time = time.time() 
    try:
        new_filenames = new_filename.split()[0]
        print(new_filenames)
        print(fileeeeeeeeeeeeeeename)
        print(path)
        
        #res = 
        #print(res)
        try :
            ftp = ftplib.FTP("130.185.79.155")
            ftp.login("pz14205", "12345678")
            checkftp(new_filenames)
            f = open(f"{path}", "rb")
            ftp.cwd(f'/domains/pz14205.parspack.net/public_html/{new_filenames}')
            ftp.storbinary(f"STOR {fileeeeeeeeeeeeeeename}", f )
            f.close()
            print("success")
            #upftp(path,new_filenames,fileeeeeeeeeeeeeeename)
        except Exception as e:
            print('eror')
            print(e)

        await ms.edit(f"UPLOAD COPLETE \n\nhttps://s2.kenzodl.xyz/{new_filenames}/{fileeeeeeeeeeeeeeename}")
        #await update.reply_text(f"UPLOAD COPLETE \n\nhttps://s2.kenzodl.xyz/{new_filenames}/{fileeeeeeeeeeeeeeename}")
        #await bot.send_message(f"UPLOAD COPLETE \n\nhttps://s2.kenzodl.xyz/{new_filenames}/{fileeeeeeeeeeeeeeename}")

    except Exception as e: 
        #await ms.edit(e) 
        os.remove(file_path)
        os.remove(path)
        if ph_path:
            os.remove(ph_path)
            
    #await ms.delete() 
    os.remove(path)
    os.remove(file_path) 
    if ph_path:
        os.remove(ph_path) 
