# coding: utf-8
######################################################################
## Filename:      plotcov19.py
## Author:        Eddie Baron <baron@ou.edu>
## Created at:    Fri May 22 09:30:20 2020
## Modified at:   Sun Jun 21 09:30:37 2020
## Modified by:   Eddie Baron <baron@ou.edu>
## Description:   
######################################################################
"""
Something I threw together this morning so that I could 
look at the data with a different running average
"""
import pandas as pd
import pylab
import numpy as np
import datetime

def boxcar(x,y,n):
  
  xsmooth = np.convolve(x,np.ones(n)/float(n),mode='valid')
  ysmooth = np.convolve(y,np.ones(n)/float(n),mode='valid')
  return xsmooth,ysmooth

def my_plt_setup(win=1):
  golden = (np.sqrt(5.)+1.)/2.

  figprops = dict(figsize=(8., 8./ golden ), dpi=128)    # Figure properties for single and stacked plots 
  # figprops = dict(figsize=(16., 8./golden), dpi=128)    # Figure properties for side by sides
  adjustprops = dict(left=0.15, bottom=0.15, right=0.90, top=0.93, wspace=0.2, hspace=0.2)       # Subp

  fig = pylab.figure(win,**figprops)   # New figure
  # fig.clf()
  fig.subplots_adjust(**adjustprops)  # Tunes the subplot layout

  ax = fig.add_subplot(1, 1, 1)
  return fig,ax

def bold_labels(ax,fontsize=None):
  if fontsize is None:
    fontsize = 14
  for tick in ax.xaxis.get_major_ticks():
    tick.label1.set_fontsize(fontsize)
    tick.label1.set_fontweight('bold')
  for tick in ax.yaxis.get_major_ticks():
    tick.label1.set_fontsize(fontsize)
    tick.label1.set_fontweight('bold')

def datestdtojd (stddate):
    fmt='%m/%d/%y'
    sdtdate = datetime.datetime.strptime(stddate, fmt)
    sdtdate = sdtdate.timetuple()
    jdate = sdtdate.tm_yday
    return(jdate)

def get_cases():

  df = pd.read_csv('https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_confirmed_usafacts.csv')

  return df

def explore_cases(mystate,df):
  if len(mystate) == 2:
    if mystate == 'US':
      dfok = df
    else:
      dfok = df[df.State == mystate ]
  else:
    dfok = df[df.State != mystate[1:]]

  cols = [ _ for _ in range(4,len(df.loc[0]))]
  sum = dfok.iloc[:,cols].sum(axis=0,skipna=True)
  diffs = np.diff(sum)
  dates = sum.index[1:]
  jd = []
  for _ in dates.values:
    jd.append(datestdtojd(_))
  jd = np.asarray(jd)
  

  ns = 0  
  while ns >= 0:
    fig,ax = my_plt_setup()
    ns = int(input("Give Window length (-1 to end): "))
    if ns < 0: break
    # ax.plot(jd,diffs,'o:')
    ax.bar(jd,diffs,label=mystate)
    xrun,yrun = boxcar(jd,diffs,ns)
    # ax.plot(xrun,yrun)
    # ymax = 150
    # if mystate == 'OK':
    #   ax.set_ylim([0,ymax])
    ax.set_xlim([70,jd.max()//10*10+10])
    md = pd.Series(index=dates,data=diffs)
    run = md.rolling(ns).mean()
    myleg_ = str(ns) +  " day running average"
    ax.plot(jd,run.values,'r',label=myleg_)
    ax.set_xlabel('Day of Year',fontsize=18)
    ax.set_ylabel('New Cases/day',fontsize=18)
    ax.legend()
    bold_labels(ax)
    pylab.show()
    pylab.clf()

def make_postage(df):
  
  figprops = dict(figsize=(8, 8 ), dpi=600)   
  adjustprops = dict(left=0.1, bottom=0.1, right=0.90, top=0.93, wspace=0.0, hspace=0.0)       # Subp

  win = 1
  myc_ = list()
  fig = pylab.figure(win,**figprops)   # New figure
  fig.subplots_adjust(**adjustprops)  # Tunes the subplot layout
  i = 0
  mylist = list(np.sort(df.State.unique()))
  mylist.append("US")
  mylist.append("!NY")

  for mystate in mylist: 
    if len(mystate) == 2:

      if mystate == 'US':
        dfok = df
      else:
        dfok = df[df.State == mystate ]

    else:
      dfok = df[df.State != mystate[1:]]

    i +=1
    ax = fig.add_subplot(7, 8, i)
    cols = [ _ for _ in range(4,len(df.loc[0]))]
    sum = dfok.iloc[:,cols].sum(axis=0,skipna=True)
    diffs = np.diff(sum)
    dates = sum.index[1:]

    if i == 1:
      jd = list()
      for _ in dates.values:
        jd.append(datestdtojd(_))
      jd = np.asarray(jd)
  

    ns = 10
    md = pd.Series(index=dates,data=diffs)
    run = md.rolling(ns).mean()
    myleg_ = str(ns) +  " day running average"
    if len(mystate) < 3:
      mylab_ = mystate
    else:
      mylab_ = "US \n w/o NY"
    # chelp = run.values[~np.isnan(run.values)].max()
    chelp = run.values[~np.isnan(run.values)][-1]
    cmax = 20000.
    c = pylab.cm.jet(chelp/cmax)
    myc_.append(c)
    # print(c,chelp,chelp/cmax,run.values.shape)
    ax.plot(jd,run.values,color=c,label=mylab_)
    ax.legend(fontsize='xx-small',frameon=False,\
              markerscale=0.1,loc='best',handlelength=0)
    # handles, labels = ax.get_legend_handles_labels()
    # for h in handles:
    #   h.set_linestyle("")
    #   h.set_fontsize='xx-small'
    #   h.set_frameon=False
    #   h.set_markerscale=0.1
    #   h.set_loc='best'
    # ax.legend(handles, labels)
    # bold_labels(ax)
    ax.set_xlim([70,jd.max()//10*10+10])
    xtl = ax.get_xticklabels()
    ytl = ax.get_yticklabels()
    for xtl_,ytl_ in zip(xtl,ytl):
      xtl_.set_visible(False)
      ytl_.set_visible(False)

  fig.text(0.5, 0.04, 'Day of 2020', ha='center')
  fig.text(0.04, 0.5, 'New Cases/day', va='center', rotation='vertical')
  m = pylab.cm.ScalarMappable(cmap=pylab.cm.jet)
  m.set_array([])
  cb_ax = fig.add_axes([.92, 0.1, 0.02, 0.8])
  cbar = fig.colorbar(m, cax=cb_ax)
  m.set_clim(0,2.e4)
  pylab.show()      
  fig.savefig('all51.png',dpi=600)

if __name__ == '__main__':
  df = get_cases()
  mystate = ' '
  while mystate != "":
    mystate = input("Give State (return to end): ")
    if mystate == "": break
    explore_cases(mystate,df)

  pylab.clf()
  make_postage(df)
