import boto3
import time
from helper_functions import *
import requests
SERVER_URL = 'YOUR_APP_URL'
REST_KEY = 'YOUR_REST_KEY'
mturk_retake_id = 'YOUR_RETAKE_ID'

mturk = boto3.client('mturk',region_name = 'us-east-1') 
def csess(**payload):
    return requests.post(SERVER_URL + '/api/v1/sessions/', json=payload,
        headers={'otree-rest-key': REST_KEY}
    )
    
# For Sandbox instead
# mturk = boto3.client('mturk',region_name = 'us-east-1',endpoint_url='https://mturk-requester-sandbox.us-east-1.amazonaws.com') 

new_qual_id = create_qualification(name='RECRUIT_QUAL_NAME', mturk=mturk)
create_qualification_HIT(reward='0.01', 
                         time_for_hit=2, 
                         assignment_duration=30, 
                         max_assignments=1, 
                         retake_qual_id=mturk_retake_id, 
                         new_qual_id=new_qual_id, 
                         mturk=mturk,
                         password="ANSWER_TO_FREE_TEXT_QUESTION")
notify_workers_with_qualification({'subject':'SUBJECT', 'body':'BODY TEXT'}, 
                                   qual_id=new_qual_id, 
                                   mturk=mturk)
initiate_mturk_session(qual_id=new_qual_id, 
                       num_participants=40, 
                       retake_qual_id=mturk_retake_id,
                       csess=csess,
                       session_name='YOUR_TREATMENT',
                       title='YOUR_TITLE',
                       template='global/mturk_template.html')
