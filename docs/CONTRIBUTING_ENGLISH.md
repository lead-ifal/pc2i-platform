# How to contribute to the project
> Follow the steps below to contribute code or suggestions for improvements/corrections to the PC2I project platform

## Prerequisites
> Install the tools below

- [Git](https://git-scm.com/downloads) - code versioning;
- [Python](https://python.org/downloads) - platform development;
- Code editor (e.g. [Visual Studio Code](https://code.visualstudio.com/Download));

---

## Run the platform
Go to the [installation guide](./README.md#compass-guia-de-installação) and follow the step by step to have the platform running on your machine.

---

## Create a _branch_
The `branch-name` must clearly and objectively describe the changes you will make

```bash
git checkout -b branchname

# Examples:
# git checkout -b user-listing-route
# git checkout -b correct-registration-zones
# git checkout -b authentication-users
```

---

## Change the code
Now you can modify existing files in the project or even create new files and folders, if necessary.

:warning: Be careful to only change what was proposed in the _branch_. Do not make major changes, as the greater the number of changes, the more difficult it will be to review your code.

### New dependencies
If you have installed a new library, run the command below to register it in the `requirements.txt` file:

```bash
pip freeze > requirements.txt
```

---

## Record changes
### 1. Add changes to Git:

```bash
git add .
```

- If you want to add a specific file, replace `.` with the file address. Example:

```bash
git add app/__init__.py
```

### 2. Record changes

```bash
git commit -m "Message"
```

- Instead of `Message`, describe the changes you made clearly and objectively. Example:

```bash
git commit -m "Add user listing route"
```

---

## Submit for analysis
```bash
git push -u origin branch-name
```

The `branch-name` must be the same as that entered when [creating the _branch_](#create-a-branch).

---

## Open a _Pull Request_ (PR)
### 1. Click on "**Pull Requests**"

![image](https://user-images.githubusercontent.com/63798776/188283632-c4941df5-ca48-4964-8faa-98213f36fbf3.png)

### 2. Click "**New pull request**"

![image](https://user-images.githubusercontent.com/63798776/188283687-05181d74-87da-4f32-80a0-75d1a4a5ee4c.png)

### 3. Choose the _branches_
Make sure the _branches_ comparison looks like this:

![image](https://user-images.githubusercontent.com/63798776/188282775-345e460a-fb70-4887-a8c1-6d9e5011ec63.png)

- Where `your-branch` is the name you defined in [creating the _branch_](#create-a-branch).

### 4. Open the PR
Click "**Create pull request**", describe what you did, add a reviewer and wait for reviews

---

## Make corrections
If someone asks for corrections to your _pull request_, follow this step by step:

### 1. Check if the active _branch_ is the same as the PR
```bash
git branch

# Something like this will appear:
# * branch-name
# main

# The active branch is the one with the asterisk
```

- If the _branch_ is different, change it to it:
```bash
git checkout branch-name
```

### 2. Make the corrections that were requested in the PR

### 3. Add to versioning
```bash
git add .
```

### 4. Record corrections
```bash
git commit --amend --no-edit
```

### 5. Upload to GitHub
```bash
git push origin branchname --force
```

- If this results in an error, synchronize with GitHub:

```bash
git pull origin branchname --rebase
```

### 7. Notify reviewers
Add a comment below the review you corrected so that those who made it can be notified and review again.

---

## Finalize the _branch_
> :warning: Only perform this step when your _pull request_ is **approved and added to the main _branch_** (_merge_) by an authorized person (reviewer).

1. Change to the main _branch_

```bash
git checkout main
```

2. Sync with GitHub

```bash
git pull origin main
```

3. Delete the _branch_ you were working on

```bash
git branch -d branch-name
```

If you want to work on another feature/fix, [create a new _branch_](#create-a-branch).

---

## :pencil: Suggest improvements or corrections
If you still don't feel confident in contributing code or have found a problem/situation for improvement and want to report it, create an _issue_.

Use [this guide](https://docs.github.com/pt/issues/tracking-your-work-with-issues/creating-an-issue) to report a problem or indicate an improvement through _issues_.

### :question: Did you have any questions? Contact one of the repository members