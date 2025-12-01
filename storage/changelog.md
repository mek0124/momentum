Task Manager - Storage Library Change Log

v0.1.0
  - created modular file structure for possible growth
  - created offline storage controller for sqlite3 relational database
  - created functions:
    - get many
    - get one by id
    - create one
    - update one
    - delete one

v0.2.0
  - reconstructed controller.py to automatically handle online/offline status
    - get_storage_controller
      - params: online: bool = False
      - obtains corresponding controller based off online usage status for cloud storage
      - written to attempt online storage connection 5 times before defaulting to relational storage
    - get_offline_storage_controller
      - check if controller can find the database file or create it if not exists
    - get_online_storage_controller
      - check if controller can connecto the online database
      - fail 5 times, default to relational database
    
    - wrapper functions:
      - get_all_tasks
      - list_task_by_id
      - create_task
      - update_task
      - delete_task
      - wrapper functions have the same names as each controllers functions. This helps in following the code as each controller reflects the other between types of databases being used.

v0.4.0
  - reconstructed controller.py and controllers/offline.py to be 'local storage first' in storage. 
  - if online connection fails, default storage is relational
  - fixed return types

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
v0.6.0 (possible version)
  - add onto storage
    - preload functions to load data into relational database on app load for smoother usage by the user
    - all user's data: settings, tasks, etc, will be loaded into a temporary relational database and deleted on app exit or user logout (negate cacheing)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~