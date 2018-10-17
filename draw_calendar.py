# coding: utf8
import os
import datetime
import matplotlib as mpl
import matplotlib.pyplot as plt

# texts
txt_page_title = '%s Conference Deadlines'

# base config drawing
font = {'size': 6}
mpl.rc('font', **font)
mpl.rcParams['figure.dpi'] = 300
mpl.rcParams['axes.linewidth'] = .5
mpl.rcParams['lines.linewidth'] = .5

mpl.rcParams['xtick.major.width'] = .5
mpl.rcParams['xtick.major.size'] = 1.5
mpl.rcParams['ytick.major.width'] = .5
mpl.rcParams['ytick.major.size'] = 1.5

mpl.rcParams['axes.xmargin'] = 0.01
mpl.rcParams['axes.ymargin'] = 0.01

# load data
confs = open('conf.txt').readlines()

# parse to list
day_confs = {}
cnt_conf = 0

for conf in confs:
    if conf.startswith('#'): continue
    
    conf = conf.strip()
    tmp = conf.split(',')
    if len(tmp)<2: continue
    # conf abbr and deadline day
    abbr, day = tmp[0], tmp[1]
    # the rank of this conf.
    if len(tmp)>=3: rank = tmp[2].upper()
    else:           rank = 'N'
    # may several deadlines on same day
    if day not in day_confs: day_confs[day] = []
    day_confs[day].append((abbr, rank))

    cnt_conf += 1

print('* done parse, %s confs in total' % cnt_conf)

# DRAW!
def _c2i(val):
    return val / 2.54

plt.clf()
year = 2018
figtitle = '%s' % year

fig, axes = plt.subplots(1, 1, figsize=(_c2i(28), _c2i(19)))
fig.patch.set_facecolor('white')
fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)  # reduce padding
ax = axes

w_m = 7
h_m = 6

w_day = 1
h_day = 1

title_indent = _c2i(0.1)
day_indent = _c2i(0.1)

fd_title = {'fontweight':'bold', 'fontsize':12}
fd_month = {'fontweight':'bold', 'fontsize':130}
fd_conf = {'fontsize':5 }
bg_ranks = {'A':'black', 'B':'dimgray', 'C':'gray', 'N':'lightgray'}
fg_ranks = {'A':'white', 'B':'white', 'C':'black', 'N':'black'}

# title
ax.text(0, 0.6, txt_page_title % year, va='bottom', ha='left', fontdict=fd_title)

# a header for weekday label
ax.plot([0, 28], [.5, .5], 'k-', linewidth=2)
labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
for i in range(4):
    for j in range(7):
        ax.text(i*w_m + j + .5, 0.15, labels[j], va='bottom', ha='center')

# loop on month
for month in range(12):
    print('* draw month %02d' % (month+1))
    
    # the border
    row_num = month // 4
    col_num = month % 4
    
    bpx = 0 + col_num * w_m
    bpy = 0 - row_num * h_m

    # big box
    ax.plot([bpx, bpx+w_m, bpx+w_m, bpx,     bpx],
            [bpy, bpy,     bpy-h_m, bpy-h_m, bpy], 'k-')
    
    # draw week row
    for i in range(h_m-1):
        ax.plot([bpx, bpx+w_m],
                [bpy - h_day * (i+1), bpy - h_day * (i+1)], color='k', linestyle='dotted')
    # draw week col
    for i in range(w_m-1):
        ax.plot([bpx + w_day * (i+1), bpx + w_day * (i+1)],
                [bpy, bpy - h_m], color='k', linestyle='dotted')
        
    # month title
    ax.text(bpx + w_m * 0.5, bpy - h_m*0.6, '%02d' % (month+1), 
            color='gray', fontdict=fd_month, alpha=.1, va='center', ha='center')
    
    # set the detail
    row_week = 0
    for i in range(1, 32):
        try:   day = datetime.datetime(year, month+1, i)
        except:  break
        
        # draw the date
        weekday = day.weekday()
        pos_x = bpx + weekday
        pos_y = bpy - row_week
        ax.text(pos_x + day_indent, pos_y - day_indent, '%02d'%i, color="gray", va='top')
        
        # add conf to this
        date_str = '%02d%02d' % (month+1, i)
        if date_str in day_confs:
            conf_seq = 0
            for conf in day_confs[date_str]:
                ax.add_patch(
                    mpl.patches.Rectangle(
                        (pos_x + w_day - 1, pos_y - (4-conf_seq)*h_day*0.25),   # (x,y)
                        w_day,          # width
                        h_day*0.24,          # height,
                        facecolor=bg_ranks[conf[1]]
                    )
                )
                ax.text(pos_x + w_day*0.5, pos_y - (4-conf_seq)*h_day*0.25, conf[0], 
                        color=fg_ranks[conf[1]], va='bottom', ha='center', fontdict=fd_conf)
                conf_seq += 1
        
        if weekday == 6: row_week += 1


ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

ax.set_xticks([])
ax.set_yticks([])

img_path = './'
if not os.path.exists(img_path): os.makedirs(img_path)
img_fn = '%s/dcal-%s' % (img_path, figtitle)
fig.savefig(img_fn + '.pdf', dpi=300, bbox_inches='tight')
print('* saved PDF!')
print('* done!')