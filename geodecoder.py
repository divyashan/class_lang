import pandas as pd 
import pdb

from geopy.geocoders import ArcGIS 

geolocator = ArcGIS()


# These two could be combined..
from geopy.geocoders import Nominatim 


def get_county_ArcGIS(row):
    geolocator = ArcGIS(timeout=1)
    latlng = "" + str(row['lat']) + ", " + str(row['lng']) + ""
    req = False
    
    if latlng in county_dict:
        return county_dict[latlng], req
    
    try:
        location = geolocator.reverse(latlng)
    except GeocoderServiceError as e: 
        county_dict[latlng] = None
        req = True
        print e
        print "Unable to find county for: ", latlng
        return 'NA', req
    except:
        time.sleep(5)
        try:
            location = geolocator.reverse(latlng)
        except GeocoderServiceError as e: 
            county_dict[latlng] = None
            req = True
            print e
            print "Unable to find county for: ", latlng
            return 'NA', req
        except:
            time.sleep(60)
            location = geolocator.reverse(latlng)
        
    if 'Subregion' in location.raw.keys():
        county_dict[latlng] = location.raw['Subregion']
        req = True
        print county_dict[latlng]        
        return county_dict[latlng], req
    print 'NA!!!'
    return 'NA', req

def get_county_ArcGIS_str(latlng):
    geolocator = ArcGIS(timeout=1)
    req = False
    
    if latlng in county_dict:
        return county_dict[latlng], req
    
    try:
        location = geolocator.reverse(latlng)
    except GeocoderServiceError as e: 
        county_dict[latlng] = None
        req = True
        print e
        print "Unable to find county for: ", latlng
        return 'NA', req
    except:
        time.sleep(5)
        try:
            location = geolocator.reverse(latlng)
        except GeocoderServiceError as e: 
            county_dict[latlng] = None
            req = True
            print e
            print "Unable to find county for: ", latlng
            return 'NA', req
        except:
            time.sleep(60)
            location = geolocator.reverse(latlng)
        
    if 'Subregion' in location.raw.keys():
        county_dict[latlng] = location.raw['Subregion']
        req = True
        print county_dict[latlng]        
        return county_dict[latlng], req
    print 'NA!!!'
    return 'NA', req
def get_state_ArcGIS(row):
    latlng = "" + str(row['lat']) + ", " + str(row['lng']) + ""

    location = geolocator.reverse(latlng)
    if 'Region' in location.raw:
        state_dict[latlng] = location['Region']
        return state_dict[latlng]
    return 'NA'

def get_county_nominatim(row):
    geolocator = Nominatim()
    latlng = "" + str(row['lat']) + ", " + str(row['lng']) + ""
    req = False
    
    if latlng in county_dict:
        return county_dict[latlng], req
    
    location = geolocator.reverse(latlng)
    if 'address' in location.raw.keys():
        if 'county' in location.raw['address'].keys():
            county_dict[latlng] = location.raw['address']['county']
            req = True
            print count_dict[latlng]
            return county_dict[latlng], req
    return 'NA'

def get_state(row):
    lat = float(row['lat'])
    lng = float(row['lng'])
    location = geolocator.reverse(lat, lng)
    if 'address' in location.raw:
        if 'county' in location.raw['address']:
            return location['address']['state']
    return 'NA'

def get_income_bracket(county_name, state_name):
    state_counties = county_income[county_income['state'] == state_name]


def get_latlngset(tweets_df):
	latlongs = []
	for i in range(len(tweets_df)):
	    row = tweets_df.iloc[i]
	    latlongs.append("" + str(row['lat']) + ", " + str(row['lng']) + "")

	latlongs_set = list(set(latlongs))
	return latlongs_set

def get_county(row):
    latlng = "" + str(row['lat']) + ", " + str(row['lng']) + ""
    return county_dict[latlng]


def populate_county_dict(latlongs_set):
	for i, latlng_opt in enumerate(latlongs_set):
	    if i % 100 == 0:
	        print i
	    if latlng_opt in county_dict:
	        continue
	    x, req = get_county_ArcGIS_str(latlng_opt)
	    if req:
	        time.sleep(1)

def populate_FIPS_dict(latlongs_set):
    FIPS_dict = dict()
    for i, latlong in enumerate(latlongs_set):
        if i % 100 == 0: 
            print i
        if latlong in FIPS_dict:
            continue
        a = latlong.split(',')
        FIPS_dict[latlong] = get_FIPS(a[0], a[1])
    pickle.dump(FIPS_dict, open("FIPS_dict.pickle", "wb"))
    return FIPS_dict
    

def produce_county_income_dataframe():
	ci_input = open('county_income.txt').readlines()
	n_counties = len(ci_input)/10
	ci_input_grouped = [ci_input[i*10:(i+1)*10] for i in range(n_counties)]
	entries = []
	for group in ci_input_grouped:
	    group = group[2:-1]
	    county = re.split('<|>', group[0])[-5]
	    state = re.split('<|>', group[1])[-3]
	    per_capita_income = re.split('<|>', group[2])[-3]
	    median_household_income =  re.split('<|>', group[3])[-3]
	    median_family_income = re.split('<|>', group[4])[-3]
	    population = re.split('<|>', group[5])[-3]
	    n_households = re.split('<|>', group[6])[-3]
	    
	    entry = {'county': county, 'state': state, 'per_capita': per_capita_income, 'median_household': median_household_income,
	     'median_family': median_family_income, 'population': population, 'n_households': n_households}
	    entries.append(entry)    

	df = pd.DataFrame(entries)
	df.to_csv('county_income.csv')


latlng = "47.528139,-122.197916"
pdb.set_trace()
get_county(latlng)