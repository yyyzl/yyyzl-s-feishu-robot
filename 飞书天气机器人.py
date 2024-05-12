import requests
import os


def get_weather():
    # 目标API的URL，请替换为实际的URL
    weather_url = os.environ["WEATHER_URL"]
    # 500100
    # 发起GET请求
    response = requests.get(weather_url)

    # 检查请求是否成功
    if response.status_code == 200:
        # 解析JSON响应
        data = response.json()
        # 获取明天的天气预报
        # 注意：数组索引为0是今天的预报，索引为1才是明天的预报
        tomorrow_forecast = data["result"]["forecasts"][1]
        # 判断明天是否下雨
        is_raining_tomorrow = "雨" in tomorrow_forecast["text_day"]
        current_weather = data["result"]["now"]
        msg = "当前天气状况：\n"
        msg += f"天气：{current_weather['text']}, 实时温度：{current_weather['temp']}℃, 体感温度：{current_weather['feels_like']}℃, 湿度：{current_weather['rh']}%, 风力等级：{current_weather['wind_class']}, 风向：{current_weather['wind_dir']}\n\n"
        msg += f"明天（{tomorrow_forecast['week']}，{tomorrow_forecast['date']}）的天气预报：\n"
        msg += f"白天：{tomorrow_forecast['text_day']}, 高温{tomorrow_forecast['high']}℃, 风力{tomorrow_forecast['wc_day']}\n"
        msg += f"夜晚：{tomorrow_forecast['text_night']}, 低温{tomorrow_forecast['low']}℃, 风力{tomorrow_forecast['wc_night']}"
        send_feishu_msg(msg)
    else:
        send_feishu_msg("请求天气失败")


def send_feishu_msg(msg):
    feishu_url = os.environ["WEBHOOK"]  # 因为$前面是大写所以也是大写

    data = {
	"msg_type": "post",
	"content": {
		"post": {
			"zh_cn": {
				"title": "天气情况通知",
				"content": [
					[{
							"tag": "text",
							"text": msg
						},
						{
							"tag": "a",
							"text": "请查看",
							"href": "https://www.baidu.com/s?wd=%E5%A4%A9%E6%B0%94"
						}
					]
				]
			}
		}
	}
}

    response = requests.post(feishu_url, json=data)


if __name__ == "__main__":
    get_weather()
