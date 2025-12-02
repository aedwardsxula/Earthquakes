# Earthquakes

## Final Release Checklist
- [x] README states purpose, contributors, and how to build, run, and test all the code from the CLI.  Build and run should not assume everyone is using a particular IDE (so don't assume users can click a Run button or use VSC's Command Prompt commands.
- [x] SDD has the project description, outline, architecture (including UML class diagrams), and all project user stories and use cases.
- [ ] Each team member must update our team's **Statement of Work** shared Excel spreadsheet.  Your grade on this assignment is based ONLY on the quality of your use cases, your GitHub contributions that result in accepted pull requests, and 10% of your grade will be assigned by your fellow team members.
- [ ] **Chloe** must finish her pushes to our repo by 8 PM on Dec 1st and then check this box.
- [x] **DeAnna** must finish her pushes to our repo by 8 PM on Dec 1st and then check this box.
- [x] **Emilio** must finish his pushes to our repo by 8 PM on Dec 1st and then check this box.
- [ v/] **Taylor** must finish her pushes to our repo by 8 PM on Dec 1st and then check this box.
- [x] **Emilio** must do one last check that the code builds, runs, and all the tests run by 10 PM on Dec 1st and then check this box.
- [x] **Emilio** must "Project Release" tag our repo.
- [ ] Everyone must complete the Brightspace survey to earn the final points for Assignment08.
- [ ] Everyone should complete the Class Climate survey to help Dr. Edwards improve her teaching.

Lead: epeguero  Emilio Peguero
Designer: cwhite29  
SWE: tmcdile  
Tester: dnichol5  DeAnna Nichols

Prioritized Project Ideas:
1. CPSC Register  
2. CPSC Core Curriculum Recommender  
3. CPSC Degree Works  
4. CPSC Study Buddies  
5. CPSC Electives  
6. CPSC Course Offerings

----------------------------------------------------------------
README:

Purpose/Goal of this project:
This project is a command-line university management system designed to simulate how students, professors, and administrators interact with an academic database. When the program runs, users log in with an ID that determines their role. Students can view their schedules, update their major, and check fiscal clearance. Professors can see their assigned classes, review enrolled students, and make updates to course information. Administrators have full control — they can create courses, assign professors, manage student accounts, and generate transcripts.

All information is stored in simple text files inside the Database/ folder, and everything is handled directly through the terminal. The entire system is launched from Driver.py, which reads the login ID and routes each user to the appropriate portal.


Contributers:
epeguero
dnichol5
tmcdile

How to Run:
1.Clone the repo
2.Open the cloned repo on vs code
3.Open the terminal
4.Run javac SignUp.java to create the class
5.In the terminal run the command that best fits your device:
      python Driver.py
      python3 Driver.py
      python -m Driver

How to test:
1. Test the Student Portal (900… IDs)

      Use any account beginning with 900

      Confirms:
      Loading student data from Student_files/load_student.py
      Viewing/changing major (student_driver.py)
      Viewing schedules and fiscal clearance
      Reading data from course files in Database/courses/

2. Test the Professor Portal (700… IDs)

      Use any account beginning with 700

      Confirms:
      Loading professor profiles via load_professor.py
      Viewing assigned courses in professor_driver.py
      Adding/dropping students
      Updating course files inside Database/courses/

3. Test the Admin Portal (800… IDs)

      Use any account beginning with 800

      Confirms:
      Admin loading through Admin_files/load_admin.py
      Creating new courses (Course.py)
      Assigning professors and managing students (admin_driver.py)
      Generating transcripts (writes to Database/Transcripts.csv)
      Updating CRN .txt files in Database/courses/

4. Test Data Files

You can edit or add test users directly in:

      Database/Accounts.txt
      Course behavior can be tested with the .txt files inside:
      Database/courses/


File Structure:
Earthquakes/                              ← project root (current folder)
│
├── Driver.py                    → Main entry point – shows Sign Up / Log In menu and routes users
├── Functions.py                 → Shared toolbox (clear_screen, auto-schedule, fiscal clearance, etc.)
├── SignUp.java & SignUp.class   → Old Java prototype (unused – safe to delete)
│
├───Admin_files/
│   ├── Admin.py                 → Admin class + create/view transcript functions
│   ├── admin_driver.py          → Complete Admin portal (create courses, assign professors, manage everything)
│   ├── Course.py                → Core Course class – generates random CRNs, saves courses as .txt files in Database/courses/
│   └── load_admin.py            → Loads an Admin object from Accounts.txt (800… IDs)
│
├───Student_files/
│   ├── Student.py               → Student class (name, major, fiscal clearance, schedule methods)
│   ├── student_driver.py        → Student portal – view info, change major, check clearance, view current & past schedules
│   └── load_student.py          → Loads a Student object from Accounts.txt (900… IDs)
│
├───Professor Files/
│   ├── Professor.py             → Professor class + assign_course() that updates course files
│   ├── professor_driver.py      → Professor portal – view classes, see/drop students, change time
│   └── load_professor.py        → Loads a Professor object from Accounts.txt (700… IDs)
│
├───Database/
│   ├── Accounts.txt             → Master list of all users (STUDENT, ADMIN, PROFESSOR lines)
│   ├── Transcripts.csv          → Generated transcripts (created by admins)
│   └── courses/                 → One .txt file per course containing CRN, time, professor ID, enrolled students
│       ├── ACC 201.txt
│       ├── ART 205.txt
│       ├── BIO 110.txt
│       └── … (20+ more course files)
└───────────────────────────────────────────────────────────────────────────────────────────────────────────

----------------------------------------------------------------
SDD:

Project Description:

Earthquakes is a command-line university management system that simulates how students, professors, and administrators interact with academic data.
Users log in with an ID (900 for students, 700 for professors, 800 for admins). Based on the user type, the program loads their profile, displays the appropriate portal, and allows them to perform actions such as viewing schedules, managing classes, creating courses, and generating transcripts.

All system data is stored as simple text files in the Database/ directory, and the entire application is launched from Driver.py.



Project Description:

Earthquakes is a command-line university management system that simulates how students, professors, and administrators interact with academic data.
Users log in with an ID (900 for students, 700 for professors, 800 for admins). Based on the user type, the program loads their profile, displays the appropriate portal, and allows them to perform actions such as viewing schedules, managing classes, creating courses, and generating transcripts.

All system data is stored as simple text files in the Database/ directory, and the entire application is launched from Driver.py.


System Outline:

The system is divided into three major portals, each with its own drivers, loaders, classes, and file operations:

Student Portal (900…)
View name, major, fiscal status
Change major
View schedule (current & past)
Load student data from Accounts.txt
Read/write course files from Database/courses/

Professor Portal (700…)
View assigned classes
View enrolled students
Drop students
Change class meeting times
Load professor data from Accounts.txt

Admin Portal (800…)
Create courses (auto-generate CRN)
Assign professors
Add/remove students
Generate transcripts (writes to Transcripts.csv)
Manage course files under Database/courses/
Shared Utilities


Functions.py for shared logic (clear screen, fiscal check, schedule utilities)
Driver.py for login validation & routing
Data stored in text files for simplicity

UML Class Diagram:
-------------------------------
Class: Student
-------------------------------
- id : int
- name : str
- major : str
- fiscal_cleared : bool
- schedule : list
-------------------------------
+ view_schedule()
+ change_major(new_major)
+ check_fiscal_clearance()
-------------------------------

-------------------------------
Class: Professor
-------------------------------
- id : int
- name : str
- assigned_courses : list
-------------------------------
+ view_courses()
+ drop_student(course, student_id)
+ change_meeting_time(course, new_time)
-------------------------------

-------------------------------
Class: Admin
-------------------------------
- id : int
- name : str
-------------------------------
+ create_course(name, time)
+ assign_professor(course, professor_id)
+ manage_student(course, student_id)
+ generate_transcript(student_id)
-------------------------------

-------------------------------
Class: Course
-------------------------------
- crn : int
- name : str
- time : str
- professor_id : int
- enrolled_students : list
-------------------------------
+ save_to_file()
+ add_student(student_id)
+ drop_student(student_id)
-------------------------------

User Case Stories are found in trello-board-export