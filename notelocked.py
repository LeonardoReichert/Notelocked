#!/usr/bin/env python

#only python >= 3x

################
#  NOTELOCKED  #
################


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


from tkinter import *;
from tkinter.simpledialog import askinteger;
from tkinter.messagebox import showwarning, askyesno, askyesnocancel;
from tkinter.font import Font;
from tkinter.filedialog import asksaveasfilename, askopenfilename;
from tkinter.ttk import Sizegrip, Separator, Scrollbar;


from hashlib import new as newSha; #sha256
from threading import Thread, Lock;
import time;
from datetime import datetime;
from platform import system; #<- need check if system is mac for button right
from sys import argv, version_info as py_version;
from os.path import basename;


#modulos from this program:
import cip_fileformat;  #cipher
import ext_funcs;       #aditional functions
import search;          #gui search, replace, go to line
import changeformat;    #change the visual, font, etc
import configsave;      #save and load the config
import help_about;      #help of program, about..
import menu_recents;    #menu of recent files
import tiphelper;       #a simple tag with help on mouse
import dialogpassword;  #dialog form for password inputs



if py_version[0] < 3:
    raise Exception("Need Python >= 3");


#En:
#At one point I was interested in making it compatible with Python2x,
#but Python2 encoders/decoders were very problematic,
#so this will only run on versions of Python3

#Es:
#En un momento me intereso hacerlo compatible con Python2x,
#pero los encoders/decoders de Python2 fueron muy problematicos,
#asi que esto solo correra en las versiones de Python3.
#Aun asi, lograr algunas retrocompatibilidades dio mejor confianza
#para evitar tener una version especifica



_helpargs = """
** Use params **

    -file:  use with a path for open a file
    -text:  use for init with a defaul text

"""



class WaitLocker:
    """ Manage sub thread to lock, auto-lock """
    def __init__(self):
        self._threadWaitLock = None;
        self.inactivity = 0;
        self.waitLockerInit = False;
        self.lockVars = Lock(); #protect GIL
        
        
    def getStateLocked(self):
        """ get state of "content" to "locked" """
        self.lockVars.acquire(True);
        v = self.locked;
        self.lockVars.release();
        return v;
        
        
    def setStateLocked(self, v):
        """ set state of "content" to "locked" """
        self.lockVars.acquire(True);
        self.locked = v;
        self.lockVars.release();
        
        
    def stop_locker_thread(self):
        """ stop the thread auto-locker"""
        self.lockVars.acquire(True);
        self.waitLockerInit = False;
        self.lockVars.release();


    def init_locker_thread(self):
        """ init or reinit thread auto-locker """
        
        self.put_activity(); #<- reinit timer
        
        if self.waitLockerInit: #a current thread locker is init, need stop
            
            self.stop_locker_thread();
            
            #print("< stoping locker Thread...", self.waitLockerInit);
            self._threadWaitLock.join(); #wait to finish the previous thread
            #print("  locker Thread ended>");
        
        self._threadWaitLock = Thread( target = self.__thread_count_inactivity );
        self.waitLockerInit = True;
        self._threadWaitLock.start();
        
        
    def put_activity(self, event=None):
        """ confirm event activity by user using this program
            reinit the time countdown for auto-lock """
        #print("<user activity", end="");
        self.lockVars.acquire(True); #protect GIL
        self.inactivity = 0; #seconds
        self.lockVars.release();


    def __thread_count_inactivity(self):
        """ Thread, inactivity counter, countdown time, auto-lock """

        print("< locker Thread has init >");
        
        seconds_per_check = 0.250; #250 ms

        isLocked = self.getStateLocked();
        
        while not isLocked:

            if self.inactivity%5 == 0:
                print("inactividad: %d falta %d seconds" %(self.inactivity,
                            self.intMinutesToLock*60 -self.inactivity));
            
            time.sleep(seconds_per_check); #<- decrease cpu usage
            
            self.lockVars.acquire(True);
              # - no critical zone, but GIL is only for CPython
            
            self.inactivity += seconds_per_check; #<- seconds passed
            isLocked = self.locked;
            waitLockerInit = self.waitLockerInit;
            curInactivity = self.inactivity;
            maxWaitMinutes = self.intMinutesToLock;
            
            self.lockVars.release();

            if not waitLockerInit:
                #print("thread is off; break");
                break;

            if curInactivity > 0:
                if curInactivity/60.0 > maxWaitMinutes: #<- check inactive minutes
                    self._auto_lock();
                    
                elif curInactivity/60.0 % 1 == 0: #<- clean inactive login every 1 minutes
                    self._clear_current_login();

                #testing:
                #elif curInactivity/60.0 % 0.5 == 0:
                #    self.frameInactivity.configure(width=50);

        
        print("<end thread locker>");
        return; #finish thread


    def _auto_lock(self):
        """ auto-lock by a thread function after of a lot inactivity """
        if self.getStateLocked() or not self.password:
            return;

        #self._close_current_login();
        
        self.lock();
        
        self._destroySubForms();


    def _clear_current_login(self):
        """ for security, clean inactive forgotten logins """
        currForm = self.grab_current();
        if str(currForm) == "form_password":
            currForm.resetClean(); #clean entrys on open login
            return True;
        return False;




class SaveFile:
    """ this part creates the methods to
        handle content, lock, unlock content and file"""
    
    def __init__(self):

        #this Lock is a Semaphore used only used in only one part:
        self.lockAutoCipher = Lock();


    def clear_reinit(self):
        """ forget all data and session, forget all """;
        self.text.configure(state="normal");
        self.text.delete("0.0", "end");
        self.text.edit_reset();
        self.text.edit_modified(False);
        self.user_last_indexs = ();
        
        self.filename = "";
        self.password = "";
        self.content_locked = b"";
        self.iv = b"";
        self.current_hash = "";
        
        self.lockVars.acquire(True);
        self.locked = False;
        self.waitLockerInit = False; #state of thread, init | no init
        self.lockVars.release();
        
        self.btnUnlock.pack_forget();


    def new_file(self):
        """ ask, clear session, user need a new file or chose old file """
        if self.asksave_content():
            self.clear_reinit();


    def _open_recentfilename(self, filename):
        """ menu command option """
        if not self.asksave_content():
            return; #user want save, but file browser was canceled

        self.clear_reinit();
        self.open_filename(filename);


    def open_filename(self, filename):
        """ the file was already chosen, work on this """
        
        err, namesha, hash_password = cip_fileformat.get_hash_saved(filename);
        if err != cip_fileformat.ERR_SUCCES:
            msg = cip_fileformat.getMessageErrorString(err);
            showwarning(parent=self, title="Error", message=msg);
            return;
        elif not cip_fileformat.existsAlgoHash(namesha):
            #no have algorithm on hashlib
            msg = cip_fileformat.getMessageErrorString(cip_fileformat.ERR_NOALGO_HASH)+" "+namesha;
            showwarning(parent=self, title="Error", message=msg);
            return;
        
        psw = dialogpassword.askoldpassword(self, hash_password,
                                            title='Access: "%s"' % basename(filename),
                                           namesha=namesha,
                                           font1="font_login",
                                           font2="font_login_password");
        if not psw:
            return 0;

        err, plainText, isOriginal = cip_fileformat.load_filename(filename, psw);
        if err == cip_fileformat.ERR_SUCCES:
            self.password = psw;
            self.current_hash = newSha(cip_fileformat.SHA_NAME, psw.encode()).hexdigest(); #sha256..
            self.setStateLocked(False);
            self.filename = filename;

            #I thank Python >= 3
            self.content_reinit(plainText);

            self.setLabelStateAction("File loaded.", 3);
            
            self.init_locker_thread(); #<-check inactivity

            self.add_recent_history(filename);

            if not isOriginal:
                showwarning(parent=self, title="Notice",
                    message="WARNING! The content was changed or is not the original.");

            return 1;
        else:
            msg = cip_fileformat.getMessageErrorString(err);
            showwarning(parent=self, title="Error", message=msg);

    def askopen_filename(self):
        """ user action, it browse a file """
        if not self.asksave_content():
            return; #user want save, but file browser was canceled
        
        self.clear_reinit(); #<-clear current content
        
        ext_funcs.makePath(); #<- try make default path
        
        filetypes = (
                       ("%s files"%cip_fileformat.format_name,
                        "*.%s"%cip_fileformat.ext),
                       ("All files", "*"),
                    );
        
        filename = askopenfilename(title="Open a file..",
                                   parent=self,
                                   initialdir = ext_funcs.pathDefault,
                                   defaultextension="*.%s"%cip_fileformat.ext,
                                   filetypes=filetypes);
        
        if not filename:
            return;

        self.open_filename(filename);
        return;


    def trylock(self):
        """ try lock by user """
        
        self._destroySubForms();
        
        if self.lock() == -1:
            #user has create password, but cancel lock
            self.init_locker_thread(); #<- checker inactivity


    def lock(self):
        """ lock the content, encrypt all content by user password """
        
        if self.getStateLocked(): #<- alredy locked
            return;
        
        if not self.password:
            psw = dialogpassword.askcreatepassword(self,
                                               namesha=cip_fileformat.SHA_NAME,
                                               font1="font_login",
                                               font2="font_login_password",
                                               minlenght=cip_fileformat.MIN_PASSWORD,
                                               maxlenght=cip_fileformat.MAX_PASSWORD);
            if psw:
                #set the current password
                self.password = psw;
                self.current_hash = newSha(cip_fileformat.SHA_NAME,psw.encode()).hexdigest();
            else:
                #user canceled, cannot encrypt without password
                #self.setLabelStateAction("Canceled", 3);
                return;

        #text plain to bytes:
        plain_text = self.text.get("0.0", "end-1c").encode();
        if not plain_text:
            #is empty, it can't be locked, but the "recycler undo&redo" needs to be cleaned
            self.put_activity();
            self.content_reinit("");
            return -1;

        #active a semaphore:
        self.lockAutoCipher.acquire(True);
            #Wait thread, it shouldn't happen, but a change password may be
            # happening right now at self.askchange_password(...) by user
            #This is fast and secure, avoid errors

        self.iv,self.content_locked = cip_fileformat.encrypt(plain_text,self.password.encode());
        self.password = "";
        
        self.setStateLocked(True);
        
        self.lockAutoCipher.release(); #<-free thread

        #remember the currents values of indexs:
        self.user_last_indexs = ();
        selection = ();
        try:
            selection = (self.text.index("sel.first"),
                         self.text.index("sel.last"));
        except:
            pass;
        
        self.user_last_indexs = ( self.text.index("insert"), #cursor
                                  selection,                #selection
                                  self.text.xview()[0], #user xview1
                                  self.text.yview()[0], # and yview1:
                                  );
        #####remember index succes
        
        self.content_reinit("?"*10);
        self.text.configure(state="disabled");
        self.update_statebar();

        self.setLabelStateAction("Content locked.", 3);
        
        #lock success

        self.btnUnlock.pack(side="left", after=self.labelStateAction);

          
    def askunlock(self): #need user acces
        """ user tries to unlock the content by user password
            return True when succes """
        
        if not self.getStateLocked():
            return;

        kw = {};
        if self.filename:
            kw["title"] = 'Unlock: "%s"' % basename(self.filename);
        
        psw = dialogpassword.askoldpassword(self, self.current_hash,
                                        namesha=cip_fileformat.SHA_NAME,
                                        font1="font_login",
                                        font2="font_login_password",
                                        **kw);
        if not psw:
            return False;
        
        self.password = psw;
        plain_text = cip_fileformat.decrypt(self.iv, self.content_locked, psw.encode());
        self.content_locked = b"";
        self.iv = b"";
        
        self.content_reinit(plain_text.decode());
        
        self.setStateLocked(False);
        
        self.update_statebar();
        
        self.init_locker_thread(); #<-secondary thread, checker inactivity

        self.setLabelStateAction("Content unlocked.", 3);
        self.btnUnlock.pack_forget();

        #indexs remember:
        if self.user_last_indexs:
            icursor, selection, xview1, yview1  = self.user_last_indexs;
            self.text.xview("moveto", xview1);
            self.text.yview("moveto", yview1);
            if selection:
                self.text.tag_add("sel", *selection); #first, last
            self.text.mark_set("insert", icursor);
        
        return True;


    def savefile(self, target_filename=""):
        """ save file content in a choosed actual filename """
        if not target_filename:
            target_filename = self.filename;
        
        if not target_filename:
            self.savefile_as();
            return False;

        #current file has been chosen
        
        if not self.getStateLocked():
            psw = self.password;
            plain_text = self.text.get("0.0", "end-1c").encode(); #str to bytes
        else:
            #ON THIS POINT self.password is UNKNOWN
            resp = self._askacces_content(); #ask password to user, get bytes
            if resp == -1:
                showwarning(parent=self, title="Error", message="Cannot save without access");
                return False;
            psw, plain_text = resp;
        
        err = cip_fileformat.save_filename(target_filename, plain_text, psw);

        if err != cip_fileformat.ERR_SUCCES:
            showwarning(parent=self, title="Error",
                            message=cip_fileformat.getMessageErrorString(err));
            self.setLabelStateAction("File not saved!", 5);
            return False;

        # save succes !
        self.filename = target_filename; #now is the current

        self.setLabelStateAction("File saved.", 3);
        
        self.text.edit_modified(False);
        
        self.add_recent_history(target_filename);
        
        return True;
        

    def savefile_as(self):
        """ New file, the user will choose a file and a password, and call the self.savefile """
        
        if self.getStateLocked():
            if not self.askunlock():
                return False; #user canceled unlock
        
        path = ext_funcs.makePath(); #<- try make default path
        
        filetypes = (
                        ("%s files"%cip_fileformat.format_name,
                         "*.%s"%cip_fileformat.ext),
                        ("All files", "*"),
                    );

        filename = asksaveasfilename(title="Save file as..",
                                     parent=self,
                                     initialdir = path,
                                     defaultextension="*.%s"%cip_fileformat.ext,
                                     filetypes=filetypes);
        
        if not filename:
            return False;
        
        password = dialogpassword.askcreatepassword(self,
                                           namesha=cip_fileformat.SHA_NAME,
                                           font1="font_login",
                                           font2="font_login_password",
                                           minlenght=cip_fileformat.MIN_PASSWORD,
                                           maxlenght=cip_fileformat.MAX_PASSWORD);

        if not password:
            #user canceled the operation of save,
            if not self.filename:
                # and no have a current working file
                self.setLabelStateAction("File not saved!", 5);
            return False;
        
        self.password = password;
        self.current_hash = newSha(cip_fileformat.SHA_NAME, password.encode()).hexdigest();
        
        self.savefile(filename);

        self.init_locker_thread(); #<-check inactivity
        
        return True;

        
    def _askacces_content(self, password=None):
        """
        internal, an user operation need unlocked content,
        return (password str, bytes plaint text) if given str 'password' is correct password
        if password is None, it ask to the user by a form.
        
         Accces to return, but it not unlock the content for the user.
        return -1 if not have succes access """
        
        if not self.current_hash:
            return -1;
        
        if not self.getStateLocked():
            return -1;
        
        if not password:
            password = dialogpassword.askoldpassword(self,self.current_hash,
                                                    title="Need Access",
                                                    namesha=cip_fileformat.SHA_NAME,
                                                    font1="font_login",
                                                    font2="font_login_password",
                                                    );
            if not password:
                return -1;
        
        if newSha(cip_fileformat.SHA_NAME,
                    password.encode()).hexdigest() != self.current_hash:
            return -1;
        
        #succes control password
        
        plain_text = cip_fileformat.decrypt(self.iv, self.content_locked, password.encode());
        
        return (password, plain_text);
        

    def askchange_password(self):
        """
        Can change the password by a entry form by user,
        """
        
        if not self.current_hash:
            return;
        
        kwTitle = {};
        if self.filename:
            kwTitle = {"title": 'Change password: "%s"' % basename(self.filename)};

        oldPsw, newPsw = dialogpassword.askchangepassword(self, self.current_hash,
                                                        namesha=cip_fileformat.SHA_NAME,
                                                        font1="font_login",
                                                        font2="font_login_password",
                                                        minlenght=cip_fileformat.MIN_PASSWORD,
                                                        maxlenght=cip_fileformat.MAX_PASSWORD,
                                                        textbutton=("Change", "Cancel"),
                                                        **kwTitle);
        if not (oldPsw and newPsw):
            return; #<- canceled by user

        #active a "semaphore":
        self.lockAutoCipher.acquire(True);
        
        if self.getStateLocked():
            resp = self._askacces_content(oldPsw);
            if resp == -1:
                self.lockAutoCipher.release();
                showwarning(parent=self, title="Error", message="Cannot change password, please retry");
                return;
            
            _oldPsw, plain_text = resp;
            
            self.iv, self.content_locked = cip_fileformat.encrypt(plain_text,
                                                                    newPsw.encode());
        
        self.password = newPsw;
        self.current_hash = newSha(cip_fileformat.SHA_NAME, newPsw.encode()).hexdigest();
        
        self.lockAutoCipher.release();
        
        self.text.edit_modified(True); #<-user can save the changes on file

        self.setLabelStateAction("Password changed.", 3);


    def _cheeck_entrys_file(self):
        """ internal, cheeck the state of menu entrys """
        self.menuFile.entryconfig(self.iEntrySave,
            state="normal" if self.text.edit_modified() else "disabled");

    
    def _cheeck_entrys_lock(self):
        """ internal, cheeck the state of menu entrys """
        locked = self.getStateLocked();
        self.menuLock.entryconfig(self.iEntryUnlockPsw, state="normal" if locked else "disabled");

        self.menuLock.entryconfig(self.iEntryLock, state="normal" if not locked else "disabled");

        self.menuLock.entryconfig(self.iEntryChangePsw, state="normal" \
                                  if self.current_hash else "disabled");
        
        self.menuLock.entryconfig(self.iEntryMenuWhenLock, state="normal" \
                                  if self.current_hash else "disabled");



class Editable:
    def __init__(self):
        if system().lower() == "darwin":
            self.text.bind("<ButtonRelease-2>",self._postMenu);
        else:
            self.text.bind("<ButtonRelease-3>",self._postMenu);


    def _postMenu(self, event):
        """ internal """
        x, y = event.x_root, event.y_root;
        self.menuEdit.post(x,y);


    def tryredo(self):
        try:
            self.text.edit_redo();
        except:
            self.bell(); #sound error


    def tryundo(self):
        try:
            self.text.edit_undo();
        except:
            self.bell(); #sound error

        
    def insert_datetime(self):
        """ user action, insert datetime on a current position cursor """
        if self.getStateLocked():
            return;
        iCursor = self.text.index("insert");
        date = datetime.today().isoformat(sep=" ", timespec="seconds");
        self.text.insert(iCursor, date);


    def select_all(self):
        """ user action, select all """
        if self.getStateLocked():
            return;
        
        self.text.focus_set();
        self.text.tag_add("sel", "0.0", "end-1c")
        #self.text.mark_set("insert", "1.0")
        #self.text.see("insert")


    def sel_delete(self):
        """ user action, delete the selection """
        try:
            self.text.delete("sel.first", "sel.last");
        except:
            pass;
        
        self.update_statebar();


    def sel_copy(self, cut=False):
        """ user action, "copy" from context menu """
        try:
            sel = self.text.get("sel.first", "sel.last");
        except:
            #no have a selection, inusual error
            self.bell(); # <- sound error
            return;
        
        self.clipboard_clear();
        self.clipboard_append(sel);
        
        if cut:
            self.sel_delete();


    def paste(self):
        """ user action, "paste" from context menu """
        try:
            #sometimes this method fails
            text = self.clipboard_get();
        except:
            text = "";
        
        if not text:
            return;
        
        self.sel_delete(); #<- try
        iCursor = self.text.index("insert");
        
        self.text.insert(iCursor, text);
        
        self.update_statebar();


    def go_to_line(self):
        """ user, can go to a specific line """
        if self.getStateLocked():
            return;
        win = search.GoToLine(self, self.text);


    def _cheeck_entrys_edit(self):
        """ internal, control state of options on menu contextual """
        
        try:
            text = self.clipboard_get();
        except:
            text="";
        self.menuEdit.entryconfig(self.iEntryPaste, state="normal" if text else "disabled");
        
        state = "disabled";
        try:
            self.text.index("sel.first"); #shut error if not have selection
            self.text.index("sel.last");
            state = "normal";
        except:
            pass;
        self.menuEdit.entryconfig(self.iEntryCut, state=state);
        self.menuEdit.entryconfig(self.iEntryCopy, state=state);
        self.menuEdit.entryconfig(self.iEntryDelete, state=state);
        
        self.menuEdit.entryconfig(self.iEntrySelAll,
                state="normal" if self.text.index("end-1c")!="1.0" else "disabled");

        try:
            #python 2.x no have this method "canredo, canundo"
            #actually I did not find since what version has appeared
            canredo = self.text.edit("canredo");
            canundo = self.text.edit("canundo");
        except:
            #use a sound error ".bell()" on improvise methods tryredo, tryundo
            canredo = True;
            canundo = True;
            
        self.menuEdit.entryconfig(self.iEntryRedo, state="normal" if canredo else "disabled");
        self.menuEdit.entryconfig(self.iEntryUndo, state="normal" if canundo else "disabled");
        
        phraseFind = "";
        try:
            phraseFind = self.getvar("search_phrase");
        except:
            pass;
        self.menuEdit.entryconfig(self.iEntryFindNext, state="normal" if phraseFind else "disabled");





class MenuEditor(SaveFile, menu_recents.MenuRecentFiles, Editable):
    """ it is a part of the program, it creates all menus """
    def __init__(self):
        self.menuBar = Menu(self, tearoff=False);
        self.configure(menu=self.menuBar);
        
        self.menuFile = Menu(self.menuBar, tearoff=False, postcommand=self._cheeck_entrys_file);
        self.menuBar.add_cascade(menu=self.menuFile, label="File");
        self.menuFile.add_command(label="New file", accelerator="Ctrl+N", command=self.new_file);
        self.bind_all("<Control-n>", lambda e: self.new_file());
        
        self.menuFile.add_command(label="Open from..", accelerator="Ctrl+O", command=self.askopen_filename);
        self.bind_all("<Control-o>", lambda e: self.askopen_filename());

        menu_recents.MenuRecentFiles.__init__(self, self, self.menuFile, self.config_save);
        self.bind_all("<F11>", lambda e: self.askunlock());
        
        self.menuFile.add_separator();
        self.menuFile.add_command(label="Save", accelerator="Ctrl+S", command=self.savefile);
        self.bind_all("<Control-s>", lambda e: self.savefile());
        self.iEntrySave = self.menuFile.index("end");
        
        self.menuFile.add_command(label="Save as..", accelerator="Ctrl+Shift+S", command=self.savefile_as);
        self.bind_all("<Control-Shift-S>", lambda e: self.savefile_as());
        
        self.menuFile.add_separator();
        
        self.menuLock = Menu(self.menuBar, tearoff=False, postcommand=self._cheeck_entrys_lock);
        self.menuFile.add_cascade(label="Secure Lock", menu=self.menuLock);
        self.iEntryLockerMenu = self.menuLock.index("end");
        
        self.menuLock.add_command(label="Lock..", accelerator="F9", command=self.trylock, underline=1);
        self.bind_all("<F9>", lambda e: self.trylock());
        self.iEntryLock = self.menuLock.index("end");
        
        self.menuLock.add_command(label="Unlock with password..", accelerator="F10", command=self.askunlock);
        self.bind_all("<F10>", lambda e: self.askunlock());
        self.iEntryUnlockPsw = self.menuLock.index("end");
        
        self.menuLock.add_command(label="Change password..", command=self.askchange_password);
        self.iEntryChangePsw = self.menuLock.index("end");
        
        self.menuTimeLock = Menu(self.menuLock, tearoff=False);
        self.menuLock.add_cascade(label="Lock when inactivity", menu=self.menuTimeLock);
        self.iEntryMenuWhenLock = self.menuLock.index("end");
        
        self.intMinutesToLock = self.config_save["lock_when"];   #<- load default 5
        self.varCheckSleep = IntVar(value=self.intMinutesToLock);
        self.menuTimeLock.add_radiobutton(label="1 minutes",
                            variable=self.varCheckSleep, value=1, command=self._updateMinutes);
        
        self.menuTimeLock.add_radiobutton(label="3 minutes",
                            variable=self.varCheckSleep, value=3, command=self._updateMinutes);
        
        self.menuTimeLock.add_radiobutton(label="5 minutes",
                            variable=self.varCheckSleep, value=5, command=self._updateMinutes);
        
        self.menuTimeLock.add_radiobutton(label="10 minutes",
                            variable=self.varCheckSleep, value=10, command=self._updateMinutes);
        
        self.menuTimeLock.add_radiobutton(label="Set minutes..",
                        command=self._askchooseMinutes,variable=self.varCheckSleep,value=-1);
        self.iEntryLockChoose = self.menuTimeLock.index("end");
        
        self._updateMinutes(); #<- check and set state of menu labels
        
        self.menuFile.add_separator();
        self.menuFile.add_command(label="Exit", accelerator="Alt+F4", command=self.exit);
        
        self.menuEdit = Menu(self.menuBar, tearoff=False, postcommand=self._cheeck_entrys_edit);
        self.menuBar.add_cascade(menu=self.menuEdit, label="Edit");
        self.menuEdit.add_command(label="Undo", accelerator="Ctrl+Z", command=self.tryundo);
        self.iEntryUndo = self.menuEdit.index("end");
        self.menuEdit.add_command(label="Redo", accelerator="Ctrl+Shift+Z", command=self.tryredo);
        self.iEntryRedo = self.menuEdit.index("end");
        self.bind_all("<Control-Shift-Z>", lambda e: self.tryredo() );
        self.menuEdit.add_separator();
        
        self.menuEdit.add_command(label="Cut", accelerator="Ctrl+X", command=lambda: self.sel_copy(cut=True));
        self.iEntryCut = self.menuEdit.index("end");
        
        self.menuEdit.add_command(label="Copy", accelerator="Ctrl+C", command=self.sel_copy);
        self.iEntryCopy = self.menuEdit.index("end");
        
        self.menuEdit.add_command(label="Paste", accelerator="Ctrl+V", command=self.paste);
        self.iEntryPaste = self.menuEdit.index("end");
        
        self.menuEdit.add_command(label="Delele", accelerator="Supr", command=self.sel_delete);
        self.iEntryDelete = self.menuEdit.index("end");
        
        self.menuEdit.add_command(label="Select all", accelerator="Ctrl+A", command=self.select_all);
        self.iEntrySelAll = self.menuEdit.index("end");
        
        self.menuEdit.add_separator();
        self.menuEdit.add_command(label="Find", accelerator="Ctrl+F", command=self.asksearch);
        self.bind_all("<Control-f>", lambda e: self.asksearch());
        
        self.menuEdit.add_command(label="Find next again", accelerator="Ctrl+G or F3", command=self.findnext, state="disabled");
        self.iEntryFindNext = self.menuEdit.index("end");
        self.bind_all("<Control-g>", lambda e: self.findnext());
        self.bind_all("<F3>", lambda e: self.findnext());
        
        self.menuEdit.add_command(label="Go to line", accelerator="Ctrl+L", command=self.go_to_line);
        self.bind_all("<Control-l>", lambda e: self.go_to_line());
        
        self.menuEdit.add_command(label="Replace", accelerator="Ctrl+R", command=self.askreplace);
        self.bind_all("<Control-r>", lambda e: self.askreplace());
        self.menuEdit.add_separator();
        self.menuEdit.add_command(label="Add Date & Hour", command=self.insert_datetime);
        
        self.menuOptions = Menu(self.menuBar, tearoff=False);
        self.menuBar.add_cascade(menu=self.menuOptions, label="Options");
        
        self.menuOptions.add_command(label="Format", command=self.change_format);
        self.varAdjustLine = BooleanVar(value=self.config_save["adjust_line"]);
        self.menuOptions.add_checkbutton(label="Adjust lines", command=self.set_adjust_line,
                                                         variable=self.varAdjustLine);
        
        self.menuHelp = Menu(self.menuBar, tearoff=False);
        self.menuBar.add_cascade(menu=self.menuHelp, label="Help");

        self.menuHelp.add_command(label="About", command=lambda: help_about.About(self));
        self.menuHelp.add_command(label="Help", command=lambda: help_about.Help(self));
     
        Editable.__init__(self);
        SaveFile.__init__(self);
        
        self.searchForm = None;


    def findnext(self):
        """called by user F3 or Ctrl+G"""
        if not self.searchForm or not self.getvar(name="search_phrase"):
            self.asksearch();
            return;
        self.searchForm.FindNext();


    def asksearch(self):
        if self.getStateLocked():
            return;
        self.searchForm = search.Searcher(self, self.text);


    def askreplace(self):
        if self.getStateLocked():
            return;
        search.Replacer(self, self.text);


    def _setMinutes(self, m):
        self.lockVars.acquire(True);
        self.intMinutesToLock = m;
        self.lockVars.release();


    def _getMinutes(self):
        self.lockVars.acquire(True);
        m = self.intMinutesToLock;
        self.lockVars.release();
        return m;   


    def _updateMinutes(self):
        """ update the "visual state" in menu radiobuttons
            and finally update the value in a variable """
        minutes = self.varCheckSleep.get();

        if minutes in (1,3,5,10):
            #<- user choose a value in menu prev-list
            self.menuTimeLock.entryconfig(self.iEntryLockChoose, label="Set minutes..");
        else:
            #choosed in a specific value by dialog entry
            self.menuTimeLock.entryconfig(self.iEntryLockChoose,
                    label="Set minutes.. [ %d mins ]" % minutes);
            self.varCheckSleep.set(-1);

        self._setMinutes(minutes);
        self.config_save["lock_when"] = minutes; #update


    def _askchooseMinutes(self):
        """ this is called to choose a specific timeout time for the lock """

        lastvalue = self._getMinutes();
        
        minutes = askinteger(parent=self, title="Auto-Lock when",
                             prompt="Maximum inactivity (minutes):", initialvalue=lastvalue);
        
        if not minutes or minutes < 1 or minutes > 120:
            #invalid choosed
            self.varCheckSleep.set(lastvalue); #<- back
            if minutes != None:
                # error out of range
                showwarning(parent=self, title="Error range",
                            message="Limit from 1 to 120 minutes");
        else:
            #ok
            self.varCheckSleep.set(minutes);
        
        self._updateMinutes();




class Editor(Tk, MenuEditor, WaitLocker):
    def __init__(self, text_default="", config_load=None):

        if config_load:
            self.config_save = config_load; #loaded
        else:
            self.config_save = configsave.Configuration(); #reload config
        
        
        Tk.__init__(self);
        WaitLocker.__init__(self);
        

        self.title("Notelocked");

        #--- reload last geometry size ---
        minwidth = 500;
        minheight = 350;
        if "last_geometry" in self.config_save:
            width, height = self.config_save["last_geometry"];

            if (width,height) != (0,0):
                
                if width < minwidth:
                    width = minwidth;
                if height < minheight:
                    height = minheight;
                    
                self.geometry("%dx%d"%(width,height));

        self.minsize(400,250);
        
        try:
            self.iconbitmap(default = ext_funcs.icon);
        except:
            pass;
        
        self.font = Font(self, **self.config_save["font"]);
        
        self.fontLogin = Font(name="font_login",family="Verdana",size=9);
        self.fontPassword = Font(name="font_login_password",family="Verdana",size=10,weight="bold");


        #--- TEXT WIDGET ---

        self.rowconfigure(0, weight=1);
        self.columnconfigure(0, weight=1);

        sp = " " if bool(self.font.metrics()["fixed"]) else "0" #fixed spaces?
        tabswidth = self.font.measure(sp)*int(self.config_save["space_tabs"]);


        
        self.text = Text(self, font=self.font, undo=True, maxundo=50,
                          takefocus=True, tabs=tabswidth, exportselection=True);

        #self.text.grid_propagate(0);
        
        try:
            self.text.configure(inactiveselectbackground=self.text["selectbackground"]);
        except:
            pass;
        
        name_colors = self.config_save["colors"];
        if name_colors != "Default":
            if name_colors in changeformat.createdStyles:
                self.text.configure( **changeformat.createdStyles[ name_colors ] );
            else:
                #no have these custom style, back to Default config style
                self.config_save["colors"] = "Default";
        
        self.text.grid(column=0, row=0, sticky=NSEW);
        
        self.sby = Scrollbar(self, command=self.text.yview, orient="vertical");
        self.sby.grid(column=1, row=0, sticky=NSEW);
        self.text.configure(yscrollcommand=self.sby.set);
        
        self.sbx = Scrollbar(self, command=self.text.xview, orient="horizontal");
        self.sbx.grid(column=0, row=1, sticky=NSEW);
        self.text.configure(xscrollcommand=self.sbx.set);

        MenuEditor.__init__(self);


        #--- STATE BAR ----
        
        self.stateFrame = Frame(self, relief="sunken", borderwidth=1);
        self.stateFrame.grid(column=0, row=2, sticky=NSEW);
        
        self.labelCursor = Label(self.stateFrame, text="", width=18);
        self.labelCursor.pack(side="right");

        Separator(self.stateFrame, orient="vertical").pack(side="right", fill="y", pady=2);

        self.labelLenghtSel = Label(self.stateFrame, text="", anchor="w", width=18);
        self.labelLenghtSel.pack(side="left", padx=5);
        
        Separator(self.stateFrame, orient="vertical").pack(side="left", fill="y", pady=2);
        
        self.labelStateAction = Label(self.stateFrame, text="", width=20, anchor="w");
        self.labelStateAction.pack(side="left", padx=5);

        #testing:
        #self.frameInactivity = Frame(self.stateFrame, bg="black", width=50, height=4);
        #self.frameInactivity.pack(side="left", padx=5);

        self.btnResizer = Sizegrip(self);
        self.btnResizer.grid(column=1, row=2, sticky="nsew");


        #--- Events --- 
        
        self.protocol("WM_DELETE_WINDOW", self.exit);
        
        self.menuBar.bind("<<MenuSelect>>", self.put_activity);
        
        self.bind("<Configure>", self.put_activity);
        
        self.bind_all("<Any-KeyPress>", self.put_activity);
        self.bind_all("<Any-ButtonPress>", self.put_activity);
        self.bind_all("<MouseWheel>", self.put_activity);
        
        self.bind_all("<FocusIn>", self.put_activity);
        self.bind_all("<FocusOut>", self.put_activity);
        
        self.text.bind("<<Paste>>", self.put_activity);
        self.text.bind("<<Copy>>", self.put_activity);
        
        self.sby.bind("<B1-Motion>", self.put_activity);

        self.text.event_add("<<statebar>>", "<KeyRelease>", "<ButtonRelease>");
        self.text.bind("<<statebar>>", self.update_statebar);
        self.text.bind("<<Selection>>", self.update_statebar);

        self.bind_all("<Escape>", lambda e: self.escapeSubForm());

        self.iEventLabelAction = None;
        self.update_statebar();
        self.set_adjust_line();


        # -- Button unlocker --

        #hand2 is for multi OS
        #https://www.tcl.tk/man/tcl8.4/TkCmd/cursors.html
        self.btnUnlock = Button(self.stateFrame,
                                bd=0,relief="flat",command=self.askunlock,cursor="hand2");

        BITMAP_LOCK = """#define image_width 18
            #define image_height 18
            static char image_bits[] = {
            0xff,0xff,0x03,0x3f,0xf0,0x03,0x1f,0xe0,0x03,0x8f,0xc7,0x03,0xcf,0xcf,0x03,
            0xcf,0xcf,0x03,0xcf,0xcf,0x03,0x03,0x00,0x03,0x03,0x00,0x03,0xf3,0x3f,0x03,
            0x73,0x38,0x03,0x73,0x38,0x03,0xf3,0x3c,0x03,0xf3,0x3c,0x03,0x73,0x38,0x03,
            0xf3,0x3f,0x03,0x03,0x00,0x03,0x03,0x00,0x03
            };"""
        
        self.bpLock = BitmapImage("locker", data=BITMAP_LOCK,
                                  foreground=self.btnUnlock["background"],background="gray20");
        
        self.btnUnlock.configure(image="locker",compound="left",bd=1,overrelief="ridge");
                
        # Tip helper (label on widgets)
        self.tipHelper = tiphelper.TipHelper(self);
        self.tipHelper.putOn(self.btnUnlock, "Unlock (F10)", "n");
        
        self.clear_reinit(); #new file
        
        if text_default:
            self.content_reinit(text_default);
        
        self.text.focus();


    def _destroySubForms(self):
        """ intern, try destroy 'all' sub-form by program or
            user, ignore focus """
        for win in self.winfo_children():
            if win.winfo_class() == "Toplevel" and not str(win) in ("help_form", "tiphelper"):
                win.destroy();


    def escapeSubForm(self):
        """ event by user keypress scape, destroy current sub-form """
        currForm = self.grab_current();
        if currForm:
            currForm.destroy();


    def update_statebar(self, event=None):
        line, col = self.text.index("insert").split(".");
        self.labelCursor.configure(text="Line: %s Col: %s" % (line, col));

        selText = "";
        try:
            first = self.text.index("sel.first");
            last = self.text.index("sel.last");
            
            if hasattr(self.text, "count"): #python 3
                lenghtSel = self.text.count(first, last, "chars");
                if lenghtSel:
                    lenghtSel = abs(lenghtSel[0]);
                    
                    lines = self.text.count(first, last, "lines");
                    if lines:
                        lines = abs(lines[0]);
                        lenghtSel -= lines;
            else:
                #python 2
                lenghtSel = len(self.text.get(first, last).replace("\n", ""));

            selText = "Sel: %d chars." % lenghtSel;
        except:
            pass;
        
        self.labelLenghtSel.configure(text=selText);


    def setLabelStateAction(self, label, seconds):
        """ set statebar label of action or file, and the duration of label """
        self.labelStateAction.configure(text=label);

        if self.iEventLabelAction:
            self.after_cancel(self.iEventLabelAction);
            
        self.iEventLabelAction = self.after(seconds*1000,
                                    lambda:self.labelStateAction.configure(text=""));


    def asksave_content(self):
        """
        ask to the user want be save the content on a file
        return False = cancel the exit
        return True = exit is posible
        """
        
        if self.text.edit_modified():
            need_save = askyesnocancel(parent=self, title="Save file ?",
                            message="you have unsaved changes, do you want to save the file?");
            
            if need_save == True:
                if self.savefile():
                    return True;  #<- save was ended on a file
                return False; #<- user interesed on save file, don't quit app
            elif need_save == None: #<- user cancel by button cancel
                return False;
        return True; #<- no need save, can exit


    def exit(self):
        """ user is leaving the program now """
        
        if not self.asksave_content():
            return; #<- cancel the exit, user want save
        
        #shutdown the secondary thread if this exists:
        self.stop_locker_thread();
        
        #sulution fix tkinter clipboard on windows:
        ext_funcs.win32clipboard_fix(self)

        #save last geometry:
        width, height = self.winfo_width(), self.winfo_height();
        
        self.destroy();
        
        self.config_save["last_geometry"] = (width,height);
        self.config_save.save();


    def set_adjust_line(self):
        """ change the state of "ajust line" """
        isAdjust = self.varAdjustLine.get();
        self.config_save["adjust_line"]=isAdjust;
        
        wrap = "none"; #<- not adjust lines
        if isAdjust:  #<- yes adjust lines
            wrap = self.config_save["end_line"]; #<- by 'char' or 'word'   
            self.sbx.grid_forget(); #<- no necessary scrollbar X
        else:
            self.sbx.grid(column=0, row=1, sticky=NSEW);

        self.text.configure(wrap=wrap);

    
    def change_format(self):
        """ user opening the format window """
        win = changeformat.FormatConfig(self, self.text,self.font,self.config_save);
        self.wait_window(win);

        
    def content_reinit(self, content_text):
        """ delete visible content, but not session as password, etc,
         and change the text in the input """
        self.text.configure(state="normal");

        #remember the state of user "have changes for save":
        isModified = self.text.edit_modified();
        self.text.delete("0.0", "end");
        self.text.insert("0.0", content_text);
        self.text.edit_reset(); # clear undo, redo memory
        self.text.edit_modified(isModified);

        #self.text.edit_modified(False);
        self.text.mark_set("insert", "0.0");
        self.text.see("insert");
        self.text.focus_set();

        #reset variables:
        self.setvar("search_phrase", "");
        self.setvar("replace_phrase", "");
        self.setvar("go_line", "");

        #remove unlocker button
        #self.btnUnlock.pack_forget();



def main():

    # - Load, reload config - 
    config = configsave.Configuration(); #reload config
    
    # - show licence a first time -
    if not config["showed_license"]:
        help_about.FirstTimeLicense(config);
    
    # - compare args -
    text = "";
    filename = "";
    if len(argv) > 2:
        if argv[1] == "-text":
            text = argv[2];
            
        elif argv[1] == "-file":
            filename = argv[2];

        elif argv[1] in ("/?", "?"):
            print(_helpargs);
            
    elif len(argv) == 2:
        print(_helpargs);

    # - init the program - 
    winMain = Editor(text, config);

    if filename:
        winMain.open_filename(filename);

    winMain.mainloop();

    #at the end of the program:
    menu_recents.GlobalRecents.compact();


if __name__ == "__main__":
    main();




