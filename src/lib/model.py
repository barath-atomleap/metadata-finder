from schematics.models import Model
from schematics.types import StringType, ModelType, GeoPointType, ListType, IntType, DateType


class Headquarters(Model):
  city = StringType()
  country = StringType()
  address = StringType()
  zip_code = StringType()
  geo = GeoPointType()


class Company(Model):
  name = StringType(required=True)
  full_name = StringType(required=True)
  domain = StringType(required=True)
  founded = DateType()
  headquarters = ModelType(Headquarters)
  long_description = StringType(required=True)
  short_description = StringType(required=True)
  technology_labels = ListType(StringType())
  industry_labels = ListType(StringType())
  num_employees = IntType()
