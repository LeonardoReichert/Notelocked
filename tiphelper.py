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



#try:

from tkinter import Toplevel,Label;

#except ImportError:
#    from Tkinter import Toplevel,Label;



class TipHelper(Toplevel):
    """ A small label text helper, appears by cursor mouse enter in a widget """
    def __init__(self, master):
        Toplevel.__init__(self, master, relief="solid", bd=1);

        self.withdraw(); #invisible
        self.overrideredirect(True); #no-border or title

        self.label = Label(self, bg="#FFFFA0"); #yellowed butter color :)
        self.label.pack(side="top", fill="both", expand="yes");

        self._lastEventId = 0;


    def putOn(self, widget, text, anchor="s"):
        """ put a event enter/leave by user mouse in a widget"""
        #add = True -> (no replace a posible previous event)
        widget.bind("<Enter>",lambda e: self._enterOn(e, text, anchor), add=True);
        widget.bind("<Leave>",lambda e: self._showOff(), add=True);
        widget.bind("<ButtonPress>",lambda e: self._showOff(), add=True);
        assert anchor in ("s", "n"), "anchor invalid"


    def _enterOn(self, e, text, anchor):
        """intern, parse event enter by user mouse"""
        
        def showOn(): #temporalized
            self.label.configure(text=text);
            
            wmid = self.winfo_width()//2;
            x = self.winfo_pointerx()-wmid; #mouse x - width//2

            height = max(self.winfo_height(), 24);
            hmid = max(height, 24)//2;

            if anchor == "n":
                y = e.widget.winfo_rooty()-height-5;
            elif anchor == "s":
                y = e.widget.winfo_rooty()+e.widget.winfo_height()+5; #y2 (Bottom)
            #elif...
            else:
                y = self.winfo_pointery()+hmid; #mouse y + height//2
            
            self.geometry("+%d+%d" % (x,y));

            self.deiconify(); #show

        self._lastEventId = self.after(1500, showOn); #need mouse 1500ms inside of widget


    def showNow(self, widget, text, anchor, duration_ms=1500):
        """
        Show label on a widget now inmediatelly, without events.
        
        Cannot use after .putOn(..) method was used before,
        need create other instance """

        assert anchor in ("w", "s"), "ivalid anchor";

        if self._lastEventId:
            self.after_cancel(self._lastEventId);

        self.label.configure(text=text);
        
        widget.bind("<ButtonPress>",lambda e: self.withdraw(), add=True);

        x = widget.winfo_rootx();
        y = widget.winfo_rooty();

        if anchor == "w":
            width = widget.winfo_width();
            self.geometry("+%d+%d" % (x+width+2,y));
        elif anchor == "s":
            height = widget.winfo_height();
            self.geometry("+%d+%d" % (x,y+height+2));
        #elif...

        self.deiconify(); #show
        self._lastEventId = self.after(duration_ms, self.withdraw); #event wait for hidden

        

    def _showOff(self):
        """intern, parse event leave by user mouse"""
        self.after_cancel(self._lastEventId);
        self.withdraw(); #invisible

    def __str__(self):
        return "tiphelper"


if __name__ == "__main__":

    #try:
    
    from tkinter import Tk, Button;
    
    #except:
    #    from Tkinter import Tk, Button;

    root = Tk();
    root.title("testing TipHelper");
    root.geometry("200x150");

    def clic():
        tip2.showNow(button, "<- by clic", "w");

    button = Button(root, text="1- click me", relief="solid", command=clic);
    button.pack(side="top", pady=10);
    
    button2 = Button(root, text="2- enter mouse here", relief="solid");
    button2.pack(side="top", pady=10);

    button3 = Button(root, text="3 - and here", relief="solid");
    button3.pack(side="top", pady=10);
    
    tip = TipHelper(root);
    tip2 = TipHelper(root);

    tip.putOn(button2, "this label is the effect test", "s");
    tip.putOn(button3, "this label\ncontain multiple lines", "s");
    
    root.mainloop();







