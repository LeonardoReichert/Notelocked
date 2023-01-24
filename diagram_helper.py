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

from tkinter import Canvas, Frame;
from tkinter.font import Font;

#except ImportError:
#    from Tkinter import Canvas, Frame;
#    from tkFont import Font;




_struct_file = (
        {"FILE Metadata v0.7":
                (
                "0 - Unique header...................",
                "1 - File version....................",
                "2 - Name hash (sha256)..............",
                "3 - Hash of password................",
                "4 - Comment MODE_CBC................",
                "5 - Encoding of text used...........",
                "6 - Hash of: \n  (password+vector+encrypted) =\n   Check data originality",
                "7 - Vector Random...................",
                "<rectdashed>",
                '8 - Encrypted plain text.\n\
Key used (32 secret bytes):\n\
hash of(password+hash of password)',
                )
        },
);


_ndiag = 0; #global, its used for add a unique tag name in Canvas

class SimpleDiagram(Canvas):
    def __init__(self, textwidget,struct,**kw):
        """
        bg or backbround: the color of background
        bgtitle: the color of background title
        bg or backbround: the color of background
        fg or foreground: the color of texts, default: "black"
        """

        self.text = textwidget;

        #need the superior window master, discard sub-widgets:
        master = self.text.master;
        while master and not master.winfo_class() in ("Toplevel", "Tk"):
            master = master.master;

        bg = kw.pop("bg", None) or kw.pop("backgound", None);
        bgtitle = kw.pop("bgtitle", "white");
        fg = kw.pop("foreground", "") or kw.pop("fg", "") or "black";

        self.font = Font(family="Courier", size=10);
        Canvas.__init__(self, master, bd=0,highlightthickness=0, bg=bg);

        try:
            self.configure(cursor="circle");
        except:
            pass;

        m = self.font.metrics();

        w = self.font.measure("_");

        heightFont = m["ascent"]+m["descent"];


        for dic in reversed(struct):
            for title in dic:
                items = dic[title];
                for text in reversed(items):
                    x1,y1, x2,y2 = self.bbox("all") or (0,0,0,0);
                    if text == "<rectdashed>":
                        self.move("all", w, 0);
                        self.create_rectangle(x1,y1-2, x2+w*2,y2+2,dash=2,
                                        width=1, tag="rectdashed", outline=fg);
                    else:
                        self.create_text(0,y1,fill=fg,text=text,anchor="sw",font=self.font);
                self.move("all", w, 0);
                
                if not title:
                    continue;
                
                x1,y1, x2,y2 = self.bbox("all");
                idTitle = self.create_text(w, y1, fill=fg,
                                           text=title, anchor="sw",
                                           font=self.font, tag="title");
                
                self.move(idTitle, 0, -heightFont/2);
                
                x1,y1, x2,y2 = self.bbox(idTitle);
                idRectTitle = self.create_rectangle(0,y1-2, x2+w,y2+2,
                                      width=1, fill=bgtitle, tag="rect_title", outline=fg);
                
                y1 = (y1+y2)/2;
                x2,y2 = self.bbox("all")[2:];
                self.create_rectangle(0, y1, x2+w-1, y2+w-1,
                                      width=1, fill="", tag="rect_container", outline=fg);
                
        x1,y1, x2,y2 = self.bbox("all");
        self.move("all", -x1+5, -y1+5);

        self.configure(width=x2-x1+10, height=y2-y1+10);

        self.lift("rect_container");
        self.lift("rect_title");
        self.lift("title");
        self.lower("rectdashed");

        # --- adjust rects ---
        rects = iter(reversed(self.find_withtag("rect_container")));
        first = next(rects, None); #default=None if not exists
        while first:
            nxt = next(rects, None);
            if nxt:
                x1,y1,x2,y2 = self.coords(nxt);
                x2 = self.coords(first)[2]-w;
                self.coords(nxt, (x1,y1,x2,y2));
            
            first = nxt;
        
        
        self.bind("<ButtonRelease>", lambda e: self.place_forget() ); #exit
        self.bind("<FocusOut>", lambda e: self._showOff() ); #exit


    def _showOn(self, tag):
        """ called by event Enter """
        first, last = self.text.tag_ranges(tag);
        
        x1,y1,x2,y2 = self.text.bbox(first);
        
        x = self.text.winfo_x()+x1;
        y = self.text.winfo_y()+y1+self.fontHeight+1;

        master = self.text.master;
        while master and not master.winfo_class() in ("Toplevel", "Tk"):
            x += master.winfo_x();
            y +=  master.winfo_y();
            master = master.master;
        
        self.text.configure(cursor="hand2");
        self.place(x=x, y=y);
        self.text.focus_set();

        
    def _showOff(self):
        if self.focus_get() != self:
            self.place_forget();
        self.text.configure(cursor="");


    def _showFocusedIn(self):
        wmid,hmid = self.winfo_width()//2, self.winfo_height()//2;
        wmastmid,hmastmid = self.master.winfo_width()//2, self.master.winfo_height()//2;

        self.place(x=wmastmid-wmid, y=hmastmid-hmid);

        self.focus_set();

    
    def bindOnTag(self, tag):
        global _ndiag;
        
        ranges = iter(self.text.tag_ranges(tag));

        def cmd(func, *args):
            return lambda e: func(*args);
        
        for first in ranges:
            last = next(ranges);
            
            _ndiag += 1;
            tag = "diag%d" % _ndiag
            self.text.tag_add(tag, first,last);

            self.text.tag_bind(tag, "<Enter>", cmd(self._showOn, (tag,)) );
            self.text.tag_bind(tag, "<Leave>", cmd(self._showOff) );
            self.text.tag_bind(tag, "<Button>", lambda e: self._showFocusedIn() );
        
        self.fontHeight = Font(font=self.text.tag_cget(tag, "font")).metrics()["linespace"];



def CreateHelperDiagramFile(textwidget, **kw):
    return SimpleDiagram(textwidget, _struct_file, **kw);



if __name__ == "__main__":

    #try:
    
    from tkinter import Tk, Button, Text;
    
    #except ImportError:
    #    from Tkinter import Tk, Button, Text;

    root = Tk();

    root.geometry("700x450");
    
    root.title("test diagram");

    root.configure(background="gray80");
    
    wtext = Text(root, wrap="word");
    wtext.place(x=20, y=20, width=300, height=300);

    wtext.insert("end", "this data is for programmer\n");
    wtext.insert("end", "test of widget HELPER\n");
    wtext.insert("end", "cursor here to view Technical ");
    wtext.insert("end", "Format", "diagramfile");
    wtext.insert("end", " Encryption, this is a test ");
    wtext.insert("end", "here", "diagramfile");
    wtext.insert("end", "\n");
    wtext.insert("end", "and here", "diagramfile");
    wtext.insert("end", "\nbye");
    
    wtext.tag_config("diagramfile", underline=True, foreground="blue");
    diag = CreateHelperDiagramFile(wtext);
    diag.bindOnTag("diagramfile");
    
    root.mainloop();



