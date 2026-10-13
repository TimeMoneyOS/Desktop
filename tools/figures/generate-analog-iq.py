"""Ideal analog quadrature conversion with reduced teaching frequencies."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT=Path(__file__).resolve().parents[2]/'docs'/'assets'/'info-wave'
plt.rcParams.update({'font.sans-serif':['Microsoft YaHei','SimHei'],'axes.unicode_minus':False,'font.size':11,'svg.fonttype':'none'})
t=np.linspace(0,3,6001)
rf=np.cos(2*np.pi*9*t+.4)
li=np.cos(2*np.pi*8*t)
lq=-np.sin(2*np.pi*8*t)
theta=2*np.pi*t+.4
lowi=.5*np.cos(theta);lowq=.5*np.sin(theta)
highi=.5*np.cos(2*np.pi*17*t+.4)
highq=-.5*np.sin(2*np.pi*17*t+.4)
assert np.allclose(rf*li,lowi+highi)
assert np.allclose(rf*lq,lowq+highq)

def plot(ax,values,title,labels):
    for v,label,color in zip(values,labels,['#1674b8','#c84049','#188468']):
        ax.plot(t,v,label=label,color=color,lw=1)
    ax.set(title=title,xlabel='时间（教学单位）',ylabel='幅度',xlim=(0,3))
    ax.grid(alpha=.18);ax.spines[['top','right']].set_visible(False)
    ax.legend(fontsize=9,loc='upper right')

def save(fig,name):
    fig.tight_layout(pad=1.8)
    fig.savefig(OUT/(name+'.svg'))
    fig.savefig(OUT/(name+'.png'),dpi=160)
    plt.close(fig)

fig,ax=plt.subplots(3,1,figsize=(11,8))
plot(ax[0],[rf],'天线输入：一条实数射频波形，教学频率 9',['RF'])
plot(ax[1],[li,lq],'正交本振：同频率 8；I 用 cos，Q 用 −sin',['LO_I','LO_Q'])
plot(ax[2],[rf*li,rf*lq],'分别相乘：两路输出含快速和频与慢速差频',['I_mix = RF × LO_I','Q_mix = RF × LO_Q'])
save(fig,'analog-01-mix')
fig,ax=plt.subplots(3,2,figsize=(11,9))
plot(ax[0,0],[highi],'I 路和频：9+8=17',['I 和频'])
plot(ax[0,1],[highq],'Q 路和频：9+8=17',['Q 和频'])
plot(ax[1,0],[lowi],'I 路差频：9−8=1',['I 差频'])
plot(ax[1,1],[lowq],'Q 路差频：9−8=1',['Q 差频'])
plot(ax[2,0],[lowi],'理想模拟低通后：I = 0.5 cos(θ)',['模拟 I'])
plot(ax[2,1],[lowq],'理想模拟低通后：Q = 0.5 sin(θ)',['模拟 Q'])
save(fig,'analog-02-components')
fig,ax=plt.subplots(2,1,figsize=(11,6))
ts=np.arange(0,3,.1)
for p,v,sv,title in [(ax[0],lowi,.5*np.cos(2*np.pi*ts+.4),'I 路 ADC：在采样时刻量化幅度'),(ax[1],lowq,.5*np.sin(2*np.pi*ts+.4),'Q 路 ADC：使用相同采样时刻')]:
    plot(p,[v],title,['模拟输入'])
    quant=np.round(sv*16)/16
    p.scatter(ts,quant,color='#c84049',s=22,label='量化采样点（教学步长 1/16）')
    p.legend(fontsize=9,loc='upper right')
save(fig,'analog-03-adc')
print('Generated 3 analog IQ figures; both mixer identities verified.')
