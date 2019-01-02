# -*- coding: utf-8 -*-
import sys

import Tkinter as tk
import myNotebook as nb
from config import config
import plug
from server import Server
import json


this = sys.modules[__name__]	# For holding module globals
this.version = "0.0.1"

def plugin_start(plugin_dir):
   """
   Load this plugin into EDMC
   """
   this.server = Server(5556)
   print 'starting plugin EDMQ v{} from "{}"'.format(this.version, plugin_dir.encode("utf-8"))
   # install('pyzmq')
   return "EDMQ"

def plugin_stop():
    """
    EDMC is closing
    """
    this.server.send_sys("Farewell cruel world!")


def plugin_prefs(parent, cmdr, is_beta):
   """
   Return a TK Frame for adding to the EDMC settings dialog.
   """
   this.port = tk.IntVar(value=config.getint("edmqPORT"))	# Retrieve saved value from config
   frame = nb.Frame(parent)
   nb.Label(frame, text="Welcome to EDMQ v"+this.version+" settings").grid()

   port_label = nb.Label(frame, text="API Key :").grid()
   # port_label.grid(row=11, padx=PADX, sticky=tk.W)
   port_entry = nb.Entry(frame, textvariable=this.port).grid()
   # port_entry.grid(row=11, column=1, padx=PADX, pady=PADY, sticky=tk.EW)
   this.server.send_sys(u'plugin_perfs')

   return frame

def prefs_changed(cmdr, is_beta):
   """
   Save settings.
   """
   config.set('edmqPORT', this.port.get())	# Store new value in config
   this.server.send_sys(u'edmqPORT %s' % (this.port.get()))


def plugin_app(parent):
   """
   Create a pair of TK widgets for the EDMC main window
   """
   label = tk.Label(parent, text="Connections:")
   this.status = tk.Label(parent, anchor=tk.W, text="")
   this.server.send_sys(u'plugin_app')
   return (label, this.status)
   # later on your event functions can directly update this.status["text"]
   # this.status["text"] = "Happy!"


def journal_entry(cmdr, is_beta, system, station, entry, state):
   obj = {"entry":entry, "cmdr": cmdr, "system": system, "station": station}#, "state": state}
   this.server.send_journal(json.dumps(obj))

   # if entry['event'] == 'FSDJump':
   #      # We arrived at a new system!
   #      if 'StarPos' in entry:
   #          sys.stderr.write("Arrived at {} ({},{},{})\n".format(entry['StarSystem'], *tuple(entry['StarPos'])))
   #      else:
   #          sys.stderr.write("Arrived at {}\n".format(entry['StarSystem']))

def dashboard_entry(cmdr, is_beta, entry):
   # is_deployed = entry['Flags'] & plug.FlagsHardpointsDeployed
   #  sys.stderr.write("Hardpoints {}\n".format(is_deployed and "deployed" or "stowed"))
   this.server.send_dashboard(json.dumps({"cmdr": cmdr, "entry": entry}))

def cmdr_data(data, is_beta):
   """
   We have new data on our commander
   """
   commander = data.get('commander') and data.get('commander').get('name') or ''
   this.server.send_cmdr(commander)
   