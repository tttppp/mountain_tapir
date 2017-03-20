#!/bin/sh
export TCL_LIBRARY=$SNAP/usr/share/tcltk/tcl8.6:$TCL_LIBRARY:$TK_LIBRARY
export TK_LIBRARY=$SNAP/usr/share/tcltk/tk8.6:$TK_LIBRARY:$TCL_LIBRARY

$SNAP/usr/bin/python3 -m mountain_tapir.mountain_tapir

