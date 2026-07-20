# weather_card.py 새 최종본 1/3

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os
import re


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.join(BASE_DIR, "assets")


FONT_DIR = os.path.join(BASE_DIR, "fonts")

FONT_REGULAR = os.path.join(
    FONT_DIR,
    "Pretendard-Regular.otf"
)

FONT_MEDIUM = os.path.join(
    FONT_DIR,
    "Pretendard-Medium.otf"
)

FONT_BOLD = os.path.join(
    FONT_DIR,
    "Pretendard-Bold.otf"
)

FONT_EXTRA = os.path.join(
    FONT_DIR,
    "Pretendard-ExtraBold.otf"
)


W = 1080
H = 1350


def get_font(path, size):
    return ImageFont.truetype(path, size)



def get_weather_message(temp, feel, rain):

    if rain >= 30:
        return (
            "비 오는 날",
            "외출 시 우산을 준비하세요"
        )

    elif feel >= 33 or temp >= 33:
        return (
            "폭염 주의",
            "더위 조심하세요"
        )

    elif feel >= 28 or temp >= 28:
        return (
            "더운 하루",
            "수분 섭취하세요"
        )

    elif temp >= 23:
        return (
            "쾌적한 날씨",
            "활동하기 좋은 날입니다"
        )

    elif temp >= 15:
        return (
            "선선한 날씨",
            "가벼운 겉옷 추천"
        )

    elif temp >= 5:
        return (
            "쌀쌀한 날씨",
            "외투를 챙겨주세요"
        )

    else:
        return (
            "추운 날씨",
            "따뜻하게 입으세요"
        )



def select_background(weather_code):

    if weather_code in [0, 1]:
        filename = "sunny.png"

    elif weather_code in [2, 3]:
        filename = "cloudy.png"

    elif weather_code in [71,73,75,77,85,86]:
        filename = "snow.png"

    else:
        filename = "rain.png"


    return os.path.join(
        ASSET_DIR,
        filename
    )



def resize_background(path):

    img = Image.open(path).convert("RGB")

    ratio = max(
        W / img.width,
        H / img.height
    )

    img = img.resize(
        (
            int(img.width * ratio),
            int(img.height * ratio)
        )
    )

    left = (img.width - W) // 2
    top = (img.height - H) // 2

    return img.crop(
        (
            left,
            top,
            left + W,
            top + H
        )
    )



def center(draw, text, y, font, color):

    box = draw.textbbox(
        (0, 0),
        text,
        font=font
    )

    x = (W - (box[2] - box[0])) / 2

    draw.text(
        (x, y),
        text,
        font=font,
        fill=color
    )
# weather_card.py 새 최종본 2/3


async def create_weather_card(
    weather_text,
    weather_code,
    compare_text,
    rain,
    today_max,
    today_min
):

    lines = weather_text.split("\n")


    def extract(text):

        nums = re.findall(
            r"\d+",
            text
        )

        return int(nums[0]) if nums else 0



    temp = extract(lines[0])
    feel = extract(lines[1])


    state, advice = get_weather_message(
        temp,
        feel,
        rain
    )



    img = resize_background(
        select_background(weather_code)
    ).convert(
        "RGBA"
    )



    # 전체 어둡기

    overlay = Image.new(
        "RGBA",
        (W, H),
        (0, 0, 0, 70)
    )


    img = Image.alpha_composite(
        img,
        overlay
    )



    # 메인 흰색 카드

    card_layer = Image.new(
        "RGBA",
        (W, H),
        (0,0,0,0)
    )


    card_draw = ImageDraw.Draw(
        card_layer
    )


    card_draw.rounded_rectangle(
        (
            90,
            160,
            990,
            1180
        ),
        radius=75,
        fill=(255,255,255,165)
    )


    img = Image.alpha_composite(
        img,
        card_layer
    )


    draw = ImageDraw.Draw(
        img
    )



    # 폰트

    brand_font = get_font(
        FONT_BOLD,
        38
    )


    date_font = get_font(
        FONT_MEDIUM,
        32
    )


    title_font = get_font(
        FONT_BOLD,
        58
    )


    temp_font = get_font(
        FONT_EXTRA,
        210
    )


    state_font = get_font(
        FONT_BOLD,
        54
    )


    compare_font = get_font(
        FONT_MEDIUM,
        32
    )


    advice_font = get_font(
        FONT_MEDIUM,
        34
    )


    info_label_font = get_font(
        FONT_BOLD,
        32
    )


    info_value_font = get_font(
        FONT_EXTRA,
        48
    )


    footer_font = get_font(
        FONT_BOLD,
        32
    )



    today = datetime.now().strftime(
        "%Y.%m.%d"
    )



    draw.text(
        (90,75),
        "JECHON YOUTH",
        font=brand_font,
        fill="white"
    )


    draw.text(
        (850,80),
        today,
        font=date_font,
        fill="white"
    )



    center(
        draw,
        "오늘의 제천 날씨",
        250,
        title_font,
        (35,55,85)
    )



    center(
        draw,
        f"{temp}°",
        360,
        temp_font,
        (20,90,220)
    )



    center(
        draw,
        state,
        640,
        state_font,
        (40,60,85)
    )



    center(
        draw,
        compare_text,
        720,
        compare_font,
        (80,100,120)
    )



    center(
        draw,
        advice,
        765,
        advice_font,
        (100,115,135)
    )



    # 정보 박스 레이어

    info_layer = Image.new(
        "RGBA",
        (W,H),
        (0,0,0,0)
    )


    info_draw = ImageDraw.Draw(
        info_layer
    )



    cards = [
        ("체감", f"{feel}°", 170, 870),
        ("최고", f"{today_max}°", 630, 870),
        ("최저", f"{today_min}°", 170, 1010),
        ("강수", f"{rain}%", 630, 1010),
    ]



    for label, value, x, y in cards:

        info_draw.rounded_rectangle(
            (
                x,
                y,
                x+280,
                y+120
            ),
            radius=28,
            fill=(255,255,255,130)
        )



        label_box = info_draw.textbbox(
            (0,0),
            label,
            font=info_label_font
        )


        label_x = x + (
            280 - (label_box[2]-label_box[0])
        ) / 2



        info_draw.text(
            (
                label_x,
                y+12
            ),
            label,
            font=info_label_font,
            fill=(90,100,120)
        )



        value_box = info_draw.textbbox(
            (0,0),
            value,
            font=info_value_font
        )


        value_x = x + (
            280 - (value_box[2]-value_box[0])
        ) / 2



        info_draw.text(
            (
                value_x,
                y+55
            ),
            value,
            font=info_value_font,
            fill=(40,60,90)
        )



    img = Image.alpha_composite(
        img,
        info_layer
    )


    draw = ImageDraw.Draw(
        img
    )
# weather_card.py 새 최종본 3/3


    # 하단 문구

    center(
        draw,
        "제천청년회 오늘 하루도 파이팅!",
        1260,
        footer_font,
        "white"
    )



    output = os.path.join(
        BASE_DIR,
        "weather_card.png"
    )



    img.convert(
        "RGB"
    ).save(
        output
    )



    return output