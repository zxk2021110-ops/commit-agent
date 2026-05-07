import os
import re
import json
from openai import OpenAI

# ===== 在这里填你的 DeepSeek API Key =====
DEEPSEEK_API_KEY = "sk-e5a6270a40f54072a1b25a31d0cc6d59"  # ← 替换这里
# ========================================

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

# 读取 commit 数据
file_path = os.path.expanduser("commits.txt")
if os.path.exists(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
else:
    # 备用示例数据
    lines = """d8da64011 Remove Source Files From gitignore
a6975eb50 CLN: remove stale FIXME comments
719314642 DOC: remove cookbook invitation
d5bcc5400 PERF: don't call unique on dtypes
26f6d47c2 BUG: DataFrame.loc setitem-with-expansion""".split('\n')

commits = []
for line in lines:
    line = line.strip()
    if line and not line.startswith('#'):
        parts = line.split(' ', 1)
        if len(parts) == 2:
            commits.append({"hash": parts[0][:7], "msg": parts[1]})

print(f"共读取 {len(commits)} 条 commit")
print("\n前5条预览:")
for c in commits[:5]:
    print(f"  {c['hash']}: {c['msg'][:50]}")

# 调用 DeepSeek 分类
print("\n正在调用 DeepSeek API 分类...")
commit_text = "\n".join([f"{c['hash']}: {c['msg']}" for c in commits])

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是 Git commit 分类专家。将每条 commit 分类为：feat, fix, docs, refactor, perf, test, chore, breaking。只返回 JSON 数组，格式：[{\"hash\":\"xxx\",\"category\":\"feat\"}]"},
        {"role": "user", "content": f"分类以下 commits:\n{commit_text}"}
    ],
    temperature=0.1
)

result = response.choices[0].message.content
result = re.sub(r'^```json\s*', '', result)
result = re.sub(r'\s*```$', '', result)
classifications = json.loads(result)

# 输出结果
print(f"\n分类完成，消耗 {response.usage.total_tokens} tokens\n")
print("=" * 50)
print("分类结果:")
print("=" * 50)

cat_count = {}
for item in classifications:
    cat = item['category']
    cat_count[cat] = cat_count.get(cat, 0) + 1

for cat, count in sorted(cat_count.items(), key=lambda x: -x[1]):
    print(f"  {cat}: {count} 条")

print("\n前10条详情:")
for i, item in enumerate(classifications[:10]):
    commit = commits[i]
    print(f"  {item['hash']} → {item['category']:8} | {commit['msg'][:45]}")