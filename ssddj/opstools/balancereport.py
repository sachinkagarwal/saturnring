#Copyright 2014 Blackberry Limited
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

#balancereport.py
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ssddj.settings")
from django.conf import settings

from ssdfrontend.models import Target
from ssdfrontend.models import LV
from ssdfrontend.models import VG
from ssdfrontend.models import AAGroup
from ssdfrontend.models import StorageHost
from ssdfrontend.models import User 


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

username = sys.argv[1]
owner = User.objects.get(username=username);
allTargets = Target.objects.filter(owner=owner)
vgdic = {}
vginfodic ={}
print bcolors.BOLD + "\n\nUsers' target information" + bcolors.ENDC
for aTarget in allTargets:
    lv = LV.objects.get(target=aTarget)
    vg = lv.vg
    aag = AAGroup.objects.get(target=aTarget)
    print owner.username,
    print bcolors.OKGREEN + aTarget.iqntar + bcolors.ENDC,
    print aTarget.iqnini,
    print str(aTarget.created_at),
    print bcolors.OKBLUE + vg.vghost.dnsname +bcolors.ENDC,
    print vg.vguuid,
    print lv.lvname,
    print str(aag)
    if str(vg) not in vgdic:
        vgdic[str(vg)] = []
	vginfodic[str(vg)] = (vg.totalGB,vg.maxavlGB)
    if (sys.argv[2] in str(aTarget)) or (sys.argv[2] in aTarget.iqnini): 
        vgdic[str(vg)].append((str(aTarget),aTarget.iqnini,lv.lvsize))


print bcolors.BOLD + "\n\nUsers' targets per VG" +bcolors.ENDC
for vg in sorted(vgdic.keys()):
    print bcolors.OKGREEN + vg + bcolors.ENDC + str(vginfodic[vg])
    count = 1
    for atarget in vgdic[vg]:
	(targetname, initiatorname, size) = atarget
        print str(count) + ")",
        print bcolors.OKBLUE + targetname + bcolors.ENDC,
        print initiatorname,
        print size
        count = count+1

 



