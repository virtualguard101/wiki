---
date: 2026-04-23 12:26:45
title: Traceroute
permalink: proj-1
publish: false
tags:
  - 计算机网络
  - CS168
---

# Traceroute

> [Project 1: Traceroute | CS168 SP26](https://sp26.cs168.io/proj1/)

In this project, we need to implement the traceroute program, which is a tool to trace the [route](Introduction%20to%20Routing.md) of a packet from the source to the destination.

## Principles Overview

Traceroute discovers each hop on the path by sending probe packets with gradually increasing TTL values (1, 2, 3, ...).  

When a router decrements TTL to 0, it drops the packet and returns an ICMP *Time Exceeded* message, revealing that router's IP.  

Once the probe reaches the destination, the destination responds differently (commonly ICMP *Port Unreachable* for UDP probes), which indicates the route has been fully traced.

Also refer to the [guide](https://sp26.cs168.io/proj1/guide/#2-introducing-traceroute) for more vivid details.

## Basic Traceroute

> [Project 1A: Basic Traceroute | CS168 SP26](https://sp26.cs168.io/proj1a/)

For basic implementation, we need to implement three parts:

1. The header of IPv4, ICMP and UDP packet (`__init__` method).

2. Some auxiliary functions to carry out [misc tasks](https://sp26.cs168.io/proj1/guide/#2-introducing-traceroute) in traceroute.

3. Main logic of traceroute.

### Implementation Thoughts

#### Protocol Headers

For those headers, is necessary to figure out the structures of each protocol.

Fortunately, CS168 project guide has provided the structures of each protocol headers, which is convient for us to referring: [Header Structures - Traceroute Guide | CS168 SP26](https://sp26.cs168.io/proj1/guide/#3-header-structure)

When implementing the headers, we need to pay attention to the following points:

- `buffer[]` is a bytearray, which is a list of bytes. It means that it will be indexed by bytes, not bits. So we need to transfer the buffer(ipv4 header) into a continuous bitstring[^1].

- For each metadata, we have different ways to implement, but the efficiency is also in difference.

    For example, the type of service field in ipv4 header is a 8-bit field, which is the second byte of the buffer. We can implement it in the following ways:

    ```python
    self.tos = int(bitstring[16:24], base=2) # inefficient, cost twice time of type conversion
    ```

    ```python
    # Evaluate the type of service field from the second byte of the buffer(TOS/DSCP+ECN) directly.
    self.tos = buffer[1] 
    ```

    As the comments saying, the second way is more efficient, because it doesn't need to convert the type of the field.

- Notice that some metadata should be converted to network byte order(big-endian).

    ```python
    self.length = int.from_bytes(buffer[2:4], byteorder='big') 
    # Extract the total length of the packet field from the buffer.
    # Convert the next 2 bytes of the buffer to an integer.
    # Notice: `byteorder='big'` is necessary to convert the bytes to an integer in network byte order(big-end).
    ```

#### Auxiliary Functions

According to the [guide](https://sp26.cs168.io/proj1/guide/#2-introducing-traceroute), we need to understand and implement three points:

1. How to exploiting the TTL field to trace the route.

2. Why and how we use ICMP *packet unreachable* messages to trace the route.

3. Why and how we use multiple probes to trace the route.

In these three problems, it is obviosly to figure out 'why' according to [Traceroute Principle](#Principles-Overview):

- For 1, we can get answer from the principles directly.

- For 2, we know that in order to consider that whether the destination is reachable, it will reply while some errors occur, such as we send a packet to an *unreachable port*. So we can send a UDP packet in some "invalid ways" so that we can get the error response(an ICMP-over-IP packet) from the destination.

- For 3, 

    !!! tip
        Recall that on a computer, each running service is associated with a port number. If we pick a port number that’s not associated with any running service, the destination computer will get confused and send back a “Port Unreachable” error message: “The port you asked for does not correspond to an existing application.”[^2]


[^1]: [Hints - Parsing Packets - Project 1A: Basic Traceroute | CS168 SP26](https://sp26.cs168.io/proj1/proj1a/#hints)

[^2]: [Unreachable Ports - Introducing Traceroute - Traceroute Guide | CS168 SP26](https://sp26.cs168.io/proj1/guide/#24-unreachable-ports)