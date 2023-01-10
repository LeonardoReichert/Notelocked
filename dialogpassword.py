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

from tkinter import Toplevel,Frame,Label, BitmapImage;
from tkinter.ttk import Entry, Button;


from hashlib import new as newSha;
from hashlib import algorithms_available;

import ext_funcs;


default_sha = "sha256";

_msg_warn = "Do not forget the password, will be impossible to recover";

_BP_EYEOPEN = """#define image_width 21
#define image_height 21
static char image_bits[] = {
0xff,0xff,0x1f,0xff,0xff,0x1f,0xff,0xff,0x1f,0xff,0xff,0x1f,0xff,0xff,0x1f,
0x7f,0xc0,0x1f,0x0f,0x00,0x1e,0xc3,0x7f,0x18,0xf1,0xf3,0x11,0xf8,0xe3,0x03,
0xfc,0xe0,0x07,0xf8,0xe0,0x03,0xf1,0xf1,0x11,0xc3,0x7f,0x18,0x0f,0x00,0x1e,
0x7f,0xc0,0x1f,0xff,0xff,0x1f,0xff,0xff,0x1f,0xff,0xff,0x1f,0xff,0xff,0x1f,
0xff,0xff,0x1f
};"""

_BP_EYECLOSE = """#define image_width 21
#define image_height 21
static char image_bits[] = {
0xff,0xff,0x1f,0xff,0xff,0x1f,0xff,0xff,0x1f,0xff,0xff,0x1f,0xff,0x3f,0x1e,
0x7f,0x1c,0x1e,0x0f,0x0e,0x1f,0xc3,0x87,0x19,0xf1,0xc3,0x11,0xf8,0xe1,0x03,
0xfc,0xf0,0x07,0x78,0xf8,0x03,0x39,0xfc,0x11,0x1f,0x7e,0x18,0x0f,0x03,0x1e,
0x87,0xc3,0x1f,0xc7,0xff,0x1f,0xff,0xff,0x1f,0xff,0xff,0x1f,0xff,0xff,0x1f,
0xff,0xff,0x1f
};"""


def _isAscii(string):
    for c in string:
        if ord(c) > 127:
            return False
    return True



class _WinPassword(Toplevel):
    
    def __init__(self, master_parent, **kw):

        """
            kw: -title: optional string (title of window)
                -message: (string, label top message with a classic icon warning),
                
                -font1: optional (font of labels)
                -font2: optional (font of passwords)
                
                -showchar: default is "*"
                
                -minlenght: default is 0 (no limits)
                -maxlenght: default is 0 (no limits)
                -onlyascii: default is True, validate only ascii
                
                -asserthash: a string hash to authenticate (example:
                    a representation hash public hashlib.new("sha256", bytesPassword).hexdigest()      
                -namesha: default is "sha256",
                    used as hashlib.new(namesha, bKey).hexdisgest() method
                    
                -textbutton: default is a tuple ("Ok", "Cancel")
        """

        Toplevel.__init__(self, master_parent);

        self.withdraw(); #<- invisible
        
        self.title(kw.pop("title", "tk password"));
        self.transient(master_parent);
        self.resizable(0, 0);
        
        self.showchar = kw.pop("showchar", "*"); #black circle
        
        self.asserthash = kw.pop("asserthash", "");
        self.namesha = kw.pop("namesha", default_sha);
        
        if not self.namesha in algorithms_available:
            raise Exception("Error arg value -namesha=\"%s\" not in hashlib.algorithms_available");
        
        self.minlenght = kw.pop("minlenght", 0);
        self.maxlenght = kw.pop("maxlenght", 0);
        self.onlyascii = kw.pop("onlyascii", True);
        
        assert self.minlenght >= 0 and self.maxlenght >= 0;
        
        self._nChars = 32;

        self.entrys = {};
        self.entryVars = {};
        
        self.font = kw.pop("font1", None);
        self.fontPassword = kw.pop("font2", None);

        if "message" in kw and kw["message"]:
            Label(self, bitmap="warning", compound="left",
                  text=kw["message"], font=self.font,
                  ).pack(side="top", fill="x", expand=True, padx=5);

        frameAcpt = Frame(self);
        frameAcpt.pack(side="bottom", pady=5, padx=3);
        
        self.labelError = Label(self, fg="red", font=self.font);
        self.labelError.pack(side="bottom");

        textbuttons = kw.pop("textbutton", ("Ok", "Cancel"));
        assert type(textbuttons) == tuple and len(textbuttons)==2;

        textok, textno = textbuttons;
        lenghtBtn = max(len(textok), len(textno));
        
        btnok = Button(frameAcpt, text=textok, width=lenghtBtn,
                    command=self._accept, takefocus=False, default="active");
        btnok.grid(row=0, column=0, padx=2, ipadx=10);
        btnok.bind("<Return>", lambda e: self._accept() );

        btnno = Button(frameAcpt, text=textno, width=lenghtBtn,
               command=self.destroy, takefocus=True);
        btnno.grid(row=0, column=1, padx=2, ipadx=10);
        btnno.bind("<Return>", lambda e: self.destroy() );

        self.oldPassword = None;
        self.password = "";

        self.bpEyeClose = BitmapImage(data=_BP_EYECLOSE,foreground="gray90",background="black");
        self.bpEyeOpen = BitmapImage(data=_BP_EYEOPEN,foreground="gray90",background="black");


    def _MsgInvalidate(self):
        password = self.entrys.get("new_password").get(); #ever
        entryRee = self.entrys.get("rep_password", None); #optional
        
        entryOld = self.entrys.get("old_password", None); #optional
        
        #--- search user error ---
        if entryRee and password != entryRee.get():
            return "Error: The re-enter passwords is diferent";
        elif self.onlyascii and not _isAscii(password):
            return "Error: Invalid characters, only ASCII is accepted"
        
        #--- compare assert password ---
        if entryOld:
            if self.asserthash and \
                   newSha( self.namesha, (entryOld.get().encode()) ).hexdigest() != self.asserthash:
                return "Error: incorrect last password";
        
        elif self.asserthash and \
                 newSha( self.namesha, password.encode() ).hexdigest() != self.asserthash:
            return "Error: incorrect enter password";
        
        #--- compare lenght of new password ---
        if self.minlenght and len(password) < self.minlenght:
            return "Error: passwords lenght, need %d more chars" % (
                                        self.minlenght-len(password));
        
        elif self.maxlenght and len(password) > self.maxlenght:
            return "Error: The password max length is %d, cannot %d" % (self.maxlenght,
                                                                        len(password));
        #succes
        return "";


    def _accept(self):
        err = self._MsgInvalidate();
        if not err:
            self.password = self.entrys["new_password"].get();
            if "old_password" in self.entrys:
                self.oldPassword = self.entrys["old_password"].get();
            self.destroy();
            return;

        self.labelError.configure(text=err);
        return;


    def createEntry(self, tagKey, prompt):
        """ constructor, this create a entry and save on self.entrys
        _MsgInvalidate method is a default invalidator """
        frame0 = Frame(self);
        frame0.pack(side="top", pady=5, padx=5, expand=True, fill="x");

        Label(frame0, font=self.font,text=prompt,anchor="w").pack(side="top",fill="x",padx=5);
        
        entry = Entry(frame0, font=self.fontPassword, show=self.showchar, width=32);
        entry.pack(side="left", expand=True, fill="x");
        #entry.pack_propagate(0);

        self.entrys[tagKey] = entry;

        entry.bind("<Return>", lambda e: self._accept() );
        entry.bind("<KeyPress>", lambda e: self.labelError.configure(text="") );
        entry.bind("<<Copy>>", lambda e: self._ignoreCopy(entry));
        
        instantBtnShow = Label(frame0, image=self.bpEyeClose);
        instantBtnShow.pack(side="right", before=entry);
        instantBtnShow.bind("<ButtonPress-1>", lambda e: self._openEye(entry, instantBtnShow));
        instantBtnShow.bind("<ButtonRelease-1>", lambda e: self._closeEye(entry, instantBtnShow));


    def _ignoreCopy(self, entry):
        if entry["show"] == self.showchar: #is hidden, cannot copy
            self.clipboard_clear();
            entry.selection_clear();
            self.bell();


    def _closeEye(self, entry, label):
        entry.configure(show=self.showchar);
        label.configure(image=self.bpEyeClose);


    def _openEye(self, entry, label):
        entry.configure(show="")
        label.configure(image=self.bpEyeOpen);

        
    def waitResp(self, exitcurgrab = True):
        """ intern function, once the form is ready,
        it show and retrieves and constrains the main focus and
        returns the response of the validated inputs """

        if exitcurgrab:
            currForm = self.grab_current();
            if currForm:
                currForm.destroy();
        
        ext_funcs.center_window(self.master, self);

        self.wait_visibility();
        
        first = tuple(self.entrys.keys())[0];
        self.entrys[first].focus_set();
        
        self.grab_set();
            
        self.wait_window(self);

        if self.oldPassword != None:
            return (self.oldPassword, self.password);
        
        return self.password;


    def resetClean(self):
        """ clear all entrys """
        for k in self.entrys:
            self.entrys[k].delete(0, "end");


    def __str__(self):
        """
        return "form_password" the name of a form, use to interrupt from outside
        """
        return "form_password";




def askcreatepassword(parent, **kw):
    """ form: create a new password, return str password """

    kw["asserthash"]="";
    kw.setdefault("title", "Create password");
    kw["message"] = _msg_warn;
    
    context = _WinPassword(parent, **kw);
    
    context.createEntry("new_password", "Password:");
    context.createEntry("rep_password", "Repeat password:");
    
    resp = context.waitResp();

    return resp;


def askoldpassword(parent, asserthash, **kw):
    """ form: return password string """

    kw["asserthash"]=asserthash;
    kw.setdefault("title", "Enter password");
    kw.setdefault("onlyascii", False);
    
    context = _WinPassword(parent, **kw);
    
    context.createEntry("new_password", "Enter last password:");
    
    resp = context.waitResp();

    return resp;


def askchangepassword(parent, asserthash, **kw):
    """ form: change old password, return (str: old password, str: new passwod) """
    
    kw["asserthash"]=asserthash;
    kw.setdefault("title", "Change password");
    kw["message"] = _msg_warn;
    
    context = _WinPassword(parent, **kw);
    
    context.createEntry("old_password", "Last password:");
    context.createEntry("new_password", "New password:");
    context.createEntry("rep_password", "Repeat password:");
    
    resp = context.waitResp();
    
    if type(resp) != tuple:
        return ("", "");
    
    return resp; #tuple(old,new) 



if __name__ == "__main__":
    from tkinter import Tk,Radiobutton;

    root = Tk();
    root.geometry("320x150");
    root.title("test form password");


    def simple_test():
        psw = askcreatepassword(root);
        if not psw:
            print("creation password canceled.");
            return;
        
        print("password: %s" % psw);

        psw = askoldpassword(root, newSha(default_sha, psw.encode()).hexdigest() );
        if not psw:
            print("canceled re-enter password");
            return;

        print("re-enter password: %s\n" % psw);

        oldPsw, newPsw = askchangepassword(root, newSha(default_sha, psw.encode()).hexdigest() );
        if not (oldPsw and newPsw):
            print("canceled change-password");
            return;

        print("old password: %s\nnew password: %s" % (oldPsw, newPsw) );


    Button(root, text="test", command=simple_test).pack(pady=10);

    root.mainloop();
    




