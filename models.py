from django.db.models import * 

from django.contrib.auth.models import User 
# Create your models here.

# create model for task table  

class Task (Model) : 
    user  = ForeignKey(User , on_delete=CASCADE )
    srno =  AutoField(primary_key= True , auto_created= True ) 
    text  =  CharField(max_length=255 )
    status = BooleanField( default=False )
    date = DateTimeField(  auto_now_add=True )

    def __str__(self):
        return  f'{self.text}'



