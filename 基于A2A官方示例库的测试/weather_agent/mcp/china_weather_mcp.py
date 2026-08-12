"""FastMCP server for China weather forecasts backed by Open-Meteo."""

from datetime import date, datetime
from typing import Any

import httpx

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("china_weather")

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
MAX_FORECAST_DAYS = 16

WEATHER_CODE_MAP = {
    0: "晴",
    1: "基本晴朗",
    2: "少云",
    3: "阴",
    45: "雾",
    48: "雾凇",
    51: "毛毛雨",
    53: "小毛毛雨",
    55: "大毛毛雨",
    56: "冻毛毛雨",
    57: "强冻毛毛雨",
    61: "小雨",
    63: "中雨",
    65: "大雨",
    66: "冻雨",
    67: "强冻雨",
    71: "小雪",
    73: "中雪",
    75: "大雪",
    77: "雪粒",
    80: "小阵雨",
    81: "中阵雨",
    82: "强阵雨",
    85: "小阵雪",
    86: "大阵雪",
    95: "雷阵雨",
    96: "雷阵雨伴冰雹",
    99: "强雷阵雨伴冰雹",
}


def _weather_label(code: Any) -> str:
    if code is None:
        return "未知"
    return WEATHER_CODE_MAP.get(int(code), f"未知天气代码({code})")


def _num(value: Any, unit: str = "") -> str:
    if value is None:
        return "-"
    return f"{value}{unit}"


def _forecast_window() -> tuple[date, date]:
    """Returns the inclusive date window supported by the forecast provider."""
    first_date = date.today()
    last_date = first_date.fromordinal(
        first_date.toordinal() + MAX_FORECAST_DAYS - 1
    )
    return first_date, last_date


async def _geocode(city: str, province: str) -> tuple[float, float, str] | None:
    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.get(
            GEOCODE_URL,
            params={"name": city, "count": 10, "language": "zh", "format": "json"},
        )
        response.raise_for_status()
        results = response.json().get("results", [])

    cn_results = [r for r in results if r.get("country_code") == "CN"]
    if not cn_results:
        return None

    if province:
        for result in cn_results:
            admin1 = result.get("admin1", "") or ""
            if province in admin1 or admin1 in province:
                return (
                    float(result["latitude"]),
                    float(result["longitude"]),
                    admin1,
                )

    best = cn_results[0]
    return (
        float(best["latitude"]),
        float(best["longitude"]),
        best.get("admin1", "") or "",
    )


@mcp.tool()
async def get_daily_forecast(
    city: str, province: str, start_date: str, end_date: str
) -> str:
    """Get the daily weather forecast for a Chinese city over a date range.

    Args:
        city: The city name in Chinese, e.g. 北京, 上海, 杭州.
        province: The province or municipality name in Chinese, e.g. 北京市,
            上海, 浙江省. Can be an empty string when unambiguous.
        start_date: The first forecast date in YYYY-MM-DD format.
        end_date: The last forecast date in YYYY-MM-DD format.
    """
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        return "日期格式错误，请使用 YYYY-MM-DD。"

    first_date, last_date = _forecast_window()
    supported_range = (
        f"当前日期：{first_date.isoformat()}；"
        f"可查询预报日期范围：{first_date.isoformat()} 至 "
        f"{last_date.isoformat()}（含首尾日期，共 {MAX_FORECAST_DAYS} 天）。"
    )

    if start > end:
        return (
            f"日期范围无效：开始日期 {start.isoformat()} 晚于结束日期 "
            f"{end.isoformat()}。{supported_range}"
        )
    if start < first_date or end > last_date:
        return (
            f"请求日期 {start.isoformat()} 至 {end.isoformat()} 超出天气预报可查询范围。"
            f"{supported_range}"
        )

    location = await _geocode(city, province)
    if location is None:
        return f"未找到中国城市：{city} {province}。请检查城市名和省/直辖市名。"

    latitude, longitude, admin = location
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": (
            "weather_code,temperature_2m_max,temperature_2m_min,"
            "precipitation_probability_max,precipitation_sum,wind_speed_10m_max"
        ),
        "timezone": "Asia/Shanghai",
        "start_date": start_date,
        "end_date": end_date,
    }

    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.get(FORECAST_URL, params=params)
        response.raise_for_status()
        data = response.json()

    daily = data.get("daily", {})
    days = daily.get("time", [])
    codes = daily.get("weather_code", [])
    temp_max = daily.get("temperature_2m_max", [])
    temp_min = daily.get("temperature_2m_min", [])
    precip_prob = daily.get("precipitation_probability_max", [])
    precip_sum = daily.get("precipitation_sum", [])
    wind = daily.get("wind_speed_10m_max", [])

    lines = [f"城市: {city}（{admin}） 预报日期: {start_date} 至 {end_date}", ""]
    for index, day in enumerate(days):
        if index >= len(codes):
            break
        weather = _weather_label(codes[index])
        high = temp_max[index] if index < len(temp_max) else None
        low = temp_min[index] if index < len(temp_min) else None
        prob = precip_prob[index] if index < len(precip_prob) else None
        amount = precip_sum[index] if index < len(precip_sum) else None
        speed = wind[index] if index < len(wind) else None

        suitable = (
            amount == 0
            and prob is not None
            and prob < 50
            and low is not None
            and high is not None
            and 10 <= low
            and high <= 30
        )
        lines.append(
            f"{day}: {weather}，最高 {_num(high, '°C')}，最低 {_num(low, '°C')}，"
            f"降水概率 {_num(prob, '%')}，降水量 {_num(amount, 'mm')}，"
            f"最大风速 {_num(speed, 'km/h')}，适合出行: {'是' if suitable else '否'}"
        )

    lines.append("")
    lines.append(
        "适合出行判定标准：无降水、降水概率低于 50%、"
        "最低温不低于 10°C 且最高温不高于 30°C。"
    )
    return "\n".join(lines)


if __name__ == "__main__":
    mcp.run(transport="stdio")
