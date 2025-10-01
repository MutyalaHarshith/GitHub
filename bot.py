import logging
import requests
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.update import Update
import imghdr_pure as imghdr


# Author / Owner Info
AUTHOR = "Mutyala Harshith"
OWNER_LINK = "https://t.me/Mutyalaharshith"
CHANNEL = "https://t.me/ExistBots"
SUPPORT = "https://t.me/GroupExist"

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Replace with your Telegram Bot Token
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# ---------- START COMMAND ----------
def start(update: Update, context: CallbackContext):
    text = (
        "👋 Welcome to <b>GitHub Info Bot</b>!\n\n"
        "📌 Features:\n"
        "1️⃣ Send me a GitHub repository link, and I'll give you a ZIP download.\n"
        "2️⃣ Use <code>/github username</code> to get GitHub user details.\n\n"
        f"👨‍💻 <b>Author:</b> {AUTHOR}\n"
        f"👑 <b>Owner:</b> <a href='{OWNER_LINK}'>@Mutyalaharshith</a>\n"
        f"📢 <b>Channel:</b> <a href='{CHANNEL}'>ExistBots</a>\n"
        f"💬 <b>Support Group:</b> <a href='{SUPPORT}'>GroupExist</a>"
    )

    update.message.reply_text(text, parse_mode="HTML", disable_web_page_preview=True)

# ---------- GITHUB PROFILE FETCH ----------
def github_profile(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text(
            "❌ Please provide a GitHub username.\n\nExample:\n<code>/github torvalds</code>",
            parse_mode="HTML"
        )
        return

    username = context.args[0].strip()
    url = f"https://api.github.com/users/{username}"

    try:
        res = requests.get(url)
        data = res.json()

        if "message" in data and data["message"] == "Not Found":
            update.message.reply_text(
                f"❌ GitHub user <b>{username}</b> not found.",
                parse_mode="HTML"
            )
            return

        # Extract fields
        name = data.get("name") or "N/A"
        login = data.get("login") or "N/A"
        id_ = data.get("id") or "N/A"
        node_id = data.get("node_id") or "N/A"
        avatar = data.get("avatar_url") or ""
        html_url = data.get("html_url") or ""
        repos_url = data.get("repos_url") or ""
        followers_url = data.get("followers_url") or ""
        following_url = data.get("following_url") or ""
        gists_url = data.get("gists_url") or ""
        blog = data.get("blog") or "N/A"
        location = data.get("location") or "N/A"
        email = data.get("email") or "N/A"
        hireable = str(data.get("hireable")) or "N/A"
        bio = data.get("bio") or "No bio provided."
        twitter = data.get("twitter_username") or "N/A"
        company = data.get("company") or "N/A"
        followers = data.get("followers", 0)
        following = data.get("following", 0)
        public_repos = data.get("public_repos", 0)
        public_gists = data.get("public_gists", 0)
        created = data.get("created_at") or "N/A"
        updated = data.get("updated_at") or "N/A"

        # Format message
        text = (
            f"<b>👤 GitHub Profile</b>\n"
            f"👨‍💻 Name: <b>{name}</b>\n"
            f"🔑 Username: <code>{login}</code>\n"
            f"🆔 ID: <code>{id_}</code>\n"
            f"🧬 Node ID: <code>{node_id}</code>\n"
            f"📍 Location: {location}\n"
            f"🏢 Company: {company}\n"
            f"📰 Blog: {blog}\n"
            f"✉️ Email: {email}\n"
            f"📌 Hireable: {hireable}\n"
            f"🐦 Twitter: {twitter}\n"
            f"📦 Public Repos: <b>{public_repos}</b>\n"
            f"🗃️ Gists: <b>{public_gists}</b>\n"
            f"👥 Followers: <b>{followers}</b> | Following: <b>{following}</b>\n"
            f"📝 Bio: <i>{bio}</i>\n"
            f"📅 Created: {created}\n"
            f"🛠️ Updated: {updated}\n"
            f"🔗 Profile: <a href='{html_url}'>{html_url}</a>\n"
            f"📁 Repos: <a href='{repos_url}'>Repos Link</a>\n"
            f"👤 Followers: <a href='{followers_url}'>Followers</a>\n"
            f"➡️ Following: <a href='{following_url}'>Following</a>\n"
            f"📑 Gists: <a href='{gists_url}'>Gists</a>"
        )

        update.message.reply_photo(photo=avatar, caption=text, parse_mode="HTML")

    except Exception as e:
        update.message.reply_text("⚠️ Failed to fetch GitHub profile. Try again later.")
        logger.error(f"Error: {e}")

# ---------- GITHUB REPO ZIP ----------
def github_repo(update: Update, context: CallbackContext):
    try:
        link = update.message.text.strip()
        if "github.com" not in link:
            update.message.reply_text("❌ Please send a valid GitHub repository link.")
            return

        download_link = f"{link}/archive/refs/heads/master.zip"

        caption = (
            f"📂 **GitHub Repository ZIP File**\n\n"
            f"[Click here to download ZIP file]({download_link})\n\n"
            f"👨‍💻 **Developer:** [Harshith](https://t.me/Mutyalaharshith)"
        )

        inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Download ZIP 📥", url=download_link)],
            [InlineKeyboardButton("Developer 👨‍💻", url=OWNER_LINK)]
        ])

        update.message.reply_document(
            document=download_link,
            caption=caption,
            parse_mode="Markdown",
            reply_markup=inline_keyboard
        )

    except Exception as e:
        update.message.reply_text(
            "❌ Unable to send the document. Please use the button below to download.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Download ZIP 📥", url=download_link)]])
        )
        logger.error(f"Error: {e}")

# ---------- MAIN ----------
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("github", github_profile))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, github_repo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
