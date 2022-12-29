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
    #python 3
from tkinter import Tk,Toplevel,Text,Frame,Label,Button,Radiobutton,IntVar,Menu,BitmapImage;
from tkinter.font import Font;
from tkinter.messagebox import askyesno;
from tkinter.ttk import Scrollbar;
#except ImportError:
    #python 2
#    from Tkinter import Tk,Toplevel,Text,Frame,Label,Button,Radiobutton,IntVar,Menu;
#    from tkFont import Font;
#    from tkMessageBox import askyesno;
#    from ttk import Scrollbar;


from webbrowser import open_new_tab; #user can open links on browser
from platform import system; #need check if SO Mac, for button right
from re import findall;

#fix for binary versions:
#from sys import exit;


import ext_funcs;
import diagram_helper;
import help_strings; #<- large strings :,) (smile)
import tiphelper;


author = "leoreichert5000@gmail.com";

version = "0.6";



ismacos = system().lower()=="darwin";

_font_order_options = ("family","size","weight","slant","underline","overstrike");


_BITMAP_GITHUB = """#define image_width 28
#define image_height 28
static char image_bits[] = {
0xff,0xff,0xff,0x0f,0xff,0xff,0xff,0x0f,0x3f,0xfe,0xf1,0x0f,0x3f,0xfc,0xf0,
0x0f,0x3f,0x00,0xf0,0x0f,0x3f,0x00,0xf0,0x0f,0x1f,0x00,0xe0,0x0f,0x1f,0x00,
0xe0,0x0f,0x1f,0x00,0xe0,0x0f,0x0f,0x00,0xc0,0x0f,0x0f,0x00,0xc0,0x0f,0x0f,
0x00,0xc0,0x0f,0x1f,0x00,0xe0,0x0f,0x1f,0x00,0xe0,0x0f,0x3f,0x00,0xf0,0x0f,
0x7f,0x00,0xf8,0x0f,0xff,0x03,0xff,0x0f,0xff,0x03,0xff,0x0f,0x9f,0x03,0xff,
0x0f,0x3f,0x00,0xff,0x0f,0xff,0x01,0xff,0x0f,0xff,0x03,0xff,0x0f,0xff,0x03,
0xff,0x0f,0xff,0x03,0xff,0x0f,0xff,0x03,0xff,0x0f,0xff,0xff,0xff,0x0f,0xff,
0xff,0xff,0x0f,0xff,0xff,0xff,0x0f
};"""


_BITMAP_BRANCH = """#define image_width 28
#define image_height 28
static char image_bits[] = {
0xff,0xff,0xff,0x0f,0xff,0xff,0xff,0x0f,0xff,0xff,0xff,0x0f,0xff,0xff,0xff,
0x0f,0x3f,0xfe,0xf1,0x0f,0x1f,0xfc,0xe0,0x0f,0x8f,0x78,0xc4,0x0f,0xcf,0x79,
0xce,0x0f,0x8f,0x78,0xc4,0x0f,0x1f,0xfc,0xe0,0x0f,0x3f,0xfe,0xf1,0x0f,0x3f,
0xff,0xf3,0x0f,0x3f,0xff,0xf3,0x0f,0x3f,0x00,0xf0,0x0f,0x3f,0x00,0xf8,0x0f,
0x3f,0xff,0xff,0x0f,0x3f,0xff,0xff,0x0f,0x3f,0xff,0xff,0x0f,0x3f,0xff,0xff,
0x0f,0x3f,0xfe,0xff,0x0f,0x1f,0xfc,0xff,0x0f,0x8f,0xf8,0xff,0x0f,0xcf,0xf9,
0xff,0x0f,0x8f,0xf8,0xff,0x0f,0x1f,0xfc,0xff,0x0f,0x3f,0xfe,0xff,0x0f,0xff,
0xff,0xff,0x0f,0xff,0xff,0xff,0x0f
};"""


###############


pattern_configtag = "(<tagconfig \"(.+)\">\n((.+ ?.+\n)+)*</tagconfig>)";

pattern_tags = "((<tag (.+?)>)(.+?)</tag>)";






class MenuCopy(Menu):
    def __init__(self, master_text):
        self.text = master_text;
        Menu.__init__(self, master_text, tearoff=False);
        self.add_command(label="Copy", command=self.cmdCopy);
        
        if ismacos:
            master_text.bind("<ButtonRelease-2>", self.postMenu, True);
        else:
            master_text.bind("<ButtonRelease-3>", self.postMenu, True);

        self.textsel = "";
        self.texttagsel = "";


    def setTextTag(self, label, text):
        """ text inside tag, example: http://example.com in 'example' """
        self.texttagsel = text;
        self.entryconfig(0, label=label);

        
    def cmdCopy(self):
        self.text.clipboard_clear();
        self.text.clipboard_append( self.textsel );

        
    def postMenu(self, event):
        text = self.texttagsel; #content selection by tag
        self.texttagsel = "";
        self.textsel = "";
        
        try:
            #have a normal selection?
            text = self.text.get("sel.first", "sel.last");
            self.entryconfig(0, label="Copy");
        except:
            pass;

        if not text:
            return;

        self.textsel = text;

        self.entryconfig(0, state="normal");
        self.post(event.x_root, event.y_root);



class DiagramsPart:
    def __init__(self, textwidget):
        
        self.diagramfile = diagram_helper.CreateHelperDiagramFile(textwidget,
                                bg="#FFFFA0", bgtitle="#FBFBFB", fg="black");
        #...
        
    def diagramBinds(self, name, tagname):
        if name == "diagramfile":
            self.diagramfile.bindOnTag(tagname);
        #...


_fontnames = {}; #global fonts created

class HelpFrame(Frame, DiagramsPart):
    """ Frame intern for help or about window """
    def __init__(self, master, themes, messages):

        Frame.__init__(self, master, bg="#AAffff"); #, width=200);
        self.pack(side="top", expand=True, fill="both");

        self.columnconfigure(0, weight=1);

        self.frame0 = Frame(self,relief="groove",bd=2,bg="#FBFBFB",width=400,height=50);
        self.frame0.grid(column=0, row=0, padx=10, pady=10, sticky="nwse");
        self.rowconfigure(0, weight=20);

        self.frame1 = Frame(self,width=400,height=240);
        self.frame1.grid(column=0, row=1, padx=10, pady=0, sticky="nwse");
        self.rowconfigure(1, weight=70);
        
        self.frame1.rowconfigure(0, weight=1);
        self.frame1.columnconfigure(0, weight=1);
        self.frame1.grid_propagate(0);

        self.frame2 = Frame(self, bg=self["bg"],width=400,height=25);
        self.frame2.grid(column=0, row=2, padx=10, pady=5, sticky="nwse");
        self.rowconfigure(2, weight=20);

        ##### fonts ####

        try:
            self.fontMark = Font(name="nameProgram", exists=True);
            self.fontTextNormal = Font(name="textNormal", exists=True);
        except:
            #first time
            self.fontMark = Font(name="nameProgram", exists=False,
                                 family="Arial", size=28, weight="bold", slant="italic");
            
            self.fontTextNormal = Font(name="textNormal", exists=False,
                                 family="Verdana", size=10);

        # buttons links
        self.frame0.columnconfigure(0, weight=1);
        self.frame0.rowconfigure((0,1), weight=1);

        self.frameLinks = Frame(self.frame0, bg=self.frame0["bg"]);
        self.frameLinks.grid(column=0, row=1, sticky="we");
        
        self.bmpGithub = BitmapImage(data=_BITMAP_GITHUB,
                                     foreground=self.frame0["bg"],background="gray60");
        self.bmpBranch = BitmapImage(data=_BITMAP_BRANCH,
                                     foreground=self.frame0["bg"],background="gray60");
        
        self.btnGit = Button(self.frameLinks, font="textNormal", text="My Github",
                fg="blue", bg=self.frame0["bg"], cursor="hand2",
                image=self.bmpGithub,compound="left", relief="flat", overrelief="ridge",
                command=lambda: self.askOpenSite("https://github.com/LeonardoReichert"),
               );
        self.btnGit.pack(side="left", padx=10);
        
        self.btnBranch = Button(self.frameLinks, font="textNormal", text="Notelocked Github",
                fg="blue", bg=self.frame0["bg"], cursor="hand2",
                image=self.bmpBranch,compound="left", relief="flat", overrelief="ridge",
                command=lambda: self.askOpenSite("https://github.com/LeonardoReichert/Notelocked"),
               );
        self.btnBranch.pack(side="left");

        tip = tiphelper.TipHelper(self);
        tip.putOn(self.btnGit, "Open Github link profile");
        tip.putOn(self.btnBranch, "Open Github link repository");

        # elements into frames

        self.lbProgName = Label(self.frame0, bg=self.frame0["bg"], text="Notelocked v"+version,
                                                                     font=self.fontMark);
        self.lbProgName.grid(column=0, row=0, sticky="we");
        
        # text body message
        
        self.text = Text(self.frame1,wrap="word",font=self.fontTextNormal,
                         bg="#FBFBFB", tabs=35, fg="black");
        self.text.grid(column=0, row=0, sticky="nsew");

        try:
            self.text.configure(cursor="");
            self.text.configure(inactiveselectbackground=self.text["selectbackground"]);
        except:
            pass;

        self.sby = Scrollbar(self.frame1,orient="vertical",command=self.text.yview);
        self.sby.grid(column=1,row=0,sticky="ns");
        self.text.configure(yscrollcommand=self.sby.set);

        self.menucopy = MenuCopy(self.text);
        
        self.ntag = 0;
        
        ##### Create Diagrams #####
        
        DiagramsPart.__init__(self, self.text);
        
        ###########################

        ##### Langs #####
        
        self.frameLangs = Frame(self.text, bg="gray90");
        
        self.text.columnconfigure(0, weight=1); # <- need for place langs to right
        self.text.grid_propagate(0); #<- need for langs frame, avoid root geometry autoexpand

        try:
            self.getvar("langtheme");
        except:
            self.setvar("langtheme", "en"); #<- default lang
        ###########################

        self.themes = themes; #<-titles
        self.msgs = list(messages);

        self.selecMsg = IntVar(value=0);
        
        index = 0;
        for theme in themes:
            Radiobutton(self.frame2,text=theme,command=self._selectMsg,
                indicatoron=False,bd=1,value=index,variable=self.selecMsg,
                        ).pack(side="left",padx=3);
            index += 1;
        
        self.stateCopy = Label(self.text,text="copied!",width=9,relief="solid",
                                    font=self.fontTextNormal,bg="#FFFFAA",bd=1);
    
        self._idEventHiddenCopy = 0;
        
        self._selectMsg();
        
        #self.wait_visibility();
        self.focus_set();


    def _selectMsg(self, msgToParse=None):
        """ Called by bottoms buttons (titles, license, etc) """
        
        if not msgToParse:
            # called by normal theme button
            index = self.selecMsg.get();
            #theme = self.themes[index]; #name of title, theme, no needed now
            msg = self.msgs[index];

            #have langs ?
            self.frameLangs.grid_forget(); #hidde langs frame container
            if type(msg) == dict: #yes, msg is a container of diferents langs
                for btnlang in self.frameLangs.winfo_children():
                    btnlang.destroy(); #clear old langs
                
                def getcmdlang(selmsg):
                    def setlang():
                        self._selectMsg(selmsg);
                    return setlang;
                
                for lang in msg:
                    msg_content = msg[lang];
                    
                    Radiobutton(self.frameLangs,text=lang.title(),bd=1,fg="black",
                           bg="#CCCCCC",selectcolor="#CCCCCC",activebackground="#CCCCCC",
                           command=getcmdlang(msg_content),indicatoron=False,
                           variable="langtheme",value=lang).pack(side="left");
                
                self.frameLangs.grid(row=0, column=0, sticky="ne");
                
                #try remember last lang
                lang = self.getvar("langtheme");
                if not lang in msg:  #<- no selected value ?
                    lang = next(iter(msg)); #<- first, default lang
                    self.setvar("langtheme", lang); #set default lang button as pressed

                msg = msg[lang];
        else:
            # called by "button lang" on theme
            msg = msgToParse;

        self.parseMessage(msg);
            

    def parseMessage(self, message):

        """ Message was selected, now need parse """

        msg = message;

        self.text.configure(state="normal");
        self.text.delete("1.0", "end");

        for tagname in self.text.tag_names():
            if tagname != "btncursor2": #tags forever
                self.text.tag_delete(tagname);

        self.tagstobind = {}; #bind tags
        
        self.parseConfigTags( help_strings._tagsconfigdefault_ );
        
        self.parseConfigTags(msg); #<- search configs <tagconfig>

        #extract <body>
        start = msg.find("<body>");
        end = msg.rfind("</body>");
            
        body = "";
        if start != -1 and end > start: #re.findall i cannot find with *\n*
            body = msg[start+len("<body>"):end];

        self.parseBody(body);

        self.parseBindTags(); 
        
        self.text.tag_bind("btncursor2", "<Enter>", self._cursor2);
        self.text.tag_bind("btncursor2", "<Leave>", self._cursorNormal);
        
        self.text.configure(state="disabled");
        
        return;


    def parseBody(self, body):
        """ parse text on body and create tags indexs """
        
        tags_result = findall(pattern_tags, body);
        
        lastend = 0; #now try extract tags and parse tags
        for allstr, _starttag, tagname, inside in tags_result:
            
            #allstr: "<tag tagname>inside</tag>"
            
            index = body.find(allstr);
            if index == -1:
                continue;
            
            body = body.replace(allstr, inside, 1);
            
            self.text.insert("end", body[lastend:index]);
            self.text.insert("end", inside, tagname);
            lastend = index + len(inside);
        
        self.text.insert("end", body[lastend:]);
            
                
    def parseConfigTags(self, msg):
        """
        apply configs <tagconfig>
        find all config tags in msg and remove,
        apply the tags config styles, create fonts .."""

        #no need re-create fonts repeated:
        
        for newconfigtag in findall(pattern_configtag, msg):
            allstr, tagname, opts, _last = newconfigtag;
            for opt in opts.split("\n"):
                if opt == "": break; #end

                line = opt.split(" ", 1);
                value="";
                if len(line)==2:
                    value = line[1];
                opt = line[0];
                    
                if opt == "font":
                    values = value.split(",");
                    fontname = values[0]; #id
                    if not fontname in _fontnames:
                        #create a first time the font, no duplicate
                        try:
                            fontargs = tuple(values[1:]);

                            # options imported from default global Font
                            font = self.fontTextNormal.copy();
                            default = font.actual();
                            #keys = tuple(default); #keys names
                            #best compatibility in Python 3.x and 2.x (dicts order):
                            keys = _font_order_options;
                            actual = dict( zip(keys, fontargs));

                            #search "defaults"
                            for k in actual:
                                if actual[k].lower() == "default":
                                    actual[k] = default[k];

                            #only apply Font changes mensioned and != Default
                            font.config(**actual);
                            
                            _fontnames[fontname] = font;
                        except Exception as msg:
                            print("debug: cannot create Font", fontname, msg, values);
                            continue;
                            #fontname = "";
                    value = fontname;
                    fontobj = _fontnames[fontname];
                    self.text.tag_config(tagname, font=fontobj);
                    continue;
                elif opt.startswith("-"): #binds
                    if not tagname in self.tagstobind:
                        self.tagstobind[tagname] = [];
                    self.tagstobind[tagname].append( (opt, value) );
                    continue;
                elif opt.startswith("//"):
                    #a comment
                    continue;

                self.text.tag_config(tagname, {opt:value});

    
    def parseBindTags(self):
        """ incoming task, apply a personalized events binds to
            tags created previous """

        ntagbind = 0;
        for tagname in self.tagstobind:
            actions = self.tagstobind[tagname];

            for action, value in actions:

                action = action.lower(); #lower letters

                #now, value is a condition, object, etc
                if action == "-binddiagram":
                    self.diagramBinds(value, tagname);
                    continue;
                #more if..

                #now, value is a value for user
                indexranges = iter( self.text.tag_ranges(tagname) );
                for iFirst in indexranges:
                    iLast = next(indexranges);

                    selvalue = value; #dont modify original, i will use on next indexs
                    
                    if ";" in selvalue: # ; separator of two values
                        selvalue, selvalue2 = selvalue.split(";", 1);
                    else:
                        selvalue2 = ""; #i will use ""(null) or "value default" 
                            
                    if selvalue == ".":
                        #value inside, content into tag <tag name>value here</tag>
                        selvalue = self.text.get(iFirst, iLast);

                    if action == "-bindcopyable":
                        self.addTextWithCopyCmd(iLast, selvalue, selvalue2 or "copy");
                        
                    elif action == "-bindcopybymenu":
                        self.bindTextCopyByMenu(iFirst,iLast,selvalue,selvalue2 or "Copy this");

                    elif action == "-bindopenweb":
                        self.bindWebOpener(iFirst, iLast, selvalue);


        self.text.tag_config("btncopy", underline=True, font=self.fontTextNormal);        


    def bindWebOpener(self, first, last, url):
        tag = "webopen%d" % self.ntag;
        self.ntag+=1;
        
        self.text.tag_add("btncursor2", first, last);
        self.text.tag_add(tag, first, last);

        self.text.tag_bind(tag, "<Button-1>", lambda e=None: self.askOpenSite(url));


    def askOpenSite(self,url):
        if askyesno(parent=self, title="Open browser",
               message="Are you want open link \"%s\" in a new tab of the web browser?" % url):
            open_new_tab(url);


    def bindTextCopyByMenu(self, first, last, text, label):
        tag = "copybymenu%d" % self.ntag;
        self.ntag+=1;
        self.text.tag_add(tag, first, last);

        def cmd(e=None):
            self.menucopy.setTextTag(label, text);

        if ismacos:
            self.text.tag_bind(tag, "<Button-2>", cmd);
        else:
            self.text.tag_bind(tag, "<Button-3>", cmd);


    def addTextWithCopyCmd(self, index, textcopy, textcmd):
        index = self.text.index(index);

        tag = "btncopy%d" % self.ntag;
        self.ntag+=1;
        
        def copythis(e):
            self._Copy(e, index, textcopy);
        
        self.text.insert(index, " "); #<-separator
        self.text.insert(index+"+1c", textcmd, ("btncursor2", "btncopy", tag));

        self.text.tag_bind(tag, "<Button-1>", copythis); #clic event


    def _cursor2(self, event=None):
        self.text.configure(cursor="hand2");

        
    def _cursorNormal(self, event=None):        
        self.text.configure(cursor="");


    def _Copy(self, event, index, string):
        """ event copy by user, add a tag message 'copied' """
        self.clipboard_clear();
        self.clipboard_append(string);

        m = self.fontTextNormal.metrics();
        d = m["descent"];
        height = m["linespace"]+d;
        x,y,w,h = self.text.bbox(index);

        w = self.fontTextNormal.measure("_")*9; #self.stateCopy.winfo_width();

        self.stateCopy.place(x=event.x-w//2, y=y-height-d*2, height=height);
        
        if self._idEventHiddenCopy:
            self.after_cancel(self._idEventHiddenCopy);
            
        self._idEventHiddenCopy = self.after(1000, self.stateCopy.place_forget);




class HelpFrameSecond(HelpFrame):
    """ frame component, when use the program """
    def __init__(self, master, themes, messages):
        HelpFrame.__init__(self, master, themes, messages);
        
        self.btnClose = Button(self.frame2, bd=1, text="Close", command=self.master.destroy);
        self.btnClose.pack(side="right", padx=15);



class HelpForm(Toplevel):
    """ window Help, About: when use the program (by menu), after use the program """
    def __init__(self, master, title, themes, messages):

        Toplevel.__init__(self, master);
        
        self.title(title);
        self.geometry("580x420");
        self.minsize(550,420);
        self.maxsize(800,530);
        self.transient(master);
        
        ext_funcs.center_window(master, self);

        frame = HelpFrameSecond(self, themes, messages );

        self.focus_set();
        self.grab_set();

    def __str__(self):
        return "help_form"; #for interrupts from outside


class LicenceShowForm(Tk):
    """ window, when start the program, first time """
    def __init__(self, title, themes, messages):

        Tk.__init__(self);

        self.withdraw();
        
        self.title(title);
        self.geometry("580x420");
        self.minsize(550,420);
        self.maxsize(800,530);

        self.frame = HelpFrame(self, themes, messages );

        self.btnAcept = Button(self.frame.frame2, text="Ok", command=self.destroy);
        self.btnAcept.pack(side="right", padx=10, ipadx=20);

        #self.protocol("WM_DELETE_WINDOW", self.No);

        self._centerToScreen();


    def _centerToScreen(self):
        self.update_idletasks();
        
        width, height = self.winfo_width(), self.winfo_height();
        centerX, centerY = self.winfo_screenwidth()//2,self.winfo_screenheight()//2;

        x = centerX-width//2;
        y = centerY-height//2;

        self.geometry("+%d+%d" % (x,y));

        self.deiconify();




def About(master):
    return HelpForm(master, "About",
                            ("About","Licence"),
                          ({"en": help_strings._about_,
                            "es": help_strings._about_esp_}, help_strings._license_),
                    );


def Help(master):
    return HelpForm(master, "Help",
                            ("Help",),
                              ({"en": help_strings._help_,"es": help_strings._help_esp_},),
                    );



def FirstTimeLicense(config_save):
    
    win = LicenceShowForm("License",
                            ("Licence", "About", "Help"),
                            (help_strings._license_,
                             {"en": help_strings._about_,"es": help_strings._about_esp_},
                             {"en": help_strings._help_,"es": help_strings._help_esp_},
                             ),
                          );
    
    win.mainloop();
    
    config_save["showed_license"] = True;
    config_save.save();
    
    _fontnames.clear();
    
    return;


if __name__ == "__main__":

    #try:

    from tkinter import Tk;
    
    #except ImportError:
    #    from Tkinter import Tk;

    root = Tk();

    root.geometry("250x100");
    root.title("dev:: test");

    about_cmd = lambda: About(root);
    help_cmd = lambda: Help(root);

    Button(root, text="About", command=about_cmd).pack();
    Button(root, text="Help", command=help_cmd).pack();

    root.mainloop();






