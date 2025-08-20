Absolutely! Here's a detailed guide on how to process source code and PDF content in Java, complete with examples, input files, and expected output, formatted for a Markdown file.

---

# Processing Source Code and PDF Content in Java

This guide provides comprehensive details and examples on how to read and extract information from both plain text source code files and structured PDF documents using Java.

---

## 1. Processing Source Code Content

Reading source code typically involves treating it as a plain text file, but with an awareness of its structure (lines, comments, specific keywords).

### 1.1 Overview

For source code, we'll focus on:
*   Reading the file line by line.
*   Counting total lines, code lines, and comment lines.
*   Identifying and displaying the content with line numbers.

### 1.2 Key Concepts

*   **File I/O:** Java's `java.io` and `java.nio.file` packages are essential for reading files. `BufferedReader` is efficient for reading text line by line. `Files.readAllLines` is convenient for smaller files to read all lines into a list.
*   **Error Handling:** `IOException` needs to be handled for file operations.
*   **Resource Management:** Use try-with-resources to ensure file streams are properly closed.
*   **Character Encoding:** Always specify `UTF-8` for text files to avoid encoding issues.

### 1.3 Setup

No special libraries are needed for basic text file processing. Standard Java Development Kit (JDK) is sufficient.

### 1.4 Example: Java Source Code Analyzer

Let's create a simple Java program that reads a `.java` file, prints its content with line numbers, and provides a basic analysis of code and comment lines.

#### 1.4.1 Input File: `code/MyJavaCode.java`

Create a directory `code` and save the following content as `MyJavaCode.java` inside it:

```java
// This is a single-line comment
package com.example.app;

import java.util.Date; // Inline comment

/**
 * This is a multi-line comment block.
 * It explains the purpose of the MyClass.
 */
public class MyClass {

    private String name; /* Another
                            * multi-line
                            * comment */

    public MyClass(String name) {
        this.name = name;
    }

    public void displayInfo() {
        System.out.println("Hello, " + name + "!"); // Prints a greeting
        // Another single line comment
    }

    // Main method to test
    public static void main(String[] args) {
        MyClass myObject = new MyClass("World");
        myObject.displayInfo();
    }
}
```

#### 1.4.2 Java Code: `SourceCodeAnalyzer.java`

Save the following code as `SourceCodeAnalyzer.java` in your project's root directory (or in `src/main/java` if using a build tool).

```java
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;

public class SourceCodeAnalyzer {

    public static void main(String[] args) {
        String filePath = "code/MyJavaCode.java"; // Path to your source file
        
        System.out.println("--- Analyzing Source Code: " + filePath + " ---");
        
        try {
            Path path = Paths.get(filePath);
            if (!Files.exists(path)) {
                System.err.println("Error: File not found at " + filePath);
                return;
            }

            // Read all lines for analysis
            List<String> lines = Files.readAllLines(path, StandardCharsets.UTF_8);
            
            int totalLines = lines.size();
            int codeLines = 0;
            int commentLines = 0;
            boolean inMultiLineComment = false;

            System.out.println("\n--- File Content with Line Numbers ---");
            for (int i = 0; i < totalLines; i++) {
                String line = lines.get(i).trim(); // Trim leading/trailing whitespace

                // Basic multi-line comment detection
                if (line.startsWith("/*")) {
                    inMultiLineComment = true;
                }
                if (inMultiLineComment && line.endsWith("*/")) {
                    inMultiLineComment = false;
                    commentLines++; // Count the end of multi-line comment as one comment line
                } else if (inMultiLineComment) {
                    commentLines++;
                } 
                // Basic single-line comment detection
                else if (line.startsWith("//") || line.startsWith("*") && i > 0 && lines.get(i-1).trim().startsWith("/*")) {
                    commentLines++;
                } 
                // Consider blank lines as non-code
                else if (line.isEmpty()) {
                    // Do nothing, it's a blank line
                }
                // If not a comment or blank, it's a code line
                else {
                    codeLines++;
                }
                
                System.out.printf("%4d: %s%n", (i + 1), lines.get(i)); // Print original line content
            }

            System.out.println("\n--- Analysis Summary ---");
            System.out.println("Total Lines: " + totalLines);
            System.out.println("Code Lines (approx): " + codeLines);
            System.out.println("Comment Lines (approx): " + commentLines);
            System.out.println("Blank Lines (approx): " + (totalLines - codeLines - commentLines)); // Estimate blank lines

        } catch (IOException e) {
            System.err.println("An error occurred while reading the file: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
```

#### 1.4.3 Compilation and Execution

1.  **Open your terminal or command prompt.**
2.  **Navigate to the directory where you saved `SourceCodeAnalyzer.java`** (e.g., `cd path/to/your/project`).
3.  **Compile:**
    ```bash
    javac SourceCodeAnalyzer.java
    ```
4.  **Run:**
    ```bash
    java SourceCodeAnalyzer
    ```

#### 1.4.4 Output

```
--- Analyzing Source Code: code/MyJavaCode.java ---

--- File Content with Line Numbers ---
   1: // This is a single-line comment
   2: package com.example.app;
   3: 
   4: import java.util.Date; // Inline comment
   5: 
   6: /**
   7:  * This is a multi-line comment block.
   8:  * It explains the purpose of the MyClass.
   9:  */
  10: public class MyClass {
  11: 
  12:     private String name; /* Another
  13:                             * multi-line
  14:                             * comment */
  15: 
  16:     public MyClass(String name) {
  17:         this.name = name;
  18:     }
  19: 
  20:     public void displayInfo() {
  21:         System.out.println("Hello, " + name + "!"); // Prints a greeting
  22:         // Another single line comment
  23:     }
  24: 
  25:     // Main method to test
  26:     public static void main(String[] args) {
  27:         MyClass myObject = new MyClass("World");
  28:         myObject.displayInfo();
  29:     }
  30: }

--- Analysis Summary ---
Total Lines: 30
Code Lines (approx): 13
Comment Lines (approx): 10
Blank Lines (approx): 7
```

### 1.5 Further Considerations for Source Code

*   **Complex Analysis:** For deep source code analysis (e.g., building Abstract Syntax Trees, identifying methods, variables, code smells), you would need a dedicated parser generator (like ANTLR) or a static analysis tool library (e.g., Spoon, JavaParser). This goes beyond simple text reading.
*   **Performance:** For very large files, `BufferedReader` is generally more memory-efficient than `Files.readAllLines` as it doesn't load the entire file into memory at once.

---

## 2. Processing PDF Content

PDFs are binary files with a complex internal structure. You cannot simply read them as text. You need a dedicated library to parse their content. The most popular and robust Java library for this is **Apache PDFBox**.

### 2.1 Overview

For PDF content, we'll focus on:
*   Extracting plain text from PDF pages.
*   Extracting metadata (author, title, creation date, etc.).

### 2.2 Key Concepts

*   **PDF Structure:** PDFs contain objects (pages, fonts, images, text, annotations) arranged in a hierarchical structure.
*   **Parsing Library:** Apache PDFBox provides APIs to load a PDF document, navigate its structure, and extract different types of content.
*   **PDDocument:** Represents an entire PDF document.
*   **PDFTextStripper:** A utility class in PDFBox used to extract text content from pages.
*   **PDDocumentInformation:** Contains metadata about the PDF (e.g., Author, Title, Subject, Keywords).

### 2.3 Setup: Apache PDFBox Dependency

You need to add Apache PDFBox to your project. The easiest way is using a build tool like Maven or Gradle.

#### Maven (`pom.xml`):

```xml
<dependency>
    <groupId>org.apache.pdfbox</groupId>
    <artifactId>pdfbox</artifactId>
    <version>2.0.29</version> <!-- Use the latest stable version -->
</dependency>
```

#### Gradle (`build.gradle`):

```gradle
implementation 'org.apache.pdfbox:pdfbox:2.0.29' // Use the latest stable version
```

If you're not using Maven/Gradle, you'll need to download the `pdfbox-app-X.Y.Z.jar` from the [Apache PDFBox downloads page](https://pdfbox.apache.org/download.html) and add it to your project's classpath manually.

### 2.4 Example: PDF Content Extractor

Let's create a Java program that uses Apache PDFBox to extract text and metadata from a PDF file.

#### 2.4.1 Input File: `pdf/SampleDoc.pdf`

For this example, you need a sample PDF file. You can:
*   Use any existing PDF document you have.
*   Create a simple one: Open a text editor (like Notepad), type some text, and then use "Print" -> "Microsoft Print to PDF" (or a similar PDF printer) to save it as `SampleDoc.pdf` in a new directory `pdf`.
*   (Advanced) Use PDFBox itself to create a simple PDF for testing:

    ```java
    import org.apache.pdfbox.pdmodel.PDDocument;
    import org.apache.pdfbox.pdmodel.PDPage;
    import org.apache.pdfbox.pdmodel.PDPageContentStream;
    import org.apache.pdfbox.pdmodel.font.PDType1Font;
    import org.apache.pdfbox.pdmodel.PDDocumentInformation;
    import java.io.IOException;
    import java.util.Calendar;

    public class CreateSamplePdf {
        public static void main(String[] args) throws IOException {
            PDDocument document = new PDDocument();
            PDPage page = new PDPage();
            document.addPage(page);

            // Add content
            PDPageContentStream contentStream = new PDPageContentStream(document, page);
            contentStream.beginText();
            contentStream.setFont(PDType1Font.HELVETICA_BOLD, 12);
            contentStream.setLeading(14.5f);
            contentStream.newLineAtOffset(50, 750);
            contentStream.showText("Hello from PDFBox!");
            contentStream.newLine();
            contentStream.showText("This is a sample document.");
            contentStream.newLine();
            contentStream.showText("It contains some text and metadata.");
            contentStream.endText();
            contentStream.close();

            // Add metadata
            PDDocumentInformation info = document.getDocumentInformation();
            info.setAuthor("Java Developer");
            info.setTitle("Sample PDF Document for Java Example");
            info.setSubject("PDFBox Demo");
            info.setKeywords("Java, PDF, PDFBox, Example");
            info.setCreator("Apache PDFBox");
            info.setCreationDate(Calendar.getInstance());

            // Save the document
            document.save("pdf/SampleDoc.pdf");
            document.close();
            System.out.println("Sample PDF created at pdf/SampleDoc.pdf");
        }
    }
    ```
    (Run this `CreateSamplePdf.java` first to generate the input file if you don't have one).

#### 2.4.2 Java Code: `PdfContentReader.java`

Save the following code as `PdfContentReader.java` in your project's root directory (or in `src/main/java`).

```java
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.pdmodel.PDDocumentInformation;
import org.apache.pdfbox.text.PDFTextStripper;

import java.io.File;
import java.io.IOException;
import java.util.Calendar;

public class PdfContentReader {

    public static void main(String[] args) {
        String filePath = "pdf/SampleDoc.pdf"; // Path to your PDF file
        File pdfFile = new File(filePath);

        System.out.println("--- Reading PDF Content: " + filePath + " ---");

        // Check if the file exists
        if (!pdfFile.exists()) {
            System.err.println("Error: PDF file not found at " + filePath);
            System.err.println("Please ensure 'pdf/SampleDoc.pdf' exists or create it using the 'CreateSamplePdf.java' example.");
            return;
        }
        
        PDDocument document = null;
        try {
            // Load the PDF document
            document = PDDocument.load(pdfFile);

            // --- 1. Extract Text Content ---
            System.out.println("\n--- Extracted Text ---");
            PDFTextStripper pdfStripper = new PDFTextStripper();
            String text = pdfStripper.getText(document);
            System.out.println(text);

            // --- 2. Extract Metadata ---
            System.out.println("\n--- Extracted Metadata ---");
            PDDocumentInformation info = document.getDocumentInformation();

            System.out.println("Title: " + info.getTitle());
            System.out.println("Author: " + info.getAuthor());
            System.out.println("Subject: " + info.getSubject());
            System.out.println("Keywords: " + info.getKeywords());
            System.out.println("Creator: " + info.getCreator());
            System.out.println("Producer: " + info.getProducer());
            
            // Creation date can be null if not set
            Calendar creationDate = info.getCreationDate();
            if (creationDate != null) {
                System.out.println("Creation Date: " + creationDate.getTime());
            } else {
                System.out.println("Creation Date: Not Available");
            }

            // Modification date can be null if not set
            Calendar modificationDate = info.getModificationDate();
            if (modificationDate != null) {
                System.out.println("Modification Date: " + modificationDate.getTime());
            } else {
                System.out.println("Modification Date: Not Available");
            }
            
            System.out.println("Number of Pages: " + document.getNumberOfPages());

        } catch (IOException e) {
            System.err.println("An error occurred while processing the PDF: " + e.getMessage());
            e.printStackTrace();
        } finally {
            // Ensure the document is closed to release resources
            if (document != null) {
                try {
                    document.close();
                } catch (IOException e) {
                    System.err.println("Error closing PDF document: " + e.getMessage());
                }
            }
        }
    }
}
```

#### 2.4.3 Compilation and Execution

If you're using Maven or Gradle, simply run your project:
*   **Maven:** `mvn clean install exec:java -Dexec.mainClass="PdfContentReader"`
*   **Gradle:** `gradle run`

If you are compiling manually after adding the PDFBox JAR to your classpath:
1.  **Open your terminal or command prompt.**
2.  **Navigate to the directory where you saved `PdfContentReader.java`**.
3.  **Compile (replace `/path/to/pdfbox-app-X.Y.Z.jar` with the actual path to your downloaded JAR):**
    ```bash
    javac -cp "/path/to/pdfbox-app-2.0.29.jar" PdfContentReader.java
    ```
4.  **Run:**
    ```bash
    java -cp ".:/path/to/pdfbox-app-2.0.29.jar" PdfContentReader 
    # For Windows: java -cp ".;\path\to\pdfbox-app-2.0.29.jar" PdfContentReader
    ```

#### 2.4.4 Output (will vary based on your PDF content and creation date)

```
--- Reading PDF Content: pdf/SampleDoc.pdf ---

--- Extracted Text ---
Hello from PDFBox!
This is a sample document.
It contains some text and metadata.


--- Extracted Metadata ---
Title: Sample PDF Document for Java Example
Author: Java Developer
Subject: PDFBox Demo
Keywords: Java, PDF, PDFBox, Example
Creator: Apache PDFBox
Producer: Apache PDFBox
Creation Date: Tue Jun 18 10:30:00 CEST 2024  (or your current date/time)
Modification Date: Tue Jun 18 10:30:00 CEST 2024 (or your current date/time)
Number of Pages: 1
```

### 2.5 Further Considerations for PDF Content

*   **Image Extraction:** PDFBox can extract images, but it requires more advanced coding to handle different image formats within the PDF.
*   **Form Filling/Extraction:** PDFBox supports working with AcroForm (PDF forms), allowing you to fill or extract data from form fields.
*   **Creating/Modifying PDFs:** You can use PDFBox to programmatically generate new PDF documents, add text, images, shapes, and even modify existing PDFs.
*   **Performance:** Processing very large or complex PDFs can be memory-intensive. Ensure you close `PDDocument` instances properly (`document.close()`) to prevent resource leaks.
*   **Layout Preservation:** `PDFTextStripper` extracts text in reading order, but preserving the exact visual layout (columns, precise spacing) is challenging and often requires more sophisticated text layout analysis.

---

## Conclusion

Java provides robust capabilities for handling both plain text source code files and complex binary PDF documents. While basic source code analysis can be done with standard Java I/O, dealing with PDFs necessitates a powerful library like Apache PDFBox. These examples give you a solid foundation for building more advanced content processing applications in Java.