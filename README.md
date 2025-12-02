# Earthquakes

## Final Release Checklist
- [x] README states purpose, contributors, and how to build, run, and test all the code from the CLI.  Build and run should not assume everyone is using a particular IDE (so don't assume users can click a Run button or use VSC's Command Prompt commands.
- [ ] SDD has the project description, outline, architecture (including UML class diagrams), and all project user stories and use cases.
- [ ] Each team member must update our team's **Statement of Work** shared Excel spreadsheet.  Your grade on this assignment is based ONLY on the quality of your use cases, your GitHub contributions that result in accepted pull requests, and 10% of your grade will be assigned by your fellow team members.
- [ ] **Chloe** must finish her pushes to our repo by 8 PM on Dec 1st and then check this box.
- [x] **DeAnna** must finish her pushes to our repo by 8 PM on Dec 1st and then check this box.
- [ ] **Emilio** must finish his pushes to our repo by 8 PM on Dec 1st and then check this box.
- [ v/] **Taylor** must finish her pushes to our repo by 8 PM on Dec 1st and then check this box.
- [ ] **Emilio** must do one last check that the code builds, runs, and all the tests run by 10 PM on Dec 1st and then check this box.
- [ ] **Emilio** must "Project Release" tag our repo.
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

Purpose of this project:
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