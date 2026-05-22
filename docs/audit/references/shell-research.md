A good prerequisite course for `vimtutor` should not try to teach “all of Unix.” It should teach the **mental model of working at a shell prompt**, enough filesystem fluency to avoid getting lost, and enough process/file knowledge to understand what Vim is doing when it opens, edits, saves, and quits.

The key framing is this: **`vimtutor` is not just a lesson inside Vim; it is a shell command that launches Vim on a temporary/copy tutorial file.** Vim’s own documentation says that on Unix you can start it from the shell with `vimtutor`, and that it makes a copy of the tutor file so the learner can edit it without damaging the original. The same documentation describes it as a roughly 30-minute hands-on tutorial for basic Vim functionality. ([Vim Help][1])

## Course title

**Shell Foundations for Vimtutor**

A reasonable prerequisite course would be short: perhaps 2–4 hours for motivated adults, or 1–2 weeks if taught slowly with exercises.

The purpose is not to make students expert shell users. The purpose is to make sure that when they type

```sh
vimtutor
```

they understand what kind of thing they just did.

## Central learning goals

By the end of the prerequisite course, students should be able to:

1. Explain the difference between the **terminal**, the **shell**, and a **program running inside the terminal**.
2. Use the shell prompt to run simple commands with arguments.
3. Navigate the filesystem using `pwd`, `ls`, and `cd`.
4. Understand relative paths, absolute paths, `.` , `..`, and `~`.
5. Create, inspect, copy, move, and remove small text files safely.
6. Explain that Vim edits a **buffer**, not the file directly, until the buffer is written.
7. Understand why `:w`, `:q`, `:q!`, and `:wq` matter.
8. Know how the shell finds a command such as `vimtutor` through `PATH`.
9. Recognize when they are at the shell prompt versus inside Vim.
10. Recover calmly from common beginner states: “I’m stuck in Vim,” “I typed a command but nothing happened,” “I’m in the wrong directory,” or “I edited the wrong file.”

That seventh goal is especially important. Vim’s reference manual says that editing a file with Vim means reading the file into a buffer, changing the buffer, and then writing the buffer back to a file; until the buffer is written, the original file remains unchanged. ([Vim Help][2]) That is one of the core ideas students should understand before `vimtutor`, because otherwise saving and quitting feel arbitrary.

## Concept 1: Terminal, shell, command, program

Students should first learn that the terminal window is not “Unix.” It is an interface that lets them talk to a shell. The shell is the command interpreter.

A useful beginner model:

```text
keyboard → terminal → shell → program
```

For example:

```sh
vimtutor
```

means: the user types text into the terminal; the shell reads the command; the shell looks for a program named `vimtutor`; that program starts Vim with the tutorial file.

The GNU Bash manual describes a shell as both a command interpreter and a programming language, and notes that it provides an interface to system utilities. ([GNU][3]) For a `vimtutor` prerequisite, students do not need shell programming yet, but they do need to understand the command-interpreter part.

Learning goals:

```text
I can identify the shell prompt.
I can run a command.
I can tell the difference between a shell command and text typed inside a program.
I can return to the shell after a program exits.
```

Essential commands:

```sh
echo hello
date
whoami
pwd
clear
exit
```

## Concept 2: The shell reads text in a structured way

A shell command is not just “a sentence.” It has a structure:

```sh
command option argument argument
```

Examples:

```sh
ls
ls -l
ls -la
cd Documents
vim notes.txt
```

Students should understand that spaces separate words, and that the first word is usually the command name.

The Bash manual describes shell operation as a sequence: it reads input, breaks it into words and operators, performs expansions and redirections, executes the command, and collects an exit status. ([GNU][3]) Students do not need all of that detail yet, but they should learn that the shell interprets certain characters specially.

Learning goals:

```text
I can identify the command name.
I can identify options and arguments.
I know that spaces matter.
I know that quotes protect spaces inside filenames.
```

Examples:

```sh
mkdir practice
cd practice
touch hello.txt
touch "two words.txt"
ls
```

This matters for Vim because commands such as these are different:

```sh
vim notes.txt
vim "my notes.txt"
vim my notes.txt
```

The last one asks Vim to open two files, `my` and `notes.txt`, not one file named `my notes.txt`.

## Concept 3: Current working directory

Before using Vim, students need to understand that the shell is always “somewhere” in the filesystem. That place is the **current working directory**.

Core commands:

```sh
pwd
ls
cd
cd ..
cd ~
```

Core concepts:

```text
pwd     print current directory
ls      list files
cd      change directory
.       current directory
..      parent directory
~       home directory
```

Learning goals:

```text
I can find where I am.
I can move to my home directory.
I can move into and out of a project folder.
I can predict where a new file will be created.
```

Practice:

```sh
pwd
mkdir vim-practice
cd vim-practice
pwd
touch sample.txt
ls
cd ..
ls
```

This is crucial because when a student later runs

```sh
vim notes.txt
```

Vim opens or creates `notes.txt` in the current directory unless given another path.

## Concept 4: Files, directories, and pathnames

Students should know the difference between files and directories, and they should understand that a pathname tells the shell where something is.

Examples:

```sh
notes.txt
practice/notes.txt
../notes.txt
/home/alice/practice/notes.txt
~/practice/notes.txt
```

Learning goals:

```text
I can distinguish a filename from a pathname.
I can explain relative and absolute paths.
I can use tab completion to avoid mistyping names.
I can tell where a file will be saved.
```

Minimum useful commands:

```sh
ls
ls -l
cat file.txt
less file.txt
cp old.txt new.txt
mv oldname.txt newname.txt
rm unwanted.txt
mkdir folder
rmdir empty-folder
```

For a prerequisite course, I would teach `rm` conservatively. Students should understand that Unix deletion is usually immediate and does not necessarily mean “move to trash.”

## Concept 5: Text files versus rendered documents

Vim is a text editor. Students should understand what a plain text file is.

They should know that these are text-like:

```text
.txt
.md
.py
.c
.html
.csv
.tex
```

And these are not normally edited as plain text in Vim:

```text
.pdf
.docx
.png
.jpg
.xlsx
```

Learning goals:

```text
I can explain what a plain text file is.
I can open a text file with cat or less.
I understand that Vim edits text, not formatted pages.
```

Practice:

```sh
echo "Hello" > hello.txt
cat hello.txt
vim hello.txt
```

For `vimtutor`, this matters because the tutorial itself is a text file that the student edits.

## Concept 6: Opening a file versus changing a file

This is one of the most important prerequisite ideas.

Students often think:

```text
I opened the file, so I changed the file.
```

But in Vim the better model is:

```text
file on disk → buffer in memory → file on disk
```

Vim reads the file into a buffer. The learner edits the buffer. The file is not actually changed until the buffer is written. Vim’s documentation states this directly: editing consists of reading the file into a buffer, changing the buffer, and writing the buffer into a file; the original remains unchanged until the buffer is written. ([Vim Help][2])

Learning goals:

```text
I can explain the difference between a file and a buffer.
I understand why quitting without saving is possible.
I understand why saving is a separate action.
```

This prepares students for:

```vim
:w
:q
:q!
:wq
```

Conceptual meanings:

```text
:w     write the buffer to the file
:q     quit, if there are no unsaved changes
:q!    quit and discard unsaved changes
:wq    write, then quit
```

## Concept 7: Command lookup and PATH

Students do not need to master environment variables before `vimtutor`, but they should know that when they type a command name, the shell has to find an executable program.

Useful commands:

```sh
command -v vim
command -v vimtutor
echo "$PATH"
```

Learning goals:

```text
I understand that vimtutor is a command found by the shell.
I can check whether Vim and vimtutor are installed.
I understand that “command not found” usually means the shell cannot find the program.
```

Useful setup check:

```sh
command -v vim
command -v vimtutor
vim --version
```

If `vimtutor` is missing but Vim is installed, that may be a packaging issue. On some systems, the tutorial is included with a fuller Vim package rather than a minimal Vi/Vim package.

## Concept 8: Standard input, output, and error

This is not strictly necessary to begin `vimtutor`, but it helps students understand the shell environment around Vim.

Core ideas:

```text
stdin   where input comes from
stdout  where normal output goes
stderr  where error messages go
```

Useful examples:

```sh
echo "hello"
echo "hello" > hello.txt
cat hello.txt
ls no-such-file
```

Students should understand that many shell programs print output and then exit, while Vim takes over the terminal screen and becomes interactive.

Learning goals:

```text
I can distinguish a command that prints output from a full-screen terminal program.
I know that Vim is interactive and does not behave like echo, ls, or cat.
```

## Concept 9: Full-screen terminal programs

This is a major source of confusion.

Some commands print output and return immediately:

```sh
ls
date
cat file.txt
```

Other commands take over the terminal until you exit them:

```sh
less file.txt
man ls
vim file.txt
vimtutor
```

Learning goals:

```text
I can tell when I am inside a full-screen terminal program.
I know that keys may mean something different inside that program.
I know how to exit less, man, and Vim.
```

Useful preparation:

```sh
less file.txt
```

Then teach:

```text
q exits less
```

This gives students a gentler example before Vim, where `q` alone is not the general exit command.

## Concept 10: The keyboard is interpreted by the current program

Students should understand that the same key can mean different things depending on context.

At the shell prompt:

```text
j
```

just types the letter `j`.

Inside Vim normal mode:

```text
j
```

moves the cursor down.

Inside Vim insert mode:

```text
j
```

inserts the letter `j`.

This prepares students for the central Vim idea: **modes**. `vimtutor` teaches modes, but students are less confused if they already understand that programs can interpret keystrokes differently.

Learning goals:

```text
I can explain why the same key does different things in different programs.
I know that Vim has modes.
I know that Esc is often used to return to Vim normal mode.
```

## Concept 11: Minimal process control and recovery

Before `vimtutor`, students should know a few emergency tools.

Useful keys:

```text
Ctrl-C    interrupt many command-line programs
Ctrl-D    send end-of-input / exit some shells or programs
Ctrl-Z    suspend a foreground job
```

For a beginner prerequisite, I would be careful with `Ctrl-Z`. It is useful, but it can also create confusion because the program is not exited; it is suspended.

Learning goals:

```text
I can interrupt a mistaken shell command with Ctrl-C.
I know that Ctrl-Z suspends rather than quits.
I know that Vim should normally be exited with :q, :q!, or :wq, not by closing the terminal.
```

Optional commands:

```sh
jobs
fg
```

## Concept 12: Man pages and built-in help

Students should learn that Unix systems have local documentation.

Useful commands:

```sh
man ls
man cd
man vim
man vimtutor
```

But they should also learn that `cd` may be a shell builtin, so `man cd` may not always behave the way they expect. The Bash manual notes that builtins such as `cd` directly manipulate the shell itself, which is why they cannot simply be ordinary external utilities. ([GNU][3])

Learning goals:

```text
I can use man pages for common commands.
I know that some commands are shell builtins.
I know that Vim has its own help system.
```

For Vim:

```vim
:help
:help tutor
:help write-quit
```

This connects nicely to `vimtutor`, because students begin to see Vim as its own command environment inside the shell environment.

## A possible prerequisite course outline

### Unit 1: Where am I?

Topics:

```text
terminal
shell
prompt
current working directory
home directory
```

Commands:

```sh
pwd
ls
cd
clear
exit
```

Learning goals:

```text
Students can open a terminal, identify the prompt, find their current directory, move to their home directory, and return to the shell after running simple commands.
```

Mini-assessment:

```sh
cd ~
mkdir vim-practice
cd vim-practice
pwd
```

Student should be able to explain what each line did.

### Unit 2: Files and paths

Topics:

```text
files
directories
relative paths
absolute paths
hidden files
tab completion
```

Commands:

```sh
touch
mkdir
cp
mv
rm
cat
less
```

Learning goals:

```text
Students can create a practice directory, create text files, rename them, copy them, inspect them, and delete only files they intentionally choose.
```

Mini-assessment:

```sh
mkdir shell-vim-demo
cd shell-vim-demo
echo "first line" > note.txt
cp note.txt backup.txt
ls
cat backup.txt
```

### Unit 3: Running commands

Topics:

```text
command names
options
arguments
quoting
PATH
command not found
```

Commands:

```sh
echo
command -v
which
type
```

Learning goals:

```text
Students can distinguish commands, options, and arguments; they can explain why filenames with spaces need quotes; and they can check whether vim and vimtutor are available.
```

Mini-assessment:

```sh
command -v vim
command -v vimtutor
echo "$PATH"
```

### Unit 4: Text files and editors

Topics:

```text
plain text
file on disk
buffer in memory
save/write
quit
discard changes
```

Commands:

```sh
cat
less
vim
```

Vim commands introduced only conceptually:

```vim
:w
:q
:q!
:wq
```

Learning goals:

```text
Students can explain that opening a file is not the same as saving changes, and that Vim edits a buffer before writing to disk.
```

Mini-assessment:

```sh
echo "do not change yet" > demo.txt
vim demo.txt
cat demo.txt
```

Then ask: Did the file change? When? Why?

### Unit 5: Full-screen programs

Topics:

```text
programs that print and exit
programs that take over the terminal
keyboard control inside programs
```

Commands:

```sh
less
man
vim
```

Learning goals:

```text
Students can tell whether they are at the shell prompt or inside another program, and they can exit common full-screen programs intentionally.
```

Mini-assessment:

```sh
man ls
```

Exit with:

```text
q
```

Then:

```sh
vim --version
```

This contrast helps: `man` is full-screen; `vim --version` prints and exits.

### Unit 6: Starting vimtutor deliberately

Topics:

```text
vimtutor as a shell command
temporary/copy tutorial file
safe experimentation
returning to the shell
```

Commands:

```sh
vimtutor
vimtutor -c 2
```

Learning goals:

```text
Students can start vimtutor, understand that it opens a copy of the tutorial file, work through the tutorial, save/quit as instructed, and return to the shell without panic.
```

The Vim documentation explicitly says that `vimtutor` can be started from the Unix shell and that it makes a copy of the tutor file so the learner can edit it without damaging the original. ([Vim Help][1])

## What students do *not* need before vimtutor

A prerequisite course should avoid overloading students. They do **not** need these before starting `vimtutor`:

```text
shell scripting
regular expressions
sed and awk
pipes in depth
permissions in depth
ssh
git
cron
package management details
advanced job control
advanced Vim configuration
.vimrc customization
plugins
buffers/windows/tabs in depth
```

Some of these are valuable later, but they are distractions before the first Vim tutorial.

## The minimal “ready for vimtutor” checklist

A student is ready for `vimtutor` if they can do the following without help:

```sh
pwd
ls
cd ~
mkdir vim-practice
cd vim-practice
command -v vim
command -v vimtutor
vimtutor
```

And they can answer:

```text
What directory am I in?
What command did I just run?
Am I at the shell prompt or inside Vim?
What is the difference between editing a buffer and saving a file?
How do I quit without saving?
How do I save and quit?
```

## Suggested final assessment

Give students this task before `vimtutor`:

```sh
cd ~
mkdir vim-prereq-check
cd vim-prereq-check
echo "This is a practice file." > practice.txt
cat practice.txt
vim practice.txt
cat practice.txt
command -v vimtutor
vimtutor
```

They should be able to narrate the whole process:

```text
I moved to my home directory.
I created a practice directory.
I entered that directory.
I created a text file.
I displayed its contents.
I opened it in Vim.
I edited a buffer.
I saved or discarded changes.
I checked that vimtutor exists.
I launched vimtutor from the shell.
```

That is the right prerequisite target: not “knows Unix,” but **can move around, run commands, understand files and buffers, and recover from confusion**.

[1]: https://vimhelp.org/usr_01.txt.html "Vim: usr_01.txt"
[2]: https://vimhelp.org/editing.txt.html "Vim: editing.txt"
[3]: https://www.gnu.org/software/bash/manual/bash.html "Bash Reference Manual"

