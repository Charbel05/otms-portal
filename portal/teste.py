from sqlalchemy.orm import aliased
from portal import app, db
from portal.forms import FormLogin, FormPhoto
from portal.models import Almox, Location, Obsolescence, Parts, Regions, System_groups, User_otms, Rpn, Vendors
from flask_login import current_user, login_required, login_user, logout_user
import portal.queries as queries

vendor_alias = aliased(Vendors)
obsolescence_alias = aliased(Obsolescence)
parts = db.session.query(Parts, vendor_alias, obsolescence_alias).join(vendor_alias, Parts.vendor_id == vendor_alias.id_vendors).join(obsolescence_alias, Parts.obsolescence_id == obsolescence_alias.id_obs).all()


for part, vendor, obsolescence in parts:
    print(f"Part Number: {part.part_number}, Vendor: {vendor.name}, Obsolescence: {obsolescence.status}")