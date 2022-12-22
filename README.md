# Deadline Calendar

A year calendar of events

## Requirements

Only one lib is required: `matplotlib`

## Usage

Only the following steps:

1. A `data.csv` must be prepared, which contains the events you want to add to the calendar. The format of each row is `YYYY-mm-dd,label,font_color,bg_color`. Please ensure a short label length because of the limited space in date cells. The font color and bg_color are not required, but it would be better to specify colors for better looking.
2. Make sure the `year` is correctly defined in the script `draw_calendar.py`.
3. Run `python draw_calendar.py`, then a PDF file will be generated in the same folder.

It looks like the following:

![](https://raw.githubusercontent.com/hehuan2112/deadline-calendar/master/demo.png)