import asyncio
import aiohttp
import json
import time
import random
import os


async def send_dingtalk_notification(message):
    """发送钉钉通知。"""
    # 将你的钉钉机器人webhook替换到这里
    webhook_url = ""
    if not webhook_url:
        print("未设置钉钉webhook，跳过通知")
        return

    headers = {"Content-Type": "application/json;charset=utf-8"}
    data = {"msgtype": "text", "text": {"content": message}}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                webhook_url, headers=headers, json=data
            ) as response:
                resp = await response.text()
                print(f"钉钉通知发送结果：{resp}")
        except aiohttp.ClientError as e:
            print(f"钉钉通知发送失败：{e}")


async def check_tickets():
    """检查余票数量并发送通知。"""
    url = ""
    headers = {
        "Connection": "keep-alive",
        "Host-Ip;": "",
        "Authorization": "",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.52(0x18003425) NetType/WIFI Language/zh_CN",
        "Referer": "",
        "content-type": "application/json",
    }
    data = {"commentateId": 6, "scheduleDate": "2024-10-18", "p": "wxmini"}

    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.post(url, headers=headers, json=data) as response:
                    if response.status == 200:
                        try:
                            json_data = await response.json()
                            ticket_amount = json_data["data"]["commentateScheduleMap"][
                                "2024-10-18_0"
                            ][1]["laveTicketAmount"]
                            if ticket_amount != 0:
                                await send_dingtalk_notification(
                                    f"国博讲解有票了！余票数量：{ticket_amount}"
                                )
                                # 可以选择在这里break，或者继续监控
                                # break  # 找到票后停止
                            else:
                                print(
                                    f"暂无余票，{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"
                                )
                        except (KeyError, IndexError, TypeError) as e:
                            print(f"JSON数据解析错误: {e},  返回数据: {json_data}")
                            await send_dingtalk_notification(
                                f"JSON数据解析错误: {e}, 请检查! 返回数据: {json_data}"
                            )

                    else:
                        print(f"请求失败，状态码：{response.status}")
                        await send_dingtalk_notification(
                            f"请求失败，状态码：{response.status}, 请检查!"
                        )

            except aiohttp.ClientError as e:
                print(f"网络请求错误：{e}")
                await send_dingtalk_notification(f"网络请求错误：{e}")

            sleep_time = random.uniform(5, 10)
            print(f"休眠 {sleep_time:.2f} 秒...")
            await asyncio.sleep(sleep_time)


async def main():
    """主函数。"""
    await check_tickets()


if __name__ == "__main__":
    asyncio.run(main())
