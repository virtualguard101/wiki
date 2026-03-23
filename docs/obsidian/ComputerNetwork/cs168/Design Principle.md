---
date: 2026-03-24 01:27:43
title: Design Principle
permalink: desgin-principle
publish: true
tags:
  - 计算机网络
  - CS168
---

# Design Principles

## Narraw Waist Model

![](assets/design-principle/network_arch.png)

This diagram shows the different components of a network architecture, notice there’s only one protocol at Layer 3. This is the “*narrow waist*” that enables Internet connectivity. 

## Demultiplexing

Think about that when a router receive a packet, how dose it know which protocol to use to process the packet?

![](assets/design-principle/demultiplexing_1.png)

The answer can be found in the related header of the packet, which we have discussed in [Multiple Headers](Layers%20of%20the%20Internet.md#Multiple-Headers) section.

![Demultiplexing in L4](assets/design-principle/demultiplexing_2.png)

This process is called *demultiplexing* (**解复用**).

Demultiplexing can not only use for choosing the protocol to process the packet (works on **L4 - Transport Layer**, we discussed above), but also for choosing the *port* to running some service, which works in **L7 - Application Layer**.

![Demultiplexing in L7](assets/design-principle/demultiplex_3.png)

!!! warning "Logical Port vs Physical Port"
    - **Logical Port**: A number identifying an application. Exists in software.

        ![](assets/design-principle/logical_port.png)

    - **Physical port**: The hole you plug a cable into. Exists in hardware.

        ![](assets/design-principle/physical_port.png)

!!! note "socket[^1]"
    The term *socket* (**套接字**) refers to an OS mechanism for connecting an application to the networking stack in the OS. When an application opens a socket, that socket is associated with a logical port number. When the OS receives a packet, it uses the port number to direct that packet to the associated socket.

In general, demultiplexing helps the operating system pass packets to the correct application, based on the [Layers Abstraction](Layers%20of%20the%20Internet.md#Layers-of-the-Internet) we've discussed previously.

![](assets/design-principle/demultiplexing_4.png)

![](assets/design-principle/demultiplexing_5.png)

## End-to-End Principle


[^1]: [Demultiplexing - Network Architecture | CS168 Textbook](https://textbook.cs168.io/intro/architecture.html#demultiplexing)