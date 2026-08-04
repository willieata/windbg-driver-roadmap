# -*- coding: utf-8 -*-
import os, glob, json, html, sys
try: sys.stdout.reconfigure(encoding='utf-8')
except Exception: pass

D = os.path.dirname(os.path.abspath(__file__))
OUT = r'C:\learning\windbg-driver-roadmap\index.html'

courses = []
for p in glob.glob(os.path.join(D, 'course_*.json')):
    with open(p, encoding='utf-8') as f:
        courses.append(json.load(f))

# order
courses.sort(key=lambda c: c.get('order', 999))

ROUTE_ORDER = ['游戏安全', '全栈安全', '驱动攻防']
ROUTE_LABEL = {
    '游戏安全': 'Route A · 游戏安全',
    '全栈安全': 'Route B · 全栈安全',
    '驱动攻防': 'Route C · 驱动攻防 (内核 · WinDbg 贯穿)',
}
ROUTE_DESC = {
    '游戏安全': 'C/C++ 基础 → 汇编与逆向 → 注入/HOOK/绘制 → 常规逆向 → 虚幻/Unity 引擎实战',
    '全栈安全': '系统化重走:开发篇(C/C++/数据结构/WIN32/GUI) → 逆向篇 → 内核篇',
    '驱动攻防': '保护模式 → 驱动开发 → 系统调用/进程线程 → 异步同步/内核对象/内存管理 → 调试异常(WinDbg/Dump/TTD) → 实战拓展',
}

def esc(s):
    return html.escape(s, quote=True)

# group courses: route -> group -> [courses]
from collections import OrderedDict
tree = OrderedDict()
for c in courses:
    r = c.get('route', '其他')
    g = c.get('group', '其他')
    tree.setdefault(r, OrderedDict()).setdefault(g, []).append(c)

# assign group ids in route/group display order
group_nav = []   # (gid, route, group, course_count, lesson_count)
gid_map = {}
gcount = 0
routes_present = [r for r in ROUTE_ORDER if r in tree] + [r for r in tree if r not in ROUTE_ORDER]

total_lessons = 0
for r in routes_present:
    for g, clist in tree[r].items():
        gcount += 1
        gid = f'g{gcount}'
        gid_map[(r, g)] = gid
        lc = sum(len(ch.get('lessons', [])) for c in clist for ch in c.get('chapters', []))
        total_lessons += lc
        group_nav.append((gid, r, g, len(clist), lc))

# ---- build rail ----
rail = []
cur_route = None
for gid, r, g, ncourse, nles in group_nav:
    if r != cur_route:
        rail.append(f'    <div class="rail-route">{esc(r)}</div>')
        cur_route = r
    rail.append(f'    <a class="frame" href="#{gid}" data-target="{gid}"><span class="fg">{esc(g)}</span><span class="fc">{ncourse}课·{nles}节</span></a>')
rail_html = '\n'.join(rail)

# ---- build main ----
main = []
cur_route = None
for gid, r, g, ncourse, nles in group_nav:
    if r != cur_route:
        main.append(f'''  <div class="route-divider">
    <h2>{esc(ROUTE_LABEL.get(r, r))}</h2>
    <p>{esc(ROUTE_DESC.get(r, ""))}</p>
  </div>''')
        cur_route = r
    main.append(f'  <section class="group" id="{gid}">')
    main.append(f'    <div class="group-head"><h3>{esc(g)}</h3><span class="gmeta">{ncourse} 门课 · {nles} 节</span></div>')
    for c in tree[r][g]:
        cid = c['id']
        cname = c['name']
        chapters = c.get('chapters', [])
        clesn = sum(len(ch.get('lessons', [])) for ch in chapters)
        note = c.get('note')
        main.append(f'    <article class="course" data-course="{cid}">')
        main.append(f'      <div class="course-head">')
        main.append(f'        <a class="course-title" href="https://ferrycofc.com/index/course/show/id/{cid}.html" target="_blank" rel="noopener">{esc(cname)}</a>')
        main.append(f'        <span class="course-prog" data-course-total="{clesn}">0 / {clesn}</span>')
        main.append(f'      </div>')
        if not chapters or clesn == 0:
            msg = esc(note or '目录未取得')
            main.append(f'      <div class="empty">（{msg}；上线后补充目录）</div>')
        else:
            idx = 0
            for ch in chapters:
                ct = ch.get('title', '课程目录')
                lessons = ch.get('lessons', [])
                if not lessons:
                    continue
                main.append(f'      <div class="chapter"><span class="chapter-title">{esc(ct)}</span><span class="chapter-n">{len(lessons)}</span></div>')
                main.append(f'      <ul class="lessons">')
                for ls in lessons:
                    lid = f'L{cid}_{idx}'
                    idx += 1
                    if isinstance(ls, dict):
                        ltitle = ls.get('t') or ls.get('title') or ''
                        res = ls.get('r') or ls.get('res') or []
                    else:
                        ltitle = ls; res = []
                    reshtml = ''
                    if res:
                        items = ''.join(f'<li><a href="{esc(u)}" target="_blank" rel="noopener">{esc(n)}</a></li>' for n, u in res)
                        reshtml = f'<div class="lres"><span class="lres-h">学习资料</span><ul>{items}</ul></div>'
                    hasres = ' has-res' if res else ''
                    main.append(f'        <li class="lesson{hasres}" data-id="{lid}">')
                    main.append(f'          <span class="dot" title="标记完成"></span>')
                    main.append(f'          <span class="lt">{esc(ltitle)}</span>')
                    main.append(f'          <button class="lx" type="button" aria-label="展开笔记与资料">＋</button>')
                    main.append(f'          <div class="lpanel">{reshtml}<div class="lnote" data-note-id="{lid}"></div></div>')
                    main.append(f'        </li>')
                main.append(f'      </ul>')
        # per-course note placeholder
        main.append(f'      <div class="course-note" data-note-id="NC{cid}"></div>')
        main.append(f'    </article>')
    main.append('  </section>')
main_html = '\n'.join(main)

ncourses = len(courses)
ngroups = len(group_nav)

PAGE = f'''<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ferry 课程目录 · 学习路线 — {ncourses} 门课 / {total_lessons} 节</title>
<style>
:root{{
  --bg:#0b0f14; --panel:#111823; --panel2:#0e141d; --line:#1e2a38;
  --ink:#d6e0ea; --dim:#8aa0b4; --cyan:#38bdf8; --amber:#f5b301;
  --green:#3ddc84; --red:#ff5c5c; --violet:#a78bfa;
}}
*{{box-sizing:border-box}}
html,body{{margin:0;background:var(--bg);color:var(--ink);font:14px/1.6 "Segoe UI","Microsoft JhengHei",system-ui,sans-serif}}
a{{color:var(--cyan);text-decoration:none}}
.topbar{{position:sticky;top:0;z-index:20;display:flex;align-items:center;gap:16px;
  padding:10px 18px;background:rgba(11,15,20,.92);backdrop-filter:blur(6px);border-bottom:1px solid var(--line)}}
.topbar h1{{font-size:15px;margin:0;color:var(--ink);font-weight:600;white-space:nowrap}}
.topbar h1 span{{color:var(--amber)}}
.prog-wrap{{flex:1;display:flex;align-items:center;gap:10px;min-width:120px}}
.bar{{flex:1;height:8px;background:var(--panel);border:1px solid var(--line);border-radius:6px;overflow:hidden}}
.bar > i{{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--cyan),var(--green));transition:width .3s}}
.prog-txt{{color:var(--dim);white-space:nowrap;font-variant-numeric:tabular-nums}}
.prog-txt b{{color:var(--green)}}
.btns{{display:flex;gap:8px}}
.btns button{{background:var(--panel);color:var(--ink);border:1px solid var(--line);border-radius:6px;
  padding:6px 12px;cursor:pointer;font-size:12px}}
.btns button:hover{{border-color:var(--cyan);color:var(--cyan)}}
.layout{{display:grid;grid-template-columns:230px 1fr;gap:0;align-items:start}}
.rail{{position:sticky;top:49px;height:calc(100vh - 49px);overflow:auto;
  padding:14px 10px;background:var(--panel2);border-right:1px solid var(--line)}}
.rail-route{{color:var(--amber);font-size:11px;letter-spacing:1px;text-transform:uppercase;
  margin:14px 6px 6px;font-weight:700}}
.frame{{display:flex;justify-content:space-between;align-items:center;gap:8px;
  padding:6px 8px;border-radius:6px;color:var(--ink);border:1px solid transparent}}
.frame:hover{{background:var(--panel);border-color:var(--line)}}
.frame.active{{background:var(--panel);border-color:var(--cyan)}}
.frame .fg{{font-size:13px}}
.frame .fc{{font-size:10px;color:var(--dim);white-space:nowrap}}
main{{padding:0 26px 80px;max-width:1000px}}
.hero{{padding:26px 0 8px}}
.hero h2{{margin:0 0 8px;font-size:22px}}
.hero p{{margin:4px 0;color:var(--dim)}}
.hero .primary{{margin-top:14px;padding:12px 14px;background:var(--panel);border:1px solid var(--line);
  border-left:3px solid var(--amber);border-radius:6px}}
.hero .primary a{{color:var(--amber)}}
.aux{{margin-top:10px;padding:10px 14px;background:var(--panel2);border:1px solid var(--line);border-radius:6px;color:var(--dim);font-size:13px}}
.aux a{{color:var(--cyan)}}
.route-divider{{margin:34px 0 10px;padding:14px 16px;border-radius:8px;
  background:linear-gradient(90deg,var(--panel),transparent);border-left:3px solid var(--cyan)}}
.route-divider h2{{margin:0;font-size:18px;color:var(--cyan)}}
.route-divider p{{margin:4px 0 0;color:var(--dim);font-size:13px}}
.group{{margin:18px 0 8px;scroll-margin-top:60px}}
.group-head{{display:flex;align-items:baseline;gap:10px;padding:6px 0;border-bottom:1px solid var(--line);margin-bottom:10px}}
.group-head h3{{margin:0;font-size:16px;color:var(--amber)}}
.gmeta{{color:var(--dim);font-size:12px}}
.course{{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:12px 14px;margin:12px 0}}
.course-head{{display:flex;align-items:center;gap:10px;justify-content:space-between}}
.course-title{{font-size:15px;font-weight:600;color:var(--ink);border-bottom:1px dashed var(--line)}}
.course-title:hover{{color:var(--cyan);border-bottom-color:var(--cyan)}}
.course-prog{{font-size:11px;color:var(--dim);font-variant-numeric:tabular-nums;white-space:nowrap;
  padding:2px 8px;border:1px solid var(--line);border-radius:10px}}
.course-prog.full{{color:var(--green);border-color:var(--green)}}
.chapter{{display:flex;align-items:center;gap:8px;margin:12px 0 4px}}
.chapter-title{{color:var(--violet);font-size:13px;font-weight:600}}
.chapter-n{{color:var(--dim);font-size:11px}}
.chapter::after{{content:"";flex:1;height:1px;background:var(--line)}}
.lessons{{list-style:none;margin:0;padding:0;display:block}}
.lesson{{display:flex;flex-wrap:wrap;align-items:center;gap:8px;padding:4px 6px;border-radius:5px;color:var(--dim)}}
.lesson:hover{{background:var(--panel2)}}
.lesson .dot{{flex:none;width:12px;height:12px;border-radius:50%;border:2px solid var(--dim);cursor:pointer;transition:.15s}}
.lesson .dot:hover{{border-color:var(--red)}}
.lesson .lt{{flex:1;min-width:0;font-size:12.5px;cursor:pointer}}
.lesson.done{{color:var(--ink)}}
.lesson.done .dot{{background:var(--red);border-color:var(--red);box-shadow:0 0 6px rgba(255,92,92,.6)}}
.lesson.done .lt{{text-decoration:line-through;text-decoration-color:var(--dim)}}
.lx{{flex:none;width:22px;height:22px;line-height:20px;text-align:center;padding:0;
  background:none;border:1px solid var(--line);border-radius:5px;color:var(--dim);cursor:pointer;font-size:14px}}
.lx:hover{{color:var(--cyan);border-color:var(--cyan)}}
.lesson.has-res .lx{{color:var(--amber);border-color:var(--amber)}}
.lesson.noted .lx{{color:var(--green);border-color:var(--green)}}
.lpanel{{display:none;flex-basis:100%;width:100%;margin:6px 0 6px 20px;padding:10px 12px;
  background:var(--panel2);border:1px solid var(--line);border-left:2px solid var(--cyan);border-radius:6px}}
.lesson.open .lpanel{{display:block}}
.lres{{margin-bottom:8px}}
.lres-h{{display:block;color:var(--amber);font-size:11px;letter-spacing:.5px;margin-bottom:4px}}
.lres ul{{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:6px 12px}}
.lres li a{{display:inline-block;font-size:12px;padding:3px 9px;background:var(--panel);
  border:1px solid var(--line);border-radius:12px;color:var(--cyan)}}
.lres li a:hover{{border-color:var(--cyan)}}
.lnote-area{{width:100%;background:var(--panel);color:var(--ink);border:1px solid var(--line);
  border-radius:6px;padding:7px 9px;font:12.5px/1.5 inherit;resize:vertical;min-height:56px}}
.empty{{color:var(--dim);font-size:12px;padding:8px 0}}
.course-note{{margin-top:10px}}
.note-toggle{{background:none;border:1px dashed var(--line);color:var(--dim);border-radius:6px;
  padding:4px 10px;font-size:11px;cursor:pointer}}
.note-toggle:hover{{color:var(--amber);border-color:var(--amber)}}
.note-toggle.has{{color:var(--amber);border-color:var(--amber);border-style:solid}}
.note-area{{width:100%;margin-top:8px;background:var(--panel2);color:var(--ink);border:1px solid var(--line);
  border-radius:6px;padding:8px 10px;font:13px/1.5 inherit;resize:vertical;min-height:70px}}
.hint{{position:fixed;bottom:16px;right:16px;background:var(--panel);border:1px solid var(--line);
  color:var(--dim);padding:8px 12px;border-radius:6px;font-size:12px;opacity:0;transition:.3s;pointer-events:none}}
.hint.show{{opacity:1}}
@media(max-width:820px){{.layout{{grid-template-columns:1fr}}.rail{{display:none}}}}
</style>
</head>
<body>
<div class="topbar">
  <h1>Ferry <span>课程目录</span> 学习路线</h1>
  <div class="prog-wrap">
    <div class="bar"><i id="barfill"></i></div>
    <span class="prog-txt"><b id="doneN">0</b> / {total_lessons} 节 · <span id="pct">0%</span></span>
  </div>
  <div class="btns">
    <button id="btnExport">导出备份</button>
    <button id="btnImport">导入备份</button>
    <input id="fileImport" type="file" accept="application/json" hidden>
  </div>
</div>
<div class="layout">
  <nav class="rail">
{rail_html}
  </nav>
  <main>
    <div class="hero">
      <h2>以 ferrycofc 课程目录重建的学习路线</h2>
      <p>{ncourses} 门课 · {ngroups} 个模块 · 共 {total_lessons} 个小节,全部按各课程真实「课程目录」逐节铺开,从零基础起步。</p>
      <div class="primary">主线以 <a href="https://ferrycofc.com/index/course/learn" target="_blank" rel="noopener">Ferry 学院课程</a> 为骨干;点击每门课标题可跳到该课程详情页。勾选小节即记录进度(圆点为 WinDbg 断点样式),每门课可写一则笔记,顶栏可导出/导入备份。</p>
      <div class="aux">辅助资源:<a href="https://bbs.kanxue.com/thread-51839.htm" target="_blank" rel="noopener">看雪学习路线</a> · 看雪论坛 <a href="https://bbs.kanxue.com/" target="_blank" rel="noopener">bbs.kanxue.com</a> · 微软官方文档(WinDbg / WDK)作内核阶段配套。</div>
    </div>
{main_html}
  </main>
</div>
<div class="hint" id="hint"></div>
<script>
(function(){{
  var NS='windbg-driver-roadmap-full';
  var K_PROG=NS+':progress', K_NOTE=NS+':notes';
  var hasArt = typeof window.storage!=='undefined';
  function get(k){{return hasArt? window.storage.getItem(k): localStorage.getItem(k);}}
  function set(k,v){{if(hasArt) window.storage.setItem(k,v); else localStorage.setItem(k,v);}}

  var done = new Set();
  try{{var a=JSON.parse(get(K_PROG)||'[]'); if(Array.isArray(a)) a.forEach(function(x){{done.add(x);}});}}catch(e){{}}
  var notes = {{}};
  try{{notes=JSON.parse(get(K_NOTE)||'{{}}')||{{}};}}catch(e){{}}

  var lessons = Array.prototype.slice.call(document.querySelectorAll('.lesson'));
  var total = lessons.length;

  function saveProg(){{set(K_PROG, JSON.stringify(Array.from(done)));}}
  function saveNotes(){{set(K_NOTE, JSON.stringify(notes));}}

  function updateHeader(){{
    var n=done.size;
    document.getElementById('doneN').textContent=n;
    var pct= total? Math.round(n/total*100):0;
    document.getElementById('pct').textContent=pct+'%';
    document.getElementById('barfill').style.width=pct+'%';
  }}
  function updateCourse(art){{
    var items=art.querySelectorAll('.lesson');
    var tot=items.length, d=0;
    items.forEach(function(li){{ if(li.classList.contains('done')) d++; }});
    var badge=art.querySelector('.course-prog');
    if(badge){{ badge.textContent=d+' / '+tot; badge.classList.toggle('full', tot>0 && d===tot); }}
  }}

  // init lessons
  function markNoted(li,id){{ li.classList.toggle('noted', !!(notes[id]&&String(notes[id]).trim())); }}
  function ensureNote(li){{
    var box=li.querySelector('.lnote');
    if(!box || box.dataset.ready) return;
    box.dataset.ready='1';
    var id=box.getAttribute('data-note-id');
    var ta=document.createElement('textarea');
    ta.className='lnote-area';
    ta.placeholder='这一节的笔记 / 疑问 / 补充链接…';
    if(notes[id]) ta.value=notes[id];
    var t=null;
    ta.addEventListener('input',function(){{
      clearTimeout(t);
      t=setTimeout(function(){{ notes[id]=ta.value; saveNotes(); markNoted(li,id); }},400);
    }});
    box.appendChild(ta);
  }}
  lessons.forEach(function(li){{
    var id=li.getAttribute('data-id');
    if(done.has(id)) li.classList.add('done');
    markNoted(li,id);
    li.querySelector('.dot').addEventListener('click',function(e){{
      e.stopPropagation();
      if(li.classList.toggle('done')) done.add(id); else done.delete(id);
      saveProg(); updateHeader(); updateCourse(li.closest('.course'));
    }});
    function toggle(){{ li.classList.toggle('open'); if(li.classList.contains('open')) ensureNote(li); }}
    li.querySelector('.lt').addEventListener('click',toggle);
    li.querySelector('.lx').addEventListener('click',toggle);
  }});
  document.querySelectorAll('.course').forEach(updateCourse);
  updateHeader();

  // notes per course
  document.querySelectorAll('.course-note').forEach(function(box){{
    var id=box.getAttribute('data-note-id');
    var btn=document.createElement('button');
    btn.className='note-toggle';
    var ta=document.createElement('textarea');
    ta.className='note-area'; ta.style.display='none';
    ta.placeholder='为这门课写点笔记(重点 / 卡点 / 参考链接)…';
    function refresh(){{
      var has=!!(notes[id]&&notes[id].trim());
      btn.textContent=(ta.style.display==='none'? '笔记 ':'收起 ')+(has?'●':'＋');
      btn.classList.toggle('has',has);
    }}
    if(notes[id]) ta.value=notes[id];
    btn.addEventListener('click',function(){{
      ta.style.display= ta.style.display==='none'?'block':'none';
      if(ta.style.display==='block') ta.focus();
      refresh();
    }});
    var t=null;
    ta.addEventListener('input',function(){{
      clearTimeout(t);
      t=setTimeout(function(){{ notes[id]=ta.value; saveNotes(); refresh(); }},400);
    }});
    box.appendChild(btn); box.appendChild(ta); refresh();
  }});

  // rail active on scroll
  var links=Array.prototype.slice.call(document.querySelectorAll('.frame'));
  var secs=links.map(function(a){{return document.getElementById(a.getAttribute('data-target'));}});
  function onScroll(){{
    var y=window.scrollY+120, best=-1;
    for(var i=0;i<secs.length;i++){{ if(secs[i]&&secs[i].offsetTop<=y) best=i; }}
    links.forEach(function(a,i){{ a.classList.toggle('active', i===best); }});
  }}
  window.addEventListener('scroll',onScroll,{{passive:true}}); onScroll();

  // hint
  var hint=document.getElementById('hint'), ht=null;
  function toast(m){{ hint.textContent=m; hint.classList.add('show'); clearTimeout(ht); ht=setTimeout(function(){{hint.classList.remove('show');}},2200); }}

  // export
  document.getElementById('btnExport').addEventListener('click',function(){{
    var data={{format:'windbg-driver-roadmap-backup',version:1,exportedAt:new Date().toISOString(),
      progress:Array.from(done),notes:notes}};
    var blob=new Blob([JSON.stringify(data,null,2)],{{type:'application/json'}});
    var url=URL.createObjectURL(blob), a=document.createElement('a');
    a.href=url; a.download='roadmap-backup.json'; a.click(); URL.revokeObjectURL(url);
    toast('已导出备份');
  }});
  // import
  var fi=document.getElementById('fileImport');
  document.getElementById('btnImport').addEventListener('click',function(){{fi.click();}});
  fi.addEventListener('change',function(){{
    var f=fi.files[0]; if(!f) return;
    var r=new FileReader();
    r.onload=function(){{
      try{{
        var d=JSON.parse(r.result);
        if(d.format!=='windbg-driver-roadmap-backup') throw 0;
        done=new Set(Array.isArray(d.progress)?d.progress:[]);
        notes=d.notes&&typeof d.notes==='object'?d.notes:{{}};
        saveProg(); saveNotes();
        toast('已导入,正在刷新…');
        setTimeout(function(){{location.reload();}},600);
      }}catch(e){{ toast('备份格式不符,已略过'); }}
      fi.value='';
    }};
    r.readAsText(f);
  }});
}})();
</script>
</body>
</html>
'''

with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
    f.write(PAGE)

print('courses:', ncourses, 'groups:', ngroups, 'lessons:', total_lessons)
print('routes:', routes_present)
for gid,r,g,nc,nl in group_nav:
    print(f'  {gid} {r}/{g}: {nc} courses, {nl} lessons')
