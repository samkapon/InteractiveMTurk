import time

def create_qualification(name, mturk):
    qual_response = mturk.create_qualification_type(Name=name,Keywords="",Description="DESCRIPTION", QualificationTypeStatus="Active", AutoGranted=False)
    print(qual_response['QualificationType']['QualificationTypeId']) 
    return qual_response['QualificationType']['QualificationTypeId']

def create_qualification_HIT(reward, time_for_hit, assignment_duration, max_assignments, retake_qual_id, new_qual_id, mturk, password):
    questions = open(file='question_answer/Test_directToMTurk.xml', mode='r').read() 
    answers = open(file='question_answer/AnswerKey_directToMTurk.xml', mode='r').read() 
    num_workers_with_current_qual = 0
    group_assignment = 0
    end_time = time.time()+time_for_hit*60+assignment_duration
    hit = mturk.create_hit(
            Reward=reward,
            LifetimeInSeconds=time_for_hit*60,
            AssignmentDurationInSeconds=assignment_duration,
            MaxAssignments = max_assignments,
            Title='Recruiting_Interactive_HIT',
            Question=questions,
            Description='Recruiting for Interactive HIT',
            Keywords='qualification, test',
            AutoApprovalDelayInSeconds=1,
            QualificationRequirements=[{'QualificationTypeId': retake_qual_id, 'Comparator': 'DoesNotExist', 'ActionsGuarded': "DiscoverPreviewAndAccept"},
                                       {'QualificationTypeId': new_qual_id, 'Comparator': 'DoesNotExist', 'ActionsGuarded': "DiscoverPreviewAndAccept"}]
            )
    hitid = hit['HIT']['HITId']
    counter = 0
    while (counter<time_for_hit*60 and time.time()<end_time):
        print('Total Recruited:', num_workers_with_current_qual)
        time.sleep(1)
        num_assignments = len(mturk.list_assignments_for_hit(HITId=hitid, MaxResults=100)['Assignments'])
        workers_with_qual = []
        num_workers_with_current_qual = len(mturk.list_workers_with_qualification_type(QualificationTypeId=new_qual_id,MaxResults=100)['Qualifications'])
        for j in range(0, num_workers_with_current_qual):
            workers_with_qual.append(mturk.list_workers_with_qualification_type(QualificationTypeId=new_qual_id,MaxResults=100)['Qualifications'][j]['WorkerId'])
        for j in range(0,num_assignments):
            cur_worker_id = mturk.list_assignments_for_hit(HITId=hitid, MaxResults=100)['Assignments'][j]['WorkerId']
            if (password in mturk.list_assignments_for_hit(HITId=hitid, MaxResults=100)['Assignments'][j]['Answer']) and (cur_worker_id not in workers_with_qual):
                group_assignment =  1
                mturk.associate_qualification_with_worker(QualificationTypeId=new_qual_id, WorkerId=cur_worker_id, IntegerValue=group_assignment, SendNotification=True)
        counter = counter+1

def notify_workers_with_qualification(message, qual_id, mturk):
    workers_with_qual = mturk.list_workers_with_qualification_type(QualificationTypeId=qual_id,MaxResults=100)['Qualifications']
    num_workers = len(workers_with_qual)
    worker_ids = []
    for j in range(0,num_workers): 
        worker_ids.append(workers_with_qual[j]['WorkerId'])
    mturk.notify_workers(Subject=message['subject'], MessageText=message['body'], WorkerIds=worker_ids)

def initiate_mturk_session(qual_id, num_participants, csess, retake_qual_id, session_name, title, template):
    mturk_hit_settings_out1 = {
        'keywords': ['bonus', 'choice', 'study'],
        'title': title,
        'description': 'N',
        'frame_height': 500,
        'template': template,
        'minutes_allotted_per_assignment': 60,
        'expiration_hours': 2, 
        'grant_qualification_id': retake_qual_id,
        'qualification_requirements': [
            {
                'QualificationTypeId': retake_qual_id,
                'Comparator': "DoesNotExist",
                'ActionsGuarded': "DiscoverPreviewAndAccept"
            },
            {
                'QualificationTypeId': qual_id,
                'Comparator': "EqualTo",
                'IntegerValues': [1],
                'ActionsGuarded': "DiscoverPreviewAndAccept"
            },
        ]
    }
    resp = csess(session_config_name=session_name, num_participants=num_participants, is_mturk=True, modified_session_config_fields = dict(mturk_hit_settings=mturk_hit_settings_out1))
    print(resp.text) # returns the session code
