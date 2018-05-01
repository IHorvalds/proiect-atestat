# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from django.core.files.base import File
import os, os.path
import mammoth
import random

# Creating the model.

class Content(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50, blank=False, default='')
    subtitle = models.CharField(max_length=70, blank=True, default='')
    author = models.CharField(max_length=25, blank=False, default='auth.User')
    path = models.TextField()
    actualfile = models.FileField(upload_to='articles/')
    articleimage = models.FileField(upload_to='article-images/')
    description = models.CharField(max_length=100, blank=True, default='')
    owner = models.ForeignKey('auth.User', related_name='content_files', on_delete=models.CASCADE)
    filetype = models.CharField(max_length=10, editable=False)
    ispublic = models.BooleanField(default=False)

    class Meta:
        ordering = ('created',)

    def getFileType(self): # Gets the filetype of the file from its title
        return self.actualfile.path.split('.')[-1].lower()

    def getFileName(self): # Gets the name of the file by eliminating the extension(thing after the last period)
        name = self.split('.')
        del name[-1]
        return ''.join(str(piece) for piece in name)

    def convertDocxToHtml(self):
        result = mammoth.convert_to_html(self.actualfile.file)
        actualfilepath = self.actualfile.path.split('.')
        actualfilepath[-1] = '.html'
        finalpath = ''.join(str(piece) for piece in actualfilepath)
        fh = open(finalpath, "wb")
        fh.write(result.value.encode('utf-8')) #we're writing at the resource(i.e. path) we're going to be copying to the self.actualfile
        fh.close()
        old_path = self.actualfile.path
        self.actualfile.save(os.path.basename(finalpath), File(open(finalpath, "rwb")), save=True)
        try:
            os.remove(finalpath)
            try:
                os.remove(old_path)
            except:
                ("Couldn't delete " + old_path)
        except:
            print("Couldn't delete " + finalpath)


    def save(self, *args, **kwargs):
        if self.getFileType() == 'docx':
            self.convertDocxToHtml()
        if self.getFileType() in ['png', 'jpg', 'jpeg']:
            self.articleimage = self.actualfile
        self.filetype = self.getFileType() #not doing this earlier because we're converting some files
        self.path = self.actualfile.url
        super(Content, self).save(*args, **kwargs)
