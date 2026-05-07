import json, requests

key = 'sk-cbs7udgj9na0bqsbxwjlpf4mtrffyyngc6yx2th4cf1gnbdi'

resp = requests.post(
    'https://api.xiaomimimo.com/v1/chat/completions',
    headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'},
    json={
        'model': 'mimo-v2.5-pro',
        'messages': [{'role': 'user', 'content': '今天上海天气怎么样'}],
        'tools': [{'type': 'web_search', 'max_keyword': 3, 'force_search': True, 'limit': 3}],
        'tool_choice': 'auto',
        'max_completion_tokens': 512,
        'thinking': {'type': 'disabled'}
    },
    timeout=30
)
print(f'Status: {resp.status_code}')
d = resp.json()
if 'error' in d:
    print(f"Error: {d['error']}")
else:
    print('=== 搜索结果 ===')
    print(d['choices'][0]['message']['content'][:800])
    print()
    print('=== 引用 ===')
    for a in d['choices'][0]['message'].get('annotations') or []:
        print(f"  - {a.get('title','')}: {a.get('url','')}")
    print()
    print('=== 用量 ===')
    print(json.dumps(d['usage'].get('web_search_usage', {}), indent=2, ensure_ascii=False))
