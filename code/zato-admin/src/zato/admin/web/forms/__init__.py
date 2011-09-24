# -*- coding: utf-8 -*-

"""
Copyright (C) 2010 Dariusz Suchojad <dsuch at gefira.pl>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

# Django
from django import forms

class ChooseClusterForm(forms.Form):
    cluster = forms.ChoiceField(widget=forms.Select())

    def __init__(self, clusters, post_data=None):
        super(ChooseClusterForm, self).__init__(post_data)
        self.fields["cluster"].choices = [("", "----------")]
        for cluster in clusters:
            server_info = "{0} - https://{1}:{2}".format(cluster.name, cluster.sec_server_host, cluster.sec_server_port)
            self.fields["cluster"].choices.append([cluster.id, server_info])

class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"required"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"required validate-password-confirm"}))