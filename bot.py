import urllib.request
import json
import time
import re
import os
import socket
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# بله اعلام کرده IP جدید API آن‌ها این است.
# URL همچنان با نام دامنه tapi.bale.ai استفاده می‌شود تا HTTPS/SNI درست بماند.
BALE_HOST = "tapi.bale.ai"
BALE_NEW_IP = "2.189.68.110"

_original_getaddrinfo = socket.getaddrinfo

def _bale_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    if host == BALE_HOST:
        host = BALE_NEW_IP
    return _original_getaddrinfo(host, port, family, type, proto, flags)

socket.getaddrinfo = _bale_getaddrinfo

TOKEN = "977852941:qyI7kowjWCw6aSJCIsVZxL2rUem0g-HgGKc"

BASE_URL = f"https://tapi.bale.ai/bot{TOKEN}"

ORDER_URL = "https://anykar.ir/categories"
SPECIALIST_URL = "https://anykar.ir/servicer-registration"
WORK_URL = "https://anykar.ir/work"
CUSTOMER_RULES_URL = "https://anykar.ir/rules"
SPECIALIST_RULES_URL = "https://anykar.ir/servicer-rules"
SITE_URL = "https://anykar.ir"


def api_request(method, data=None):
    url = f"{BASE_URL}/{method}"

    try:
        body = json.dumps(
            data or {},
            ensure_ascii=False
        ).encode("utf-8")

        request = urllib.request.Request(
            url,
            data=body,
            headers={
                "Content-Type": "application/json"
            },
            method="POST"
        )

        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(
                response.read().decode("utf-8")
            )

    except Exception as e:
        print("API ERROR:", repr(e))
        return None


def get_updates(offset=None):
    data = {}

    if offset is not None:
        data["offset"] = offset

    return api_request("getUpdates", data)


def send_message(chat_id, text, keyboard=None):
    data = {
        "chat_id": chat_id,
        "text": text
    }

    if keyboard:
        data["reply_markup"] = keyboard

    return api_request("sendMessage", data)


def normalize_text(text):
    text = text.lower().strip()

    replacements = {
        "ي": "ی",
        "ى": "ی",
        "ك": "ک",
        "ۀ": "ه",
        "ة": "ه",
        "\u200c": " ",
        "‌": " "
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r"\s+", " ", text)

    return text


def contains_any(text, words):
    return any(word in text for word in words)


def main_keyboard():
    return {
        "keyboard": [
            [
                {"text": "📝 ثبت سفارش"},
                {"text": "👨‍🔧 همکاری متخصص"}
            ],
            [
                {"text": "📱 نحوه کار"},
                {"text": "💰 قیمت خدمات"}
            ],
            [
                {"text": "🛡️ پرداخت و ضمانت"},
                {"text": "📜 قوانین مشتری"}
            ],
            [
                {"text": "📋 قوانین متخصص"},
                {"text": "🎧 پشتیبانی"}
            ],
            [
                {"text": "❓ سوالات متداول"},
                {"text": "ℹ️ راهنما"}
            ]
        ],
        "resize_keyboard": True
    }


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


def answer(text):
    text = normalize_text(text)

    # سلام
    if contains_any(text, [
        "سلام",
        "درود",
        "صبح بخیر",
        "شب بخیر",
        "خسته نباشید"
    ]):
        return (
            "سلام 👋✨\n\n"
            "به دستیار هوشمند آنی‌کار خوش آمدید.\n\n"
            "من می‌تونم درباره ثبت سفارش، متخصصین، "
            "قیمت، پرداخت، ضمانت، قوانین و نحوه "
            "کار آنی‌کار راهنمایی‌تون کنم.\n\n"
            "سؤالتون رو همینجا بنویسید یا از منوی "
            "پایین استفاده کنید."
        ), None

    # آنی کار چیست
    if contains_any(text, [
        "آنی کار چیه",
        "آنی‌کار چیه",
        "آنی کار چیست",
        "آنی‌کار چیست",
        "آنی کار یعنی چی",
        "آنی‌کار یعنی چی",
        "آنی کار چه کاری",
        "آنی‌کار چه کاری",
        "درباره آنی کار",
        "درباره آنی‌کار",
        "در مورد آنی کار",
        "در مورد آنی‌کار",
        "معرفی آنی کار",
        "معرفی آنی‌کار",
        "این آنی کار چیه",
        "این آنی‌کار چیه"
    ]):
        return (
            "💛 آنی‌کار چیست؟\n\n"
            "آنی‌کار یک پلتفرم برای ارتباط مشتریان "
            "با متخصصین خدمات مختلف در محل است.\n\n"
            "هدف آنی‌کار اینه که پیدا کردن متخصص "
            "مناسب برای خدمات موردنیاز، سریع‌تر، "
            "مطمئن‌تر و ساده‌تر انجام بشه.\n\n"
            "🌐 برای آشنایی بیشتر با آنی‌کار:"
        ), inline_button("🌐 ورود به آنی‌کار", SITE_URL)

    # ثبت سفارش
    if contains_any(text, [
        "ثبت سفارش",
        "سفارش ثبت کنم",
        "چطور سفارش",
        "چگونه سفارش",
        "سفارش بدم",
        "سفارش بزارم",
        "سفارش بذارم",
        "درخواست ثبت",
        "درخواست بدم",
        "متخصص میخوام",
        "متخصص می‌خوام",
        "خدمات میخوام",
        "خدمت میخوام",
        "استادکار میخوام",
        "استاد کار میخوام"
    ]):
        return (
            "📝 ثبت سفارش در آنی‌کار\n\n"
            "برای درخواست خدمات، خدمت موردنظرتون "
            "رو انتخاب و درخواستتون رو ثبت کنید.\n\n"
            "متخصصین مرتبط درخواست شما رو بررسی "
            "می‌کنن و می‌تونید متخصص مناسب رو "
            "انتخاب کنید.\n\n"
            "👇 برای شروع ثبت درخواست:"
        ), inline_button("🚀 ثبت سفارش در آنی‌کار", ORDER_URL)

    # متخصص / ثبت نام
    if contains_any(text, [
        "متخصص بشم",
        "متخصص شوم",
        "متخصص شدن",
        "ثبت نام متخصص",
        "ثبت‌نام متخصص",
        "عضویت متخصص",
        "عضو متخصص",
        "همکاری متخصص",
        "همکاری با آنی کار",
        "همکاری با آنی‌کار",
        "چطور با آنی کار همکاری",
        "چطور با آنی‌کار همکاری",
        "استادکار بشم",
        "استاد کار بشم",
        "ثبت نام استادکار",
        "ثبت‌نام استادکار"
    ]):
        return (
            "👨‍🔧 همکاری با آنی‌کار\n\n"
            "اگر در زمینه خدمات تخصص دارید و "
            "می‌خواهید به‌عنوان متخصص با آنی‌کار "
            "همکاری کنید، می‌تونید از طریق صفحه "
            "ثبت‌نام متخصص اقدام کنید.\n\n"
            "👇 شروع ثبت‌نام:"
        ), inline_button("🚀 ثبت‌نام متخصص", SPECIALIST_URL)

    # نحوه کار
    if contains_any(text, [
        "نحوه کار",
        "چطور کار میکنه",
        "چطور کار می‌کنه",
        "چگونه کار میکند",
        "چگونه کار می‌کنه",
        "روش کار",
        "آموزش کار با برنامه",
        "آموزش برنامه",
        "راهنمای برنامه",
        "چطور از برنامه استفاده",
        "چگونه از برنامه استفاده",
        "چطور از آنی کار استفاده",
        "چطور از آنی‌کار استفاده"
    ]):
        return (
            "📱 نحوه کار با آنی‌کار\n\n"
            "برای مشاهده آموزش و آشنایی کامل "
            "با نحوه استفاده از آنی‌کار، راهنمای "
            "مخصوص کاربران رو ببینید.\n\n"
            "👇 مشاهده راهنما:"
        ), inline_button("🎬 مشاهده نحوه کار", WORK_URL)

    # قیمت
    if contains_any(text, [
        "قیمت",
        "هزینه",
        "نرخ",
        "اجرت",
        "دستمزد",
        "چقدر میشه",
        "چند میشه",
        "هزینه کار",
        "قیمت کار",
        "قیمت خدمات"
    ]):
        return (
            "💰 قیمت خدمات آنی‌کار\n\n"
            "هزینه نهایی خدمات می‌تونه با توجه "
            "به نوع خدمت، شرایط کار، میزان کار "
            "و نظر متخصص متفاوت باشه.\n\n"
            "آنی‌کار برای راهنمایی مشتری، اطلاعات "
            "قیمت خدمات رو در فرآیند ثبت درخواست "
            "ارائه می‌کنه."
        ), inline_button("📝 مشاهده خدمات و ثبت سفارش", ORDER_URL)

    # کمیسیون
    if contains_any(text, [
        "کمیسیون",
        "درصد کمیسیون",
        "درصد آنی کار",
        "درصد آنی‌کار",
        "سهم آنی کار",
        "سهم آنی‌کار",
        "کمیسیون متخصص"
    ]):
        return (
            "💳 کمیسیون متخصصین\n\n"
            "درصد و شرایط کمیسیون متخصصین طبق "
            "قوانین و شرایط همکاری آنی‌کار تعیین "
            "شده است.\n\n"
            "برای مشاهده درصد و جزئیات دقیق، "
            "صفحه قوانین متخصصین رو ببینید."
        ), inline_button(
            "📋 مشاهده قوانین متخصصین",
            SPECIALIST_RULES_URL
        )

    # پرداخت
    if contains_any(text, [
        "پرداخت",
        "پول رو بدم",
        "پول را بدم",
        "پول متخصص",
        "مبلغ کار",
        "واریز",
        "درگاه",
        "مستقیم به متخصص",
        "مستقیم به استادکار"
    ]):
        return (
            "💳 پرداخت امن آنی‌کار\n\n"
            "برای برخورداری از فرآیند ضمانت و "
            "پیگیری آنی‌کار، مبلغ کار باید از "
            "طریق درگاه آنی‌کار پرداخت بشه.\n\n"
            "پس از پرداخت، مبلغ تا ۷۲ ساعت "
            "در وضعیت بلوکه باقی می‌مونه.\n\n"
            "اگر مشتری در این بازه مشکلی درباره "
            "انجام کار اعلام نکنه، مبلغ طبق "
            "فرآیند آنی‌کار به متخصص پرداخت می‌شه."
        ), inline_button(
            "📜 مشاهده قوانین مشتری",
            CUSTOMER_RULES_URL
        )

    # ضمانت
    if contains_any(text, [
        "ضمانت",
        "گارانتی",
        "پول بلوکه",
        "۷۲ ساعت",
        "72 ساعت",
        "هفتاد و دو ساعت",
        "اگر مشکل داشته باشم",
        "اگر مشکلی پیش بیاد",
        "مشکل بعد از کار",
        "نارضایتی",
        "ناراضی",
        "کار خراب",
        "متخصص کار رو خراب"
    ]):
        return (
            "🛡️ ضمانت و پیگیری آنی‌کار\n\n"
            "برای استفاده از فرآیند ضمانت، "
            "پرداخت باید از طریق درگاه آنی‌کار "
            "انجام بشه.\n\n"
            "💳 مبلغ پرداختی تا ۷۲ ساعت بلوکه "
            "می‌مونه.\n\n"
            "اگر مشتری مشکلی درباره انجام کار "
            "اعلام نکنه، مبلغ طبق فرآیند آنی‌کار "
            "به متخصص پرداخت می‌شه.\n\n"
            "در صورت بروز مشکل، موضوع باید از "
            "طریق پشتیبانی آنی‌کار پیگیری بشه."
        ), inline_button(
            "📜 قوانین و شرایط",
            CUSTOMER_RULES_URL
        )

    # قوانین مشتری
    if contains_any(text, [
        "قوانین مشتری",
        "قانون مشتری",
        "شرایط مشتری",
        "قوانین سایت",
        "قوانین آنی کار",
        "قوانین آنی‌کار",
        "قانون آنی کار",
        "قانون آنی‌کار"
    ]):
        return (
            "📜 قوانین مشتریان آنی‌کار\n\n"
            "برای مشاهده نسخه کامل و به‌روز "
            "قوانین و شرایط استفاده، از صفحه "
            "رسمی قوانین آنی‌کار استفاده کنید.\n\n"
            "👇 مشاهده قوانین:"
        ), inline_button(
            "📖 قوانین مشتریان",
            CUSTOMER_RULES_URL
        )

    # قوانین متخصص
    if contains_any(text, [
        "قوانین متخصص",
        "قانون متخصص",
        "شرایط متخصص",
        "قوانین استادکار",
        "قانون استادکار",
        "شرایط همکاری متخصص"
    ]):
        return (
            "📋 قوانین متخصصین آنی‌کار\n\n"
            "در صفحه قوانین متخصصین، شرایط "
            "همکاری، کمیسیون و ضوابط مربوط "
            "به متخصصین به‌صورت کامل توضیح "
            "داده شده است.\n\n"
            "👇 مشاهده قوانین:"
        ), inline_button(
            "📋 قوانین متخصصین",
            SPECIALIST_RULES_URL
        )

    # پشتیبانی
    if contains_any(text, [
        "پشتیبانی",
        "کمک",
        "راهنمایی",
        "مشکل دارم",
        "مشکل پیش اومده",
        "مشکل پیش آمده",
        "تماس",
        "ارتباط",
        "پیگیری"
    ]):
        return (
            "🎧 پشتیبانی آنی‌کار\n\n"
            "موضوع یا مشکلتون رو همینجا "
            "توضیح بدید تا راهنمایی‌تون کنم.\n\n"
            "اگر موضوع مربوط به یک سفارش هست، "
            "اطلاعات و مستندات مربوط به سفارش "
            "رو هم آماده داشته باشید."
        ), None

    # FAQ
    if contains_any(text, [
        "سوالات متداول",
        "سوال رایج",
        "سوالات رایج",
        "faq",
        "چه سوالاتی",
        "سوال دارم"
    ]):
        return (
            "❓ سوالات متداول\n\n"
            "هر سؤالی درباره آنی‌کار دارید "
            "می‌تونید همینجا بنویسید.\n\n"
            "مثلاً:\n"
            "• چطور سفارش بدم؟\n"
            "• چطور متخصص بشم؟\n"
            "• پرداخت چطور انجام میشه؟\n"
            "• ضمانت آنی‌کار چطوره؟\n"
            "• قوانین رو از کجا ببینم؟"
        ), None

    # خدمات خاص
    if contains_any(text, [
        "برقکار",
        "برق کاری",
        "برقکاری",
        "سیم کشی",
        "سیم‌کشی",
        "لوله کش",
        "لوله‌کش",
        "لوله کشی",
        "لوله‌کشی",
        "کولر گازی",
        "کولرگازی",
        "کولر آبی",
        "پکیج",
        "آبگرمکن",
        "نظافتچی",
        "نظافت",
        "تعمیرکار",
        "تعمیرات"
    ]):
        return (
            "🔧 پیدا کردن متخصص\n\n"
            "برای این نوع خدمت می‌تونید "
            "درخواستتون رو در آنی‌کار ثبت کنید "
            "تا متخصص مرتبط درخواست شما رو "
            "بررسی کنه.\n\n"
            "👇 شروع درخواست:"
        ), inline_button(
            "🚀 ثبت سفارش",
            ORDER_URL
        )

    # تشکر
    if contains_any(text, [
        "ممنون",
        "مرسی",
        "متشکرم",
        "تشکر",
        "دمت گرم",
        "سپاس"
    ]):
        return (
            "خواهش می‌کنم 🌹\n\n"
            "هر سؤال دیگه‌ای درباره آنی‌کار "
            "داشتی، من در خدمتم."
        ), None

    # خداحافظی
    if contains_any(text, [
        "خداحافظ",
        "فعلا",
        "فعلاً",
        "بای"
    ]):
        return (
            "به امید دیدار 👋💛\n\n"
            "هر وقت درباره آنی‌کار سؤالی داشتی "
            "می‌تونی دوباره پیام بدی."
        ), None

    # خارج از حوزه
    if contains_any(text, [
        "بیت کوین",
        "بیتکوین",
        "کریپتو",
        "ارز دیجیتال",
        "فوتبال",
        "فیلم",
        "آب و هوا",
        "هوا چطوره",
        "خبر",
        "اخبار"
    ]):
        return (
            "🙂 من دستیار آنی‌کار هستم و تمرکزم "
            "روی خدمات و پلتفرم آنی‌کاره.\n\n"
            "اگر درباره ثبت سفارش، متخصصین، "
            "قیمت، پرداخت، ضمانت، قوانین یا "
            "نحوه کار آنی‌کار سؤالی دارید، "
            "با خیال راحت بپرسید."
        ), None

    # پیش فرض
    return (
        "🤔 متوجه منظورتون نشدم.\n\n"
        "من می‌تونم درباره این موارد راهنمایی‌تون کنم:\n\n"
        "📝 ثبت سفارش\n"
        "👨‍🔧 همکاری متخصص\n"
        "📱 نحوه کار\n"
        "💰 قیمت خدمات\n"
        "💳 پرداخت و ضمانت\n"
        "📜 قوانین\n"
        "🎧 پشتیبانی\n\n"
        "یا سؤال خودتون رو با جزئیات بیشتری "
        "بنویسید."
    ), None


def main():

    print("AnykarHelpBot - Luxury Smart Brain فعال شد...")

    keyboard = main_keyboard()

    offset = None

    while True:

        result = get_updates(offset)

        if result and result.get("ok"):

            for update in result.get("result", []):

                offset = update["update_id"] + 1

                message = update.get("message")

                if not message:
                    continue

                chat_id = message["chat"]["id"]

                text = message.get(
                    "text",
                    ""
                )

                print("پیام دریافت شد:", text)

                if text == "/start":

                    reply = (
                        "╭──────────────╮\n"
                        "      💛 ANYKAR\n"
                        "   دستیار هوشمند آنی‌کار\n"
                        "╰──────────────╯\n\n"
                        "سلام 👋\n"
                        "به دستیار هوشمند آنی‌کار خوش اومدی.\n\n"
                        "اینجام تا درباره خدمات، ثبت سفارش، "
                        "متخصصین، پرداخت، ضمانت و قوانین "
                        "راهنمایی‌ات کنم.\n\n"
                        "💬 سؤالت رو مستقیم بنویس\n"
                        "یا یکی از گزینه‌های زیر رو انتخاب کن."
                    )

                    send_message(
                        chat_id,
                        reply,
                        keyboard
                    )

                    continue

                if text == "📝 ثبت سفارش" or text == "/order":

                    reply = (
                        "📝 ثبت سفارش در آنی‌کار\n\n"
                        "خدمت موردنظرت رو انتخاب کن، "
                        "درخواستت رو ثبت کن و منتظر "
                        "پیشنهاد متخصصین مرتبط باش.\n\n"
                        "👇 شروع کن:"
                    )

                    send_message(
                        chat_id,
                        reply,
                        inline_button(
                            "🚀 ثبت سفارش در آنی‌کار",
                            ORDER_URL
                        )
                    )

                    continue

                if text == "👨‍🔧 همکاری متخصص" or text == "/specialist":

                    reply = (
                        "👨‍🔧 همکاری به‌عنوان متخصص\n\n"
                        "اگر متخصص خدمات هستی و می‌خوای "
                        "با آنی‌کار همکاری کنی، از صفحه "
                        "ثبت‌نام متخصص شروع کن.\n\n"
                        "👇"
                    )

                    send_message(
                        chat_id,
                        reply,
                        inline_button(
                            "🚀 ثبت‌نام متخصص",
                            SPECIALIST_URL
                        )
                    )

                    continue

                if text == "📱 نحوه کار":

                    reply = (
                        "📱 نحوه کار با آنی‌کار\n\n"
                        "برای مشاهده آموزش کامل نحوه "
                        "استفاده از آنی‌کار:"
                    )

                    send_message(
                        chat_id,
                        reply,
                        inline_button(
                            "🎬 مشاهده نحوه کار",
                            WORK_URL
                        )
                    )

                    continue

                if text == "💰 قیمت خدمات":

                    reply = (
                        "💰 قیمت خدمات\n\n"
                        "قیمت نهایی بسته به نوع خدمت و "
                        "شرایط واقعی کار متفاوت هست.\n\n"
                        "برای مشاهده خدمات و ثبت درخواست:"
                    )

                    send_message(
                        chat_id,
                        reply,
                        inline_button(
                            "📝 مشاهده خدمات",
                            ORDER_URL
                        )
                    )

                    continue

                if text == "🛡️ پرداخت و ضمانت":

                    reply = (
                        "🛡️ پرداخت و ضمانت آنی‌کار\n\n"
                        "پرداخت کار باید از طریق درگاه "
                        "آنی‌کار انجام بشه.\n\n"
                        "💳 مبلغ پرداختی تا ۷۲ ساعت "
                        "بلوکه می‌مونه.\n\n"
                        "اگر مشتری مشکلی درباره انجام "
                        "کار اعلام نکنه، مبلغ طبق فرآیند "
                        "آنی‌کار به متخصص پرداخت می‌شه.\n\n"
                        "در صورت بروز مشکل، موضوع از "
                        "طریق پشتیبانی پیگیری می‌شه."
                    )

                    send_message(
                        chat_id,
                        reply,
                        inline_button(
                            "📜 قوانین مشتری",
                            CUSTOMER_RULES_URL
                        )
                    )

                    continue

                if text == "📜 قوانین مشتری":

                    reply = (
                        "📜 قوانین مشتریان آنی‌کار\n\n"
                        "برای مشاهده آخرین نسخه قوانین "
                        "و شرایط استفاده:"
                    )

                    send_message(
                        chat_id,
                        reply,
                        inline_button(
                            "📖 مطالعه قوانین",
                            CUSTOMER_RULES_URL
                        )
                    )

                    continue

                if text == "📋 قوانین متخصص":

                    reply = (
                        "📋 قوانین متخصصین آنی‌کار\n\n"
                        "شرایط همکاری، کمیسیون و "
                        "ضوابط متخصصین در صفحه رسمی "
                        "قوانین متخصصین قرار دارد.\n\n"
                        "👇"
                    )

                    send_message(
                        chat_id,
                        reply,
                        inline_button(
                            "📋 مطالعه قوانین متخصصین",
                            SPECIALIST_RULES_URL
                        )
                    )

                    continue

                if text == "🎧 پشتیبانی" or text == "/support":

                    reply = (
                        "🎧 پشتیبانی آنی‌کار\n\n"
                        "مشکل یا سؤال خودت رو همینجا "
                        "بنویس تا راهنمایی‌ات کنم.\n\n"
                        "اگر موضوع مربوط به سفارش هست، "
                        "اطلاعات سفارش و مستندات مرتبط "
                        "رو هم آماده داشته باش."
                    )

                    send_message(
                        chat_id,
                        reply,
                        keyboard
                    )

                    continue

                if text == "❓ سوالات متداول" or text == "/faq":

                    reply = (
                        "❓ سوالات متداول\n\n"
                        "سؤال خودت رو همینجا بنویس.\n\n"
                        "مثلاً:\n"
                        "«آنی‌کار چیه؟»\n"
                        "«چطور سفارش بدم؟»\n"
                        "«چطور متخصص بشم؟»\n"
                        "«پول رو چطور پرداخت کنم؟»\n"
                        "«ضمانت کار چطوره؟»"
                    )

                    send_message(
                        chat_id,
                        reply,
                        keyboard
                    )

                    continue

                if text == "ℹ️ راهنما" or text == "/help":

                    reply = (
                        "ℹ️ راهنمای AnykarHelpBot\n\n"
                        "من می‌تونم درباره این موارد "
                        "راهنمایی‌ات کنم:\n\n"
                        "📝 ثبت سفارش\n"
                        "👨‍🔧 همکاری متخصص\n"
                        "📱 نحوه کار\n"
                        "💰 قیمت خدمات\n"
                        "🛡️ پرداخت و ضمانت\n"
                        "📜 قوانین مشتری\n"
                        "📋 قوانین متخصص\n"
                        "🎧 پشتیبانی\n\n"
                        "💬 حتی لازم نیست از منو استفاده کنی؛ "
                        "سؤالت رو آزادانه بنویس."
                    )

                    send_message(
                        chat_id,
                        reply,
                        keyboard
                    )

                    continue

                # پیام آزاد کاربر
                reply, button = answer(text)

                send_message(
                    chat_id,
                    reply,
                    button if button else keyboard
                )

        time.sleep(1)


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"AnykarHelpBot is running")

    def log_message(self, format, *args):
        return


def start_health_server():
    port = int(os.environ.get("PORT", "10000"))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    print(f"Health server running on port {port}")
    server.serve_forever()


if __name__ == "__main__":
    health_thread = threading.Thread(
        target=start_health_server,
        daemon=True
    )
    health_thread.start()

    print(f"Bale API forced IP: {BALE_NEW_IP}")
    main()
