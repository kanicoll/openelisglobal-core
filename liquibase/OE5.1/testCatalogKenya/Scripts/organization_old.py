#!/usr/bin/env python
# -*- coding: utf-8 -*-

organization = []
region = []
region_dict = {}
used = ['']
county_list = []
organization_file = open('input_files/FacilityScripts.txt','r')
region_file = open('input_files/region.txt', 'r')

for line in organization_file:
    if len(line) > 1:
        organization.append(line.strip(" "))
organization_file.close()

for line in region_file:
    if len(line) > 1:
        region.append(line.strip(" "))
region_file.close()

for row in range(0, len(region)):
	#create dictionary for the county/region name and number
	county_list = region[row].split(",")
	region_dict[county_list[0].strip()] = county_list[1].strip()

	
def abbr_state(name):

    if name.strip() == 'Nairobi':
	return 'NB'
    elif name.strip() == 'Central':
        return 'CN'
    elif name.strip() == 'Nyanza':
        return 'NY'
    elif name.strip() == 'Western':
        return 'WE'
    elif name.strip() == 'Rift Valley':
        return 'RF'
    elif name.strip() == 'Coast':
        return 'CO'
    elif name.strip() == 'Eastern':
        return 'ES'
    elif name.strip() == 'North Eastern':
        return 'NE'
    return name
print region_dict
def get_org_id(county):
    county_name = county.strip()
    if len(county_name) > 3:
	#print region_dict[county_name]
	return region_dict[county_name]
    return 'NULL'

def get_org_type_id(org):
    for row in range(0, len(region)):
        region_name = region[row]
	region_field = region_name.split(",")
	if len(org) > 3 and region_field[0].strip() == org.strip():
	   return '8'
    return '7'

def esc_name(name):
    if "'" in name:
        return name.replace("'", "''")
    else:
        return name.strip()

sql_insert = "INSERT INTO clinlims.organization( id, name, city, zip_code, street_address, state, org_id, lastupdated,  is_active) \n\t VALUES ("
count = 10
organization_results = open("output_files/organization.sql", 'w')
for row in range(0, len(organization)):
        organization_name = organization[row]
	org_field = organization_name.split(",")
        if org_field not in used and 'n/a' not in org_field:
            used.append(org_field)
            organization_results.write(sql_insert)
            organization_results.write(org_field[0] + ", '" + esc_name(org_field[1]) + "', '" + esc_name(org_field[2]) + "', '" + org_field[3] + "' , '" + esc_name(org_field[4]) + "', '" + abbr_state(org_field[5]) + "'," + get_org_id(org_field[6]) +", now(), 'Y');\n\t")
	    organization_results.write("INSERT INTO clinlims.organization_organization_type( org_id, org_type_id) \n\t\t VALUES ( "+ org_field[0] +",'"+ get_org_type_id(org_field[1]) +"');\n")

print "Done Look for the results in organization.sql"
