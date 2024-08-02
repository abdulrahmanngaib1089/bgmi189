#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    PicklePersistence,
    filters
)
from telegram.error import BadRequest

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define the rules message
RULES_MESSAGE = (
    "Rules for original views, likes, or reach:\n"
    "1. Your account doesn't have fake followers.\n"
    "2. Your account should be active.\n"
    "3. Your account should not be too old.\n"
    "4. Posting time should be 12pm, 6pm, or 8pm.\n"
    "5. Use proper hashtags and viral music on your post.\n\n"
    "Follow these rules to help in making your content viral."
)

JOIN_CHANNEL_URL = "https://t.me/akramteam"  # Replace with your channel join link
CHANNEL_ID = "@akramteam"  # Replace with your channel ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message asking the user to join the channel first."""
    join_channel_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(text="Join Channel", url=JOIN_CHANNEL_URL)],
    ])
    await update.message.reply_text(
        "Hello!!! Welcome to the most advanced viral Instagram and YouTube bot.📈",
        reply_markup=join_channel_keyboard
    )

    await update.message.reply_text(
        "💀 Please join the following channel to access premium bot features 💀\n\n"
        "🤖 After joining the channel, click here\n"
        "----------👉 /viral 👈---------\n"
        "to access premium features 🤖"
    )

async def handle_join_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the event when the user clicks the 'I have joined' button."""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    try:
        # Check if the user is a member of the channel
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        if member.status in ['member', 'administrator', 'creator']:
            keyboard = [
                [InlineKeyboardButton(text="📸 📸  Instagram  📸 📸", callback_data="instagram")],
                [InlineKeyboardButton(text="▶️ ▶️ YouTube ▶️ ▶️", callback_data="youtube")]
            ]
            await query.message.reply_text("Thanks for joining us! 📲 Ready to choose a platform that could go viral? Let’s dive in!", reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            join_channel_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton(text="Join Channel", url=JOIN_CHANNEL_URL)],
                [InlineKeyboardButton(text="I have joined", callback_data="joined_check")]
            ])
            await query.message.reply_text("It looks like you haven't joined the channel yet. Please join our channel first:", reply_markup=join_channel_keyboard)
    except BadRequest as e:
        if str(e) == 'Chat not found':
            await query.message.reply_text("There was an error checking your channel membership. Please ensure you have joined the channel.")
        else:
            logger.error(f"Error checking channel membership: {e}")
            await query.message.reply_text("There was an error checking your channel membership. Please try again later.")

async def handle_platform_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the platform choice (Instagram or YouTube)."""
    query = update.callback_query
    await query.answer()
    platform = query.data

    if platform == "instagram":
        keyboard = [
            [InlineKeyboardButton(text="📸 📸 Make your content viral 📸 📸", callback_data="insta_viral")],
            [InlineKeyboardButton(text=" 📸 📸 Instagram views 📸 📸", callback_data="insta_views")],
            [InlineKeyboardButton(text=" 📸 📸 Likes 📸 📸",  callback_data="insta_likes")],
            [InlineKeyboardButton(text=" 📸 📸 IG reach 📸 📸", callback_data="insta_reach")],
            [InlineKeyboardButton(text=" 📸 📸 IG monetization 📸 📸", callback_data="insta_monetization")]
        ]
    else:
        keyboard = [
            [InlineKeyboardButton(text=" ▶️ ▶️ Channel views ▶️ ▶️", callback_data="yt_views")],
            [InlineKeyboardButton(text=" ▶️ ▶️ Likes ▶️ ▶️", callback_data="yt_likes")],
            [InlineKeyboardButton(text=" ▶️ ▶️ Watch time ▶️ ▶️", callback_data="yt_watch_time")],
            [InlineKeyboardButton(text=" ▶️ ▶️ Channel monetization ▶️ ▶️", callback_data="yt_monetization")]
        ]

    await query.message.reply_text("🚀 🚀Select an option to viral you content 🚀 🚀 :", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_option_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the choice of specific Instagram or YouTube options."""
    query = update.callback_query
    await query.answer()
    option = query.data

    # Show the rules message
    await query.message.reply_text(RULES_MESSAGE)

    # Ask if the user has followed the rules
    keyboard = [
        [InlineKeyboardButton(text="Yes, I have followed the rules", callback_data=f"confirm_{option}")]
    ]
    await query.message.reply_text("Have you followed these rules?", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_rule_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the confirmation that the user has followed the rules."""
    query = update.callback_query
    await query.answer()
    option = query.data.split("_", 1)[1]

    # Ask the user to send their post link
    await query.message.reply_text("Please send your post link:")

    context.user_data["option"] = option
    context.user_data["awaiting_post_link"] = True

async def handle_post_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the receipt of the post link."""
    if context.user_data.get("awaiting_post_link"):
        post_link = update.message.text
        option = context.user_data["option"]

        # Check if the link starts with 'https://'
        if not post_link.startswith("https://"):
            await update.message.reply_text("Sorry 😭!! , Please provide the correct link!! ")
            return

        # Show the task processing message
        await update.message.reply_text(
            "Your task is in process, you will get the result in 3-4 hours.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text="Research in progress", callback_data="in_progress")]
            ])
        )

        # Clear the waiting state
        context.user_data["awaiting_post_link"] = False
        logger.info(f"Post link received: {post_link}, Option: {option}")

async def handle_viral(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /viral command and checks channel membership."""
    user_id = update.effective_user.id

    try:
        # Check if the user is a member of the channel
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        if member.status in ['member', 'administrator', 'creator']:
            # Provide platform choices if user is a member
            keyboard = [
                [InlineKeyboardButton(text="📸 📸  Instagram  📸 📸", callback_data="instagram")],
                [InlineKeyboardButton(text="▶️ ▶️ YouTube ▶️ ▶️", callback_data="youtube")]
            ]
            await update.message.reply_text("Thanks for joining us! 📲 Ready to choose a platform that could go viral? Let’s dive in!", reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            # Prompt the user to join the channel
            join_channel_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton(text="Join Channel", url=JOIN_CHANNEL_URL)],
                [InlineKeyboardButton(text="I have joined", callback_data="joined_check")]
            ])
            await update.message.reply_text("Sorry 😭,!!You need to join our channel to access premium features. Please join the channel first:", reply_markup=join_channel_keyboard)
    except BadRequest as e:
        if str(e) == 'Chat not found':
            await update.message.reply_text("There was an error checking your channel membership. Please ensure you have joined the channel.")
        else:
            logger.error(f"Error checking channel membership: {e}")
            await update.message.reply_text("There was an error checking your channel membership. Please try again later.")

async def handle_random_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Replies to any random text message with a join channel prompt."""
    logger.info(f"Random message received: {update.message.text}")
    join_channel_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(text="Join Channel", url=JOIN_CHANNEL_URL)],
    ])
    await update.message.reply_text(
        "Please join our channel to access premium features:",
        reply_markup=join_channel_keyboard
    )

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /clear command to reset the state and provide a join channel prompt."""
    user_id = update.effective_user.id
    
    # Reset any user data
    context.user_data.clear()
    
    # Send a message asking the user to join the channel
    join_channel_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(text="Join Channel", url=JOIN_CHANNEL_URL)],
    ])

    await update.message.reply_text(
        "All previous interactions have been cleared. Please join our channel to start fresh to viral you content 📈:",
        reply_markup=join_channel_keyboard
    )
        
    # Send the additional message with instructions
    await update.message.reply_text(
        "💀 Please join the following channel to access premium bot features 💀\n\n"
        "🤖 After joining the channel, click here\n"
        "----------👉 /viral 👈---------\n"
        "to access premium features 🤖"
    )

def main() -> None:
    """Run the bot."""
    persistence = PicklePersistence(filepath="viralo_bot")
    application = (
        Application.builder()
        .token("7137320181:AAHKhI4vaMMBrgsroww7WWdplePYkjyBKSM")
        .persistence(persistence)
        .arbitrary_callback_data(True)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("viral", handle_viral))
    application.add_handler(CommandHandler("clear", clear))

    application.add_handler(CallbackQueryHandler(handle_join_check, pattern="^joined_check$"))
    application.add_handler(CallbackQueryHandler(handle_platform_choice, pattern="^(instagram|youtube)$"))
    application.add_handler(CallbackQueryHandler(handle_option_choice, pattern="^(insta_|yt_)"))
    application.add_handler(CallbackQueryHandler(handle_rule_confirmation, pattern="^confirm_"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_post_link))  # Handle post link before random messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_random_message))  # General message handler for random texts

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
