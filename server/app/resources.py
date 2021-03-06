from flask_restful import Resource, reqparse
from app import api
from .models import User, Report, Symptom, Building, School
from app import db
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from datetime import datetime, timedelta, date
from . import notifier
from random import choice

''' 
START OF SECTION FOR CONSOLODATING POST REQUEST ARGUMENT PARSERS
'''

# parse for numbers
number_parser = reqparse.RequestParser()
number_parser.add_argument('email', help = 'This field cannot be blank', required = True)

# parser for getting homepage data
home_data_parser = reqparse.RequestParser()
home_data_parser.add_argument('email', help = 'This field cannot be blank', required = True)

# parser for adding a new report
report_parser = reqparse.RequestParser()
report_parser.add_argument('severity', help = 'This field cannot be blank', required = True, type=int)
report_parser.add_argument('symptoms', help = 'This field cannot be blank', required = True)
report_parser.add_argument('email', help = 'This field cannot be blank', required = True)
report_parser.add_argument('date', help = 'This field cannot be blank', required = True, type=int)

# parser for authenticating
auth_parser = reqparse.RequestParser()
auth_parser.add_argument('email', help = 'This field cannot be blank', required = True)
auth_parser.add_argument('password', help = 'This field cannot be blank', required = True)

# parser for registration
registration_parser = reqparse.RequestParser()
registration_parser.add_argument('name', help = 'This field cannot be blank', required = True)
registration_parser.add_argument('email', help = 'This field cannot be blank', required = True)
registration_parser.add_argument('password', help = 'This field cannot be blank', required = True)

# parser for adding building
building_parser = reqparse.RequestParser()
building_parser.add_argument('name', help = 'This field cannot be blank', required = True)
building_parser.add_argument('school', help = 'This field cannot be blank', required = True)

# parser for adding school
school_parser = reqparse.RequestParser()
school_parser.add_argument('name', help = 'This field cannot be blank', required = True)

# parser for adding symptom
symptom_parser = reqparse.RequestParser()
symptom_parser.add_argument('name', help = 'This field cannot be blank', required = True)

# parser for adding 
additional_info_parser = reqparse.RequestParser()
additional_info_parser.add_argument('email', help = 'This field cannot be blank', required = True)
additional_info_parser.add_argument('school', help = 'This field cannot be blank', required = True)
additional_info_parser.add_argument('buildings', help = 'This field cannot be blank', required = True)

'''
END OF ARG PARSER SECTION
'''

# numbers for charts

class ChartNumbers(Resource):
    def get(self):
        data = number_parser.parse_args()
        user = User.query.filter_by(email = data['email']).first()
        user_numbers = len(user.reports)
        total_numbers = Report.query.count()
        return {"user_numbers": user_numbers, "total_numbers":total_numbers}


# adding new schools/buildings (and symptoms if necessary?)

class AddSchool(Resource):
    def post(self):
        data = school_parser.parse_args()
        new_school = School(name=data['name'])
        try:
            db.session.add(new_school)
            db.session.commit()
            return {
                'message': '{} school created successfully.'.format(new_school.name),
                'status': True
            }
        except:
            return {
                'message':'Error occurred during creation of school.',
                'status': False
            }

class AddBuilding(Resource):
    def post(self):
        data = building_parser.parse_args()
        school_id = School.query.filter_by(name=data['school']).first().id

        if not school_id:
            return {
                'message': 'School not found in database.',
                'status': False
            }
        
        new_building = Building(name=data['name'], school_id=school_id)
        try:
            db.session.add(new_building)
            db.session.commit()
            return {
                'message': '{} building created successfully.'.format(new_building.name),
                'status': True
            }
        except:
            return {
                'message':'Error occurred during creation of building.',
                'status': False
            }

class AddSymptom(Resource):
    def post(self):
        data = symptom_parser.parse_args()
        new_symptom = Symptom(name=data['name'])
        try:
            db.session.add(new_symptom)
            db.session.commit()
            return {
                'message': 'Successfully added symptom {} to database.'.format(new_symptom.name),
                'status': True
            }
        except:
            return {
                'message': 'Failed to add symptom to database.',
                'status': False
            }


# post endpoint for submiting a new report
class SubmitReport(Resource):
    def post(self):
        data = report_parser.parse_args()
        # grabbing all raw data from request
        severity = data['severity']
        date = data['date'] # expected format for date: int
        email = data['email']
        symptoms = data['symptoms']
        symptoms = symptoms.split(',')
        # converting raw data into variables to instantiate Report
        user = User.query.filter_by(email=email).first()
        if not user:
            return {
                'message': 'Requested user for report not found in database.',
                'status': False
            }
        user_id = user.id
        school = user.school
        if not school:
            return {
                'message': 'Requested school for report not found in database.',
                'status': False
            }
        school = school.id
        date = datetime.today() - timedelta(days=date)
        # instantiate report from variables
        new_report = Report(severity=severity, user_id=user_id, school_id=school, date=date)

        # adding linked symptoms and buildings through for loop
        new_report.symptoms = []
        new_report.buildings = []
        print(symptoms)
        for symptom in symptoms:
            s = Symptom.query.filter_by(name=symptom).first()
            if s:
                new_report.symptoms.append(s)
            else:
                print(symptom)
        for building in user.buildings:
            new_report.buildings.append(Building.query.filter_by(name=building.name).first())
        notifier.notify("Try to avoid " + choice(user.buildings).name + "! There seems to be a lot of germs there...")
        try:
            db.session.add(new_report)
            db.session.commit()
            return {
                'message': 'Successfully created report for user {}'.format(new_report.user.email),
                'status': True
            }
        except:
            return {
                'message': 'Failed to create new report.',
                'status': False
            }

        
# get endpoints to get data for different pages       
class HotspotSymptomsData(Resource):
    def post(self):
        data = home_data_parser.parse_args()
        user = User.query.filter_by(email=data['email']).first()
        if not user:
            return {
                'message': 'Failed to get data for incorrect user.',
                'status': False
            }
        school = user.school.name
        symptoms = {}
        buildings = {}
        for report in Report.query.filter_by(school_id = user.school_id).all():
            for symptom in report.symptoms:
                if symptom.name in symptoms:
                    symptoms[symptom.name] += 1
                else:
                    symptoms[symptom.name] = 1
            for building in report.buildings:
                if building.name in buildings:
                    buildings[building.name] += 1
                else:
                    buildings[building.name] = 1

        symptom_counts = {symptom.name:len(symptom.reports) for symptom in Symptom.query.all()}
        sorted_symptoms = dict(sorted(symptom_counts.items(), reverse = True, key=lambda kv: kv[1]))

        building_counts = {building.name:len(building.reports) for building in Building.query.all()}
        sorted_buildings = dict(sorted(building_counts.items(), reverse=True, key=lambda kv: kv[1]))
        user_buildings = {}
        for key, value in sorted_buildings.items():
            if Building.query.filter_by(name=key).first():
                if Building.query.filter_by(name=key).first().school_id == user.school_id:
                    user_buildings[key] = value

        return {
            'school': school,
            'symptoms': sorted_symptoms,
            'buildings': user_buildings
        }

class TimeChartData(Resource):
    def get(self):
        day_reports = {}
        for symptom in Symptom.query.all():
            day_reports[symptom] = [0 for i in range(0,7)]
            for report in symptom.reports:
                print(report.date == date.today() - timedelta(days = 6))
                if report.date == date.today() - timedelta(days = 6):
                    day_reports[symptom][0] += 1
                elif report.date == date.today() - timedelta(days = 5):
                    day_reports[symptom][1] += 1
                elif report.date == date.today() - timedelta(days = 4):
                    day_reports[symptom][2] += 1
                elif report.date == date.today() - timedelta(days = 3):
                    day_reports[symptom][3] += 1
                elif report.date == date.today() - timedelta(days = 2):
                    day_reports[symptom][4] += 1
                elif report.date == date.today() - timedelta(days = 1):
                    day_reports[symptom][5] += 1
                elif report.date == date.today():
                    day_reports[symptom][6] += 1
        return_list = []
        for key, value in day_reports.items():
            return_list.append({'name':key.name, 'values':value})
        print(return_list)
        return return_list

class UserChartsData(Resource):
    def get(self):
        return "test"



'''
START OF SECTION FOR USER AUTHENTICATION LOGIC
'''
class UserAdditionalInformation(Resource):
    def get(self):
        return_dict = {}
        schools = School.query.all()
        for s in schools:
            return_dict[s.name] = [b.name for b in s.buildings]
        return return_dict
    
    def post(self):
        data = additional_info_parser.parse_args()
        user = User.find_by_email(data['email'])
        if not user:
            return {
                'message': "Failed to change user's data.",
                'status': False
            }
        school = School.query.filter_by(name = data['school']).first()
        if not school:
            return {
                'message': "Failed to find chosen school.",
                'status': False
            }
        user.school_id = school.id
        try:
            buildings = data['buildings'].split(',')
            for b in buildings:
                user.buildings.append(Building.query.filter_by(name=b).first())
            db.session.add(user)
            db.session.commit()
            return {
                'message': "Successfully updated student settings.",
                'status': True
            }
        except:
            return {
                'message': "Failed to update user settings",
                'status': False
            }
class UserRegistration(Resource):
    def post(self):
        data = registration_parser.parse_args()
        new_user = User(name = data['name'], email = data['email'], password = User.generate_hash(data['password']))

        if User.find_by_email(data['email']):
            return {
                'message': 'User {} already exists'. format(data['email']),
                'status': False
            }
        try:
            new_user.save_to_db()
            access_token = create_access_token(identity = data['email'])
            refresh_token = create_refresh_token(identity = data['email'])
            return {
                'message': 'User has been registered: {}'.format(new_user.email),
                'access_token': access_token,
                'refresh_token': refresh_token,
                'status': True
            }
        except:
            return {
                'message': 'Error while attempting to register user.',
                'status': False
            }, 500


class UserLogin(Resource):
    def post(self):
        data = auth_parser.parse_args()
        current_user = User.find_by_email(data['email'])

        if not current_user:
            return {
                'message': 'User {} doesn\'t exist'.format(data['email']),
                'status': False
            }
        
        if User.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity = data['email'])
            refresh_token = create_refresh_token(identity = data['email'])
            return {
                'message': 'Logged in as {}'.format(current_user.email),
                'access_token': access_token,
                'refresh_token': refresh_token,
                'status': True
            }
        else:
            return {
                'message': 'Wrong credentials',
                'status': False
            }
      
      
class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {
                'message': 'Access token has been revoked',
                'status': True
            }
        except:
            return {
                'message': 'Something went wrong',
                'status': False
            }, 500
      
      
class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {
                'message': 'Refresh token has been revoked',
                'status': True
            }
        except:
            return {
                'message': 'Something went wrong',
                'status': False
            }, 500
      
      
class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {
            'access_token': access_token,
            'status': True
        }
      
