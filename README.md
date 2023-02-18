# python_arch_patterns

Coding along while studying Architecture Patterns with Python by Harry J.W. Percival & Bob Gregory

### Introduction

A big ball of mud is the natural state of software similar to wilderness of a garden.  
It takes energy and direction to prevent the collapse.

Fortunately, the techniques to avoid it are not complex.  
They are:

* **Encapsulation and Abstraction**  
    We encapsulate behavior by identifying a task that needs to be done nd giving that task to a well-defined object or function. We call that object and _abstraction_.  
* **Layering**  
    We divide our code into categories or roles, and we introduce rules about how the different categories can interact.
* **The Dependency Inversion Principle (DIP, D from SOLID)**  
    1. High-level modules should not depend on low-level modules. Both should depend on abstractions.
    2. Abstractions should not depend on details. Details should depend on abstractions. 

    High-level modules are the code that your organization cares about. Low-level modules are the code that your organization doesn't care about. In other words, the business code shouldn't depend on technical details. Instead, both should depend on abstractions.

### Chapter 1: Domain Modeling

* When designing a new system, behavior should come first and drive our storage requirements.
* _Domain model_ from DDD is kind of substitution of term _business logic layer_ in three-layerd architecture.
* The _domain_ is a fancy way of saying _the problem you're trying to solve_.
* The domain is the set of activities that supported by business processes.
* A model is a map of proces that captures a useful property. It's the mental map that business owners have of their businesses.
* The terminology used by business stakeholders represents a distilled understanding of the domain model. Complex ideas and processes are boiled down to a single word or phrase. We should use that language writing our code.
* It's a good idea to stick to design principles of encapsulation and layering from the beginning even the domain is small and simple at the time. It will serve well later.
* A _Value Object_ is any domain object that uniquely identified by the data it holds. It has data, but no identity. We make them immutable.
* An _Entity_ is a domain object that has long-lived identity.
* Entities have _identity equality_. We can change attributes, but they still will stay the same things.
* Not everything has to be an object (at least in Python). It's often better to use functions instead.
* Domain Model is the best place to apply all good OO design principles.

### Chapter 2: Repository Pattern

* Repository Pattern is a simplifying abstraction over data storage
  * The domain model should be free of infrastructure concerns, ORM should import the model
  * The repository is like having a collection of in-memory objects
  * It's easier to test or swap detail of infrastructure
* ORM is already an abstraction, but for complex cases is not enough
* Ports and Adapter, Hexagonal/Onion/Clean architecture - pretty much the same thing relied on [DI Principle](https://blog.ploeh.dk/2013/12/03/layers-onions-ports-adapters-its-all-the-same/)
* The simplest repository has two methods: add() and get()

### Chapter 3: Coupling and Abstractions

* Locally, coupling is a good thing - cohesion
* Globally - it's bad. It increases the risk and the cost of changing the code.
* We can reduce the degree of coupling by abstracting away the details (I/O, infrastructure)
* Abstracting state aids testability
* Mocks does nothing to improve the design
* Tests with mocks tend to be more coupled to implementation details
* Overuse of mocks leads to complicated tests that don't explain the code
* What to read/watch:
  * https://martinfowler.com/articles/mocksArentStubs.html
  * https://dannorth.net/introducing-bdd/
  *  [Edwin Jung - Mocking and Patching Pitfalls - PyCon 2019](https://www.youtube.com/watch?v=Ldlz4V-UCFw)
  * [Talk: Harry Percival - Stop Using Mocks (for a while)](https://www.youtube.com/watch?v=rk-f3B-eMkI)
  * [Brandon Rhodes: Hoist Your I/O - PyWaw Summit 2015](https://www.youtube.com/watch?v=PBQN62oUnN8)

### Chapter 4: Service Layer

* It often makes sense to split out service layer (orchestration or use-case layer)
* Service layer provides and _application service_. Its job is to handle requests from the outside world and to orchestrate an operation.
* This layer _drives_ the application by doing simple steps like:
  * Get come data from database
  * Update the domain model
  * Persis any changes
* This is the kind of boring work that has to happen for every operation in the system, and keeping it separate from business logic.
* Pros of introducing Service Layer:
  * Single place to capture all the use cases
  * Domain logic is behind an API, which makes refactoring easier
  * Separate HTTP stuff from domain logic stuff
  * Writing test now easier on the higher level of abstraction, above domain
* It's not always needed. In some cases it's better to capture all the cases in controllers/views or push logic from controllers to domain model layer
* It's better to introduce this layer after spotting orchestration logic in controllers.


### Chapter 5: TDD in High Gear and Low Gear
* **The Shifting Gear Metaphor**: we need low gear in the beginning of movement (bike or car), then we go faster, so a higher gear is needed.  
  Same in projects: in the beginning write test on domain layer and then move it to service layer while the project grows. But if we need some design feedback, it's a good idea to lower "the gear" again.
* The more low-level (meaning related to implementation and not to abstractions) tests we have, the harder it will be to change things.
* But we can stick to low-level tests sometimes, because they could drive the design and trigger refactoring. 
* When we actually want to improve the design of the code, it's better to replace/delete low-level test, because they are coupled to a particular implementation.
* Hint: if we need to do something from Domain Layer while testing Service Layer, it could be a sign that the Service Layer is incomplete and misses some extra service.
* Rules of Thumb for tests
  * One E2E test per feature (happy path)
  * Most of the tests against the service layer (cover edge cases)
  * Keep a small core of the domain model tests (they have the highest feedback, but more coupled to implementation)
  * One Error Handler = One Feature (e2e unhappy paths). In the unit test there will be many unhappy paths.
* Service Layer should be expressed in terms of primitives (easier to test and maintain)
* Ideally, we should have all the service in Service Layer to test itself.


### Chapter 6: Unit of Work
* The Unit of Work pattern is a way to manage the persistence of domain objects.
* It's an abstraction over the idea of atomic operations
* UoW is a part of the service layer as a collaborator
* SqlAlchemy Session is a complex object, it could lead to data access code being spread across the application. UoW is a way to encapsulate it.
* "Don't mock what you don't own" is a rule of thumb that forces us to build simple abstractions over messy subsystems.
* Pros:
  * Nice abstracton over the concept of atomic operations grouped together (with context manager in Python)
  * Explicit control over when a transaction starts and finishes. It fails in a safe way by default
  * It's a nice place to put all the repositories so client code can access them
* Cons:
  * ORM probably already has a transaction management system. We can use it instead of UoW
  * We need to be careful with multithreading and nested transactions


### Chapter 7: Aggregates and Consistency Boundaries
* An aggregate is a cluster of domain objects that can be treated as a unit. It's like a public method in a class.
* We modify only one aggregate at a time.
* An aggregate is a consistency boundary. It's a place where we can enforce consistency rules.
* An aggregate is a place where we can enforce invariants.
* Aggregates and concurrency issues go together. We should think about transactions and locks.
* Dealing with eventual consistency between aggregates can be complex
* [Optimistic](https://martinfowler.com/eaaCatalog/optimisticOfflineLock.html) and [Pessimistic](https://martinfowler.com/eaaCatalog/pessimisticOfflineLock.html) locking - ways to deal with consistency
* Note on performance: 
  * Sometimes it's better to have a few aggregates with a lot of data than a lot of aggregates with a little data. It's easier to scale.
  * Example in the book: one query to read all the products and one query to persist data.


### Chapter 8: Events and the Message Bus
* Events can help with the single responsibility principle
* We use events for communication between aggregates
* A message bus routes messages to handlers. Message bus doesn't know anything about the meaning of events.
  * Option 1: Service layer raises events and passes them to message bys
  * Option 2: Domain model raises events, Service layer passes them to message bus (the logic when to raise an event should be in the domain model)
  * Option 3: UoW collects events from aggregates and passes them to message bus
* Pros:
  * A nice way to separate responsibilities when whe have multiple actions in response to a single request
  * Event handlers are decoupled from the "core" application logic
  * Domain events are a great way to model the real world
* Events are simple dataclasses. They dont have behavior.


### Chapter 9: Going to Town on the Message Bus
* Events are simple dataclasses that define data structures for inputs.
* Handlers are the way we react to events. They can call internal services, external services.
* We can define multiple handlers for the same event.
* Handler can also raise other events.
* Pros:
  * Handlers and services are the same thing - so it's simple.
  * Nice data structure for inputs
* Cons:
  * It's slightly unpredictable. You don't know when things are going to end.
  * Duplications of fields and structures between model objects and events - it adds maintenance cost.   
    Adding a new field to the model object means adding it to at least one of the event as well.
