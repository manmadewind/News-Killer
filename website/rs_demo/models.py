from django.db import models

# Create your models here.
class Article(models.Model):
    aid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=80)
    publish_date = models.DateField(null=True)
    link = models.URLField()
    summary = models.TextField(null = True)
    auto_summary = models.TextField(null = True)
    img = models.URLField(max_length = 300, null=True)
    labels = models.TextField(null=True)
    
    hit = models.IntegerField()
    like = models.IntegerField()#models.CommaSeparatedIntegerField()

    hit_list = models.CommaSeparatedIntegerField(max_length=2048, null = True)
    like_list = models.CommaSeparatedIntegerField(max_length=2048, null = True)

    def __unicode__(self):
        return self.title


    #    hit_ref = models.ManyToManyField(User)
    #    link_ref = models.ManyToManyField(User)
    
class User(models.Model):
    uid = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 30)
    psw = models.CharField(max_length=256) # sha-1
    regist_date = models.DateField()
    email = models.EmailField(max_length = 100)
    
    hit_list = models.CommaSeparatedIntegerField(max_length=2048, null = True)
    like_list = models.CommaSeparatedIntegerField(max_length=2048, null = True)

    hit_ref = models.ManyToManyField(Article ,related_name='h+', null = True)
    link_ref = models.ManyToManyField(Article, related_name='l+', null = True)

    def __unicode__(self):
        return name


