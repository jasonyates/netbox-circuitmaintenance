from django_rq import job

@job("default")
def test_my_job(job_result):

    job_result.start()
    
    print("success")

    job_result.set_status(status='completed')
