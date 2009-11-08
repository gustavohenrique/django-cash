from copy import copy, deepcopy
from django import forms
from django.core.serializers.json import DjangoJSONEncoder
from django.forms import fields
from django.forms.forms import BoundField
from django.forms.models import  ModelChoiceField, ModelMultipleChoiceField

from custom import TextField, PositiveDecimalField, HiddenIdField


class ExtJSONEncoder(DjangoJSONEncoder):
    """
    JSONEncoder subclass that knows how to encode django forms into ExtJS config objects.
    """

    CHECKBOX_EDITOR = {
        'xtype': 'checkbox',
        'checked': False,
    }
    COMBO_EDITOR = {
        'width': 150,
        'xtype': 'combo',
    }
    DATE_EDITOR = {
        'xtype': 'datefield',
        'format': 'd/m/Y',
        #'cls': 'brdatefield',
        #'cls': "{mask:'99/99/9999'}",
        'minLength': 10,
        'maxLength': 10,
    }
    EMAIL_EDITOR = {
        'vtype': 'email',
        'xtype': 'textfield'
    }
    NUMBER_EDITOR = {
        'xtype': 'numberfield',
        'allowNegative': False,
    }
    HIDDEN_EDITOR = {
        'xtype': 'hidden',
    }
    TEXT_EDITOR = {
        'xtype': 'textfield'
    }
    TEXTAREA_EDITOR = {
        'xtype': 'textarea'
    }
    TIME_EDITOR = {
        'xtype': 'timefield'
    }
    URL_EDITOR = {
        'vtype': 'url',
        'xtype': 'textfield'
    }
    FILE_EDITOR = {
        'xtype': 'textfield',
        'inputType': 'file'
    }

    CHAR_PIXEL_WIDTH = 8

    EXT_DEFAULT_CONFIG = {
        'editor': TEXT_EDITOR
    }

    DJANGO_EXT_FIELD_TYPES = {
        fields.BooleanField: ["Ext.form.Checkbox", CHECKBOX_EDITOR],
        fields.CharField: ["Ext.form.TextField", TEXT_EDITOR],
        TextField: ["Ext.form.TextArea", TEXTAREA_EDITOR],
        HiddenIdField: ["Ext.form.TextArea", HIDDEN_EDITOR],
        fields.ChoiceField: ["Ext.form.ComboBox", COMBO_EDITOR],
        fields.DateField: ["Ext.form.DateField", DATE_EDITOR],
        fields.DateTimeField: ["Ext.form.DateField", DATE_EDITOR],
        fields.DecimalField: ["Ext.form.NumberField", NUMBER_EDITOR],
        PositiveDecimalField: ["Ext.form.NumberField", NUMBER_EDITOR],
        fields.EmailField: ["Ext.form.TextField", EMAIL_EDITOR],
        fields.IntegerField: ["Ext.form.NumberField", NUMBER_EDITOR],
        ModelChoiceField: ["Ext.form.ComboBox", COMBO_EDITOR],
        ModelMultipleChoiceField: ["Ext.form.ComboBox", COMBO_EDITOR],
        fields.MultipleChoiceField: ["Ext.form.ComboBox",COMBO_EDITOR],
        fields.NullBooleanField: ["Ext.form.Checkbox", CHECKBOX_EDITOR],
        fields.SplitDateTimeField: ["Ext.form.DateField", DATE_EDITOR],
        fields.TimeField: ["Ext.form.DateField", TIME_EDITOR],
        fields.URLField: ["Ext.form.TextField", URL_EDITOR],
        #HiddenField: ["Ext.form.TextField", HIDDEN_EDITOR],
        fields.FileField: ["Ext.form.TextField", FILE_EDITOR],
    }

    #EXT_DATE_ALT_FORMATS = 'm/d/Y|n/j/Y|n/j/y|m/j/y|n/d/y|m/j/Y|n/d/Y|m-d-y|m-d-Y|m/d|m-d|md|mdy|mdY|d|Y-m-d'
    EXT_DATE_ALT_FORMATS = 'd/m/Y'

    EXT_TIME_ALT_FORMATS = 'm/d/Y|m-d-y|m-d-Y|m/d|m-d|d'

    DJANGO_EXT_FIELD_ATTRS = {
        #Key: django field attribute name
        #Value: tuple[0] = ext field attribute name,
        #       tuple[1] = default value
        'choices': ['store', None],
        #'default': ['value', None],
        'fieldset': ['fieldSet', None],
        'help_text': ['helpText', None],
        'initial': ['value', None],
        #'input_formats': ['altFormats', None],
        'label': ['fieldLabel', None],
        'max_length': ['maxLength', None],
        'max_value': ['maxValue', None],
        'min_value': ['minValue', None],
        'name': ['name', None],
        'required': ['allowBlank', False],
        'size': ['width', None],
        'show_hidden_initial': ['hidden', False],
    }

    def default(self, o, form=None, field_name=None):
        if issubclass(o.__class__, (forms.Form,forms.BaseForm)):
            flds = []

            for name, field in o.fields.items():
                if isinstance(field, dict):
                    field['title'] = name
                else:
                    field.name = name
                cfg = self.default(field, o, name)
                flds.append(cfg)
            return flds
        elif isinstance(o, dict):
            #Fieldset
            default_config = {
                'autoHeight': True,
                'collapsible': True,
                'items': [],
                'labelWidth': 100,
                'title': o['title'],
                'xtype':'fieldset',
                'fieldHidden': False
            }
            del o['title']

            #Ensure fields are added sorted by position
            for name, field in sorted(o.items()):
                field.name = name
                default_config['items'].append(self.default(field))
            return default_config
        elif issubclass(o.__class__, fields.Field):
            #bf = form and form.is_bound and BoundField(form, o, field_name) or None
            bf = BoundField(form, o, field_name)
            default_config = {}


            #if field_name == 'pk':
            #    DJANGO_EXT_FIELD_ATTRS.update({'hidden':['fieldHidden',True]})
            #    print field_name


            if o.__class__ in self.DJANGO_EXT_FIELD_TYPES:
                default_config.update(self.DJANGO_EXT_FIELD_TYPES[o.__class__][1])
            else:
                default_config.update(self.EXT_DEFAULT_CONFIG['editor'])
            config = deepcopy(default_config)
            if bf:
                config['invalidText']="".join(form[field_name].errors)

            if form and form.is_bound:
                data = bf.data
            else:
                if field_name:
                    data = form.initial.get(field_name, o.initial)
                    if callable(data):
                        data = data()
                else:
                    data = None
            if o.__class__ == PositiveDecimalField or o.__class__ == fields.DecimalField:
                data = str(data).replace('-','')
                
            elif o.__class__ == fields.BooleanField:
                config['checked'] = [False, True] [data == True]
            elif o.__class__ == fields.DateField:
                import datetime, time
                if data is not None:
                    data = data.strftime('%d/%m/%Y')
                
            config['value'] = data
            

            for dj, ext in self.DJANGO_EXT_FIELD_ATTRS.items():
                v = None
                if dj == 'size':
                    v = o.widget.attrs.get(dj, None)
                    if v is not None:
                        if o.__class__ in (fields.DateField, fields.DateTimeField,
                           fields.SplitDateTimeField, fields.TimeField):
                            v += 8
                        #Django's size attribute is the number of characters,
                        #so multiply by the pixel width of a character
                        v = v * self.CHAR_PIXEL_WIDTH
                elif dj == 'hidden':
                    v = o.widget.attrs.get(dj, default_config.get('fieldHidden', ext[1]))
                elif dj == 'name':
                    v = bf and bf.html_name or field_name
                elif dj == 'label':
                    v = bf and bf.label or getattr(o, dj, ext[1])
                elif getattr(o, dj, ext[1]) is None:
                    #print "dj:%s field name:%s"%(dj,field_name)
                    pass
                #elif dj == 'input_formats':
                    #alt_fmts = []
                    ##Strip out the '%'  placeholders
                    #for fmt in getattr(field, dj, ext[1]):
                        #alt_fmts.append(fmt.replace('%', ''))
                    #v = u'|'.join(alt_fmts)
                elif isinstance(ext[1], basestring):
                    v = getattr(o, dj, getattr(field, ext[1]))
                elif ext[0] == 'store':
                    v = {
                        'autoLoad': True,
                        'storeId': o.name,
                        'url': '/csds/ext/rdo/queryset/%s/' % (o.name.lower(),),
                        #'xtype': 'jsonstore',
                    }
                elif dj == 'required':
                    try:
                        v = not getattr(o, dj)
                    except AttributeError :
                        v = ext[1]
                else:
                    v = getattr(o, dj, ext[1])
                if v is not None:
                    if ext[0] == 'name':
                        config[ext[0]] = v
                        config['header'] = v
                    elif ext[0] not in ('name', 'dataIndex', 'fieldLabel', 'header', 'defaultValue'):
                    #elif ext[0] in ('allowBlank', 'listWidth', 'store', 'width'):
                            #if isinstance(v, QuerySetIterator):
                            #    config['editor'][ext[0]] = list(v)
                        config[ext[0]] = v
                        if ext[0] == 'store':
                            #config['url'] = v['url']
                            choices = [(c[0],c[1]) for c in o.choices]
                            config['store'] = choices
                            config['displayField'] = 'display'
                            config['editable'] = False
                            #config['editor']['forceSelection'] = True
                            config['hiddenName'] = o.name
                            #config['lastQuery'] = ''
                            config['mode'] = 'local'
                            config['triggerAction'] = 'all'
                            #config['valueField'] = 'id'

                    elif isinstance(v, unicode):
                        config[ext[0]] = v.encode('utf8')
                    else:
                        config[ext[0]] = v
            return config
        else:
            return super(ExtJSONEncoder, self).default(o)
