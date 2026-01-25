# 导入 selenium 核心模块
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from datetime import datetime, timedelta, timezone

# ==================== 配置区（用户交互式输入）====================
print("=" * 50)
print("        🚄 12306 智能抢票助手")
print("=" * 50)

# 基础信息输入
Init = input("\n📍 请输入出发站（如：北京）: ").strip()
Dest = input("\n📍 请输入目的地（如：上海）: ").strip()
Departure_time = input("\n📅 请输入出发日期（格式：2026-01-01）: ").strip()

# 选择车次
target_train = input("\n🚄 请输入你要预订的车次（例如：G1786、G1234）：").strip()

# 座位类型配置
print("\n💺 可选座位类型：")
print("   1-商务座  2-一等座  3-二等座  4-软卧  5-硬卧  6-硬座")
seat_choice = input("   请选择座位类型（可多选，用逗号分隔，如：3,2 表示选择二等座和一等座）: ").strip()

# 座位映射
SEAT_MAP = {
    "1": ("cc_seat_type_9_check", "商务座"),
    "2": ("cc_seat_type_M_check", "一等座"),
    "3": ("cc_seat_type_O_check", "二等座"),
    "4": ("cc_seat_type_4_check", "软卧"),
    "5": ("cc_seat_type_3_check", "硬卧"),
    "6": ("cc_seat_type_1_check", "硬座")
}

# 解析座位选择
SEAT_SELECTIONS = []
SEAT_NAMES = []
for choice in seat_choice.split(','):
    choice = choice.strip()
    if choice in SEAT_MAP:
        seat_id, seat_name = SEAT_MAP[choice]
        SEAT_SELECTIONS.append(seat_id)
        SEAT_NAMES.append(seat_name)

# 如果没有输入座位，默认选择二等座
if not SEAT_SELECTIONS:
    SEAT_SELECTIONS = ["cc_seat_type_O_check"]
    SEAT_NAMES = ["二等座"]

# 选择乘车人及座位分配
print("\n👴 乘车人座位分配规则：")
print("   输入顺序决定座位位置：")
print("   第1个数字 → C座")
print("   第2个数字 → B座")
print("   第3个数字 → A座")
print("   第4个数字 → D座")
print("   第5个数字 → F座")

user_input = input("\n请输入乘车人序号（多个序号用空格分隔）：").strip()
passenger_nums_str = user_input.split()
valid_passenger_range = [1, 2, 3, 4, 5]

# 座位分配映射
SEAT_POSITION_MAP = {0: "C", 1: "B", 2: "A", 3: "D", 4: "F"}

passenger_seat_assignments = []
for idx, num_str in enumerate(passenger_nums_str):
    try:
        passenger_num = int(num_str)
        if passenger_num in valid_passenger_range:
            seat_letter = SEAT_POSITION_MAP.get(idx, "")
            passenger_seat_assignments.append({
                'passenger_num': passenger_num,
                'seat_letter': seat_letter,
                'seat_name': seat_letter if seat_letter else "未指定"
            })
    except ValueError:
        pass

# 显示配置摘要
print("\n" + "=" * 50)
print("📋 配置确认:")
print(f"   出发站: {Init}")
print(f"   目的地: {Dest}")
print(f"   日期: {Departure_time}")
print(f"   车次: {target_train}")
print(f"   座位类型: {', '.join(SEAT_NAMES)}")
print(f"   乘车人座位分配：")
for assignment in passenger_seat_assignments:
    print(f"      乘车人{assignment['passenger_num']} → {assignment['seat_name']}座")
print("=" * 50)

input("\n✅ 确认配置无误，按回车继续...")

# ==================== 定时抢票设置（仅记录时间）====================
timing_choice = input("\n是否需要定时抢票？(Y/N): ").strip().upper()
target_time = None
BEIJING_TZ = timezone(timedelta(hours=8))

if timing_choice == "Y":
    print("\n📌 请输入开始抢票的时间（北京时间 HH:MM:SS）")
    while True:
        time_input = input("⏰ 请输入抢票时间: ").strip()
        try:
            target_hour, target_minute, target_second = map(int, time_input.split(':'))
            now = datetime.now(BEIJING_TZ)
            target_time = now.replace(hour=target_hour, minute=target_minute, second=target_second, microsecond=0)
            if target_time <= now:
                target_time += timedelta(days=1)
            print(f"✅ 定时成功！目标：{target_time.strftime('%H:%M:%S')}")
            break
        except ValueError:
            print("❌ 格式错误，请重新输入")

input("\n🚀 确认无误，按回车启动浏览器并登录...")

# ==================== 自动化执行区 ====================
driver = webdriver.Chrome()
driver.maximize_window()

try:
    # 2-4. 登录流程
    driver.get("https://www.12306.cn")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "J-btn-login"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[text()="扫码登录"]'))).click()
    print("📱 请在手机端扫码...")
    
    input("\n✅ 登录完成后，按回车开始自动跳转...")
    driver.get("https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc")
    
    # 5. 输入查询参数
    init_button = driver.find_element(By.ID, "fromStationText")
    init_button.click()
    init_button.send_keys(Init + Keys.ENTER)
    
    dest_button = driver.find_element(By.ID, "toStationText")
    dest_button.click()
    dest_button.send_keys(Dest + Keys.ENTER)
    
    time_button = driver.find_element(By.ID, "train_date")
    time_button.click()
    time_button.clear()
    time_button.send_keys(Departure_time + Keys.ENTER)
    time.sleep(0.5)
    
    # 6. 点击查询
    driver.find_element(By.ID, "query_ticket").click()
    time.sleep(1)

    # 7. 选择座位类型（筛选条件）
    print(f"\n💺 正在勾选座位筛选条件...")
    for seat_id in SEAT_SELECTIONS:
        try:
            seat_checkbox = driver.find_element(By.ID, seat_id)
            if not seat_checkbox.is_selected():
                seat_checkbox.click()
        except:
            pass

    # ==================== 核心修改：在此处进行定时等待 ====================
    if timing_choice == "Y" and target_time:
        print("\n" + "—" * 30)
        print("⏳ 筛选条件已就绪，正在等待开售时刻...")
        try:
            while datetime.now(BEIJING_TZ) < target_time:
                remaining = (target_time - datetime.now(BEIJING_TZ)).total_seconds()
                if remaining > 0:
                    print(f"\r🕒 距离开抢还有: {int(remaining // 3600):02d}:{int((remaining % 3600) // 60):02d}:{int(remaining % 60):02d}", end="", flush=True)
                    time.sleep(0.5) # 频率略微提高，增加准时度
                else:
                    break
            print("\n\n🎯 时间到！正在执行秒杀预订...")
        except KeyboardInterrupt:
            print("\n\n⚠️ 用户手动跳过等待，立即开始抢票！")
    else:
        print("\n✅ 即时抢票模式，开始预订...")
    # ====================================================================

    # 8. 再次点击查询（刷新票态）并点击预定
    driver.find_element(By.ID, "query_ticket").click() 
    for seat_id in SEAT_SELECTIONS:
        try:
            seat_checkbox = driver.find_element(By.ID, seat_id)
            if not seat_checkbox.is_selected():
                seat_checkbox.click()
        except:
            pass
    book_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f'//a[@class="btn72" and contains(@onclick, "{target_train}")]')))
    book_button.click()

    # 9. 勾选乘车人
    print("\n💺 正在勾选乘车人...")
    for assignment in passenger_seat_assignments:
        passenger_num = assignment['passenger_num']
        passenger_id = f"normalPassenger_{passenger_num - 1}"
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, passenger_id))).click()
    
    # 10. 提交订单
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "submitOrder_id"))).click()
    time.sleep(0.5)
    
    # 11. 选择座位
    print("\n🚉 正在智能分配座位...")
    for assignment in passenger_seat_assignments:
        seat_letter = assignment.get('seat_letter', '')
        if seat_letter:
            success = False
            for row in ['1', '2']:
                try:
                    elem = driver.find_element(By.ID, f"{row}{seat_letter}")
                    if "disabled" not in (elem.get_attribute("class") or "").lower():
                        driver.execute_script("arguments[0].click();", elem)
                        success = True
                        break
                except:
                    continue
    
    # 12. 点击确认提交
    time.sleep(0.5)
    #input("\n🤚 return to continue...")
    print("\n✅ 正在提交最终确认...")
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "qr_submit_id"))).click()
    print("\n🎉 座位分配完成！请在页面上检查并完成支付。")

    # 保持浏览器打开，让用户可以查看结果或继续操作
    input("\n🚪 按回车关闭浏览器...")

except (TimeoutException, NoSuchElementException) as e:
    print(f"\n❌ 操作失败！错误原因：{e}")
except KeyboardInterrupt:
    print("\n\n⚠️  用户手动停止程序")
except Exception as e:
    print(f"\n❌ 出现未知错误！错误原因：{e}")
finally:
    driver.quit()
    print("✅ 浏览器已成功关闭！")