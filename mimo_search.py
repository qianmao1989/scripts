import os, sys, json, requests

def mimo_search(query, max_results=5, force_search=True):
    """MiMo native web search via API"""
    key = os.environ.get('MIMO_SEARCH_KEY') or os.environ.get('XIAOMI_API_KEY')
    if not key:
        return {'error': 'MIMO_SEARCH_KEY not set'}

    resp = requests.post(
        'https://api.xiaomimimo.com/v1/chat/completions',
        headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'},
        json={
            'model': 'mimo-v2.5-pro',
            'messages': [{'role': 'user', 'content': query}],
            'tools': [{'type': 'web_search', 'max_keyword': 3, 'force_search': force_search, 'limit': max_results}],
            'tool_choice': 'auto',
            'max_completion_tokens': 1024,
            'thinking': {'type': 'disabled'}
        },
        timeout=30
    )

    if resp.status_code != 200:
        return {'error': f'HTTP {resp.status_code}', 'detail': resp.text[:300]}

    d = resp.json()
    msg = d['choices'][0]['message']
    return {
        'content': msg['content'],
        'citations': [
            {'title': a.get('title',''), 'url': a.get('url',''), 'summary': a.get('summary','')}
            for a in (msg.get('annotations') or [])
        ],
        'usage': d['usage'].get('web_search_usage', {})
    }

if __name__ == '__main__':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    query = sys.argv[1] if len(sys.argv) > 1 else '今天上海天气'
    result = mimo_search(query)
    print(json.dumps(result, indent=2, ensure_ascii=False))
