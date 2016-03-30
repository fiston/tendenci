import imghdr
from os.path import splitext

from django import forms

from tendenci.apps.perms.forms import TendenciBaseForm
from tendenci.apps.staff.models import Staff, StaffFile
#from tendenci.apps.files.models import File
from tendenci.libs.tinymce.widgets import TinyMCE

ALLOWED_LOGO_EXT = (
    '.jpg',
    '.jpeg',
    '.gif',
    '.png'
)

class StaffForm(TendenciBaseForm):

    biography = forms.CharField(required=False,
        widget=TinyMCE(attrs={'style':'width:100%'},
        mce_attrs={'storme_app_label':Staff._meta.app_label,
        'storme_model':Staff._meta.model_name.lower()}))

    cv = forms.CharField(
        label='CV',
        required=False,
        widget=TinyMCE(attrs={'style':'width:100%'},
            mce_attrs={'storme_app_label':Staff._meta.app_label,
            'storme_model':Staff._meta.model_name.lower()}))
    
    status_detail = forms.ChoiceField(choices=(('active','Active'),('inactive','Inactive')))

    def clean_photo(self):
        photo = self.cleaned_data['photo']
        if photo:
            extension = splitext(photo.name)[1]

            # check the extension
            if extension.lower() not in ALLOWED_LOGO_EXT:
                raise forms.ValidationError('The photo must be of jpg, gif, or png image type.')

            # check the image header
            image_type = '.%s' % imghdr.what('', photo.read())
            if image_type not in ALLOWED_LOGO_EXT:
                raise forms.ValidationError('The photo is an invalid image. Try uploading another photo.')

        return photo

    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['biography'].widget.mce_attrs['app_instance_id'] = self.instance.pk
        else:
            self.fields['biography'].widget.mce_attrs['app_instance_id'] = 0

    class Meta:
        model = Staff
        fields = (
            'name',
            'slug',
            'department',
            'positions',
            'biography',
            'cv',         
            'email',
            'phone',
            'personal_sites',
            'tags',
            'allow_anonymous_view',
            'user_perms',
            'group_perms',
            'member_perms',
            'status_detail',
        )

class FileForm(forms.ModelForm):
    class Meta:
        model = StaffFile
        fields = (
            'file',
            'description',
            'photo_type',
            'position',
        )

    def __init__(self, *args, **kwargs):
        super(FileForm, self).__init__(*args, **kwargs)
