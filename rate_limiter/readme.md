# Rate Limiter Project

## Rate Limiter Algorithms:

- **Token Bucket**:
  - A bucket that is initialised with n tokens and refills at a rate of k tokens per second (until the bucket reaches it's capacity n). If the tokens available are zero then the request is rejected, if not, then one is minused from the available tokens and the request is accepted.

- **Leaky Bucket**:
  - A bucket that is initialised with zero requests, a maximum capacity of n and 'leaks' at a rate of k requests per second (until the bucket returns to zero). If a request is sent and the bucket is at its capacity the request is rejected, otherwise a new token is added to the bucket and the request is accepted.

- **Fixed Window Counter**:
  - A window is set to span a particular time period (say a minute), at the start of every window a quota of n requests are allowed. All requests are accepted until the quote is met and then all requests are rejected until the next window begins and the quota resets.

- **Sliding Window Counter**:
  - At any point in time we have a capacity of n requests that we will allow. We will split our time into windows of size t. When calculating the total number of requests that have been received that will count towards our capacity, we find out first what % of the way through the current window we are _(now - window_start)/t_. We then take the remainder of time we have left in the window, get the total number of requests from the previous window multiplied by that ratio and add it to the number of requests received during the current window. If greater than or equal to the capacity, reject the request, otherwise, accept it.

- **Sliding Window Log**:
  - We record all the requests we accept within the last window of time t. When receiving a new request, remove any old requests we accepted that have since fallen out of that time window. Accept the request if we are now below our capacity n, if accepting, add the current timestamp to the end of the queue.
