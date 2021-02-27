from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, validates

import components.validator as validator
from components.framework.baseModel import BaseModel, RelationsBase


def geo_location():
    geo = None
    try:
        """
        Need license, but I think the "How to" was more important then then actually result. 
        This would return IP location, not physical address location, which I don't believe make sense. 
        I assume GPS coordinates was desired, again no free resources and depending on the application
        Should be done "offline" as to not delay or fail the API call. 
        geo = requests.get(f'https://geoip.maxmind.com/geoip/v2.1/city/{request.remote_addr}?demo=1')
        """
    finally:
        return geo

class Profile(BaseModel, RelationsBase):
    __tablename__ = 'pid_Profile'
    _remove_columns = ['created_at', 'updated_at', 'deleted_at']
    # Model attributes
    first_name = Column(String(length=25))
    last_name = Column(String(length=25))
    email = Column(String(length=100))
    address1 = Column(String(length=100))
    address2 = Column(String(length=100))
    locality = Column(String(length=100))
    state = Column(String(length=100))  # This would normally an INT relation to an xref table
    postcode = Column(String(length=20))
    phone = Column(String(length=20))
    mobile = Column(String(length=25))
    geo_location = Column(String(), default=geo_location())
    # Model relationships
    interactions = relationship('Interaction', back_populates='profile')

    @validates('first_name')
    def validate_first_name(self, key, value):
        return validator.is_string(self, key, value)

    @validates('last_name')
    def validate_last_name(self, key, value):
        return validator.is_string(self, key, value)

    @validates('email')
    def validate_email(self, key, value):
        return validator.is_email(self, key, value)

    @validates('address1')
    def validate_address1(self, key, value):
        return validator.is_string(self, key, value)

    @validates('address2')
    def validate_address2(self, key, value):
        return validator.is_string(self, key, value)

    @validates('locality')
    def validate_locality(self, key, value):
        return validator.is_string(self, key, value)

    @validates('state')
    def validate_state(self, key, value):
        return validator.is_string(self, key, value)

    @validates('postcode')
    def validate_postcode(self, key, value):
        return validator.is_string(self, key, value)

    @validates('phone')
    def validate_phone(self, key, value):
        return validator.is_string(self, key, value)

    @validates('mobile')
    def validate_mobile(self, key, value):
        return validator.is_string(self, key, value)
