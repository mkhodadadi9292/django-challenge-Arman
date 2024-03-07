1) Work Queue Concept:
   - Work Queues (Task Queues) distribute time-consuming tasks among multiple workers.
   - Tasks are scheduled to be done later by sending them as messages to a queue.
   - Worker processes run in the background, popping tasks and executing them.
   - Useful for handling resource-intensive tasks asynchronously.
2) Round-Robin Dispatching:
   - Task Queues allow easy parallelization of work.
   - Multiple workers can be added to scale easily.
   - Messages are distributed in round-robin fashion by default.
3) Message Acknowledgment:
   - Message acknowledgments ensure that a message is fully processed before deletion.
   - If a worker terminates before completing a task, RabbitMQ re-queues the message.
   - Acknowledgment must be sent on the same channel that received the delivery.
4) Message Persistence:
   - To prevent message loss on RabbitMQ restart, mark both the queue and messages as durable.
   - Declare the queue as durable: `channel.queue_declare(queue='task_queue', durable=True)`
   - Mark messages as persistent: `delivery_mode = pika.DeliveryMode.Persistent`
5) Note on Message Persistence:
   - Marking messages as persistent doesn't guarantee no loss; there's a short time window.
   - RabbitMQ may not perform fsync(2) for every message, leading to potential cache saving.
6) Fair Dispatch:
   - By default, RabbitMQ dispatches messages evenly, regardless of worker load.
   - Use `channel.basic_qos(prefetch_count=1)` to limit one message to a worker at a time.
   - Helps distribute messages more evenly among workers.
