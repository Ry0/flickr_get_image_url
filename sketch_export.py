# Code from
# http://blenderscripts.googlecode.com/svn-history/r41/trunk/scripts/sketch_export.py
def copy_to_clipboard(text):
    """
   Copy text to the clipboard
   Returns True if successful. False otherwise.
   """

    # =============================================================================
    # win32 (Windows)
    try:
        import win32clipboard
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(text)
        win32clipboard.CloseClipboard()
        return True
    except:
        pass

    # =============================================================================
    # clip (Windows)
    try:
        import subprocess
        p = subprocess.Popen(['clip'], stdin=subprocess.PIPE)
        p.stdin.write(text)
        p.stdin.close()
        retcode = p.wait()
        return True
    except:
        pass

    # =============================================================================
    # pbcopy (Mac OS X)
    try:
        import subprocess
        p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        p.stdin.write(text)
        p.stdin.close()
        retcode = p.wait()
        return True
    except:
        pass

    # =============================================================================
    # xclip (Linux)
    try:
        import subprocess
        p = subprocess.Popen(['xclip', '-selection', 'c'], stdin=subprocess.PIPE)
        p.stdin.write(text)
        p.stdin.close()
        retcode = p.wait()
        return True
    except:
        pass

    # =============================================================================
    # xsel (Linux)
    try:
        import subprocess
        p = subprocess.Popen(['xsel'], stdin=subprocess.PIPE)
        p.stdin.write(text)
        p.stdin.close()
        retcode = p.wait()
        return True
    except:
        pass

    # =============================================================================
    # pygtk
    try:
        # Code from
        # http://www.vector-seven.com/2007/06/27/passing-data-between-gtk-applications-with-gtkclipboard/
        import pygtk
        pygtk.require('2.0')
        import gtk
        # get the clipboard
        clipboard = gtk.clipboard_get()
        # set the clipboard text data
        clipboard.set_text(text)
        # make our data available to other applications
        clipboard.store()
        return True
    except:
        pass

    return False