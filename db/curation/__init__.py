"""人工复核数据（curation）的加载器。

`db/curation/*.json` 只放一类东西：**必须由人判断、且以后还会不断增补**的结论。
比如「这条粉丝影像算不算数」「这张图能不能当公演封面」「这场是不是整场辞退」。
抓取/推导逻辑留在 `db/task*.py` 里，结论一律从这里读 —— 改数据不用改代码。

    from curation import load
    V = load('videos')          # -> {'keep': [...], 'reject': [...]}
    KEEP = {x['id'] for x in V['keep']}

文件缺失或不是合法 JSON 时直接抛 SystemExit（带中文说明），
避免脚本静默跑成「什么都没匹配到」。
"""
import json
import os

DIR = os.path.dirname(os.path.abspath(__file__))
_cache = {}


def path(name):
    """`load('videos')` 与 `load('videos.json')` 等价。"""
    return os.path.join(DIR, name if name.endswith('.json') else name + '.json')


def load(name):
    """读取并缓存一份 curation 文件。"""
    if name in _cache:
        return _cache[name]
    p = path(name)
    if not os.path.exists(p):
        raise SystemExit(f'缺少人工复核数据文件：{p}')
    try:
        with open(p, encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise SystemExit(f'{os.path.basename(p)} 不是合法 JSON：第 {e.lineno} 行第 {e.colno} 列 —— {e.msg}')
    if not isinstance(data, dict):
        raise SystemExit(f'{os.path.basename(p)} 顶层必须是对象 {{...}}')
    _cache[name] = data
    return data
