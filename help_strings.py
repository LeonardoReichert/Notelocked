


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



_tagsconfigdefault_ = """
Author: Leonardo A. Reichert

<tagconfig "title1">
font title,Default,20,bold
foreground #202020
underline 1
//positionals args font as _font_order_options
//'Default' (word) replace with default option-font of text widget
</tagconfig>

<tagconfig "titleprogram">
font fontprog,Default,15,bold,italic
foreground #202020
</tagconfig>

<tagconfig "tagcopyaction">
font copyaction,Default,Default,normal,italic
foreground black
-bindcopyable .;Copy
//Copy is the label of text command insert
</tagconfig>

<tagconfig "tagcopyactionesp">
font copyaction
-bindcopyable .;Copiar
</tagconfig>

<tagconfig "tagurlopen">
font urls,Default,Default,normal
foreground #0000ff
underline 1
-bindopenweb .
-bindcopybymenu .;Copy this link
//comment ';' is bind separator, dont use ,
//-bindcopybymenu have 2 args
</tagconfig>

<tagconfig "fontbold">
font simplebold,Default,Default,bold
//comentario
</tagconfig>

<tagconfig "uline">
underline 1
</tagconfig>

<tagconfig "subtitles">
font subtitle,Default,12,bold
underline 1
foreground #202020
</tagconfig>

<tagconfig "fileformat">
font dialogFont,Default,Default,bold
foreground #2020B0
-binddiagram diagramfile
</tagconfig>


<tagconfig "openmygithub">
font urls
foreground #0000ff
underline 1
-bindopenweb https://github.com/LeonardoReichert
-bindcopybymenu https://github.com/LeonardoReichert;Copy Github link
</tagconfig>


<tagconfig "itembold">
font simplebold
foreground #202020
//without underline
</tagconfig>
"""

###############




_license_ = """

<body>

      GNU GENERAL PUBLIC LICENSE
                           Version 2, June 1991

     Copyright (C) 1989, 1991 Free Software Foundation, Inc.,
     51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
     Everyone is permitted to copy and distribute verbatim copies
     of this license document, but changing it is not allowed.

                                Preamble

      The licenses for most software are designed to take away your
    freedom to share and change it.  By contrast, the GNU General Public
    License is intended to guarantee your freedom to share and change free
    software--to make sure the software is free for all its users.  This
    General Public License applies to most of the Free Software
    Foundation's software and to any other program whose authors commit to
    using it.  (Some other Free Software Foundation software is covered by
    the GNU Lesser General Public License instead.)  You can apply it to
    your programs, too.

      When we speak of free software, we are referring to freedom, not
    price.  Our General Public Licenses are designed to make sure that you
    have the freedom to distribute copies of free software (and charge for
    this service if you wish), that you receive source code or can get it
    if you want it, that you can change the software or use pieces of it
    in new free programs; and that you know you can do these things.

      To protect your rights, we need to make restrictions that forbid
    anyone to deny you these rights or to ask you to surrender the rights.
    These restrictions translate to certain responsibilities for you if you
    distribute copies of the software, or if you modify it.

      For example, if you distribute copies of such a program, whether
    gratis or for a fee, you must give the recipients all the rights that
    you have.  You must make sure that they, too, receive or can get the
    source code.  And you must show them these terms so they know their
    rights.

      We protect your rights with two steps: (1) copyright the software, and
    (2) offer you this license which gives you legal permission to copy,
    distribute and/or modify the software.

      Also, for each author's protection and ours, we want to make certain
    that everyone understands that there is no warranty for this free
    software.  If the software is modified by someone else and passed on, we
    want its recipients to know that what they have is not the original, so
    that any problems introduced by others will not reflect on the original
    authors' reputations.

      Finally, any free program is threatened constantly by software
    patents.  We wish to avoid the danger that redistributors of a free
    program will individually obtain patent licenses, in effect making the
    program proprietary.  To prevent this, we have made it clear that any
    patent must be licensed for everyone's free use or not licensed at all.

      The precise terms and conditions for copying, distribution and
    modification follow.

                        GNU GENERAL PUBLIC LICENSE
       TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

      0. This License applies to any program or other work which contains
    a notice placed by the copyright holder saying it may be distributed
    under the terms of this General Public License.  The "Program", below,
    refers to any such program or work, and a "work based on the Program"
    means either the Program or any derivative work under copyright law:
    that is to say, a work containing the Program or a portion of it,
    either verbatim or with modifications and/or translated into another
    language.  (Hereinafter, translation is included without limitation in
    the term "modification".)  Each licensee is addressed as "you".

    Activities other than copying, distribution and modification are not
    covered by this License; they are outside its scope.  The act of
    running the Program is not restricted, and the output from the Program
    is covered only if its contents constitute a work based on the
    Program (independent of having been made by running the Program).
    Whether that is true depends on what the Program does.

      1. You may copy and distribute verbatim copies of the Program's
    source code as you receive it, in any medium, provided that you
    conspicuously and appropriately publish on each copy an appropriate
    copyright notice and disclaimer of warranty; keep intact all the
    notices that refer to this License and to the absence of any warranty;
    and give any other recipients of the Program a copy of this License
    along with the Program.

    You may charge a fee for the physical act of transferring a copy, and
    you may at your option offer warranty protection in exchange for a fee.

      2. You may modify your copy or copies of the Program or any portion
    of it, thus forming a work based on the Program, and copy and
    distribute such modifications or work under the terms of Section 1
    above, provided that you also meet all of these conditions:

        a) You must cause the modified files to carry prominent notices
        stating that you changed the files and the date of any change.

        b) You must cause any work that you distribute or publish, that in
        whole or in part contains or is derived from the Program or any
        part thereof, to be licensed as a whole at no charge to all third
        parties under the terms of this License.

        c) If the modified program normally reads commands interactively
        when run, you must cause it, when started running for such
        interactive use in the most ordinary way, to print or display an
        announcement including an appropriate copyright notice and a
        notice that there is no warranty (or else, saying that you provide
        a warranty) and that users may redistribute the program under
        these conditions, and telling the user how to view a copy of this
        License.  (Exception: if the Program itself is interactive but
        does not normally print such an announcement, your work based on
        the Program is not required to print an announcement.)

    These requirements apply to the modified work as a whole.  If
    identifiable sections of that work are not derived from the Program,
    and can be reasonably considered independent and separate works in
    themselves, then this License, and its terms, do not apply to those
    sections when you distribute them as separate works.  But when you
    distribute the same sections as part of a whole which is a work based
    on the Program, the distribution of the whole must be on the terms of
    this License, whose permissions for other licensees extend to the
    entire whole, and thus to each and every part regardless of who wrote it.

    Thus, it is not the intent of this section to claim rights or contest
    your rights to work written entirely by you; rather, the intent is to
    exercise the right to control the distribution of derivative or
    collective works based on the Program.

    In addition, mere aggregation of another work not based on the Program
    with the Program (or with a work based on the Program) on a volume of
    a storage or distribution medium does not bring the other work under
    the scope of this License.

      3. You may copy and distribute the Program (or a work based on it,
    under Section 2) in object code or executable form under the terms of
    Sections 1 and 2 above provided that you also do one of the following:

        a) Accompany it with the complete corresponding machine-readable
        source code, which must be distributed under the terms of Sections
        1 and 2 above on a medium customarily used for software interchange; or,

        b) Accompany it with a written offer, valid for at least three
        years, to give any third party, for a charge no more than your
        cost of physically performing source distribution, a complete
        machine-readable copy of the corresponding source code, to be
        distributed under the terms of Sections 1 and 2 above on a medium
        customarily used for software interchange; or,

        c) Accompany it with the information you received as to the offer
        to distribute corresponding source code.  (This alternative is
        allowed only for noncommercial distribution and only if you
        received the program in object code or executable form with such
        an offer, in accord with Subsection b above.)

    The source code for a work means the preferred form of the work for
    making modifications to it.  For an executable work, complete source
    code means all the source code for all modules it contains, plus any
    associated interface definition files, plus the scripts used to
    control compilation and installation of the executable.  However, as a
    special exception, the source code distributed need not include
    anything that is normally distributed (in either source or binary
    form) with the major components (compiler, kernel, and so on) of the
    operating system on which the executable runs, unless that component
    itself accompanies the executable.

    If distribution of executable or object code is made by offering
    access to copy from a designated place, then offering equivalent
    access to copy the source code from the same place counts as
    distribution of the source code, even though third parties are not
    compelled to copy the source along with the object code.

      4. You may not copy, modify, sublicense, or distribute the Program
    except as expressly provided under this License.  Any attempt
    otherwise to copy, modify, sublicense or distribute the Program is
    void, and will automatically terminate your rights under this License.
    However, parties who have received copies, or rights, from you under
    this License will not have their licenses terminated so long as such
    parties remain in full compliance.

      5. You are not required to accept this License, since you have not
    signed it.  However, nothing else grants you permission to modify or
    distribute the Program or its derivative works.  These actions are
    prohibited by law if you do not accept this License.  Therefore, by
    modifying or distributing the Program (or any work based on the
    Program), you indicate your acceptance of this License to do so, and
    all its terms and conditions for copying, distributing or modifying
    the Program or works based on it.

      6. Each time you redistribute the Program (or any work based on the
    Program), the recipient automatically receives a license from the
    original licensor to copy, distribute or modify the Program subject to
    these terms and conditions.  You may not impose any further
    restrictions on the recipients' exercise of the rights granted herein.
    You are not responsible for enforcing compliance by third parties to
    this License.

      7. If, as a consequence of a court judgment or allegation of patent
    infringement or for any other reason (not limited to patent issues),
    conditions are imposed on you (whether by court order, agreement or
    otherwise) that contradict the conditions of this License, they do not
    excuse you from the conditions of this License.  If you cannot
    distribute so as to satisfy simultaneously your obligations under this
    License and any other pertinent obligations, then as a consequence you
    may not distribute the Program at all.  For example, if a patent
    license would not permit royalty-free redistribution of the Program by
    all those who receive copies directly or indirectly through you, then
    the only way you could satisfy both it and this License would be to
    refrain entirely from distribution of the Program.

    If any portion of this section is held invalid or unenforceable under
    any particular circumstance, the balance of the section is intended to
    apply and the section as a whole is intended to apply in other
    circumstances.

    It is not the purpose of this section to induce you to infringe any
    patents or other property right claims or to contest validity of any
    such claims; this section has the sole purpose of protecting the
    integrity of the free software distribution system, which is
    implemented by public license practices.  Many people have made
    generous contributions to the wide range of software distributed
    through that system in reliance on consistent application of that
    system; it is up to the author/donor to decide if he or she is willing
    to distribute software through any other system and a licensee cannot
    impose that choice.

    This section is intended to make thoroughly clear what is believed to
    be a consequence of the rest of this License.

      8. If the distribution and/or use of the Program is restricted in
    certain countries either by patents or by copyrighted interfaces, the
    original copyright holder who places the Program under this License
    may add an explicit geographical distribution limitation excluding
    those countries, so that distribution is permitted only in or among
    countries not thus excluded.  In such case, this License incorporates
    the limitation as if written in the body of this License.

      9. The Free Software Foundation may publish revised and/or new versions
    of the General Public License from time to time.  Such new versions will
    be similar in spirit to the present version, but may differ in detail to
    address new problems or concerns.

    Each version is given a distinguishing version number.  If the Program
    specifies a version number of this License which applies to it and "any
    later version", you have the option of following the terms and conditions
    either of that version or of any later version published by the Free
    Software Foundation.  If the Program does not specify a version number of
    this License, you may choose any version ever published by the Free Software
    Foundation.

      10. If you wish to incorporate parts of the Program into other free
    programs whose distribution conditions are different, write to the author
    to ask for permission.  For software which is copyrighted by the Free
    Software Foundation, write to the Free Software Foundation; we sometimes
    make exceptions for this.  Our decision will be guided by the two goals
    of preserving the free status of all derivatives of our free software and
    of promoting the sharing and reuse of software generally.

                                NO WARRANTY

      11. BECAUSE THE PROGRAM IS LICENSED FREE OF CHARGE, THERE IS NO WARRANTY
    FOR THE PROGRAM, TO THE EXTENT PERMITTED BY APPLICABLE LAW.  EXCEPT WHEN
    OTHERWISE STATED IN WRITING THE COPYRIGHT HOLDERS AND/OR OTHER PARTIES
    PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED
    OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
    MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.  THE ENTIRE RISK AS
    TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH YOU.  SHOULD THE
    PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL NECESSARY SERVICING,
    REPAIR OR CORRECTION.

      12. IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING
    WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MAY MODIFY AND/OR
    REDISTRIBUTE THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES,
    INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING
    OUT OF THE USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED
    TO LOSS OF DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY
    YOU OR THIRD PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER
    PROGRAMS), EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE
    POSSIBILITY OF SUCH DAMAGES.

                         END OF TERMS AND CONDITIONS

                How to Apply These Terms to Your New Programs

      If you develop a new program, and you want it to be of the greatest
    possible use to the public, the best way to achieve this is to make it
    free software which everyone can redistribute and change under these terms.

      To do so, attach the following notices to the program.  It is safest
    to attach them to the start of each source file to most effectively
    convey the exclusion of warranty; and each file should have at least
    the "copyright" line and a pointer to where the full notice is found.

        <one line to give the program's name and a brief idea of what it does.>
        Copyright (C) <year>  <name of author>

        This program is free software; you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation; either version 2 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License along
        with this program; if not, write to the Free Software Foundation, Inc.,
        51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

    Also add information on how to contact you by electronic and paper mail.

    If the program is interactive, make it output a short notice like this
    when it starts in an interactive mode:

        Gnomovision version 69, Copyright (C) year name of author
        Gnomovision comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
        This is free software, and you are welcome to redistribute it
        under certain conditions; type `show c' for details.

    The hypothetical commands `show w' and `show c' should show the appropriate
    parts of the General Public License.  Of course, the commands you use may
    be called something other than `show w' and `show c'; they could even be
    mouse-clicks or menu items--whatever suits your program.

    You should also get your employer (if you work as a programmer) or your
    school, if any, to sign a "copyright disclaimer" for the program, if
    necessary.  Here is a sample; alter the names:

      Yoyodyne, Inc., hereby disclaims all copyright interest in the program
      `Gnomovision' (which makes passes at compilers) written by James Hacker.

      <signature of Ty Coon>, 1 April 1989
      Ty Coon, President of Vice

    This General Public License does not permit incorporating your program into
    proprietary programs.  If your program is a subroutine library, you may
    consider it more useful to permit linking proprietary applications with the
    library.  If this is what you want to do, use the GNU Lesser General
    Public License instead of this License.

</body>

"""


##############


_about_ = """
#can add or update <tagconfigs> same _tagsconfigdefault_
#but cannot re-config a exist font name, need other name

<tagconfig "openwikiencbc">
font urls
foreground #0000ff
underline 1
-bindopenweb https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Cipher_block_chaining_(CBC)
-bindcopybymenu https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Cipher_block_chaining_(CBC);Copy wikipedia link
</tagconfig>

<body>
<tag title1>\tAbout</tag>

  <tag titleprogram>Notelocked</tag>

 <tag fontbold>Author:</tag> "Leonardo A. Reichert"
 <tag fontbold>Email:</tag> <tag tagcopyaction>leoreichert5000@gmail.com</tag>
 <tag fontbold>Github:</tag> <tag openmygithub>LeonardoReichert@Github</tag>

\t<tag subtitles>Description</tag>
 Notelocked is a simple editor to save <tag fontbold>encrypted texts with a password</tag>, it maintains a simple aspect and an easy way of use, is free software and multiplatform with the licence GNU General Public License v2.0 or later.

 Many times we have saved important data in text files but these simple files are exposed and open to everyone who opens the file on our computer, that is a problem.

 A very important objective is the protection and privacy of the content, so this program measures the user's inactivity in the program and when there is an "open and password" <tag fontbold>content in full inactivity, it auto-encrypts the open content and blocks it</tag> so that when the program is forgotten open and careless data are blocked on the computer turned on, this is protection against carelessness.

 When you are editing text you can choose a password for the content or <tag fontbold>when saving a new file you need to enter a password</tag> if it was not created before.
 Every time you need to open the content, or unlock it, you will need to use your own password, <tag fontbold>the passwords are protected by you and no one else has them</tag>, so don't lose it or you will lose the content of the saved or edited file.

\t<tag subtitles>Technical Format & Encryption</tag>
 The encryption method used is "AES Mode CBC" -<tag openwikiencbc>see on wikipedia</tag>- with the purpose of "<tag fontbold>confidentiality</tag>" of the encrypted content for the total secrecy of the original data.
 The <tag fileformat>format and structure</tag> of the saved file is not a secret, because basing security on keeping the secret of the encryption procedure is not security, instead you choose to trust the encryption mode and its correct and recommended use for security.

\t<tag subtitles>Notice</tag>
 Remember very well that it is not recommended at any time to save important or personal information in any digital medium including this one. Other programs could access to read the open windows, or read the memory. This program is not intended to replace other programs or other ways of saving information.
 This program, it does not read the inactivity outside the program, only the inactivity of this program. Is not a transmission or communication medium and it only stores the files on the chosen local drive.
 Remember, no guarantees are made about the features of the program, no warranties of any kind.
 Read the "license" or "licenses".

 Thank you very much.

 (This text is a translation from Spanish, which could have errors.)

</body>
"""

###############




_about_esp_ = u"""
#can add or update <tagconfigs> same _tagsconfigdefault_
#but cannot re-config a exist font name, need other name

<tagconfig "openwikicbc">
font urls
foreground #0000ff
underline 1
-bindopenweb https://es.wikipedia.org/wiki/Modos_de_operaci%C3%B3n_de_una_unidad_de_cifrado_por_bloques#Modo_CBC_(Cipher-block_chaining)
-bindcopybymenu https://es.wikipedia.org/wiki/Modos_de_operaci%C3%B3n_de_una_unidad_de_cifrado_por_bloques#Modo_CBC_(Cipher-block_chaining);Copiar link de wikipedia
</tagconfig>

<tagconfig "openmygithubesp">
font urls
foreground #0000ff
underline 1
-bindopenweb https://github.com/LeonardoReichert
-bindcopybymenu https://github.com/LeonardoReichert;Copiar link de Github
</tagconfig>


<body>
<tag title1>\tAcerca de</tag>

  <tag titleprogram>Notelocked</tag>

 <tag fontbold>Autor:</tag> "Leonardo A. Reichert"
 <tag fontbold>Email:</tag> <tag tagcopyactionesp>leoreichert5000@gmail.com</tag>
 <tag fontbold>Github:</tag> <tag openmygithubesp>LeonardoReichert@Github</tag>

\t<tag subtitles>Descripci\u00f3n</tag>
 Notelocked es un simple editor para guardar <tag fontbold>textos cifrados con contrase\u00f1a</tag>, mantiene un aspecto sencillo y una f\u00e1cil manera de uso, es software libre y multiplataforma, con licencia GNU General Public License v2.0 o posterior.

 Muchas veces hemos guardado datos importantes en archivos de texto pero estos archivos sencillos est\u00e1n expuestos y abiertos a todo el mundo que abra el archivo en nuestro ordenador, eso es un problema.

 Un objetivo muy importante es la protecci\u00f3n y privacidad del contenido, entonces este programa mide la inactividad del usuario en el programa y cuando hay un contenido "abierto y con clave" <tag fontbold>en plena inactividad auto-cifra al contenido abierto y lo bloquea</tag> para que al olvidarse el programa en el ordenador encendido se bloqueen los datos abiertos y descuidados, esto es una protecci\u00f3n al descuido.

 Cuando se esta editando texto se puede elegir una clave para el contenido o <tag fontbold>al guardar un nuevo archivo se necesita introducir una clave</tag> si no se creo antes.
 Cada vez que necesites abrir el contenido, o desbloquearlo, necesitaras usar esa clave propia, <tag fontbold>las claves las custodias tu mismo y no la tiene nadie mas</tag>, as\u00ed que no la pierdas o perder\u00e1s el contenido del archivo guardado o en edici\u00f3n.

\t<tag subtitles>Formato t\u00e9cnico y Cifrado</tag>
 El m\u00e9todo de cifrado usado es "AES Modo CBC" -<tag openwikicbc>ver en Wikipedia</tag>- con el prop\u00f3sito de "<tag fontbold>confidencialidad</tag>" del contenido cifrado para el secreto total de los datos originales.
 El <tag fileformat>formato y estructura del archivo</tag> guardado no es un secreto, porque basar la seguridad en guardar el secreto del procedimiento del cifrado no es seguridad, en lugar de eso, se elige confiar en el modo de cifrado y de su uso correcto y recomendado.

\t<tag subtitles>Aviso</tag>
 Recuerda muy bien, no se recomienda en ning\u00fan momento guardar información importante o personal en ning\u00fan medio digital incluido este. Otros programas podr\u00edan acceder a leer las ventanas abiertas, o leer la memoria. Este programa no pretende remplazar a otros programas o a otras formas de guardar informaci\u00f3n. 
 Este programa, no lee la inactividad fuera del programa, solo la inactividad de este programa. No es un medio de transmisi\u00f3n o comunicaci\u00f3n y solo almacena los archivos en el disco local elegido.
 Ten en cuenta, no se ofrecen garant\u00edas de ninguna funci\u00f3n del programa, no se ofrecen garant\u00edas de ning\u00fan tipo.
 Leer la "licencia" o las "licencias adjuntas".

 Muchas gracias.



</body>

"""

##############



_help_  = u"""
<tagconfig "openwikipasswsecenglish">
font urls
foreground #0000ff
underline 1
-bindopenweb https://en.wikipedia.org/wiki/Password_strength
-bindcopybymenu https://en.wikipedia.org/wiki/Password_strength;Copy Wiki link
</tagconfig>

<body>
<tag title1>\tHelp</tag>

  <tag titleprogram>Notelocked</tag>

\t<tag subtitles>Modo of use</tag>
 It is used as a "plain text" editor, but when saving the file we need to create a password that we remember and that is not too simple, <tag fontbold>do not forget the password, because if you lose it you also lose the content forever</tag>. It's best to create a strong password before writing anything you want to protect.
 While we are using the program, it will be common for us to enter the password several times to authenticate that another person does not read the data saved or opened with a password. The program is designed to take care that no one in our environment reads the data except its owner. Therefore, it may be common to have more stress when using this program than some other common program without extra precautions.

\t<tag subtitles>Secure Lock</tag>
 This is a <tag uline>menu</tag> found under the "File" menu.
 Here you have several options for the "locker", understanding its use is very easy and necessary:
  \u2022 <tag itembold>Lock</tag>: encrypt content and lock with the password, if the content is empty just create the password. Each time it is used it also clears undo/redo or undo/redo recycling data.
  \u2022 <tag itembold>Unlock with password</tag>: decrypts and unlocks previously locked content with the password.
  \u2022 <tag itembold>Change password</tag>: change the current password.
  \u2022 <tag itembold>Lock when inactivity</tag>: here you can choose how often to auto-lock content if the program is idle, raising the time may reduce human stress, but raising it too much may cause you to forget the program and someone will read the open content.

\t<tag subtitles>Password security</tag>
 When choosing a new password, it must be more than 12 characters long or up to 30, no more and no less.
 If you forget the password, you will never be able to recover it, so <tag fontbold>try to choose a password that is difficult enough to guess but that you will remember in the future</tag>, if you think it is convenient to keep the password on paper, do it and hide it. 

 Throughout the "history of cryptography", its security has been a "capacity" that has been eventually surpassed by scientific discoveries and the advancement of increasingly faster computers to guess passwords or discover collisions in their hashes than in their time were the safest hashes or most advanced algorithms for the time.
 It is for this reason that today in this program the length of the password must be greater than 12, the more complex it will be, the more difficult it will be for a computer to guess it with its full current processor capacity, it could even take hundreds or thousands of passwords. years to guess a more complex password, while simple passwords could be guessed very quickly.

  <tag uline>See more on wikipedia</tag>: <tag openwikipasswsecenglish>"Password strength"</tag>

\t<tag subtitles>Recent Files</tag>
 It is a list of the history of used files, it seems common but with the possibility of deactivating this history and deleting it (also by pressing F12).
 Although you may wish to activate it so you won't forget where you had your files.

\t<tag subtitles>Finally</tag>
 There are other options such as creating new color profiles for text editing, in the Options > Format menu.

 Thank you very much and good luck.

 (This text is a translation from Spanish, which could have errors.)

 Support: <tag tagcopyaction>leoreichert5000@gmail.com</tag>


</body>
"""

###############



_help_esp_ = u"""
<tagconfig "openwikipasswsec">
font urls
foreground #0000ff
underline 1
-bindopenweb https://es.wikipedia.org/wiki/Seguridad_de_la_contrase%C3%B1a
-bindcopybymenu https://es.wikipedia.org/wiki/Seguridad_de_la_contrase%C3%B1a;Copiar link de wikipedia
</tagconfig>

<body>
<tag title1>\tAyuda</tag>

  <tag titleprogram>Notelocked</tag>

\t<tag subtitles>Modo de uso</tag>
 Se usa como un editor de "texto simple", pero al guardar el archivo deberemos crear una contrase\u00f1a que recordemos y que no sea demasiado sencilla, <tag fontbold>no olvides la contrase\u00f1a, porque si la pierdes tambi\u00e9n pierdes el contenido para siempre</tag>. Es mejor crear una contrase\u00f1a segura antes de escribir un dato que desees proteger.
 Mientras estemos usando el programa, ser\u00e1 habitual que debamos introducir la contrase\u00f1a en varias oportunidades para autenticar que otra persona no lea los datos guardados o abiertos con contrase\u00f1a. El programa esta pensado para cuidar que nadie en nuestro entorno lea los datos excepto su due\u00f1o. Por eso, puede ser com\u00fan tener mas estr\u00e9s al usar este programa que alg\u00fan otro programa com\u00fan sin cuidados extras.

\t<tag subtitles>Secure Lock</tag>
 Este es un <tag uline>men\u00fa</tag> que se encuentra en el men\u00fa "File" (Archivo).
 Aqu\u00ed tienes varias opciones para el "locker", entender su uso es muy f\u00e1cil y necesario:
  \u2022 <tag itembold>Lock</tag>: cifrar contenido y bloquear con la contrase\u00f1a, si el contenido esta vacio solo crea la contrase\u00f1a. Cada vez que se usa tambi\u00e9n borra los datos de reciclaje undo/redo o deshacer/rehacer.
  \u2022 <tag itembold>Unlock with password</tag>: descifra y desbloquea con la contrase\u00f1a el contenido antes bloqueado.
  \u2022 <tag itembold>Change password</tag>: cambia la contrase\u00f1a actual.
  \u2022 <tag itembold>Lock when inactivity</tag>: aqu\u00ed puedes elegir con que frecuencia de tiempo auto-bloquear el contenido si el programa esta inactivo, si elevas el tiempo puede reducir el estr\u00e9s humano, pero elevarlo demasiado puede ocasionar que olvides el programa y alguien lea el contenido abierto.

\t<tag subtitles>Seguridad de contrase\u00f1a</tag>
 Al elegir una nueva contrase\u00f1a, esta debe ser de mas de 12 caracteres de longitud o hasta 30, no mas ni menos.
 Si te olvidas de la contrase\u00f1a, no podr\u00e1s recuperarla nunca mas, as\u00ed que <tag fontbold>trata de elegir una contrase\u00f1a lo bastante dif\u00edcil de adivinar pero que recuerdes en el futuro</tag>, si crees conveniente guardar la contrase\u00f1a en un papel hazlo y esc\u00f3ndelo.

 A lo largo de la "historia de la criptograf\u00eda", su seguridad ha sido una "capacidad" que ha sido superada eventualmente por descubrimientos cient\u00edficos y el avance de los ordenadores cada vez mas r\u00e1pidos para lograr adivinar contrase\u00f1as o descubrir colisiones en sus Hashes que en su momento eran los Hashes mas seguros o algoritmos mas avanzados para la \u00e9poca.
 Es por esta raz\u00f3n, que al d\u00eda de hoy en este programa la longitud de la contrase\u00f1a debe ser superior a 12, mientras mas compleja ser\u00e1 mas dif\u00edcil que un computador la adivine con su plena capacidad de procesador actual, incluso podr\u00eda tardar cientos o miles de a\u00f1os adivinar una contrase\u00f1a muy compleja, mientras que contrase\u00f1as sencillas podr\u00edan adivinarse muy r\u00e1pidamente.

  <tag uline>Ver mas en Wikipedia</tag>:  <tag openwikipasswsec>"Seguridad de la contrase\u00f1a"</tag>

\t<tag subtitles>Recent Files</tag>
 Es una lista del historial de archivos usados que parece com\u00fan pero con la posibilidad de desactivar este historial y borrarlo (tambi\u00e9n al presionar F12). 
 Aunque quiz\u00e1s quieras activarlo para no olvidar d\u00f3nde ten\u00edas tus archivos.

\t<tag subtitles>Por ultimo</tag>
 Hay otras opciones como crear nuevos perfiles de color para la edici\u00f3n del texto, en el men\u00fa Options > Format.

 Muchas gracias y suerte.

 Soporte: <tag tagcopyactionesp>leoreichert5000@gmail.com</tag>


</body>
"""



