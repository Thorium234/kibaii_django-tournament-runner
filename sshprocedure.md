 Here’s the *full "zero to hero" SSH + Git procedure for Termux* 

Copy-paste this and you’ll never type password again.



### *FULL PROCEDURE: SSH Keys for Git in Termux - For Beginners*



#### *STEP 1: Install Tools*
pkg update && pkg upgrade -y
pkg install git openssh -y
#### *STEP 2: Generate SSH Key Pair*
ssh-keygen -t ed25519 -C "your_email@gmail.com"
What to press:

1.  `Enter` to save at default location

2.  `Enter` for no passphrase OR type one if you want extra security

3.  `Enter` again



Output:
Your public key has been saved in /data/data/com.termux/files/home/.ssh/id_ed25519.pub
#### *STEP 3: Copy Your Public Key*
cat ~/.ssh/id_ed25519.pub
Long press > Copy. It should start with `ssh-ed25519 AAAA... your_email@gmail.com`



#### *STEP 4: Add Key to GitHub/GitLab*

1.  Go to `github.com/settings/keys`

2.  Click `New SSH key`

3.  *Title*: `Termux Phone`

4.  *Key*: Paste the 1 line from step 3

5.  Click `Add SSH key`



#### *STEP 5: Test If SSH Works*
ssh -T git@github.com
Expected: `Hi YourUsername! You've successfully authenticated`

Type `yes` if it asks about `known_hosts`



#### *STEP 6: Clone Repo Using SSH*

THIS IS THE MOST IMPORTANT STEP
git clone git@github.com:YourUsername/repo-name.git
Now `cd repo-name` and you can `git push` / `git pull` with no password.



---



### *SUMMARY CHEAT SHEET OF COMMANDS*
pkg install git openssh
ssh-keygen -t ed25519 -C "email"
cat ~/.ssh/id_ed25519.pub          # copy this to github
ssh -T git@github.com              # test
git clone git@github.com:user/repo.git  # clone with SSH
git remote -v                      # check if using ssh or https
---



### *5 POSSIBLE MISTAKES + HOW TO FIX*
#	Mistake	Error You’ll See	Fix
**1**	**Cloned with HTTPS instead of SSH**	`Username for 'https://github.com':`	Change remote: `git remote set-url origin git@github.com:User/Repo.git`
**2**	**Pasted wrong key to GitHub**	`Key is invalid. Must be OpenSSH public key format`	You pasted private key. Run `cat ~/.ssh/id_ed25519.pub` and paste THAT one. Must start with `ssh-ed25519`
**3**	**Bad permissions**	`Permissions 0644 for id_ed25519 are too open`	`chmod 700 ~/.ssh && chmod 600 ~/.ssh/id_ed25519`
**4**	**Permission denied publickey**	`git@github.com: Permission denied (publickey)`	1. Key not added to github 2. Testing with wrong email. Run `ssh -T git@github.com` to check which account
**5**	**Host key verification failed**	`Host key verification failed`	`ssh-keyscan github.com >> ~/.ssh/known_hosts` then test again
### *Pro Tips for Termux*

1.  *Auto-start ssh-agent*: Add this to `~/.bashrc` so you don't type passphrase
    eval $(ssh-agent -s)
    ssh-add
2.  *Multiple GitHub accounts*: Create `~/.ssh/config` file to switch keys

3.  *Storage*: `termux-setup-storage` if you want to clone to `/sdcard`



Rule to remember:  

`https://` = asks password  

`git@github.com:` = uses SSH key




