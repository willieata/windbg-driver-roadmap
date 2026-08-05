# -*- coding: utf-8 -*-
"""串行低频抓取 ferrycofc 课程目录,回填 build/course_<id>.json 的 chapters。

用法: python build/fetch_catalog.py [id ...]
不给 id 时,自动抓所有 chapters 为空的课程(id=36 已下架,跳过)。

注意: 并发抓取会触发「访问次数过多」验证码并黏性封锁 IP,务必保持串行 + 间隔。
"""
import os, re, sys, json, glob, time, html, random
import urllib.request

try: sys.stdout.reconfigure(encoding='utf-8')
except Exception: pass

D = os.path.dirname(os.path.abspath(__file__))
URL = 'https://ferrycofc.com/index/course/show/id/{}.html'
UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')
SKIP = {36}          # 已下架,无目录
DELAY = (9, 16)      # 每门课之间的随机间隔(秒)

CHAPTER_RE = re.compile(
    r'<div class="chapterbox">(.*?)</ul>', re.S)
TIT_RE = re.compile(r'<p class="chapterTit[^"]*">.*?<span>(.*?)</span>', re.S)
LESSON_RE = re.compile(r'<li[^>]*data-ids="\d+".*?<span>(.*?)</span>', re.S)


def clean(s):
    s = re.sub(r'<[^>]+>', '', s)
    s = html.unescape(s).replace('\xa0', ' ')
    return ' '.join(s.split())


def fetch(cid):
    req = urllib.request.Request(URL.format(cid), headers={
        'User-Agent': UA,
        'Accept': 'text/html,application/xhtml+xml',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    })
    return urllib.request.urlopen(req, timeout=30).read().decode('utf-8', 'replace')


def parse(page):
    chapters = []
    for block in CHAPTER_RE.findall(page):
        m = TIT_RE.search(block)
        title = clean(m.group(1)) if m else '课程目录'
        lessons = [clean(x) for x in LESSON_RE.findall(block)]
        lessons = [x for x in lessons if x]
        if lessons:
            chapters.append({'title': title, 'lessons': lessons})
    return chapters


def targets():
    if len(sys.argv) > 1:
        return [int(x) for x in sys.argv[1:]]
    out = []
    for p in sorted(glob.glob(os.path.join(D, 'course_*.json'))):
        d = json.load(open(p, encoding='utf-8'))
        if d['id'] in SKIP:
            continue
        if not sum(len(c.get('lessons', [])) for c in d.get('chapters', [])):
            out.append((d.get('order', 999), d['id']))
    out.sort()
    return [i for _, i in out]


def main():
    ids = targets()
    print(f'待抓 {len(ids)} 门: {ids}', flush=True)
    ok = fail = 0
    for n, cid in enumerate(ids, 1):
        path = os.path.join(D, f'course_{cid}.json')
        try:
            page = fetch(cid)
        except Exception as e:
            print(f'[{n}/{len(ids)}] id={cid} 请求失败: {e}', flush=True)
            fail += 1
            time.sleep(random.uniform(*DELAY))
            continue
        if '次数过多' in page or 'captcha' in page.lower():
            print(f'[{n}/{len(ids)}] id={cid} 被限流/验证码,中止', flush=True)
            break
        chapters = parse(page)
        if not chapters:
            print(f'[{n}/{len(ids)}] id={cid} 未解析到目录(可能已下架)', flush=True)
            fail += 1
        else:
            d = json.load(open(path, encoding='utf-8'))
            d['chapters'] = chapters
            d.pop('note', None)
            with open(path, 'w', encoding='utf-8', newline='\n') as f:
                json.dump(d, f, ensure_ascii=False, indent=2)
                f.write('\n')
            nl = sum(len(c['lessons']) for c in chapters)
            print(f'[{n}/{len(ids)}] id={cid} {d["name"]}: {len(chapters)} 章 / {nl} 节 ✓', flush=True)
            ok += 1
        if n < len(ids):
            time.sleep(random.uniform(*DELAY))
    print(f'完成: 成功 {ok} / 失败 {fail}', flush=True)


if __name__ == '__main__':
    main()
