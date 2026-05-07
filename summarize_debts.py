import csv
from collections import defaultdict

def summarize_debts(csv_file):
    customer_totals = defaultdict(float)
    try:
        with open(csv_file, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            fieldnames = [name.strip() for name in (reader.fieldnames or [])]
            if '客户名' not in fieldnames or '欠款金额' not in fieldnames:
                print(f"错误: CSV文件缺少必要的列。当前列名: {fieldnames}")
                return
            for row in reader:
                customer_name = row.get('客户名', '').strip()
                debt_str = row.get('欠款金额', '0').strip()
                if not customer_name:
                    continue
                try:
                    debt_amount = float(debt_str)
                    customer_totals[customer_name] += debt_amount
                except ValueError:
                    print(f"警告: 客户 '{customer_name}' 的金额 '{debt_str}' 不是有效数字，已跳过")
        if customer_totals:
            print("客户欠款汇总:")
            print("-" * 40)
            grand_total = 0
            for customer in sorted(customer_totals.keys()):
                total = customer_totals[customer]
                print(f"{customer}: {total:.2f}")
                grand_total += total
            print("-" * 40)
            print(f"总计: {grand_total:.2f}")
        else:
            print("没有找到有效的欠款记录")
    except FileNotFoundError:
        print(f"错误: 找不到文件 '{csv_file}'")
    except Exception as e:
        print(f"读取文件时发生错误: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("用法: python summarize_debts.py <csv文件路径>")
    else:
        summarize_debts(sys.argv[1])
