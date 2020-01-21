from django import forms


class LoginForm(forms.Form):
    def as_p(self):
        return self._html_output(
            normal_row=u'<p%(html_class_attr)s>%(label)s</p> %(field)s%(help_text)s',
            error_row=u'%s',
            row_ender='</p>',
            help_text_html=u' <span class="helptext">%s</span>',
            errors_on_separate_row=True)