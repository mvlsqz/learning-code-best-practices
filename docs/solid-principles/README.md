# SOLID Principles

A comprehensive guide to the 5 SOLID principles of object-oriented design, with practical examples and real-world applications.

## 📚 The Principles

### [1. Single Responsibility Principle (SRP)](./01-srp.md)
**"A class should have one, and only one, reason to change."**

Each class should do ONE thing and do it well. This makes code easier to understand, test, and maintain.

**Key takeaway**: If you can't name a class without using "and" or "or", it probably has too many responsibilities.

---

### [2. Open/Closed Principle (OCP)](./02-ocp.md)
**"Software entities should be open for extension but closed for modification."**

You should be able to add new functionality without modifying existing code. Use abstractions and interfaces to create extension points.

**Key takeaway**: Write code that can grow without changing what already works.

---

### [3. Liskov Substitution Principle (LSP)](./03-lsp.md)
**"Objects of a superclass should be replaceable with objects of a subclass without breaking the application."**

Subtypes must be fully substitutable for their base types. If it says it's a duck, it should quack like a duck.

**Key takeaway**: Don't break the contract. Implementations must honor their interface's promises.

---

### [4. Interface Segregation Principle (ISP)](./04-isp.md)
**"No client should be forced to depend on methods it does not use."**

Keep interfaces small and focused. It's better to have many specific interfaces than one large, general-purpose interface.

**Key takeaway**: Don't force clients to depend on things they don't need.

---

### [5. Dependency Inversion Principle (DIP)](./05-dip.md)
**"Depend upon abstractions, not concretions."**

High-level modules should not depend on low-level modules. Both should depend on abstractions. Inject dependencies instead of creating them.

**Key takeaway**: Code to interfaces, not implementations. Use dependency injection.

---

## 🎯 Quick Reference

| Principle | Question to Ask | Red Flag |
|-----------|----------------|----------|
| **SRP** | Does this class have multiple reasons to change? | Large classes, mixing concerns |
| **OCP** | Can I add features without modifying existing code? | Modifying classes for every new feature |
| **LSP** | Can I swap this implementation without breaking things? | Type checking, unexpected behavior |
| **ISP** | Am I forced to implement methods I don't need? | Empty implementations, "not supported" errors |
| **DIP** | Am I depending on concrete implementations? | Creating dependencies internally, hard to test |

## 📖 Learning Path

**Recommended Order:**
1. Start with **SRP** - It's the most intuitive and immediately applicable
2. Move to **DIP** - It enables testability and flexibility
3. Study **OCP** - Understanding extension points is crucial
4. Learn **LSP** - Ensures your abstractions actually work
5. Finish with **ISP** - Refines your interface design

## 🛠️ Practical Application

See the **Task Manager CLI** project for a complete implementation demonstrating all 5 principles:
- [Python Implementation](../../projects/01-task-manager-cli/python/)
- [SOLID Principles Explanation](../../projects/01-task-manager-cli/python/SOLID_PRINCIPLES.md)

## 💡 Key Insights

### SOLID Principles Work Together

- **SRP** creates focused classes
- **OCP** makes them extensible
- **LSP** ensures substitutability
- **ISP** keeps interfaces clean
- **DIP** inverts dependencies for flexibility

### Trade-offs

SOLID principles are **guidelines, not rigid rules**:
- They add upfront complexity
- They make code more maintainable long-term
- They're most valuable in larger, evolving systems
- They can be over-applied to simple code

### When to Apply

**Good scenarios:**
- Production code that will be maintained
- Code that's likely to change or grow
- Team projects with multiple developers
- Building frameworks or libraries

**Consider skipping:**
- Quick prototypes or spike solutions
- Very simple scripts (<100 lines)
- Throwaway code
- When performance overhead matters more than maintainability

## 🔗 Additional Resources

### Books
- "Clean Code" by Robert C. Martin (Uncle Bob)
- "Clean Architecture" by Robert C. Martin
- "Design Patterns" by Gang of Four

### Online
- [refactoring.guru - SOLID Principles](https://refactoring.guru/design-patterns/solid)
- [Uncle Bob's Blog](http://blog.cleancoder.com/)
- [SOLID Principles Explained with Code](https://stackify.com/solid-design-principles/)

## 🎓 Practice Tips

1. **Read real code**: Look at well-designed open-source projects
2. **Refactor deliberately**: Take existing code and apply one principle at a time
3. **Write tests first**: SOLID code is testable code
4. **Get feedback**: Have others review your designs
5. **Know the why**: Understand not just how, but why each principle matters

## 📝 Summary

The SOLID principles guide you toward code that is:
- ✅ **Maintainable** - Easy to understand and modify
- ✅ **Testable** - Can be tested in isolation
- ✅ **Flexible** - Can adapt to changing requirements
- ✅ **Robust** - Less likely to break when extended

Master these principles, and you'll write better object-oriented code. But remember: they're tools, not rules. Use judgment to apply them appropriately for your context.

---

**Remember**: Perfect is the enemy of good. Aim for "good enough" SOLID design, not perfect adherence to every principle in every line of code.
