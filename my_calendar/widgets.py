# from django import forms
# from django.db import models
# from django.forms import fields
# from django.forms.widgets import Select, MultiWidget, DateInput, TextInput

# from time import strptime, strftime


# class JqSplitDateTimeWidget(MultiWidget):
#     def __init__(self, attrs=None, date_format=None, time_format=None):
#         date_class = attrs['date_class']
#         time_class = attrs['time_class']
#         del attrs['time_class']
#         del attrs['date_class']

#         time_attrs = attrs.copy()
#         time_attrs['class'] = time_class
#         date_attrs = attrs.copy()
#         date_attrs['class'] = date_class

#         widgets = (DateInput(attrs=date_attrs, format=date_format),
#         		   TextInput(attrs=time_attrs), TextInput(attrs=time_attrs))

#         super(JqSplitDateTimeWidget, self).__init__(widgets, attrs)

#         def decompress(self, value):
#         	if value:
#         		date = strftime("%d-%m-%Y", value.timetuple())
#         		hour = strftime("%H", value.timetuple())
#         		minute = strftime("%M", value.timetuple())
#         		return (date, hour, minute)
#         	else:
#         		return (None, None, None)

#         def format_output(self, rendered_widgets):
#         	return "Date: %s<br/>Time: %s:%s" % (rendered_widgets[0], rendered_widgets[1], rendered_widgets[2])

        	
# class JqSplitDateTimeField(fields.MultiValueField):
#     widget = JqSplitDateTimeWidget

#     def __init__(self, *args, **kwargs):
#         all_fields = (fields.CharField(max_length=10),
#                       fields.CharField(max_length=2),
#                       fields.CharField(max_length=2))
#         super(JqSplitDateTimeField, self).__init__(all_fields, *args, **kwargs)

#     def compress(self, data_list):
#         if data_list:
#             if not (data_list[0] and data_list[1]) and data_list[2]:
#                 raise forms.ValidationError("Missing data.")
#             input_time = strptime("%s:%s"%(data_list[1], data_list[2]))
#             datetime_string = "%s %s" % (data_list[0], strftime('%H:%M', input_time))
#             print("Datetime: %s"%datetime_string)
#             return datetime_string
#         return None

