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

from tkinter import Toplevel, Label, Menu, StringVar, Frame, IntVar;
from tkinter.ttk import Separator, Entry, Button, Checkbutton, Radiobutton;

#except ImportError:
#    from Tkinter import Toplevel, Label, Menu, StringVar, Frame, IntVar;
#    from ttk import Separator, Entry, Button, Checkbutton, Radiobutton;
    

from platform import system; #need check if SO is Mac, for button right

import ext_funcs;
center_window = ext_funcs.center_window;




ismacos = system().lower()=="darwin";

class MenuClipboard(Menu):
    def __init__(self, master):
        Menu.__init__(self, tearoff=False);

        self.add_command(label="Copy", command=self._copy);
        self.add_command(label="Cut", command=self._cut);
        self.add_command(label="Paste", command=self._paste);
        self.add_separator();
        self.add_command(label="Delete", command=self._delselected);


    def putInEntry(self, entry_widget):
        if ismacos:
            entry_widget.bind("<ButtonRelease-2>", self._postInEntry);
        else:
            entry_widget.bind("<ButtonRelease-3>", self._postInEntry);


    def _copy(self):
        text = self.entryNow.selection_get();
        self.clipboard_clear();
        self.clipboard_append(text);

    def _cut(self):
        self._copy();
        self._delselected();

    def _paste(self):
        self._delselected();
        self.entryNow.insert("insert", self.clipboard_get());

    def _delselected(self):
        if self.entryNow.selection_present():
            self.entryNow.delete("sel.first", "sel.last");

    def _postInEntry(self, event):
        self.entryNow = event.widget;
        
        self._cheeckentrys();
        
        self.post(event.x_root, event.y_root);

    def _cheeckentrys(self):
        if self.entryNow.selection_present():
            self.entryconfig(0, state="normal");
            self.entryconfig(1, state="normal");
            self.entryconfig(4, state="normal");
        else:
            self.entryconfig(0, state="disabled");
            self.entryconfig(1, state="disabled");
            self.entryconfig(4, state="disabled");
        
        try:
            assert self.clipboard_get();
            state="normal";
        except:
            state="disabled";

        self.entryconfig(2, state=state);

class Searcher(Toplevel):
    def __init__(self, win_master, text_widget):

        currForm = win_master.grab_current();
        if currForm:
            currForm.destroy();

        Toplevel.__init__(self, win_master);

        self.resizable(False, False);
        self.transient(win_master);
        self.title("Search");

        self.text = text_widget;

        self.frame0 = Frame(self);
        self.frame0.grid(row=0, column=0, sticky="nw", padx=5, pady=2);

        # --- variables ---
        try:
            # remember old values ?
            self.getvar(name="search_direction"); #< first time = error
            #.getvar(name="search_phrase"); search_phrase is reset from main form = never error
        except:
            # set default values
            self.setvar(name="search_phrase", value="");
            self.setvar(name="search_direction", value="end");
            self.setvar(name="search_go_round", value=1);
            self.setvar(name="search_match_case", value=0);
        
        # --- phrases ---
        
        self.frameSearch = Frame(self.frame0,pady=5);
        self.frameSearch.pack(side="top",fill="x",padx=5);
        Label(self.frameSearch,text="Search:",anchor="e").pack(side="left");
        
        self.entrySearch = Entry(self.frameSearch,textvariable="search_phrase",takefocus=True,width=25)
        self.entrySearch.pack(side="right");

        self.menuclip = MenuClipboard(self);
        self.menuclip.putInEntry(self.entrySearch);

        # --- actions ---
        
        self.frameActions1 = Frame(self);
        self.frameActions1.grid(row=0, column=1, sticky="nwe", padx=5, pady=5);
        
        Button(self.frameActions1, text="Find Next",takefocus=False, command=self.FindNext).pack(side="top", fill="x");

        self.buttonCount = Button(self.frameActions1,takefocus=False, text="Count All", width=17, command=self.CountMarkAll);
        self.buttonCount.pack(side="top", fill="x");
        
        if "counted" in self.text.tag_names():
            self.buttonCount.configure(text="Un-Count All");

        self.labelCount = Label(self, text="");
        self.labelCount.grid(column=0, row=1, columnspan=2, sticky="we");
        
        Button(self.frameActions1, text="Close",takefocus=False, command=self.destroy).pack(side="top", fill="x", pady=3);
        
        # --- direction ---
        
        self.frameDirection = Frame(self.frame0);
        self.frameDirection.pack(side="top",fill="x", padx=5, pady=10); 
        
        Label(self.frameDirection, text="Direction: ").pack(side="left");
        self.rbUp = Radiobutton(self.frameDirection,text="Up",
                                takefocus=False,variable="search_direction", value="0.0");
        self.rbUp.pack(side="left");

        self.rbDown = Radiobutton(self.frameDirection,text="Down",
                            takefocus=False,variable="search_direction", value="end");
        self.rbDown.pack(side="left");
        
        self.checkRound = Checkbutton(self.frameDirection,text="Go round",
                            takefocus=False,variable="search_go_round",onvalue=1, offvalue=0);
        self.checkRound.pack(side="left");

        #--- options ----
        Separator(self.frame0, orient="horizontal").pack(side="top", fill="x", padx=10, pady=5);
        
        self.frameOptions = Frame(self.frame0);
        self.frameOptions.pack(side="top",fill="x", padx=5);
        
        Label(self.frameOptions, text="Options: ").pack(side="left");
        
        Checkbutton(self.frameOptions, text="Match case",
                        variable="search_match_case",takefocus=False, state="normal",
                        onvalue=1, offvalue=0).pack(side="left");
        
        self.intCountLenght = IntVar(value=0);

        center_window(win_master, self);
        
        self.grab_set();
        self.entrySearch.focus_set();
        self.entrySearch.icursor("end");

        
    def FindNext(self):
        """ Search on direction, and select the finded """
        
        phrase = self.getvar("search_phrase");
        if not phrase:
            return;
        
        self.text.tag_delete("counted"); #<- marks
            
        matchCase = not self.getvar("search_match_case");
        
        to = self.getvar("search_direction");
        down = True;
        up = False;
        fromIndex = "insert";
        if to == "0.0":
            down = False;
            up = True;
            try:
                fromIndex = self.text.index("sel.first"); #if no have 'sel', 'insert' is fine
            except:
                pass;
            
        stopindex = "" if self.getvar("search_go_round") else to;
        
        indexFinded = self.text.search(phrase, index=fromIndex, stopindex=stopindex,
                            nocase=matchCase, forwards=down, backwards=up,
                            exact=True, count=self.intCountLenght);
        
        if indexFinded:
            lenght = self.intCountLenght.get();
            first, last = indexFinded.split(".");
            indexEnd = "%s.%d" % (first, int(last)+lenght);
            
            self.text.tag_remove("sel", "0.0", "end");
            self.text.tag_add("sel", indexFinded, indexEnd);
            self.text.mark_set("insert", indexEnd);
            self.text.see("insert");
            
            self.text.focus_set();
        else:
            self.text.bell(); #sound stop
            try:
                fromIndex = self.text.index("sel.first");
                self.text.focus_set();
            except:
                pass;
        
        self.text.event_generate("<<statebar>>");

    def IterFind(self, iter_callback):
        """
            Iter all content on Text widget with var "search_phrase"
                execute inter_callback(first, last) for all finded

            inter_callback need return diference modified int < 0 or  int > 0 or int == 0

        """
                  
        phrase = self.getvar(name="search_phrase");
        if not phrase:
            return -1;
        
        matchCase = not self.getvar("search_match_case");
        
        count=0;
        indexStart="0.0";
        while indexStart:
            indexStart = self.text.search(phrase,
                        index=indexStart, stopindex="end", forwards=True,
                        nocase=matchCase, count=self.intCountLenght);
            if not indexStart:
                break;
            
            count += 1;
            
            lenght = self.intCountLenght.get();
            first, last = indexStart.split(".");
            indexLast = "%s.%d" % (first, int(last)+lenght);
            
            dif = iter_callback(indexStart, indexLast); #return the modified lenght from first
            if dif: #< diferent lenght
                indexLast = "%s.%d" % (first, int(last)+dif);
            
            indexStart = indexLast;
        
        return count;

    def CountMarkAll(self):

        # -- Del Marks
        if "counted" in self.text.tag_names(): #<- alredy exists marks
            self.text.tag_delete("counted");
            self.buttonCount.configure(text="Count");
            self.labelCount.configure(text="");
            return;

        # -- Create Marks
        
        markCall = (lambda first_index, last_index:
                    self.text.tag_add("counted", first_index, last_index));
        
        count = self.IterFind(markCall);
        if count >= 0:
            self.labelCount.configure(text="Count: %d"%count);
            self.buttonCount.configure(text="Un-Count All");
            self.text.tag_config("counted", background=self.text["foreground"], foreground=self.text["background"]);
        else:
            self.labelCount.configure(text="");


class Replacer(Searcher):
    def __init__(self, win_master, text):
        self.text = text;
        Searcher.__init__(self, win_master, text);
        self.title("Find & Replace");

        try:
            self.getvar("replace_phrase");
        except:
            self.setvar("replace_phrase", "");

        self.frameReplace = Frame(self.frame0);
        self.frameReplace.pack(side="top",fill="x", padx=5, pady=5, after=self.frameSearch);
        Label(self.frameReplace, text="Replace with:", anchor="e").pack(side="left");
        self.varReplacePhrase = StringVar(name="replace_phrase");
        self.entryReplace = Entry(self.frameReplace, textvariable="replace_phrase", width=25, takefocus=True);
        self.entryReplace.pack(side="right");

        self.menuclip.putInEntry(self.entryReplace);

        Button(self.frameActions1,text="Replace All",command=self.ReplaceAll,takefocus=False,
               ).pack(side="top", fill="x", after=self.buttonCount);
        Button(self.frameActions1,text="Find & Replace",command=self.FindAndReplace,takefocus=False,
               ).pack(side="top", fill="x", after=self.buttonCount);

    def Replace(self, first, last, totext):
        """ Python 2 Tkinter.text no have "replace" method, improvise """
        if hasattr(self.text, "replace"):
            self.text.replace(first, last, totext);
        else:
            #improvise text.replace
            self.text.delete(first, last);
            self.text.insert(first, totext);

    def ReplaceAll(self):
            
        toPhrase = self.getvar("replace_phrase");
        if toPhrase == self.getvar("search_phrase"):
            self.bell(); #sound
            return;
        
        lenght = len(toPhrase);

        def replace(first, last):
            dif = lenght-(float(last)-float(first));
            self.Replace(first, last, toPhrase);
            return dif;

        count = self.IterFind( replace ); #iter
        if count >= 0:
            self.text.event_generate("<<statebar>>");
            self.labelCount.configure(text="Replaced: %d"%count);

    def FindAndReplace(self):
            
        phrase_search = self.getvar("search_phrase");
        if not phrase_search:
            return;

        phrase_replace = self.getvar("replace_phrase");
        if phrase_replace == phrase_search:
            return;

        sel_first = sel_last = "";
        try:
            sel_first = self.text.index("sel.first");
            sel_last = self.text.index("sel.last");
        except:
            pass;
        if sel_first and sel_last:
            text_sel = self.text.get(sel_first, sel_last);
            if not self.getvar("search_match_case"):
                phrase_search = phrase_search.upper();
                text_sel = text_sel.upper();
                
            if text_sel == phrase_search: #<- finded
                    #start to replace
                
                self.Replace(sel_first, sel_last, phrase_replace);
                
                first, last = sel_first.split(".");
                indexLast = "%s.%d" % (first, int(last)+len(phrase_replace));
                
                self.text.tag_remove("sel", "0.0", "end");
                self.text.tag_add("sel", sel_first, indexLast);
                self.text.mark_set("insert", indexLast);
                self.text.see("insert");

                self.text.focus_set();
            
                self.text.event_generate("<<statebar>>");
                #replace succes
            else:
                self.FindNext();
        else:
            self.FindNext();


class GoToLine(Toplevel):
    def __init__(self, master, text_widget):

        currForm = master.grab_current();
        if currForm:
            currForm.destroy();

        Toplevel.__init__(self, master);

        #ext_funcs.repl_subwin(master,  self);
        
        self.title("Go to line");
        #self.geometry("245x85");
        self.transient(master);
        self.resizable(False, False);
        
        Label(self,
            text="Enter number line 1 ... %d\n 'end' to go to the end, or 'first'"%int(
            float(text_widget.index("end-1c"))) ).grid(row=0, column=0, columnspan=2, sticky="nwe", padx=5, pady=5);

        self.text = text_widget;

        self.varGoLine = StringVar(name="go_line");
    
        try:
            #set the current line by cursor
            self.varGoLine.set( str(int(float(self.text.index("insert")))) );
        except:
            pass;
        
        self.entryLine = Entry(self, justify="left", textvariable="go_line", takefocus=True);
        self.entryLine.grid(row=1, column=0, sticky="swe", padx=10, pady=8);

        Button(self, text="Go", takefocus=True, command=self.go_to_line,
               ).grid(row=1, column=1, sticky="se", padx=5, pady=8);
        
        #_place_window(self, master);
        center_window(master, self);
        
        self.grab_set();
        
        self.entryLine.focus_set();
        self.entryLine.icursor("end");

        self.entryLine.bind("<Return>", lambda e: self.go_to_line());

    def go_to_line(self):
        index = self.varGoLine.get().lower();
        if not index.isdigit():
            if index == "first":
                index = "1.0";
            elif index == "end":
                index = self.text.index("end-1c");
            else:
                self.varGoLine.set("");
                self.bell();
                return;
        
        end = float(self.text.index("end-1c"));
        if float(index) > end:
            self.varGoLine.set(int(end));
            self.bell();
            return;
        elif float(index) < 1:
            self.varGoLine.set("1");
            self.bell();
            return;
        
        index = str(float(index));
        
        self.text.tag_remove("sel", "0.0", "end");
        self.text.mark_set("insert", index);
        self.text.see("insert");
        self.text.event_generate("<<statebar>>");
        self.text.focus_set();
        self.destroy();
        


if __name__ == "__main__":
    ####### TEST #######

    #try:
    
    from tkinter import Tk, Text;
    
    #except ImportError:
    #    from Tkinter import Tk, Text;
        
    root = Tk();
    root.title("Test:Searchers");
    root.configure(background="gray80");

    text = Text(root, takefocus=True);
    text.pack(side="top");

    try:
        text.configure(inactiveselectbackground = text["selectbackground"]);
    except:
        pass;

    text.insert("0.0", "First line\nSecond line\nEnd line?\n:)");

    search = lambda: Searcher(root, text);
    replace = lambda: Replacer(root, text);
    toline = lambda: GoToLine(root, text);


    frameActions = Frame(root, background="#90F090");
    frameActions.pack(side="bottom",ipady=5);

    Button(frameActions, text="Search", command=search).pack(side="left", padx=5);
    Button(frameActions, text="Replace", command=replace).pack(side="left", padx=5);
    Button(frameActions, text="Go To line", command=toline).pack(side="left", padx=5);


    root.mainloop();










