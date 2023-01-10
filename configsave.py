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


import pickle;
#from os.path import exists;



filecnf = "config000.dat";


_default_ = {
            "showed_license": False,
            "lock_when": 5, #minutes
            "last_geometry": (0, 0),

            #----- Recents -----

            "forget_history": False,

            #----- format options ---- :
           
             "adjust_line": True,
           
             "font": {"family": "Verdana",
                      "size":11,
                      "weight": "normal",
                      "slant": "roman",
                     },
           
             "end_line": "word",

             "colors": "Default",
             "space_tabs": 4,
           };


class Configuration(dict):
    def __init__(self, filename=filecnf):
        dict.__init__(self);
        self.filename = filename;

        self.readload();
        
    def readload(self):
        try:
            fp = open(self.filename, "rb");
        except:
            self.update(_default_);
            return False;
        
        try:
            self.update( pickle.load(fp) );
        except:
            #is changed version of python ? from 3.4 to < 3.4 ?
            #protocol can be not supported
            #print("pickle protocol no supported for this python version");
            self.update(_default_);
            
        fp.close();
        return True;
            
    def save(self):
        try:
            fp = open(self.filename, "wb");
        except:
            return False;

        try:
            pickle.dump(self,fp);
            print("Se guardo la configuracion");
        except:
            #pass;
            print("Error: no se guardo la configuracion");

        fp.close();


if __name__ == "__main__":
    config = Configuration();
    print("actual configuration: \n", config);

    print("\n")
    input("Pause")












