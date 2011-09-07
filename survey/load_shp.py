import os
from django.contrib.gis.utils import LayerMapping
from models import School, District, Street, Town, Employer

district_mapping = {
    'districtid': 'districtid',
    'distname': 'distname',
    'slug': 'slug',
    'startgrade': 'startgrade',
    'endgrade': 'endgrade',
    'distcode4': 'distcode4',
    'distcode8': 'distcode8',
    'geometry': 'MULTIPOLYGON',
}

districts_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'C:/gis/walkboston/districts.shp'))

def load_districts(verbose=True):
    lm = LayerMapping(District, districts_shp, district_mapping,
                      transform=False, encoding='iso-8859-1')

    lm.save(strict=True, verbose=verbose)


school_mapping = {
    'schid': 'schid',
    'name': 'name',
    'address': 'address',
    'slug': 'slug',
    'town_mail': 'town_mail',
    'town': 'town',
    'state': 'state',
    'zip': 'zip',
    'principal': 'principal',
    'phone': 'phone',
    'fax': 'fax',
    'grades': 'grades',
    'schl_type': 'schl_type',
    'districtid_tmp': 'districtid',
    'geometry' : 'POINT',
}

schools_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'C:/gis/walkboston/schools.shp'))

def load_schools(verbose=True):
    lm = LayerMapping(School, schools_shp, school_mapping,
                      transform=False, encoding='iso-8859-1')

    lm.save(strict=True, verbose=verbose)    


town_mapping = {
    'town_id': 'town_id',
    'name': 'name',
    'slug': 'slug',
    'geometry': 'MULTIPOLYGON',
}

towns_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'C:/gis/greenstreets/towns.shp'))
    
def load_towns(verbose=True):
    lm = LayerMapping(Town, towns_shp, town_mapping,
                      transform=False, encoding='iso-8859-1')

    lm.save(strict=True, verbose=verbose)  


employer_mapping = {
    'name': 'COMPANY_NA',
    'address': 'PRIMARY_AD',
    'infousa_id': 'INFOUSA_ID',
    'Muni_ID': 'Muni_ID',
    'geometry': 'POINT',
}

employers_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'C:/gis/greenstreets/employers.shp'))

def load_employers(verbose=True):
    lm = LayerMapping(Employer, employers_shp, employer_mapping,
                      transform=False, encoding='iso-8859-1')
    
    lm.save(strict=True, verbose=verbose)


street_mapping = {
    'name': 'ST_NAME',
    'tmp_districtid': 'districtid',
    'tmp_town': 'L_TOWN_ID',
    'geometry': 'MULTILINESTRING',
}

street_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'C:/gis/greenstreets/streets.shp'))

def load_streets(verbose=True):
    lm = LayerMapping(Street, street_shp, street_mapping,
                      transform=False, encoding='iso-8859-1')
    
    lm.save(strict=True, verbose=verbose)
        