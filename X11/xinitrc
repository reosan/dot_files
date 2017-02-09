#!/bin/sh

userresources=$HOME/.Xresources
usermodmap=$HOME/.Xmodmap
sysresources=/etc/X11/xinit/.Xresources
sysmodmap=/etc/X11/xinit/.Xmodmap

# merge in defaults and keymaps

if [ -f $sysresources ]; then
    xrdb -merge $sysresources
fi
if [ -f $sysmodmap ]; then
    xmodmap $sysmodmap
fi
if [ -f "$userresources" ]; then
    xrdb -merge "$userresources"
fi
if [ -f "$usermodmap" ]; then
    xmodmap "$usermodmap"
fi
# start some nice programs
if [ -d /etc/X11/xinit/xinitrc.d ] ; then
 for f in /etc/X11/xinit/xinitrc.d/?* ; do
  [ -x "$f" ] && . "$f"
 done
 unset f
fi

#twm &
#xclock -geometry 50x50-1+1 &
#xterm -geometry 80x50+494+51 &
#xterm -geometry 80x20+494-0 &
#exec xterm -geometry 80x66+0+0 -name login

#export XIM_PROGRAM=/usr/bin/ibus-daemon
#export XIM_ARGS="--xim"
#ibus-daemon -d -x --xim &

im=fcitx
export XIM=$im
export XMODIFIERS="@im=${im}"
export GTK_IM_MODULE=$im
export QT_IM_MODULE=$im
fcitx-autostart

IN='LVDS1'
HDMI='HDMI1'
if (xrandr | grep "$HDMI disconnected"); then
    xrandr --output $HDMI --off --output $IN --auto
else
    xrandr --output $HDMI --mode 1920x1080 --pos 0x0 \
           --output $IN --mode 1280x800 --pos 1920x280
    xrandr --output $HDMI --set "Broadcast RGB" "Full"
    
    # xrandr --newmode "1920x1200_60.00"  193.25  1920 2056 2256 2592  1200 1203 1209 1245 -hsync +vsync
    # xrandr --addmode VIRTUAL1 1920x1200_60.00
    # xrandr --output VIRTUAL1 --mode 1920x1200_60.00 --pos 0x1080
    # x11vnc -display :0 -clip 1920x1200+0+1080 -rfbauth ~/.vnc/passwd -ncache 10 -nocursorhape -forever & 

    xrandr --newmode  "480x300_60.00" 10.45 480 472 520 560 300 301 304 311 -HSync +Vsync
    xrandr --addmode VIRTUAL1 480x300_60.00
    xrandr --output VIRTUAL1 --mode 480x300_60.00 --pos 0x1080
    x11vnc -display :0 -clip 480x300+0+1080 -rfbauth ~/.vnc/passwd -ncache 10 -nocursorhape -forever & 
fi

exec xmonad
