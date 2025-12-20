---
date: 2025-12-20 17:09:35
title: Process API
permalink: process-api
publish: true
---

# Process API

>[Interlude: Process API | Operating Systems: Three Easy Pieces](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-intro.pdf)

!!! abstract "Key Terms"
    - Each process has a name; in most systems, that name is a number known as a process ID (PID).

    - The `fork()` system call is used in UNIX systems to create a new process. The creator is called the parent; the newly created process is called the child. As sometimes occurs in real life [J16], the child process is a nearly identical copy of the parent.

    - The `wait()` system call allows a parent to wait for its child to complete execution.

    - The `exec()` family of system calls allows a child to break free from its similarity to its parent and execute an entirely new program.

    - A UNIX shell commonly uses `fork()`, `wait()`, and `exec()` to launch user commands; the separation of fork and exec enables features like input/output redirection, pipes, and other cool features, all without changing anything about the programs being run.

    - Process control is available in the form of signals, which can cause jobs to stop, continue, or even terminate.

    - Which processes can be controlled by a particular person is encapsulated in the notion of a user; the operating system allows multiple users onto the system, and ensures users can only control their own processes.

    - A superuser can control all processes (and indeed do many other things); this role should be assumed infrequently and with caution for security reasons.
