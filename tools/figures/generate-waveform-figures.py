"""Generate reproducible teaching figures; these are not captured RF samples."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parents[2] / 'docs' / 'assets' / 'info-wave'
plt.rcParams.update({"font.sans-serif": ["Microsoft YaHei", "SimHei"],
                     "axes.unicode_minus": False, "font.size": 12,
                     "svg.fonttype": "none"})
BLUE, RED, GREEN = "#1674b8", "#c84049", "#188468"

def finish(fig, name):
    fig.set_facecolor("white")
    for ax in fig.axes:
        ax.grid(alpha=.18)
        ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(pad=1.6)
    fig.savefig(OUT / (name + ".svg"))
    fig.savefig(OUT / (name + ".png"), dpi=170)
    plt.close(fig)

t = np.linspace(0, 2, 801)
fig, axes = plt.subplots(2, 1, figsize=(9, 6))
axes[0].plot(t, np.cos(2*np.pi*t), label="I = cos(相位)", color=BLUE)
axes[0].plot(t, np.sin(2*np.pi*t), label="Q = sin(相位)", color=RED)
axes[0].scatter([.125], [np.cos(np.pi/4)], color=BLUE)
axes[0].scatter([.125], [np.sin(np.pi/4)], color=RED)
axes[0].set(xlabel="时间（教学归一化单位）", ylabel="归一化幅度", title="同一信号的两个分量：I 与 Q 相差四分之一周期")
axes[0].legend(loc="upper right")
a = np.linspace(0, 2*np.pi, 400)
axes[1].plot(np.cos(a), np.sin(a), color=BLUE)
axes[1].annotate("", xy=(.707,.707), xytext=(0,0), arrowprops={"arrowstyle":"->", "color":RED,"lw":2})
axes[1].text(1.12,.65,"相位 45°\nI = Q ≈ 0.707", transform=axes[1].transAxes)
axes[1].set(xlabel="I（实部）", ylabel="Q（虚部）", title="把同一时刻的 (I, Q) 画成点：角度是相位，离原点的距离是幅度", aspect="equal", xlim=(-1.25,1.25), ylim=(-1.25,1.25))
finish(fig,"waveform-iq")

bits = np.array([1,1,0,1,0,0,1,0])
sps=100
x=np.arange(len(bits)*sps)/sps
levels=np.repeat(2*bits-1,sps)
k=np.arange(-100,101)
g=np.exp(-.5*(k/20)**2); g/=g.sum()
smooth=np.convolve(np.pad(levels,(100,100),mode="edge"),g,mode="valid")
fig,axes=plt.subplots(4,1,figsize=(10,10),sharex=True)
axes[0].step(x,np.repeat(bits,sps),where="post",color=BLUE)
axes[0].set(ylabel="比特",ylim=(-.3,1.5),title="GFSK：比特控制瞬时频率，高斯平滑让频率逐渐过渡")
axes[1].plot(x,levels,":",color="gray",label="未经平滑的理想频率")
axes[1].plot(x,smooth,color=GREEN,label="平滑后的频率趋势")
axes[1].set(ylabel="频偏 / Δf",ylim=(-1.4,1.4));axes[1].legend(loc="upper right")
phase=np.cumsum(smooth)*2*np.pi*11.689981/sps
axes[2].plot(x,np.cos(phase),color=BLUE,label="I = cos(相位)",lw=1)
axes[2].plot(x,np.sin(phase),color=RED,label="Q = sin(相位)",lw=1,alpha=.85)
axes[2].legend(loc="upper right",fontsize=9)
axes[2].set(ylabel="基带 I / Q",title="实际频偏尺度：Δf·T ≈ 11.69；用 I/Q 相位关系区分旋转方向")
carrier_phase=np.cumsum(6+4*smooth)*2*np.pi/sps
axes[3].plot(x,np.cos(carrier_phase),color=BLUE,label="I = cos(相位)",lw=1)
axes[3].plot(x,np.sin(carrier_phase),color=RED,label="Q = sin(相位)",lw=1,alpha=.85)
axes[3].legend(loc="upper right",fontsize=9)
axes[3].set(xlabel="时间 / 位宽 T（每一格是一位）",ylabel="载波示意 I / Q",title="便于观察的正载频示意：1 约 10 圈/位（密），0 约 2 圈/位（疏）")
for ax in axes:
    for n,b in enumerate(bits):
        ax.axvline(n,color="gray",alpha=.25)
        if ax is axes[0]:ax.text(n+.5,1.2,str(b),ha="center")
finish(fig,"waveform-gfsk")

f=np.linspace(-500,500,2001)
target=lambda c: np.exp(-.5*((f-c)/65)**2)
fig,axes=plt.subplots(2,1,figsize=(9,6),sharex=True)
axes[0].plot(f,target(200),color=BLUE,label="目标中心 +200 kHz")
axes[0].plot(f,.6*target(-200),color=RED,label="另一个信号")
axes[0].set(title="数字混频前：频率相对于录波中心",ylabel="相对功率（示意）");axes[0].legend()
axes[1].axvspan(-280,280,color=GREEN,alpha=.12,label="低通通带示意 ±280 kHz")
axes[1].plot(f,target(0),color=BLUE,label="目标搬到 0 kHz")
axes[1].plot(f,.6*target(-400),color=RED,label="另一个信号搬到 -400 kHz")
axes[1].set(title="乘以 -200 kHz 复数本振后：所有频率一起平移",xlabel="基带频率（kHz）",ylabel="相对功率（示意）");axes[1].legend(fontsize=10)
finish(fig,"waveform-spectrum")

rng=np.random.default_rng(17)
noisy=smooth+rng.normal(0,.3,len(x))
fig,axes=plt.subplots(2,1,figsize=(9,6),sharex=True)
axes[0].plot(x,noisy,color="#9aa8b3",lw=.8,label="含噪软值（模拟）")
axes[0].plot(x,smooth,color=BLUE,label="平滑趋势")
axes[0].set(title="解调后的软值：正负决定比特，绝对值表示离判决门限的距离",ylabel="软值（归一化）");axes[0].legend()
centers=np.arange(8)+.5
values=np.interp(centers,x,smooth)
axes[1].plot(x,smooth,color=BLUE)
axes[1].axhline(0,color="black",lw=1,label="判决门限 0")
axes[1].scatter(centers,values,color=GREEN,s=50,label="位中心采样")
axes[1].scatter(np.arange(1,8),np.interp(np.arange(1,8),x,smooth),color=RED,marker="x",s=50,label="边界采样，翻转处容易出错")
for n,b in enumerate(bits):axes[1].text(n+.5,1.2,str(b),ha="center")
axes[1].set(xlabel="时间 / 位宽 T",ylabel="软值",ylim=(-1.4,1.55),title="定时恢复：找到每一位里面较可靠的采样位置");axes[1].legend(loc="lower left",fontsize=10)
finish(fig,"waveform-timing")

template_bits=np.array([int(b) for b in f'{0x2F6F4C74B914492E:064b}{15:016b}{15:016b}'])
template=2*template_bits-1
stream=rng.normal(0,.75,330)
start=130
stream[start:start+96]=template+rng.normal(0,.25,96)
windows=np.lib.stride_tricks.sliding_window_view(stream,96)
score=(windows@template)/(np.linalg.norm(windows,axis=1)*np.linalg.norm(template))
fig,axes=plt.subplots(2,1,figsize=(9,6))
axes[0].plot(stream,color=BLUE,lw=1)
axes[0].axvspan(start,start+96,color=GREEN,alpha=.15,label="埋入的 96 位同步模板")
axes[0].set(title="在一长串软值中找包起点（人工模拟，按位展示）",xlabel="软值序号",ylabel="软值");axes[0].legend()
axes[1].plot(score,color=GREEN)
axes[1].axhline(.45,color=BLUE,ls="--",label="TCR 门限 0.45")
axes[1].axhline(.34,color=RED,ls=":",label="Fast 门限 0.34")
axes[1].axvline(start,color="gray",alpha=.6)
axes[1].set(title="窗口与已知模板越像，归一化相关分数越高",xlabel="候选窗口起点",ylabel="相关分数",ylim=(-.45,1.1));axes[1].legend()
finish(fig,"waveform-sync")
print("Generated 5 SVG and 5 PNG teaching figures.")
