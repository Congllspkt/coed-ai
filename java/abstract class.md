
An `abstract class` in Java is a class that cannot be instantiated directly. It serves as a blueprint for other classes, providing a common interface and potentially some partial implementation for its subclasses. It's declared using the `abstract` keyword.

## Key Characteristics of an `abstract class`

1.  **Cannot be Instantiated:** You cannot create an object of an `abstract class` using the `new` keyword.
    *   `Mammal m = new Mammal();` // This would be a compile-time error if `Mammal` is abstract.

2.  **Can Contain Abstract Methods:** An `abstract class` can have one or more `abstract` methods. An `abstract` method is a method declared without an implementation (without a method body). Subclasses *must* provide an implementation for all inherited `abstract` methods, unless the subclass itself is declared `abstract`.
    *   `public abstract void makeSound();`

3.  **Can Contain Concrete (Non-Abstract) Methods:** An `abstract class` can also have regular, non-abstract methods with full implementations. These methods provide common functionality that all subclasses can inherit and use directly or override.

4.  **Can Contain Constructors:** `abstract class` can have constructors. These constructors are called by the constructors of their concrete subclasses using `super()`, allowing the abstract class to initialize its state.

5.  **Can Contain Instance Variables and Static Variables:** Just like regular classes, abstract classes can have fields (instance variables) and static variables.

6.  **Can Contain `final` and `static` Methods:** An `abstract class` can have `final` methods (which cannot be overridden by subclasses) and `static` methods.

7.  **Inheritance:** An abstract class can extend another class (abstract or concrete) and implement interfaces. A concrete class can only extend *one* abstract class but can implement *multiple* interfaces.

## When to Use an `abstract class`?

You should consider using an `abstract class` when:

1.  **You want to define a common interface and provide a partial implementation:** When several classes share a common set of behaviors and some of these behaviors can be implemented identically, while others need specific implementations for each subclass.
2.  **You want to enforce certain methods:** When you want to ensure that all concrete subclasses implement specific methods.
3.  **You need to define common fields/state:** When subclasses will share common instance variables or states.
4.  **You need constructors:** When you need to provide a constructor for the base class to initialize common state.
5.  **You have an "is-a" relationship but the base class isn't fully implementable:** For example, a `Shape` class might be abstract because a generic `Shape` can't be drawn, but a `Circle` or `Rectangle` can.

## Abstract Class vs. Interface

| Feature               | `abstract class`                                | `interface`                                            |
| :-------------------- | :---------------------------------------------- | :----------------------------------------------------- |
| **Instantiation**     | Cannot be instantiated                          | Cannot be instantiated                                 |
| **Methods**           | Can have abstract and concrete methods          | Pre-Java 8: All methods were implicitly abstract.      |
|                       |                                                 | Post-Java 8: Can have abstract, default, and static methods. Post-Java 9: Can have private methods. |
| **Variables**         | Can have instance (non-final) and static variables | Only `public static final` constants                   |
| **Constructors**      | Can have constructors                           | Cannot have constructors                               |
| **Inheritance**       | A class can extend only one abstract class      | A class can implement multiple interfaces              |
| **Access Modifiers**  | Can have any access modifier for members        | All members are implicitly `public` (except private methods in Java 9+) |
| **Purpose**           | Defines a common base for related classes, allowing for partial implementation and state. "is-a" relationship. | Defines a contract for behaviors. "can-do" or "has-a" capability. |

---

## Example: Animal Kingdom

Let's create an `abstract class` called `Mammal` and then two concrete subclasses: `Dog` and `Cat`.

### Scenario

We want to model different mammals. All mammals have a name and age, can eat, but they make different sounds and move in different ways.

### File Structure

```
├── src
│   ├── Mammal.java
│   ├── Dog.java
│   ├── Cat.java
│   └── AnimalShelter.java
```

### 1. `Mammal.java` (Abstract Class)

This class defines the common properties (`name`, `age`), a common method (`eat`), and abstract methods (`makeSound`, `move`) that *must* be implemented by its concrete subclasses.

```java
// src/Mammal.java
public abstract class Mammal {
    protected String name; // Protected so subclasses can access directly
    protected int age;

    // Constructor for the abstract class
    // Subclasses will call this using super()
    public Mammal(String name, int age) {
        this.name = name;
        this.age = age;
        System.out.println("LOG: A new Mammal object is being initialized: " + name);
    }

    // Concrete method (has a body, shared by all mammals)
    public void eat() {
        System.out.println(name + " is eating its food.");
    }

    // Abstract method (no body, must be implemented by concrete subclasses)
    public abstract void makeSound();

    // Another abstract method
    public abstract void move();

    // Concrete method to display info (shared by all mammals)
    public void displayInfo() {
        System.out.println("Name: " + name + ", Age: " + age + " years.");
    }
}
```

### 2. `Dog.java` (Concrete Subclass)

This class extends `Mammal` and provides concrete implementations for the `makeSound()` and `move()` abstract methods.

```java
// src/Dog.java
public class Dog extends Mammal {
    private String breed;

    // Dog's constructor, calls Mammal's constructor using super()
    public Dog(String name, int age, String breed) {
        super(name, age); // Calls public Mammal(String name, int age)
        this.breed = breed;
        System.out.println("LOG: Dog object created: " + name + " (" + breed + ")");
    }

    // Implementation of abstract method from Mammal
    @Override
    public void makeSound() {
        System.out.println(name + " barks: Woof! Woof!");
    }

    // Implementation of another abstract method from Mammal
    @Override
    public void move() {
        System.out.println(name + " runs on four legs.");
    }

    // Dog-specific method
    public void fetch() {
        System.out.println(name + " is fetching a ball.");
    }
}
```

### 3. `Cat.java` (Concrete Subclass)

This class also extends `Mammal` and provides its own unique implementations for the `makeSound()` and `move()` methods.

```java
// src/Cat.java
public class Cat extends Mammal {
    private boolean isHouseCat;

    // Cat's constructor, calls Mammal's constructor using super()
    public Cat(String name, int age, boolean isHouseCat) {
        super(name, age); // Calls public Mammal(String name, int age)
        this.isHouseCat = isHouseCat;
        System.out.println("LOG: Cat object created: " + name + " (HouseCat: " + isHouseCat + ")");
    }

    // Implementation of abstract method from Mammal
    @Override
    public void makeSound() {
        System.out.println(name + " meows: Meow! Purrrr.");
    }

    // Implementation of another abstract method from Mammal
    @Override
    public void move() {
        System.out.println(name + " stealthily pounces and climbs.");
    }

    // Cat-specific method
    public void purr() {
        System.out.println(name + " is purring contentedly.");
    }
}
```

### 4. `AnimalShelter.java` (Main Class for Demonstration)

This class demonstrates how to use the abstract class and its concrete subclasses, including polymorphism.

```java
// src/AnimalShelter.java
public class AnimalShelter {
    public static void main(String[] args) {
        System.out.println("--- Creating Animal Objects ---");

        // Create instances of concrete subclasses
        Dog myDog = new Dog("Buddy", 3, "Golden Retriever");
        Cat myCat = new Cat("Whiskers", 5, true);

        System.out.println("\n--- Interacting via Mammal (Polymorphism) ---");

        // You can use the abstract class type to refer to concrete objects
        Mammal animal1 = myDog; // Polymorphism in action
        Mammal animal2 = myCat; // Polymorphism in action

        System.out.println("\n--- Actions for animal1 (Buddy the Dog) ---");
        animal1.displayInfo(); // Concrete method from Mammal
        animal1.makeSound();   // Abstract method, Dog's implementation
        animal1.eat();         // Concrete method from Mammal
        animal1.move();        // Abstract method, Dog's implementation
        // animal1.fetch(); // Compile-time error: Mammal type does not have fetch() method

        System.out.println("\n--- Actions for animal2 (Whiskers the Cat) ---");
        animal2.displayInfo(); // Concrete method from Mammal
        animal2.makeSound();   // Abstract method, Cat's implementation
        animal2.eat();         // Concrete method from Mammal
        animal2.move();        // Abstract method, Cat's implementation
        // animal2.purr(); // Compile-time error: Mammal type does not have purr() method

        System.out.println("\n--- Specific actions (Casting or direct object) ---");
        // To call specific methods, you need to use the specific object type or cast
        myDog.fetch();
        myCat.purr();

        // This line would cause a compile-time error:
        // Mammal genericMammal = new Mammal("Generic Mammal", 10);
        // System.out.println("\nERROR: Cannot instantiate an abstract class!");
    }
}
```

### How to Compile and Run

1.  **Save:** Save all files in the `src` directory as shown above.
2.  **Navigate to `src` directory:** Open your terminal or command prompt and navigate to the `src` directory where your `.java` files are saved.
    ```bash
    cd path/to/your/project/src
    ```
3.  **Compile:** Compile all the Java files.
    ```bash
    javac Mammal.java Dog.java Cat.java AnimalShelter.java
    # Or, to compile all .java files in the current directory:
    # javac *.java
    ```
4.  **Run:** Run the `AnimalShelter` class.
    ```bash
    java AnimalShelter
    ```

### Expected Output

```
--- Creating Animal Objects ---
LOG: A new Mammal object is being initialized: Buddy
LOG: Dog object created: Buddy (Golden Retriever)
LOG: A new Mammal object is being initialized: Whiskers
LOG: Cat object created: Whiskers (HouseCat: true)

--- Interacting via Mammal (Polymorphism) ---

--- Actions for animal1 (Buddy the Dog) ---
Name: Buddy, Age: 3 years.
Buddy barks: Woof! Woof!
Buddy is eating its food.
Buddy runs on four legs.

--- Actions for animal2 (Whiskers the Cat) ---
Name: Whiskers, Age: 5 years.
Whiskers meows: Meow! Purrrr.
Whiskers is eating its food.
Whiskers stealthily pounces and climbs.

--- Specific actions (Casting or direct object) ---
Buddy is fetching a ball.
Whiskers is purring contentedly.
```

## Conclusion

Abstract classes are a powerful feature in Java for achieving abstraction and polymorphism. They allow you to define a common blueprint for related classes, enforce method implementations, and provide shared functionality while preventing direct instantiation of an incomplete base class. This helps in building robust, organized, and extensible object-oriented applications.