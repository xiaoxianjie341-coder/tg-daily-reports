#!/usr/bin/env python3
"""
Pickle Fight Club 群聊日报生成器

标准:
- 分析所有聊天记录文件
- 每个话题 ≥10 条聊天记录
- 话题描述 ≥80 字
"""

import re
import os
import sys

# ============ 标准配置 ============
MIN_CHAT_RECORDS_PER_TOPIC = 10  # 每个话题最少聊天记录
MIN_DESC_LENGTH = 80  # 话题描述最少字数
# =================================

def count_messages_and_users(file_paths):
    """统计所有文件的消息数和唯一用户数"""
    total_msgs = 0
    all_senders = set()

    for f in file_paths:
        try:
            with open(f, 'r', encoding='utf-8') as file:
                content = file.read()
                msg_count = content.count('class="message default')
                total_msgs += msg_count

                senders = re.findall(r'from_name">([^"<]+)', content)
                for s in senders:
                    if s.strip():
                        all_senders.add(s.strip())
        except Exception as e:
            print(f"Warning: 无法读取 {f}: {e}")

    return total_msgs, len(all_senders)

def extract_topic_messages(file_paths, keywords):
    """提取与话题相关的聊天记录"""
    messages = []

    for f in file_paths:
        try:
            with open(f, 'r', encoding='utf-8') as file:
                content = file.read()

                # 提取消息
                pattern = r'<div class="message[^"]*"[^>]*>.*?from_name">([^<]+)</div>.*?<div class="text">([^<]+)'
                matches = re.findall(pattern, content, re.DOTALL)

                for sender, msg in matches:
                    sender = sender.strip()
                    msg = msg.strip().replace('<br>', '\n')
                    msg_lower = msg.lower()

                    for kw in keywords:
                        if kw.lower() in msg_lower:
                            if msg not in [m.split(']: ')[1] if ']: ' in m else '' for m in messages]:
                                messages.append(f"[{sender}]: {msg}")
                            break
        except Exception as e:
            print(f"Warning: 处理 {f} 时出错: {e}")

    return messages

def validate_report(messages_count, users_count, topics_data):
    """验证报告是否符合标准"""
    print("\n" + "="*50)
    print("📊 报告验证报告")
    print("="*50)
    print(f"总消息数: {messages_count}")
    print(f"活跃用户: {users_count}")
    print(f"核心话题: {len(topics_data)}")

    all_valid = True
    for topic_name, msgs in topics_data.items():
        count = len(msgs)
        status = "✅" if count >= MIN_CHAT_RECORDS_PER_TOPIC else "❌"
        print(f"{status} {topic_name}: {count} 条")
        if count < MIN_CHAT_RECORDS_PER_TOPIC:
            all_valid = False

    print("="*50)
    if all_valid:
        print("✅ 报告符合所有标准!")
    else:
        print("⚠️ 报告不符合标准，需要补充内容")
    print()

    return all_valid

# 标准配置
REPORT_STANDARDS = {
    "min_chat_records_per_topic": 10,
    "min_desc_length": 80,
    "required_sections": [
        "活跃度概览",
        "核心热点话题",
        "深度洞察",
        "资源与工具分享"
    ]
}

if __name__ == "__main__":
    print("Pickle Fight Club 群聊日报生成器")
    print(f"标准: 每个话题 ≥{MIN_CHAT_RECORDS_PER_TOPIC} 条聊天记录")
    print(f"标准: 话题描述 ≥{MIN_DESC_LENGTH} 字")
