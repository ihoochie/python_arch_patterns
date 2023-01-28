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
