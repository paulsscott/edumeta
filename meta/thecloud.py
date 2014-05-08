# -*- coding: utf-8 -*-

import requests
import sys
import json
import os
sys.path.append('.')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from apps.metadata.models import *

def get_metadata():
	l = []
	r = requests.get("https://api.thecloud.net/cloudapi/hotspots/all")
	locations = json.loads(r.content)
	for location in locations:
	        if location['address'].get('country') == "Sverige" and location['address'].get('addressLine3') == 'eduroam' and location.get('latitude') and location.get('longitude') and location.get('name'):
	                l.append(location)
	return l

def insert_locations(locations=None, institution=None):
	if locations and institution:
		for loc in locations:
			name = loc.get('name')
			lat = str(loc.get('latitude'))
			long = str(loc.get('longitude'))
			city = loc['address'].get('city', "NA")
			street = loc['address'].get('addressLine1', "NA")
			try:
				Location.objects.get(institution=institution, location_name_en=name, street=street)
				create = False
			except:
				create = True
			
			if create:
                		l = Location.objects.create(
                	        	institution = institution,
                	        	location_name_se = name,
                	        	location_name_en = name,
                	        	latitude = lat,
                	        	longitude = long,
                	        	street = street,
                	        	city = city,
                	        	ssid = 'eduroam',
                	        	enc_level = 'wpa2',
                	        	port_restrict = False,
                	        	transp_proxy = False,
                	        	ipv6 = False,
                	        	nat = True,
                	        	ap_no = 1,
                	        	wired = False,
                	        	info_url_se = 'http://www.eduroam.se/',
                	        	info_url_en = 'http://www.eduroam.se/'
                		)

if __name__ == "__main__":
	institution = Institution.objects.get(realm="thecloud.eu")
	locations = get_metadata()
	insert_locations(locations=locations, institution=institution)
