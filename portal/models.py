import datetime

from sqlalchemy import ForeignKey
from portal import db, login
from flask_login import UserMixin

@login.user_loader
def load_user(id_user):
    return User_otms.query.get(int(id_user))

class User_otms(db.Model, UserMixin):
    id_user = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    group_loc = db.Column(db.String(50), nullable=True)

    def get_id(self):
        return self.id_user
    def get_name(self):
        return self.name

class Rpn(db.Model):
    id_rpn = db.Column(db.Integer, primary_key=True)
    c_impact_id = db.Column(db.Integer, nullable=True)
    spare_av_id = db.Column(db.Integer, nullable=True)
    spare_c_id = db.Column(db.Integer, nullable=True)
    scomplexity_id = db.Column(db.Integer, nullable=True)
    loc_id = db.Column(db.Integer, nullable=True)
    part_id = db.Column(db.Integer, nullable=True)
    sgroups_id = db.Column(db.Integer, nullable=True)
    vendorsuport_id = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String(500), nullable=True)
    last_modified = db.Column(db.String(200), nullable=True, default=datetime.date.today)
    modified_by = db.Column(db.String(200), nullable=True)
    created_by = db.Column(db.String(200), nullable=True)
    quantity = db.Column(db.Integer, nullable=True)
    pa = db.Column(db.String(20), nullable=True)
    cost = db.Column(db.Integer, nullable=True)
    inactive = db.Column(db.Integer, nullable=True)
    almox_id = db.Column(db.Integer, ForeignKey('almox.id_almox'), nullable=True)

class Parts(db.Model):
    id_parts = db.Column(db.Integer, primary_key=True)
    part_number = db.Column(db.String(200), nullable=True)
    product = db.Column(db.String(200), nullable=True)
    vendor_id = db.Column(db.Integer, ForeignKey('vendors.id_vendors'), nullable=True)
    obsolescence_id = db.Column(db.Integer, ForeignKey('obsolescence.id_obs'), nullable=True)
    almox_id = db.Column(db.Integer, ForeignKey('almox.id_almox'), nullable=True)
    end_life = db.Column(db.Integer, nullable=True)
    created = db.Column(db.Date, nullable=True)
    last_modified = db.Column(db.Date, default=datetime.date.today)
    modified_by = db.Column(db.String(200), nullable=True)
    fotos = db.Column(db.String(200), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Almox(db.Model):
    id_almox = db.Column(db.Integer, primary_key=True)
    cd_item = db.Column(db.String(200), nullable=True)
    qtd = db.Column(db.Integer, nullable=True)
    active = db.Column(db.Boolean, nullable=True)
    description = db.Column(db.String(200), nullable=True)
    part_number = db.Column(db.String(200), nullable=True)

class Vendors(db.Model):
    id_vendors = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    region_id = db.Column(db.Integer, ForeignKey('regions.id_region'), nullable=True)
    area_novelis_id = db.Column(db.Integer, nullable=True)
    sgroups_id = db.Column(db.Integer, nullable=True)
    area_vendor_id = db.Column(db.Integer, nullable=True)
    site = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(100), nullable=True)
    support_after_sales = db.Column(db.Boolean, nullable=True)
    active = db.Column(db.Boolean, nullable=True)
    last_modified = db.Column(db.Date, default=datetime.date.today)
    modified_by = db.Column(db.String(200), primary_key=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
    
class Regions(db.Model):
    id_region = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(100), nullable=True)
    abbreviation = db.Column(db.String(10), nullable=True)

class Location(db.Model):
    id_location = db.Column(db.Integer, primary_key=True)
    description_category = db.Column(db.String(100), nullable=True)
    plant_id = db.Column(db.Integer, ForeignKey('plant.id_plant'), nullable=True)
    mu_id = db.Column(db.Integer, ForeignKey('manufactoring_unit.id_mu'), nullable=True)
    subarea_id = db.Column(db.Integer, ForeignKey('subarea.id_subarea'), nullable=True)
    class_loc = db.Column(db.String(100), nullable=True)
    code_subarea = db.Column(db.String(100), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
    
class Plant(db.Model):
    id_plant = db.Column(db.Integer, primary_key=True)
    plant = db.Column(db.String(100), nullable=True)

class Manufactoring_unit(db.Model):
    id_mu = db.Column(db.Integer, primary_key=True)
    mu = db.Column(db.String(100), nullable=True)

class Subarea(db.Model):
    id_subarea = db.Column(db.Integer, primary_key=True)
    subarea = db.Column(db.String(100), nullable=True)
    region_id = db.Column(db.Integer, ForeignKey('regions.id_region'), nullable=True)

class System_groups(db.Model):
    id_s_group = db.Column(db.Integer, primary_key=True)
    system_group = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(100), nullable=True)
    skillset_id = db.Column(db.Integer, nullable=True)

class Obsolescence(db.Model):
    id_obs = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(100), nullable=True)
    level = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String(100), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class System_complexity(db.Model):
    id_scomplexity = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String(100), nullable=True)

class Spare_availability(db.Model):
    id_spare_av = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(100), nullable=True)

class Spare_condition(db.Model):
    id_spare_cond = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(100), nullable=True)


