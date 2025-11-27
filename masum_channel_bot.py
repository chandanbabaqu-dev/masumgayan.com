import logging
from telegram import Update, MessageEntity
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import BadRequest

# ---  (      ) ---

# BotFather      
TOKEN = "8386791954:AAGXVZoDXnQEwA_EstCu_OKB6uEA1okvriY"

#  /  
GROUP_NAME = "Masum Channel"

#  
YOUTUBE_LINK = "https://youtube.com/@modmasumofficel?si=mRw40NOfBYCvbKQv"
TELEGRAM_LINK = "https://t.me/bankulmasum"
INSTAGRAM_LINK = "https://www.instagram.com/king_come10m?igsh=Mjdid3Zqb3VkMjM2"

#    
SUPPORT_ADMIN = "@masumbankul"

# ---   ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ---   (   ) ---
async def send_welcome_message(user, chat, context: ContextTypes.DEFAULT_TYPE):
    """       """
    try:
        user_photos = await user.get_profile_photos(limit=1)
        username = f"@{user.username}" if user.username else "Not available"

        caption_text = (
            f" <b>Welcome to {GROUP_NAME}!</b> \n\n"
            f"<b>Name:</b> {user.mention_html()}\n"
            f"<b>Username:</b> {username}\n"
            f"<b>User ID:</b> <code>{user.id}</code>\n"
            f"\n"
            f" <b>Privacy & Security Rules</b>\n\n"
            f" Sharing external links, promotions, or spam is strictly prohibited.\n"
            f" The use of abusive language or any form of harassment will not be tolerated.\n"
            f" Engaging in unauthorized buying/selling or posting scam links is forbidden.\n\n"
            f"<i>Violation of these rules will lead to an immediate ban.</i>\n"
            f"\n"
            f" To see all available commands, type <b>/help</b>\n\n"
            f" <b>Support Admin:</b> {SUPPORT_ADMIN}"
        )

        if user_photos and user_photos.photos:
            photo_id = user_photos.photos[0][-1].file_id
            await context.bot.send_photo(
                chat_id=chat.id,
                photo=photo_id,
                caption=caption_text,
                parse_mode='HTML'
            )
        else:
            await context.bot.send_message(
                chat_id=chat.id,
                text=caption_text,
                parse_mode='HTML',
                disable_web_page_preview=True
            )
    except Exception as e:
        logger.error(f"    : {e}")

# ---    ---

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        " <b>Here are the available commands:</b>\n\n"
        "<code>/help</code> - Shows this list of commands.\n"
        "<code>/rules</code> - Displays the group rules.\n"
        "<code>/yt</code> - Get the link to our YouTube channel.\n"
        "<code>/tme</code> - Get our Telegram channel link.\n"
        "<code>/insta</code> - Get our Instagram profile link.\n"
        "<code>/myid</code> - Shows your personal Telegram ID.\n"
        "<code>/sos</code> - Lists all group administrators.\n"
        "<code>/ban [reason]</code> - Reply to a message to report a user.\n"
        "<code>/pin</code> - Shows the latest pinned message.\n"
        "<code>/new</code> - Shows your welcome message again."
    )
    await update.message.reply_text(help_text, parse_mode='HTML')

async def rules_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    rules_text = (
        " <b>Group Rules</b> \n\n"
        "1. No spamming or sharing external links.\n"
        "2. Be respectful. No abusive language or personal attacks.\n"
        "3. Do not share any illegal or adult content.\n"
        "4. Stick to the group's topic.\n\n"
        "<i>Breaking these rules will result in a ban.</i>"
    )
    await update.message.reply_text(rules_text, parse_mode='HTML')

async def yt_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_html(f' <b>Our YouTube Channel:</b> <a href="{YOUTUBE_LINK}">Click Here</a>')

async def tme_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_html(f' <b>Our Telegram Channel:</b> <a href="{TELEGRAM_LINK}">Click Here</a>')

async def insta_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_html(f' <b>Our Instagram Profile:</b> <a href="{INSTAGRAM_LINK}">Click Here</a>')

async def myid_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    await update.message.reply_text(f"Your Telegram ID is: <code>{user_id}</code>", parse_mode='HTML')

async def new_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """       """
    user = update.effective_user
    chat = update.effective_chat
    await send_welcome_message(user, chat, context)

async def sos_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """       """
    if update.effective_chat.type == 'private':
        await update.message.reply_text("This command only works in groups.")
        return

    try:
        admins = await context.bot.get_chat_administrators(update.effective_chat.id)
        admin_list = [f" {admin.user.mention_html()}" for admin in admins]
        if not admin_list:
            await update.message.reply_text("Could not find any admins.")
            return
            
        await update.message.reply_html(" <b>Group Administrators:</b>\n\n" + "\n".join(admin_list))
    except Exception as e:
        logger.error(f"/sos   : {e}")
        await update.message.reply_text("Could not retrieve the admin list.")

async def ban_report_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """      """
    if not update.message.reply_to_message:
        await update.message.reply_text("Please reply to the message of the user you want to report.")
        return
        
    reporter = update.effective_user
    reported_user = update.message.reply_to_message.from_user
    reason = " ".join(context.args) if context.args else "No reason provided."

    try:
        admins = await context.bot.get_chat_administrators(update.effective_chat.id)
        admin_mentions = [admin.user.mention_html() for admin in admins if not admin.user.is_bot]

        if not admin_mentions:
            await update.message.reply_text("Could not find any admins to notify.")
            return

        report_message = (
            f" <b>User Report</b> \n\n"
            f"<b>Reported by:</b> {reporter.mention_html()}\n"
            f"<b>Reported User:</b> {reported_user.mention_html()}\n"
            f"<b>Reason:</b> {reason}\n\n"
            f"Admins, please review: {' '.join(admin_mentions)}"
        )
        
        await update.message.reply_html(report_message)
    except Exception as e:
        logger.error(f"/ban   : {e}")

async def pin_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """        """
    if update.effective_chat.type == 'private':
        await update.message.reply_text("This command only works in groups.")
        return
    try:
        chat_info = await context.bot.get_chat(update.effective_chat.id)
        if chat_info.pinned_message:
            await chat_info.pinned_message.forward(update.effective_chat.id)
        else:
            await update.message.reply_text("There is no pinned message in this group.")
    except BadRequest:
        await update.message.reply_text("Could not access the pinned message. Make sure the bot is an admin.")

# ---    ---

async def handle_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """       """
    for new_member in update.message.new_chat_members:
        await send_welcome_message(new_member, update.effective_chat, context)

async def delete_links(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """-        """
    if not update.message or update.effective_chat.type == 'private':
        return

    user = update.effective_user
    message = update.message
    
    has_link = any(e.type in [MessageEntity.URL, MessageEntity.TEXT_LINK] for e in message.entities)

    if has_link:
        try:
            admins = await context.bot.get_chat_administrators(update.effective_chat.id)
            admin_ids = {admin.user.id for admin in admins}
            
            if user.id not in admin_ids:
                await message.delete()
                logger.info(f"{user.first_name}       ")
        except Exception as e:
            logger.error(f"    : {e}")

# ---    ---

def main() -> None:
    """    """
    logger.info("    ...")
    
    application = Application.builder().token(TOKEN).build()

    #  
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("rules", rules_command))
    application.add_handler(CommandHandler("yt", yt_command))
    application.add_handler(CommandHandler("tme", tme_command))
    application.add_handler(CommandHandler("insta", insta_command))
    application.add_handler(CommandHandler("myid", myid_command))
    application.add_handler(CommandHandler("new", new_command))
    application.add_handler(CommandHandler("sos", sos_command))
    application.add_handler(CommandHandler("ban", ban_report_command))
    application.add_handler(CommandHandler("pin", pin_command))
    
    #  
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handle_new_member))
    application.add_handler(MessageHandler(
        (filters.Entity(MessageEntity.URL) | filters.Entity(MessageEntity.TEXT_LINK)) & (~filters.COMMAND),
        delete_links
    ))

    #   
    application.run_polling()
    logger.info("   ")

if __name__ == '__main__':
    main()