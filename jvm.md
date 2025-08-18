# Java Virtual Machine (JVM) - Complete Guide

## Table of Contents
1. [What is JVM?](#what-is-jvm)
2. [JVM Architecture](#jvm-architecture)
3. [JVM Components](#jvm-components)
4. [Memory Management](#memory-management)
5. [Garbage Collection](#garbage-collection)
6. [Class Loading](#class-loading)
7. [JIT Compilation](#jit-compilation)
8. [JVM Performance Tuning](#jvm-performance-tuning)
9. [JVM Monitoring Tools](#jvm-monitoring-tools)
10. [Best Practices](#best-practices)

## What is JVM?

The **Java Virtual Machine (JVM)** is a runtime environment that executes Java bytecode. It provides a platform-independent execution environment, enabling Java's "write once, run anywhere" capability.

### Key Features:
- **Platform Independence**: Java code runs on any system with a JVM
- **Memory Management**: Automatic memory allocation and garbage collection
- **Security**: Built-in security features and sandboxing
- **Performance Optimization**: Just-In-Time (JIT) compilation
- **Multi-threading Support**: Native support for concurrent execution

### JVM vs JRE vs JDK:
```
JDK (Java Development Kit) = JRE + Development Tools
JRE (Java Runtime Environment) = JVM + Standard Libraries
JVM (Java Virtual Machine) = Core execution engine
```

## JVM Architecture

The JVM architecture consists of several key components working together:

```
┌─────────────────────────────────────────────────────────┐
│                    JVM Architecture                     │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │ Class Loader│  │   Runtime   │  │   Native    │    │
│  │  Subsystem  │  │ Data Areas  │  │   Method    │    │
│  │             │  │             │  │ Interface   │    │
│  └─────────────┘  └─────────────┘  └─────────────┘    │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │            Execution Engine                     │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────────┐   │   │
│  │  │Interpreter│ │JIT Compiler│ │Garbage Collector│   │   │
│  │  └──────────┘ └──────────┘ └──────────────┘   │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## JVM Components

### 1. Class Loader Subsystem

The Class Loader is responsible for loading, linking, and initializing classes.

#### Types of Class Loaders:
- **Bootstrap Class Loader**: Loads core Java classes (rt.jar)
- **Extension Class Loader**: Loads extension classes from ext directory
- **Application Class Loader**: Loads application classes from classpath

#### Class Loading Process:
```java
// Example of class loading
public class ClassLoadingExample {
    public static void main(String[] args) {
        // This triggers class loading
        MyClass obj = new MyClass();
        
        // Get class loader information
        ClassLoader loader = obj.getClass().getClassLoader();
        System.out.println("Class Loader: " + loader);
    }
}
```

### 2. Runtime Data Areas

#### Method Area (Metaspace in Java 8+)
- Stores class-level data (metadata, constant pool, static variables)
- Shared among all threads
- Garbage collected in newer JVM versions

#### Heap Memory
- **Young Generation**:
  - Eden Space: Where new objects are created
  - Survivor Spaces (S0, S1): Objects that survive first GC
- **Old Generation**: Long-lived objects
- **Permanent Generation** (Java 7 and earlier): Class metadata

#### Stack Memory
- Thread-specific memory area
- Stores method call frames, local variables, partial results
- LIFO (Last In, First Out) structure

#### PC (Program Counter) Register
- Stores the address of currently executing instruction
- Thread-specific register

#### Native Method Stacks
- Used for native method calls (JNI)
- Platform-dependent implementation

### 3. Execution Engine

#### Interpreter
- Executes bytecode line by line
- Slower execution but quick startup

#### Just-In-Time (JIT) Compiler
- Compiles frequently used bytecode to native code
- Faster execution for hot spots

#### Garbage Collector
- Automatically manages memory
- Removes unreferenced objects

## Memory Management

### Heap Memory Structure

```
┌─────────────────────────────────────────────────┐
│                   Heap Memory                   │
├─────────────────────────────────────────────────┤
│              Young Generation                   │
│  ┌────────┐  ┌──────────┐  ┌──────────┐       │
│  │ Eden   │  │Survivor 0│  │Survivor 1│       │
│  │ Space  │  │  (S0)    │  │  (S1)    │       │
│  └────────┘  └──────────┘  └──────────┘       │
├─────────────────────────────────────────────────┤
│              Old Generation                     │
│  ┌─────────────────────────────────────────┐   │
│  │           Tenured Space                 │   │
│  └─────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

### Memory Allocation Process:
1. **New objects** created in Eden space
2. When Eden fills up, **minor GC** occurs
3. Surviving objects move to **Survivor space**
4. Objects surviving multiple GC cycles move to **Old Generation**
5. When Old Generation fills up, **major GC** occurs

### JVM Memory Parameters:
```bash
# Heap size configuration
java -Xms512m -Xmx2g MyApplication

# Young generation size
java -Xmn256m MyApplication

# Metaspace size (Java 8+)
java -XX:MetaspaceSize=128m -XX:MaxMetaspaceSize=512m MyApplication
```

## Garbage Collection

### Types of Garbage Collectors:

#### 1. Serial GC
```bash
java -XX:+UseSerialGC MyApplication
```
- Single-threaded
- Best for small applications
- Suitable for client-side applications

#### 2. Parallel GC (Default in Java 8)
```bash
java -XX:+UseParallelGC MyApplication
```
- Multi-threaded
- Good for throughput-focused applications
- Uses multiple threads for both minor and major GC

#### 3. CMS (Concurrent Mark Sweep)
```bash
java -XX:+UseConcMarkSweepGC MyApplication
```
- Low-latency collector
- Concurrent collection in Old Generation
- Deprecated in Java 9, removed in Java 14

#### 4. G1 (Garbage First)
```bash
java -XX:+UseG1GC MyApplication
```
- Low-latency collector for large heaps
- Predictable pause times
- Default in Java 9+

#### 5. ZGC (Z Garbage Collector)
```bash
java -XX:+UseZGC MyApplication
```
- Ultra-low latency collector
- Available from Java 11+
- Suitable for very large heaps

#### 6. Shenandoah
```bash
java -XX:+UseShenandoahGC MyApplication
```
- Low-pause collector
- Available from Java 12+

### GC Tuning Example:
```bash
# G1GC with custom settings
java -XX:+UseG1GC \
     -XX:MaxGCPauseMillis=200 \
     -XX:G1HeapRegionSize=16m \
     -XX:+G1PrintRegionRememberedSetInfo \
     MyApplication
```

## Class Loading

### Class Loading Phases:

#### 1. Loading
- Reads .class file and creates Class object
- Performed by ClassLoader

#### 2. Linking
- **Verification**: Checks bytecode validity
- **Preparation**: Allocates memory for static variables
- **Resolution**: Converts symbolic references to direct references

#### 3. Initialization
- Executes static initializers and static blocks

### Custom Class Loader Example:
```java
public class CustomClassLoader extends ClassLoader {
    @Override
    public Class<?> findClass(String name) throws ClassNotFoundException {
        byte[] classData = loadClassData(name);
        return defineClass(name, classData, 0, classData.length);
    }
    
    private byte[] loadClassData(String className) {
        // Implementation to load class bytes
        // from custom source (database, network, etc.)
        return new byte[0];
    }
}
```

## JIT Compilation

### How JIT Works:
1. **Interpretation**: Initially, bytecode is interpreted
2. **Profiling**: JVM identifies frequently executed code (hot spots)
3. **Compilation**: Hot spots are compiled to native code
4. **Optimization**: Native code is optimized for performance

### JIT Compiler Types:

#### C1 Compiler (Client)
- Fast compilation
- Basic optimizations
- Lower compilation overhead

#### C2 Compiler (Server)
- Aggressive optimizations
- Higher compilation overhead
- Better long-term performance

### JIT Configuration:
```bash
# Disable JIT compilation
java -Xint MyApplication

# Enable compilation details
java -XX:+PrintCompilation MyApplication

# Set compilation threshold
java -XX:CompileThreshold=1000 MyApplication
```

## JVM Performance Tuning

### Key Performance Parameters:

#### Heap Tuning:
```bash
# Initial and maximum heap size
java -Xms1g -Xmx4g MyApplication

# Young generation ratio
java -XX:NewRatio=3 MyApplication

# Survivor space ratio
java -XX:SurvivorRatio=8 MyApplication
```

#### GC Tuning:
```bash
# Parallel GC threads
java -XX:ParallelGCThreads=4 MyApplication

# GC overhead limit
java -XX:GCTimeRatio=19 MyApplication

# Adaptive size policy
java -XX:+UseAdaptiveSizePolicy MyApplication
```

#### Compilation Tuning:
```bash
# Tiered compilation
java -XX:+TieredCompilation MyApplication

# Compiler threads
java -XX:CICompilerCount=4 MyApplication
```

### Performance Monitoring:
```java
// Runtime information
Runtime runtime = Runtime.getRuntime();
long maxMemory = runtime.maxMemory();
long totalMemory = runtime.totalMemory();
long freeMemory = runtime.freeMemory();

System.out.println("Max Memory: " + maxMemory / (1024 * 1024) + " MB");
System.out.println("Total Memory: " + totalMemory / (1024 * 1024) + " MB");
System.out.println("Free Memory: " + freeMemory / (1024 * 1024) + " MB");
System.out.println("Used Memory: " + (totalMemory - freeMemory) / (1024 * 1024) + " MB");
```

## JVM Monitoring Tools

### Command Line Tools:

#### 1. jps (Java Process Status)
```bash
jps -l  # List running Java processes
```

#### 2. jstat (JVM Statistics)
```bash
jstat -gc [pid] 250ms  # GC statistics every 250ms
jstat -gcutil [pid]    # GC utilization
jstat -compiler [pid]  # Compilation statistics
```

#### 3. jmap (Memory Map)
```bash
jmap -heap [pid]           # Heap summary
jmap -dump:file=heap.hprof [pid]  # Heap dump
```

#### 4. jstack (Stack Trace)
```bash
jstack [pid]  # Thread dump
```

#### 5. jcmd (JVM Command)
```bash
jcmd [pid] VM.version      # JVM version
jcmd [pid] GC.run_finalization  # Run finalization
jcmd [pid] Thread.print    # Thread dump
```

### GUI Tools:

#### 1. JVisualVM
- Visual profiling and monitoring
- Heap dump analysis
- CPU and memory profiling

#### 2. JConsole
- MBean monitoring
- Real-time JVM statistics
- Built into JDK

#### 3. JProfiler
- Commercial profiling tool
- Advanced analysis capabilities

### JVM Flags for Monitoring:
```bash
# Enable GC logging
java -XX:+PrintGC -XX:+PrintGCDetails -XX:+PrintGCTimeStamps MyApplication

# Enable compilation logging
java -XX:+PrintCompilation -XX:+UnlockDiagnosticVMOptions -XX:+PrintInlining MyApplication

# Flight Recorder (Java 11+)
java -XX:+FlightRecorder -XX:StartFlightRecording=duration=60s,filename=app.jfr MyApplication
```

## Best Practices

### 1. Memory Management
```java
// Good practice: Proper resource management
try (FileInputStream fis = new FileInputStream("file.txt")) {
    // Use the stream
} catch (IOException e) {
    e.printStackTrace();
}

// Avoid memory leaks
List<String> list = new ArrayList<>();
// Clear collections when done
list.clear();
list = null;
```

### 2. Garbage Collection
- Choose appropriate GC algorithm for your use case
- Monitor GC logs and tune parameters
- Avoid creating unnecessary objects in loops

### 3. Performance Optimization
```java
// String concatenation in loops
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 1000; i++) {
    sb.append("Value: ").append(i).append("\n");
}
String result = sb.toString();

// Use object pools for expensive objects
ObjectPool<ExpensiveObject> pool = new ObjectPool<>();
```

### 4. Monitoring and Profiling
- Regularly monitor application performance
- Use profiling tools to identify bottlenecks
- Set up alerting for memory and GC issues

### 5. JVM Configuration
```bash
# Production-ready JVM configuration
java -server \
     -Xms2g -Xmx2g \
     -XX:+UseG1GC \
     -XX:MaxGCPauseMillis=200 \
     -XX:+PrintGC \
     -XX:+PrintGCDetails \
     -XX:+PrintGCTimeStamps \
     -XX:+HeapDumpOnOutOfMemoryError \
     -XX:HeapDumpPath=/path/to/dumps/ \
     MyApplication
```

## Common JVM Issues and Solutions

### 1. OutOfMemoryError
```bash
# Increase heap size
java -Xmx4g MyApplication

# Enable heap dump on OOM
java -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/tmp/ MyApplication
```

### 2. High GC Overhead
```bash
# Tune GC parameters
java -XX:+UseG1GC -XX:MaxGCPauseMillis=100 MyApplication
```

### 3. Memory Leaks
- Use memory profilers to identify leak sources
- Analyze heap dumps
- Review code for unclosed resources

### 4. Performance Issues
- Enable JIT compilation logging
- Profile CPU usage
- Optimize hot code paths

## Conclusion

The JVM is a sophisticated runtime environment that provides:
- **Platform independence** through bytecode execution
- **Automatic memory management** via garbage collection
- **Performance optimization** through JIT compilation
- **Security** through bytecode verification
- **Monitoring capabilities** for production environments

Understanding JVM internals is crucial for:
- Writing efficient Java applications
- Troubleshooting performance issues
- Optimizing application deployment
- Managing production environments effectively

---

*Last updated: August 2025*


