from pfac.crm import *
from pfac import const
from math import *
import string
import biggles

def spectrum(neles, temp, den, population,
             pref, suf = 'b', dir = '', nion = 3):
    for k in neles:
        print 'NELE = %d'%k
        f1 = '%s%02d%s'%(pref, k-1, suf)
        f2 = '%s%02d%s'%(pref, k, suf)
        f3 = '%s%02d%s'%(pref, k+1, suf)
        AddIon(k, 0.0, dir+f2) 
        if (nion == 3):
            AddIon(k+1, 0.0, dir+f3)
        if (nion > 1):
            SetBlocks(0.0, dir+f1)
        else:
            SetBlocks(-1.0)

        for i in range(len(temp)):
            p1 = population[i][k-1]
            p2 = population[i][k]
            p3 = population[i][k+1]
            p1 = p1/p2
            p3 = p3/p2
            p2 = 1.0
            print 'Temp = %10.3E'%(temp[i])
            print 'Abund: %10.3E %10.3E %10.3E'%(p1, p2, p3)

            SetEleDist(0, temp[i])
            print 'CE rates...'
            SetCERates(1)
            print 'TR rates...'
            SetTRRates(0)
            if (nion > 1):
                print 'RR rates...'
                SetRRRates(0)
                print 'CI rates...'
                SetCIRates(0)
                print 'AI rates...'
                SetAIRates(1)
                SetAbund(k-1, p1)
            SetAbund(k, p2)
            if (nion == 3):
                SetAbund(k+1, p3)
                
            for d in range(len(den)):
                print 'Density = %10.3E'%den[d]
                SetEleDensity(den[d])
                print 'Init blocks...'
                InitBlocks()
                s = 't%dd%di%d'%(i, d, nion)
                rt_file = '%s_%s.rt'%(f2,s)
                sp_file = '%s_%s.sp'%(f2,s)
                rt_afile = '%sa_%s.rt'%(f2[:-1],s)
                sp_afile = '%sa_%s.sp'%(f2[:-1],s)

                LevelPopulation()
                Cascade()

                RateTable(rt_file)
                SpecTable(sp_file)
                PrintTable(rt_file, rt_afile, 1)
                PrintTable(sp_file, sp_afile, 1)
                ReinitCRM(2)
            ReinitCRM(1)
        ReinitCRM()

def read_lines(file, nele):
    k = -1
    s = []
    for line in open(file, 'r').readlines():
        a = string.split(line)
        if (len(a) != 5):
            continue
        if (int(a[0]) != nele):
            continue
        e = float(a[3])
        i = int(a[1])
        j = int(a[2])
        s0 = float(a[4])
        s.append([i, j, e, s0])
                
    return s

def id_lines(w, s, name, eps=''):
    n = len(w)
    biggles.configure('screen', 'width', 800)
    biggles.configure('screen', 'height', 500)
    p = biggles.FramedPlot()
    p.aspect_ratio = 0.7
    xmin = min(w)
    xmax = max(w)
    for i in range(n):
        q1 = (w[i], 0)
        q2 = (w[i], s[i])
        l = biggles.Line(q1, q2)
        p.add(l)
        l = biggles.Label(q2[0], q2[1], '%d: %s'%(i,name[i]),
                          color='red', textangle=90)
        p.add(l)
    p.add(biggles.Line((xmin,0), (xmax,0), color='red'))
    if (eps):
        p.write_eps(eps)
    else:
        p.show()