---
date: 2026-04-23 22:52:45
title: Traceroute
permalink: proj-1
publish: true
tags:
  - 计算机网络
  - CS168
---

# Traceroute

> [Project 1: Traceroute | CS168 SP26](https://sp26.cs168.io/proj1/)

In this project, we need to implement the traceroute program, which is a tool to trace the [route](Introduction%20to%20Routing.md) of a packet from the source to the destination.

## Principles Overview

!!! info
    Normally, if we send a packet and receive a response packet, we don’t know what path the packets used to travel through the network. In other words, we can’t figure out which intermediate routers forwarded your packet. None of the header fields tell us about the path the packet used.

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

    !!! tip
        Recall that on a computer, each running service is associated with a port number. If we pick a port number that’s not associated with any running service, the destination computer will get confused and send back a “Port Unreachable” error message: “The port you asked for does not correspond to an existing application.”[^2]

- For 3, one probe per TTL is often not enough: loss and delay jitter can make results unstable, and under ECMP different probes may take different paths. So traceroute sends multiple probes per TTL to get more reliable RTTs and expose path diversity.

### Traceroute Main Logic

```python
def traceroute(sendsock: util.Socket, recvsock: util.Socket, ip: str) \
        -> list[list[str]]:
    """ Run traceroute and returns the discovered path.

    Calls util.print_result() on the result of each TTL's probes to show
    progress.

    Arguments:
    sendsock -- This is a UDP socket you will use to send traceroute probes.
    recvsock -- This is the socket on which you will receive ICMP responses.
    ip -- This is the IP address of the end host you will be tracerouting.

    Returns:
    A list of lists representing the routers discovered for each ttl that was
    probed.  The ith list contains all of the routers found with TTL probe of
    i+1.   The routers discovered in the ith list can be in any order.  If no
    routers were found, the ith list can be empty.  If `ip` is discovered, it
    should be included as the final element in the list.
    """

    # Accumulate one router list per TTL hop.
    discovered_routers = []
    # Probe TTL values from 1 up to the configured maximum.
    for ttl in range(1, TRACEROUTE_MAX_TTL+1):
        # Configure outgoing probe packets to expire after `ttl` hops.
        sendsock.set_ttl(ttl)
        # Store unique router IPs discovered for this specific TTL.
        routers = []
        # Send multiple probes for this TTL to tolerate packet loss.
        for _ in range(PROBE_ATTEMPT_COUNT):
            # Send a UDP traceroute probe toward the target host and destination port.
            sendsock.sendto(b"traceroute probe", (ip, TRACEROUTE_PORT_NUMBER))
            # Try to read one valid ICMP response for this probe.
            addr = probe_response(recvsock=recvsock, ttl=ttl)
            # Keep only non-empty and non-duplicate hop addresses.
            if addr and addr not in routers:
                routers.append(addr)
        # Print intermediate traceroute output for this TTL.
        util.print_result(routers=routers, ttl=ttl)
        # Persist this TTL result into the overall traceroute path.
        discovered_routers.append(routers)
        # Stop early once the destination host is reached.
        if ip in routers:
            break
    return discovered_routers
```

### Some Troubleshooting

> [Troubleshooting - Traceroute | vglab](https://github.com/virtualguard101/vglab/blob/main/network/cs168/traceroute/troubleshooting.md)


[^1]: [Hints - Parsing Packets - Project 1A: Basic Traceroute | CS168 SP26](https://sp26.cs168.io/proj1/proj1a/#hints)

[^2]: [Unreachable Ports - Introducing Traceroute - Traceroute Guide | CS168 SP26](https://sp26.cs168.io/proj1/guide/#24-unreachable-ports)