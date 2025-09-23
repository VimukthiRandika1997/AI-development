# REST

![image](https://cdn.prod.website-files.com/610d78d90f895fbe6aef8810/65d758bf5012935a3275c97f_-ah7zBY6okEhyyYUN1GH9NaHH9NB_67j6TXGvKqLhRNib4VUgrRoesmX7rI7cuWhhn6HOUhiDrUiDWtyA2npR_S0l8wQmaEMbUAUcQnFYGiFzASLZlFTIVMmAUXVy0iXYHS6gnHTq86V5Xzh.avif)

The REST (Representational State Transfer) architecture adhere to 6 principles

1. Separation—of the client (application requesting data) and the API server (providing data).
2. Statelessness—Each request sent by the client to the server must contain all the information needed for processing. 
3. Resource-based—REST APIs present data and functionality as resources accessible through URIs.
4. Uniform Interface—Consistent rules for how clients interact with server resources. 
5. Cacheable—Responses to requests should be cacheable by both the client and server as much as possible.
6. Layered system—The architecture allows for the presence of intermediaries like caches and load balancers between servers and clients

To access and manipulate resources, clients can use standard HTTP methods liek `GET`, `POST`, `PUT`, `DELETE`

- Each resource has a unique identifier
- Within the request `headers` and `parameters` can be included