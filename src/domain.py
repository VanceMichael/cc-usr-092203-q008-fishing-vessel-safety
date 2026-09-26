"""读取并检查项目共享资料。"""

import json
from pathlib import Path

REQUIRED = {
    "domain",
    "version",
    "sample_id",
    "title",
    "actors",
    "facts",
    "records",
    "stages",
    "blocking_scenarios",
    "constraints",
    "escalation",
    "feedback_loop",
}

# 放行判断必须确认的闭环资料类别
REQUIRED_RECORDS = {
    "船舶证照",
    "船员清单",
    "海况预报",
    "动力检查",
    "通信测试",
    "救生衣状态",
    "救生筏状态",
    "缺陷整改与复检",
    "离港许可",
}

# 任何情况下都不得绕过未关闭缺陷的场景
NON_BYPASSABLE_SCENARIOS = {
    "船员临时更换",
    "设备借用",
    "海况预报升级",
    "跨港转场",
    "系统断网离线采集",
}


def load_domain(path: Path) -> dict:
    """读取字段完整且带版本的业务资料。"""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not REQUIRED.issubset(value):
        raise ValueError("共享资料缺少必要字段")
    if value["version"] < 1 or len(value["actors"]) < 2 or len(value["facts"]) < 2:
        raise ValueError("共享资料内容不完整")
    if not REQUIRED_RECORDS.issubset(value["records"]):
        raise ValueError("闭环资料类别不完整")
    if not NON_BYPASSABLE_SCENARIOS.issubset(value["blocking_scenarios"]):
        raise ValueError("阻断场景不完整")
    if not value["feedback_loop"].strip():
        raise ValueError("缺少返港反馈闭环约定")
    return value
