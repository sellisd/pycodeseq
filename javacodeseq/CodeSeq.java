import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.body.ClassOrInterfaceDeclaration;
import com.github.javaparser.ast.visitor.VoidVisitor;
import com.github.javaparser.ast.Node;
import com.github.javaparser.Range;
import com.github.javaparser.ParseProblemException;

import java.io.FileInputStream;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import java.lang.Math;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;

// javac -classpath ../../javaparser/javaparser-core/target/classes/:. ./CodeSeq.java 
// java -cp ../../javaparser/javaparser-core/target/classes/:. CodeSeq


public class CodeSeq {

  /** private static String outputFilePath = "./java_data.tsv";*/

   public static void main(String[] args) throws Exception {
    String outputFilePath = "./java_data.tsv";
    String RootPath = "/mnt/Data/scratch/github_java";
    try{
      FileWriter outputFile = new FileWriter(outputFilePath);
      outputFile.write("class\tclass_lines\tmethod\tmethod_lines\n");
      try(Stream<Path> walk = Files.walk(Paths.get(RootPath))){
        List<String> result = walk.map(x -> x.toString()).filter(f -> f.endsWith(".java")).collect(Collectors.toList());
        for (String fileName : result) {
          Path fileNamePath = Paths.get(fileName);
          if (Files.isRegularFile(fileNamePath)) {
            FileInputStream f = new FileInputStream(fileName);
            try {
              CompilationUnit cu = StaticJavaParser.parse(f);
              VoidVisitor<FileWriter> methodNamePrinter = new MethodNamePrinter();
              methodNamePrinter.visit(cu, outputFile);
            } catch (ParseProblemException e) {
              System.out.println("Skipping file: " + fileName);
            }
          }
        }
        outputFile.close();
      } catch(IOException e){
        e.printStackTrace();
      }
    }catch(IOException ex){
      System.out.println("Error writing to file");
      ex.printStackTrace();
    }
  }

  private static class MethodNamePrinter extends VoidVisitorAdapter<FileWriter> {
    @Override
    public void visit(ClassOrInterfaceDeclaration cl, FileWriter arg) {
      super.visit(cl, arg);
    Range class_range = cl.getRange().get();
    int class_loc = Math.max(class_range.begin.line, class_range.end.line) - Math.min(class_range.begin.line, class_range.end.line) + 1;
    for (MethodDeclaration method : cl.getMethods()) {
        Range r = method.getRange().get();
        int loc = Math.max(r.begin.line, r.end.line) - Math.min(r.begin.line, r.end.line) + 1;
        try{
          arg.write(cl.getName() + "\t" + class_loc + "\t" + method.getName() + "\t" + loc + "\n");
        }catch(IOException ex){
          System.out.println("Error writing to file");
        }
      }
    }
  }


  }


