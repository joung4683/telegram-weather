import random


SUN = [
"""☀️ 오늘의 묵상

맑은 하늘처럼 오늘도 말씀으로
마음을 밝게 채우는 하루가 되길 바랍니다.

📖 시편 119:105
주의 말씀은 내 발의 등이요
내 길의 빛이니이다."""
]


CLOUD = [
"""☁️ 오늘의 묵상

흐린 하늘이 계속되어도
태양은 언제나 그 자리에 있습니다.

우리의 믿음도 환경이 아니라
약속을 바라보는 믿음이 되길 바랍니다.

📖 히브리서 11:1
믿음은 바라는 것들의 실상이요
보이지 않는 것들의 증거니."""
]


RAIN = [
"""🌧 오늘의 묵상

비를 준비하듯
오늘도 말씀으로 하루를 준비합시다.

📖 마태복음 24:42
그러므로 깨어 있으라."""
]


SNOW = [
"""❄️ 오늘의 묵상

새하얀 눈처럼
새로운 마음으로 하루를 시작합시다.

📖 이사야 1:18
너희 죄가 주홍 같을지라도
눈과 같이 희어질 것이요."""
]


def get_message(weather_code):

    if weather_code == 0:
        return random.choice(SUN)

    elif weather_code in [1, 2, 3]:
        return random.choice(CLOUD)

    elif weather_code in [51,53,55,61,63,65,80,81,82]:
        return random.choice(RAIN)

    elif weather_code in [71,73,75,77,85,86]:
        return random.choice(SNOW)

    else:
        return random.choice(CLOUD)