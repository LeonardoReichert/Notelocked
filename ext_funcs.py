#!/usr/bin/env python3


"""

This file is part of Notelocked.
Copyright (C) 2022  Leonardo A. Reichert

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

"""
#you can see the full license at: "LICENSE" file

#https://www.gnu.org/licenses/old-licenses/gpl-2.0.html

# Contact: leoreichert5000@gmail.com


from os import mkdir, getcwd;
from os.path import exists;
from platform import system;



### fix clipboard clipboard:
#on windows, tkinter after exit cannot save data on clipboard
#optional: "pip install pywin32"

win32clipboard = None;
if system().lower() == "windows":
    try:
        import win32clipboard;
    except ImportError:
        pass;
        

def win32clipboard_fix(tkwin):
    """ optional: "pip install pywin32"
        only for windows, try fix the clipboard,
        tkinter cannot save the data on windows after exit app """
    
    if win32clipboard:
        try:
            text = tkwin.clipboard_get();
            win32clipboard.OpenClipboard();
            win32clipboard.EmptyClipboard();
            win32clipboard.SetClipboardData(win32clipboard.CF_TEXT, text.encode());
            win32clipboard.CloseClipboard();
            #fixed succes
        except:
            pass;
        
##############




def _geticon():
    # need multiplatform ?
    ico = "icon.ico";
    return ico;

icon = _geticon();


pathDefaultName = "/saves/";
pathDefault = getcwd()+"/"+pathDefaultName;


def makePath():
    if not exists(pathDefault):
        try:
            mkdir(pathDefault);
        except:
            return "";
        
    return pathDefault;



def center_window(master, window):
    
    window.withdraw();

    window.update_idletasks(); #<- need the geometry...
    
    xMaster, yMaster = master.winfo_rootx(),master.winfo_rooty();
    wMaster, hMaster = master.winfo_width(),master.winfo_height();
    
    xCenter, yCenter = xMaster +wMaster//2, yMaster +hMaster//2;
    
    wScreen, hScreen = master.winfo_screenwidth(),master.winfo_screenheight();
    
    w2, h2 = window.winfo_width(),window.winfo_height();
    
    x, y = xCenter-w2//2, yCenter-h2//2;
    
    x2 = x + w2;
    y2 = y + h2;
    
    if x2 > wScreen or x < 0:
        xCenter = wScreen // 2;
        x = xCenter-w2//2;
    
    if y2 > hScreen or y < 0:
        yCenter = hScreen // 2;
        y = yCenter-h2//2;
    
    window.geometry("+%d+%d" % (x, y));
    window.deiconify();




if __name__ == "__main__":

    #try:
    
    from tkinter import Tk, Toplevel, Button;
    
    #except ImportError:
    #    from Tkinter import Tk, Toplevel, Button;

    root = Tk();
    root.geometry("500x300");
    root.title("testing center window function");

    def testCenterWin():

        win2 = Toplevel(root);
        win2.geometry("200x150");

        win2.transient(root);

        center_window(root, win2);

        win2.focus_set();

    Button(root, text="Test Center Window", command=testCenterWin).pack();

    root.mainloop();
        















