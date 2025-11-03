---
date: 2025-09-17 01:13:00
title: Rust入门要点
permalink: 
publish: true
---

# Rust 入门要点

## 安装编译环境

可参考[安装 | Rust 程序设计语言 简体中文版](https://kaisery.github.io/trpl-zh-cn/ch01-01-installation.html)

## `Hello, World`

- 使用 `cargo` 创建一个新的Rust项目:

    ```bash
    cargo new hello-world
    ```
    这会在当前目录下生成一个名为 `hello-world` 的项目目录。

- 切换至这个目录，使用 `tree` 命令查看项目结构:

    ```bash
    $ tree .
    .
    ├── Cargo.toml
    └── src
        └── main.rs
    ```

- 其中用于输出 `Hello, world!` 的源码已经位于 `src/main.rs`:

    ```rs
    fn main() {
        println!("Hello, world!");
    }
    ```

- 使用Rust编译器（`rustc`）对源码进行编译:

    ```bash
    rustc src/main.rs
    ```
    在哪个目录下执行的这个编译命令，就会在哪生成一个与源码文件同名的可执行程序，这里就会在项目根目录下生成一个名为 `main` 的可执行程序。

- 执行这个可执行程序，就会在终端上输出`Hello, world!`字符串:

    ```bash
    $ ./main
    Hello, world!
    ```

## `Cargo`

> [Hello, Cargo! | Rust 程序设计语言 简体中文版](https://kaisery.github.io/trpl-zh-cn/ch01-03-hello-cargo.html)

`Cargo` 是 Rust 的构建系统和包管理器。它可以为我们处理很多任务，比如初始化版本控制、构建代码、下载依赖库并编译这些库。

!!! tip "astral uv"
    如果有使用[`uv`](../../tools/uv.md)管理Python项目的经验，那么快速上手`cargo`应当不是问题，因为uv在设计时很大程度上参考了 Cargo 的理念，==以及其目标就是**成为"Python 的 Cargo"**==。另外一个有意思的事实是，==uv本身其实就是用 Rust 写的==。

Cargo 的强大之处在于其可作为一个**统一工具链**使用，==即**通过单一工具覆盖开发、测试、构建、发布全流程**==，提供从项目创建到依赖管理的完整生命周期管理。

在上文中的项目目录结构中，不难发现还有一个名为 `Cargo` 的 [`.toml` 文件（Tom's Obvious, Minimal Language）](https://toml.io/)，这个是 Cargo 的配置文件，用于配置 Cargo 行为与项目信息。

以下是一些常用的 Cargo 子命令:

- 可通过 `new` 命令创建一个新项目:

    ```bash
    cargo new [project-name]
    ```

    - 也可以通过 `init` 命令在现有目录初始化 Rust 项目:

        ```bash
        cargo init [/path/to/project]
        ```

- 通过 `add` 命令添加项目依赖:

    ```bash
    cargo add [dependencies1@version] [dependencies2@version] [...]
    ```

- ==通过 `build` 构建项目==:

    ```bash
    $ cargo build
      Compiling hello-world v0.1.0 (/path/to/hello-world)
       Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.23s
    ```

- ==使用 `run` 命令运行项目==:

    ```bash
    $ cargo run
       Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.00s
        Running `target/debug/hello-world`
    Hello, world!
    ```

- ==使用 `check` 命令在不生成二进制文件的情况下构建项目来检查错误==:

    ```bash
    $ cargo check
       Checking hello-world v0.1.0 (/home/virtualguard/csdiy/rust/hello-world)
        Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.04s

    ```
    通常 `cargo check` 要比 `cargo build` 快得多，因为它省略了生成可执行文件的步骤。如果你在编写代码时持续的进行检查，使用`cargo check` 可以快速了解现在的代码能不能正常通过编译！

    在编写代码时定期运行 `cargo check` 是一个良好实践。

- 使用 `-h` 获取帮助信息:

    ```bash
    $ cargo -h
    Rust's package manager

    Usage: cargo [+toolchain] [OPTIONS] [COMMAND]
        cargo [+toolchain] [OPTIONS] -Zscript <MANIFEST_RS> [ARGS]...

    Options:
    -V, --version                  Print version info and exit
        --list                     List installed commands
        --explain <CODE>           Provide a detailed explanation of a rustc error message
    -v, --verbose...               Use verbose output (-vv very verbose/build.rs output)
    -q, --quiet                    Do not print cargo log messages
        --color <WHEN>             Coloring [possible values: auto, always, never]
    -C <DIRECTORY>                 Change to DIRECTORY before doing anything (nightly-only)
        --locked                   Assert that `Cargo.lock` will remain unchanged
        --offline                  Run without accessing the network
        --frozen                   Equivalent to specifying both --locked and --offline
        --config <KEY=VALUE|PATH>  Override a configuration value
    -Z <FLAG>                      Unstable (nightly-only) flags to Cargo, see 'cargo -Z help' for details
    -h, --help                     Print help

    Commands:
        build, b    Compile the current package
        check, c    Analyze the current package and report errors, but don't build object files
        clean       Remove the target directory
        doc, d      Build this package's and its dependencies' documentation
        new         Create a new cargo package
        init        Create a new cargo package in an existing directory
        add         Add dependencies to a manifest file
        remove      Remove dependencies from a manifest file
        run, r      Run a binary or example of the local package
        test, t     Run the tests
        bench       Run the benchmarks
        update      Update dependencies listed in Cargo.lock
        search      Search registry for crates
        publish     Package and upload this package to the registry
        install     Install a Rust binary
        uninstall   Uninstall a Rust binary
        ...         See all commands with --list

    See 'cargo help <command>' for more information on a specific command.
    ```

## 一个简单的猜数字游戏

- [编写一个猜数字游戏 | Rust 程序设计语言 简体中文版](https://kaisery.github.io/trpl-zh-cn/ch02-00-guessing-game-tutorial.html)
