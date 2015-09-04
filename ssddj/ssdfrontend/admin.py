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

from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django import forms
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from traceback import format_exc
from ssdfrontend.models import Target
from ssdfrontend.models import StorageHost
from ssdfrontend.models import LV
from ssdfrontend.models import VG
from ssdfrontend.models import Provisioner
from ssdfrontend.models import AAGroup
from ssdfrontend.models import ClumpGroup
from ssdfrontend.models import TargetHistory
from ssdfrontend.models import TargetNameMap
from ssdfrontend.models import Interface
from ssdfrontend.models import IPRange
from ssdfrontend.models import Lock
from ssdfrontend.models import GenerateRandomPin
#from ssdfrontend.models import HostGroup
from utils.targetops import DeleteTargetObject
from globalstatemanager.gsm import PollServer
#admin.site.register(StorageHost)
# Register your models here.
#from django.contrib import admin
from admin_stats.admin import StatsAdmin, Avg, Sum
import time
import logging
import django_rq
import os
import ConfigParser
from django import db
from logging import getLogger
#admin.site.disable_action('delete_selected')

#if 'delete_selected' in admin.site.actions:
admin.site.disable_action('delete_selected')

class VGAdmin(StatsAdmin):	
    actions = ['delete_selected']
    readonly_fields = ('vguuid','vghost','totalGB','maxavlGB','CurrentAllocGB')
    list_display = ['vguuid','vghost','storemedia','totalGB','maxavlGB','CurrentAllocGB','is_locked','in_error','is_thin']
    exclude = ('vgsize','vguuid','vgpesize','vgtotalpe','vgfreepe',)
    def has_add_permission(self, request):
        return False
admin.site.register(VG,VGAdmin)


def config_snapshots(StatsAdmin,request,queryset):
    targetList = []
    for obj in queryset:
        targetList.append(obj.iqntar)
    return redirect('snapbackup:snapconfig',targets=obj)
#    return redirect('snapconfig')

def set_identical_pin_for_all_selected_targets(StatsAdmin,request,queryset):
    logger = logging.getLogger(__name__)
    randompin = GenerateRandomPin()
    for obj in queryset:
        obj.pin = randompin
        obj.save()


def delete_selected_iscsi_targets(StatsAdmin,request,queryset):
    logger = logging.getLogger(__name__)
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    config = ConfigParser.RawConfigParser()
    config.read(os.path.join(BASE_DIR,'saturn.ini'))
    numqueues = config.get('saturnring','numqueues')
    jobs =[]
    for obj in queryset:
        queuename = 'queue'+str(hash(obj.targethost)%int(numqueues))
        queue = django_rq.get_queue(queuename)
        jobs = []
        jobs.append( (queue.enqueue(DeleteTargetObject,args=(obj.iqntar,),timeout=45), obj.iqntar) )
        logger.info("Using queue %s for deletion" %(queuename,))
    rtnStatus= {}
    rtnFlag=0
    numDone=0
    timeCtr=0
    while (numDone < len(jobs)) and (timeCtr < 120):
        ii=0
        timeCtr=timeCtr+1
        time.sleep(0.5)
        for ii in range(0,len(jobs)):
            if jobs[ii] == 0:
                continue
            (job,target) = jobs[ii]
            if (job.result == 0) or (job.result == 1):
                if job.result==1:
                    try:
                        logger.error('Failed deletion of '+target)
                        raise forms.ValidationError(
                            ('Failed deletion target: %(target)'),
                            code='invalid', 
                            params={'values': 'Check if session is up'},
                        )
                    except:
                        rtnStatus[target]="Error "+str(job.result)
                rtnFlag=rtnFlag + job.result
                jobs[ii]=0
                numDone=numDone+1
            else:
                logger.info('...Working on deleting target '+target)
                break
    if timeCtr == 120:
        logger.error("Gave up trying to delete after 1 minute")
    return (rtnFlag,str(rtnStatus))

class InterfaceAdmin(StatsAdmin):
    readonly_fields = ('storagehost','ip')
    list_display = ('storagehost','ip','owner')
    def has_add_permission(self, request):
        return False

admin.site.register(Interface,InterfaceAdmin)


class TargetHistoryAdmin(StatsAdmin):
    readonly_fields = ('iqntar','iqnini','sizeinGB','owner','created_at','deleted_at','rkb','wkb')
    list_display = ('iqntar','iqnini','sizeinGB','owner','created_at','deleted_at','rkb','wkb')
    search_fields = ['iqntar','owner__username']
    stats=(Sum('sizeinGB'),Sum('rkb'),Sum('wkb'))
    actions=[]

    def has_change_permission(self, request, obj=None):
        has_class_permission = super(TargetHistoryAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user.id != obj.owner.id:
            return False
        return True

    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None): # note the obj=None
                return False
    
    def queryset(self, request):
        if request.user.is_superuser:
            return TargetHistory.objects.all()
        return TargetHistory.objects.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user
        obj.save()

admin.site.register(TargetHistory,TargetHistoryAdmin)

class TargetAdmin(StatsAdmin):
#    if self.request.user.is_superuser: 
#        readonly_fields = ('targethost','iqnini','iqntar','sizeinGB','owner','rkb','wkb','rkbpm','wkbpm','storageip1','storageip2')
#    else:
#        readonly_fields = ('targethost','iqnini','iqntar','sizeinGB','owner','sessionup','rkb','wkb','rkbpm','wkbpm','storageip1','storageip2')
    def __getstate__(self):
        d = dict(self.__dict__)
        del d['logger']
        return d

    def __setstate__(self, d):
        self.__dict__.update(d)

    list_display = ['iqntar','iqnini','created_at','sizeinGB','isencrypted','aagroup','clumpgroup','rkbpm','wkbpm','sessionup','Physical_Location','owner']
    actions = [delete_selected_iscsi_targets,set_identical_pin_for_all_selected_targets]
    #actions = [delete_selected_iscsi_targets]
    search_fields = ['iqntar','iqnini','lv__lvname','lv__vg__vguuid','targethost__dnsname']
    stats = (Sum('sizeinGB'),)

    def get_readonly_fields(self,request,obj=None):
        if request.user.is_superuser:
            return ('targethost','iqnini','iqntar','sizeinGB','owner','rkb','wkb','rkbpm','wkbpm','storageip1','storageip2','isencrypted')
        else:
            return ('targethost','iqnini','iqntar','sizeinGB','owner','sessionup','rkb','wkb','rkbpm','wkbpm','storageip1','storageip2','isencrypted')

    def has_add_permission(self, request):
        return False
    def Physical_Location(self,obj):
        mylv = LV.objects.get(target=obj)
        return str(mylv.vg) + ":LV:"+str(mylv)

    def has_delete_permission(self, request, obj=None): # note the obj=None
        if request.user.is_superuser:
            return True
        else:
            return False

    def has_change_permission(self, request, obj=None):
        has_class_permission = super(TargetAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user.id != obj.owner.id:
            return False
        return True
    
    def aagroup(self,obj):
        try:
            name = AAGroup.objects.get(target=obj).name
            return name
        except:
            return "No AAGroup"
        
    def clumpgroup(self,obj):
        try:
            name = ClumpGroup.objects.get(target=obj).name
            return name
        except:
            return "No ClumpGroup"
        
    def iscsi_storeip1(self, obj):
        return obj.storageip1

    def iscsi_storeip2(self, obj):
        return obj.storageip2

    def queryset(self, request):
        if request.user.is_superuser:
            return Target.objects.all()
        return Target.objects.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user
        obj.save()

#    def get_actions(self, request):
    #Disable delete
#        actions = super(TargetAdmin, self).get_actions(request)
#        del actions['delete_selected']
#        return actions



class LVAdmin(StatsAdmin):
    readonly_fields = ('target','vg','lvname','lvsize','lvuuid','created_at','isencrypted')
    list_display = ['lvname','vg','target', 'lvsize','lvuuid']
    stats = (Sum('lvsize'),)
    search_fields = ['target__iqntar','target__owner__username','lvname','lvuuid']
    def owner_name(self, instance):
                return instance.target.owner
    owner_name.admin_order_field  = 'target__owner'

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None): # note the obj=None
                return False
    def has_change_permission(self, request, obj=None):
        has_class_permission = super(LVAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user.id != obj.owner.id:
            return False
        return True

    def queryset(self, request):
        if request.user.is_superuser:
            return LV.objects.all()
        return LV.objects.filter(target__owner=request.user)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user
        obj.save()

    def has_add_permission(self, request):
        return False

class LockAdmin(StatsAdmin):
    readonly_fields = ('lockname',)
    list_display = ['lockname','locked']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None): # note the obj=None
        return False

admin.site.register(Lock,LockAdmin)

class AAGroupAdmin(StatsAdmin):
    readonly_fields = ('name','hosts','target')
    list_display = ['name','target','storage_host','target_owner']

    def has_add_permission(self, request):
        return False
    
    def target_owner (self,obj):
        return obj.target.owner

    def storage_host (self,obj):
        return obj.target.targethost



admin.site.register(AAGroup,AAGroupAdmin)

class ClumpGroupAdmin(StatsAdmin):
    readonly_fields = ('name','hosts','target')
    list_display = ['name','target','storage_host','target_owner']

    def has_add_permission(self, request):
        return False
    
    def target_owner (self,obj):
        return obj.target.owner

    def storage_host (self,obj):
        return obj.target.targethost



admin.site.register(ClumpGroup,ClumpGroupAdmin)

class TargetNameMapAdmin(StatsAdmin):
    readonly_fields = ['owner','oldtarname','newtarname','created_at','updated_at']
    list_display = ['newtarname','oldtarname','owner','created_at','updated_at']

    def has_add_permission(self, request):
        return False

#admin.site.register(Provisioner)
admin.site.register(Target, TargetAdmin)
admin.site.register(LV,LVAdmin)
admin.site.register(IPRange)
admin.site.register(TargetNameMap, TargetNameMapAdmin)

class StorageHostForm(forms.ModelForm):
    class Meta:
        model = StorageHost
	
    def clean_dnsname(self):
        logger = getLogger(__name__)
    	saturnserver = self.cleaned_data['dnsname']
        try:
            p = PollServer(saturnserver)
            if (p.InstallScripts() == -1):
                raise Exception("Error creating SSH connection/installing saturn scripts")
        except:
            logger.error(format_exc())
            logger.error("Error with Saturn server specified on the form, will try to disable server "+saturnserver)
            try:
                obj = StorageHost.objects.get(dnsname=saturnserver)
                obj.enabled=False
                obj.save()
                raise forms.ValidationError("Error with Saturn Server, therefore disabled "+saturnserver)
            except:
                logger.error("Could not install scripts on the new server, new server not in DB, check its DNS entry, ssh keys")
                logger.error(format_exc())
                raise forms.ValidationError("Error with Saturn Server, check its DNS entry/SSH key file perhaps? "+saturnserver)
	return self.cleaned_data['dnsname']

class StorageHostAdmin(admin.ModelAdmin):
    form = StorageHostForm
    actions = ['delete_selected']
    list_display=['dnsname','ipaddress','storageip1','storageip2','created_at','updated_at','enabled']
admin.site.register(StorageHost, StorageHostAdmin)



#Code for bringing extended user attributes to Django admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from ssdfrontend.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
    
    def clean_max_alloc_sizeGB(self):
        logger = getLogger(__name__)
        oldalloc = 0
        usedsize = 0
        #Test 1:  if the user has already used more than the new quota
        try:
            requestedGB = self.cleaned_data['max_alloc_sizeGB']
            usedsize = Target.objects.filter(owner=self.cleaned_data['user']).aggregate(used_size=db.models.Sum('sizeinGB'))['used_size']
            if usedsize == None:
                usedsize = 0
            if (usedsize > requestedGB):
                raise forms.ValidationError("Sorry, user targets already using %d GB > new requested quota %d GB, perhaps the user should delete some iSCSI targets before asking for a lower quota." %(usedsize,requestedGB))
        except:
            logger.error(format_exc())
            raise forms.ValidationError("Sorry, user targets already using %d GB > new requested quota %d GB, perhaps the user should delete some iSCSI targets before asking for a lower quota." %(usedsize,requestedGB))
            logger.error("Sorry, user targets already using %d GB > new requested quota %d GB, perhaps the user should delete some iSCSI targets before asking for a lower quota." %(usedsize,requestedGB))

        #Test 2: if the cluster has that much available storage
        try:
            requestedGB = self.cleaned_data['max_alloc_sizeGB']
            if requestedGB == 0:
                return requestedGB
            totalGB = VG.objects.all().aggregate(totalGB=db.models.Sum('totalGB'))['totalGB']
            if totalGB == None:
                totalGB = 0
            allocGB = Profile.objects.all().aggregate(CAGB=db.models.Sum('max_alloc_sizeGB'))['CAGB']
            if allocGB == None:
                allocGB = 0
            thisuser = self.cleaned_data['user']
            try:
                oldalloc = Profile.objects.get(user=thisuser).max_alloc_sizeGB
            except:
                oldalloc = None
            if oldalloc == None:
                oldalloc = 0
            #logger.info("totalGB = %d, Allocated to all users = %d, This users old allocation = %d" %(totalGB,allocGB,oldalloc)) 
            if (totalGB < allocGB+requestedGB-oldalloc) and (requestedGB > oldalloc):
                raise forms.ValidationError("Sorry, cluster capacity exceeded; maximum possible is %d GB" %(totalGB-allocGB+oldalloc,))
        except:
            logger.error(format_exc())
            logger.error("Sorry, cluster capacity exceeded; maximum possible is %d GB" %(totalGB-allocGB+oldalloc,))
            raise forms.ValidationError("Sorry, cluster capacity exceeded; maximum possible is %d GB" %(totalGB-allocGB+oldalloc,))
        return requestedGB


class ProfileInline(admin.StackedInline):
    form = ProfileForm
    model = Profile
    can_delete = False
    list_display=[]
    verbose_name_plural = 'Quota Information'


class UserChangeList(ChangeList):
    def get_results(self, *args, **kwargs):
        super(UserChangeList,self).get_results(*args, **kwargs)
        q = self.result_list.aggregate(total_alloc_GB=db.models.Sum('profile__max_alloc_sizeGB'))
        self.total_alloc_GB = q['total_alloc_GB']


admin.site.unregister(User)
class UserAdmin(UserAdmin):
    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            obj.is_staff = True
            obj.save()

    inlines = (ProfileInline,)
    list_display = ('username','email', 'max_alloc_GB','used_GB','max_target_GB')

    def get_changelist(self, request):
        return UserChangeList

    def max_target_GB(self, obj):
        try:
            mts = obj.profile.max_target_sizeGB 
            return mts
        except:
            return ""
    max_target_GB.short_description = 'Max Target size GB'

    def used_GB(self,obj):
        try:
            usedsize = Target.objects.filter(owner=obj).aggregate(used_size=db.models.Sum('sizeinGB'))['used_size']
            if usedsize == None:
                usedsize = 0
            return usedsize
        except:
            return ""
    used_GB.short_description = 'Currently used GB'

    def max_alloc_GB(self, obj):
     try:
        ma = obj.profile.max_alloc_sizeGB 
        return ma
     except:
         return ""
    max_alloc_GB.short_description = 'Assigned quota GB'

admin.site.register(User, UserAdmin)
