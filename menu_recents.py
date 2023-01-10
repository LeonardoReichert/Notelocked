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



#author: Leonardo A. Reichert
#2022

#try:

from tkinter import Menu, BooleanVar;
from tkinter.messagebox import showinfo;

#except ImportError:
#    from Tkinter import Menu, BooleanVar;
#    from tkMessageBox import showinfo;

from os.path import exists;


msgInfo = """Recent history will only remember files if you enable history.
If you choose to forget the history files, the history will remain clean.

Can use F12 to clear and turn desactive the history"""

filename_recents = "myrecents000.dat";
MAX_RECENTS = 10;

class ListRecents(list):
    """ Simple, Fast and Small DB or List of filenames recents used """
    def __init__(self, filename=filename_recents):
        list.__init__(self);
        self.filename = filename_recents;
        self._loadRecents(); #a first time

    def _loadRecents(self):
        """ Load limited last appends files by MAX_RECENTS """;
        try:
            fp = open(self.filename, "r");
        except:
            return;
        
        allLines = fp.readlines();
        fp.close();
        #no-null lines:
        allLines = [ line.replace("\n", "").replace("\r", "") for line in allLines if line ];

        for fname in allLines:
            if not fname in self and exists(fname):
                list.append(self, fname);
                if len(self) >= MAX_RECENTS:
                    break;

    def append(self, fname):
        """ put filename to end of list, and save at the end of file """;

        if len(self) and self[-1] == fname:
            #cannot abuse by Ctrl+S (save);
            return;
        
        if fname in self:
            self.remove(fname);

        list.append(self, fname);
        try:
            fp = open(self.filename, "a");
            fp.write("\n"+fname);
            fp.close();
        except:
            pass;
        
    def clear(self):
        """ Reinit DB, clear and erase all values """
        list.clear(self);
        try:
            fp = open(self.filename, "w");
            fp.close();
        except:
            pass;
        
    def compact(self):
        """ Rewrite DB and save only the last loaded values.
            Oldest values are forget. """

        try:
            fp = open(self.filename, "w");
        except:
            return;

        for fname in self:
            if exists(fname):
                fp.write("\n"+fname);

        fp.close();


GlobalRecents = ListRecents();


class MenuRecentFiles:
    def __init__(self, win, menu_master, dict_config):

        self.win = win;

        self.config = dict_config;

        self.menuRecents = Menu(menu_master, tearoff=False);
        menu_master.add_cascade(label="Recents files", menu=self.menuRecents);

        self._varNoRememberRecents = BooleanVar(value=self.config["forget_history"]);
        self.menuRecents.add_checkbutton(label="Clear & Disable History", accelerator="F12",
                            onvalue=True, offvalue=False, variable=self._varNoRememberRecents,
                            command=self._cheeck_remember);

        self.menuRecents.add_command(label="Info", command=self._showMsgInfo);

        self.iExtraRecents = self.menuRecents.index("end");
        
        if not self._varNoRememberRecents.get():
            for filename in GlobalRecents:
                self._insert_recent_option(filename, save=False);

        self.win.bind_all("<F12>", lambda e: self.clear_and_desactive());

    def clear_and_desactive(self):
        """fast force to forget historial, by user key-accelerator"""
        newState = not self._varNoRememberRecents.get();
        self._varNoRememberRecents.set(newState);
        self._cheeck_remember();

    def _showMsgInfo(self):
        showinfo(parent=self.win,title="Info", message=msgInfo);

    def _insert_recent_option(self, filename, save=True):
        """Add a new filename on menu history, or put on top if exists"""
        if self.menuRecents.index("end") == self.iExtraRecents: #first time need a sep
            self.menuRecents.insert_separator(0);
        
        if save: #<- no exists on LIST or file
            if filename in GlobalRecents: #alredy exists
                self._history_remove_val(filename); #find & remove from menu
            GlobalRecents.append(filename); #add to end & save
        
        self.menuRecents.insert_command(0, label=filename, #add to top menu
                    command=lambda: self._open_recentfilename(filename));
        
    def add_recent_history(self, filename):
        """ for humans, add a limited and sorted quantity of filenames to history if
            only the history is activated """
        
        if self._varNoRememberRecents.get():
            return;

        self._insert_recent_option(filename); #put on top

        # control limit on memory and menu
        if len(GlobalRecents) > MAX_RECENTS:
            del GlobalRecents[0];
            index = MAX_RECENTS; #last recent on menu
            if self.menuRecents.type(index) == "command":
                self.menuRecents.delete(index);
        
    def _history_remove_val(self, value):
        """ remove from menu, not from memory config """
        end = self.menuRecents.index("end") or 0;
        
        for index in range(0, end):
            
            if self.menuRecents.type(index) != "command":
                #limited by separator
                break;
            
            label = self.menuRecents.entrycget(index, "label");
            if label == value:
                self.menuRecents.delete(index);
                return;

    def _open_recentfilename(self, f):
        " it is tester, will be replace on main by Inheritance "
        print("open test", f);

    def clear_menu_history(self):
        """ clear the menu recents """
        end = self.menuRecents.index("end");
        if end < self.iExtraRecents+1:
            return;
        
        self.menuRecents.delete(0, end-(self.iExtraRecents+1));

    def _cheeck_remember(self):
        """ call by user, desactive & clear or activate historial """
        clearHistory = self._varNoRememberRecents.get();
        
        if clearHistory:
            self.clear_menu_history();
            GlobalRecents.clear();
        
        #is a new value ? cheeck if need save on file
        if self.config["forget_history"] != clearHistory:
            self.config["forget_history"] = clearHistory;
            self.config.save();

            if clearHistory:
                self.setLabelStateAction("Recents [OFF][Cleared]", 8);
            else:
                self.setLabelStateAction("Recents [ON]", 8);

    def setLabelStateAction(self, label, seconds):
        """ method tester, it is replaced from main """
        print("test", label, seconds, "seconds");
        


if __name__ == "__main__":

    print("Recents (exists)", GlobalRecents);

    #try:
    
    from tkinter import Tk, Entry, Button;
    
    #except ImportError:
    #    from Tkinter import Tk, Entry, Button;
        
    root = Tk();
    root.title("Test recents");
    root.geometry("400x200");

    import configsave;
    cnf = configsave.Configuration();

    menubar = root["menu"] = Menu(root, tearoff=False);

    menuTest = Menu(menubar, tearoff=False);
    menubar.add_cascade(label="Test", menu=menuTest);

    recents = MenuRecentFiles(root, menuTest, cnf);

    entryRecent = Entry(root);
    entryRecent.insert(0, "Testfilename.ltxt");
    entryRecent.pack(side="top", pady=10);
    
    def test():
        text = entryRecent.get();
        if text:
            recents.add_recent_history(text);

    buttonAdd = Button(root, text="Add recent", command=test);
    buttonAdd.pack(side="top", pady=10);

    root.mainloop();

    GlobalRecents.compact(); #at the end of the program







