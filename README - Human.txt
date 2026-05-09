Introduction
Hello human, I am also a human. I made this document to create an AI Coding “seed”. The idea is that you give this file to an AI and it has everything that it needs to program at an expert level via Scott Fackler’s method. 


An initial note: I believe that anyone can code. No, you do not need to know how the “syntax” works or what all the fancy functions are. Today, you can mostly just talk to your AI and it will do all the hard work for you. Don’t be afraid to try, and I believe you will succeed. The hardest part is setting everything up, but when that is done you will be amazed at how easily and quickly you can turn an idea into a fully functioning prototype right on your own computer!


My general philosophy on coding with AI is as follows:


* Tell your AI exactly what you want it to be and how you want it to act
   * Have strict procedures that my AI goes through when it approaches coding tasks
   * Make it be your advanced professional engineering team with all the modern best practices, let it explicitly know that
   * Tell it to not embellish statements. It should remain humble, it should question your judgement, and it should cross-check all critical claims
* Tell your AI who you are - you will have to explain LESS in the future to get what you actually want
* You are the producer of the code, the artist with the image in their head. Your job is to make the AI bring that idea to life.
   * Before you ever write any code, talk to your AI out loud…a lot
   * Tell it about the device your code will be used on, who it will be used by, the color palette you would like, the location of different menus or tabs, whether there will be touchscreen interaction, are there files, such as pictures or spreadsheets, that need to be saved, do settings need to persist between logins, are there noises, login credentials, external devices, network conditions that need to be taken into account
   * Don’t say too much at once, let it digest and internally formalize what you are saying
   * When you think you’re done, take a quick break then go again with more ideas
* Transition your conversation into a formal system of code production
   * Translate conversation into set of requirements
   * Work on producing code that meets those requirements
   * Use a ton of tools to assist with that
      * Extensive document control
         * Every document gets a version number, revision number, date of revision, what revisions were made, etc.
      * Machine-referencable requirements and completion documents
      * Have the AI self-audit
      * Keep a debt registry
* There should always be a “specific and detailed plan” before the AI goes to code:
   * Define the objective in one clear sentence.
   * Identify the target environment, constraints, and assumptions.
   * Restate what success looks like.
   * Break the work into phases.
   * For each phase, define: Purpose; concrete tasks; expected output; acceptance gate.
   * Separate quick prototype work from formal package/project work.
   * Identify required files, folders, modules, tools, and dependencies.
   * Define the data flow, control flow, or user workflow.
   * Define safety, shutdown, persistence, and recovery behavior if hardware/data is involved.
   * Define diagnostics and smoke tests early.
   * Define risks and mitigations.
   * Define likely failure modes and fallback paths.
   * Define what should not be changed or removed.
   * Define the minimum viable first pass.
   * Define the later professionalized version.
   * Define documentation that must ship with the work.
   * Define acceptance tests / definition of done.
   * End with the immediate next action.
* The AI should follow a procedure when coding:
   * Unzip and record package identity.
   * Confirm zip/internal folder naming.
   * Read README_START_HERE.
   * Read CHANGELOG.
   * Read FEATURE_INVENTORY.
   * Read ACCEPTANCE_TEST_PLAN.
   * Run structure audit.
   * Run smoke tests.
   * Inspect actual changed/current files.
   * Define task scope.
   * Update WORKPLAN_CURRENT_RUN.
   * Make smallest safe change.
   * Update docs/registers.
   * Run tests again.
   * Generate reports.
   * Repackage with matching folder/zip name.
   * Provide final package report.
* Iterate in measured chunks, but don’t bite off more than you can chew
   * AI likes to build momentum within a context-window
   * Context-windows can only grow so large before they become unstable
   * After iterating a zipped package about 5 times, you want to wrap that conversation up with a documentation update and next steps
   * Pass that package on to the next conversation along with what your AI recommends as next steps
   * You should be able to pass this package to any AI and, as long as that AI follows the instructions, they should be able to work on or review it
   * I believe it is very beneficial to have another AI review the package and send their criticism to your AI for review
* At some point, I imagine, the code is complete enough (or you are tired enough) to use w=for whatever application you had in mind




I think at the end of the day it comes down to defining how you want projects to be executed. I have found that the methods in this documents have worked well for my purposes. I hope they work for you as well.


### INSTRUCTIONS
So, with that out of the way, here are the instructions:
Setup


1. Verify that the cd or flash drive you received contains the following files:
   1. README - Human.txt / README - Human.pdf
      1. You’re reading it
   2. 20260502_01_AISOP_SEED.zip
      1. This is the custom instruction set for you and your AI, embedded in a formalized file and document structure that it teaches you to create
   3. Wm2703.zip
      1. Writemonkey is a Windows zenware* writing application with an extremely stripped down user interface, leaving you alone with your thoughts and your words. 
   4. Python-3.13.5-amd64.exe
      1. This is that program that runs the code
2. Install Python by double clicking on the .exe
   1. Make sure to Add Python to Environment Variables…if you want
3. Install Visual Studio Code (if this is on a flash drive it may be present) from the internet: https://code.visualstudio.com/
   1.      4. If you can’t get VSCode, WriteMonkey is included and needs no installation
   1. It is difficult to use, expect to have to consult the internet muchly
   2. No installation necessary
   3. Double click on WriteMonkey.exe 
   1.         4. Right-Click on the blank screen and select Jumps…
      1.    
         5. At the bottom of the pop-up, select Open in folders
         1.    
            6. Choose your folder and navigate to read the docs
            1.                  7. Right click and Quit to escape
               1.    
                  5. I strongly encourage you to read through all of the documents and familiarize yourself with the folder structure


Training your AI
                  1. Upload 20260502_01_AISOP_SEED.zip to your AI
                  2. Ask it for a comprehensive review
                  3. Cross-check it’s review with your own
                  4. Begin a project - it should be able to run the show from here














Scott Fackler
Ithaca, New York