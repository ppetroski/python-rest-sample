from flask import request
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, validates
from components.framework.baseModel import BaseModel, RelationsBase
import components.validator as validator


def ip_address():
    ip = None
    try:
        assert isinstance(request.remote_addr, object)
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    finally:
        return ip

def geo_location():
    geo = None
    try:
        """
        Need license, but I think the "How to" was more important then then actually result. 
        This would return IP location, which I don't believe make sense - as this looks like an Admin interface  
        I assume GPS coordinates was desired, again no free resources and depending on the application
        Should be done "offline" as to not delay or fail the API call. 
        geo = requests.get(f'https://geoip.maxmind.com/geoip/v2.1/city/{request.remote_addr}?demo=1')
        """
    finally:
        return geo

class Interaction(BaseModel, RelationsBase):
    __tablename__ = 'trk_Interaction'
    _remove_columns = ['updated_at', 'deleted_at']
    # Model attributes
    pid_Profile = Column(Integer, ForeignKey('pid_Profile.id'))
    type = Column(String(length=50))
    outcome = Column(String(length=50))
    ip_address = Column(String(length=50), default=ip_address)
    geo_location = Column(String(), default=geo_location)
    # Model relationships
    profile = relationship('Profile', back_populates='interactions')

    @validates('pid_Profile')
    def validate_type(self, key, value):
        return validator.is_int(self, key, value)

    @validates('type')
    def validate_type(self, key, value):
        value = value.upper()
        validator.has_value(self, key, value, ['IN-PERSON', 'EMAIL', 'PHONE', 'SMS'])
        return validator.is_string(self, key, value)

    @validates('outcome')
    def validate_outcome(self, key, value):
        value = value.upper()
        validator.has_value(self, key, value, ['CONTACTED', 'NOT HOME', 'NO ANSWER', 'NO RESPONSE'])
        return validator.is_string(self, key, value)

    @validates('ip_address')
    def validate_ip_address(self, key, value):
        return validator.is_string(self, key, value)

