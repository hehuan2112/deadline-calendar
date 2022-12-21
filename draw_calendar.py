# coding: utf8
import os
import csv
import datetime
import matplotlib as mpl
import matplotlib.pyplot as plt

# YEAR!
year = 2022

# input file name
fn = 'data.csv'

# create the figure title
page_title = '%s Events' % (year)

# output to the following folder
img_path = './'
# create the output folder if not exists
if not os.path.exists(img_path): os.makedirs(img_path)
# make a output file name
img_fn = '%s/%s-page.pdf' % (img_path, year)

# load events from the CSV file
day_events_dict = {}
with open(fn) as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'* found column names: {", ".join(row)}')
            line_count += 1

        day = row['date']
        if day not in day_events_dict: 
            day_events_dict[day] = []

        day_events_dict[day].append({
            'label': row['label'],
            'font_color': 'black' if row['font_color'] == '' else row['font_color'],
            'bg_color': 'white' if row['bg_color'] == '' else row['bg_color'],
        })
        line_count += 1
    print(f'* processed {line_count} lines.')

# a helper function for converting 
def _cm2inch(val):
    '''Convert cm to inch
    '''
    return val / 2.54

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

# Draw now! 
# clear the figure first
plt.clf()

# create the canvas
fig, axes = plt.subplots(1, 1, figsize=(_cm2inch(28), _cm2inch(19)))

# set background of canvas to white
fig.patch.set_facecolor('white')

# adjust the margin for this canvas
fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)  # reduce padding
ax = axes

# width of month block
w_m = 7
# height of month block
h_m = 6
# width of day block
w_day = 1
# height of day block
h_day = 1

# the location of title and day
title_indent = _cm2inch(0.1)
day_indent = _cm2inch(0.1)

# font dictionary for default settings
fd_title = {'fontweight':'bold', 'fontsize':12}
fd_month = {'fontweight':'bold', 'fontsize':130}
fd_event = {'fontsize':5 }

# title
ax.text(
    0, 0.6, 
    page_title, 
    va='bottom', ha='left', fontdict=fd_title
)

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
    ax.plot(
        [bpx, bpx+w_m, bpx+w_m, bpx,     bpx],
        [bpy, bpy,     bpy-h_m, bpy-h_m, bpy], 
        'k-',
        linewidth=1
    )
    
    # draw week row
    for i in range(h_m-1):
        ax.plot(
            [bpx, bpx+w_m],
            [bpy - h_day * (i+1), bpy - h_day * (i+1)], 
            color='k', 
            linestyle='dotted'
        )
    # draw week col
    for i in range(w_m-1):
        ax.plot(
            [bpx + w_day * (i+1), bpx + w_day * (i+1)],
            [bpy, bpy - h_m], 
            color='k', 
            linestyle='dotted'
        )
        
    # month title
    ax.text(bpx + w_m * 0.5, bpy - h_m*0.6, '%02d' % (month+1), 
            color='gray', fontdict=fd_month, alpha=.2, va='center', ha='center')
    
    # set the detail
    row_week = 0
    for i in range(1, 32):
        try:
            # if 31 is out of range for some months
            # this will throw an exception   
            day = datetime.datetime(year, month+1, i)
        except:  
            break
        
        # draw the date
        weekday = day.weekday()
        pos_x = bpx + weekday
        pos_y = bpy - row_week
        ax.text(pos_x + day_indent, pos_y - day_indent, '%02d'%i, color="gray", va='top')
        
        # add event to this date
        # format the date as YYYY-mm-dd
        date_str = day.strftime('%Y-%m-%d')

        # try to find this date in the dictionary
        if date_str in day_events_dict:
            # define the sequence number of the events
            event_seq = 0
            for event in day_events_dict[date_str]:
                e_label = event['label']
                ax.add_patch(
                    mpl.patches.Rectangle(
                        (pos_x + w_day - 1, pos_y - (4-event_seq)*h_day*0.25),   # (x,y)
                        w_day,          # width
                        h_day*0.24,          # height,
                        facecolor=event['bg_color']
                    )
                )
                ax.text(
                    pos_x + w_day*0.5, 
                    pos_y - (4-event_seq)*h_day*0.25, 
                    e_label, 
                    color=event['font_color'], 
                    va='bottom', 
                    ha='center', 
                    fontdict=fd_event
                )
                event_seq += 1
        
        if weekday == 6: row_week += 1


ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

ax.set_xticks([])
ax.set_yticks([])

# save this file
fig.savefig(img_fn, dpi=300, bbox_inches='tight')
print('* saved PDF!')
print('* done!')