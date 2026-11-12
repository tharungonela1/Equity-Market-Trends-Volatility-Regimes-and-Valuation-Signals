# Market trends exercise - Tharun Gonela. Run in order: part 1 (analysis), part 2 (charts).
# Data: https://raw.githubusercontent.com/datasets/s-and-p-500/main/data/data.csv saved as sp500.csv
# ---------- PART 1: analysis ----------
import pandas as pd, numpy as np
d = pd.read_csv('sp500.csv', parse_dates=['Date']).set_index('Date')
d = d.replace(0, np.nan)            # zeros are missing-value placeholders in this file
px  = d['SP500']                    # nominal price, to Sep 2026
rpx = d['Real Price']               # real price, to Sep 2023
pe  = d['PE10']                     # CAPE, to Sep 2023 (and only from ~1881)

# A) regimes: rolling 12m realised vol of monthly nominal returns
r = px.pct_change()
vol = r.rolling(12).std() * np.sqrt(12)
fwd12 = px.shift(-12) / px - 1
A = pd.DataFrame({'vol':vol,'fwd12':fwd12}).dropna()
thr = A['vol'].quantile(0.8)
hi, lo = A[A.vol>=thr], A[A.vol<thr]
print('A) vol threshold (80th pct): %.3f' % thr)
print('   n high=%d mean fwd12=%.3f median=%.3f | n other=%d mean=%.3f median=%.3f' %
      (len(hi),hi.fwd12.mean(),hi.fwd12.median(),len(lo),lo.fwd12.mean(),lo.fwd12.median()))
print('   same split, last 30y only:')
B_ = A.loc['1996':]; t2 = B_.vol.quantile(0.8)
print('   n high=%d mean=%.3f | n other=%d mean=%.3f' % ((B_.vol>=t2).sum(), B_[B_.vol>=t2].fwd12.mean(), (B_.vol<t2).sum(), B_[B_.vol<t2].fwd12.mean()))

# B) valuation vs next-10y annualised real price return
f10 = (rpx.shift(-120)/rpx)**(1/10) - 1
B = pd.DataFrame({'pe':pe,'f10':f10}).dropna()
print('B) n=%d range %s..%s  corr(PE10, fwd10y real)=%.3f  corr(log PE10, ...)=%.3f' %
      (len(B),B.index.min().date(),B.index.max().date(),B.corr().iloc[0,1], np.corrcoef(np.log(B.pe),B.f10)[0,1]))
B['q'] = pd.qcut(B.pe,5,labels=['Q1 cheapest','Q2','Q3','Q4','Q5 dearest'])
print(B.groupby('q',observed=True).f10.agg(['count','mean','min','max']))

# C) walk-forward test: predict next-12m real return from log PE10 vs expanding-mean baseline
f12 = rpx.shift(-12)/rpx - 1
C = pd.DataFrame({'x':np.log(pe),'y':f12}).dropna()
preds=[]; 
test_idx = C.loc['1960':].index
for t in test_idx:
    # only use observations whose 12m outcome was already known at t (i.e. ended on/before t)
    train = C.loc[:t - pd.DateOffset(months=12)]
    if len(train)<240: continue
    b,a = np.polyfit(train.x, train.y, 1)
    preds.append((t, a + b*C.loc[t,'x'], train.y.mean(), C.loc[t,'y']))
P = pd.DataFrame(preds, columns=['t','model','base','y']).set_index('t')
rm  = np.sqrt(((P.y-P.model)**2).mean()); rb = np.sqrt(((P.y-P.base)**2).mean())
r2os = 1 - ((P.y-P.model)**2).sum()/((P.y-P.base)**2).sum()
print('C) test %s..%s n=%d  RMSE model=%.4f baseline=%.4f  OOS R2=%.3f' % (P.index.min().date(),P.index.max().date(),len(P),rm,rb,r2os))
for lbl,sl in [('1960-1989',slice('1960','1989')),('1990-2022',slice('1990','2022'))]:
    q=P.loc[sl]; print('   ',lbl,'n=%d OOS R2=%.3f'%(len(q),1-((q.y-q.model)**2).sum()/((q.y-q.base)**2).sum()))
P.to_pickle('P.pkl'); A.to_pickle('A.pkl'); B.to_pickle('B.pkl'); px.to_pickle('px.pkl'); vol.to_pickle('vol.pkl')

# ---------- PART 2: charts ----------
import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
px=pd.read_pickle('px.pkl'); vol=pd.read_pickle('vol.pkl'); B=pd.read_pickle('B.pkl'); P=pd.read_pickle('P.pkl')
NAVY='#0C1F3D'; BLUE='#1A56A0'; RED='#B91C1C'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False})

# 1 price (log) with high-vol regimes shaded
thr=vol.dropna().quantile(0.8)
fig,ax=plt.subplots(figsize=(7.2,3.0))
ax.semilogy(px.index,px.values,color=NAVY,lw=1.1)
hv=(vol>=thr)
start=None
for t,v in hv.items():
    if v and start is None: start=t
    if (not v) and start is not None: ax.axvspan(start,t,color=RED,alpha=0.15,lw=0); start=None
if start is not None: ax.axvspan(start,hv.index[-1],color=RED,alpha=0.15,lw=0)
ax.set_title('S&P 500 monthly price (log scale); shaded = top-20% 12-month volatility',fontsize=9.5,loc='left')
ax.set_ylabel('Index level (log)'); fig.tight_layout(); fig.savefig('c1.png',dpi=200); plt.close()

# 2 CAPE quintiles vs next-10y real return
g=B.groupby('q',observed=True).f10.mean()*100
fig,ax=plt.subplots(figsize=(7.2,2.8))
bars=ax.bar(g.index.astype(str),g.values,color=[BLUE]*5)
for b,v in zip(bars,g.values): ax.text(b.get_x()+b.get_width()/2,v+0.1,f'{v:.1f}%',ha='center',fontsize=8.5)
ax.set_ylabel('Mean next-10y\nreal return p.a. (%)')
ax.set_title('Starting valuation (CAPE quintile) vs subsequent 10-year real price return, 1881–2013 starts',fontsize=9.5,loc='left')
fig.tight_layout(); fig.savefig('c2.png',dpi=200); plt.close()

# 3 cumulative squared-error advantage of model over baseline
adv=((P.y-P.base)**2-(P.y-P.model)**2).cumsum()
fig,ax=plt.subplots(figsize=(7.2,2.8))
ax.plot(adv.index,adv.values,color=NAVY,lw=1.2); ax.axhline(0,color='grey',lw=0.8)
ax.set_title('Walk-forward test: cumulative error advantage of CAPE model vs expanding-mean baseline',fontsize=9.5,loc='left')
ax.set_ylabel('Above 0 = model better'); fig.tight_layout(); fig.savefig('c3.png',dpi=200); plt.close()
print('threshold',round(thr,4))
