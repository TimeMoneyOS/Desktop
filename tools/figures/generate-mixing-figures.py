"""A complete numerical complex-mixing example, independent of recorded IQ."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.signal import firwin, freqz, fftconvolve

OUT = Path(__file__).resolve().parents[2] / 'docs' / 'assets' / 'info-wave'
plt.rcParams.update({'font.sans-serif':['Microsoft YaHei','SimHei'], 'axes.unicode_minus':False, 'font.size':11, 'svg.fonttype':'none'})
fs=1_000_000
n=np.arange(12000)
t=n/fs
a=np.exp(2j*np.pi*100000*t)
b=.55*np.exp(-2j*np.pi*180000*t)
raw=a+b
lo_a=np.exp(-2j*np.pi*100000*t)
lo_b=np.exp(2j*np.pi*180000*t)
mix_a=raw*lo_a
mix_b=raw*lo_b
h=firwin(161,60000,fs=fs,window=('kaiser',8.6))
filtered_a=fftconvolve(mix_a,h,mode='same')
filtered_b=fftconvolve(mix_b,h,mode='same')
sl=slice(3000,3080)
us=(t[sl]-t[sl.start])*1e6

def save(fig,name):
    for ax in fig.axes:
        ax.grid(alpha=.18)
        ax.spines[['top','right']].set_visible(False)
    fig.tight_layout(pad=1.8)
    fig.savefig(OUT/(name+'.svg'))
    fig.savefig(OUT/(name+'.png'),dpi=160)
    plt.close(fig)

def timeplot(ax,z,title):
    ax.plot(us,z.real[sl],label='I（实部）',color='#1674b8')
    ax.plot(us,z.imag[sl],label='Q（虚部）',color='#c84049')
    ax.set(title=title,xlabel='时间（µs；截取稳态 80 点）',ylabel='幅度',ylim=(-1.75,1.75))
    ax.legend(loc='upper right',fontsize=9)

def spectrum(ax,z,title):
    v=z[2000:10000]
    f=np.fft.fftshift(np.fft.fftfreq(len(v),1/fs))/1000
    amp=np.abs(np.fft.fftshift(np.fft.fft(v)))/len(v)
    ax.plot(f,amp,color='#188468')
    ax.set(title=title,xlabel='基带频率（kHz）',ylabel='幅度谱（线性）',xlim=(-500,500),ylim=(-.03,1.15))

fig,ax=plt.subplots(3,2,figsize=(11,9))
for row,z,label in zip(ax,[a,b,raw],['用于构造的波源 A：+100 kHz，幅度 1','用于构造的波源 B：−180 kHz，幅度 0.55','实际交给两支路的原始 IQ：A + B']):
    timeplot(row[0],z,label);spectrum(row[1],z,label+' 的频谱')
save(fig,'mixing-01-input')

fig,ax=plt.subplots(3,2,figsize=(11,9))
for col,z,lo,label in [(0,mix_a,lo_a,'A 支路'),(1,mix_b,lo_b,'B 支路')]:
    timeplot(ax[0,col],raw,label+' 输入：同一份原始 IQ')
    timeplot(ax[1,col],lo,label+(' 本振：−100 kHz' if col==0 else ' 本振：+180 kHz'))
    spectrum(ax[2,col],z,label+(' 相乘后：0 与 −280 kHz' if col==0 else ' 相乘后：+280 与 0 kHz'))
save(fig,'mixing-02-branches')

I,Q=raw.real,raw.imag
C,S=lo_a.real,lo_a.imag
fig,ax=plt.subplots(3,2,figsize=(11,9))
terms=[I*C,Q*S,I*S,Q*C,mix_a.real,mix_a.imag]
labels=['乘积 1：I × C','乘积 2：Q × S','乘积 3：I × S','乘积 4：Q × C','结果实部：I′ = I×C − Q×S','结果虚部：Q′ = I×S + Q×C']
for p,z,label in zip(ax.flat,terms,labels):
    p.plot(us,z[sl],color='#1674b8');p.set(title=label,xlabel='时间（µs）',ylabel='幅度',ylim=(-1.75,1.75))
save(fig,'mixing-03-products')

fig,ax=plt.subplots(3,2,figsize=(11,9))
ax[0,0].plot(np.arange(len(h)),h,color='#1674b8');ax[0,0].set(title='教学 FIR：161 个系数 h[k]',xlabel='系数序号 k',ylabel='系数值')
w,H=freqz(h,worN=4096,fs=fs)
ax[0,1].plot(w/1000,20*np.log10(np.maximum(np.abs(H),1e-7)),color='#188468')
ax[0,1].axvline(60,color='#c84049',ls='--',label='设计截止 60 kHz')
ax[0,1].set(title='低通频率响应：通带保留、阻带衰减',xlabel='正频率（kHz；负频率对称）',ylabel='增益（dB）',ylim=(-140,5));ax[0,1].legend()
timeplot(ax[1,0],mix_a,'A 支路：低通前 I/Q');timeplot(ax[1,1],filtered_a,'A 支路：低通后 I/Q')
spectrum(ax[2,0],mix_a,'低通前：目标 0，另一波源 −280 kHz');spectrum(ax[2,1],filtered_a,'低通后：目标保留，另一波源被衰减')
save(fig,'mixing-04-filter')

fig,ax=plt.subplots(2,2,figsize=(11,6))
timeplot(ax[0,0],filtered_a,'A 支路最终：I ≈ 1，Q ≈ 0')
timeplot(ax[0,1],filtered_b,'B 支路最终：I ≈ 0.55，Q ≈ 0')
spectrum(ax[1,0],filtered_a,'A 支路最终频谱：中心 0 kHz')
spectrum(ax[1,1],filtered_b,'B 支路最终频谱：中心 0 kHz')
save(fig,'mixing-05-output')
assert np.max(np.abs(mix_a-(I*C-Q*S+1j*(I*S+Q*C)))) < 1e-12
assert np.max(np.abs(filtered_a[2000:10000]-1)) < 1e-4
assert np.max(np.abs(filtered_b[2000:10000]-.55)) < 1e-4
print('Generated 5 full processing figures; complex product and filtered steady-state verified.')
