#!/usr/bin/env python

"""
File: create_json.py
Author: John Letteboer (https://github.com/jletteboer/)
Date: July 23, 2017
Description:  This script is creating a exampleInfo.json file.
              The file contains the visable and enabled Spluk Apps.
              See README.md for more information.
"""


import os
import json
import re
from splunk.clilib import cli_common as cli

basepath = os.environ["SPLUNK_HOME"]  # Assume SPLUNK_HOME env has been set
app_dir = basepath + '/etc/apps/'
app = 'app_overview'
target_dir = '/appserver/static/'
exportpath = app_dir + app + target_dir + 'exampleInfo.json'

dirs = os.listdir(app_dir)
exclude = [".old.", "alert_", "appsbrowser", "framework",
           "introspection_generator_addon", "learned", "launcher", "legacy",
           "rest_ta", "sample", "simple_xml", "splunk_app", "splunk_arch",
           "splunk_httpinput", "splunk_inst", "Splunk_ML", "splunk_mon",
           "Splunk_SA", "SplunkAppForWebAnalytics", "SplunkForwarder",
           "SplunkLightForwarder", "user-prefs", "config", ".DS_Store", ".git",
           "TA-"]

for i in exclude:
    dirs = [x for x in dirs if i not in x]

app_dirs = [os.path.join(app_dir, i) for i in dirs]


def getSelfConfStanza(stanza, appdir):
    apikeyconfpath = os.path.join(appdir, "default", "app.conf")
    apikeyconf = cli.readConfFile(apikeyconfpath)
    localconfpath = os.path.join(appdir, "local", "app.conf")
    if os.path.exists(localconfpath):
        used_conf = cli.readConfFile(localconfpath)
    else:
        used_conf = apikeyconf
    for name, content in used_conf.items():
        if name in apikeyconf:
            apikeyconf[name].update(content)
        else:
            apikeyconf[name] = content
    return apikeyconf[stanza]

l = []
for id in app_dirs:
    app_id = os.path.basename(id)
    ui = getSelfConfStanza('ui', id)
    title = ui['label']
    visible = ui['is_visible']

    if visible.lower() == "true":
        visible = "1"
    elif visible.lower() == "false":
        visible = "0"

    launcher = getSelfConfStanza('launcher', id)
    description = launcher['description']
    category = "Default"

    mydict = {"id": app_id,
              "title": title,
              "visible":  visible,
              "short-description": description,
              "category": category}
    l.append(mydict)


with open(exportpath, 'wb') as fp:
    json.dump(l, fp, sort_keys=True, indent=4, separators=(',', ': '))
