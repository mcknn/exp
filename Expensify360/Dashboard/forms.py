from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, HTML
from crispy_forms.bootstrap import FormActions
from django.contrib.auth.forms import UserCreationForm

# crispy docs: https://django-crispy-forms.readthedocs.io/en/latest/


class CreateOrgForm(forms.Form):
    Organization_Name = forms.CharField()

    helper = FormHelper()
    helper.form_class = 'bootstrap4'
    helper.layout = Layout(
        Field('Organization_Name', css_class='input-xlarge'),

        FormActions(
            Submit('create', 'Create', css_class="btn btn-primary btn-me me-2"),
            HTML("<a href={% url 'home' %} class='btn btn-secondary text-dark btn-me me-2'>Cancel</a>")
        )
    )


class CreateProjForm(forms.Form):
    Project_Name = forms.CharField()

    helper = FormHelper()
    helper.form_class = 'bootstrap4'
    helper.layout = Layout(
        Field('Project_Name', css_class='input-xlarge'),

        FormActions(
            Submit('create', 'Create', css_class="btn btn-primary btn-me me-2"),
            HTML("<a href={% url 'home' %} class='btn btn-secondary text-dark btn-me me-2'>Cancel</a>")
        )
    )
    

class ManageUsers(forms.Form):
    
    # TODO: add user to project

    helper = FormHelper()
    helper.form_class = 'bootstrap4'
    helper.layout = Layout(
        FormActions(
            Submit('add-user', 'Add User', css_class="btn btn-primary btn-me me-2"),
        )
    )


class RemoveUser(forms.Form):
    Username = forms.CharField()

    helper = FormHelper()
    helper.form_class = 'bootstrap4'
    helper.layout = Layout(
        Field('Username', css_class='input-xlarge'),

        FormActions(
            Submit('remove-user', 'Remove User', css_class="btn btn-primary btn-me me-2"),
        )
    )


class SubmitOrCancel(forms.Form):
    helper = FormHelper()
    helper.form_class = 'bootstrap4'
    helper.layout = Layout(

        FormActions(
            Submit('register', 'Create Account', css_class="btn btn-primary btn-me me-2"),
            HTML("<a href={% url 'user_management' %} class='btn btn-secondary text-dark btn-me me-2'>Cancel</a>")
        )
    )


class AddToGroup(forms.Form):
    helper = FormHelper()
    helper.form_class = 'bootstrap4'
    helper.layout = Layout(

        FormActions(
            Submit('add-group', 'Add To Group', css_class="btn btn-primary btn-me me-2"),
        )
    )


class UserNameForm(forms.Form):
    Username = forms.CharField()

    helper = FormHelper()
    helper.form_class = 'bootstrap4'
    helper.layout = Layout(
        Field('Username', css_class='input-xlarge')
    )


class SelectGroupForm(forms.Form):
    helper = FormHelper()
    helper.form_class = 'bootstrap4'
    helper.layout = Layout(

        FormActions(
            Submit('select_group', 'Add', css_class="btn btn-primary btn-me me-2"),
        )
    )


class ManageGroups(forms.Form):
    pass
    # TODO: edit group name
    # TODO: delete group
    # TODO: add user
    # TODO: change manager


'''
crispy gist, here for reference. from https://gist.github.com/maraujop/1838193

# -*- coding: utf-8 -*-
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


class MessageForm(forms.Form):
    text_input = forms.CharField()

    textarea = forms.CharField(
        widget = forms.Textarea(),
    )

    radio_buttons = forms.ChoiceField(
        choices = (
            ('option_one', "Option one is this and that be sure to include why it's great"), 
            ('option_two', "Option two can is something else and selecting it will deselect option one")
        ),
        widget = forms.RadioSelect,
        initial = 'option_two',
    )

    checkboxes = forms.MultipleChoiceField(
        choices = (
            ('option_one', "Option one is this and that be sure to include why it's great"), 
            ('option_two', 'Option two can also be checked and included in form results'),
            ('option_three', 'Option three can yes, you guessed it also be checked and included in form results')
        ),
        initial = 'option_one',
        widget = forms.CheckboxSelectMultiple,
        help_text = "<strong>Note:</strong> Labels surround all the options for much larger click areas and a more usable form.",
    )

    appended_text = forms.CharField(
        help_text = "Here's more help text"
    )

    prepended_text = forms.CharField()

    prepended_text_two = forms.CharField()

    multicolon_select = forms.MultipleChoiceField(
        choices = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')),
    )

    # Uni-form
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('text_input', css_class='input-xlarge'),
        Field('textarea', rows="3", css_class='input-xlarge'),
        'radio_buttons',
        Field('checkboxes', style="background: #FAFAFA; padding: 10px;"),
        AppendedText('appended_text', '.00'),
        PrependedText('prepended_text', '<input type="checkbox" checked="checked" value="" id="" name="">', active=True),
        PrependedText('prepended_text_two', '@'),
        'multicolon_select',
        FormActions(
            Submit('save_changes', 'Save changes', css_class="btn-primary"),
            Submit('cancel', 'Cancel'),
        )
    )
'''
