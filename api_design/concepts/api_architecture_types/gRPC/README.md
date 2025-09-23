# gRPC

![image](https://cdn.prod.website-files.com/610d78d90f895fbe6aef8810/65d758bf914784ee0928cc96_QawAm8pZxsyI2H9zpvwx240uq1OrLDNXegNExL2IvgO8IB9hXrepIZmbXycpS88grM_cmRo9BKJrVwz-To55ltMZYIk3dvIpEdx0gEUlb0zUro4kS-6pZq_700_xkCdShYyUO7owODuUa152.avif)

- This is an API architecture style that uses remote procedure calls for API interaction
- Services expose functionalities as methods (clients can call them similar to local function calls)
- gRPC employs **Protocol** bufferes which is a language-neutral format for defining data structures and messages
- This supports single request, single response communication
- Supports for:
    - server streaming: continuous server updates
    - client streaming: sending stream of data
    - bi-directional streaming: real-time communication

- This is fast and efficient in data exchange, making this ideal for latency sensitive applications (suitable for scenarios where rapid data exchange is required)

