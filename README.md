# Earthquakes

## Final Release Checklist
- [ ] README states purpose, contributors, and how to build, run, and test all the code from the CLI.  Build and run should not assume everyone is using a particular IDE (so don't assume users can click a Run button or use VSC's Command Prompt commands.
- [ ] SDD has the project description, outline, architecture (including UML class diagrams), and all project user stories and use cases.
- [ ] Each team member must update our team's **Statement of Work** shared Excel spreadsheet.  Your grade on this assignment is based ONLY on the quality of your use cases, your GitHub contributions that result in accepted pull requests, and 10% of your grade will be assigned by your fellow team members.
- [ ] **Chloe** must finish her pushes to our repo by 8 PM on Dec 1st and then check this box.
- [x] **DeAnna** must finish her pushes to our repo by 8 PM on Dec 1st and then check this box.
- [ ] **Emilio** must finish his pushes to our repo by 8 PM on Dec 1st and then check this box.
- [ ] **Taylor** must finish her pushes to our repo by 8 PM on Dec 1st and then check this box.
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
Data Base Structure:

Database/
│
├── Accounts.txt               (stores all user accounts)
├── Courses.csv                (shows how course files should be formatted)
├── Security_Pins.txt          (pins needed for professor/admin signup)
├── University_Database.csv    (list of all IDs and what type they are)
│
└── courses/                   (folder that holds every course file)
      ├── Comp Sci.txt         (info about one course)
      ├── Math 101.txt         (info about one course)
      └── ...                  (more courses)
