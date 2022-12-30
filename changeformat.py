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
from tkinter import (Toplevel, Label,Entry, Frame,
                              Text, Spinbox, Menu, Spinbox,
                             StringVar, BooleanVar, LabelFrame);
from tkinter import Button as tkButton;
from tkinter.font import Font, families;
from tkinter.ttk import Combobox,Button,OptionMenu,Separator,Checkbutton;
from tkinter.colorchooser import askcolor;
#except ImportError:
#    from Tkinter import (Toplevel, Label,Entry, Frame,
#                              Text, Spinbox, Menu, Spinbox,
#                             StringVar, BooleanVar, LabelFrame);
#    from Tkinter import Button as tkButton;
#    from tkFont import Font, families;
#    from ttk import Combobox,Button,OptionMenu,Separator,Checkbutton;
#    from tkColorChooser import askcolor;


from string import hexdigits;

import ext_funcs;
import tiphelper;




def ishex( strval):
    return (not -1 in [hexdigits.find(c) for c in strval]); #true if str is hex


def iscolor(strval):
    """string is a color #00ff00 ? True """
    if len(strval)==7 and strval[0]=="#" and ishex(strval[1:]):
        return True;
    return False;





FILENAME_STYLES = "userstyles000.dat";

NAME_STYLE_LENGHT = 28; #max lenght


EXAMPLE_TEXT = "This is an...\n\
\texample text... In the summer the chickens ate corn...";


#human display easy values:
OPTS_DISPLAY_FRIENDLY = {"bg": "Background=BG",
                        "fg": "Text",
                        "selectforeground": "Selected Text",
                        "selectbackground": "Selected BG",
                        "insertbackground": "Cursor insert"};


#default styles:
createdStyles = {"Black & White": {"bg": "#303030",
                                   "fg": "#FFFFFF",
                                   "selectforeground": "#95F0E0",
                                   "selectbackground": "#555575",
                                   "insertbackground": "white"},

                "Black & Green": {"bg": "#202020",
                                  "fg": "#15FF8A",
                                  "selectforeground": "white",
                                  "selectbackground": "#0070AA",
                                  "insertbackground": "white"},

                "Green Retro": {"bg": "#202000",
                                "fg": "#15FF8A",
                                "selectforeground": "#FFFF40",
                                "selectbackground": "#009F00",
                                "insertbackground": "yellow"},

                "Papher Lover": {"bg": "#FFFFA6",
                                 "fg": "#282828",
                                 "selectforeground": "#FFFFFF",
                                 "selectbackground": "#007EFD",
                                 "insertbackground": "#080808"},
                 };

#reserved names, cannot edit by user
DEFAULT_STYLES = list(createdStyles);
DEFAULT_STYLES.append("Default");



_loaded_styles = False;

def LoadUserCustomStyles():

    """ One times, read styles from the file """
    
    global _loaded_styles;
    if _loaded_styles:
        #not need load two times
        return;
    _loaded_styles = True;
    
    try:
        fp = open(FILENAME_STYLES, "r");
    except:
        #print("dont load the saved styles");
        return;

    maxValues = 5;
        
    line = -1;
    while line:
        line = fp.readline();

        #name=val1;...val5;
        parts = line.split("=");
        if len(parts) != 2:
            continue;

        name, valuepart = parts;

        if len(name) > NAME_STYLE_LENGHT or name in DEFAULT_STYLES:
            #name very long or is reserved
            continue;

        #only valid hex colors:
        colors = [c for c in valuepart.split(";")[:-1] if iscolor(c)];

        if len(colors) != maxValues:
            continue;

        createdStyles[name] = {"bg": colors[0],
                        "fg": colors[1],
                        "selectforeground": colors[2],
                        "selectbackground": colors[3],
                        "insertbackground": colors[4]};
    
    fp.close();


LoadUserCustomStyles(); #load from file




def SaveUserCustomStyles():
    #small and simplist DB

    """ Rewrite DB, append styles to small DB file .dat """

    try:
        fp = open(FILENAME_STYLES, "w");
    except:
        return;

    for name in createdStyles:
        if name in DEFAULT_STYLES: #ignore reserveds
            continue;

        s = createdStyles[name];

        ordervalues = (s["bg"],s["fg"],s["selectforeground"],
                        s["selectbackground"],s["insertbackground"]);

        #save config on 'name'=tuple options
        fp.write("\n"+name+"=");
        for value in ordervalues:
            fp.write(value+";"); #example: Name=#00ff00;...  #ff00ff;
        
    fp.close();



class MenuStyleCreator(Toplevel):
    """ A custom Menu for choose colors """
    def __init__(self, master, master_button, namekey, font=None):

        Toplevel.__init__(self, master, borderwidth=2, relief="raised");

        self.withdraw(); #makeme invisible

        self.overrideredirect(True);

        self.font = font;

        self.labelTop = Label(self, text="Text style color", font=self.font);
        self.labelTop.grid(row=1, column=0, sticky="ew",pady=2);
        self.frameOptions = Frame(self, borderwidth=1, relief="sunken", bg="#E5E5E5");
        
        self.frameSave = Frame(self);
        
        self.entryName = Entry(self.frameSave, font=self.font);
        self.entryName.insert(0, namekey);
        self.entryName.pack(side="top", fill="x", expand=True, pady=3);

        self.frameActions = Frame(self.frameSave);

        tkButton(self.frameActions,text="Save", font=self.font,command=self.saveChanges, width=6,
                 bg="#E5E5E5",relief="groove",
               ).pack(side="left", fill="x", expand=True);
        
        if not namekey in DEFAULT_STYLES:
            tkButton(self.frameActions,text="Delete", font=self.font,command=self.styleDelete,
                     bg="#E5E5E5",relief="groove",
                   ).pack(side="left", fill="x", expand=True);
        
        tkButton(self.frameActions,text="Cancel", font=self.font,command=self.destroy,
                 bg="#E5E5E5",relief="groove",
               ).pack(side="left", fill="x", expand=True);

        self.frameActions.pack(side="top", fill="x");
        
        self.name = namekey;
        self._loadStyle();

        self.frameOptions.grid(row=2, column=0, sticky="nes");
        self.frameSave.grid(row=3, column=0, sticky="nesw");

        self.post(master_button);

        # --- bind --- :

        self.bind("<FocusOut>", self.destroyByFocus );
        self.bind("<Escape>", self.destroyByFocus );
        self._userIsChoosingColor = False;

        self.tiphelp = tiphelper.TipHelper(self);


    def post(self, button_widget):
        
        # --- post, place menu --- :
        
        self.update_idletasks(); #need geometry

        width, height = self.winfo_reqwidth(), self.winfo_reqheight();
        x = button_widget.winfo_rootx()+button_widget.winfo_width();
        y = button_widget.winfo_rooty();
        
        x = x-width;
        y = y-height;

        if y < -self.labelTop.winfo_height()//2:
            #it's too high, need put on bottom
            y = button_widget.winfo_rooty() + button_widget.winfo_height();

        self.geometry("+%d+%d" % (x,y));

        self.deiconify();
        self.focus_set();
        

    def destroyByFocus(self, event=None):
        focusWin = self.focus_get();
        
        for win in self.winfo_children():
            if focusWin in win.winfo_children():
                return;
        
        if self._userIsChoosingColor:
            return;
        
        self.destroy();


    def validateColors(self):
        """ validate colors on all entrys """
        options = self.select.copy();
        for opt in options:
            entry = self.entrys[opt];
            value = entry.get();
            if not iscolor(value): #(incorrect value ?)
                
                #correct color entry:
                if not value.startswith("#"):
                    entry.insert(0,"#");
                    value = "#"+value;
                    
                if len(value) > 7:
                    entry.delete(7, "end");
                elif len(value) < 7:
                    entry.insert("end", "0"*(7-len(value)));

                #find error index
                for ch in value:
                    if not ch in "#"+hexdigits:
                        index = value.find(ch);
                        entry.select_range(index, index+1);
                        entry.icursor(index+1);
                        break;
                
                self.bell(); #<-sound
                entry.focus_set();
                self.tiphelp.showNow(self.entrys[opt],
                  "Invalid color: need only HEX numbers\nfrom #000000 to #FFFFFF", "s", 3000);
                
                return;
            options[opt] = value; #save
        return options;


    def styleDelete(self):
        name = self.entryName.get();
        if not name in DEFAULT_STYLES and name in createdStyles:
            self.master._delStyle(name);
            self.destroy();


    def saveChanges(self):
        """save changes in memory, not in file"""

        if self._makeDefaultAlt(): #<-user cannot select a invalid save name
            self.bell();
            return;

        options = self.validateColors(); #<-dict valid
        if not options:
            return;
        
        name = self.entryName.get();
        
        if not name in createdStyles:
            #save and create a new name key style
            self.master._addStyle(name);
        createdStyles[name] = options;

        self.destroy();
        self.master.varColorStyle.set(name);
        self.master.testColor(); #<- update


    def c2chtml(self, color):
        """ tranform color to html, example:
        yellow to: #ffff00
        >>> root.winfo_rgb("yellow");
        (65535, 65535, 0)
        (65535/256, 65535/256, 0/256)
         0xff 0xff 0x0
         #ffff00
        """
        try:
            rgb = self.winfo_rgb(color); #< invalid color ? error
            return "#%02x%02x%02x"% (int(rgb[0]/256),int(rgb[1]/256),int(rgb[2]/256));
        except:
            return "";


    def _loadStyle(self):
        self.select = createdStyles[self.name];

        self.entrys = {};
        
        r = 0;
        for opt in self.select:
            color = self.c2chtml( self.select[opt] ).upper();
            
            Label(self.frameOptions, font=self.font, text=OPTS_DISPLAY_FRIENDLY[opt]+":",
                  bg=self.frameOptions["bg"],
                  ).grid(row=r, column=0, sticky="e");
            
            self.entrys[opt] = Entry(self.frameOptions, font=self.font, justify="center", width=8);
            self.entrys[opt].grid(row=r, column=1);
            self.entrys[opt].insert(0, color);
            
            btn = tkButton(self.frameOptions, font=self.font, bg=color, text="", bd=1, relief="solid", cursor="hand2");
            btn.grid(row=r, column=2, ipadx=6, padx=2,pady=2);

            btn.configure(command= self._chooserColor(btn,self.entrys[opt]) );
            
            r+=1;


    def _chooserColor(self, btn, entry):
        def tryChange():
            # control focus, cancel the automatic exit, this class is a customized menu
            self._userIsChoosingColor = True;
            color = askcolor(entry.get(), parent=self);
            self._userIsChoosingColor = False;
            
            rgb, chtml = color;

            if not chtml: #user cancel
                return;
            
            try:
                btn.configure(bg=chtml);
            except:
                return;
            
            entry.delete(0, "end");
            entry.insert(0, chtml.upper());
            
        return tryChange;


    def _makeDefaultAlt(self):
        """names 'Default'.. styles is reserved,
                generate alternative 'Default(Num)' """
        
        name = self.entryName.get();
        
        alt = 0;

        if not name:
            self.entryName.insert(0, "#Name");
            #self._makeDefaultAlt(); #<- recursive

        elif len(name) > NAME_STYLE_LENGHT:
            self.entryName.delete(0, "end");
            self.entryName.insert(0, name[:NAME_STYLE_LENGHT]);
            self.tiphelp.showNow(self,"Style name: %d max length"%NAME_STYLE_LENGHT,"s",3000);
        elif name in DEFAULT_STYLES:
            nameAlt = name;
            alt = 1;
            while nameAlt in DEFAULT_STYLES:
                nameAlt = "%s(%d)" % (name,alt);
                alt += 1;

            #edited name succes
            self.entryName.delete(0, "end");
            self.entryName.insert(0, nameAlt);
            #self.tiphelp.showNow(self, "Choose other Style name: \"%s\" is reserved"%name, "s", 3000);
            #name = nameAlt;
        else:
            return False; #<-no need alternative, name is correct
            
        self.entryName.focus_set();
                    
        return True;




class FormatConfig(Toplevel):
    def __init__(self, master, text_widget, font_obj, config_obj):

        #try load from file styles DB
        LoadUserCustomStyles();

        Toplevel.__init__(self, master);

        self.withdraw();
        
        self.title("Format");
        self.geometry("480x340");
        self.minsize(480,340);
        self.maxsize(520,380);
        self.transient(master);
        
        fontOptions = font_obj.actual(); #copy config font used in example font
        
        self.fontToConfig = font_obj;
        self.saveText = text_widget;
        self.config_save = config_obj;
        
        families_sorted = list( families() );
        families_sorted.sort();
        #families_sorted = [fam for fam in sorted(families_sorted) if not fam.startswith("@")];
        
        frameFont = LabelFrame(self, text="Font",width=180,height=120,bd=0,labelanchor="n");
        frameFont.grid(column=0, row=0, sticky="nwse", padx=5, pady=5);
        frameFont.rowconfigure((0,1,2,3), weight=1);
        frameFont.columnconfigure((0,1,2), weight=1);
        frameFont.grid_propagate(0);
        
        self.rowconfigure(0, weight=10);
        self.rowconfigure(1, weight=8);
        self.rowconfigure(2, weight=4);
        self.columnconfigure(0, weight=10);
        self.columnconfigure(1, weight=2);
        self.columnconfigure(2, weight=10);
        
        self.varFamily = StringVar(value=fontOptions["family"]);
        self.optFamily = Combobox(frameFont, textvariable=self.varFamily,values=families_sorted,
                                  exportselection=False, width=25, state="readonly");
        self.optFamily.grid(column=0, row=1, columnspan=3, sticky="nwe", padx=10, pady=5);

        
        Label(frameFont, text="Size:",anchor="w").grid(column=0, row=2, sticky="nwse");
        self.varFontSize = StringVar(value=fontOptions["size"]);
        self.entryFontSize = Spinbox(frameFont, to=60, increment=1, width=4,
                                     textvariable=self.varFontSize, justify="center");
        self.entryFontSize["from"] = 1;
        self.entryFontSize.grid(column=0, row=3, sticky="nwse", padx=5, pady=3);
        
        Label(frameFont, text="Font style:",anchor="w").grid(column=1, row=2, sticky="nws");
        
        self.varWeight = StringVar(value=fontOptions["weight"]);
        self.checkBold = Checkbutton(frameFont, variable=self.varWeight, text="Bold",
                                    offvalue="normal", onvalue="bold", command=self.testFont);
        self.checkBold.grid(column=1, row=3, sticky="nwse", padx=5, pady=3);
        
        self.varSlant = StringVar(value=fontOptions["slant"]);
        self.optSlant = Checkbutton(frameFont, variable=self.varSlant, text="Italic",
                            offvalue="roman", onvalue="italic", command=self.testFont);
        self.optSlant.grid(column=2, row=3, sticky="nwse", padx=5, pady=3);


        Separator(self, orient="vertical").grid(column=1, row=0, sticky="nswe", pady=10);


        # - Frame Format - :
        
        frameFormat = LabelFrame(self, text="Format",labelanchor="n",bd=0,width=180,height=120 );
        frameFormat.grid(column=2, row=0, sticky="nwse", padx=5, pady=5);
        frameFormat.rowconfigure((0,1,3), weight=12);
        frameFormat.rowconfigure((2,4), weight=32);
        
        frameFormat.columnconfigure(0, weight=100);
        frameFormat.columnconfigure(1, weight=50);
        
        frameFormat.grid_propagate(0);

        
        Label(frameFormat,text="End line by:",anchor="w", width=16,
              ).grid(column=0,row=0,sticky="nw");
        self.varEndLine = StringVar(value = str(self.config_save["end_line"]).lower().title() );
        self.optEndLine = OptionMenu(frameFormat, self.varEndLine,
                                     self.varEndLine.get(),
                                     *("Char", "Word"));
        self.optEndLine.grid(column=0, row=1, sticky="swe", pady=3);

        
        Label(frameFormat, text="Tabs spaces:", anchor="w",
              ).grid(column=1, row=0,sticky="sw");
        
        self.varNumTabs = StringVar(value=self.config_save["space_tabs"]);
        self.entryNumTabs = Spinbox(frameFormat, to=20, increment=1, width=4,
                                     textvariable=self.varNumTabs, justify="center");
        self.entryNumTabs["from"] = 1;
        self.entryNumTabs.grid(column=1, row=1, sticky="swn", padx=3, pady=3);
        
        self._captureDefKw(); #<- capture default options for widgets Text
        
        #--- name styles combo ---
        
        Label(frameFormat, text="Color style:", anchor="w").grid(column=0, row=2, sticky="sw");
        
        nameColors = self.config_save["colors"]; #Default, Black & Green, etc...
        if nameColors != "Default" and not nameColors in createdStyles:
            nameColors = "Default";

        
        self.varColorStyle = StringVar(value=nameColors);
        self.optColorStyle = OptionMenu(frameFormat, self.varColorStyle,
                                     nameColors,
                                     *tuple(createdStyles));
        
        self.optColorStyle.grid(column=0, row=3, sticky="swe", pady=3);
        
        self.btnConfigStyle = tkButton(frameFormat,text="{..}",command=self.configStyle,width=4,
                                       relief="flat",bd=1,overrelief="ridge");
        self.btnConfigStyle.grid(column=1, row=3, sticky="sw", pady=3);


        tkeventvars = (self.varFamily, self.varFontSize, self.varEndLine,
                         self.varNumTabs);

        for tkvar in tkeventvars:
            if hasattr(tkvar, "trace_add"):
                tkvar.trace_add("write", self.testFont);
            else:
                tkvar.trace("w", self.testFont);

        if hasattr(self.varColorStyle, "trace_add"):
            self.varColorStyle.trace_add("write", self.testColor);
            
        try:
            self.fontTest = Font(name="testing", exists=True);
        except:
            #first time, it is innecesary
            self.fontTest = Font(name="testing", exists=False, **fontOptions);
            
        # - the text of test - 
        frameExample = LabelFrame(self, text="Example",relief="groove",width=200,height=120);
        frameExample.grid(column=0, row=1, columnspan=3, sticky="nwse", padx=5, pady=5);
        frameExample.grid_propagate(0);
        frameExample.rowconfigure(0, weight=1);
        frameExample.columnconfigure(0, weight=1);
        
        sp = " " if bool(self.fontTest.metrics()["fixed"]) else "0" #fixed spaces?
        tabwidth = self.fontTest.measure(sp)*self.config_save["space_tabs"];

        self.textExample = Text(frameExample, wrap=self.config_save["end_line"],
                                takefocus=False, font=self.fontTest, relief="flat",
                                tabs=tabwidth);
        
        self.textExample.insert("0.0", EXAMPLE_TEXT);

        self.textExample.configure(**createdStyles[ nameColors ]);
        self.textExample.configure(state="disabled");
        self.textExample.grid(row=0,column=0,sticky="nwse",padx=3,pady=3);
        #self.textExample.grid_propagate(0);


        # - buttons -
        
        frameButtons = Frame(self);
        frameButtons.grid(column=0, columnspan=3, row=2, sticky="nswe", padx=8, pady=8);
        
        buttonRest = Button(frameButtons, text="Default", command=self.resetDefault);
        buttonRest.pack(side="left",padx=5);
        
        buttonCancel = Button(frameButtons, text="Cancel", command=self.destroy);
        buttonCancel.pack(side="right",padx=5);
        
        buttonApply = Button(frameButtons, text="Apply", command=self.saveChanges);
        buttonApply.pack(side="right",padx=5);
        
        self.deletedStyles = [];
        
        ### TIP HELPER BINDS ###
        self.tipHelper = tiphelper.TipHelper(self);
        self.tipHelper.putOn(self.optFamily, "Letter font name");
        self.tipHelper.putOn(self.entryFontSize, "Font size in the text editor");
        self.tipHelper.putOn(self.checkBold, "Bold highlight font type");
        self.tipHelper.putOn(self.optSlant, "Italic style font type");
        self.tipHelper.putOn(self.optEndLine, "How a line ends, by letter or word");
        self.tipHelper.putOn(self.entryNumTabs, "Number of spaces per tabs");
        self.tipHelper.putOn(self.optColorStyle, "Color style profile for text editing");
        self.tipHelper.putOn(self.btnConfigStyle, "Change or create color style profile");
        self.tipHelper.putOn(buttonRest, "Reset all settings");
        self.tipHelper.putOn(buttonApply, "Acept & save all changes");
        self.tipHelper.putOn(buttonCancel, "Cancel all changes");
        
        ########################
        
        ext_funcs.center_window(master, self);
        
        # --- set focus ---
        currForm = self.grab_current();
        if currForm:
            currForm.destroy();
        self.grab_set();
        
        self.focus_set();
        
        #necesary for python 2.x:
        for index in range(self.optColorStyle["menu"].index("end")+1):
            #set default variable, on python 2.xx this var is not setted
            self.optColorStyle["menu"].entryconfig(index, variable=self.varColorStyle);
            #yes, i know, python 2.x has die
            #But I didn't get documentation of exactly when tkinter changed,
            #so this solution always
            
        #self.varColorStyle.set(nameColors);

    def _addStyle(self, name):
        """ intern, by default ttk.OptionMenu cannot add a new item """
        self.optColorStyle["menu"].insert_radiobutton(0, label=name,
                            variable=self.varColorStyle, value=name,
                            command = ( lambda :self.varColorStyle.set(name) ));

    def _delStyle(self, name):
        """ intern, by default ttk.OptionMenu cannot del a item """
        if not name in createdStyles or name in DEFAULT_STYLES: #<- Default Names are reserved
            #invalidate action
            return;
        
        menu = self.optColorStyle["menu"];
        end = menu.index("end");

        for index in range(0, end+1):
            if menu.entrycget(index, "value") == name:
                menu.delete(index);
                break;

        #succes, now need select other-prev
        
        other = menu.entrycget(index, "value");
        self.varColorStyle.set(other);

        #add the deletes on a list:
        self.deletedStyles.append(name);
        #delete when user "save changes"
        

    def configStyle(self):
        """ init MenuStyleCreator by user, can choose color style """

        name = self.varColorStyle.get();
            
        win = MenuStyleCreator(self, self.btnConfigStyle, name);
        

    def resetDefault(self):
        """ user command button, reset values to default """
        self.varFamily.set("Arial");
        self.varFontSize.set("12");
        self.varEndLine.set("Word");
        self.varWeight.set("normal");
        self.varSlant.set("roman");
        self.varNumTabs.set("4")
        self.varColorStyle.set("Default")
        
    def saveChanges(self):
        """ user command button, ok, apply al changes """

        #validate tabs
        spTabs = self.varNumTabs.get();
        if not spTabs.isdigit() or int(spTabs) < 1:
            if spTabs:
                self.varFontSize.set( "" );
            self.entryNumTabs.focus_set();
            self.bell();
            return;
        spTabs = int(spTabs);

        #validate size font
        size = self.varFontSize.get();
        if not size.isdigit() or int(size) < 1:
            if size:
                self.varFontSize.set( "" );
            self.entryFontSize.focus_set();
            self.bell(); #<-sound
            return;

        #succes all validate
        
        font_opts = self.fontTest.actual();
        self.fontToConfig.configure(**font_opts);
        
        adjust_line_by = self.varEndLine.get().lower(); #<- 'word' or 'char'
        if self.saveText["wrap"] != "none": #<- master text is adjusted
            self.saveText.configure(wrap = adjust_line_by);
        
        style = self.varColorStyle.get();
        self.saveText.configure(** createdStyles[style] );

        try:
            self.saveText.configure(
                inactiveselectbackground=createdStyles[style]["selectbackground"]);
        except:
            pass;
        
        sp = " " if bool(self.fontTest.metrics()["fixed"]) else "0" #fixed spaces?
        tabswidth = self.fontTest.measure(sp)*spTabs;
        self.saveText.configure(tabs = tabswidth);
        
        self.saveText.tag_delete("counted");
        
        #succes master tk.Text updated

        # --- now need update on memory 'dict' config ---
        self.config_save.update( {"font": font_opts,
                                    "end_line": adjust_line_by,
                                    "colors": style,
                                    "space_tabs": spTabs, #change on future
                                   } );
        # succes update memory config
 
        # --- now need save styles on file ---

        for name in self.deletedStyles:
            del createdStyles[name];
            
        SaveUserCustomStyles();

        #succes
        
        self.destroy();

    def testColor(self, *event):
        name = self.varColorStyle.get();
           
        self.textExample.configure(**createdStyles[name]);



    def _captureDefKw(self):
        
        if not "Default" in createdStyles:
            t = Text();
            createdStyles["Default"] = {
                                "bg": t["bg"],
                                "fg": t["fg"],
                                "selectforeground": t["selectforeground"],
                                "selectbackground": t["selectbackground"],
                                "insertbackground": t["insertbackground"],
                                };
            t.destroy();

        
    def testFont(self, *event):
        self.textExample.configure(wrap=self.varEndLine.get().lower());

        #--- font ---
        size = self.varFontSize.get();
        if not size.isdigit() or int(size) < 1:
            if size:
                self.varFontSize.set( "" );
                self.bell(); #<-sound while user editing
        else:
            self.fontTest.configure(family=self.varFamily.get(),
                                    size=size,
                                    weight=self.varWeight.get(),
                                    slant=self.varSlant.get(),
                                    );
        
        #--- N spaces by tabs ---
        nTabs = self.varNumTabs.get();
        if not nTabs.isdigit() or int(nTabs) < 1:
            if nTabs:
                self.varNumTabs.set( "" );
                self.bell(); #<-sound while user editing
        else:
            sp = " " if bool(self.fontTest.metrics()["fixed"]) else "0" #fixed spaces?
            tabwidth = self.fontTest.measure(sp)*int(nTabs);
            self.textExample.configure(tabs=tabwidth);






if __name__ == "__main__":

    #try:
    from tkinter import Tk;
    #except ImportError:
    #    from Tkinter import Tk;
    
    root = Tk();
    root.title("Test format");
    root.geometry("400x200");
    
    myfont = Font(font=("Courier", 11));
    
    frametext = Frame(root, bg="gray40");
    #testing,
    #Text widget need a frame, because Text is autoadjust geometry of root
    frametext.grid(column=0, row=0, sticky="nwse");
    frametext.columnconfigure(0, weight=1);
    frametext.rowconfigure(0, weight=1);
    frametext.grid_propagate(0)

    mytext = Text(frametext, font=myfont, width=1, height=1);
    mytext.insert("0.0", "is a test changing font");
    mytext.grid(column=0, row=0, sticky="nwse", padx=10, pady=10);

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=3)
    #mytext.grid_propagate(0)
    root.grid_propagate(0)

    import configsave;
    
    cnf = configsave.Configuration();
    
    def configure():
        win2 = FormatConfig(root, mytext, myfont, cnf);
        #win2.wait_window(win2);
        #print("cnf", cnf);
    
    Button(root, text="test format", command=configure).grid(column=0, row=1)
    root.rowconfigure(1, weight=1)

    root.mainloop();

    


