# Dan The Deployment Machine
A django app to run mass deployment tests for cloud providers

Alpha: 
  * Celery to maintain and control the jobs
  * Supports Apache CloudStack
    * Configurable deployments options
      * Start time
      * End time (or deployment count)
      * Single or multizone deployment
      * Ignore any errors when running queryasyncjob (upto 3 times?)