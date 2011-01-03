from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from forms import UploadFileForm
from bulk_uploader import bulk_uploader

@login_required
def bulk_upload(request,status=None):
    messages = []
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        print request.FILES
        if form.is_valid():
            try:
               bulk_uploader(request.FILES['file'])
               return HttpResponseRedirect('./bulk_upload/success')
            except Exception,e:
               messages.append({'type':'error','text':'Error Updating database. Error was %s'%e})
        else:
            messages.append({'type':'error','text':'Form is invalid. Check filename'})
    else:
        if status == 'success':
            messages.append({'type':'success','text':'The File is uploaded successfully and database has been updated'})
        form = UploadFileForm()
    return render_to_response('janitor/bulk_upload.html', {'form': form, 'messages': messages}, context_instance=RequestContext(request))
