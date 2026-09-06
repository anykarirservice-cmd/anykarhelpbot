import urllib.request
import urllib.error
import json
import time
import re
import socket
import threading
import os
import io
import uuid
import textwrap
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

from PIL import Image, ImageDraw, ImageFont


# =========================================================
# ØªÙ†Ø¸ÛŒÙ…Ø§Øª Bale
# =========================================================

TOKEN = "977852941:VxYGRdYZlZaUo7htQS4X5TZLk_VKRKWKnHg"

BASE_URL = f"https://tapi.bale.ai/bot{TOKEN}"

BALE_HOST = "tapi.bale.ai"
BALE_NEW_IP = "2.189.68.110"


# =========================================================
# Ù¾Ø´ØªÛŒØ¨Ø§Ù†ÛŒ
# =========================================================

ADMIN_CHAT_ID = 121442435

support_sessions = {}
                   
# =========================================================
# ÙØ±Ù… Ø®ÙˆØ¯Ø§Ø¸Ù‡Ø§Ø±ÛŒ Ù…ØªØ®ØµØµ
# =========================================================

self_declaration_sessions = {}


SELF_DECLARATION_TEXT = """Ù…ØªÙ† ØªØ¹Ù‡Ø¯ Ùˆ Ø®ÙˆØ¯Ø§Ø¸Ù‡Ø§Ø±ÛŒ Ù…ØªØ®ØµØµ

Ø§ÛŒÙ†Ø¬Ø§Ù†Ø¨ [Ù†Ø§Ù… Ùˆ Ù†Ø§Ù… Ø®Ø§Ù†ÙˆØ§Ø¯Ú¯ÛŒ] Ø¨Ø§ Ú©Ø¯ Ù…Ù„ÛŒ [Ú©Ø¯ Ù…Ù„ÛŒ] Ùˆ Ø´Ù…Ø§Ø±Ù‡ ØªÙ…Ø§Ø³ Ø«Ø¨Øªâ€ŒØ´Ø¯Ù‡ Ø¯Ø± Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± [Ø´Ù…Ø§Ø±Ù‡ ØªÙ…Ø§Ø³]ØŒ Ø¨Ø§ Ø¢Ø¯Ø±Ø³ Ø¯Ù‚ÛŒÙ‚ Ù…Ø­Ù„ Ø³Ú©ÙˆÙ†Øª [Ø¢Ø¯Ø±Ø³ Ø¯Ù‚ÛŒÙ‚ Ù…Ø­Ù„ Ø³Ú©ÙˆÙ†Øª]ØŒ Ø¨Ø§ ØªØ®ØµØµ [Ù†Ø§Ù… ØªØ®ØµØµ] Ùˆ Ø³Ø§Ø¨Ù‚Ù‡ ÙØ¹Ø§Ù„ÛŒØª Ø§Ø¹Ù„Ø§Ù…â€ŒØ´Ø¯Ù‡ [Ù…ÛŒØ²Ø§Ù† Ø³Ø§Ø¨Ù‚Ù‡]ØŒ Ø¶Ù…Ù† ØªØ£ÛŒÛŒØ¯ ØµØ­Øª Ø§Ø·Ù„Ø§Ø¹Ø§Øª Ùˆ Ø§Ø¸Ù‡Ø§Ø±Ø§Øª Ø«Ø¨Øªâ€ŒØ´Ø¯Ù‡ØŒ Ø§Ø¹Ù„Ø§Ù… Ù…ÛŒâ€ŒÙ†Ù…Ø§ÛŒÙ… Ú©Ù‡ ØªØ®ØµØµØŒ Ù…Ù‡Ø§Ø±Øª Ùˆ Ø³Ø§Ø¨Ù‚Ù‡ ÙØ¹Ø§Ù„ÛŒØª Ù…Ø°Ú©ÙˆØ± Ù…ØªØ¹Ù„Ù‚ Ø¨Ù‡ Ø§ÛŒÙ†Ø¬Ø§Ù†Ø¨ Ø¨ÙˆØ¯Ù‡ Ùˆ Ù…Ø³Ø¦ÙˆÙ„ÛŒØª ØµØ­Øª Ú©Ù„ÛŒÙ‡ Ø§Ø·Ù„Ø§Ø¹Ø§Øª Ø§Ø±Ø§Ø¦Ù‡â€ŒØ´Ø¯Ù‡ Ø¨Ø± Ø¹Ù‡Ø¯Ù‡ Ø§ÛŒÙ†Ø¬Ø§Ù†Ø¨ Ø§Ø³Øª.

Ù‡Ù…Ú†Ù†ÛŒÙ† Ù…ØªØ¹Ù‡Ø¯ Ù…ÛŒâ€ŒØ´ÙˆÙ… Ø®Ø¯Ù…Ø§Øª Ø§Ø¹Ù„Ø§Ù…â€ŒØ´Ø¯Ù‡ Ø±Ø§ Ø¨Ø§ Ø±Ø¹Ø§ÛŒØª Ø§ØµÙˆÙ„ ÙÙ†ÛŒ Ùˆ Ø­Ø±ÙÙ‡â€ŒØ§ÛŒ Ø§Ù†Ø¬Ø§Ù… Ø¯Ø§Ø¯Ù‡ Ùˆ Ù…Ø³Ø¦ÙˆÙ„ÛŒØª Ù‡Ø±Ú¯ÙˆÙ†Ù‡ Ù‚ØµÙˆØ±ØŒ Ø§Ø´ØªØ¨Ø§Ù‡ØŒ ØªØ®Ù„ÙØŒ Ø®Ø³Ø§Ø±Øª Ù…Ø§Ù„ÛŒ ÛŒØ§ Ø¬Ø§Ù†ÛŒ Ùˆ Ù‡Ù…Ú†Ù†ÛŒÙ† Ø®Ø³Ø§Ø±Ø§Øª ÙˆØ§Ø±Ø¯Ù‡ Ø¨Ù‡ Ø§Ù…ÙˆØ§Ù„ Ù…Ø´ØªØ±ÛŒ Ú©Ù‡ Ù†Ø§Ø´ÛŒ Ø§Ø² Ø¹Ù…Ù„Ú©Ø±Ø¯ØŒ Ø§Ù‚Ø¯Ø§Ù… ÛŒØ§ Ø¹Ø¯Ù… Ø±Ø¹Ø§ÛŒØª Ø§ØµÙˆÙ„ ÙÙ†ÛŒ Ø§Ø² Ø³ÙˆÛŒ Ø§ÛŒÙ†Ø¬Ø§Ù†Ø¨ Ø¨Ø§Ø´Ø¯ØŒ Ø¨Ø± Ø¹Ù‡Ø¯Ù‡ Ø§ÛŒÙ†Ø¬Ø§Ù†Ø¨ Ø¨ÙˆØ¯Ù‡ Ùˆ Ù…ÙˆØ¸Ù Ø¨Ù‡ Ø¬Ø¨Ø±Ø§Ù† Ø®Ø³Ø§Ø±Øª ÙˆØ§Ø±Ø¯Ù‡ Ù…Ø·Ø§Ø¨Ù‚ Ù‚ÙˆØ§Ù†ÛŒÙ† Ùˆ Ù…Ù‚Ø±Ø±Ø§Øª Ù…Ø±Ø¨ÙˆØ· Ø®ÙˆØ§Ù‡Ù… Ø¨ÙˆØ¯.

Ø§ÛŒÙ†Ø¬Ø§Ù†Ø¨ Ø¢Ú¯Ø§Ù‡ Ù‡Ø³ØªÙ… Ú©Ù‡ ØµØ±Ù Ø«Ø¨Øª Ø§ÛŒÙ† Ø®ÙˆØ¯Ø§Ø¸Ù‡Ø§Ø±ÛŒ Ø¨Ù‡ Ù…Ù†Ø²Ù„Ù‡ ØªØ£ÛŒÛŒØ¯ ØªØ®ØµØµ ÛŒØ§ ØµÙ„Ø§Ø­ÛŒØª Ø­Ø±ÙÙ‡â€ŒØ§ÛŒ Ø§Ø² Ø³ÙˆÛŒ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± Ù†Ø¨ÙˆØ¯Ù‡ Ùˆ ØµØ­Øª Ø§Ø¯Ø¹Ø§Ù‡Ø§ Ùˆ Ù…Ø³Ø¦ÙˆÙ„ÛŒØª Ø¹Ù…Ù„Ú©Ø±Ø¯ Ø­Ø±ÙÙ‡â€ŒØ§ÛŒ Ø¨Ø± Ø¹Ù‡Ø¯Ù‡ Ø§ÛŒÙ†Ø¬Ø§Ù†Ø¨ Ù…ÛŒâ€ŒØ¨Ø§Ø´Ø¯.

â˜‘ï¸ Ø§ÛŒÙ†Ø¬Ø§Ù†Ø¨ Ù…ØªÙ† ÙÙˆÙ‚ Ø±Ø§ Ø¨Ù‡â€ŒØ·ÙˆØ± Ú©Ø§Ù…Ù„ Ù…Ø·Ø§Ù„Ø¹Ù‡ Ú©Ø±Ø¯Ù‡ Ùˆ Ø¨Ø§ ØªØ£ÛŒÛŒØ¯ Ø¢Ù†ØŒ ØµØ­Øª Ø§Ø·Ù„Ø§Ø¹Ø§Øª Ùˆ Ù…Ø³Ø¦ÙˆÙ„ÛŒØªâ€ŒÙ‡Ø§ÛŒ Ù…Ù†Ø¯Ø±Ø¬ Ø¯Ø± Ø§ÛŒÙ† ØªØ¹Ù‡Ø¯Ù†Ø§Ù…Ù‡ Ø±Ø§ Ù…ÛŒâ€ŒÙ¾Ø°ÛŒØ±Ù…."""


# =========================================================
# ÙÙˆÙ†Øª ÙØ§Ø±Ø³ÛŒ
# =========================================================

FONT_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "Vazirmatn-Regulr.ttf"
)


# =========================================================
# Ø§Ø¬Ø¨Ø§Ø± DNS Ø¨Ù„Ù‡ Ø±ÙˆÛŒ IP Ù…Ø´Ø®Øµ
# =========================================================

_original_getaddrinfo = socket.getaddrinfo


def _bale_getaddrinfo(
    host,
    port,
    family=0,
    type=0,
    proto=0,
    flags=0
):

    if host == BALE_HOST:
        host = BALE_NEW_IP

    return _original_getaddrinfo(
        host,
        port,
        family,
        type,
        proto,
        flags
    )


socket.getaddrinfo = _bale_getaddrinfo


# =========================================================
# Ù„ÛŒÙ†Ú©â€ŒÙ‡Ø§ÛŒ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±
# =========================================================

ORDER_URL = "https://anykar.ir/categories/"
SPECIALIST_URL = "https://anykar.ir/servicer-registration"
WORK_URL = "https://anykar.ir/work"
CUSTOMER_RULES_URL = "https://anykar.ir/rules"
SPECIALIST_RULES_URL = "https://anykar.ir/servicer-rules"
SITE_URL = "https://anykar.ir"

BOT_USERNAME = "@anykarhelpbot"
BOT_URL = "https://ble.ir/anykarhelpbot"

CHANNEL_USERNAME = "@anykar"
CHANNEL_URL = "https://ble.ir/anykar"


# =========================================================
# API REQUEST
# =========================================================

def api_request(method, data=None, retries=3):

    url = f"{BASE_URL}/{method}"

    for attempt in range(1, retries + 1):

        try:

            body = json.dumps(
                data or {},
                ensure_ascii=False
            ).encode("utf-8")

            request = urllib.request.Request(
                url,
                data=body,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "AnykarHelpBot/1.0"
                },
                method="POST"
            )

            print(
                f"[API] {method} | attempt={attempt}"
            )

            with urllib.request.urlopen(
                request,
                timeout=35
            ) as response:

                raw = response.read().decode("utf-8")

                result = json.loads(raw)

                print(
                    f"[API OK] {method} | "
                    f"ok={result.get('ok')}"
                )

                return result

        except Exception as e:

            print(
                f"[API ERROR] {method} | "
                f"attempt={attempt} | "
                f"{repr(e)}"
            )

            if attempt < retries:

                wait_time = attempt * 3

                time.sleep(wait_time)

            else:

                print(
                    f"[API] {method} failed "
                    f"after {retries} attempts"
                )

    return None


# =========================================================
# Ø¯Ø±ÛŒØ§ÙØª Ù¾ÛŒØ§Ù…â€ŒÙ‡Ø§
# =========================================================

def get_updates(offset=None):

    data = {
        "timeout": 25
    }

    if offset is not None:
        data["offset"] = offset

    return api_request(
        "getUpdates",
        data,
        retries=3
    )


# =========================================================
# Ø§Ø±Ø³Ø§Ù„ Ù¾ÛŒØ§Ù…
# =========================================================

def send_message(chat_id, text, keyboard=None):

    data = {
        "chat_id": chat_id,
        "text": text
    }

    if keyboard:
        data["reply_markup"] = keyboard

    result = api_request(
        "sendMessage",
        data,
        retries=3
    )

    if result is None:

        print(
            f"[SEND FAILED] chat_id={chat_id}"
        )

    elif not result.get("ok"):

        print(
            f"[SEND BALE ERROR] "
            f"chat_id={chat_id} | "
            f"{result}"
        )

    else:

        print(
            f"[SEND OK] chat_id={chat_id}"
        )

    return result


# =========================================================
# Ø§Ø±Ø³Ø§Ù„ Ø¹Ú©Ø³ Ø¨Ù‡ Bale
# =========================================================

def get_channel_membership_status(user_id):

    result = api_request(
        "getChatMember",
        {
            "chat_id": CHANNEL_USERNAME,
            "user_id": user_id
        },
        retries=3
    )

    if not result or not result.get("ok"):
        print(
            f"[CHANNEL CHECK ERROR] "
            f"user_id={user_id} | result={result}"
        )
        return None

    member = result.get("result", {})
    status = member.get("status")

    print(
        f"[CHANNEL CHECK] "
        f"user_id={user_id} | status={status}"
    )

    if status in ("member", "administrator", "creator"):
        return True

    if status == "restricted":
        return bool(member.get("is_member"))

    return False


def send_photo(chat_id, photo, caption=None):

    url = f"{BASE_URL}/sendPhoto"

    for attempt in range(1, 4):

        try:

            boundary = (
                "----AnykarBoundary"
                + uuid.uuid4().hex
            )

            body = bytearray()

            # ---------------------------------------------
            # chat_id
            # ---------------------------------------------

            body.extend(
                (
                    f"--{boundary}\r\n"
                    f'Content-Disposition: form-data; '
                    f'name="chat_id"\r\n'
                    f"\r\n"
                    f"{chat_id}\r\n"
                ).encode("utf-8")
            )

            # ---------------------------------------------
            # caption
            # ---------------------------------------------

            if caption:

                body.extend(
                    (
                        f"--{boundary}\r\n"
                        f'Content-Disposition: form-data; '
                        f'name="caption"\r\n'
                        f"\r\n"
                        f"{caption}\r\n"
                    ).encode("utf-8")
                )

            # ---------------------------------------------
            # photo
            # ---------------------------------------------

            body.extend(
                (
                    f"--{boundary}\r\n"
                    f'Content-Disposition: form-data; '
                    f'name="photo"; '
                    f'filename="self_declaration.jpg"\r\n'
                    f"Content-Type: image/jpeg\r\n"
                    f"\r\n"
                ).encode("utf-8")
            )

            body.extend(photo)

            body.extend(
                (
                    f"\r\n"
                    f"--{boundary}--\r\n"
                ).encode("utf-8")
            )

            # ---------------------------------------------
            # request Ø¬Ø¯ÛŒØ¯ Ø¨Ø±Ø§ÛŒ Ù‡Ø± ØªÙ„Ø§Ø´
            # ---------------------------------------------

            request = urllib.request.Request(
                url,
                data=bytes(body),
                headers={
                    "Content-Type":
                        f"multipart/form-data; "
                        f"boundary={boundary}",
                    "User-Agent":
                        "AnykarHelpBot/1.0"
                },
                method="POST"
            )

            print(
                f"[PHOTO API] attempt={attempt}"
            )

            with urllib.request.urlopen(
                request,
                timeout=35
            ) as response:

                raw = response.read().decode(
                    "utf-8"
                )

                result = json.loads(raw)

                print(
                    f"[PHOTO API RESULT] {result}"
                )

                if result.get("ok"):

                    print(
                        f"[SEND PHOTO OK] "
                        f"chat_id={chat_id}"
                    )

                    return result

                print(
                    f"[SEND PHOTO BALE ERROR] "
                    f"{result}"
                )

        except Exception as e:

            print(
                f"[SEND PHOTO ERROR] "
                f"attempt={attempt} | "
                f"{repr(e)}"
            )

        if attempt < 3:

            time.sleep(
                attempt * 3
            )

    print(
        f"[SEND PHOTO FAILED] "
        f"chat_id={chat_id}"
    )

    return None


# =========================================================
# Ø³Ø§Ø®Øª ØªØµÙˆÛŒØ± ØªØ¹Ù‡Ø¯Ù†Ø§Ù…Ù‡
# =========================================================

def create_self_declaration_image(
    session,
    declaration_id,
    current_time
):

    if not os.path.exists(FONT_PATH):

        raise FileNotFoundError(
            f"ÙÙˆÙ†Øª Ù¾ÛŒØ¯Ø§ Ù†Ø´Ø¯: {FONT_PATH}"
        )

    # -----------------------------------------------------
    # Ø¬Ø§ÛŒÚ¯Ø²ÛŒÙ†ÛŒ Ø§Ø·Ù„Ø§Ø¹Ø§Øª
    # -----------------------------------------------------

    declaration_text = SELF_DECLARATION_TEXT

    declaration_text = declaration_text.replace(
        "[Ù†Ø§Ù… Ùˆ Ù†Ø§Ù… Ø®Ø§Ù†ÙˆØ§Ø¯Ú¯ÛŒ]",
        session["name"]
    )

    declaration_text = declaration_text.replace(
        "[Ú©Ø¯ Ù…Ù„ÛŒ]",
        session["national_id"]
    )

    declaration_text = declaration_text.replace(
        "[Ø´Ù…Ø§Ø±Ù‡ ØªÙ…Ø§Ø³]",
        session["phone"]
    )

    declaration_text = declaration_text.replace(
        "[Ø¢Ø¯Ø±Ø³ Ø¯Ù‚ÛŒÙ‚ Ù…Ø­Ù„ Ø³Ú©ÙˆÙ†Øª]",
        session["address"]
    )

    declaration_text = declaration_text.replace(
        "[Ù†Ø§Ù… ØªØ®ØµØµ]",
        session["specialty"]
    )

    declaration_text = declaration_text.replace(
        "[Ù…ÛŒØ²Ø§Ù† Ø³Ø§Ø¨Ù‚Ù‡]",
        session["experience"]
    )

    # -----------------------------------------------------
    # ØªÙ†Ø¸ÛŒÙ…Ø§Øª ØµÙØ­Ù‡
    # -----------------------------------------------------

    width = 1654
    margin = 110

    title_font = ImageFont.truetype(
        FONT_PATH,
        48
    )

    info_font = ImageFont.truetype(
        FONT_PATH,
        34
    )

    body_font = ImageFont.truetype(
        FONT_PATH,
        32
    )

    small_font = ImageFont.truetype(
        FONT_PATH,
        25
    )

    # -----------------------------------------------------
    # Ø´Ú©Ø³ØªÙ† Ø®Ø·ÙˆØ· ÙØ§Ø±Ø³ÛŒ
    # -----------------------------------------------------

    def wrap_persian(text, max_chars=55):

        result = []

        paragraphs = text.split("\n")

        for paragraph in paragraphs:

            if not paragraph.strip():

                result.append("")

                continue

            lines = textwrap.wrap(
                paragraph,
                width=max_chars,
                break_long_words=False,
                break_on_hyphens=False
            )

            result.extend(lines)

        return result

    body_lines = wrap_persian(
        declaration_text,
        55
    )

    # -----------------------------------------------------
    # Ø§Ø±ØªÙØ§Ø¹
    # -----------------------------------------------------

    line_height = 52

    header_height = 430

    footer_height = 190

    body_height = (
        len(body_lines) * line_height
    )

    height = (
        margin
        + header_height
        + body_height
        + footer_height
        + margin
    )

    height = max(
        height,
        2339
    )

    # -----------------------------------------------------
    # Ø³Ø§Ø®Øª ØªØµÙˆÛŒØ±
    # -----------------------------------------------------

    image = Image.new(
        "RGB",
        (width, height),
        "white"
    )

    draw = ImageDraw.Draw(image)

    # -----------------------------------------------------
    # Ø¹Ù†ÙˆØ§Ù†
    # -----------------------------------------------------

    title = "Ù…ØªÙ† ØªØ¹Ù‡Ø¯ Ùˆ Ø®ÙˆØ¯Ø§Ø¸Ù‡Ø§Ø±ÛŒ Ù…ØªØ®ØµØµ"

    bbox = draw.textbbox(
        (0, 0),
        title,
        font=title_font
    )

    title_width = (
        bbox[2] - bbox[0]
    )

    draw.text(
        (
            (width - title_width) / 2,
            90
        ),
        title,
        font=title_font,
        fill="black"
    )

    # -----------------------------------------------------
    # Ø®Ø· Ø¬Ø¯Ø§Ú©Ù†Ù†Ø¯Ù‡
    # -----------------------------------------------------

    draw.line(
        (
            margin,
            175,
            width - margin,
            175
        ),
        fill="black",
        width=3
    )

    # -----------------------------------------------------
    # Ø§Ø·Ù„Ø§Ø¹Ø§Øª Ù…ØªØ®ØµØµ
    # -----------------------------------------------------

    info_y = 215

    info_lines = [
        f"Ù†Ø§Ù… Ùˆ Ù†Ø§Ù… Ø®Ø§Ù†ÙˆØ§Ø¯Ú¯ÛŒ: {session['name']}",
        f"Ú©Ø¯ Ù…Ù„ÛŒ: {session['national_id']}",
        f"Ø´Ù…Ø§Ø±Ù‡ ØªÙ…Ø§Ø³: {session['phone']}",
        f"ØªØ®ØµØµ: {session['specialty']}",
        f"Ø³Ø§Ø¨Ù‚Ù‡ ÙØ¹Ø§Ù„ÛŒØª: {session['experience']}",
        f"Ø´Ù†Ø§Ø³Ù‡ Ø®ÙˆØ¯Ø§Ø¸Ù‡Ø§Ø±ÛŒ: {declaration_id}",
        f"ØªØ§Ø±ÛŒØ® Ùˆ Ø³Ø§Ø¹Øª ØªØ£ÛŒÛŒØ¯: {current_time}"
    ]

    for line in info_lines:

        draw.text(
            (
                margin,
                info_y
            ),
            line,
            font=info_font,
            fill="black",
            anchor="la"
        )

        info_y += 40

    # -----------------------------------------------------
    # Ø¢Ø¯Ø±Ø³
    # -----------------------------------------------------

    address_lines = wrap_persian(
        "Ø¢Ø¯Ø±Ø³ Ø¯Ù‚ÛŒÙ‚ Ù…Ø­Ù„ Ø³Ú©ÙˆÙ†Øª: "
        + session["address"],
        65
    )

    for line in address_lines:

        draw.text(
            (
                margin,
                info_y
            ),
            line,
            font=info_font,
            fill="black",
            anchor="la"
        )

        info_y += 40

    # -----------------------------------------------------
    # Ù…ØªÙ† Ø§ØµÙ„ÛŒ
    # -----------------------------------------------------

    body_y = header_height

    for line in body_lines:

        draw.text(
            (
                width - margin,
                body_y
            ),
            line,
            font=body_font,
            fill="black",
            anchor="ra"
        )

        body_y += line_height

    # -----------------------------------------------------
    # Ù¾Ø§ÛŒÛŒÙ† Ø³Ù†Ø¯
    # -----------------------------------------------------

    footer_y = height - 150

    draw.line(
        (
            margin,
            footer_y - 25,
            width - margin,
            footer_y - 25
        ),
        fill="black",
        width=2
    )

    footer_text = (
        f"Ø´Ù†Ø§Ø³Ù‡ Ø®ÙˆØ¯Ø§Ø¸Ù‡Ø§Ø±ÛŒ: {declaration_id}   |   "
        f"ØªØ§Ø±ÛŒØ® ØªØ£ÛŒÛŒØ¯: {current_time}"
    )

    draw.text(
        (
            width - margin,
            footer_y
        ),
        footer_text,
        font=small_font,
        fill="black",
        anchor="ra"
    )

    # -----------------------------------------------------
    # Ø®Ø±ÙˆØ¬ÛŒ JPEG Ø¯Ø± Ø­Ø§ÙØ¸Ù‡
    # -----------------------------------------------------

    output = io.BytesIO()

    image.save(
        output,
        format="JPEG",
        quality=95,
        optimize=True
    )

    output.seek(0)

    return output


# =========================================================
# Ø§Ø±Ø³Ø§Ù„ Ø®ÙˆØ¯Ø§Ø¸Ù‡Ø§Ø±ÛŒ Ø¨Ù‡ Ø§Ø¯Ù…ÛŒÙ†
# =========================================================

def send_self_declaration_to_admin(chat_id):

    session = self_declaration_sessions.get(
        chat_id
    )

    if not session:

        print(
            "[SELF DECLARATION] "
            "Session not found."
        )

        return False

    try:

        current_time = time.strftime(
            "%Y/%m/%d - %H:%M:%S"
        )

        declaration_id = (
            "SD-"
            + time.strftime("%Y%m%d-%H%M%S")
            + "-"
            + uuid.uuid4().hex[:6].upper()
        )

        # -------------------------------------------------
        # Ø³Ø§Ø®Øª Ø¹Ú©Ø³ Ø§Ø² Ù…ØªÙ†
        # -------------------------------------------------

        print(
            "[SELF DECLARATION] "
            "Creating image..."
        )

        image_file = create_self_declaration_image(
            session,
            declaration_id,
            current_time
        )

        # -------------------------------------------------
        # Ú©Ù¾Ø´Ù† Ø¹Ú©Ø³
        # -------------------------------------------------

        caption = (
            "ðŸ“‹ Ø®ÙˆØ¯Ø§Ø¸Ù‡Ø§Ø±ÛŒ Ù…ØªØ®ØµØµ Ø¬Ø¯ÛŒØ¯\n\n"
            f"ðŸ‘¤ {session['name']}\n"
            f"ðŸªª Ú©Ø¯ Ù…Ù„ÛŒ: {session['national_id']}\n"
            f"ðŸ“± {session['phone']}\n"
            f"ðŸ”§ {session['specialty']}\n"
            f"â±ï¸ {session['experience']}\n\n"
            f"ðŸ†” Chat ID: {chat_id}\n"
            f"ðŸ“„ Ø´Ù†Ø§Ø³Ù‡ Ø®ÙˆØ¯Ø§Ø¸Ù‡Ø§Ø±ÛŒ: {declaration_id}\n"
            f"ðŸ“… ØªØ§Ø±ÛŒØ® Ùˆ Ø³Ø§Ø¹Øª: {current_time}"
        )

        # -------------------------------------------------
        # Ø§Ø±Ø³Ø§Ù„ Ø¹Ú©Ø³
        # -------------------------------------------------

        print(
            "[SELF DECLARATION] "
            "Sending image to admin..."
        )

        result = send_photo(
            ADMIN_CHAT_ID,
            image_file.getvalue(),
            caption
        )

        # -------------------------------------------------
        # Ø¨Ø±Ø±Ø³ÛŒ Ù†ØªÛŒØ¬Ù‡
        # -------------------------------------------------

        if result is None or not result.get("ok"):

            print(
                "[SELF DECLARATION] "
                "Image sending failed."
            )

            return False

        print(
            "[SELF DECLARATION] "
            f"Sent successfully: {declaration_id}"
        )

        return True

    except Exception as e:

        print(
            "[SELF DECLARATION ERROR]",
            repr(e)
        )

        return False


# =========================================================
# Ù†Ø±Ù…Ø§Ù„â€ŒØ³Ø§Ø²ÛŒ Ù…ØªÙ† ÙØ§Ø±Ø³ÛŒ
# =========================================================

def normalize_text(text):

    text = text.lower().strip()

    replacements = {

        "ÙŠ": "ÛŒ",
        "Ù‰": "ÛŒ",
        "Ùƒ": "Ú©",
        "Û€": "Ù‡",
        "Ø©": "Ù‡",

        "\u200c": " ",
        "â€Œ": " "
    }

    for old, new in replacements.items():

        text = text.replace(
            old,
            new
        )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text


def contains_any(text, words):

    return any(
        word in text
        for word in words
    )


# =========================================================
# Ú©ÛŒØ¨ÙˆØ±Ø¯ Ø§ØµÙ„ÛŒ
# =========================================================

def main_keyboard():

    return {

        "keyboard": [

            [
                {"text": "ðŸ“ Ø«Ø¨Øª Ø³ÙØ§Ø±Ø´"},
                {"text": "ðŸ‘¨â€ðŸ”§ Ù‡Ù…Ú©Ø§Ø±ÛŒ Ù…ØªØ®ØµØµ"}
            ],

            [
                {"text": "ðŸ“‹ Ø®ÙˆØ¯Ø§Ø¸Ù‡Ø§Ø±ÛŒ Ù…ØªØ®ØµØµ"},
                {"text": "ðŸ“± Ù†Ø­ÙˆÙ‡ Ú©Ø§Ø±"}
            ],

            [
                {"text": "ðŸ’° Ù‚ÛŒÙ…Øª Ø®Ø¯Ù…Ø§Øª"},
                {"text": "ðŸ›¡ï¸ Ù¾Ø±Ø¯Ø§Ø®Øª Ùˆ Ø¶Ù…Ø§Ù†Øª"}
            ],

            [
                {"text": "ðŸ“œ Ù‚ÙˆØ§Ù†ÛŒÙ† Ù…Ø´ØªØ±ÛŒ"},
                {"text": "ðŸ“‹ Ù‚ÙˆØ§Ù†ÛŒÙ† Ù…ØªØ®ØµØµ"}
            ],

            [
                {"text": "ðŸŽ§ Ù¾Ø´ØªÛŒØ¨Ø§Ù†ÛŒ"},
                {"text": "â“ Ø³ÙˆØ§Ù„Ø§Øª Ù…ØªØ¯Ø§ÙˆÙ„"}
            ],

            [
                {"text": "ðŸ‘¥ Ø¯Ø¹ÙˆØª Ø§Ø² Ø¯ÙˆØ³ØªØ§Ù†"},
                {"text": "â„¹ï¸ Ø±Ø§Ù‡Ù†Ù…Ø§"}
            ]
        ],

        "resize_keyboard": True
    }


# =========================================================
# Ø¯Ú©Ù…Ù‡ Ù„ÛŒÙ†Ú©
# =========================================================

def inline_button(text, url):

    return {

        "inline_keyboard": [

            [
                {
                    "text": text,
                    "url": url
                }
            ]
        ]
    }


# =========================================================
# Ø¯Ø¹ÙˆØª Ø§Ø² Ø¯ÙˆØ³ØªØ§Ù†
# =========================================================

def invite_friends(chat_id):

    return (
        "ðŸ‘¥ Ø¯Ø¹ÙˆØª Ø§Ø² Ø¯ÙˆØ³ØªØ§Ù†\n\n"
        "Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± Ø±Ùˆ Ø¨Ù‡ Ø¯ÙˆØ³ØªØ§Øª Ù…Ø¹Ø±ÙÛŒ Ú©Ù† ðŸ’›\n\n"
        "ðŸ¤– Ø¨Ø§Øª Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±:\n"
        f"{BOT_URL}\n\n"
        "Ù…ÛŒâ€ŒØªÙˆÙ†ÛŒ Ù‡Ù…ÛŒÙ† Ù¾ÛŒØ§Ù… Ø±Ùˆ Ø¨Ø±Ø§ÛŒ Ø¯ÙˆØ³ØªØ§Øª ÙÙˆØ±ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒ."
    )


# =========================================================
# Ù†Ù…Ø§ÛŒØ´ Ù…Ù†ÙˆÛŒ Ø§ØµÙ„ÛŒ + Ù„ÛŒÙ†Ú© Ú©Ø§Ù†Ø§Ù„
# =========================================================

def send_main_menu(chat_id, keyboard=None):

    send_message(
        chat_id,
        "ðŸ“¢ Ø¨Ø±Ø§ÛŒ Ø§Ø·Ù„Ø§Ø¹ Ø§Ø² Ø¢Ø®Ø±ÛŒÙ† Ø§Ø®Ø¨Ø§Ø± Ùˆ Ø§Ø·Ù„Ø§Ø¹ÛŒÙ‡â€ŒÙ‡Ø§ÛŒ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±ØŒ "
        "Ù…ÛŒâ€ŒØªÙˆÙ†ÛŒ Ø¹Ø¶Ùˆ Ú©Ø§Ù†Ø§Ù„Ù…ÙˆÙ† Ø¨Ø´ÛŒ. ðŸ’›",
        inline_button(
            "ðŸ“¢ Ø¹Ø¶ÙˆÛŒØª Ø¯Ø± Ú©Ø§Ù†Ø§Ù„ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±",
            CHANNEL_URL
        )
    )

    send_message(
        chat_id,
        "ðŸ‘‡ ÛŒÚ©ÛŒ Ø§Ø² Ú¯Ø²ÛŒÙ†Ù‡â€ŒÙ‡Ø§ÛŒ Ø²ÛŒØ± Ø±Ùˆ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†:",
        keyboard if keyboard else main_keyboard()
    )



# =========================================================
# Ø´Ø±ÙˆØ¹ Ø®ÙˆØ¯Ø§Ø¸Ù‡Ø§Ø±ÛŒ
# =========================================================

def start_self_declaration(chat_id):

    self_declaration_sessions[chat_id] = {
        "step": "name",
        "name": "",
        "national_id": "",
        "phone": "",
        "address": "",
        "specialty": "",
        "experience": ""
    }

    send_message(
        chat_id,
        "ðŸ“ Ø®ÙˆØ¯Ø§Ø¸Ù‡Ø§Ø±ÛŒ Ù…ØªØ®ØµØµ\n\n"
        "Ù„Ø·ÙØ§Ù‹ Ù†Ø§Ù… Ùˆ Ù†Ø§Ù… Ø®Ø§Ù†ÙˆØ§Ø¯Ú¯ÛŒ Ø®ÙˆØ¯Øª Ø±Ùˆ ÙˆØ§Ø±Ø¯ Ú©Ù†:"
    )


# =========================================================
# Ù¾Ø±Ø¯Ø§Ø²Ø´ Ø®ÙˆØ¯Ø§Ø¸Ù‡Ø§Ø±ÛŒ
# =========================================================

def process_self_declaration(
    chat_id,
    message
):

    session = self_declaration_sessions.get(
        chat_id
    )

    if not session:

        return False

    step = session["step"]

    # -----------------------------------------
    # Ù†Ø§Ù…
    # -----------------------------------------

    if step == "name":

        text = message.get(
            "text",
            ""
        ).strip()

        if not text:

            send_message(
                chat_id,
                "âŒ Ù„Ø·ÙØ§Ù‹ Ù†Ø§Ù… Ùˆ Ù†Ø§Ù… Ø®Ø§Ù†ÙˆØ§Ø¯Ú¯ÛŒ Ø±Ùˆ ÙˆØ§Ø±Ø¯ Ú©Ù†."
            )

            return True

        session["name"] = text

        session["step"] = "national_id"

        send_message(
            chat_id,
            "ðŸªª Ú©Ø¯ Ù…Ù„ÛŒ Ø®ÙˆØ¯Øª Ø±Ùˆ ÙˆØ§Ø±Ø¯ Ú©Ù†:"
        )

        return True

    # -----------------------------------------
    # Ú©Ø¯ Ù…Ù„ÛŒ
    # -----------------------------------------

    if step == "national_id":

        text = message.get(
            "text",
            ""
        ).strip()

        if not text:

            send_message(
                chat_id,
                "âŒ Ù„Ø·ÙØ§Ù‹ Ú©Ø¯ Ù…Ù„ÛŒ Ø±Ùˆ ÙˆØ§Ø±Ø¯ Ú©Ù†."
            )

            return True

        session["national_id"] = text

        session["step"] = "phone"

        send_message(
            chat_id,
            "ðŸ“± Ø´Ù…Ø§Ø±Ù‡ ØªÙ…Ø§Ø³ Ø«Ø¨Øªâ€ŒØ´Ø¯Ù‡ Ø¯Ø± Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± Ø±Ùˆ ÙˆØ§Ø±Ø¯ Ú©Ù†:"
        )

        return True

    # -----------------------------------------
    # Ø´Ù…Ø§Ø±Ù‡ ØªÙ…Ø§Ø³
    # -----------------------------------------

    if step == "phone":

        text = message.get(
            "text",
            ""
        ).strip()

        if not text:

            send_message(
                chat_id,
                "âŒ Ù„Ø·ÙØ§Ù‹ Ø´Ù…Ø§Ø±Ù‡ ØªÙ…Ø§Ø³ Ø±Ùˆ ÙˆØ§Ø±Ø¯ Ú©Ù†."
            )

            return True

        session["phone"] = text

        session["step"] = "address"

        send_message(
            chat_id,
            "ðŸ“ Ø¢Ø¯Ø±Ø³ Ø¯Ù‚ÛŒÙ‚ Ù…Ø­Ù„ Ø³Ú©ÙˆÙ†ØªØª Ø±Ùˆ ÙˆØ§Ø±Ø¯ Ú©Ù†:"
        )

        return True

    # -----------------------------------------
    # Ø¢Ø¯Ø±Ø³
    # -----------------------------------------

    if step == "address":

        text = message.get(
            "text",
            ""
        ).strip()

        if not text:

            send_message(
                chat_id,
                "âŒ Ù„Ø·ÙØ§Ù‹ Ø¢Ø¯Ø±Ø³ Ø¯Ù‚ÛŒÙ‚ Ù…Ø­Ù„ Ø³Ú©ÙˆÙ†Øª Ø±Ùˆ ÙˆØ§Ø±Ø¯ Ú©Ù†."
            )

            return True

        session["address"] = text

        session["step"] = "specialty"

        send_message(
            chat_id,
            "ðŸ”§ Ø­Ø§Ù„Ø§ ØªØ®ØµØµØª Ø±Ùˆ ÙˆØ§Ø±Ø¯ Ú©Ù†:\n\n"
            "Ù…Ø«Ù„Ø§Ù‹: Ù†Ù‚Ø§Ø´ÛŒ Ø³Ø§Ø®ØªÙ…Ø§Ù†ØŒ Ú©Ø§Ø´ÛŒâ€ŒÚ©Ø§Ø±ÛŒØŒ "
            "Ù„ÙˆÙ„Ù‡â€ŒÚ©Ø´ÛŒØŒ Ø¨Ø±Ù‚Ú©Ø§Ø±ÛŒ Ùˆ..."
        )

        return True

    # -----------------------------------------
    # ØªØ®ØµØµ
    # -----------------------------------------

    if step == "specialty":

        text = message.get(
            "text",
            ""
        ).strip()

        if not text:

            send_message(
                chat_id,
                "âŒ Ù„Ø·ÙØ§Ù‹ ØªØ®ØµØµ Ø±Ùˆ ÙˆØ§Ø±Ø¯ Ú©Ù†."
            )

            return True

        session["specialty"] = text

        session["step"] = "experience"

        send_message(
            chat_id,
            "â± Ù…ÛŒØ²Ø§Ù† Ø³Ø§Ø¨Ù‚Ù‡ ÙØ¹Ø§Ù„ÛŒØªØª Ø±Ùˆ ÙˆØ§Ø±Ø¯ Ú©Ù†:\n\n"
            "Ù…Ø«Ù„Ø§Ù‹: Ûµ Ø³Ø§Ù„"
        )

        return True

    # -----------------------------------------
    # Ø³Ø§Ø¨Ù‚Ù‡
    # -----------------------------------------

    if step == "experience":

        text = message.get(
            "text",
            ""
        ).strip()

        if not text:

            send_message(
                chat_id,
                "âŒ Ù„Ø·ÙØ§Ù‹ Ù…ÛŒØ²Ø§Ù† Ø³Ø§Ø¨Ù‚Ù‡ ÙØ¹Ø§Ù„ÛŒØªØª Ø±Ùˆ ÙˆØ§Ø±Ø¯ Ú©Ù†."
            )

            return True

        session["experience"] = text

        session["step"] = "confirmation"

        # -----------------------------------------
        # Ø³Ø§Ø®Øª Ù…ØªÙ† Ù¾ÛŒØ´â€ŒÙ†Ù…Ø§ÛŒØ´
        # -----------------------------------------

        declaration_preview = SELF_DECLARATION_TEXT

        declaration_preview = declaration_preview.replace(
            "[Ù†Ø§Ù… Ùˆ Ù†Ø§Ù… Ø®Ø§Ù†ÙˆØ§Ø¯Ú¯ÛŒ]",
            session["name"]
        )

        declaration_preview = declaration_preview.replace(
            "[Ú©Ø¯ Ù…Ù„ÛŒ]",
            session["national_id"]
        )

        declaration_preview = declaration_preview.replace(
            "[Ø´Ù…Ø§Ø±Ù‡ ØªÙ…Ø§Ø³]",
            session["phone"]
        )

        declaration_preview = declaration_preview.replace(
            "[Ø¢Ø¯Ø±Ø³ Ø¯Ù‚ÛŒÙ‚ Ù…Ø­Ù„ Ø³Ú©ÙˆÙ†Øª]",
            session["address"]
        )

        declaration_preview = declaration_preview.replace(
            "[Ù†Ø§Ù… ØªØ®ØµØµ]",
            session["specialty"]
        )

        declaration_preview = declaration_preview.replace(
            "[Ù…ÛŒØ²Ø§Ù† Ø³Ø§Ø¨Ù‚Ù‡]",
            session["experience"]
        )

        send_message(
            chat_id,
            "ðŸ“œ Ù…ØªÙ† ØªØ¹Ù‡Ø¯ Ùˆ Ø®ÙˆØ¯Ø§Ø¸Ù‡Ø§Ø±ÛŒ Ù…ØªØ®ØµØµ\n\n"
            + declaration_preview
            + "\n\n"
            "Ø§Ú¯Ø± Ù…ØªÙ† Ø±Ùˆ Ú©Ø§Ù…Ù„ Ù…Ø·Ø§Ù„Ø¹Ù‡ Ú©Ø±Ø¯ÛŒ Ùˆ Ù‚Ø¨ÙˆÙ„Ø´ Ø¯Ø§Ø±ÛŒØŒ "
            "Ø¯Ú©Ù…Ù‡ Ø²ÛŒØ± Ø±Ùˆ Ø¨Ø²Ù†:",
            {
                "keyboard": [
                    [
                        {
                            "text": "âœ… ØªØ£ÛŒÛŒØ¯ Ùˆ Ø§Ø±Ø³Ø§Ù„"
                        }
                    ],
                    [
                        {
                            "text": "âŒ Ø§Ù†ØµØ±Ø§Ù"
                        }
                    ]
                ],
                "resize_keyboard": True
            }
        )

        return True

    # -----------------------------------------
    # ØªØ£ÛŒÛŒØ¯ Ù†Ù‡Ø§ÛŒÛŒ
    # -----------------------------------------

    if step == "confirmation":

        text = message.get(
            "text",
            ""
        ).strip()

        # -----------------------------------------
        # Ø§Ù†ØµØ±Ø§Ù
        # -----------------------------------------

        if text == "âŒ Ø§Ù†ØµØ±Ø§Ù":

            del self_declaration_sessions[
                chat_id
            ]

            send_message(
                chat_id,
                "âŒ ÙØ±Ù… Ø®ÙˆØ¯Ø§Ø¸Ù‡Ø§Ø±ÛŒ Ù„ØºÙˆ Ø´Ø¯.",
                main_keyboard()
            )

            return True

        # -----------------------------------------
        # ØªØ£ÛŒÛŒØ¯ Ùˆ Ø§Ø±Ø³Ø§Ù„
        # -----------------------------------------

        if text == "âœ… ØªØ£ÛŒÛŒØ¯ Ùˆ Ø§Ø±Ø³Ø§Ù„":

            print(
                f"[SELF DECLARATION] "
                f"User confirmed | chat_id={chat_id}"
            )

            # -----------------------------------------
            # Ø§ÙˆÙ„:
            # Ù…ØªÙ† â†’ Ø¹Ú©Ø³ â†’ Ø§Ø±Ø³Ø§Ù„ Ø¨Ù‡ Ø§Ø¯Ù…ÛŒÙ†
            # -----------------------------------------

            success = send_self_declaration_to_admin(
                chat_id
            )

            # -----------------------------------------
            # ÙÙ‚Ø· Ø§Ú¯Ø± Ø¹Ú©Ø³ Ø¨Ø§ Ù…ÙˆÙÙ‚ÛŒØª Ø§Ø±Ø³Ø§Ù„ Ø´Ø¯
            # -----------------------------------------

            if success:

                del self_declaration_sessions[
                    chat_id
                ]

                send_message(
                    chat_id,
                    "âœ… Ø§Ø·Ù„Ø§Ø¹Ø§Øª Ø®ÙˆØ¯Ø§Ø¸Ù‡Ø§Ø±ÛŒ Ø´Ù…Ø§ Ø«Ø¨Øª Ø´Ø¯.\n\n"
                    "ØªØ¹Ù‡Ø¯Ù†Ø§Ù…Ù‡ Ù†Ù‡Ø§ÛŒÛŒ Ø¨Ù‡â€ŒØµÙˆØ±Øª ØªØµÙˆÛŒØ± Ø¨Ø±Ø§ÛŒ "
                    "Ù¾Ø´ØªÛŒØ¨Ø§Ù†ÛŒ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± Ø§Ø±Ø³Ø§Ù„ Ø´Ø¯. ðŸ’›",
                    main_keyboard()
                )

            else:

                send_message(
                    chat_id,
                    "âš ï¸ Ù‡Ù†Ú¯Ø§Ù… Ø§Ø±Ø³Ø§Ù„ Ø®ÙˆØ¯Ø§Ø¸Ù‡Ø§Ø±ÛŒ Ù…Ø´Ú©Ù„ÛŒ Ù¾ÛŒØ´ Ø¢Ù…Ø¯.\n\n"
                    "Ø§Ø·Ù„Ø§Ø¹Ø§Øª Ø´Ù…Ø§ Ø­Ø°Ù Ù†Ø´Ø¯Ù‡ Ø§Ø³Øª.\n"
                    "Ù„Ø·ÙØ§Ù‹ Ø¯ÙˆØ¨Ø§Ø±Ù‡ Ø±ÙˆÛŒ Â«âœ… ØªØ£ÛŒÛŒØ¯ Ùˆ Ø§Ø±Ø³Ø§Ù„Â» Ø¨Ø²Ù†."
                )

            return True

        send_message(
            chat_id,
            "Ù„Ø·ÙØ§Ù‹ ÛŒÚ©ÛŒ Ø§Ø² Ú¯Ø²ÛŒÙ†Ù‡â€ŒÙ‡Ø§ÛŒ Ø²ÛŒØ± Ø±Ùˆ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†."
        )

        return True

    return True


# =========================================================
# Ù…ØºØ² Ù¾Ø§Ø³Ø®â€ŒÚ¯ÙˆÛŒÛŒ
# =========================================================

def answer(text):

    text = normalize_text(text)

    # Ø³Ù„Ø§Ù…
    if contains_any(text, [
        "Ø³Ù„Ø§Ù…",
        "Ø¯Ø±ÙˆØ¯",
        "ØµØ¨Ø­ Ø¨Ø®ÛŒØ±",
        "Ø´Ø¨ Ø¨Ø®ÛŒØ±",
        "Ø®Ø³ØªÙ‡ Ù†Ø¨Ø§Ø´ÛŒØ¯"
    ]):

        return (
            "Ø³Ù„Ø§Ù… ðŸ‘‹âœ¨\n\n"
            "Ø¨Ù‡ Ø¯Ø³ØªÛŒØ§Ø± Ù‡ÙˆØ´Ù…Ù†Ø¯ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± Ø®ÙˆØ´ Ø¢Ù…Ø¯ÛŒØ¯.\n\n"
            "Ù…Ù† Ù…ÛŒâ€ŒØªÙˆÙ†Ù… Ø¯Ø±Ø¨Ø§Ø±Ù‡ Ø«Ø¨Øª Ø³ÙØ§Ø±Ø´ØŒ Ù…ØªØ®ØµØµÛŒÙ†ØŒ "
            "Ù‚ÛŒÙ…ØªØŒ Ù¾Ø±Ø¯Ø§Ø®ØªØŒ Ø¶Ù…Ø§Ù†ØªØŒ Ù‚ÙˆØ§Ù†ÛŒÙ† Ùˆ Ù†Ø­ÙˆÙ‡ "
            "Ú©Ø§Ø± Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± Ø±Ø§Ù‡Ù†Ù…Ø§ÛŒÛŒâ€ŒØªÙˆÙ† Ú©Ù†Ù….\n\n"
            "Ø³Ø¤Ø§Ù„ØªÙˆÙ† Ø±Ùˆ Ù‡Ù…ÛŒÙ†Ø¬Ø§ Ø¨Ù†ÙˆÛŒØ³ÛŒØ¯ ÛŒØ§ Ø§Ø² Ù…Ù†ÙˆÛŒ "
            "Ù¾Ø§ÛŒÛŒÙ† Ø§Ø³ØªÙØ§Ø¯Ù‡ Ú©Ù†ÛŒØ¯."
        ), None

    # Ø¢Ù†ÛŒ Ú©Ø§Ø± Ú†ÛŒØ³Øª
    if contains_any(text, [
        "Ø¢Ù†ÛŒ Ú©Ø§Ø± Ú†ÛŒÙ‡",
        "Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± Ú†ÛŒÙ‡",
        "Ø¢Ù†ÛŒ Ú©Ø§Ø± Ú†ÛŒØ³Øª",
        "Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± Ú†ÛŒØ³Øª",
        "Ø¢Ù†ÛŒ Ú©Ø§Ø± ÛŒØ¹Ù†ÛŒ Ú†ÛŒ",
        "Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± ÛŒØ¹Ù†ÛŒ Ú†ÛŒ",
        "Ø¯Ø±Ø¨Ø§Ø±Ù‡ Ø¢Ù†ÛŒ Ú©Ø§Ø±",
        "Ø¯Ø±Ø¨Ø§Ø±Ù‡ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±",
        "Ø¯Ø± Ù…ÙˆØ±Ø¯ Ø¢Ù†ÛŒ Ú©Ø§Ø±",
        "Ø¯Ø± Ù…ÙˆØ±Ø¯ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±",
        "Ù…Ø¹Ø±ÙÛŒ Ø¢Ù†ÛŒ Ú©Ø§Ø±",
        "Ù…Ø¹Ø±ÙÛŒ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±",
        "Ø§ÛŒÙ† Ø¢Ù†ÛŒ Ú©Ø§Ø± Ú†ÛŒÙ‡",
        "Ø§ÛŒÙ† Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± Ú†ÛŒÙ‡"
    ]):

        return (
            "ðŸ’› Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± Ú†ÛŒØ³ØªØŸ\n\n"
            "Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± ÛŒÚ© Ù¾Ù„ØªÙØ±Ù… Ø¨Ø±Ø§ÛŒ Ø§Ø±ØªØ¨Ø§Ø· Ù…Ø´ØªØ±ÛŒØ§Ù† "
            "Ø¨Ø§ Ù…ØªØ®ØµØµÛŒÙ† Ø®Ø¯Ù…Ø§Øª Ù…Ø®ØªÙ„Ù Ø¯Ø± Ù…Ø­Ù„ Ø§Ø³Øª.\n\n"
            "Ù‡Ø¯Ù Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± Ø§ÛŒÙ†Ù‡ Ú©Ù‡ Ù¾ÛŒØ¯Ø§ Ú©Ø±Ø¯Ù† Ù…ØªØ®ØµØµ "
            "Ù…Ù†Ø§Ø³Ø¨ Ø¨Ø±Ø§ÛŒ Ø®Ø¯Ù…Ø§Øª Ù…ÙˆØ±Ø¯Ù†ÛŒØ§Ø²ØŒ Ø³Ø±ÛŒØ¹â€ŒØªØ±ØŒ "
            "Ù…Ø·Ù…Ø¦Ù†â€ŒØªØ± Ùˆ Ø³Ø§Ø¯Ù‡â€ŒØªØ± Ø§Ù†Ø¬Ø§Ù… Ø¨Ø´Ù‡.\n\n"
            "ðŸŒ Ø¨Ø±Ø§ÛŒ Ø¢Ø´Ù†Ø§ÛŒÛŒ Ø¨ÛŒØ´ØªØ± Ø¨Ø§ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±:"
        ), inline_button(
            "ðŸŒ ÙˆØ±ÙˆØ¯ Ø¨Ù‡ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±",
            SITE_URL
        )

    # Ø«Ø¨Øª Ø³ÙØ§Ø±Ø´
    if contains_any(text, [
        "Ø«Ø¨Øª Ø³ÙØ§Ø±Ø´",
        "Ø³ÙØ§Ø±Ø´ Ø«Ø¨Øª Ú©Ù†Ù…",
        "Ú†Ø·ÙˆØ± Ø³ÙØ§Ø±Ø´",
        "Ú†Ú¯ÙˆÙ†Ù‡ Ø³ÙØ§Ø±Ø´",
        "Ø³ÙØ§Ø±Ø´ Ø¨Ø¯Ù…",
        "Ø³ÙØ§Ø±Ø´ Ø¨Ø²Ø§Ø±Ù…",
        "Ø³ÙØ§Ø±Ø´ Ø¨Ø°Ø§Ø±Ù…",
        "Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ø«Ø¨Øª",
        "Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ø¨Ø¯Ù…",
        "Ù…ØªØ®ØµØµ Ù…ÛŒØ®ÙˆØ§Ù…",
        "Ù…ØªØ®ØµØµ Ù…ÛŒâ€ŒØ®ÙˆØ§Ù…",
        "Ø®Ø¯Ù…Ø§Øª Ù…ÛŒØ®ÙˆØ§Ù…",
        "Ø®Ø¯Ù…Øª Ù…ÛŒØ®ÙˆØ§Ù…",
        "Ø§Ø³ØªØ§Ø¯Ú©Ø§Ø± Ù…ÛŒØ®ÙˆØ§Ù…",
        "Ø§Ø³ØªØ§Ø¯ Ú©Ø§Ø± Ù…ÛŒØ®ÙˆØ§Ù…"
    ]):

        return (
            "ðŸ“ Ø«Ø¨Øª Ø³ÙØ§Ø±Ø´ Ø¯Ø± Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±\n\n"
            "Ø¨Ø±Ø§ÛŒ Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ø®Ø¯Ù…Ø§ØªØŒ Ø®Ø¯Ù…Øª Ù…ÙˆØ±Ø¯Ù†Ø¸Ø±ØªÙˆÙ† "
            "Ø±Ùˆ Ø§Ù†ØªØ®Ø§Ø¨ Ùˆ Ø¯Ø±Ø®ÙˆØ§Ø³ØªØªÙˆÙ† Ø±Ùˆ Ø«Ø¨Øª Ú©Ù†ÛŒØ¯.\n\n"
            "Ù…ØªØ®ØµØµÛŒÙ† Ù…Ø±ØªØ¨Ø· Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ø´Ù…Ø§ Ø±Ùˆ Ø¨Ø±Ø±Ø³ÛŒ "
            "Ù…ÛŒâ€ŒÚ©Ù†Ù† Ùˆ Ù…ÛŒâ€ŒØªÙˆÙ†ÛŒØ¯ Ù…ØªØ®ØµØµ Ù…Ù†Ø§Ø³Ø¨ Ø±Ùˆ "
            "Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ÛŒØ¯.\n\n"
            "ðŸ‘‡ Ø¨Ø±Ø§ÛŒ Ø´Ø±ÙˆØ¹ Ø«Ø¨Øª Ø¯Ø±Ø®ÙˆØ§Ø³Øª:"
        ), inline_button(
            "ðŸš€ Ø«Ø¨Øª Ø³ÙØ§Ø±Ø´ Ø¯Ø± Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±",
            ORDER_URL
        )

    # Ù…ØªØ®ØµØµ
    if contains_any(text, [
        "Ù…ØªØ®ØµØµ Ø¨Ø´Ù…",
        "Ù…ØªØ®ØµØµ Ø´ÙˆÙ…",
        "Ù…ØªØ®ØµØµ Ø´Ø¯Ù†",
        "Ø«Ø¨Øª Ù†Ø§Ù… Ù…ØªØ®ØµØµ",
        "Ø«Ø¨Øªâ€ŒÙ†Ø§Ù… Ù…ØªØ®ØµØµ",
        "Ø¹Ø¶ÙˆÛŒØª Ù…ØªØ®ØµØµ",
        "Ø¹Ø¶Ùˆ Ù…ØªØ®ØµØµ",
        "Ù‡Ù…Ú©Ø§Ø±ÛŒ Ù…ØªØ®ØµØµ",
        "Ù‡Ù…Ú©Ø§Ø±ÛŒ Ø¨Ø§ Ø¢Ù†ÛŒ Ú©Ø§Ø±",
        "Ù‡Ù…Ú©Ø§Ø±ÛŒ Ø¨Ø§ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±",
        "Ú†Ø·ÙˆØ± Ø¨Ø§ Ø¢Ù†ÛŒ Ú©Ø§Ø± Ù‡Ù…Ú©Ø§Ø±ÛŒ",
        "Ú†Ø·ÙˆØ± Ø¨Ø§ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± Ù‡Ù…Ú©Ø§Ø±ÛŒ",
        "Ø§Ø³ØªØ§Ø¯Ú©Ø§Ø± Ø¨Ø´Ù…",
        "Ø§Ø³ØªØ§Ø¯ Ú©Ø§Ø± Ø¨Ø´Ù…",
        "Ø«Ø¨Øª Ù†Ø§Ù… Ø§Ø³ØªØ§Ø¯Ú©Ø§Ø±",
        "Ø«Ø¨Øªâ€ŒÙ†Ø§Ù… Ø§Ø³ØªØ§Ø¯Ú©Ø§Ø±"
    ]):

        return (
            "ðŸ‘¨â€ðŸ”§ Ù‡Ù…Ú©Ø§Ø±ÛŒ Ø¨Ø§ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±\n\n"
            "Ø§Ú¯Ø± Ø¯Ø± Ø²Ù…ÛŒÙ†Ù‡ Ø®Ø¯Ù…Ø§Øª ØªØ®ØµØµ Ø¯Ø§Ø±ÛŒØ¯ Ùˆ "
            "Ù…ÛŒâ€ŒØ®ÙˆØ§Ù‡ÛŒØ¯ Ø¨Ù‡â€ŒØ¹Ù†ÙˆØ§Ù† Ù…ØªØ®ØµØµ Ø¨Ø§ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± "
            "Ù‡Ù…Ú©Ø§Ø±ÛŒ Ú©Ù†ÛŒØ¯ØŒ Ù…ÛŒâ€ŒØªÙˆÙ†ÛŒØ¯ Ø§Ø² Ø·Ø±ÛŒÙ‚ ØµÙØ­Ù‡ "
            "Ø«Ø¨Øªâ€ŒÙ†Ø§Ù… Ù…ØªØ®ØµØµ Ø§Ù‚Ø¯Ø§Ù… Ú©Ù†ÛŒØ¯.\n\n"
            "ðŸ‘‡ Ø´Ø±ÙˆØ¹ Ø«Ø¨Øªâ€ŒÙ†Ø§Ù…:"
        ), inline_button(
            "ðŸš€ Ø«Ø¨Øªâ€ŒÙ†Ø§Ù… Ù…ØªØ®ØµØµ",
            SPECIALIST_URL
        )

    # Ù†Ø­ÙˆÙ‡ Ú©Ø§Ø±
    if contains_any(text, [
        "Ù†Ø­ÙˆÙ‡ Ú©Ø§Ø±",
        "Ú†Ø·ÙˆØ± Ú©Ø§Ø± Ù…ÛŒÚ©Ù†Ù‡",
        "Ú†Ø·ÙˆØ± Ú©Ø§Ø± Ù…ÛŒâ€ŒÚ©Ù†Ù‡",
        "Ú†Ú¯ÙˆÙ†Ù‡ Ú©Ø§Ø± Ù…ÛŒÚ©Ù†Ø¯",
        "Ú†Ú¯ÙˆÙ†Ù‡ Ú©Ø§Ø± Ù…ÛŒâ€ŒÚ©Ù†Ù‡",
        "Ø±ÙˆØ´ Ú©Ø§Ø±",
        "Ø¢Ù…ÙˆØ²Ø´ Ú©Ø§Ø± Ø¨Ø§ Ø¨Ø±Ù†Ø§Ù…Ù‡",
        "Ø¢Ù…ÙˆØ²Ø´ Ø¨Ø±Ù†Ø§Ù…Ù‡",
        "Ø±Ø§Ù‡Ù†Ù…Ø§ÛŒ Ø¨Ø±Ù†Ø§Ù…Ù‡",
        "Ú†Ø·ÙˆØ± Ø§Ø² Ø¨Ø±Ù†Ø§Ù…Ù‡ Ø§Ø³ØªÙØ§Ø¯Ù‡",
        "Ú†Ú¯ÙˆÙ†Ù‡ Ø§Ø² Ø¨Ø±Ù†Ø§Ù…Ù‡ Ø§Ø³ØªÙØ§Ø¯Ù‡",
        "Ú†Ø·ÙˆØ± Ø§Ø² Ø¢Ù†ÛŒ Ú©Ø§Ø± Ø§Ø³ØªÙØ§Ø¯Ù‡",
        "Ú†Ø·ÙˆØ± Ø§Ø² Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± Ø§Ø³ØªÙØ§Ø¯Ù‡"
    ]):

        return (
            "ðŸ“± Ù†Ø­ÙˆÙ‡ Ú©Ø§Ø± Ø¨Ø§ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±\n\n"
            "Ø¨Ø±Ø§ÛŒ Ù…Ø´Ø§Ù‡Ø¯Ù‡ Ø¢Ù…ÙˆØ²Ø´ Ùˆ Ø¢Ø´Ù†Ø§ÛŒÛŒ Ú©Ø§Ù…Ù„ "
            "Ø¨Ø§ Ù†Ø­ÙˆÙ‡ Ø§Ø³ØªÙØ§Ø¯Ù‡ Ø§Ø² Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±ØŒ Ø±Ø§Ù‡Ù†Ù…Ø§ÛŒ "
            "Ù…Ø®ØµÙˆØµ Ú©Ø§Ø±Ø¨Ø±Ø§Ù† Ø±Ùˆ Ø¨Ø¨ÛŒÙ†ÛŒØ¯.\n\n"
            "ðŸ‘‡ Ù…Ø´Ø§Ù‡Ø¯Ù‡ Ø±Ø§Ù‡Ù†Ù…Ø§:"
        ), inline_button(
            "ðŸŽ¬ Ù…Ø´Ø§Ù‡Ø¯Ù‡ Ù†Ø­ÙˆÙ‡ Ú©Ø§Ø±",
            WORK_URL
        )

    # Ù‚ÛŒÙ…Øª
    if contains_any(text, [
        "Ù‚ÛŒÙ…Øª",
        "Ù‡Ø²ÛŒÙ†Ù‡",
        "Ù†Ø±Ø®",
        "Ø§Ø¬Ø±Øª",
        "Ø¯Ø³ØªÙ…Ø²Ø¯",
        "Ú†Ù‚Ø¯Ø± Ù…ÛŒØ´Ù‡",
        "Ú†Ù†Ø¯ Ù…ÛŒØ´Ù‡",
        "Ù‡Ø²ÛŒÙ†Ù‡ Ú©Ø§Ø±",
        "Ù‚ÛŒÙ…Øª Ú©Ø§Ø±",
        "Ù‚ÛŒÙ…Øª Ø®Ø¯Ù…Ø§Øª"
    ]):

        return (
            "ðŸ’° Ù‚ÛŒÙ…Øª Ø®Ø¯Ù…Ø§Øª Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±\n\n"
            "Ù‡Ø²ÛŒÙ†Ù‡ Ù†Ù‡Ø§ÛŒÛŒ Ø®Ø¯Ù…Ø§Øª Ù…ÛŒâ€ŒØªÙˆÙ†Ù‡ Ø¨Ø§ ØªÙˆØ¬Ù‡ "
            "Ø¨Ù‡ Ù†ÙˆØ¹ Ø®Ø¯Ù…ØªØŒ Ø´Ø±Ø§ÛŒØ· Ú©Ø§Ø±ØŒ Ù…ÛŒØ²Ø§Ù† Ú©Ø§Ø± "
            "Ùˆ Ù†Ø¸Ø± Ù…ØªØ®ØµØµ Ù…ØªÙØ§ÙˆØª Ø¨Ø§Ø´Ù‡.\n\n"
            "Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± Ø¨Ø±Ø§ÛŒ Ø±Ø§Ù‡Ù†Ù…Ø§ÛŒÛŒ Ù…Ø´ØªØ±ÛŒØŒ Ø§Ø·Ù„Ø§Ø¹Ø§Øª "
            "Ù‚ÛŒÙ…Øª Ø®Ø¯Ù…Ø§Øª Ø±Ùˆ Ø¯Ø± ÙØ±Ø¢ÛŒÙ†Ø¯ Ø«Ø¨Øª Ø¯Ø±Ø®ÙˆØ§Ø³Øª "
            "Ø§Ø±Ø§Ø¦Ù‡ Ù…ÛŒâ€ŒÚ©Ù†Ù‡."
        ), inline_button(
            "ðŸ“ Ù…Ø´Ø§Ù‡Ø¯Ù‡ Ø®Ø¯Ù…Ø§Øª Ùˆ Ø«Ø¨Øª Ø³ÙØ§Ø±Ø´",
            ORDER_URL
        )

    # Ú©Ù…ÛŒØ³ÛŒÙˆÙ†
    if contains_any(text, [
        "Ú©Ù…ÛŒØ³ÛŒÙˆÙ†",
        "Ø¯Ø±ØµØ¯ Ú©Ù…ÛŒØ³ÛŒÙˆÙ†",
        "Ø¯Ø±ØµØ¯ Ø¢Ù†ÛŒ Ú©Ø§Ø±",
        "Ø¯Ø±ØµØ¯ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±",
        "Ø³Ù‡Ù… Ø¢Ù†ÛŒ Ú©Ø§Ø±",
        "Ø³Ù‡Ù… Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±",
        "Ú©Ù…ÛŒØ³ÛŒÙˆÙ† Ù…ØªØ®ØµØµ"
    ]):

        return (
            "ðŸ’³ Ú©Ù…ÛŒØ³ÛŒÙˆÙ† Ù…ØªØ®ØµØµÛŒÙ†\n\n"
            "Ø¯Ø±ØµØ¯ Ùˆ Ø´Ø±Ø§ÛŒØ· Ú©Ù…ÛŒØ³ÛŒÙˆÙ† Ù…ØªØ®ØµØµÛŒÙ† Ø·Ø¨Ù‚ "
            "Ù‚ÙˆØ§Ù†ÛŒÙ† Ùˆ Ø´Ø±Ø§ÛŒØ· Ù‡Ù…Ú©Ø§Ø±ÛŒ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± ØªØ¹ÛŒÛŒÙ† "
            "Ø´Ø¯Ù‡ Ø§Ø³Øª.\n\n"
            "Ø¨Ø±Ø§ÛŒ Ù…Ø´Ø§Ù‡Ø¯Ù‡ Ø¯Ø±ØµØ¯ Ùˆ Ø¬Ø²Ø¦ÛŒØ§Øª Ø¯Ù‚ÛŒÙ‚ØŒ "
            "ØµÙØ­Ù‡ Ù‚ÙˆØ§Ù†ÛŒÙ† Ù…ØªØ®ØµØµÛŒÙ† Ø±Ùˆ Ø¨Ø¨ÛŒÙ†ÛŒØ¯."
        ), inline_button(
            "ðŸ“‹ Ù…Ø´Ø§Ù‡Ø¯Ù‡ Ù‚ÙˆØ§Ù†ÛŒÙ† Ù…ØªØ®ØµØµÛŒÙ†",
            SPECIALIST_RULES_URL
        )

    # Ù¾Ø±Ø¯Ø§Ø®Øª
    if contains_any(text, [
        "Ù¾Ø±Ø¯Ø§Ø®Øª",
        "Ù¾ÙˆÙ„ Ø±Ùˆ Ø¨Ø¯Ù…",
        "Ù¾ÙˆÙ„ Ø±Ø§ Ø¨Ø¯Ù…",
        "Ù¾ÙˆÙ„ Ù…ØªØ®ØµØµ",
        "Ù…Ø¨Ù„Øº Ú©Ø§Ø±",
        "ÙˆØ§Ø±ÛŒØ²",
        "Ø¯Ø±Ú¯Ø§Ù‡",
        "Ù…Ø³ØªÙ‚ÛŒÙ… Ø¨Ù‡ Ù…ØªØ®ØµØµ",
        "Ù…Ø³ØªÙ‚ÛŒÙ… Ø¨Ù‡ Ø§Ø³ØªØ§Ø¯Ú©Ø§Ø±"
    ]):

        return (
            "ðŸ’³ Ù¾Ø±Ø¯Ø§Ø®Øª Ø§Ù…Ù† Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±\n\n"
            "Ø¨Ø±Ø§ÛŒ Ø¨Ø±Ø®ÙˆØ±Ø¯Ø§Ø±ÛŒ Ø§Ø² ÙØ±Ø¢ÛŒÙ†Ø¯ Ø¶Ù…Ø§Ù†Øª Ùˆ "
            "Ù¾ÛŒÚ¯ÛŒØ±ÛŒ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±ØŒ Ù…Ø¨Ù„Øº Ú©Ø§Ø± Ø¨Ø§ÛŒØ¯ Ø§Ø² "
            "Ø·Ø±ÛŒÙ‚ Ø¯Ø±Ú¯Ø§Ù‡ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± Ù¾Ø±Ø¯Ø§Ø®Øª Ø¨Ø´Ù‡.\n\n"
            "Ù¾Ø³ Ø§Ø² Ù¾Ø±Ø¯Ø§Ø®ØªØŒ Ù…Ø¨Ù„Øº ØªØ§ Û·Û² Ø³Ø§Ø¹Øª "
            "Ø¯Ø± ÙˆØ¶Ø¹ÛŒØª Ø¨Ù„ÙˆÚ©Ù‡ Ø¨Ø§Ù‚ÛŒ Ù…ÛŒâ€ŒÙ…ÙˆÙ†Ù‡.\n\n"
            "Ø§Ú¯Ø± Ù…Ø´ØªØ±ÛŒ Ø¯Ø± Ø§ÛŒÙ† Ø¨Ø§Ø²Ù‡ Ù…Ø´Ú©Ù„ÛŒ Ø¯Ø±Ø¨Ø§Ø±Ù‡ "
            "Ø§Ù†Ø¬Ø§Ù… Ú©Ø§Ø± Ø§Ø¹Ù„Ø§Ù… Ù†Ú©Ù†Ù‡ØŒ Ù…Ø¨Ù„Øº Ø·Ø¨Ù‚ "
            "ÙØ±Ø¢ÛŒÙ†Ø¯ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± Ø¨Ù‡ Ù…ØªØ®ØµØµ Ù¾Ø±Ø¯Ø§Ø®Øª Ù…ÛŒâ€ŒØ´Ù‡."
        ), inline_button(
            "ðŸ“œ Ù…Ø´Ø§Ù‡Ø¯Ù‡ Ù‚ÙˆØ§Ù†ÛŒÙ† Ù…Ø´ØªØ±ÛŒ",
            CUSTOMER_RULES_URL
        )

    # Ø¶Ù…Ø§Ù†Øª
    if contains_any(text, [
        "Ø¶Ù…Ø§Ù†Øª",
        "Ú¯Ø§Ø±Ø§Ù†ØªÛŒ",
        "Ù¾ÙˆÙ„ Ø¨Ù„ÙˆÚ©Ù‡",
        "Û·Û² Ø³Ø§Ø¹Øª",
        "72 Ø³Ø§Ø¹Øª",
        "Ù‡ÙØªØ§Ø¯ Ùˆ Ø¯Ùˆ Ø³Ø§Ø¹Øª",
        "Ø§Ú¯Ø± Ù…Ø´Ú©Ù„ Ø¯Ø§Ø´ØªÙ‡ Ø¨Ø§Ø´Ù…",
        "Ø§Ú¯Ø± Ù…Ø´Ú©Ù„ÛŒ Ù¾ÛŒØ´ Ø¨ÛŒØ§Ø¯",
        "Ù…Ø´Ú©Ù„ Ø¨Ø¹Ø¯ Ø§Ø² Ú©Ø§Ø±",
        "Ù†Ø§Ø±Ø¶Ø§ÛŒØªÛŒ",
        "Ù†Ø§Ø±Ø§Ø¶ÛŒ",
        "Ú©Ø§Ø± Ø®Ø±Ø§Ø¨",
        "Ù…ØªØ®ØµØµ Ú©Ø§Ø± Ø±Ùˆ Ø®Ø±Ø§Ø¨"
    ]):

        return (
            "ðŸ›¡ï¸ Ø¶Ù…Ø§Ù†Øª Ùˆ Ù¾ÛŒÚ¯ÛŒØ±ÛŒ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±\n\n"
            "Ø¨Ø±Ø§ÛŒ Ø§Ø³ØªÙØ§Ø¯Ù‡ Ø§Ø² ÙØ±Ø¢ÛŒÙ†Ø¯ Ø¶Ù…Ø§Ù†ØªØŒ "
            "Ù¾Ø±Ø¯Ø§Ø®Øª Ø¨Ø§ÛŒØ¯ Ø§Ø² Ø·Ø±ÛŒÙ‚ Ø¯Ø±Ú¯Ø§Ù‡ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± "
            "Ø§Ù†Ø¬Ø§Ù… Ø¨Ø´Ù‡.\n\n"
            "ðŸ’³ Ù…Ø¨Ù„Øº Ù¾Ø±Ø¯Ø§Ø®ØªÛŒ ØªØ§ Û·Û² Ø³Ø§Ø¹Øª Ø¨Ù„ÙˆÚ©Ù‡ "
            "Ù…ÛŒâ€ŒÙ…ÙˆÙ†Ù‡.\n\n"
            "Ø§Ú¯Ø± Ù…Ø´ØªØ±ÛŒ Ù…Ø´Ú©Ù„ÛŒ Ø¯Ø±Ø¨Ø§Ø±Ù‡ Ø§Ù†Ø¬Ø§Ù… Ú©Ø§Ø± "
            "Ø§Ø¹Ù„Ø§Ù… Ù†Ú©Ù†Ù‡ØŒ Ù…Ø¨Ù„Øº Ø·Ø¨Ù‚ ÙØ±Ø¢ÛŒÙ†Ø¯ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± "
            "Ø¨Ù‡ Ù…ØªØ®ØµØµ Ù¾Ø±Ø¯Ø§Ø®Øª Ù…ÛŒâ€ŒØ´Ù‡.\n\n"
            "Ø¯Ø± ØµÙˆØ±Øª Ø¨Ø±ÙˆØ² Ù…Ø´Ú©Ù„ØŒ Ù…ÙˆØ¶ÙˆØ¹ Ø¨Ø§ÛŒØ¯ Ø§Ø² "
            "Ø·Ø±ÛŒÙ‚ Ù¾Ø´ØªÛŒØ¨Ø§Ù†ÛŒ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± Ù¾ÛŒÚ¯ÛŒØ±ÛŒ Ø¨Ø´Ù‡."
        ), inline_button(
            "ðŸ“œ Ù‚ÙˆØ§Ù†ÛŒÙ† Ùˆ Ø´Ø±Ø§ÛŒØ·",
            CUSTOMER_RULES_URL
        )

    # Ù‚ÙˆØ§Ù†ÛŒÙ† Ù…Ø´ØªØ±ÛŒ
    if contains_any(text, [
        "Ù‚ÙˆØ§Ù†ÛŒÙ† Ù…Ø´ØªØ±ÛŒ",
        "Ù‚Ø§Ù†ÙˆÙ† Ù…Ø´ØªØ±ÛŒ",
        "Ø´Ø±Ø§ÛŒØ· Ù…Ø´ØªØ±ÛŒ",
        "Ù‚ÙˆØ§Ù†ÛŒÙ† Ø³Ø§ÛŒØª",
        "Ù‚ÙˆØ§Ù†ÛŒÙ† Ø¢Ù†ÛŒ Ú©Ø§Ø±",
        "Ù‚ÙˆØ§Ù†ÛŒÙ† Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±",
        "Ù‚Ø§Ù†ÙˆÙ† Ø¢Ù†ÛŒ Ú©Ø§Ø±",
        "Ù‚Ø§Ù†ÙˆÙ† Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±"
    ]):

        return (
            "ðŸ“œ Ù‚ÙˆØ§Ù†ÛŒÙ† Ù…Ø´ØªØ±ÛŒØ§Ù† Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±\n\n"
            "Ø¨Ø±Ø§ÛŒ Ù…Ø´Ø§Ù‡Ø¯Ù‡ Ù†Ø³Ø®Ù‡ Ú©Ø§Ù…Ù„ Ùˆ Ø¨Ù‡â€ŒØ±ÙˆØ² "
            "Ù‚ÙˆØ§Ù†ÛŒÙ† Ùˆ Ø´Ø±Ø§ÛŒØ· Ø§Ø³ØªÙØ§Ø¯Ù‡ØŒ Ø§Ø² ØµÙØ­Ù‡ "
            "Ø±Ø³Ù…ÛŒ Ù‚ÙˆØ§Ù†ÛŒÙ† Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± Ø§Ø³ØªÙØ§Ø¯Ù‡ Ú©Ù†ÛŒØ¯.\n\n"
            "ðŸ‘‡ Ù…Ø´Ø§Ù‡Ø¯Ù‡ Ù‚ÙˆØ§Ù†ÛŒÙ†:"
        ), inline_button(
            "ðŸ“– Ù‚ÙˆØ§Ù†ÛŒÙ† Ù…Ø´ØªØ±ÛŒØ§Ù†",
            CUSTOMER_RULES_URL
        )

    # Ù‚ÙˆØ§Ù†ÛŒÙ† Ù…ØªØ®ØµØµ
    if contains_any(text, [
        "Ù‚ÙˆØ§Ù†ÛŒÙ† Ù…ØªØ®ØµØµ",
        "Ù‚Ø§Ù†ÙˆÙ† Ù…ØªØ®ØµØµ",
        "Ø´Ø±Ø§ÛŒØ· Ù…ØªØ®ØµØµ",
        "Ù‚ÙˆØ§Ù†ÛŒÙ† Ø§Ø³ØªØ§Ø¯Ú©Ø§Ø±",
        "Ù‚Ø§Ù†ÙˆÙ† Ø§Ø³ØªØ§Ø¯Ú©Ø§Ø±",
        "Ø´Ø±Ø§ÛŒØ· Ù‡Ù…Ú©Ø§Ø±ÛŒ Ù…ØªØ®ØµØµ"
    ]):

        return (
            "ðŸ“‹ Ù‚ÙˆØ§Ù†ÛŒÙ† Ù…ØªØ®ØµØµÛŒÙ† Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±\n\n"
            "Ø¯Ø± ØµÙØ­Ù‡ Ù‚ÙˆØ§Ù†ÛŒÙ† Ù…ØªØ®ØµØµÛŒÙ†ØŒ Ø´Ø±Ø§ÛŒØ· "
            "Ù‡Ù…Ú©Ø§Ø±ÛŒØŒ Ú©Ù…ÛŒØ³ÛŒÙˆÙ† Ùˆ Ø¶ÙˆØ§Ø¨Ø· Ù…Ø±Ø¨ÙˆØ· "
            "Ø¨Ù‡ Ù…ØªØ®ØµØµÛŒÙ† Ø¨Ù‡â€ŒØµÙˆØ±Øª Ú©Ø§Ù…Ù„ ØªÙˆØ¶ÛŒØ­ "
            "Ø¯Ø§Ø¯Ù‡ Ø´Ø¯Ù‡ Ø§Ø³Øª.\n\n"
            "ðŸ‘‡ Ù…Ø´Ø§Ù‡Ø¯Ù‡ Ù‚ÙˆØ§Ù†ÛŒÙ†:"
        ), inline_button(
            "ðŸ“‹ Ù‚ÙˆØ§Ù†ÛŒÙ† Ù…ØªØ®ØµØµÛŒÙ†",
            SPECIALIST_RULES_URL
        )

    # Ù¾Ø´ØªÛŒØ¨Ø§Ù†ÛŒ
    if contains_any(text, [
        "Ù¾Ø´ØªÛŒØ¨Ø§Ù†ÛŒ",
        "Ú©Ù…Ú©",
        "Ø±Ø§Ù‡Ù†Ù…Ø§ÛŒÛŒ",
        "Ù…Ø´Ú©Ù„ Ø¯Ø§Ø±Ù…",
        "Ù…Ø´Ú©Ù„ Ù¾ÛŒØ´ Ø§ÙˆÙ…Ø¯Ù‡",
        "Ù…Ø´Ú©Ù„ Ù¾ÛŒØ´ Ø¢Ù…Ø¯Ù‡",
        "ØªÙ…Ø§Ø³",
        "Ø§Ø±ØªØ¨Ø§Ø·",
        "Ù¾ÛŒÚ¯ÛŒØ±ÛŒ"
    ]):

        return (
            "ðŸŽ§ Ù¾Ø´ØªÛŒØ¨Ø§Ù†ÛŒ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±\n\n"
            "Ù…ÙˆØ¶ÙˆØ¹ ÛŒØ§ Ù…Ø´Ú©Ù„ØªÙˆÙ† Ø±Ùˆ Ù‡Ù…ÛŒÙ†Ø¬Ø§ "
            "ØªÙˆØ¶ÛŒØ­ Ø¨Ø¯ÛŒØ¯ ØªØ§ Ø±Ø§Ù‡Ù†Ù…Ø§ÛŒÛŒâ€ŒØªÙˆÙ† Ú©Ù†Ù….\n\n"
            "Ø§Ú¯Ø± Ù…ÙˆØ¶ÙˆØ¹ Ù…Ø±Ø¨ÙˆØ· Ø¨Ù‡ ÛŒÚ© Ø³ÙØ§Ø±Ø´ Ù‡Ø³ØªØŒ "
            "Ø§Ø·Ù„Ø§Ø¹Ø§Øª Ùˆ Ù…Ø³ØªÙ†Ø¯Ø§Øª Ù…Ø±Ø¨ÙˆØ· Ø¨Ù‡ Ø³ÙØ§Ø±Ø´ "
            "Ø±Ùˆ Ù‡Ù… Ø¢Ù…Ø§Ø¯Ù‡ Ø¯Ø§Ø´ØªÙ‡ Ø¨Ø§Ø´ÛŒØ¯."
        ), None

    # FAQ
    if contains_any(text, [
        "Ø³ÙˆØ§Ù„Ø§Øª Ù…ØªØ¯Ø§ÙˆÙ„",
        "Ø³ÙˆØ§Ù„ Ø±Ø§ÛŒØ¬",
        "Ø³ÙˆØ§Ù„Ø§Øª Ø±Ø§ÛŒØ¬",
        "faq",
        "Ú†Ù‡ Ø³ÙˆØ§Ù„Ø§ØªÛŒ",
        "Ø³ÙˆØ§Ù„ Ø¯Ø§Ø±Ù…"
    ]):

        return (
            "â“ Ø³ÙˆØ§Ù„Ø§Øª Ù…ØªØ¯Ø§ÙˆÙ„\n\n"
            "Ù‡Ø± Ø³Ø¤Ø§Ù„ÛŒ Ø¯Ø±Ø¨Ø§Ø±Ù‡ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± Ø¯Ø§Ø±ÛŒØ¯ "
            "Ù…ÛŒâ€ŒØªÙˆÙ†ÛŒØ¯ Ù‡Ù…ÛŒÙ†Ø¬Ø§ Ø¨Ù†ÙˆÛŒØ³ÛŒØ¯.\n\n"
            "Ù…Ø«Ù„Ø§Ù‹:\n"
            "â€¢ Ú†Ø·ÙˆØ± Ø³ÙØ§Ø±Ø´ Ø¨Ø¯Ù…ØŸ\n"
            "â€¢ Ú†Ø·ÙˆØ± Ù…ØªØ®ØµØµ Ø¨Ø´Ù…ØŸ\n"
            "â€¢ Ù¾Ø±Ø¯Ø§Ø®Øª Ú†Ø·ÙˆØ± Ø§Ù†Ø¬Ø§Ù… Ù…ÛŒØ´Ù‡ØŸ\n"
            "â€¢ Ø¶Ù…Ø§Ù†Øª Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± Ú†Ø·ÙˆØ±Ù‡ØŸ\n"
            "â€¢ Ù‚ÙˆØ§Ù†ÛŒÙ† Ø±Ùˆ Ø§Ø² Ú©Ø¬Ø§ Ø¨Ø¨ÛŒÙ†Ù…ØŸ"
        ), None

    # Ø§Ù†ØªØ®Ø§Ø¨ Ù…ØªØ®ØµØµ
    if contains_any(text, [
        "Ú†Ø·ÙˆØ± Ù…ØªØ®ØµØµ Ù¾ÛŒØ¯Ø§ Ú©Ù†Ù…",
        "Ù…ØªØ®ØµØµ Ø§Ø² Ú©Ø¬Ø§ Ù¾ÛŒØ¯Ø§ Ú©Ù†Ù…",
        "Ù…ØªØ®ØµØµ Ù…Ù†Ø§Ø³Ø¨",
        "Ø¨Ù‡ØªØ±ÛŒÙ† Ù…ØªØ®ØµØµ",
        "Ù…ØªØ®ØµØµ Ø®ÙˆØ¨",
        "Ú†Ù†Ø¯ Ù…ØªØ®ØµØµ",
        "Ú†Ù†Ø¯ ØªØ§ Ù…ØªØ®ØµØµ",
        "Ù¾ÛŒØ´Ù†Ù‡Ø§Ø¯ Ù…ØªØ®ØµØµ",
        "Ù¾ÛŒØ´Ù†Ù‡Ø§Ø¯ Ù‚ÛŒÙ…Øª Ù…ØªØ®ØµØµ",
        "Ø§Ù†ØªØ®Ø§Ø¨ Ù…ØªØ®ØµØµ",
        "Ù…ØªØ®ØµØµ Ø±Ùˆ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†Ù…",
        "Ù…ØªØ®ØµØµ Ø±Ø§ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†Ù…",
        "Ø¨Ø¹Ø¯ Ø§Ø² Ø«Ø¨Øª Ø³ÙØ§Ø±Ø´",
        "Ø¨Ø¹Ø¯ Ø«Ø¨Øª Ø³ÙØ§Ø±Ø´",
        "Ø¨Ø¹Ø¯Ø´ Ú†ÛŒ Ù…ÛŒØ´Ù‡",
        "Ø¨Ø¹Ø¯Ø´ Ú†Ù‡ Ø§ØªÙØ§Ù‚ÛŒ Ù…ÛŒÙØªÙ‡"
    ]):

        return (
            "ðŸ‘¨â€ðŸ”§ Ø§Ù†ØªØ®Ø§Ø¨ Ù…ØªØ®ØµØµ Ø¯Ø± Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±\n\n"
            "Ø¨Ø¹Ø¯ Ø§Ø² Ø«Ø¨Øª Ø¯Ø±Ø®ÙˆØ§Ø³ØªØŒ Ù…ØªØ®ØµØµÛŒÙ† Ù…Ø±ØªØ¨Ø· "
            "Ù…ÛŒâ€ŒØªÙˆÙ†Ù† Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ø´Ù…Ø§ Ø±Ùˆ Ø¨Ø±Ø±Ø³ÛŒ Ú©Ù†Ù† "
            "Ùˆ Ù¾ÛŒØ´Ù†Ù‡Ø§Ø¯ Ø®ÙˆØ¯Ø´ÙˆÙ† Ø±Ùˆ Ø§Ø±Ø§Ø¦Ù‡ Ø¨Ø¯Ù†.\n\n"
            "Ø´Ù…Ø§ Ù…ÛŒâ€ŒØªÙˆÙ†ÛŒØ¯ Ù…ØªØ®ØµØµ Ù…Ù†Ø§Ø³Ø¨ Ø±Ùˆ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ÛŒØ¯."
        ), inline_button(
            "ðŸ“ Ø«Ø¨Øª Ø³ÙØ§Ø±Ø´",
            ORDER_URL
        )

    # Ù‚ÛŒÙ…Øª ØªÙˆØ§ÙÙ‚ÛŒ
    if contains_any(text, [
        "Ù‚ÛŒÙ…Øª ØªÙˆØ§ÙÙ‚ÛŒ",
        "Ù‚ÛŒÙ…Øª Ø±Ùˆ Ú©ÛŒ ØªØ¹ÛŒÛŒÙ† Ù…ÛŒÚ©Ù†Ù‡",
        "Ù‚ÛŒÙ…Øª Ø±Ø§ Ú©ÛŒ ØªØ¹ÛŒÛŒÙ† Ù…ÛŒÚ©Ù†Ø¯",
        "Ú†Ù‡ Ú©Ø³ÛŒ Ù‚ÛŒÙ…Øª Ø±Ø§ ØªØ¹ÛŒÛŒÙ† Ù…ÛŒÚ©Ù†Ø¯",
        "Ù…ØªØ®ØµØµ Ù‚ÛŒÙ…Øª",
        "Ù‚ÛŒÙ…Øª Ø¨Ø§ Ù…ØªØ®ØµØµ",
        "Ø§Ø¬Ø±Øª ØªÙˆØ§ÙÙ‚ÛŒ",
        "Ù‡Ø²ÛŒÙ†Ù‡ ØªÙˆØ§ÙÙ‚ÛŒ",
        "Ù‚ÛŒÙ…Øª Ù†Ù‡Ø§ÛŒÛŒ",
        "Ù‚ÛŒÙ…Øª Ù‚Ø·Ø¹ÛŒ",
        "Ù‚ÛŒÙ…Øª Ù‚Ø¨Ù„ Ø§Ø² Ú©Ø§Ø±",
        "Ù‚Ø¨Ù„ Ø§Ø² Ø´Ø±ÙˆØ¹ Ú©Ø§Ø± Ù‚ÛŒÙ…Øª",
        "Ù‚Ø¨Ù„ Ú©Ø§Ø± Ù‚ÛŒÙ…Øª",
        "Ù‚ÛŒÙ…Øª Ú©Ø§Ø± Ø±Ùˆ Ú©ÛŒ Ù…ÛŒÚ¯Ù‡"
    ]):

        return (
            "ðŸ’° Ù‚ÛŒÙ…Øª Ø®Ø¯Ù…Ø§Øª Ø¯Ø± Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±\n\n"
            "Ù‚ÛŒÙ…Øª Ù†Ù‡Ø§ÛŒÛŒ Ø¨Ø§ ØªÙˆØ¬Ù‡ Ø¨Ù‡ Ù†ÙˆØ¹ Ø®Ø¯Ù…ØªØŒ "
            "Ø´Ø±Ø§ÛŒØ· ÙˆØ§Ù‚Ø¹ÛŒ Ú©Ø§Ø±ØŒ Ù…ÛŒØ²Ø§Ù† Ú©Ø§Ø± Ùˆ ØªÙˆØ§ÙÙ‚ "
            "Ø¨ÛŒÙ† Ù…Ø´ØªØ±ÛŒ Ùˆ Ù…ØªØ®ØµØµ ØªØ¹ÛŒÛŒÙ† Ù…ÛŒâ€ŒØ´Ù‡.\n\n"
            "Ø¨Ø±Ø§ÛŒ Ø´Ø±ÙˆØ¹ØŒ Ø®Ø¯Ù…Øª Ù…ÙˆØ±Ø¯Ù†Ø¸Ø± Ø±Ùˆ Ø§Ù†ØªØ®Ø§Ø¨ "
            "Ùˆ Ø¯Ø±Ø®ÙˆØ§Ø³ØªØªÙˆÙ† Ø±Ùˆ Ø«Ø¨Øª Ú©Ù†ÛŒØ¯."
        ), inline_button(
            "ðŸ“ Ø«Ø¨Øª Ø³ÙØ§Ø±Ø´",
            ORDER_URL
        )

    # Ù„ØºÙˆ
    if contains_any(text, [
        "Ù„ØºÙˆ Ø³ÙØ§Ø±Ø´",
        "Ø³ÙØ§Ø±Ø´ Ø±Ùˆ Ù„ØºÙˆ Ú©Ù†Ù…",
        "Ø³ÙØ§Ø±Ø´ Ø±Ø§ Ù„ØºÙˆ Ú©Ù†Ù…",
        "Ú†Ø·ÙˆØ± Ø³ÙØ§Ø±Ø´ Ø±Ùˆ Ù„ØºÙˆ Ú©Ù†Ù…",
        "Ú†Ú¯ÙˆÙ†Ù‡ Ø³ÙØ§Ø±Ø´ Ø±Ø§ Ù„ØºÙˆ Ú©Ù†Ù…",
        "Ù…ÛŒØ®ÙˆØ§Ù… Ø³ÙØ§Ø±Ø´ Ø±Ùˆ Ù„ØºÙˆ Ú©Ù†Ù…",
        "Ù…ÛŒ Ø®ÙˆØ§Ù‡Ù… Ø³ÙØ§Ø±Ø´ Ø±Ø§ Ù„ØºÙˆ Ú©Ù†Ù…",
        "Ú©Ù†Ø³Ù„ Ú©Ø±Ø¯Ù† Ø³ÙØ§Ø±Ø´",
        "Ú©Ù†Ø³Ù„ Ø³ÙØ§Ø±Ø´",
        "Ø³ÙØ§Ø±Ø´ Ú©Ù†Ø³Ù„",
        "Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ø±Ùˆ Ù„ØºÙˆ",
        "Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ø±Ø§ Ù„ØºÙˆ"
    ]):

        return (
            "âŒ Ù„ØºÙˆ Ø³ÙØ§Ø±Ø´\n\n"
            "Ø§Ú¯Ø± Ù‚ØµØ¯ Ù„ØºÙˆ ÛŒÚ© Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ø±Ùˆ Ø¯Ø§Ø±ÛŒØ¯ØŒ "
            "ÙˆØ¶Ø¹ÛŒØª Ø³ÙØ§Ø±Ø´ Ùˆ Ø´Ø±Ø§ÛŒØ· Ù„ØºÙˆ Ø±Ùˆ Ø¨Ø±Ø±Ø³ÛŒ Ú©Ù†ÛŒØ¯.\n\n"
            "Ø§Ú¯Ø± Ø³ÙØ§Ø±Ø´ ÙØ¹Ø§Ù„ Ø¯Ø§Ø±ÛŒØ¯ Ùˆ Ù†ÛŒØ§Ø² Ø¨Ù‡ Ø±Ø§Ù‡Ù†Ù…Ø§ÛŒÛŒ "
            "Ø¯Ø§Ø±ÛŒØ¯ØŒ Ø¨Ø§ Ù¾Ø´ØªÛŒØ¨Ø§Ù†ÛŒ Ø¯Ø± Ø§Ø±ØªØ¨Ø§Ø· Ø¨Ø§Ø´ÛŒØ¯."
        ), None

    # Ø²Ù…Ø§Ù† Ù…ØªØ®ØµØµ
    if contains_any(text, [
        "Ù…ØªØ®ØµØµ Ú©ÛŒ Ù…ÛŒØ§Ø¯",
        "Ù…ØªØ®ØµØµ Ú†Ù‡ Ø²Ù…Ø§Ù†ÛŒ Ù…ÛŒØ§Ø¯",
        "Ú©ÛŒ Ù…ØªØ®ØµØµ Ù…ÛŒØ§Ø¯",
        "Ø²Ù…Ø§Ù† Ø±Ø³ÛŒØ¯Ù† Ù…ØªØ®ØµØµ",
        "Ú†Ù‚Ø¯Ø± Ø·ÙˆÙ„ Ù…ÛŒÚ©Ø´Ù‡ Ù…ØªØ®ØµØµ Ø¨ÛŒØ§Ø¯",
        "Ú†Ù‚Ø¯Ø± Ø·ÙˆÙ„ Ù…ÛŒ Ú©Ø´Ù‡ Ù…ØªØ®ØµØµ Ø¨ÛŒØ§Ø¯",
        "Ú©ÛŒ Ù…ÛŒØ±Ø³Ù‡ Ù…ØªØ®ØµØµ",
        "Ø²Ù…Ø§Ù† Ø­Ø¶ÙˆØ± Ù…ØªØ®ØµØµ",
        "Ø²Ù…Ø§Ù† Ù…Ø±Ø§Ø¬Ø¹Ù‡ Ù…ØªØ®ØµØµ",
        "Ù…ØªØ®ØµØµ Ú†Ù‡ Ø³Ø§Ø¹ØªÛŒ Ù…ÛŒØ§Ø¯",
        "Ø³Ø§Ø¹Øª Ø¢Ù…Ø¯Ù† Ù…ØªØ®ØµØµ"
    ]):

        return (
            "â° Ø²Ù…Ø§Ù† Ù…Ø±Ø§Ø¬Ø¹Ù‡ Ù…ØªØ®ØµØµ\n\n"
            "Ø²Ù…Ø§Ù† Ø­Ø¶ÙˆØ± Ù…ØªØ®ØµØµ Ø¨Ù‡ Ù†ÙˆØ¹ Ø®Ø¯Ù…ØªØŒ "
            "Ø²Ù…Ø§Ù† Ø«Ø¨Øª Ø¯Ø±Ø®ÙˆØ§Ø³ØªØŒ Ø´Ø±Ø§ÛŒØ· Ø³ÙØ§Ø±Ø´ "
            "Ùˆ Ù‡Ù…Ø§Ù‡Ù†Ú¯ÛŒ Ø¨Ø§ Ù…ØªØ®ØµØµ Ø¨Ø³ØªÚ¯ÛŒ Ø¯Ø§Ø±Ù‡."
        ), None

    # Ø´Ù‡Ø±Ù‡Ø§
    if contains_any(text, [
        "Ú©Ø¯ÙˆÙ… Ø´Ù‡Ø±Ù‡Ø§",
        "Ú†Ù‡ Ø´Ù‡Ø±Ù‡Ø§ÛŒÛŒ",
        "Ú©Ø¯Ø§Ù… Ø´Ù‡Ø±Ù‡Ø§",
        "Ø¯Ø± Ú†Ù‡ Ø´Ù‡Ø±Ù‡Ø§ÛŒÛŒ",
        "Ø´Ù‡Ø± Ù…Ù†",
        "Ø´Ù‡Ø± Ù…Ø§",
        "Ø¯Ø± Ø´Ù‡Ø± Ù…Ù†",
        "Ø¢Ù†ÛŒ Ú©Ø§Ø± Ø¯Ø± Ø´Ù‡Ø± Ù…Ù†",
        "Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± Ø¯Ø± Ø´Ù‡Ø± Ù…Ù†",
        "Ù¾ÙˆØ´Ø´ Ø´Ù‡Ø±",
        "Ù…Ø­Ø¯ÙˆØ¯Ù‡ ÙØ¹Ø§Ù„ÛŒØª",
        "Ù…Ù†Ø·Ù‚Ù‡ Ù…Ø§",
        "Ù…Ø­Ù„Ù‡ Ù…Ø§",
        "Ø®Ø¯Ù…Ø§Øª Ø¯Ø± Ø´Ù‡Ø± Ù…Ù†"
    ]):

        return (
            "ðŸ“ Ù…Ø­Ø¯ÙˆØ¯Ù‡ Ø®Ø¯Ù…Ø§Øª Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±\n\n"
            "Ù¾ÙˆØ´Ø´ Ø®Ø¯Ù…Ø§Øª Ø¨Ù‡ Ø´Ù‡Ø± Ùˆ Ù†ÙˆØ¹ Ø®Ø¯Ù…Øª Ø¨Ø³ØªÚ¯ÛŒ Ø¯Ø§Ø±Ù‡. "
            "Ø¨Ø±Ø§ÛŒ Ø¨Ø±Ø±Ø³ÛŒ Ø§Ù…Ú©Ø§Ù† Ø«Ø¨Øª Ø®Ø¯Ù…Øª Ø¯Ø± Ù…Ø­Ø¯ÙˆØ¯Ù‡â€ŒØªÙˆÙ†ØŒ "
            "Ø§Ø² Ø¨Ø®Ø´ Ø«Ø¨Øª Ø³ÙØ§Ø±Ø´ Ø´Ø±ÙˆØ¹ Ú©Ù†ÛŒØ¯."
        ), inline_button(
            "ðŸ“ Ø«Ø¨Øª Ø³ÙØ§Ø±Ø´",
            ORDER_URL
        )

    # Ø´Ù…Ø§Ø±Ù‡ Ù¾Ø´ØªÛŒØ¨Ø§Ù†ÛŒ
    if contains_any(text, [
        "Ø´Ù…Ø§Ø±Ù‡ Ù¾Ø´ØªÛŒØ¨Ø§Ù†ÛŒ",
        "Ø´Ù…Ø§Ø±Ù‡ ØªÙ…Ø§Ø³",
        "ØªÙ„ÙÙ† Ù¾Ø´ØªÛŒØ¨Ø§Ù†ÛŒ",
        "Ø´Ù…Ø§Ø±Ù‡ ØªÙ„ÙÙ†",
        "Ú†Ø·ÙˆØ± ØªÙ…Ø§Ø³ Ø¨Ú¯ÛŒØ±Ù…",
        "Ø¨Ø§ Ù¾Ø´ØªÛŒØ¨Ø§Ù†ÛŒ ØªÙ…Ø§Ø³",
        "Ù¾Ø´ØªÛŒØ¨Ø§Ù†ÛŒ Ú©Ø¬Ø§Ø³Øª",
        "Ø±Ø§Ù‡ Ø§Ø±ØªØ¨Ø§Ø·ÛŒ",
        "ØªÙ…Ø§Ø³ Ø¨Ø§ Ø¢Ù†ÛŒ Ú©Ø§Ø±",
        "ØªÙ…Ø§Ø³ Ø¨Ø§ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±",
        "Ø§Ø±ØªØ¨Ø§Ø· Ø¨Ø§ Ù¾Ø´ØªÛŒØ¨Ø§Ù†ÛŒ",
        "Ù¾Ø´ØªÛŒØ¨Ø§Ù†",
        "Ø§Ù¾Ø±Ø§ØªÙˆØ±"
    ]):

        return (
            "ðŸŽ§ Ù¾Ø´ØªÛŒØ¨Ø§Ù†ÛŒ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±\n\n"
            "Ø§Ú¯Ø± Ø¯Ø±Ø¨Ø§Ø±Ù‡ Ø³ÙØ§Ø±Ø´ ÛŒØ§ Ø§Ø³ØªÙØ§Ø¯Ù‡ Ø§Ø² "
            "Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± Ù…Ø´Ú©Ù„ÛŒ Ø¯Ø§Ø±ÛŒØ¯ØŒ Ù…ÙˆØ¶ÙˆØ¹ Ø±Ùˆ Ù‡Ù…ÛŒÙ†Ø¬Ø§ "
            "Ø¨Ø§ Ø¬Ø²Ø¦ÛŒØ§Øª Ø¨Ù†ÙˆÛŒØ³ÛŒØ¯ ØªØ§ Ø±Ø§Ù‡Ù†Ù…Ø§ÛŒÛŒâ€ŒØªÙˆÙ† Ú©Ù†Ù…."
        ), None

    # Ø§Ù¾Ù„ÛŒÚ©ÛŒØ´Ù†
    if contains_any(text, [
        "Ø§Ù¾Ù„ÛŒÚ©ÛŒØ´Ù†",
        "Ø§Ù¾ Ø¢Ù†ÛŒ Ú©Ø§Ø±",
        "Ø§Ù¾ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±",
        "Ø¨Ø±Ù†Ø§Ù…Ù‡ Ø¢Ù†ÛŒ Ú©Ø§Ø±",
        "Ø¨Ø±Ù†Ø§Ù…Ù‡ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±",
        "Ù†Ø±Ù… Ø§ÙØ²Ø§Ø±",
        "Ù†Ø±Ù…â€ŒØ§ÙØ²Ø§Ø±",
        "Ø³Ø§ÛŒØª Ø¢Ù†ÛŒ Ú©Ø§Ø±",
        "Ø³Ø§ÛŒØª Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±",
        "Ø¢Ø¯Ø±Ø³ Ø³Ø§ÛŒØª",
        "Ø¢Ø¯Ø±Ø³ Ø¢Ù†ÛŒ Ú©Ø§Ø±",
        "Ø¢Ø¯Ø±Ø³ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±",
        "Ù„ÛŒÙ†Ú© Ø¢Ù†ÛŒ Ú©Ø§Ø±",
        "Ù„ÛŒÙ†Ú© Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±"
    ]):

        return (
            "ðŸŒ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±\n\n"
            "Ø¨Ø±Ø§ÛŒ Ø§Ø³ØªÙØ§Ø¯Ù‡ Ø§Ø² Ø®Ø¯Ù…Ø§Øª Ùˆ Ø«Ø¨Øª Ø¯Ø±Ø®ÙˆØ§Ø³ØªØŒ "
            "ÙˆØ§Ø±Ø¯ Ø³Ø§ÛŒØª Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± Ø¨Ø´ÛŒØ¯."
        ), inline_button(
            "ðŸŒ ÙˆØ±ÙˆØ¯ Ø¨Ù‡ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±",
            SITE_URL
        )

    # Ø«Ø¨Øª Ù†Ø§Ù… Ù…Ø´ØªØ±ÛŒ
    if contains_any(text, [
        "Ø«Ø¨Øª Ù†Ø§Ù… Ù…Ø´ØªØ±ÛŒ",
        "Ø«Ø¨Øªâ€ŒÙ†Ø§Ù… Ù…Ø´ØªØ±ÛŒ",
        "Ø¹Ø¶ÙˆÛŒØª Ù…Ø´ØªØ±ÛŒ",
        "Ú†Ø·ÙˆØ± Ø«Ø¨Øª Ù†Ø§Ù… Ú©Ù†Ù…",
        "Ú†Ú¯ÙˆÙ†Ù‡ Ø«Ø¨Øª Ù†Ø§Ù… Ú©Ù†Ù…",
        "Ø«Ø¨Øª Ù†Ø§Ù… Ø¯Ø± Ø³Ø§ÛŒØª",
        "Ø³Ø§Ø®Øª Ø­Ø³Ø§Ø¨",
        "Ø³Ø§Ø®Øª Ø§Ú©Ø§Ù†Øª",
        "Ø§Ú©Ø§Ù†Øª Ø¨Ø³Ø§Ø²Ù…",
        "Ø­Ø³Ø§Ø¨ Ú©Ø§Ø±Ø¨Ø±ÛŒ",
        "Ø¹Ø¶ÙˆÛŒØª Ø¯Ø± Ø¢Ù†ÛŒ Ú©Ø§Ø±",
        "Ø¹Ø¶ÙˆÛŒØª Ø¯Ø± Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±"
    ]):

        return (
            "ðŸ‘¤ Ø«Ø¨Øªâ€ŒÙ†Ø§Ù… Ùˆ Ø§Ø³ØªÙØ§Ø¯Ù‡ Ø§Ø² Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±\n\n"
            "Ø¨Ø±Ø§ÛŒ Ø´Ø±ÙˆØ¹ Ø§Ø³ØªÙØ§Ø¯Ù‡ Ø§Ø² Ø®Ø¯Ù…Ø§ØªØŒ ÙˆØ§Ø±Ø¯ "
            "Ø³Ø§ÛŒØª Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± Ø¨Ø´ÛŒØ¯ Ùˆ Ù…Ø±Ø§Ø­Ù„ Ø«Ø¨Øª Ø¯Ø±Ø®ÙˆØ§Ø³Øª "
            "ÛŒØ§ Ø§ÛŒØ¬Ø§Ø¯ Ø­Ø³Ø§Ø¨ Ú©Ø§Ø±Ø¨Ø±ÛŒ Ø±Ùˆ Ø§Ù†Ø¬Ø§Ù… Ø¨Ø¯ÛŒØ¯."
        ), inline_button(
            "ðŸŒ ÙˆØ±ÙˆØ¯ Ø¨Ù‡ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±",
            SITE_URL
        )

    # Ú©Ø¯ ØªØ§ÛŒÛŒØ¯
    if contains_any(text, [
        "Ú©Ø¯ ØªØ§ÛŒÛŒØ¯",
        "Ú©Ø¯ ØªØ£ÛŒÛŒØ¯",
        "Ú©Ø¯ ÙˆØ±ÙˆØ¯",
        "Ú©Ø¯ Ù†Ù…ÛŒØ§Ø¯",
        "Ø§Ø³ Ø§Ù… Ø§Ø³ Ù†Ù…ÛŒØ§Ø¯",
        "Ù¾ÛŒØ§Ù…Ú© Ù†Ù…ÛŒØ§Ø¯",
        "Ù¾ÛŒØ§Ù…Ú© Ù†ÛŒØ§Ù…Ø¯Ù‡",
        "ÙˆØ§Ø±Ø¯ Ù†Ù…ÛŒØ´Ù…",
        "ÙˆØ§Ø±Ø¯ Ù†Ù…ÛŒ Ø´Ù…",
        "ÙˆØ±ÙˆØ¯ Ù†Ù…ÛŒØ´Ù‡",
        "Ø±Ù…Ø² Ø¹Ø¨ÙˆØ±",
        "Ù…Ø´Ú©Ù„ ÙˆØ±ÙˆØ¯"
    ]):

        return (
            "ðŸ” Ù…Ø´Ú©Ù„ ÙˆØ±ÙˆØ¯\n\n"
            "Ø§Ú¯Ø± Ú©Ø¯ ÙˆØ±ÙˆØ¯ ÛŒØ§ Ù¾ÛŒØ§Ù…Ú© ØªØ£ÛŒÛŒØ¯ Ø¯Ø±ÛŒØ§ÙØª "
            "Ù†Ù…ÛŒâ€ŒÚ©Ù†ÛŒØ¯ØŒ Ø´Ù…Ø§Ø±Ù‡ Ù…ÙˆØ¨Ø§ÛŒÙ„ Ùˆ Ø§ØªØµØ§Ù„ Ø´Ø¨Ú©Ù‡ "
            "Ø±Ùˆ Ø¨Ø±Ø±Ø³ÛŒ Ú©Ù†ÛŒØ¯ Ùˆ Ø¯Ø± ØµÙˆØ±Øª Ø§Ø¯Ø§Ù…Ù‡ Ù…Ø´Ú©Ù„ØŒ "
            "Ù…ÙˆØ¶ÙˆØ¹ Ø±Ùˆ Ø¨Ø§ Ù¾Ø´ØªÛŒØ¨Ø§Ù†ÛŒ Ø¯Ø± Ù…ÛŒØ§Ù† Ø¨Ø°Ø§Ø±ÛŒØ¯."
        ), None

    # Ù¾Ø±Ø¯Ø§Ø®Øª Ø¢Ù†Ù„Ø§ÛŒÙ†
    if contains_any(text, [
        "Ù¾Ø±Ø¯Ø§Ø®Øª Ø¢Ù†Ù„Ø§ÛŒÙ†",
        "Ù¾Ø±Ø¯Ø§Ø®Øª Ø§ÛŒÙ†ØªØ±Ù†ØªÛŒ",
        "Ø¯Ø±Ú¯Ø§Ù‡ Ù¾Ø±Ø¯Ø§Ø®Øª",
        "Ú†Ø·ÙˆØ± Ù¾Ø±Ø¯Ø§Ø®Øª Ú©Ù†Ù…",
        "Ú†Ú¯ÙˆÙ†Ù‡ Ù¾Ø±Ø¯Ø§Ø®Øª Ú©Ù†Ù…",
        "Ù¾Ø±Ø¯Ø§Ø®Øª Ø§Ø² Ø³Ø§ÛŒØª",
        "Ù¾Ø±Ø¯Ø§Ø®Øª Ø§Ø² Ø·Ø±ÛŒÙ‚ Ø³Ø§ÛŒØª",
        "Ú©Ø§Ø±Øª Ø¨Ù‡ Ú©Ø§Ø±Øª",
        "Ú©Ø§Ø±Øªâ€ŒØ¨Ù‡â€ŒÚ©Ø§Ø±Øª",
        "Ù†Ù‚Ø¯ÛŒ Ø¨Ù‡ Ù…ØªØ®ØµØµ",
        "Ù†Ù‚Ø¯ÛŒ",
        "Ù¾ÙˆÙ„ Ù†Ù‚Ø¯",
        "Ù¾Ø±Ø¯Ø§Ø®Øª Ù…Ø³ØªÙ‚ÛŒÙ…"
    ]):

        return (
            "ðŸ’³ Ù¾Ø±Ø¯Ø§Ø®Øª Ø¯Ø± Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±\n\n"
            "Ø¨Ø±Ø§ÛŒ Ø§Ø³ØªÙØ§Ø¯Ù‡ Ø§Ø² ÙØ±Ø¢ÛŒÙ†Ø¯ Ø¶Ù…Ø§Ù†Øª Ùˆ Ù¾ÛŒÚ¯ÛŒØ±ÛŒØŒ "
            "Ù¾Ø±Ø¯Ø§Ø®Øª Ø¨Ø§ÛŒØ¯ Ø§Ø² Ø·Ø±ÛŒÙ‚ Ø¯Ø±Ú¯Ø§Ù‡ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± Ø§Ù†Ø¬Ø§Ù… Ø¨Ø´Ù‡.\n\n"
            "Ù¾Ø±Ø¯Ø§Ø®Øª Ù…Ø³ØªÙ‚ÛŒÙ… Ø®Ø§Ø±Ø¬ Ø§Ø² ÙØ±Ø¢ÛŒÙ†Ø¯ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± Ù…Ù…Ú©Ù†Ù‡ "
            "Ø¨Ø§Ø¹Ø« Ø§Ø² Ø¨ÛŒÙ† Ø±ÙØªÙ† Ø§Ù…Ú©Ø§Ù† Ù¾ÛŒÚ¯ÛŒØ±ÛŒ Ùˆ Ø¶Ù…Ø§Ù†Øª "
            "Ù¾Ù„ØªÙØ±Ù… Ø¨Ø´Ù‡."
        ), inline_button(
            "ðŸ“œ Ù‚ÙˆØ§Ù†ÛŒÙ† Ù…Ø´ØªØ±ÛŒ",
            CUSTOMER_RULES_URL
        )

    # Ø¨Ø±Ú¯Ø´Øª Ù¾ÙˆÙ„
    if contains_any(text, [
        "Ø¨Ø±Ú¯Ø´Øª Ù¾ÙˆÙ„",
        "Ù¾Ø³ Ú¯Ø±ÙØªÙ† Ù¾ÙˆÙ„",
        "Ø§Ø³ØªØ±Ø¯Ø§Ø¯ ÙˆØ¬Ù‡",
        "Ø¹ÙˆØ¯Øª ÙˆØ¬Ù‡",
        "Ù¾ÙˆÙ„Ù… Ø¨Ø±Ù…ÛŒÚ¯Ø±Ø¯Ù‡",
        "Ù¾ÙˆÙ„Ù… Ø¨Ø±Ù…ÛŒâ€ŒÚ¯Ø±Ø¯Ù‡",
        "Ø¨Ø§Ø²Ú¯Ø´Øª ÙˆØ¬Ù‡",
        "Ù„ØºÙˆ Ù¾Ø±Ø¯Ø§Ø®Øª",
        "Ù¾Ø±Ø¯Ø§Ø®Øª Ø§Ø´ØªØ¨Ø§Ù‡",
        "Ø¯Ùˆ Ø¨Ø§Ø± Ù¾Ø±Ø¯Ø§Ø®Øª Ú©Ø±Ø¯Ù…"
    ]):

        return (
            "ðŸ’³ Ù¾ÛŒÚ¯ÛŒØ±ÛŒ Ù¾Ø±Ø¯Ø§Ø®Øª\n\n"
            "Ø§Ú¯Ø± Ø¯Ø±Ø¨Ø§Ø±Ù‡ ÛŒÚ© Ù¾Ø±Ø¯Ø§Ø®Øª ÛŒØ§ Ø¨Ø§Ø²Ú¯Ø´Øª ÙˆØ¬Ù‡ "
            "Ù…Ø´Ú©Ù„ Ø¯Ø§Ø±ÛŒØ¯ØŒ Ø§Ø·Ù„Ø§Ø¹Ø§Øª Ø³ÙØ§Ø±Ø´ Ùˆ Ù¾Ø±Ø¯Ø§Ø®Øª "
            "Ø±Ùˆ Ù†Ú¯Ù‡ Ø¯Ø§Ø±ÛŒØ¯ Ùˆ Ù…ÙˆØ¶ÙˆØ¹ Ø±Ùˆ Ø§Ø² Ø·Ø±ÛŒÙ‚ "
            "Ù¾Ø´ØªÛŒØ¨Ø§Ù†ÛŒ Ù¾ÛŒÚ¯ÛŒØ±ÛŒ Ú©Ù†ÛŒØ¯."
        ), None

    # ØªØ³ÙˆÛŒÙ‡
    if contains_any(text, [
        "Ú†Ø±Ø§ 72 Ø³Ø§Ø¹Øª",
        "Ú†Ø±Ø§ Û·Û² Ø³Ø§Ø¹Øª",
        "Ø³Ù‡ Ø±ÙˆØ² Ù¾ÙˆÙ„",
        "Ø³Ù‡ Ø±ÙˆØ² Ø¨Ù„ÙˆÚ©Ù‡",
        "Ù¾ÙˆÙ„ Ú†Ù†Ø¯ Ø±ÙˆØ² Ø¨Ù„ÙˆÚ©Ù‡",
        "Ú†Ù‡ Ø²Ù…Ø§Ù†ÛŒ Ù¾ÙˆÙ„ Ù…ØªØ®ØµØµ",
        "Ù¾ÙˆÙ„ Ù…ØªØ®ØµØµ Ú©ÛŒ Ø¢Ø²Ø§Ø¯",
        "Ù¾ÙˆÙ„ Ù…ØªØ®ØµØµ Ú†Ù‡ Ø²Ù…Ø§Ù†ÛŒ",
        "ØªØ³ÙˆÛŒÙ‡ Ù…ØªØ®ØµØµ",
        "ØªØ³ÙˆÛŒÙ‡ Ø­Ø³Ø§Ø¨ Ù…ØªØ®ØµØµ",
        "Ø²Ù…Ø§Ù† ØªØ³ÙˆÛŒÙ‡"
    ]):

        return (
            "ðŸ›¡ï¸ Ø²Ù…Ø§Ù† ØªØ³ÙˆÛŒÙ‡\n\n"
            "Ù…Ø¨Ù„Øº Ù¾Ø±Ø¯Ø§Ø®ØªÛŒ Ø¨Ø±Ø§ÛŒ Ù…Ø¯Øª ØªØ¹ÛŒÛŒÙ†â€ŒØ´Ø¯Ù‡ "
            "Ø¯Ø± ÙØ±Ø¢ÛŒÙ†Ø¯ Ø¶Ù…Ø§Ù†Øª Ù†Ú¯Ù‡Ø¯Ø§Ø±ÛŒ Ù…ÛŒâ€ŒØ´Ù‡ ØªØ§ "
            "Ø§Ù…Ú©Ø§Ù† Ù¾ÛŒÚ¯ÛŒØ±ÛŒ Ù…Ø´Ú©Ù„Ø§Øª Ø§Ø­ØªÙ…Ø§Ù„ÛŒ Ø³ÙØ§Ø±Ø´ "
            "ÙˆØ¬ÙˆØ¯ Ø¯Ø§Ø´ØªÙ‡ Ø¨Ø§Ø´Ù‡.\n\n"
            "Ø¬Ø²Ø¦ÛŒØ§Øª Ú©Ø§Ù…Ù„ Ø¯Ø± Ù‚ÙˆØ§Ù†ÛŒÙ† Ù…Ø´ØªØ±ÛŒ Ùˆ "
            "Ù…ØªØ®ØµØµÛŒÙ† Ù‚Ø§Ø¨Ù„ Ù…Ø´Ø§Ù‡Ø¯Ù‡ Ø§Ø³Øª."
        ), inline_button(
            "ðŸ“œ Ù‚ÙˆØ§Ù†ÛŒÙ† Ù…Ø´ØªØ±ÛŒ",
            CUSTOMER_RULES_URL
        )

    # Ù…ØªØ®ØµØµ Ù†ÛŒØ§Ù…Ø¯
    if contains_any(text, [
        "Ø§Ú¯Ø± Ù…ØªØ®ØµØµ Ù†ÛŒØ§Ø¯",
        "Ù…ØªØ®ØµØµ Ù†ÛŒØ§Ù…Ø¯",
        "Ù…ØªØ®ØµØµ Ù†ÛŒÙˆÙ…Ø¯",
        "Ù…ØªØ®ØµØµ Ø­Ø§Ø¶Ø± Ù†Ø´Ø¯",
        "Ù…ØªØ®ØµØµ Ú©Ù†Ø³Ù„ Ú©Ø±Ø¯",
        "Ú©Ø§Ø± Ø§Ù†Ø¬Ø§Ù… Ù†Ø´Ø¯",
        "Ú©Ø§Ø± Ø§Ù†Ø¬Ø§Ù… Ù†Ø´Ø¯Ù‡",
        "Ú©Ø§Ø± Ù†Ø§Ù‚Øµ",
        "Ú©Ø§Ø± Ú©Ø§Ù…Ù„ Ù†Ø´Ø¯Ù‡"
    ]):

        return (
            "ðŸ›¡ï¸ Ù…Ø´Ú©Ù„ Ø¯Ø± Ø§Ù†Ø¬Ø§Ù… Ø³ÙØ§Ø±Ø´\n\n"
            "Ø§Ú¯Ø± Ù…ØªØ®ØµØµ Ø¨Ø±Ø§ÛŒ Ø³ÙØ§Ø±Ø´ Ø­Ø§Ø¶Ø± Ù†Ø´Ø¯ ÛŒØ§ "
            "Ú©Ø§Ø± Ø·Ø¨Ù‚ Ø§Ù†ØªØ¸Ø§Ø± Ø§Ù†Ø¬Ø§Ù… Ù†Ø´Ø¯ØŒ Ø§Ø·Ù„Ø§Ø¹Ø§Øª "
            "Ø³ÙØ§Ø±Ø´ Ø±Ùˆ Ù†Ú¯Ù‡ Ø¯Ø§Ø±ÛŒØ¯ Ùˆ Ù…ÙˆØ¶ÙˆØ¹ Ø±Ùˆ Ø§Ø² "
            "Ø·Ø±ÛŒÙ‚ Ù¾Ø´ØªÛŒØ¨Ø§Ù†ÛŒ Ù¾ÛŒÚ¯ÛŒØ±ÛŒ Ú©Ù†ÛŒØ¯."
        ), None

    # Ø®Ø³Ø§Ø±Øª
    if contains_any(text, [
        "Ø®Ø³Ø§Ø±Øª",
        "Ø®Ø³Ø§Ø±Øª Ø¨Ù‡ ÙˆØ³Ø§ÛŒÙ„",
        "ÙˆØ³ÛŒÙ„Ù‡ Ø®Ø±Ø§Ø¨ Ø´Ø¯",
        "ÙˆØ³ÛŒÙ„Ù‡ Ù…Ù† Ø®Ø±Ø§Ø¨ Ø´Ø¯",
        "Ø¨Ù‡ ÙˆØ³Ø§ÛŒÙ„Ù… Ø¢Ø³ÛŒØ¨ Ø²Ø¯",
        "Ø¢Ø³ÛŒØ¨ Ø¨Ù‡ ÙˆØ³Ø§ÛŒÙ„",
        "Ú¯Ù… Ø´Ø¯Ù† ÙˆØ³ÛŒÙ„Ù‡",
        "ÙˆØ³Ø§ÛŒÙ„ Ú¯Ù… Ø´Ø¯",
        "Ø³Ø±Ù‚Øª",
        "Ø§Ù…ÙˆØ§Ù„",
        "ÙˆØ³Ø§ÛŒÙ„ Ø®Ø§Ù†Ù‡",
        "Ù…Ø³Ø¦ÙˆÙ„ÛŒØª ÙˆØ³Ø§ÛŒÙ„",
        "Ù…Ø³Ø¦ÙˆÙ„ ÙˆØ³Ø§ÛŒÙ„"
    ]):

        return (
            "âš ï¸ Ø¯Ø±Ø¨Ø§Ø±Ù‡ Ù…Ø³Ø¦ÙˆÙ„ÛŒØª Ø§Ù…ÙˆØ§Ù„\n\n"
            "Ø´Ø±Ø§ÛŒØ· Ùˆ Ù…Ø³Ø¦ÙˆÙ„ÛŒØªâ€ŒÙ‡Ø§ÛŒ Ù…Ø±Ø¨ÙˆØ· Ø¨Ù‡ Ø§Ù…ÙˆØ§Ù„ "
            "Ùˆ Ø§Ù†Ø¬Ø§Ù… Ú©Ø§Ø± Ø±Ùˆ Ù…Ø·Ø§Ø¨Ù‚ Ù‚ÙˆØ§Ù†ÛŒÙ† Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± "
            "Ø¯Ø± Ù†Ø¸Ø± Ø¨Ú¯ÛŒØ±ÛŒØ¯.\n\n"
            "Ø¨Ø±Ø§ÛŒ Ù…ÙˆØ¶ÙˆØ¹Ø§Øª Ø®Ø³Ø§Ø±Øª ÛŒØ§ Ø§Ø®ØªÙ„Ø§ÙØŒ Ø³ÙØ§Ø±Ø´ "
            "Ùˆ Ù…Ø³ØªÙ†Ø¯Ø§Øª Ù…Ø±Ø¨ÙˆØ· Ø±Ùˆ Ù†Ú¯Ù‡ Ø¯Ø§Ø±ÛŒØ¯ Ùˆ Ø¨Ø§ "
            "Ù¾Ø´ØªÛŒØ¨Ø§Ù†ÛŒ Ù¾ÛŒÚ¯ÛŒØ±ÛŒ Ú©Ù†ÛŒØ¯."
        ), inline_button(
            "ðŸ“œ Ù‚ÙˆØ§Ù†ÛŒÙ† Ù…Ø´ØªØ±ÛŒ",
            CUSTOMER_RULES_URL
        )

    # Ù…Ø¯Ø§Ø±Ú© Ù…ØªØ®ØµØµ
    if contains_any(text, [
        "Ù…Ø¯Ø§Ø±Ú© Ù…ØªØ®ØµØµ",
        "Ú†Ù‡ Ù…Ø¯Ø§Ø±Ú©ÛŒ Ø¨Ø±Ø§ÛŒ Ù…ØªØ®ØµØµ",
        "Ù…Ø¯Ø±Ú© Ø«Ø¨Øª Ù†Ø§Ù… Ù…ØªØ®ØµØµ",
        "Ù…Ø¯Ø§Ø±Ú© Ø«Ø¨Øª Ù†Ø§Ù…",
        "Ø§Ø­Ø±Ø§Ø² Ù‡ÙˆÛŒØª Ù…ØªØ®ØµØµ",
        "Ø§Ø­Ø±Ø§Ø² Ù‡ÙˆÛŒØª",
        "ØªØ§ÛŒÛŒØ¯ Ù…ØªØ®ØµØµ",
        "ØªØ£ÛŒÛŒØ¯ Ù…ØªØ®ØµØµ",
        "ØªØ§ÛŒÛŒØ¯ Ù…Ø¯Ø§Ø±Ú©",
        "ØªØ£ÛŒÛŒØ¯ Ù…Ø¯Ø§Ø±Ú©",
        "Ø³ÙˆØ¡ Ù¾ÛŒØ´ÛŒÙ†Ù‡",
        "Ø¹Ø¯Ù… Ø³ÙˆØ¡ Ù¾ÛŒØ´ÛŒÙ†Ù‡",
        "Ú¯ÙˆØ§Ù‡ÛŒ Ø³ÙˆØ¡ Ù¾ÛŒØ´ÛŒÙ†Ù‡"
    ]):

        return (
            "ðŸ‘¨â€ðŸ”§ Ø«Ø¨Øªâ€ŒÙ†Ø§Ù… Ù…ØªØ®ØµØµ\n\n"
            "Ø´Ø±Ø§ÛŒØ· Ùˆ Ù…Ø¯Ø§Ø±Ú© Ù…ÙˆØ±Ø¯Ù†ÛŒØ§Ø² Ù‡Ù…Ú©Ø§Ø±ÛŒ "
            "Ù…ØªØ®ØµØµÛŒÙ† Ø¯Ø± ÙØ±Ø¢ÛŒÙ†Ø¯ Ø«Ø¨Øªâ€ŒÙ†Ø§Ù… Ùˆ Ù‚ÙˆØ§Ù†ÛŒÙ† "
            "Ù…ØªØ®ØµØµÛŒÙ† Ø§Ø¹Ù„Ø§Ù… Ù…ÛŒâ€ŒØ´Ù‡."
        ), inline_button(
            "ðŸš€ Ø«Ø¨Øªâ€ŒÙ†Ø§Ù… Ù…ØªØ®ØµØµ",
            SPECIALIST_URL
        )

    # Ø¯Ø±Ø¢Ù…Ø¯ Ù…ØªØ®ØµØµ
    if contains_any(text, [
        "Ø¯Ø±Ø¢Ù…Ø¯ Ù…ØªØ®ØµØµ",
        "Ø¯Ø±Ø¢Ù…Ø¯ Ø§Ø³ØªØ§Ø¯Ú©Ø§Ø±",
        "Ú†Ù‚Ø¯Ø± Ø¯Ø±Ø¢Ù…Ø¯ Ø¯Ø§Ø±Ù…",
        "Ú†Ù‚Ø¯Ø± Ù¾ÙˆÙ„ Ø¯Ø±Ù…ÛŒØ§Ø±Ù…",
        "Ú©Ø§Ø± Ø¨Ø±Ø§ÛŒ Ù…ØªØ®ØµØµ",
        "Ø³ÙØ§Ø±Ø´ Ø¨Ø±Ø§ÛŒ Ù…ØªØ®ØµØµ",
        "Ø³ÙØ§Ø±Ø´ Ù…ÛŒØ§Ø¯",
        "Ú†Ø·ÙˆØ± Ø³ÙØ§Ø±Ø´ Ø¨Ú¯ÛŒØ±Ù…",
        "Ú†Ø·ÙˆØ± Ù…Ø´ØªØ±ÛŒ Ø¨Ú¯ÛŒØ±Ù…",
        "Ù…Ø´ØªØ±ÛŒ Ø¨Ø±Ø§ÛŒ Ù…ØªØ®ØµØµ"
    ]):

        return (
            "ðŸ‘¨â€ðŸ”§ Ù‡Ù…Ú©Ø§Ø±ÛŒ Ø¨Ù‡â€ŒØ¹Ù†ÙˆØ§Ù† Ù…ØªØ®ØµØµ\n\n"
            "Ù…ØªØ®ØµØµÛŒÙ† Ù¾Ø³ Ø§Ø² Ø«Ø¨Øªâ€ŒÙ†Ø§Ù… Ùˆ ØªØ£ÛŒÛŒØ¯ "
            "Ø´Ø±Ø§ÛŒØ· Ù‡Ù…Ú©Ø§Ø±ÛŒ Ù…ÛŒâ€ŒØªÙˆÙ†Ù† Ø¯Ø±Ø®ÙˆØ§Ø³Øªâ€ŒÙ‡Ø§ÛŒ "
            "Ù…Ø±ØªØ¨Ø· Ø¨Ø§ Ø­ÙˆØ²Ù‡ ÙØ¹Ø§Ù„ÛŒØª Ø®ÙˆØ¯Ø´ÙˆÙ† Ø±Ùˆ "
            "Ø¯Ø±ÛŒØ§ÙØª Ùˆ Ø¨Ø±Ø±Ø³ÛŒ Ú©Ù†Ù†."
        ), inline_button(
            "ðŸ“‹ Ù‚ÙˆØ§Ù†ÛŒÙ† Ù…ØªØ®ØµØµÛŒÙ†",
            SPECIALIST_RULES_URL
        )

    # Ú©ÛŒÙ Ù¾ÙˆÙ„
    if contains_any(text, [
        "Ú©ÛŒÙ Ù¾ÙˆÙ„ Ù…ØªØ®ØµØµ",
        "Ú©ÛŒÙ Ù¾ÙˆÙ„",
        "Ø´Ø§Ø±Ú˜ Ú©ÛŒÙ Ù¾ÙˆÙ„",
        "Ø§Ø¹ØªØ¨Ø§Ø± Ú©ÛŒÙ Ù¾ÙˆÙ„",
        "Ø¨Ø±Ø¯Ø§Ø´Øª Ø§Ø² Ú©ÛŒÙ Ù¾ÙˆÙ„",
        "Ø¨Ø±Ø¯Ø§Ø´Øª Ù¾ÙˆÙ„",
        "Ù…ÙˆØ¬ÙˆØ¯ÛŒ Ù…ØªØ®ØµØµ",
        "Ø´Ø§Ø±Ú˜ Ø­Ø³Ø§Ø¨ Ù…ØªØ®ØµØµ",
        "Ù‡Ø²ÛŒÙ†Ù‡ Ù‡Ù…Ú©Ø§Ø±ÛŒ",
        "Ù‡Ø²ÛŒÙ†Ù‡ Ù…ØªØ®ØµØµ",
        "Ø¯Ø±ØµØ¯ Ø§Ø² Ú©Ø§Ø±",
        "Ú†Ù†Ø¯ Ø¯Ø±ØµØ¯ Ø§Ø² Ú©Ø§Ø±",
        "Ú©Ø³Ø± Ø§Ø² Ù…Ø¨Ù„Øº"
    ]):

        return (
            "ðŸ’³ Ø´Ø±Ø§ÛŒØ· Ù…Ø§Ù„ÛŒ Ù…ØªØ®ØµØµÛŒÙ†\n\n"
            "Ø¯Ø±ØµØ¯ Ú©Ù…ÛŒØ³ÛŒÙˆÙ† Ùˆ Ø³Ø§ÛŒØ± Ø´Ø±Ø§ÛŒØ· Ù…Ø§Ù„ÛŒ "
            "Ø·Ø¨Ù‚ Ù‚ÙˆØ§Ù†ÛŒÙ† Ùˆ Ø´Ø±Ø§ÛŒØ· Ù‡Ù…Ú©Ø§Ø±ÛŒ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± "
            "ØªØ¹ÛŒÛŒÙ† Ù…ÛŒâ€ŒØ´Ù‡."
        ), inline_button(
            "ðŸ“‹ Ù‚ÙˆØ§Ù†ÛŒÙ† Ù…ØªØ®ØµØµÛŒÙ†",
            SPECIALIST_RULES_URL
        )

    # Ø¨Ø±Ù‚
    if contains_any(text, [
        "Ù„Ø§Ù…Ù¾",
        "ØªØ¹ÙˆÛŒØ¶ Ù„Ø§Ù…Ù¾",
        "Ú©Ù„ÛŒØ¯ Ø¨Ø±Ù‚",
        "Ù¾Ø±ÛŒØ²",
        "Ù¾Ø±ÛŒØ² Ø¨Ø±Ù‚",
        "ÙÛŒÙˆØ²",
        "Ø¬Ø¹Ø¨Ù‡ ÙÛŒÙˆØ²",
        "Ø¨Ø±Ù‚ Ù‚Ø·Ø¹",
        "Ø¨Ø±Ù‚ Ù¾Ø±ÛŒØ¯Ù‡",
        "Ø§ØªØµØ§Ù„ Ø¨Ø±Ù‚",
        "Ø§ØªØµØ§Ù„ Ú©ÙˆØªØ§Ù‡",
        "Ø³ÛŒÙ… Ø¨Ø±Ù‚",
        "Ø³ÛŒÙ… Ú©Ø´ÛŒ Ø³Ø§Ø®ØªÙ…Ø§Ù†",
        "Ø±ÙˆØ´Ù†Ø§ÛŒÛŒ",
        "Ú†Ø±Ø§Øº",
        "Ù„ÙˆØ³ØªØ±",
        "Ø¢ÛŒÙÙˆÙ†",
        "Ø¢ÛŒÙÙˆÙ† ØªØµÙˆÛŒØ±ÛŒ"
    ]):

        return (
            "âš¡ Ø®Ø¯Ù…Ø§Øª Ø¨Ø±Ù‚Ú©Ø§Ø±ÛŒ\n\n"
            "Ø¨Ø±Ø§ÛŒ Ù†ØµØ¨ ÛŒØ§ ØªØ¹ÙˆÛŒØ¶ Ú©Ù„ÛŒØ¯ Ùˆ Ù¾Ø±ÛŒØ²ØŒ "
            "Ø±ÙˆØ´Ù†Ø§ÛŒÛŒØŒ Ø³ÛŒÙ…â€ŒÚ©Ø´ÛŒØŒ Ø±ÙØ¹ Ù…Ø´Ú©Ù„Ø§Øª Ø¨Ø±Ù‚ "
            "Ùˆ Ù…ÙˆØ§Ø±Ø¯ Ù…Ø´Ø§Ø¨Ù‡ Ù…ÛŒâ€ŒØªÙˆÙ†ÛŒØ¯ Ø¯Ø±Ø®ÙˆØ§Ø³Øª "
            "Ø¨Ø±Ù‚Ú©Ø§Ø± Ø«Ø¨Øª Ú©Ù†ÛŒØ¯."
        ), inline_button(
            "âš¡ Ø«Ø¨Øª Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ø¨Ø±Ù‚Ú©Ø§Ø±",
            ORDER_URL
        )

    # Ù„ÙˆÙ„Ù‡
    if contains_any(text, [
        "Ø´ÛŒØ± Ø¢Ø¨",
        "Ø´ÛŒØ±Ø¢Ø¨",
        "Ø´ÛŒØ± Ø¸Ø±ÙØ´ÙˆÛŒÛŒ",
        "Ø´ÛŒØ± Ø³ÛŒÙ†Ú©",
        "Ø´ÛŒØ± Ø­Ù…Ø§Ù…",
        "Ø´ÛŒØ± ØªÙˆØ§Ù„Øª",
        "Ú†Ú©Ù‡",
        "Ù†Ø´ØªÛŒ Ø¢Ø¨",
        "Ù†Ø´ØªÛŒ",
        "Ù„ÙˆÙ„Ù‡ Ø¢Ø¨",
        "Ù„ÙˆÙ„Ù‡ ÙØ§Ø¶Ù„Ø§Ø¨",
        "Ú¯Ø±ÙØªÚ¯ÛŒ Ù„ÙˆÙ„Ù‡",
        "Ù„ÙˆÙ„Ù‡ Ú¯Ø±ÙØªÙ‡",
        "ÙØ§Ø¶Ù„Ø§Ø¨ Ú¯Ø±ÙØªÙ‡",
        "Ø³ÛŒÙ†Ú© Ú¯Ø±ÙØªÙ‡",
        "ØªÙˆØ§Ù„Øª Ú¯Ø±ÙØªÙ‡",
        "Ø¢Ø¨ Ø¬Ù…Ø¹ Ø´Ø¯Ù‡",
        "Ø±ÙØ¹ Ú¯Ø±ÙØªÚ¯ÛŒ",
        "ØªØ¹ÙˆÛŒØ¶ Ø´ÛŒØ±"
    ]):

        return (
            "ðŸ”§ Ø®Ø¯Ù…Ø§Øª Ù„ÙˆÙ„Ù‡â€ŒÚ©Ø´ÛŒ\n\n"
            "Ø¨Ø±Ø§ÛŒ Ø±ÙØ¹ Ù†Ø´ØªÛŒØŒ Ú¯Ø±ÙØªÚ¯ÛŒØŒ ØªØ¹ÙˆÛŒØ¶ "
            "Ø´ÛŒØ±Ø¢Ù„Ø§ØªØŒ Ù…Ø´Ú©Ù„Ø§Øª Ù„ÙˆÙ„Ù‡ Ùˆ ÙØ§Ø¶Ù„Ø§Ø¨ "
            "Ùˆ Ø®Ø¯Ù…Ø§Øª Ù…Ø´Ø§Ø¨Ù‡ Ù…ÛŒâ€ŒØªÙˆÙ†ÛŒØ¯ Ø¯Ø±Ø®ÙˆØ§Ø³Øª "
            "Ù„ÙˆÙ„Ù‡â€ŒÚ©Ø´ Ø«Ø¨Øª Ú©Ù†ÛŒØ¯."
        ), inline_button(
            "ðŸ”§ Ø«Ø¨Øª Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ù„ÙˆÙ„Ù‡â€ŒÚ©Ø´",
            ORDER_URL
        )

    # Ú©ÙˆÙ„Ø± Ú¯Ø§Ø²ÛŒ
    if contains_any(text, [
        "Ø§Ø³Ù¾Ù„ÛŒØª",
        "Ú©ÙˆÙ„Ø± Ø§Ø³Ù¾Ù„ÛŒØª",
        "Ú©ÙˆÙ„Ø± Ú¯Ø§Ø²ÛŒ Ø®Ø±Ø§Ø¨",
        "Ú©ÙˆÙ„Ø± Ú¯Ø§Ø²ÛŒ Ø®Ù†Ú© Ù†Ù…ÛŒÚ©Ù†Ù‡",
        "Ú©ÙˆÙ„Ø± Ú¯Ø§Ø²ÛŒ Ø®Ù†Ú© Ù†Ù…ÛŒ Ú©Ù†Ù‡",
        "Ú©ÙˆÙ„Ø± Ú¯Ø§Ø²ÛŒ Ø¨Ø§Ø¯ Ú¯Ø±Ù…",
        "Ú¯Ø§Ø² Ú©ÙˆÙ„Ø±",
        "Ø´Ø§Ø±Ú˜ Ú¯Ø§Ø² Ú©ÙˆÙ„Ø±",
        "Ù†Ø´ØªÛŒ Ú¯Ø§Ø² Ú©ÙˆÙ„Ø±",
        "Ø³Ø±ÙˆÛŒØ³ Ú©ÙˆÙ„Ø± Ú¯Ø§Ø²ÛŒ",
        "Ù†ØµØ¨ Ú©ÙˆÙ„Ø± Ú¯Ø§Ø²ÛŒ",
        "ØªØ¹Ù…ÛŒØ± Ø§Ø³Ù¾Ù„ÛŒØª",
        "ØªØ¹Ù…ÛŒØ± Ú©ÙˆÙ„Ø± Ú¯Ø§Ø²ÛŒ"
    ]):

        return (
            "â„ï¸ Ø®Ø¯Ù…Ø§Øª Ú©ÙˆÙ„Ø± Ú¯Ø§Ø²ÛŒ\n\n"
            "Ø¨Ø±Ø§ÛŒ Ù†ØµØ¨ØŒ Ø³Ø±ÙˆÛŒØ³ØŒ ØªØ¹Ù…ÛŒØ±ØŒ Ø¨Ø±Ø±Ø³ÛŒ "
            "Ø³Ø±Ù…Ø§ÛŒØ´ Ùˆ Ù…Ø´Ú©Ù„Ø§Øª Ø±Ø§ÛŒØ¬ Ú©ÙˆÙ„Ø± Ú¯Ø§Ø²ÛŒ "
            "Ù…ÛŒâ€ŒØªÙˆÙ†ÛŒØ¯ Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ù…ØªØ®ØµØµ Ù…Ø±ØªØ¨Ø· "
            "Ø«Ø¨Øª Ú©Ù†ÛŒØ¯."
        ), inline_button(
            "â„ï¸ Ø«Ø¨Øª Ø¯Ø±Ø®ÙˆØ§Ø³Øª",
            ORDER_URL
        )

    # Ú©ÙˆÙ„Ø± Ø¢Ø¨ÛŒ
    if contains_any(text, [
        "Ú©ÙˆÙ„Ø± Ø¢Ø¨ÛŒ Ø®Ø±Ø§Ø¨",
        "Ú©ÙˆÙ„Ø± Ø¢Ø¨ÛŒ Ø®Ù†Ú© Ù†Ù…ÛŒÚ©Ù†Ù‡",
        "Ú©ÙˆÙ„Ø± Ø¢Ø¨ÛŒ Ø®Ù†Ú© Ù†Ù…ÛŒ Ú©Ù†Ù‡",
        "Ù¾Ù…Ù¾ Ú©ÙˆÙ„Ø±",
        "Ù¾ÙˆØ´Ø§Ù„ Ú©ÙˆÙ„Ø±",
        "ØªØ³Ù…Ù‡ Ú©ÙˆÙ„Ø±",
        "Ù…ÙˆØªÙˆØ± Ú©ÙˆÙ„Ø±",
        "Ø¢Ø¨ Ú©ÙˆÙ„Ø±",
        "Ø³Ø±ÙˆÛŒØ³ Ú©ÙˆÙ„Ø± Ø¢Ø¨ÛŒ",
        "ØªØ¹Ù…ÛŒØ± Ú©ÙˆÙ„Ø± Ø¢Ø¨ÛŒ",
        "Ù†ØµØ¨ Ú©ÙˆÙ„Ø± Ø¢Ø¨ÛŒ"
    ]):

        return (
            "â„ï¸ Ø®Ø¯Ù…Ø§Øª Ú©ÙˆÙ„Ø± Ø¢Ø¨ÛŒ\n\n"
            "Ø¨Ø±Ø§ÛŒ Ø³Ø±ÙˆÛŒØ³ØŒ ØªØ¹Ù…ÛŒØ±ØŒ Ù†ØµØ¨ Ùˆ Ø¨Ø±Ø±Ø³ÛŒ "
            "Ù…Ø´Ú©Ù„Ø§Øª Ú©ÙˆÙ„Ø± Ø¢Ø¨ÛŒ Ù…ÛŒâ€ŒØªÙˆÙ†ÛŒØ¯ Ø¯Ø±Ø®ÙˆØ§Ø³Øª "
            "Ù…ØªØ®ØµØµ Ø«Ø¨Øª Ú©Ù†ÛŒØ¯."
        ), inline_button(
            "â„ï¸ Ø«Ø¨Øª Ø¯Ø±Ø®ÙˆØ§Ø³Øª",
            ORDER_URL
        )

    # Ù¾Ú©ÛŒØ¬
    if contains_any(text, [
        "Ù¾Ú©ÛŒØ¬ Ø®Ø±Ø§Ø¨",
        "Ù¾Ú©ÛŒØ¬ Ø±ÙˆØ´Ù† Ù†Ù…ÛŒØ´Ù‡",
        "Ù¾Ú©ÛŒØ¬ Ø±ÙˆØ´Ù† Ù†Ù…ÛŒ Ø´ÙˆØ¯",
        "Ù¾Ú©ÛŒØ¬ Ø¢Ø¨ Ú¯Ø±Ù…",
        "Ø¢Ø¨ Ú¯Ø±Ù… Ù†Ø¯Ø§Ø±Ù…",
        "Ø¢Ø¨ Ú¯Ø±Ù… Ù†Ù…ÛŒØ´Ù‡",
        "Ø¢Ø¨Ú¯Ø±Ù…Ú©Ù† Ø®Ø±Ø§Ø¨",
        "Ø¢Ø¨Ú¯Ø±Ù…Ú©Ù† Ø±ÙˆØ´Ù† Ù†Ù…ÛŒØ´Ù‡",
        "Ø¢Ø¨Ú¯Ø±Ù…Ú©Ù† Ø±ÙˆØ´Ù† Ù†Ù…ÛŒ Ø´ÙˆØ¯",
        "Ø³Ø±ÙˆÛŒØ³ Ù¾Ú©ÛŒØ¬",
        "ØªØ¹Ù…ÛŒØ± Ù¾Ú©ÛŒØ¬",
        "Ù†ØµØ¨ Ù¾Ú©ÛŒØ¬",
        "ØªØ¹Ù…ÛŒØ± Ø¢Ø¨Ú¯Ø±Ù…Ú©Ù†",
        "Ø³Ø±ÙˆÛŒØ³ Ø¢Ø¨Ú¯Ø±Ù…Ú©Ù†",
        "Ù†ØµØ¨ Ø¢Ø¨Ú¯Ø±Ù…Ú©Ù†"
    ]):

        return (
            "ðŸ”¥ Ø®Ø¯Ù…Ø§Øª Ù¾Ú©ÛŒØ¬ Ùˆ Ø¢Ø¨Ú¯Ø±Ù…Ú©Ù†\n\n"
            "Ø¨Ø±Ø§ÛŒ Ù†ØµØ¨ØŒ Ø³Ø±ÙˆÛŒØ³ØŒ ØªØ¹Ù…ÛŒØ± Ùˆ Ø¨Ø±Ø±Ø³ÛŒ "
            "Ù…Ø´Ú©Ù„Ø§Øª Ù¾Ú©ÛŒØ¬ ÛŒØ§ Ø¢Ø¨Ú¯Ø±Ù…Ú©Ù† Ù…ÛŒâ€ŒØªÙˆÙ†ÛŒØ¯ "
            "Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ù…ØªØ®ØµØµ Ù…Ø±ØªØ¨Ø· Ø«Ø¨Øª Ú©Ù†ÛŒØ¯."
        ), inline_button(
            "ðŸ”¥ Ø«Ø¨Øª Ø¯Ø±Ø®ÙˆØ§Ø³Øª",
            ORDER_URL
        )

    # Ù†Ø¸Ø§ÙØª
    if contains_any(text, [
        "Ù†Ø¸Ø§ÙØª Ù…Ù†Ø²Ù„",
        "ØªÙ…ÛŒØ²Ú©Ø§Ø±ÛŒ",
        "ØªÙ…ÛŒØ² Ú©Ø±Ø¯Ù† Ø®Ø§Ù†Ù‡",
        "Ù†Ø¸Ø§ÙØª Ø®Ø§Ù†Ù‡",
        "Ù†Ø¸Ø§ÙØªÚ†ÛŒ Ù…Ù†Ø²Ù„",
        "Ú©Ø§Ø±Ú¯Ø± Ù†Ø¸Ø§ÙØª",
        "Ù†Ø¸Ø§ÙØªÚ†ÛŒ Ù…ÛŒØ®ÙˆØ§Ù…",
        "Ù†Ø¸Ø§ÙØªÚ†ÛŒ Ù…ÛŒâ€ŒØ®ÙˆØ§Ù…",
        "Ù†Ø¸Ø§ÙØª Ø³Ø§Ø®ØªÙ…Ø§Ù†",
        "Ù†Ø¸Ø§ÙØª Ø±Ø§Ù‡ Ù¾Ù„Ù‡",
        "Ø±Ø§Ù‡ Ù¾Ù„Ù‡",
        "Ù†Ø¸Ø§ÙØª Ù…Ø­Ù„ Ú©Ø§Ø±",
        "Ù†Ø¸Ø§ÙØª Ø´Ø±Ú©Øª",
        "Ù†Ø¸Ø§ÙØª Ø§Ø¯Ø§Ø±ÛŒ"
    ]):

        return (
            "ðŸ§¹ Ø®Ø¯Ù…Ø§Øª Ù†Ø¸Ø§ÙØª\n\n"
            "Ø¨Ø±Ø§ÛŒ Ù†Ø¸Ø§ÙØª Ù…Ù†Ø²Ù„ØŒ Ø³Ø§Ø®ØªÙ…Ø§Ù†ØŒ Ù…Ø­Ù„ Ú©Ø§Ø± "
            "Ùˆ Ø®Ø¯Ù…Ø§Øª Ù…Ø´Ø§Ø¨Ù‡ Ù…ÛŒâ€ŒØªÙˆÙ†ÛŒØ¯ Ø¯Ø±Ø®ÙˆØ§Ø³Øª "
            "Ù†ÛŒØ±ÙˆÛŒ Ø®Ø¯Ù…Ø§ØªÛŒ Ø«Ø¨Øª Ú©Ù†ÛŒØ¯."
        ), inline_button(
            "ðŸ§¹ Ø«Ø¨Øª Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ù†Ø¸Ø§ÙØª",
            ORDER_URL
        )

    # Ø§Ø³Ø¨Ø§Ø¨ Ú©Ø´ÛŒ
    if contains_any(text, [
        "Ø§Ø³Ø¨Ø§Ø¨ Ú©Ø´ÛŒ",
        "Ø§Ø³Ø¨Ø§Ø¨â€ŒÚ©Ø´ÛŒ",
        "Ø§Ø«Ø§Ø« Ú©Ø´ÛŒ",
        "Ø§Ø«Ø§Ø«â€ŒÚ©Ø´ÛŒ",
        "Ø¬Ø§Ø¨Ø¬Ø§ÛŒÛŒ Ø§Ø«Ø§Ø«",
        "Ø¬Ø§Ø¨Ù‡ Ø¬Ø§ÛŒÛŒ Ø§Ø«Ø§Ø«",
        "Ø¬Ø§Ø¨Ù‡â€ŒØ¬Ø§ÛŒÛŒ Ø§Ø«Ø§Ø«",
        "Ø­Ù…Ù„ Ø§Ø«Ø§Ø«",
        "Ø­Ù…Ù„ ÙˆØ³Ø§ÛŒÙ„",
        "Ú©Ø§Ø±Ú¯Ø± Ø§Ø³Ø¨Ø§Ø¨ Ú©Ø´ÛŒ",
        "Ú©Ø§Ø±Ú¯Ø± Ø§Ø³Ø¨Ø§Ø¨â€ŒÚ©Ø´ÛŒ",
        "Ú©Ø§Ø±Ú¯Ø± Ø³Ø§Ø¯Ù‡",
        "Ù†ÛŒØ±ÙˆÛŒ Ø³Ø§Ø¯Ù‡",
        "Ù†ÛŒØ±ÙˆÛŒ Ú©Ù…Ú©ÛŒ",
        "Ø¬Ø§Ø¨Ø¬Ø§ÛŒÛŒ ÙˆØ³ÛŒÙ„Ù‡",
        "Ø¬Ø§Ø¨Ù‡ Ø¬Ø§ÛŒÛŒ ÙˆØ³ÛŒÙ„Ù‡",
        "Ø­Ù…Ù„ ÙˆØ³ÛŒÙ„Ù‡ Ø³Ù†Ú¯ÛŒÙ†",
        "Ø¬Ø§Ø¨Ø¬Ø§ÛŒÛŒ ÙˆØ³ÛŒÙ„Ù‡ Ø³Ù†Ú¯ÛŒÙ†"
    ]):

        return (
            "ðŸ“¦ Ø®Ø¯Ù…Ø§Øª Ø¬Ø§Ø¨Ù‡â€ŒØ¬Ø§ÛŒÛŒ Ùˆ Ø§Ø³Ø¨Ø§Ø¨â€ŒÚ©Ø´ÛŒ\n\n"
            "Ø¨Ø±Ø§ÛŒ Ø§Ø³Ø¨Ø§Ø¨â€ŒÚ©Ø´ÛŒØŒ Ø¬Ø§Ø¨Ù‡â€ŒØ¬Ø§ÛŒÛŒ ÙˆØ³Ø§ÛŒÙ„ØŒ "
            "Ù†ÛŒØ±ÙˆÛŒ Ú©Ù…Ú©ÛŒ Ùˆ Ø®Ø¯Ù…Ø§Øª Ù…Ø±ØªØ¨Ø· Ù…ÛŒâ€ŒØªÙˆÙ†ÛŒØ¯ "
            "Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ø«Ø¨Øª Ú©Ù†ÛŒØ¯.\n\n"
            "Ø§Ú¯Ø± Ù…Ø§Ø´ÛŒÙ† Ù‡Ù… Ù„Ø§Ø²Ù… Ø¯Ø§Ø±ÛŒØ¯ØŒ Ù†ÙˆØ¹ ÙˆØ³ÛŒÙ„Ù‡ "
            "Ùˆ Ù†ÛŒØ§Ø² Ø­Ù…Ù„ Ø±Ùˆ Ø¯Ø± ØªÙˆØ¶ÛŒØ­Ø§Øª Ø³ÙØ§Ø±Ø´ "
            "Ù…Ø´Ø®Øµ Ú©Ù†ÛŒØ¯."
        ), inline_button(
            "ðŸ“¦ Ø«Ø¨Øª Ø¯Ø±Ø®ÙˆØ§Ø³Øª",
            ORDER_URL
        )

    # Ù¾Ø±Ø¯Ù‡
    if contains_any(text, [
        "Ù¾Ø±Ø¯Ù‡",
        "Ù†ØµØ¨ Ù¾Ø±Ø¯Ù‡",
        "Ø±ÛŒÙ„ Ù¾Ø±Ø¯Ù‡",
        "Ú†ÙˆØ¨ Ù¾Ø±Ø¯Ù‡",
        "Ù†ØµØ¨ Ú†ÙˆØ¨ Ù¾Ø±Ø¯Ù‡",
        "ØªØ¹ÙˆÛŒØ¶ Ú†ÙˆØ¨ Ù¾Ø±Ø¯Ù‡",
        "Ù†ØµØ¨ Ø±ÛŒÙ„",
        "Ø±ÛŒÙ„ Ù¾Ø±Ø¯Ù‡ Ù†ØµØ¨",
        "Ù¾Ø±Ø¯Ù‡ Ø¬Ø¯ÛŒØ¯"
    ]):

        return (
            "ðŸªŸ Ø®Ø¯Ù…Ø§Øª Ù†ØµØ¨ Ù¾Ø±Ø¯Ù‡\n\n"
            "Ø¨Ø±Ø§ÛŒ Ù†ØµØ¨ ÛŒØ§ ØªØ¹ÙˆÛŒØ¶ Ú†ÙˆØ¨ Ù¾Ø±Ø¯Ù‡ØŒ "
            "Ø±ÛŒÙ„ Ùˆ Ø®Ø¯Ù…Ø§Øª Ù…Ø´Ø§Ø¨Ù‡ Ù…ÛŒâ€ŒØªÙˆÙ†ÛŒØ¯ "
            "Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ù…ØªØ®ØµØµ Ø«Ø¨Øª Ú©Ù†ÛŒØ¯."
        ), inline_button(
            "ðŸªŸ Ø«Ø¨Øª Ø¯Ø±Ø®ÙˆØ§Ø³Øª",
            ORDER_URL
        )

    # Ù‚ÙÙ„
    if contains_any(text, [
        "Ù‚ÙÙ„",
        "Ù‚ÙÙ„ Ø¯Ø±",
        "Ù‚ÙÙ„ Ø¯Ø±Ø¨",
        "Ø¯Ø³ØªÚ¯ÛŒØ±Ù‡",
        "Ø¯Ø³ØªÚ¯ÛŒØ±Ù‡ Ø¯Ø±",
        "ØªØ¹ÙˆÛŒØ¶ Ù‚ÙÙ„",
        "ØªØ¹ÙˆÛŒØ¶ Ø¯Ø³ØªÚ¯ÛŒØ±Ù‡",
        "Ú©Ù„ÛŒØ¯ Ø³Ø§Ø²",
        "Ú©Ù„ÛŒØ¯Ø³Ø§Ø²ÛŒ",
        "Ø¯Ø± Ø¨Ø§Ø² Ù†Ù…ÛŒØ´Ù‡",
        "Ø¯Ø± Ø¨Ø§Ø² Ù†Ù…ÛŒ Ø´ÙˆØ¯",
        "Ú©Ù„ÛŒØ¯ Ø´Ú©Ø³ØªÙ‡",
        "Ú©Ù„ÛŒØ¯ Ø¯Ø§Ø®Ù„ Ù‚ÙÙ„",
        "Ù‚ÙÙ„ Ú¯ÛŒØ± Ú©Ø±Ø¯Ù‡"
    ]):

        return (
            "ðŸ” Ø®Ø¯Ù…Ø§Øª Ù‚ÙÙ„ Ùˆ Ø¯Ø³ØªÚ¯ÛŒØ±Ù‡\n\n"
            "Ø¨Ø±Ø§ÛŒ ØªØ¹ÙˆÛŒØ¶ ÛŒØ§ ØªØ¹Ù…ÛŒØ± Ù‚ÙÙ„ØŒ Ø¯Ø³ØªÚ¯ÛŒØ±Ù‡ "
            "Ùˆ Ù…Ø´Ú©Ù„Ø§Øª Ù…Ø±ØªØ¨Ø· Ø¨Ø§ Ø¯Ø±Ø¨ Ù…ÛŒâ€ŒØªÙˆÙ†ÛŒØ¯ "
            "Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ù…ØªØ®ØµØµ Ø«Ø¨Øª Ú©Ù†ÛŒØ¯."
        ), inline_button(
            "ðŸ” Ø«Ø¨Øª Ø¯Ø±Ø®ÙˆØ§Ø³Øª",
            ORDER_URL
        )

    # Ø®Ø¯Ù…Ø§Øª ÙÙ†ÛŒ
    if contains_any(text, [
        "ÙÙ†ÛŒ Ú©Ø§Ø±",
        "Ú©Ø§Ø± ÙÙ†ÛŒ",
        "Ú©Ø§Ø±Ù‡Ø§ÛŒ ÙÙ†ÛŒ",
        "ØªØ¹Ù…ÛŒØ±Ú©Ø§Ø± Ù…Ù†Ø²Ù„",
        "ØªØ¹Ù…ÛŒØ±Ú©Ø§Ø± Ù…ÛŒØ®ÙˆØ§Ù…",
        "ØªØ¹Ù…ÛŒØ±Ú©Ø§Ø± Ù…ÛŒâ€ŒØ®ÙˆØ§Ù…",
        "Ù†ØµØ§Ø¨",
        "Ù†ØµØ§Ø¨ Ù…ÛŒØ®ÙˆØ§Ù…",
        "Ù†ØµØ§Ø¨ Ù…ÛŒâ€ŒØ®ÙˆØ§Ù…",
        "Ù†ØµØ¨ ÙˆØ³ÛŒÙ„Ù‡",
        "Ù†ØµØ¨ ØªØ¬Ù‡ÛŒØ²Ø§Øª",
        "Ø®Ø¯Ù…Ø§Øª Ù…Ù†Ø²Ù„",
        "Ø®Ø¯Ù…Ø§Øª ÙÙ†ÛŒ Ù…Ù†Ø²Ù„"
    ]):

        return (
            "ðŸ› ï¸ Ø®Ø¯Ù…Ø§Øª ÙÙ†ÛŒ Ø¯Ø± Ù…Ø­Ù„\n\n"
            "Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± Ø¨Ø±Ø§ÛŒ Ø®Ø¯Ù…Ø§Øª Ù…Ø®ØªÙ„Ù Ø¯Ø± Ù…Ø­Ù„ØŒ "
            "Ø§Ù…Ú©Ø§Ù† Ø«Ø¨Øª Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ùˆ Ø§Ø±ØªØ¨Ø§Ø· Ø¨Ø§ "
            "Ù…ØªØ®ØµØµ Ù…Ø±ØªØ¨Ø· Ø±Ùˆ ÙØ±Ø§Ù‡Ù… Ù…ÛŒâ€ŒÚ©Ù†Ù‡.\n\n"
            "Ù†ÙˆØ¹ Ø¯Ù‚ÛŒÙ‚ Ú©Ø§Ø± Ø±Ùˆ Ø¯Ø± Ø³ÙØ§Ø±Ø´ Ø¨Ù†ÙˆÛŒØ³ÛŒØ¯."
        ), inline_button(
            "ðŸ“ Ø«Ø¨Øª Ø³ÙØ§Ø±Ø´",
            ORDER_URL
        )

    # ØªÙˆØ¶ÛŒØ­Ø§Øª Ø³ÙØ§Ø±Ø´
    if contains_any(text, [
        "Ø¹Ú©Ø³ Ø³ÙØ§Ø±Ø´",
        "Ø¹Ú©Ø³ Ø¨ÙØ±Ø³ØªÙ…",
        "Ø¹Ú©Ø³ Ø¨ÙØ±Ø³ØªÙ… Ø¨Ø±Ø§ÛŒ Ù…ØªØ®ØµØµ",
        "ØªÙˆØ¶ÛŒØ­Ø§Øª Ø³ÙØ§Ø±Ø´",
        "ØªÙˆØ¶ÛŒØ­ Ø³ÙØ§Ø±Ø´",
        "Ø´Ø±Ø­ Ø³ÙØ§Ø±Ø´",
        "Ú†ÛŒ Ø¨Ù†ÙˆÛŒØ³Ù… Ø¯Ø± ØªÙˆØ¶ÛŒØ­Ø§Øª",
        "ØªÙˆØ¶ÛŒØ­Ø§Øª Ø±Ùˆ Ú†ÛŒ Ø¨Ù†ÙˆÛŒØ³Ù…",
        "Ù…Ø´Ú©Ù„ Ø±Ùˆ Ú†Ø·ÙˆØ± ØªÙˆØ¶ÛŒØ­ Ø¨Ø¯Ù…"
    ]):

        return (
            "ðŸ“ ØªÙˆØ¶ÛŒØ­ Ø¯Ù‚ÛŒÙ‚ Ø³ÙØ§Ø±Ø´\n\n"
            "Ù†ÙˆØ¹ Ø®Ø¯Ù…ØªØŒ Ù…Ø´Ú©Ù„ØŒ Ù…Ø­Ù„ Ø§Ù†Ø¬Ø§Ù… Ú©Ø§Ø±ØŒ "
            "ØªØ¹Ø¯Ø§Ø¯ ÛŒØ§ Ø§Ø¨Ø¹Ø§Ø¯ Ø¯Ø± ØµÙˆØ±Øª Ù†ÛŒØ§Ø² Ùˆ Ù‡Ø± "
            "Ù†Ú©ØªÙ‡â€ŒØ§ÛŒ Ú©Ù‡ Ø¨Ù‡ Ù…ØªØ®ØµØµ Ú©Ù…Ú© Ù…ÛŒâ€ŒÚ©Ù†Ù‡ "
            "Ø±Ùˆ Ø¯Ø± ØªÙˆØ¶ÛŒØ­Ø§Øª Ø¨Ù†ÙˆÛŒØ³ÛŒØ¯."
        ), inline_button(
            "ðŸ“ Ø«Ø¨Øª Ø³ÙØ§Ø±Ø´",
            ORDER_URL
        )

    # Ø§Ù…Ù†ÛŒØª
    if contains_any(text, [
        "Ù…Ø·Ù…Ø¦Ù†Ù‡",
        "Ù…Ø·Ù…Ø¦Ù† Ù‡Ø³Øª",
        "Ù‚Ø§Ø¨Ù„ Ø§Ø¹ØªÙ…Ø§Ø¯",
        "Ø§Ø¹ØªÙ…Ø§Ø¯ Ú©Ù†Ù…",
        "Ù…ØªØ®ØµØµ Ù‚Ø§Ø¨Ù„ Ø§Ø¹ØªÙ…Ø§Ø¯",
        "Ø§Ù…Ù† Ù‡Ø³Øª",
        "Ø§Ù…Ù†ÛŒØª",
        "Ø§Ù…Ù†ÛŒØª Ù¾Ø±Ø¯Ø§Ø®Øª",
        "Ø¢ÛŒØ§ Ø¢Ù†ÛŒ Ú©Ø§Ø± Ø§Ù…Ù† Ø§Ø³Øª",
        "Ø¢ÛŒØ§ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± Ø§Ù…Ù† Ø§Ø³Øª",
        "Ú†Ø·ÙˆØ± Ù…Ø·Ù…Ø¦Ù† Ø¨Ø´Ù…"
    ]):

        return (
            "ðŸ›¡ï¸ Ø§Ù…Ù†ÛŒØª Ùˆ Ù¾ÛŒÚ¯ÛŒØ±ÛŒ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±\n\n"
            "Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± Ø¨Ø±Ø§ÛŒ Ø«Ø¨Øª Ø¯Ø±Ø®ÙˆØ§Ø³ØªØŒ Ø§Ø±ØªØ¨Ø§Ø· "
            "Ø¨Ø§ Ù…ØªØ®ØµØµ Ùˆ ÙØ±Ø¢ÛŒÙ†Ø¯ Ù¾Ø±Ø¯Ø§Ø®Øª Ùˆ Ù¾ÛŒÚ¯ÛŒØ±ÛŒØŒ "
            "Ú†Ø§Ø±Ú†ÙˆØ¨ Ù…Ø´Ø®ØµÛŒ Ø¯Ø§Ø±Ù‡.\n\n"
            "Ø¨Ø±Ø§ÛŒ Ø§Ø³ØªÙØ§Ø¯Ù‡ Ø§Ø² ÙØ±Ø¢ÛŒÙ†Ø¯ Ø¶Ù…Ø§Ù†ØªØŒ Ù¾Ø±Ø¯Ø§Ø®Øª "
            "Ø±Ùˆ Ø§Ø² Ø·Ø±ÛŒÙ‚ Ø¯Ø±Ú¯Ø§Ù‡ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± Ø§Ù†Ø¬Ø§Ù… Ø¨Ø¯ÛŒØ¯."
        ), inline_button(
            "ðŸ“œ Ù‚ÙˆØ§Ù†ÛŒÙ† Ù…Ø´ØªØ±ÛŒ",
            CUSTOMER_RULES_URL
        )

    # ÙØ§Ú©ØªÙˆØ±
    if contains_any(text, [
        "ÙØ§Ú©ØªÙˆØ±",
        "Ø±Ø³ÛŒØ¯",
        "Ø±Ø³ÛŒØ¯ Ù¾Ø±Ø¯Ø§Ø®Øª",
        "Ø±Ø³ÛŒØ¯ Ú©Ø§Ø±",
        "ØµÙˆØ±ØªØ­Ø³Ø§Ø¨",
        "ØµÙˆØ±Øª Ø­Ø³Ø§Ø¨",
        "Ù…Ø¯Ø±Ú© Ù¾Ø±Ø¯Ø§Ø®Øª",
        "Ø§Ø«Ø¨Ø§Øª Ù¾Ø±Ø¯Ø§Ø®Øª"
    ]):

        return (
            "ðŸ§¾ Ø±Ø³ÛŒØ¯ Ùˆ Ù¾Ø±Ø¯Ø§Ø®Øª\n\n"
            "Ø§Ø·Ù„Ø§Ø¹Ø§Øª Ù¾Ø±Ø¯Ø§Ø®Øª Ùˆ Ø³ÙØ§Ø±Ø´ Ø±Ùˆ Ù†Ú¯Ù‡ Ø¯Ø§Ø±ÛŒØ¯ "
            "ØªØ§ Ø¯Ø± ØµÙˆØ±Øª Ù†ÛŒØ§Ø² Ø¨Ø±Ø§ÛŒ Ù¾ÛŒÚ¯ÛŒØ±ÛŒØŒ Ø§Ø·Ù„Ø§Ø¹Ø§Øª "
            "Ù„Ø§Ø²Ù… Ø¯Ø± Ø§Ø®ØªÛŒØ§Ø± Ù¾Ø´ØªÛŒØ¨Ø§Ù†ÛŒ Ø¨Ø§Ø´Ù‡."
        ), None

    # Ø´Ø±ÙˆØ¹
    if contains_any(text, [
        "Ø§Ø² Ú©Ø¬Ø§ Ø´Ø±ÙˆØ¹ Ú©Ù†Ù…",
        "Ú†ÛŒÚ©Ø§Ø± Ú©Ù†Ù…",
        "Ú†Ù‡ Ú©Ø§Ø± Ú©Ù†Ù…",
        "Ø§Ù„Ø§Ù† Ú†ÛŒÚ©Ø§Ø± Ú©Ù†Ù…",
        "Ø±Ø§Ù‡Ù†Ù…Ø§ÛŒÛŒ Ù…ÛŒØ®ÙˆØ§Ù…",
        "Ø±Ø§Ù‡Ù†Ù…Ø§ÛŒÛŒ Ù…ÛŒâ€ŒØ®ÙˆØ§Ù…",
        "Ú©Ù…Ú©Ù… Ú©Ù†",
        "Ú©Ù…Ú© Ù…ÛŒØ®ÙˆØ§Ù…",
        "Ú©Ù…Ú© Ù…ÛŒâ€ŒØ®ÙˆØ§Ù…",
        "Ø§ÙˆÙ„ Ú†ÛŒ",
        "Ù…Ø±Ø­Ù„Ù‡ Ø§ÙˆÙ„",
        "Ù‚Ø¯Ù… Ø§ÙˆÙ„"
    ]):

        return (
            "ðŸš€ Ø§Ø² Ø§ÛŒÙ†Ø¬Ø§ Ø´Ø±ÙˆØ¹ Ú©Ù†ÛŒØ¯\n\n"
            "Ø§Ú¯Ø± Ù…Ø´ØªØ±ÛŒ Ù‡Ø³ØªÛŒØ¯ØŒ Ù†ÙˆØ¹ Ø®Ø¯Ù…Øª Ù…ÙˆØ±Ø¯Ù†ÛŒØ§Ø²ØªÙˆÙ† "
            "Ø±Ùˆ Ù…Ø´Ø®Øµ Ú©Ù†ÛŒØ¯ Ùˆ Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ø±Ùˆ Ø«Ø¨Øª Ú©Ù†ÛŒØ¯.\n\n"
            "Ø§Ú¯Ø± Ù…ØªØ®ØµØµ Ù‡Ø³ØªÛŒØ¯ Ùˆ Ù‚ØµØ¯ Ù‡Ù…Ú©Ø§Ø±ÛŒ Ø¯Ø§Ø±ÛŒØ¯ØŒ "
            "Ø§Ø² Ø¨Ø®Ø´ Ø«Ø¨Øªâ€ŒÙ†Ø§Ù… Ù…ØªØ®ØµØµ Ø§Ù‚Ø¯Ø§Ù… Ú©Ù†ÛŒØ¯."
        ), inline_button(
            "ðŸŒ ÙˆØ±ÙˆØ¯ Ø¨Ù‡ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±",
            SITE_URL
        )

    # Ø®Ø¯Ù…Ø§Øª Ø¹Ù…ÙˆÙ…ÛŒ
    if contains_any(text, [
        "Ø¨Ø±Ù‚Ú©Ø§Ø±",
        "Ø¨Ø±Ù‚ Ú©Ø§Ø±ÛŒ",
        "Ø¨Ø±Ù‚Ú©Ø§Ø±ÛŒ",
        "Ø³ÛŒÙ… Ú©Ø´ÛŒ",
        "Ø³ÛŒÙ…â€ŒÚ©Ø´ÛŒ",
        "Ù„ÙˆÙ„Ù‡ Ú©Ø´",
        "Ù„ÙˆÙ„Ù‡â€ŒÚ©Ø´",
        "Ù„ÙˆÙ„Ù‡ Ú©Ø´ÛŒ",
        "Ù„ÙˆÙ„Ù‡â€ŒÚ©Ø´ÛŒ",
        "Ú©ÙˆÙ„Ø± Ú¯Ø§Ø²ÛŒ",
        "Ú©ÙˆÙ„Ø±Ú¯Ø§Ø²ÛŒ",
        "Ú©ÙˆÙ„Ø± Ø¢Ø¨ÛŒ",
        "Ù¾Ú©ÛŒØ¬",
        "Ø¢Ø¨Ú¯Ø±Ù…Ú©Ù†",
        "Ù†Ø¸Ø§ÙØªÚ†ÛŒ",
        "Ù†Ø¸Ø§ÙØª",
        "ØªØ¹Ù…ÛŒØ±Ú©Ø§Ø±",
        "ØªØ¹Ù…ÛŒØ±Ø§Øª"
    ]):

        return (
            "ðŸ”§ Ù¾ÛŒØ¯Ø§ Ú©Ø±Ø¯Ù† Ù…ØªØ®ØµØµ\n\n"
            "Ø¨Ø±Ø§ÛŒ Ø§ÛŒÙ† Ù†ÙˆØ¹ Ø®Ø¯Ù…Øª Ù…ÛŒâ€ŒØªÙˆÙ†ÛŒØ¯ "
            "Ø¯Ø±Ø®ÙˆØ§Ø³ØªØªÙˆÙ† Ø±Ùˆ Ø¯Ø± Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± Ø«Ø¨Øª Ú©Ù†ÛŒØ¯ "
            "ØªØ§ Ù…ØªØ®ØµØµ Ù…Ø±ØªØ¨Ø· Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ø´Ù…Ø§ Ø±Ùˆ "
            "Ø¨Ø±Ø±Ø³ÛŒ Ú©Ù†Ù‡.\n\n"
            "ðŸ‘‡ Ø´Ø±ÙˆØ¹ Ø¯Ø±Ø®ÙˆØ§Ø³Øª:"
        ), inline_button(
            "ðŸš€ Ø«Ø¨Øª Ø³ÙØ§Ø±Ø´",
            ORDER_URL
        )

    # ØªØ´Ú©Ø±
    if contains_any(text, [
        "Ù…Ù…Ù†ÙˆÙ†",
        "Ù…Ø±Ø³ÛŒ",
        "Ù…ØªØ´Ú©Ø±Ù…",
        "ØªØ´Ú©Ø±",
        "Ø¯Ù…Øª Ú¯Ø±Ù…",
        "Ø³Ù¾Ø§Ø³"
    ]):

        return (
            "Ø®ÙˆØ§Ù‡Ø´ Ù…ÛŒâ€ŒÚ©Ù†Ù… ðŸŒ¹\n\n"
            "Ù‡Ø± Ø³Ø¤Ø§Ù„ Ø¯ÛŒÚ¯Ù‡â€ŒØ§ÛŒ Ø¯Ø±Ø¨Ø§Ø±Ù‡ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± "
            "Ø¯Ø§Ø´ØªÛŒØŒ Ù…Ù† Ø¯Ø± Ø®Ø¯Ù…ØªÙ…."
        ), None

    # Ø®Ø¯Ø§Ø­Ø§ÙØ¸ÛŒ
    if contains_any(text, [
        "Ø®Ø¯Ø§Ø­Ø§ÙØ¸",
        "ÙØ¹Ù„Ø§",
        "ÙØ¹Ù„Ø§Ù‹",
        "Ø¨Ø§ÛŒ"
    ]):

        return (
            "Ø¨Ù‡ Ø§Ù…ÛŒØ¯ Ø¯ÛŒØ¯Ø§Ø± ðŸ‘‹ðŸ’›\n\n"
            "Ù‡Ø± ÙˆÙ‚Øª Ø¯Ø±Ø¨Ø§Ø±Ù‡ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± Ø³Ø¤Ø§Ù„ÛŒ Ø¯Ø§Ø´ØªÛŒ "
            "Ù…ÛŒâ€ŒØªÙˆÙ†ÛŒ Ø¯ÙˆØ¨Ø§Ø±Ù‡ Ù¾ÛŒØ§Ù… Ø¨Ø¯ÛŒ."
        ), None

    # Ø®Ø§Ø±Ø¬ Ø§Ø² Ø­ÙˆØ²Ù‡
    if contains_any(text, [
        "Ø¨ÛŒØª Ú©ÙˆÛŒÙ†",
        "Ø¨ÛŒØªÚ©ÙˆÛŒÙ†",
        "Ú©Ø±ÛŒÙ¾ØªÙˆ",
        "Ø§Ø±Ø² Ø¯ÛŒØ¬ÛŒØªØ§Ù„",
        "ÙÙˆØªØ¨Ø§Ù„",
        "ÙÛŒÙ„Ù…",
        "Ø¢Ø¨ Ùˆ Ù‡ÙˆØ§",
        "Ù‡ÙˆØ§ Ú†Ø·ÙˆØ±Ù‡",
        "Ø®Ø¨Ø±",
        "Ø§Ø®Ø¨Ø§Ø±"
    ]):

        return (
            "ðŸ™‚ Ù…Ù† Ø¯Ø³ØªÛŒØ§Ø± Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± Ù‡Ø³ØªÙ… Ùˆ ØªÙ…Ø±Ú©Ø²Ù… "
            "Ø±ÙˆÛŒ Ø®Ø¯Ù…Ø§Øª Ùˆ Ù¾Ù„ØªÙØ±Ù… Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±Ù‡.\n\n"
            "Ø§Ú¯Ø± Ø¯Ø±Ø¨Ø§Ø±Ù‡ Ø«Ø¨Øª Ø³ÙØ§Ø±Ø´ØŒ Ù…ØªØ®ØµØµÛŒÙ†ØŒ "
            "Ù‚ÛŒÙ…ØªØŒ Ù¾Ø±Ø¯Ø§Ø®ØªØŒ Ø¶Ù…Ø§Ù†ØªØŒ Ù‚ÙˆØ§Ù†ÛŒÙ† ÛŒØ§ "
            "Ù†Ø­ÙˆÙ‡ Ú©Ø§Ø± Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± Ø³Ø¤Ø§Ù„ÛŒ Ø¯Ø§Ø±ÛŒØ¯ØŒ "
            "Ø¨Ø§ Ø®ÛŒØ§Ù„ Ø±Ø§Ø­Øª Ø¨Ù¾Ø±Ø³ÛŒØ¯."
        ), None

    # Ù¾ÛŒØ´ ÙØ±Ø¶
    return (
        "ðŸ¤” Ù…ØªÙˆØ¬Ù‡ Ù…Ù†Ø¸ÙˆØ±ØªÙˆÙ† Ù†Ø´Ø¯Ù….\n\n"
        "Ù…Ù† Ù…ÛŒâ€ŒØªÙˆÙ†Ù… Ø¯Ø±Ø¨Ø§Ø±Ù‡ Ø§ÛŒÙ† Ù…ÙˆØ§Ø±Ø¯ Ø±Ø§Ù‡Ù†Ù…Ø§ÛŒÛŒâ€ŒØªÙˆÙ† Ú©Ù†Ù…:\n\n"
        "ðŸ“ Ø«Ø¨Øª Ø³ÙØ§Ø±Ø´\n"
        "ðŸ‘¨â€ðŸ”§ Ù‡Ù…Ú©Ø§Ø±ÛŒ Ù…ØªØ®ØµØµ\n"
        "ðŸ“± Ù†Ø­ÙˆÙ‡ Ú©Ø§Ø±\n"
        "ðŸ’° Ù‚ÛŒÙ…Øª Ø®Ø¯Ù…Ø§Øª\n"
        "ðŸ’³ Ù¾Ø±Ø¯Ø§Ø®Øª Ùˆ Ø¶Ù…Ø§Ù†Øª\n"
        "ðŸ“œ Ù‚ÙˆØ§Ù†ÛŒÙ†\n"
        "ðŸŽ§ Ù¾Ø´ØªÛŒØ¨Ø§Ù†ÛŒ\n\n"
        "ÛŒØ§ Ø³Ø¤Ø§Ù„ Ø®ÙˆØ¯ØªÙˆÙ† Ø±Ùˆ Ø¨Ø§ Ø¬Ø²Ø¦ÛŒØ§Øª Ø¨ÛŒØ´ØªØ±ÛŒ "
        "Ø¨Ù†ÙˆÛŒØ³ÛŒØ¯."
    ), None


# =========================================================
# Health Server Ø¨Ø±Ø§ÛŒ Render
# =========================================================

class HealthHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "text/plain; charset=utf-8"
        )

        self.end_headers()

        self.wfile.write(
            b"AnykarHelpBot is running"
        )

    def log_message(
        self,
        format,
        *args
    ):

        return


def start_health_server():

    port = int(
        os.environ.get(
            "PORT",
            "10000"
        )
    )

    server = HTTPServer(
        ("0.0.0.0", port),
        HealthHandler
    )

    print(
        f"Health server running on port {port}"
    )

    server.serve_forever()


# =========================================================
# Ø§Ø¬Ø±Ø§ÛŒ Ø§ØµÙ„ÛŒ Ø±Ø¨Ø§Øª
# =========================================================

def main():

    print(
        "AnykarHelpBot starting..."
    )

    print(
        "AnykarHelpBot - Luxury Smart Brain ÙØ¹Ø§Ù„ Ø´Ø¯..."
    )

    keyboard = main_keyboard()

    offset = None

    consecutive_failures = 0

    while True:

        try:

            result = get_updates(offset)

            if result is None:

                consecutive_failures += 1

                print(
                    f"[POLL ERROR] "
                    f"consecutive_failures="
                    f"{consecutive_failures}"
                )

                time.sleep(
                    min(
                        10 + consecutive_failures * 3,
                        60
                    )
                )

                continue

            if not result.get("ok"):

                consecutive_failures += 1

                print(
                    "[POLL BALE ERROR]",
                    result
                )

                time.sleep(
                    min(
                        10 + consecutive_failures * 3,
                        60
                    )
                )

                continue

            if consecutive_failures > 0:

                print(
                    "[POLL RECOVERED] "
                    "Bale connection recovered."
                )

            consecutive_failures = 0

            updates = result.get(
                "result",
                []
            )

            for update in updates:

                try:

                    update_id = update.get(
                        "update_id"
                    )

                    if update_id is not None:

                        offset = update_id + 1

                    message = update.get(
                        "message"
                    )

                    if not message:

                        continue

                    chat = message.get(
                        "chat",
                        {}
                    )

                    chat_id = chat.get(
                        "id"
                    )

                    if chat_id is None:

                        continue

                    text = message.get(
                        "text",
                        ""
                    )

                    # -----------------------------------------
                    # Ø®ÙˆØ¯Ø§Ø¸Ù‡Ø§Ø±ÛŒ
                    # -----------------------------------------

                    if text == "ðŸ“‹ Ø®ÙˆØ¯Ø§Ø¸Ù‡Ø§Ø±ÛŒ Ù…ØªØ®ØµØµ":

                        membership = get_channel_membership_status(
                            chat_id
                        )

                        if membership is None:

                            send_message(
                                chat_id,
                                "âš ï¸ Ø¨Ø±Ø±Ø³ÛŒ Ø¹Ø¶ÙˆÛŒØª Ø¯Ø± Ú©Ø§Ù†Ø§Ù„ Ø§Ù†Ø¬Ø§Ù… Ù†Ø´Ø¯.\n\n"
                                "Ù„Ø·ÙØ§Ù‹ Ú†Ù†Ø¯ Ù„Ø­Ø¸Ù‡ Ø¨Ø¹Ø¯ Ø¯ÙˆØ¨Ø§Ø±Ù‡ ØªÙ„Ø§Ø´ Ú©Ù†."
                            )

                            continue

                        if not membership:

                            send_message(
                                chat_id,
                                "ðŸ“¢ Ø¨Ø±Ø§ÛŒ Ø§Ù†Ø¬Ø§Ù… Ø®ÙˆØ¯Ø§Ø¸Ù‡Ø§Ø±ÛŒ Ù…ØªØ®ØµØµØŒ Ø§Ø¨ØªØ¯Ø§ Ø¨Ø§ÛŒØ¯ "
                                "Ø¯Ø± Ú©Ø§Ù†Ø§Ù„ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± Ø¹Ø¶Ùˆ Ø¨Ø´ÛŒ.\n\n"
                                "Ø¨Ø¹Ø¯ Ø§Ø² Ø¹Ø¶ÙˆÛŒØªØŒ Ø¯ÙˆØ¨Ø§Ø±Ù‡ Ø±ÙˆÛŒ Â«ðŸ“‹ Ø®ÙˆØ¯Ø§Ø¸Ù‡Ø§Ø±ÛŒ Ù…ØªØ®ØµØµÂ» Ø¨Ø²Ù†.",
                                inline_button(
                                    "ðŸ“¢ Ø¹Ø¶ÙˆÛŒØª Ø¯Ø± Ú©Ø§Ù†Ø§Ù„ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±",
                                    CHANNEL_URL
                                )
                            )

                            continue

                        start_self_declaration(
                            chat_id
                        )

                        continue

                    # -----------------------------------------
                    # Ø§Ø¯Ø§Ù…Ù‡ Ø®ÙˆØ¯Ø§Ø¸Ù‡Ø§Ø±ÛŒ
                    # -----------------------------------------

                    if chat_id in self_declaration_sessions:

                        process_self_declaration(
                            chat_id,
                            message
                        )

                        continue

                    print(
                        f"[MESSAGE] "
                        f"chat_id={chat_id} | "
                        f"text={repr(text)}"
                    )

                    # -----------------------------------------
                    # MY ID
                    # -----------------------------------------

                    if text == "/myid":

                        send_message(
                            chat_id,
                            f"ðŸ†” Chat ID Ø´Ù…Ø§:\n{chat_id}"
                        )

                        continue

                    # -----------------------------------------
                    # START
                    # -----------------------------------------

                    if text == "/start":

                        try:

                            with open(
                                os.path.join(
                                    os.path.dirname(
                                        os.path.abspath(__file__)
                                    ),
                                    "welcome.jpg"
                                ),
                                "rb"
                            ) as photo:

                                send_photo(
                                    chat_id,
                                    photo.read()
                                )

                            send_message(
                                chat_id,
                                "ðŸ‘‹ Ø®ÙˆØ´ Ø§ÙˆÙ…Ø¯ÛŒ Ø¨Ù‡ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± ðŸ’›"
                            )

                            send_main_menu(
                                chat_id,
                                keyboard
                            )

                        except Exception as e:

                            print(
                                "[WELCOME IMAGE ERROR]",
                                repr(e)
                            )

                            send_message(
                                chat_id,
                                "Ø³Ù„Ø§Ù… ðŸ‘‹\n"
                                "Ø¨Ù‡ Ø¯Ø³ØªÛŒØ§Ø± Ù‡ÙˆØ´Ù…Ù†Ø¯ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± Ø®ÙˆØ´ Ø§ÙˆÙ…Ø¯ÛŒ."
                            )

                            send_main_menu(
                                chat_id,
                                keyboard
                            )

                        continue

                    # -----------------------------------------
                    # Ø¯Ø¹ÙˆØª Ø§Ø² Ø¯ÙˆØ³ØªØ§Ù†
                    # -----------------------------------------

                    if text == "ðŸ‘¥ Ø¯Ø¹ÙˆØª Ø§Ø² Ø¯ÙˆØ³ØªØ§Ù†":

                        send_message(
                            chat_id,
                            invite_friends(chat_id),
                            inline_button(
                                "ðŸ¤– ÙˆØ±ÙˆØ¯ Ø¨Ù‡ Ø¨Ø§Øª Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±",
                                BOT_URL
                            )
                        )

                        continue

                    # -----------------------------------------
                    # Ø«Ø¨Øª Ø³ÙØ§Ø±Ø´
                    # -----------------------------------------

                    if (
                        text == "ðŸ“ Ø«Ø¨Øª Ø³ÙØ§Ø±Ø´"
                        or text == "/order"
                    ):

                        reply = (
                            "ðŸ“ Ø«Ø¨Øª Ø³ÙØ§Ø±Ø´ Ø¯Ø± Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±\n\n"
                            "Ø®Ø¯Ù…Øª Ù…ÙˆØ±Ø¯Ù†Ø¸Ø±Øª Ø±Ùˆ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ØŒ "
                            "Ø¯Ø±Ø®ÙˆØ§Ø³ØªØª Ø±Ùˆ Ø«Ø¨Øª Ú©Ù† Ùˆ Ù…Ù†ØªØ¸Ø± "
                            "Ù¾ÛŒØ´Ù†Ù‡Ø§Ø¯ Ù…ØªØ®ØµØµÛŒÙ† Ù…Ø±ØªØ¨Ø· Ø¨Ø§Ø´.\n\n"
                            "ðŸ‘‡ Ø´Ø±ÙˆØ¹ Ú©Ù†:"
                        )

                        send_message(
                            chat_id,
                            reply,
                            inline_button(
                                "ðŸš€ Ø«Ø¨Øª Ø³ÙØ§Ø±Ø´ Ø¯Ø± Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±",
                                ORDER_URL
                            )
                        )

                        continue

                    # -----------------------------------------
                    # Ù‡Ù…Ú©Ø§Ø±ÛŒ Ù…ØªØ®ØµØµ
                    # -----------------------------------------

                    if (
                        text == "ðŸ‘¨â€ðŸ”§ Ù‡Ù…Ú©Ø§Ø±ÛŒ Ù…ØªØ®ØµØµ"
                        or text == "/specialist"
                    ):

                        reply = (
                            "ðŸ‘¨â€ðŸ”§ Ù‡Ù…Ú©Ø§Ø±ÛŒ Ø¨Ù‡â€ŒØ¹Ù†ÙˆØ§Ù† Ù…ØªØ®ØµØµ\n\n"
                            "Ø§Ú¯Ø± Ù…ØªØ®ØµØµ Ø®Ø¯Ù…Ø§Øª Ù‡Ø³ØªÛŒ Ùˆ Ù…ÛŒâ€ŒØ®ÙˆØ§ÛŒ "
                            "Ø¨Ø§ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± Ù‡Ù…Ú©Ø§Ø±ÛŒ Ú©Ù†ÛŒØŒ Ø§Ø² ØµÙØ­Ù‡ "
                            "Ø«Ø¨Øªâ€ŒÙ†Ø§Ù… Ù…ØªØ®ØµØµ Ø´Ø±ÙˆØ¹ Ú©Ù†.\n\n"
                            "ðŸ‘‡"
                        )

                        send_message(
                            chat_id,
                            reply,
                            inline_button(
                                "ðŸš€ Ø«Ø¨Øªâ€ŒÙ†Ø§Ù… Ù…ØªØ®ØµØµ",
                                SPECIALIST_URL
                            )
                        )

                        continue

                    # -----------------------------------------
                    # Ù†Ø­ÙˆÙ‡ Ú©Ø§Ø±
                    # -----------------------------------------

                    if text == "ðŸ“± Ù†Ø­ÙˆÙ‡ Ú©Ø§Ø±":

                        reply = (
                            "ðŸ“± Ù†Ø­ÙˆÙ‡ Ú©Ø§Ø± Ø¨Ø§ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±\n\n"
                            "Ø¨Ø±Ø§ÛŒ Ù…Ø´Ø§Ù‡Ø¯Ù‡ Ø¢Ù…ÙˆØ²Ø´ Ú©Ø§Ù…Ù„ Ù†Ø­ÙˆÙ‡ "
                            "Ø§Ø³ØªÙØ§Ø¯Ù‡ Ø§Ø² Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±:"
                        )

                        send_message(
                            chat_id,
                            reply,
                            inline_button(
                                "ðŸŽ¬ Ù…Ø´Ø§Ù‡Ø¯Ù‡ Ù†Ø­ÙˆÙ‡ Ú©Ø§Ø±",
                                WORK_URL
                            )
                        )

                        continue

                    # -----------------------------------------
                    # Ù‚ÛŒÙ…Øª
                    # -----------------------------------------

                    if text == "ðŸ’° Ù‚ÛŒÙ…Øª Ø®Ø¯Ù…Ø§Øª":

                        reply = (
                            "ðŸ’° Ù‚ÛŒÙ…Øª Ø®Ø¯Ù…Ø§Øª\n\n"
                            "Ù‚ÛŒÙ…Øª Ù†Ù‡Ø§ÛŒÛŒ Ø¨Ø³ØªÙ‡ Ø¨Ù‡ Ù†ÙˆØ¹ Ø®Ø¯Ù…Øª Ùˆ "
                            "Ø´Ø±Ø§ÛŒØ· ÙˆØ§Ù‚Ø¹ÛŒ Ú©Ø§Ø± Ù…ØªÙØ§ÙˆØª Ù‡Ø³Øª.\n\n"
                            "Ø¨Ø±Ø§ÛŒ Ù…Ø´Ø§Ù‡Ø¯Ù‡ Ø®Ø¯Ù…Ø§Øª Ùˆ Ø«Ø¨Øª Ø¯Ø±Ø®ÙˆØ§Ø³Øª:"
                        )

                        send_message(
                            chat_id,
                            reply,
                            inline_button(
                                "ðŸ“ Ù…Ø´Ø§Ù‡Ø¯Ù‡ Ø®Ø¯Ù…Ø§Øª",
                                ORDER_URL
                            )
                        )

                        continue

                    # -----------------------------------------
                    # Ù¾Ø±Ø¯Ø§Ø®Øª Ùˆ Ø¶Ù…Ø§Ù†Øª
                    # -----------------------------------------

                    if text == "ðŸ›¡ï¸ Ù¾Ø±Ø¯Ø§Ø®Øª Ùˆ Ø¶Ù…Ø§Ù†Øª":

                        reply = (
                            "ðŸ›¡ï¸ Ù¾Ø±Ø¯Ø§Ø®Øª Ùˆ Ø¶Ù…Ø§Ù†Øª Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±\n\n"
                            "Ù¾Ø±Ø¯Ø§Ø®Øª Ú©Ø§Ø± Ø¨Ø§ÛŒØ¯ Ø§Ø² Ø·Ø±ÛŒÙ‚ Ø¯Ø±Ú¯Ø§Ù‡ "
                            "Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± Ø§Ù†Ø¬Ø§Ù… Ø¨Ø´Ù‡.\n\n"
                            "ðŸ’³ Ù…Ø¨Ù„Øº Ù¾Ø±Ø¯Ø§Ø®ØªÛŒ ØªØ§ Û·Û² Ø³Ø§Ø¹Øª "
                            "Ø¨Ù„ÙˆÚ©Ù‡ Ù…ÛŒâ€ŒÙ…ÙˆÙ†Ù‡.\n\n"
                            "Ø§Ú¯Ø± Ù…Ø´ØªØ±ÛŒ Ù…Ø´Ú©Ù„ÛŒ Ø¯Ø±Ø¨Ø§Ø±Ù‡ Ø§Ù†Ø¬Ø§Ù… "
                            "Ú©Ø§Ø± Ø§Ø¹Ù„Ø§Ù… Ù†Ú©Ù†Ù‡ØŒ Ù…Ø¨Ù„Øº Ø·Ø¨Ù‚ ÙØ±Ø¢ÛŒÙ†Ø¯ "
                            "Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± Ø¨Ù‡ Ù…ØªØ®ØµØµ Ù¾Ø±Ø¯Ø§Ø®Øª Ù…ÛŒâ€ŒØ´Ù‡.\n\n"
                            "Ø¯Ø± ØµÙˆØ±Øª Ø¨Ø±ÙˆØ² Ù…Ø´Ú©Ù„ØŒ Ù…ÙˆØ¶ÙˆØ¹ Ø§Ø² "
                            "Ø·Ø±ÛŒÙ‚ Ù¾Ø´ØªÛŒØ¨Ø§Ù†ÛŒ Ù¾ÛŒÚ¯ÛŒØ±ÛŒ Ù…ÛŒâ€ŒØ´Ù‡."
                        )

                        send_message(
                            chat_id,
                            reply,
                            inline_button(
                                "ðŸ“œ Ù‚ÙˆØ§Ù†ÛŒÙ† Ù…Ø´ØªØ±ÛŒ",
                                CUSTOMER_RULES_URL
                            )
                        )

                        continue

                    # -----------------------------------------
                    # Ù‚ÙˆØ§Ù†ÛŒÙ† Ù…Ø´ØªØ±ÛŒ
                    # -----------------------------------------

                    if text == "ðŸ“œ Ù‚ÙˆØ§Ù†ÛŒÙ† Ù…Ø´ØªØ±ÛŒ":

                        reply = (
                            "ðŸ“œ Ù‚ÙˆØ§Ù†ÛŒÙ† Ù…Ø´ØªØ±ÛŒØ§Ù† Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±\n\n"
                            "Ø¨Ø±Ø§ÛŒ Ù…Ø´Ø§Ù‡Ø¯Ù‡ Ø¢Ø®Ø±ÛŒÙ† Ù†Ø³Ø®Ù‡ Ù‚ÙˆØ§Ù†ÛŒÙ† "
                            "Ùˆ Ø´Ø±Ø§ÛŒØ· Ø§Ø³ØªÙØ§Ø¯Ù‡:"
                        )

                        send_message(
                            chat_id,
                            reply,
                            inline_button(
                                "ðŸ“– Ù…Ø·Ø§Ù„Ø¹Ù‡ Ù‚ÙˆØ§Ù†ÛŒÙ†",
                                CUSTOMER_RULES_URL
                            )
                        )

                        continue

                    # -----------------------------------------
                    # Ù‚ÙˆØ§Ù†ÛŒÙ† Ù…ØªØ®ØµØµ
                    # -----------------------------------------

                    if text == "ðŸ“‹ Ù‚ÙˆØ§Ù†ÛŒÙ† Ù…ØªØ®ØµØµ":

                        reply = (
                            "ðŸ“‹ Ù‚ÙˆØ§Ù†ÛŒÙ† Ù…ØªØ®ØµØµÛŒÙ† Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±\n\n"
                            "Ø´Ø±Ø§ÛŒØ· Ù‡Ù…Ú©Ø§Ø±ÛŒØŒ Ú©Ù…ÛŒØ³ÛŒÙˆÙ† Ùˆ "
                            "Ø¶ÙˆØ§Ø¨Ø· Ù…ØªØ®ØµØµÛŒÙ† Ø¯Ø± ØµÙØ­Ù‡ Ø±Ø³Ù…ÛŒ "
                            "Ù‚ÙˆØ§Ù†ÛŒÙ† Ù…ØªØ®ØµØµÛŒÙ† Ù‚Ø±Ø§Ø± Ø¯Ø§Ø±Ø¯.\n\n"
                            "ðŸ‘‡"
                        )

                        send_message(
                            chat_id,
                            reply,
                            inline_button(
                                "ðŸ“‹ Ù…Ø·Ø§Ù„Ø¹Ù‡ Ù‚ÙˆØ§Ù†ÛŒÙ† Ù…ØªØ®ØµØµÛŒÙ†",
                                SPECIALIST_RULES_URL
                            )
                        )

                        continue

                    # -----------------------------------------
                    # Ù¾Ø´ØªÛŒØ¨Ø§Ù†ÛŒ
                    # -----------------------------------------

                    if (
                        text == "ðŸŽ§ Ù¾Ø´ØªÛŒØ¨Ø§Ù†ÛŒ"
                        or text == "/support"
                    ):

                        support_sessions[chat_id] = {
                            "step": "name",
                            "name": "",
                            "phone": "",
                            "service": "",
                            "problem": ""
                        }

                        send_message(
                            chat_id,
                            "ðŸŽ§ Ù¾Ø´ØªÛŒØ¨Ø§Ù†ÛŒ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø±\n\n"
                            "Ø¨Ø±Ø§ÛŒ Ù¾ÛŒÚ¯ÛŒØ±ÛŒØŒ Ù„Ø·ÙØ§Ù‹ Ù†Ø§Ù… Ùˆ Ù†Ø§Ù… Ø®Ø§Ù†ÙˆØ§Ø¯Ú¯ÛŒ Ø®ÙˆØ¯ Ø±Ø§ ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒØ¯."
                        )

                        continue

                    # -----------------------------------------
                    # Ø§Ø¯Ø§Ù…Ù‡ Ù¾Ø´ØªÛŒØ¨Ø§Ù†ÛŒ
                    # -----------------------------------------

                    if chat_id in support_sessions:

                        session = support_sessions[
                            chat_id
                        ]

                        step = session["step"]

                        if step == "name":

                            session["name"] = text

                            session["step"] = "phone"

                            send_message(
                                chat_id,
                                "ðŸ“ž Ù…Ù…Ù†ÙˆÙ†.\n\n"
                                "Ø­Ø§Ù„Ø§ Ø´Ù…Ø§Ø±Ù‡ ØªÙ…Ø§Ø³ Ø®ÙˆØ¯Øª Ø±Ùˆ ÙˆØ§Ø±Ø¯ Ú©Ù†:"
                            )

                            continue

                        if step == "phone":

                            session["phone"] = text

                            session["step"] = "service"

                            send_message(
                                chat_id,
                                "ðŸ”§ Ø´Ù…Ø§Ø±Ù‡ ØªÙ…Ø§Ø³ Ø«Ø¨Øª Ø´Ø¯.\n\n"
                                "Ø­Ø§Ù„Ø§ Ø¨Ú¯Ùˆ Ø¨Ø±Ø§ÛŒ Ú†Ù‡ Ø®Ø¯Ù…ØªÛŒ "
                                "Ù†ÛŒØ§Ø² Ø¨Ù‡ Ù¾Ø´ØªÛŒØ¨Ø§Ù†ÛŒ Ø¯Ø§Ø±ÛŒØŸ\n\n"
                                "Ù…Ø«Ù„Ø§Ù‹: Ø¨Ø±Ù‚Ú©Ø§Ø±ÛŒØŒ Ù„ÙˆÙ„Ù‡â€ŒÚ©Ø´ÛŒØŒ Ù†Ø¸Ø§ÙØªØŒ "
                                "Ø§Ø³Ø¨Ø§Ø¨â€ŒÚ©Ø´ÛŒ Ùˆ..."
                            )

                            continue

                        if step == "service":

                            session["service"] = text

                            session["step"] = "problem"

                            send_message(
                                chat_id,
                                "ðŸ“ Ø­Ø§Ù„Ø§ Ù…Ø´Ú©Ù„ ÛŒØ§ Ø¯Ø±Ø®ÙˆØ§Ø³ØªØª Ø±Ùˆ "
                                "Ø¨Ø§ Ø¬Ø²Ø¦ÛŒØ§Øª Ø¨Ø±Ø§Ù… Ø¨Ù†ÙˆÛŒØ³:"
                            )

                            continue

                        if step == "problem":

                            session["problem"] = text

                            support_message = (
                                "ðŸŽ§ Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ù¾Ø´ØªÛŒØ¨Ø§Ù†ÛŒ Ø¬Ø¯ÛŒØ¯\n\n"
                                "ðŸ‘¤ Ù†Ø§Ù… Ùˆ Ù†Ø§Ù… Ø®Ø§Ù†ÙˆØ§Ø¯Ú¯ÛŒ:\n"
                                f"{session['name']}\n\n"
                                "ðŸ“ž Ø´Ù…Ø§Ø±Ù‡ ØªÙ…Ø§Ø³:\n"
                                f"{session['phone']}\n\n"
                                "ðŸ”§ Ø®Ø¯Ù…Øª:\n"
                                f"{session['service']}\n\n"
                                "ðŸ“ Ø´Ø±Ø­ Ù…Ø´Ú©Ù„:\n"
                                f"{session['problem']}\n\n"
                                "ðŸ†” Chat ID Ú©Ø§Ø±Ø¨Ø±:\n"
                                f"{chat_id}"
                            )

                            send_message(
                                ADMIN_CHAT_ID,
                                support_message
                            )

                            send_message(
                                chat_id,
                                "âœ… Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ù¾Ø´ØªÛŒØ¨Ø§Ù†ÛŒ Ø´Ù…Ø§ Ø«Ø¨Øª Ø´Ø¯.\n\n"
                                "Ø§Ø·Ù„Ø§Ø¹Ø§Øª Ø´Ù…Ø§ Ø¨Ø±Ø§ÛŒ Ù¾Ø´ØªÛŒØ¨Ø§Ù†ÛŒ Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± "
                                "Ø§Ø±Ø³Ø§Ù„ Ø´Ø¯ Ùˆ Ø¯Ø± Ø§ÙˆÙ„ÛŒÙ† ÙØ±ØµØª Ø¨Ø±Ø±Ø³ÛŒ Ù…ÛŒâ€ŒØ´ÙˆØ¯. ðŸ’›"
                            )

                            send_main_menu(
                                chat_id,
                                keyboard
                            )

                            del support_sessions[
                                chat_id
                            ]

                            continue

                    # -----------------------------------------
                    # FAQ
                    # -----------------------------------------

                    if (
                        text == "â“ Ø³ÙˆØ§Ù„Ø§Øª Ù…ØªØ¯Ø§ÙˆÙ„"
                        or text == "/faq"
                    ):

                        reply = (
                            "â“ Ø³ÙˆØ§Ù„Ø§Øª Ù…ØªØ¯Ø§ÙˆÙ„\n\n"
                            "Ø³Ø¤Ø§Ù„ Ø®ÙˆØ¯Øª Ø±Ùˆ Ù‡Ù…ÛŒÙ†Ø¬Ø§ Ø¨Ù†ÙˆÛŒØ³.\n\n"
                            "Ù…Ø«Ù„Ø§Ù‹:\n"
                            "Â«Ø¢Ù†ÛŒâ€ŒÚ©Ø§Ø± Ú†ÛŒÙ‡ØŸÂ»\n"
                            "Â«Ú†Ø·ÙˆØ± Ø³ÙØ§Ø±Ø´ Ø¨Ø¯Ù…ØŸÂ»\n"
                            "Â«Ú†Ø·ÙˆØ± Ù…ØªØ®ØµØµ Ø¨Ø´Ù…ØŸÂ»\n"
                            "Â«Ù¾ÙˆÙ„ Ø±Ùˆ Ú†Ø·ÙˆØ± Ù¾Ø±Ø¯Ø§Ø®Øª Ú©Ù†Ù…ØŸÂ»\n"
                            "Â«Ø¶Ù…Ø§Ù†Øª Ú©Ø§Ø± Ú†Ø·ÙˆØ±Ù‡ØŸÂ»"
                        )

                        send_main_menu(
                            chat_id,
                            keyboard
                        )

                        continue

                    # -----------------------------------------
                    # HELP
                    # -----------------------------------------

                    if (
                        text == "â„¹ï¸ Ø±Ø§Ù‡Ù†Ù…Ø§"
                        or text == "/help"
                    ):

                        reply = (
                            "â„¹ï¸ Ø±Ø§Ù‡Ù†Ù…Ø§ÛŒ AnykarHelpBot\n\n"
                            "Ù…Ù† Ù…ÛŒâ€ŒØªÙˆÙ†Ù… Ø¯Ø±Ø¨Ø§Ø±Ù‡ Ø§ÛŒÙ† Ù…ÙˆØ§Ø±Ø¯ "
                            "Ø±Ø§Ù‡Ù†Ù…Ø§ÛŒÛŒâ€ŒØ§Øª Ú©Ù†Ù…:\n\n"
                            "ðŸ“ Ø«Ø¨Øª Ø³ÙØ§Ø±Ø´\n"
                            "ðŸ‘¨â€ðŸ”§ Ù‡Ù…Ú©Ø§Ø±ÛŒ Ù…ØªØ®ØµØµ\n"
                            "ðŸ“± Ù†Ø­ÙˆÙ‡ Ú©Ø§Ø±\n"
                            "ðŸ’° Ù‚ÛŒÙ…Øª Ø®Ø¯Ù…Ø§Øª\n"
                            "ðŸ›¡ï¸ Ù¾Ø±Ø¯Ø§Ø®Øª Ùˆ Ø¶Ù…Ø§Ù†Øª\n"
                            "ðŸ“œ Ù‚ÙˆØ§Ù†ÛŒÙ† Ù…Ø´ØªØ±ÛŒ\n"
                            "ðŸ“‹ Ù‚ÙˆØ§Ù†ÛŒÙ† Ù…ØªØ®ØµØµ\n"
                            "ðŸŽ§ Ù¾Ø´ØªÛŒØ¨Ø§Ù†ÛŒ\n\n"
                            "ðŸ’¬ Ø­ØªÛŒ Ù„Ø§Ø²Ù… Ù†ÛŒØ³Øª Ø§Ø² Ù…Ù†Ùˆ Ø§Ø³ØªÙØ§Ø¯Ù‡ Ú©Ù†ÛŒØ› "
                            "Ø³Ø¤Ø§Ù„Øª Ø±Ùˆ Ø¢Ø²Ø§Ø¯Ø§Ù†Ù‡ Ø¨Ù†ÙˆÛŒØ³."
                        )

                        send_main_menu(
                            chat_id,
                            keyboard
                        )

                        continue

                    # -----------------------------------------
                    # Ù¾ÛŒØ§Ù… Ø¢Ø²Ø§Ø¯
                    # -----------------------------------------

                    reply, button = answer(
                        text
                    )

                    send_message(
                        chat_id,
                        reply,
                        button if button else keyboard
                    )

                except Exception as e:

                    print(
                        "[UPDATE ERROR]",
                        repr(e)
                    )

                    continue

        except Exception as e:

            print(
                "[MAIN LOOP ERROR]",
                repr(e)
            )

            print(
                "Bot will reconnect automatically..."
            )

            time.sleep(10)


# =========================================================
# START
# =========================================================

if __name__ == "__main__":

    try:

        health_thread = threading.Thread(
            target=start_health_server,
            daemon=True
        )

        health_thread.start()

        print(
            f"Bale API forced IP: {BALE_NEW_IP}"
        )

        main()

    except Exception as e:

        print(
            "[FATAL ERROR]",
            repr(e)
        )

        time.sleep(10)

        while True:

            try:

                main()

            except Exception as inner_error:

                print(
                    "[RESTART ERROR]",
                    repr(inner_error)
                )

                time.sleep(10)
