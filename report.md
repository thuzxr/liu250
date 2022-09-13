1.1

traceroute from LYON-host to MUNI-host
```
LYON_host:~# traceroute -4 68.105.0.1 -n
traceroute to 68.105.0.1 (68.105.0.1), 30 hops max, 46 byte packets
 1  68.106.0.2  0.008 ms  0.003 ms  0.002 ms
 2  68.0.8.1  0.301 ms  0.237 ms  0.435 ms
 3  68.0.7.2  0.527 ms  0.470 ms  0.473 ms
 4  68.105.0.1  3.662 ms  0.465 ms  0.437 ms
```


traceroute from host_2 in the North Data Center to MILA-host
 ```
 host_2:~# traceroute -4 68.108.0.1 -n
traceroute to 68.108.0.1 (68.108.0.1), 30 hops max, 46 byte packets
 1  68.200.0.1  6.641 ms  4.290 ms  4.136 ms
 2  68.0.3.2  4.617 ms  68.0.9.2  3.621 ms  3.254 ms
 3  68.0.11.2  3.588 ms  3.430 ms  3.468 ms
 4  68.108.0.1  4.030 ms  3.611 ms  3.602 ms
 ```
