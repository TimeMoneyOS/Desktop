"""Reproducible teaching diagrams, not measured SDR traces."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT=Path(__file__).resolve().parents[2]/'docs'/'assets'/'gain'
OUT.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.sans-serif':['Microsoft YaHei','SimHei'],'axes.unicode_minus':False,'font.size':11,'svg.fonttype':'none'})
rng=np.random.default_rng(9361)
def save(fig,name):
    fig.savefig(OUT/(name+'.svg'),bbox_inches='tight',facecolor='white')
    fig.savefig(OUT/(name+'.png'),dpi=140,bbox_inches='tight',facecolor='white');plt.close(fig)

fig,ax=plt.subplots(figsize=(12,7));ax.set(xlim=(0,12),ylim=(0,7));ax.axis('off')
rows=[(5.8,['Pluto 软件 IQ','数字幅度 ×a','DAC / 上变频','TX 衰减器','TX1A 天线']),
      (3.6,['B210 天线','LNA / 混频 / TIA','模拟基带滤波与增益','ADC 量化','数字滤波 → IQ']),
      (1.4,['I/Q 波形','FFT / 瀑布图','数字移频 / 滤波','GFSK 解调','校验 → 位置 / 血量'])]
for y,labels in rows:
    for i,label in enumerate(labels):
        x=.2+i*2.4
        ax.add_patch(plt.Rectangle((x,y-.4),2.1,.8,facecolor=['#dcefeb','#e1eaf6','#f8e6e5'][rows.index((y,labels))],edgecolor='#52616b',lw=1))
        # Explicit wrapping keeps labels inside fixed boxes.
        label=label.replace('模拟基带滤波与增益','模拟基带滤波\n与增益').replace('LNA / 混频 / TIA','LNA / 混频\n/ TIA').replace('校验 → 位置 / 血量','校验 →\n位置 / 血量')
        ax.text(x+1.05,y,label,ha='center',va='center',fontsize=10)
        if i<4:ax.annotate('',(x+2.4,y),(x+2.1,y),arrowprops={'arrowstyle':'->','color':'#52616b'})
ax.text(.2,6.55,'① 发射端：数字幅度与硬件衰减共同决定输出；实际 dBm 需要校准',fontsize=12)
ax.text(.2,4.4,'② 空口／线缆：路径损耗、噪声、干扰先到达接收机',fontsize=12)
ax.text(.2,2.2,'③ 接收增益在 ADC 前改变电压；主机缩放不能修复已经削顶的信号',fontsize=12)
save(fig,'link')

t=np.linspace(0,4,1600);s=.08*np.sin(2*np.pi*3*t);noise=rng.normal(0,.012,len(t))
fig,axes=plt.subplots(3,1,figsize=(11,8),sharex=True)
for ax,g,title in zip(axes,[1,5,18],['增益偏低：量化利用不足','增益合适：有足够幅度，也有峰值余量','增益过高：ADC 截断超出范围的部分']):
    before=(s+noise)*g;after=np.clip(before,-1,1)
    ax.plot(t,before,color='#b5bdc7',lw=.7,label='ADC 前理想电压')
    ax.plot(t,after,color='#1674b8' if g<18 else '#c84049',lw=.9,label='ADC 输入范围内的记录')
    ax.axhline(1,color='#c84049',ls='--');ax.axhline(-1,color='#c84049',ls='--')
    ax.set(title=title,ylabel='归一化电压',ylim=(-1.8,1.8));ax.grid(alpha=.2);ax.legend(loc='upper right',fontsize=9)
axes[-1].set_xlabel('时间（教学单位）');fig.tight_layout();save(fig,'adc')

fig,axes=plt.subplots(1,3,figsize=(12,4),sharey=True)
for ax,g,title in zip(axes,[1,4,4],['原始 IQ','数字乘 4','数字乘 4 后发生限幅']):
    v=(s+noise)*g
    if ax is axes[2]:v=np.clip(v,-.2,.2)
    ax.plot(t,v,lw=.8,color='#1674b8');ax.set(title=title,xlabel='时间',ylim=(-.5,.5));ax.grid(alpha=.2)
axes[0].set_ylabel('数值幅度');fig.tight_layout();save(fig,'digital')

fig,axes=plt.subplots(1,3,figsize=(12,4),sharey=True)
for ax,signal,noise_db,title in zip(axes,[-80,-60,-50],[-90,-70,-60],['低接收增益','接收增益 +20 dB','同一 IQ 数字放大 +10 dB']):
    ax.bar(['信号','噪声'],[signal+110,noise_db+110],bottom=-110,color=['#1674b8','#d49045'])
    ax.set(ylim=(-110,-35),title=title,ylabel='相对功率 dB');ax.text(.5,-42,'信噪比均为 10 dB',ha='center',fontsize=10);ax.grid(axis='y',alpha=.2)
fig.suptitle('理想增益：信号和已有噪声一起移动（示意，忽略后级噪声与非线性）');fig.tight_layout();save(fig,'snr')

t=np.linspace(0,6,1800);env=np.where(t<2,.08,np.where(t<4,.75,.08))
fig,axes=plt.subplots(3,1,figsize=(11,7),sharex=True)
axes[0].plot(t,env,color='#1674b8');axes[0].set(title='输入从弱 → 强 → 弱（教学包络）',ylabel='输入幅度')
for ax,rate,title in zip(axes[1:],[.012,.18],['慢响应示意：强信号到来后可能短时过载','快响应示意：更快降增益，恢复也有过渡']):
    target=.45/env;gain=np.empty(len(t));gain[0]=target[0]
    for i in range(1,len(t)):gain[i]=gain[i-1]+rate*(target[i]-gain[i-1])
    out=env*gain;ax.plot(t,out,color='#188468');ax.axhline(1,color='#c84049',ls='--');ax.set(title=title,ylabel='输出包络',ylim=(0,4.5))
for ax in axes:ax.grid(alpha=.2)
axes[-1].set_xlabel('时间（教学单位；非芯片 AGC 响应时间）');fig.tight_layout();save(fig,'agc')

fig,ax=plt.subplots(figsize=(11,4));ax.axis('off')
labels=['先固定 TX 与天线连接','RX 从适中增益开始','观察削顶、噪底、有效包率','过载则降增益／加衰减','弱且未过载则逐步加增益']
for i,label in enumerate(labels):
    y=4-i*.8;ax.text(.5,y,label,ha='center',va='center',bbox={'boxstyle':'square,pad=.35','fc':'#e1eaf6','ec':'#52616b'})
    if i<4:ax.annotate('',(.5,y-.55),(.5,y-.2),arrowprops={'arrowstyle':'->'})
ax.set(xlim=(0,1),ylim=(.3,4.5));save(fig,'workflow')
assert np.isclose(20*np.log10(2),6.020599913)
print('Generated six diagram sets')
