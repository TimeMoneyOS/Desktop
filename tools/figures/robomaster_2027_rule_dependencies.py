from pathlib import Path
from html import escape
out=Path(__file__).resolve().parents[2] / 'docs/assets/robomaster-2027';out.mkdir(parents=True,exist_ok=True)
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="650" viewBox="0 0 1080 650" role="img" aria-labelledby="title desc">','<title id="title">2027 规则关键依赖关系</title><desc id="desc">装配解锁重装重火力，阵地影响控制度与胜负，基地血量影响后勤，雷达连接命中与装甲加固。</desc>','<defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="8" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8" fill="#527078"/></marker></defs>','<rect width="1080" height="650" rx="20" fill="#f4f8fa"/>','<g font-family="Microsoft YaHei,Noto Sans CJK SC,sans-serif"><text x="42" y="52" font-size="28" font-weight="700" fill="#143b45">2027：装配、控图、信息形成联动</text><text x="42" y="84" font-size="16" fill="#526b74">规则关系示意 · 非对局仿真 · 对应正文各章节</text>']
def box(x,y,w,h,title,lines,color):
 svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="white" stroke="{color}" stroke-width="2"/>')
 svg.append(f'<rect x="{x}" y="{y+12}" width="5" height="{h-24}" fill="{color}"/>')
 svg.append(f'<text x="{x+20}" y="{y+34}" font-size="21" font-weight="700" fill="#143b45">{escape(title)}</text>')
 for i,line in enumerate(lines):svg.append(f'<text x="{x+20}" y="{y+64+i*25}" font-size="16" fill="#3d5560">{escape(line)}</text>')
def arrow(x1,y1,x2,y2):svg.append(f'<path d="M{x1} {y1} L{x2} {y2}" stroke="#527078" stroke-width="2.5" fill="none" marker-end="url(#arrow)"/>')
box(40,120,290,130,'科技核心装配',['持续金币、重装等级','三级装配解锁 42mm 使用权'],'#008577')
box(395,120,290,130,'工作台与重装火力',['另有差值相关时间解锁路径','安装、确认后投入重火力'],'#008577')
box(750,120,290,130,'基地血量与后勤',['血量降低 → 后勤系数降低','回血、复活、通信、图传受影响'],'#c46e32')
box(40,325,290,125,'阵地争夺',['前哨阵地 / 基地阵地','临时控制与完全控制'],'#347bb3')
box(395,325,290,125,'累计控制度',['同时控制两个前哨：+1/秒','同时控制两个基地：+3/秒'],'#347bb3')
box(750,325,290,125,'胜负判定',['基地均存活，到时先比控制度','基地击毁仍可提前结束比赛'],'#347bb3')
box(40,515,290,100,'命中位置与精度',['命中率、散布、区域反馈'],'#8a5eb5')
box(395,515,290,100,'雷达加固决策',['选择全队装甲加固中心'],'#8a5eb5')
box(750,515,290,100,'自适应装甲',['加固区 ×0.5 / 未加固区 ×1.5'],'#8a5eb5')
arrow(330,185,395,185);arrow(685,185,750,185);arrow(330,388,395,388);arrow(685,388,750,388);arrow(330,565,395,565);arrow(685,565,750,565)
svg.append('</g></svg>');(out/'rule-dependencies.svg').write_text('\n'.join(svg),encoding='utf-8')
