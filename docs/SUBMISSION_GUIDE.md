# Submission guide: step by step, no technical knowledge needed

This guide gets the project from your computer to all four submission areas. Set aside about an hour for the first time. You don't need to write any code.

You will need: a web browser (Chrome or Edge works best), an email address, and the project folder `RateSimulator_Capstone` on your computer.

## Part A. Put the project on GitHub (one-off, about 20 minutes)

GitHub is a free website that stores project folders. The final submission asks for a link to your project there.

**A1. Make an account**
1. Go to https://github.com and click **Sign up**.
2. Enter your email, choose a password and a username, then follow the prompts. GitHub emails you a code; type it in.
3. Write your username down. It will be part of your project link.

**A2. Make an empty project (called a repository)**
1. Once signed in, click the **+** at the top right and choose **New repository**.
2. Repository name: `rate-card-price-prediction`
3. Description: `Capstone project: predicting courier rate-card prices`
4. Choose **Public**. (Reviewers must be able to open it without logging in.)
5. Leave every tick-box unticked. Click **Create repository**.

**A3. Upload the files**
1. On the new page, click the link **uploading an existing file**.
2. Open the `RateSimulator_Capstone` folder on your computer. Select everything inside it (press Ctrl+A on Windows, Cmd+A on a Mac) and **drag it into the GitHub page**. Drag the contents, not the outer folder, so that `README.md` ends up at the top level.
3. Wait until every file has finished uploading. You should see the folders `notebooks`, `data`, `src`, `models`, `reports`, `test_data`, `tests` and `docs`.
4. At the bottom, type `Add capstone project` in the box and click **Commit changes**.

If the browser says there are too many files, upload the folders one at a time: drag `notebooks` first, commit, then do the next one. Do the single files (`README.md`, `requirements.txt`, `.gitignore`) last.

**A4. Check it worked**
1. Click the repository name at the top to return to its home page.
2. You should see the README text displayed below the file list, starting with "Can a rate card's structure predict its price?".
3. Click `notebooks`, then `01_data_cleaning.ipynb`. It should open as a readable page with tables and charts.
4. Copy the address from your browser's address bar. It looks like `https://github.com/yourname/rate-card-price-prediction`. This is **your project link**. Paste it into a note.
5. Open a private window (Ctrl+Shift+N in Chrome) and paste the link. If you can see the project without logging in, you're done with Part A.

## Part B. Submit the four stages

The brief names four areas. Each one must be done separately, and finishing one does not finish the others. Open each by clicking its link in the Capstone Project Request document.

Ready-made text and Word versions of every stage write-up are in `docs/submissions/`.

| Stage | Where to submit | Points | What to give them |
|---|---|---|---|
| 1 | Capstone 11.1 submission area | 15 | The file `stage1_problem_statement_11.1.docx` (or paste its text) |
| 2 | Capstone 16.1 discussion area | 10 | Paste the text of `stage2_refined_problem_statement_16.1.docx` as a post |
| 3 | Capstone 20.1 submission area | 25 | `stage3_initial_report_20.1.docx`, plus your repository link and the two notebooks `01_data_cleaning.ipynb` and `02_exploratory_analysis.ipynb` if the area allows attachments |
| 4 | Capstone Project 24.1 submission area | 50 | **Only your GitHub repository link** from step A4 |

**For each stage**
1. Open the stage link from the brief and read the instructions on that page first.
2. Upload the file or paste the text from the table above.
3. Press the submit or post button.
4. Take a screenshot of the confirmation message for your records.

## Part C. Final check before and after Stage 4

Tick each box.

- [ ] The repository is **Public** (open it in a private window to test).
- [ ] `README.md` shows on the repository home page.
- [ ] The four notebook links in the README open.
- [ ] You submitted Stage 1, Stage 2, Stage 3 and Stage 4. Look at the status of all four; one does not complete the others.
- [ ] You pasted the repository link, not a link to a single file.

## If something goes wrong

| Problem | What to do |
|---|---|
| "Page not found" when opening your link in a private window | The repository is private. Open it, go to **Settings**, scroll to the bottom, click **Change visibility** and choose **Public**. |
| README doesn't appear | The files went into an extra outer folder. Delete the repository (Settings, bottom of the page) and upload again, dragging the *contents* of `RateSimulator_Capstone`. |
| A notebook shows "Unable to render" | Wait a minute and refresh. GitHub is occasionally slow with large notebooks. |
| The submission area rejects `.md` files | Use the `.docx` versions in `docs/submissions/`. |

## A note on the data

All prices and customers in this project are simulated. No real contract is included, so it is safe to make the repository Public. The README says so near the top, and a reviewer reading it will see that.
