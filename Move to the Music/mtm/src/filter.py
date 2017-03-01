import numpy as N

t = N.array([1,2,3,4,5,6,6.9,8.1,9,10.2,10.9,12.1,13,14,15])

dt = N.diff(t)

mdt = dt.mean()

foo = N.concatenate([[mdt]*3, dt, [mdt]*3])

print foo

print 't=',t

print 'dt=', dt

f = N.bartlett(7)
f = f / sum(f)

print 'f=', f

fdt = N.convolve(foo, f, 'same')

fdt = fdt[3:-3]

print 'fdt=', fdt
