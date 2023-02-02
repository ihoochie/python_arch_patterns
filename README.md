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
