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

class OneTimeSchedulerJobForm(forms.Form):
    temp_id = forms.CharField(widget=forms.HiddenInput())
    original_job_name = forms.CharField(widget=forms.HiddenInput())
    job_name = forms.CharField(widget=forms.TextInput(attrs={"class":"required", "style":"width:100%"}))
    service = forms.CharField(widget=forms.TextInput(attrs={"class":"required", "style":"width:100%"}))
    extra = forms.CharField(widget=forms.Textarea(attrs={"style":"width:100%"}))

    # The only attribute specific to one-time jobs.
    date_time = forms.CharField(widget=forms.TextInput(attrs={"class":"required", "style":"width:30%; height:19px"}))

class IntervalBasedSchedulerJobForm(forms.Form):
    temp_id = forms.CharField(widget=forms.HiddenInput())
    original_job_name = forms.CharField(widget=forms.HiddenInput())
    job_name = forms.CharField(widget=forms.TextInput(attrs={"class":"required", "style":"width:100%"}))
    service = forms.CharField(widget=forms.TextInput(attrs={"class":"required", "style":"width:100%"}))
    extra = forms.CharField(widget=forms.Textarea(attrs={"style":"width:100%"}))

    # Attributes specific to interval-based jobs.
    weeks = forms.CharField(widget=forms.TextInput(attrs={"class":"validate-digits", "style":"width:8%"}))
    days = forms.CharField(widget=forms.TextInput(attrs={"class":"validate-digits", "style":"width:8%"}))
    hours = forms.CharField(widget=forms.TextInput(attrs={"class":"validate-digits", "style":"width:8%"}))
    minutes = forms.CharField(widget=forms.TextInput(attrs={"class":"validate-digits", "style":"width:8%"}))
    seconds = forms.CharField(widget=forms.TextInput(attrs={"class":"validate-digits", "style":"width:8%"}))
    start_date = forms.CharField(widget=forms.TextInput(attrs={"class":"required", "style":"width:30%; height:19px"}))
    repeat = forms.CharField(widget=forms.TextInput(attrs={"style":"width:8%"}))