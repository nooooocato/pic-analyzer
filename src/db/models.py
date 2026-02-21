from peewee import (
    Model, CharField, IntegerField, DateTimeField, 
    ForeignKeyField, BlobField, Proxy, TextField
)
import datetime

db_proxy = Proxy()

class BaseModel(Model):
    class Meta:
        database = db_proxy

class Workspace(BaseModel):
    name = CharField(unique=True)
    path = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        table_name = 'workspaces'

class Image(BaseModel):
    workspace = ForeignKeyField(Workspace, backref='images', on_delete='CASCADE')
    path = CharField(unique=True)
    filename = CharField()
    file_size = IntegerField(null=True)
    created_at = DateTimeField(null=True)
    modified_at = IntegerField(null=True)
    thumbnail = BlobField(null=True)
    
    class Meta:
        table_name = 'images'

class AnalysisResult(BaseModel):
    image = ForeignKeyField(Image, backref='analysis_results', on_delete='CASCADE')
    plugin_name = CharField()
    result_data = TextField() # Store as JSON string or text
    timestamp = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        table_name = 'analysis_results'

class SidebarState(BaseModel):
    workspace = ForeignKeyField(Workspace, backref='sidebar_states', on_delete='CASCADE')
    # Store the entire rules dict as JSON
    config_data = TextField()
    updated_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'sidebar_states'
