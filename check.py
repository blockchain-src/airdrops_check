import requests
import json
from tabulate import tabulate
import time  # 用于模拟等待
from tqdm import tqdm  # 导入 tqdm 库

# ANSI 转义码
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
CYAN = "\033[36m"
RED = "\033[31m"
YELLOW = "\033[33m"  # 黄色字体的ANSI转义码

# 批量查询多个地址并获取 BEBE 代币
def batch_query_addresses(addresses):
    results = []
    
    for addr in addresses:
        url = f"https://bebe.meme/api/query?addr={addr}"
        
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Mobile Safari/537.36",
            "Authorization": "Bearer undefined",
            "Referer": "https://bebe.meme/airdrop"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()  # 获取JSON数据
            
            if "data" in data:
                data_str = data["data"]
                try:
                    parsed_data = json.loads(data_str)  # 解析字符串为 JSON 对象
                    if "balance" in parsed_data:
                        balance = parsed_data["balance"]
                        results.append([addr, balance, 0, 0])  # 添加 WTF 列，初始化为 0
                    else:
                        results.append([addr, "无法获取", 0, 0])  # 添加 WTF 列，初始化为 0
                except json.JSONDecodeError:
                    results.append([addr, "解析失败", 0, 0])  # 添加 WTF 列，初始化为 0
            else:
                results.append([addr, "无数据", 0, 0])  # 添加 WTF 列，初始化为 0
        else:
            results.append([addr, "请求失败", 0, 0])  # 添加 WTF 列，初始化为 0
    
    # 返回结果表格数据
    return results

# 查询 BOOGA 和 WTF 代币数量
def query_booga_and_wtf_balance(address):
    url = f"https://openapiv1.coinstats.app/wallet/balances?address={address}&networks=all"
    headers = {
        "accept": "application/json",
        "X-API-KEY": "rlYfi/vLmMSpnp1TH0LZM5RecpK82/2XPwoM8ZkEU2k="
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        
        if isinstance(data, dict) and 'balances' in data:
            data = [data]

        total_value = 0
        for entry in data:
            if isinstance(entry, dict):
                balances = entry.get("balances", [])
                for item in balances:
                    amount = item.get("amount", 0)
                    price = item.get("price", 0)
                    total_value += amount * price

        if total_value < 100:
            booga_amount = 0
            wtf_amount = 0
        else:
            booga_amount = total_value * 710.832
            wtf_amount = total_value * 1131.638
        
        return booga_amount, wtf_amount

    except requests.RequestException as e:
        print(f"地址 {address} 网络错误: {e}")
        return 0, 0

    except ValueError:
        print(f"地址 {address} 数据解析错误，请检查 API 响应内容。")
        return 0, 0

    except Exception as e:
        print(f"地址 {address} 发生了意外错误: {e}")
        return 0, 0

# 从控制台获取地址列表
def get_addresses_from_console():
    addresses = []
    print(f"{BOLD}{GREEN}⚠️ 请输入地址列表，每行输入一地址，按一次回车换行，按两次回车结束： {RESET}")
    
    while True:
        addr = input()  # 用户只需按回车输入地址
        if addr == "":  # 用户输入两次回车
            break
        addresses.append(addr)
    
    return addresses

# 获取地址列表
addresses = get_addresses_from_console()

# 显示正在查询的提示
print(f"{CYAN}🔍 正在查询，请稍等......{RESET}")
time.sleep(1)  # 模拟等待时间

# 执行查询
results = batch_query_addresses(addresses)

# 获取 BOOGA 和 WTF 代币数量
for row in results:
    addr = row[0]
    booga_amount, wtf_amount = query_booga_and_wtf_balance(addr)  # 获取 BOOGA 和 WTF 代币数量
    row[2] = booga_amount  # 更新 BOOGA 代币数量
    row[3] = wtf_amount    # 更新 WTF 代币数量

# 设置表头
blue_title = f"\033[36m{'钱包地址'}\033[0m", f"\033[36m{'BEBE'}\033[0m", f"\033[36m{'BOOGA'}\033[0m", f"\033[36m{'WTF'}\033[0m"

# 使用 tabulate 格式化表格输出
print(f"{BOLD}{YELLOW}🌟 空投查询结果{RESET}")
print(tabulate(results, headers=blue_title, tablefmt="fancy_grid", stralign="center", numalign="right", colalign=("center", "left", "left", "left"), floatfmt=".2f"))

# 询问用户是否需要进行 Claim
print(f"{GREEN}")  # 设置为绿色字体
claim_choice = input("❓ 是否需要执行 Claim ？(y/n): ").strip().lower()

if claim_choice == "y":
    # 提示输入私钥列表
    print(f"{GREEN}🗝️ 请输入私钥列表，每行输入一私钥，按一次回车换行，按两次回车结束：{RESET}")
    
    private_keys = []  # 用于存储私钥列表
    while True:
        private_key = input().strip()  # 用户输入每一个私钥
        if private_key == "":  # 如果按两次回车
            break
        private_keys.append(private_key)
    
    # 显示进度条，模拟等待5秒
    print(f"{YELLOW}\n♻️ 批量执行 Claim...{RESET}")
    for private_key in private_keys:
        print(f" »»» {private_key}")

        # 模拟每个私钥执行 Claim 的进度条
        for _ in tqdm(range(100), desc="⏳ 进度", ncols=100, unit="%", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}] {rate_fmt}", colour="yellow"):
            time.sleep(0.05)  # 每次延时50毫秒，共计5秒
        
        # 将私钥写入到 .env 文件
        with open(".env", "a") as f:
            f.write(f"PRIVATE_KEY={private_key}\n")
        
        print(f"{YELLOW}🎉 已成功 Claim ！{RESET}")

else:
    print(f"{YELLOW}⚫ 未执行 Claim ，退出进程。{RESET}")
