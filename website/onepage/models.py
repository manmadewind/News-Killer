from django.db import models

# Create your models here.



class Article(models.Model):
    aid          = models.AutoField(primary_key=True)
    title        = models.CharField(max_length=80)
    summary      = models.TextField(null = True)
    content      = models.TextField(null=True)
    img_link     = models.URLField(max_length=300, null=True)    
    pub_time     = models.DateTimeField(null=True)
    origin       = models.CharField(max_length=80, null=True)    
    link         = models.URLField(null=True)

    mm_summary   = models.TextField(null=True)
    mm_labels    = models.TextField(null=True)
    mm_score     = models.IntegerField(null=True)
    hit_count     = models.IntegerField(null=True)
    origin_count  = models.IntegerField(null=True)
    like_count    = models.IntegerField(null=True)
    dislike_count = models.IntegerField(null=True)

    create_date  = models.DateField(auto_now=True)

    def __unicode__(self):
        return self.title


    #    hit_ref = models.ManyToManyField(User)
    #    link_ref = models.ManyToManyField(User)
    
class User(models.Model):
    uid         = models.AutoField(primary_key=True)
    psw         = models.CharField(max_length=256) # sha-1
    regist_date = models.DateField(null=True)
    email       = models.EmailField(max_length = 100, null=True)
    
    hit_count     = models.IntegerField(null=True)
    origin_count  = models.IntegerField(null=True)
    like_count    = models.IntegerField(null=True)
    dislike_count = models.IntegerField(null=True)

    pushmail      = models.BooleanField()
    def __unicode__(self):
        return self.email


class Behavior(models.Model):
    aid = models.IntegerField(null=True)
    uid = models.IntegerField(null=True)
    op = models.IntegerField(null=True) # 1: like; 2: dislike; 0: NULL
    op_time = models.DateTimeField(null=True)
    def __unicode__(self):
        return ("%d :: %d :: %d" % (self.uid, self.op, self.aid))

class Login(models.Model):
    uid = models.IntegerField(null=True)
    login_time = models.DateTimeField(null=True)
    ip = models.IPAddressField(null=True)

    def __unicode__(self):
        return self.uid
