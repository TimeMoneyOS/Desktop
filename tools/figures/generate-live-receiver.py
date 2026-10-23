"""Deterministic teaching figures; no hardware access or captured IQ."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import signal

OUT=Path(__file__).resolve().parents[2]/'docs/assets/live-receiver'
OUT.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.sans-serif':['Microsoft YaHei','SimHei'],'axes.unicode_minus':False,'svg.fonttype':'none','font.size':11})
def save(fig,name):
    fig.savefig(OUT/(name+'.svg'),bbox_inches='tight',facecolor='white')
    fig.savefig(OUT/(name+'.png'),bbox_inches='tight',dpi=130,facecolor='white')
    plt.close(fig)

fig,ax=plt.subplots(figsize=(12,8));ax.set(xlim=(0,12),ylim=(0,8));ax.axis('off')
rows=[(6.8,['设备 / IIO 缓冲','采集线程\n只读取和入队','rx_queue\n有界主机队列']),
      (4.5,['主循环取批次\n处理命令 / 缺口','数字混频\nFIR 低通 / 抽取','1 MS/s 解码\n空口包 → 协议帧']),
      (2.1,['stdout JSON 行','Rust 转发事件','React 显示\n字段 / 地图 / 频谱'])]
for y,labels in rows:
    for i,label in enumerate(labels):
        x=.3+i*4
        ax.add_patch(plt.Rectangle((x,y-.45),3.25,.9,facecolor=['#dcefeb','#e4edf7','#fae6de'][rows.index((y,labels))],edgecolor='#48616b'))
        ax.text(x+1.625,y,label,ha='center',va='center')
        if i<2:ax.annotate('',(x+4,y),(x+3.25,y),arrowprops={'arrowstyle':'->'})
ax.annotate('',(.8,5),(9.7,6.3),arrowprops={'arrowstyle':'->','connectionstyle':'angle,angleA=-90,angleB=180,rad=10'})
ax.annotate('',(.8,2.6),(9.7,4),arrowprops={'arrowstyle':'->','connectionstyle':'angle,angleA=-90,angleB=180,rad=10'})
ax.text(.3,7.65,'真实执行路径：采集、消费和显示相互解耦',fontsize=16)
ax.text(.3,.9,'预览旁路：主循环每隔至少 50 ms 取本批前 16384 点；解码仍使用整批数据。',fontsize=11)
ax.text(.3,.45,'Pluto 队列满：丢弃新到批次并计数；后续批次携带缺口标记，触发解码重置。',fontsize=11)
save(fig,'threads')

fig,axs=plt.subplots(3,1,figsize=(12,7),layout='constrained')
for ax,rate,size in zip(axs,[2e6,4e6,10e6],[65536,262144,262144]):
    duration=size/rate*1000
    for i in range(4):
        ax.broken_barh([(i*duration,duration*.98)],(.2,.6),facecolors='#57a99e')
        ax.text((i+.5)*duration,.5,f'批 {i+1}',ha='center',va='center')
    ax.set(xlim=(0,270),ylim=(0,1),yticks=[],xlabel='时间 / ms',title=f'{rate/1e6:g} MS/s：每批 {size} 点 = {duration:.3f} ms')
fig.suptitle('缓冲块时长由点数 ÷ 采样率决定；各行采用当前实际块长',fontsize=15)
save(fig,'buffers')

rng=np.random.default_rng(9361);fs=4e6;n=131072;t=np.arange(n)/fs
x=np.exp(2j*np.pi*.8e6*t)+.55*np.exp(2j*np.pi*1.7e6*t)+.06*(rng.normal(size=n)+1j*rng.normal(size=n))
mixed=x*np.exp(-2j*np.pi*.8e6*t)
count,beta=signal.kaiserord(80,35000/(fs/2));taps=signal.firwin(count|1,280000,fs=fs,window=('kaiser',beta))
filtered=signal.oaconvolve(mixed,taps)[:n];down=filtered[::4]
fig,axs=plt.subplots(4,1,figsize=(12,10),layout='constrained')
for ax,data,rate,title in zip(axs,[x,mixed,filtered,down],[fs,fs,fs,1e6],['① 原始复 IQ：目标 +0.8 MHz，干扰 +1.7 MHz','② 乘负频率复本振：目标移到 0，干扰移到 +0.9 MHz','③ FIR 低通：保留中心通带，抑制邻道','④ 每 4 点取 1 点：输出 1 MS/s，目标保持在中心']):
    k=min(len(data),32768);window=np.hanning(k);p=20*np.log10(np.maximum(abs(np.fft.fftshift(np.fft.fft(data[-k:]*window)))/window.sum(),1e-8))
    f=np.fft.fftshift(np.fft.fftfreq(k,1/rate))/1e6
    ax.plot(f,p,lw=.7,color='#237b85');ax.set(title=title,xlabel='相对当前中心的频率 / MHz',ylabel='幅度 / dB',ylim=(-100,5));ax.grid(alpha=.2)
fig.suptitle('教学仿真：单音用于展示移频与抗混叠；不是实际 GFSK 录波',fontsize=15)
save(fig,'filter-stages')

fig,axs=plt.subplots(2,1,figsize=(12,6),layout='constrained')
bits=np.array([0,1,1,0,1,0,0,1]);freq=np.repeat(bits*2-1,47)*200000
phase=2*np.pi*np.cumsum(freq)/1e6;z=np.exp(1j*phase)
us=np.arange(len(z))
axs[0].plot(us,z.real,label='I');axs[0].plot(us,z.imag,label='Q',alpha=.7);axs[0].legend();axs[0].set(xlabel='时间 / μs',ylabel='归一化幅度',title='简化连续相位 2-FSK：I/Q 同时携带相位旋转')
demod=np.angle(z[1:]*z[:-1].conj())*1e6/(2*np.pi)
axs[1].plot(us[1:],demod/1e3,color='#b55248');axs[1].axhline(0,color='gray',lw=.7);axs[1].set(xlabel='时间 / μs',ylabel='瞬时频率 / kHz',title='相邻样本相位差 → 正负频率 → 符号判决；实际程序还进行高斯匹配和同步')
for ax in axs:
    for edge in range(0,len(z),47):ax.axvline(edge,color='gray',lw=.5,alpha=.4)
save(fig,'demod')
