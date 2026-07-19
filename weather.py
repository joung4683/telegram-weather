from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from weather_card import create_weather_card

from apscheduler.schedulers.asyncio import AsyncIOScheduler

import requests


TOKEN = "8058281661:AAFKDra1SZj_U1JXXqxRLHZ7Hpuid8IzCVY"

CHAT_ID = -1003284680807

THREAD_ID = 4



def get_faith_message(weather_code, temp, rain):

    if rain >= 50 or weather_code >= 50:
        return (
            "내리는 빗방울처럼 하나님의 은혜가 "
            "마음에 차곡차곡 내려와 평안과 위로가 가득한 하루 되세요 🙏\n"
            "비 오는 순간에도 하나님께서 함께하심을 기억하며 "
            "감사로 걸어가는 하루 되세요."
        )

    elif weather_code in [0, 1]:
        return (
            "맑은 하늘처럼 우리의 마음도 감사와 기쁨으로 "
            "밝게 채워지는 하루 되세요 🙏\n"
            "오늘 허락된 모든 순간 속에서 하나님의 인도하심을 "
            "느끼는 복된 하루 되세요."
        )

    elif temp >= 30:
        return (
            "무더운 날씨 속에서도 지치지 않고 "
            "믿음의 열정과 감사의 마음이 식지 않는 하루 되세요 🙏\n"
            "몸과 마음 모두 건강하게 지키며 맡겨진 자리에서 "
            "기쁨으로 걸어가는 하루 되세요."
        )

    elif temp <= 5:
        return (
            "차가운 날씨 속에서도 하나님의 사랑 안에서 "
            "따뜻한 위로와 힘을 얻는 하루 되세요 🙏\n"
            "오늘도 변함없는 은혜 가운데 평안하게 "
            "하루를 보내시길 바랍니다."
        )

    else:
        return (
            "하나님께서 허락하신 오늘 하루, "
            "감사와 평안 가운데 힘차게 걸어가는 하루 되세요 🙏\n"
            "작은 순간에도 하나님의 은혜를 발견하며 "
            "기쁨으로 살아가는 하루 되세요."
        )



def get_weather_feature(temp, feel, rain, compare_text):

    if feel >= 33:
        return (
            f"{compare_text}\n"
            "체감온도가 높아 무더위와 온열질환에 주의가 필요합니다.\n"
            "물을 자주 마시고 충분한 휴식으로 건강을 잘 챙겨주세요."
        )

    elif rain >= 50:
        return (
            f"{compare_text}\n"
            "비 소식이 있어 외출 시 우산을 준비해주세요.\n"
            "도로가 미끄러울 수 있으니 이동 시 안전에 유의해주세요."
        )

    elif temp >= 28:
        return (
            f"{compare_text}\n"
            "더운 날씨가 예상되어 수분 섭취가 필요합니다.\n"
            "장시간 야외 활동 시 무리하지 않도록 주의해주세요."
        )

    elif temp <= 10:
        return (
            f"{compare_text}\n"
            "기온이 낮아 외출 시 따뜻한 옷차림이 좋겠습니다.\n"
            "건강 관리에 유의하며 따뜻한 하루 보내세요."
        )

    else:
        return (
            f"{compare_text}\n"
            "비교적 쾌적한 날씨로 활동하기 좋은 하루입니다.\n"
            "가벼운 산책과 야외 활동을 즐기기 좋은 날씨입니다."
        )



def get_weather():

    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=37.1326"
        "&longitude=128.1928"
        "&models=ecmwf_ifs025"
        "&current=temperature_2m,apparent_temperature,weather_code"
        "&daily=temperature_2m_max,temperature_2m_min,"
        "apparent_temperature_max,precipitation_probability_max"
        "&past_days=1"
        "&timezone=Asia%2FSeoul"
    )


    response = requests.get(url)

    data = response.json()


    current = data["current"]

    daily = data["daily"]


    temp = round(current["temperature_2m"])

    feel = round(current["apparent_temperature"])


    weather_code = current["weather_code"]


    today_max = round(
        daily["temperature_2m_max"][0]
    )


    today_min = round(
        daily["temperature_2m_min"][0]
    )


    yesterday_feel = round(
        daily["apparent_temperature_max"][1]
    )


    rain = daily["precipitation_probability_max"][0]
    feel_diff = feel - yesterday_feel


    if feel_diff >= 3:

        compare_text = (
            "어제보다 더 덥게 느껴지는 날씨입니다."
        )

    elif feel_diff <= -3:

        compare_text = (
            "어제보다 선선하게 느껴지는 날씨입니다."
        )

    else:

        compare_text = (
            "어제와 비슷한 날씨가 이어집니다."
        )



    weather_text = (
        f"현재기온 : {temp}°\n"
        f"체감온도 : {feel}°\n"
        f"최고기온 : {today_max}°\n"
        f"최저기온 : {today_min}°\n"
        f"강수확률 : {rain}%"
    )



    feature = get_weather_feature(
        temp,
        feel,
        rain,
        compare_text
    )



    faith = get_faith_message(
        weather_code,
        temp,
        rain
    )



    return (
        weather_text,
        weather_code,
        compare_text,
        feature,
        faith,
        rain,
        today_max,
        today_min
    )





async def send_weather_to_chat(app):

    (
        weather_text,
        weather_code,
        compare_text,
        feature,
        faith,
        rain,
        today_max,
        today_min
    ) = get_weather()



    image = await create_weather_card(
        weather_text,
        weather_code,
        compare_text,
        rain,
        today_max,
        today_min
    )



    caption = (
        "🌤 <b>오늘의 제천 날씨</b>\n\n"
        f"📌 <b>날씨 특징</b>\n"
        f"{feature}\n\n"
        f"🙏 <b>오늘의 마음</b>\n"
        f"{faith}"
    )



    with open(image, "rb") as photo:

        await app.bot.send_photo(
    chat_id=CHAT_ID,
    message_thread_id=THREAD_ID,
    photo=photo,
    caption=caption,
    parse_mode="HTML"
)





async def weather_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    (
        weather_text,
        weather_code,
        compare_text,
        feature,
        faith,
        rain,
        today_max,
        today_min
    ) = get_weather()



    image = await create_weather_card(
        weather_text,
        weather_code,
        compare_text,
        rain,
        today_max,
        today_min
    )



    caption = (
        "🌤 <b>오늘의 제천 날씨</b>\n\n"
        f"📌 <b>날씨 특징</b>\n"
        f"{feature}\n\n"
        f"🙏 <b>오늘의 마음</b>\n"
        f"{faith}"
    )



    with open(image, "rb") as photo:

        await update.message.reply_photo(
            photo=photo,
            caption=caption,
            parse_mode="HTML"
        )





async def sendnow_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await send_weather_to_chat(
        context.application
    )


    await update.message.reply_text(
        "✅ 활동공유방 테스트 전송 완료"
    )





async def chatid_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        f"Chat ID : {update.effective_chat.id}"
    )





async def start_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "🌤 제천 날씨 알림봇입니다.\n\n"
        "/weather - 현재 날씨 확인\n"
        "/sendnow - 활동공유방 테스트 전송"
    )
def main():

    app = Application.builder().token(
        TOKEN
    ).build()



    app.add_handler(
        CommandHandler(
            "start",
            start_command
        )
    )



    app.add_handler(
        CommandHandler(
            "weather",
            weather_command
        )
    )



    app.add_handler(
        CommandHandler(
            "chatid",
            chatid_command
        )
    )



    app.add_handler(
        CommandHandler(
            "sendnow",
            sendnow_command
        )
    )



    async def post_init(application):

        scheduler = AsyncIOScheduler()


        scheduler.add_job(
            send_weather_to_chat,
            "cron",
            hour=8,
            minute=0,
            args=[application]
        )


        scheduler.start()


        print(
            "⏰ 매일 오전 8시 자동 전송 예약 완료"
        )



    app.post_init = post_init



    print(
        "🌤 제천 날씨 봇 실행 중..."
    )



    app.run_polling()





if __name__ == "__main__":

    main()