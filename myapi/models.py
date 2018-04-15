# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from brethren import settings

# Create your models here.

class Content(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50, blank=False, default='')
    path = models.TextField()
    actualfile = models.FileField(upload_to='files/')
    description = models.CharField(max_length=100, blank=True, default='')
    owner = models.ForeignKey('auth.User', related_name='content_files', on_delete=models.CASCADE)
    filetype = models.CharField(max_length=10, editable=False)

    class Meta:
        ordering = ('created',)
# upload = models.FileField(upload_to='content/') #TODO: make the upload_to value be set by user with a dropdown menu. options: /content, /private

    # def getTitle(self): # Gets the title of the file from its path
    #     return self.actualfile.url.split('.')[-1]

    def getFileType(self): # Gets the filetype of the file from its title
        return self.actualfile.url.split('.')[-1].lower()

    def getFileName(self): # Gets the name of the file by eliminating the extension(thing after the last period)
        name = self.split('.')
        del name[-1]
        return ''.join(str(piece) for piece in name)

    def save(self, *args, **kwargs):
        self.path = self.actualfile.url
        self.filetype = self.getFileType()
        super(Content, self).save(*args, **kwargs)
