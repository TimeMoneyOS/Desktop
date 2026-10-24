"""DM VQF teaching diagrams. Curve data: ideal integration + desktop example CSV.

Run with Python + NumPy + Matplotlib from any working directory.
No sensor/hardware access; SVG diagrams retain editable text and paths.
"""
from pathlib import Path
from html import escape
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parents[2] / 'docs/assets/dm-imu-vqf'
OUT.mkdir(parents=True, exist_ok=True)


def start(width, height, title, desc):
    return [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>
<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8" fill="none" stroke="#45636c" stroke-width="1.5"/></marker></defs>
<rect width="100%" height="100%" fill="#ffffff"/>
<g font-family="Microsoft YaHei,Noto Sans CJK SC,Arial,sans-serif" fill="#193b43">''']


def text(svg, x, y, value, size=22, anchor='middle', color='#193b43', weight='normal'):
    svg.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" fill="{color}" font-weight="{weight}">{escape(value)}</text>')


def box(svg, x, y, w, h, lines, fill='#e7f3ef'):
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="#6c9998" stroke-width="1.5"/>')
    top = y + h/2 - (len(lines)-1)*16 + 8
    for n, line in enumerate(lines):
        text(svg, x+w/2, top+32*n, line, 22 if n == 0 else 19)


def arrow(svg, points, dashed=False):
    dash = ' stroke-dasharray="8 6"' if dashed else ''
    svg.append(f'<polyline points="{points}" fill="none" stroke="#45636c" stroke-width="2" marker-end="url(#arrow)"{dash}/>')


def save(svg, name):
    svg.append('</g></svg>')
    (OUT / (name+'.svg')).write_text('\n'.join(svg), encoding='utf-8')


s = start(1100, 1070, '一帧六轴解算的实际顺序', '安全检查后依次进行陀螺检测、积分、加速度检测、倾角校正、偏置更新；新偏置反馈到下一帧。')
text(s, 550, 42, '一帧采样：姿态更新与偏置反馈', 30, weight='bold')
rows = [
    (80, ['dm_vqf_update()', 'gyro：rad/s；acc：m/s²；拒绝空指针与 NaN/Inf']),
    (210, ['① check_gyro_rest()', 'restBias 或 magDist 开启时：低通、变化量、幅度检查']),
    (340, ['② integrate_gyro()', '减去当前 bias → 旋转增量 → qG 右乘并归一化']),
    (470, ['③ check_acc_rest()', '静止估计开启时：加速度稳定检测、累计持续时间']),
    (600, ['④ correct_inclination()', 'qG 旋转加速度 → 低通 → 用 qA 校正倾斜']),
    (730, ['⑤ update_bias()', '准备 H/e/W → 预测 P → 有观测时更新 bias/P']),
    (860, ['输出 q = qA ⊗ qG', 'get_quaternion / get_euler 只读出结果，不推进状态']),
]
for i, (y, lines) in enumerate(rows):
    box(s, 70, y, 720, 90, lines, '#e7f3ef' if i != 5 else '#fff0dc')
    if i < len(rows)-1:
        arrow(s, f'430,{y+90} 430,{y+130}')
box(s, 830, 330, 230, 112, ['bias 反馈', '新估计作用于', '下一帧陀螺积分'], '#fff0dc')
arrow(s, '790,775 1075,775 1075,385 1060,385', True)
arrow(s, '830,385 790,385', True)
text(s, 808, 458, 'acc 全零：积分后返回', 19, 'start')
text(s, 808, 699, '两种偏置估计', 18, 'start')
text(s, 808, 725, '均关闭：跳过⑤', 18, 'start')
text(s, 70, 1000, '执行顺序决定状态含义：本帧积分使用旧 bias，运动残差保留倾角校正前的方向。', 21, 'start')
text(s, 70, 1035, '安全接口检查一次；核心函数不重复检查。图示省略数学辅助函数内部循环。', 19, 'start')
save(s, 'update-flow')

s = start(1100, 580, 'qG 和 qA 连接的三个坐标系', '机体系向量经 qG 进入近惯性系，再经 qA 进入六轴参考系；加速度在近惯性系低通。')
text(s, 550, 45, '两个四元数：把快速旋转与慢速倾角修正分开', 29, weight='bold')
box(s, 45, 100, 270, 120, ['机体系 B', '随 IMU 转动', 'aBody、gyro、bias'])
box(s, 415, 100, 270, 120, ['近惯性系 I', '由去偏陀螺积分维持', '允许缓慢积分误差'])
box(s, 785, 100, 270, 120, ['六轴参考系 E', '+Z 对齐重力参考', '水平无绝对北向'])
arrow(s, '315,160 415,160'); text(s, 365, 133, 'R(qG)', 21)
arrow(s, '685,160 785,160'); text(s, 735, 133, 'R(qA)', 21)
box(s, 60, 330, 260, 95, ['aI = R(qG) aBody', '先抵消机体旋转'], '#e8eef9')
box(s, 420, 330, 260, 95, ['aI_LP = LP(aI)', '近惯性系二阶低通'], '#e8eef9')
box(s, 780, 330, 260, 95, ['gPre = normalize(', 'R(qA_old) aI_LP )'], '#e8eef9')
arrow(s, '320,378 420,378'); arrow(s, '680,378 780,378')
text(s, 550, 495, '最终 q = qA ⊗ qG；倾角校正左乘 qA，陀螺增量右乘 qG。', 23)
text(s, 550, 539, '低通可抑制较快线性加速度；持续加速度仍可能污染重力方向。', 21)
save(s, 'frames')

s = start(1100, 750, '两种偏置观测进入三状态 Kalman 更新', '先维护矩阵与旋转偏置的低通历史，静止观测优先，否则使用启用的运动观测；无观测仍预测协方差。')
text(s, 550, 44, '偏置估计：先构造观测，再计算相信多少', 29, weight='bold')
box(s, 180, 80, 740, 90, ['先维护 LP(R) 与 LP((R bias)水平分量)', '静止期间也维护历史；R 来自本帧倾角校正后的姿态'], '#e8eef9')
arrow(s, '400,170 280,230'); arrow(s, '700,170 820,230')
box(s, 40, 230, 480, 160, ['静止且开启静止估计：优先', 'H = I；e = gyroLP − bias', '三轴使用 Wrest', '假设真实角速度约为零'])
box(s, 580, 230, 480, 160, ['否则，开启运动估计', 'H = LP(R)；水平残差来自倾角误差', 'W = diag(Wmotion,Wmotion,Wvertical)', '竖直弱约束不能给出绝对航向'], '#fff0dc')
arrow(s, '280,390 280,440 550,440 550,480')
arrow(s, '820,390 820,440 550,440')
box(s, 140, 480, 820, 110, ['三状态偏置更新：bx、by、bz', '先预测 P；有观测时 K = P Hᵀ (H P Hᵀ + W)⁻¹', 'bias += K e；P -= K H P；最后偏置限幅'])
text(s, 550, 646, '无可用观测：只预测 P；两种估计都关闭：整个更新器不执行。', 21)
text(s, 550, 691, 'Kalman 状态不包含四元数；姿态由独立的积分与倾角校正路径维护。', 21)
save(s, 'bias-observation')

plt.rcParams.update({'font.sans-serif': ['Microsoft YaHei', 'SimHei'],
                     'axes.unicode_minus': False, 'svg.fonttype': 'none',
                     'svg.hashsalt': 'dm-vqf-teaching', 'font.size': 11})
with (OUT/'example_result.csv').open(encoding='utf-8-sig', newline='') as f:
    records = list(csv.DictReader(f))
t = np.array([float(r['time_s']) for r in records])
yaw = np.array([float(r['yaw_deg']) for r in records])
bias = np.array([float(r['bias_z_deg_s']) for r in records])
assert len(t) == 60 and t[-1] == 60
assert np.isclose(3/3600, 0.0008333333333333334)
fig, axes = plt.subplots(1, 2, figsize=(13, 5.5), layout='constrained')
h = np.linspace(0, 1, 101)
for drift, color in [(3, '#d67735'), (0.36, '#327e77')]:
    axes[0].plot(h, h*drift, label=f'{drift:g} °/h（残偏 {drift/3600:.6g} °/s）', color=color, linewidth=2)
axes[0].set(xlabel='时间 / h', ylabel='理想航向误差 / °', title='A. 教学计算：常值残余偏置的积分')
axes[0].legend(loc='upper left', fontsize=9); axes[0].grid(alpha=.25)
axes[1].plot(t, yaw, color='#327e77', linewidth=2, label='yaw / °（左轴）')
axes[1].set(xlabel='时间 / s', ylabel='yaw / °', title='B. 实际库执行：固定输入、水平静止 60 s')
axes[1].set_ylim(0, .11); axes[1].grid(alpha=.25)
right = axes[1].twinx()
right.plot(t, bias, color='#d67735', linewidth=2, label='估计 biasZ / (°/s)（右轴）')
right.axhline(.05, color='#777777', linestyle='--', linewidth=1, label='输入偏置 0.05 °/s（右轴）')
right.set(ylabel='偏置 / (°/s)', ylim=(0, .065))
lines = axes[1].lines + right.lines
axes[1].legend(lines, [line.get_label() for line in lines], loc='lower right', fontsize=8)
fig.suptitle('软件示例与理想关系：不是硬件长时漂移实测', fontsize=16)
svg_path = OUT/'drift-and-example.svg'
fig.savefig(svg_path, facecolor='white', metadata={'Date': None})
svg_path.write_text('\n'.join(line.rstrip() for line in svg_path.read_text(encoding='utf-8').splitlines())+'\n', encoding='utf-8')
fig.savefig(OUT/'drift-and-example.png', facecolor='white', dpi=140)
plt.close(fig)
print('Generated 4 SVG diagrams and curve PNG preview:', OUT)
