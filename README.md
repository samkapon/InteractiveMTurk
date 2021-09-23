# InteractiveMTurk

Simple code to

1) recruit participants and notify MTurk workers using boto3
2) create HIT with qualification requirements using oTree REST API

After downloading folder, go to master.py

1) set SERVER_URL and REST_KEY (on this, see https://otree.readthedocs.io/en/latest/misc/rest_api.html)
2) set mturk_retake_id

The recruitment HITs that will be published have a free text reponse box which can be edited in question_answer/Test_directToMTurk.xml.  In master.py, editing the password entry in the create_qualification_HIT call will change the correct answer to the recruitment question.  Future versions will implement alternatives to free text response.

Code tested on otree 2.6.
