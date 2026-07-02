# Linux Command Cheat Sheet

`ls` – list files in a directory. `ls -la`
`cd` – change directory. `cd /var/log`
`pwd` – print current directory. `pwd`
`cat` – print file contents. `cat /etc/passwd`
`less` – view file page by page. `less /var/log/syslog`
`grep` – search text in files. `grep "error" app.log`
`find` – search for files. `find / -name "*.conf"`
`ps` – list running processes. `ps aux`
`top` – live process/resource monitor. `top`
`kill` – stop a process by PID. `kill -9 1234`
`chmod` – change file permissions. `chmod 644 file.txt`
`chown` – change file owner. `chown user:group file.txt`
`whoami` – show current user. `whoami`
`su` – switch user. `su root`
`sudo` – run command as another user (root). `sudo apt update`
`tail -f` – follow live log output. `tail -f /var/log/auth.log`
`head` – show first lines of a file. `head -n 20 file.txt`
`journalctl` – view systemd logs. `journalctl -u ssh`
`netstat` / `ss` – show network connections. `ss -tulpn`
`man` – show manual for a command. `man chmod`
mkdir – create a directory. mkdir test
rm – remove file. rm file.txt
rm -r – remove directory. rm -r folder/
cp – copy file. cp a.txt b.txt
mv – move/rename. mv a.txt b.txt
touch – create empty file. touch file.txt
df -h – disk space usage. df -h
du -sh – size of a folder. du -sh /var/log
history – show command history. history
alias – shortcut for a command. alias ll='ls -la'
