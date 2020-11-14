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

//javac -classpath ../javaparser/javaparser-core/target/classes/:. ./CodeSeq.java

public class CodeSeq {

  private static final String FILE_PATH = "./ReversePolishNotation.java";

  public static void main(String[] args) throws Exception {
    System.out.println("File\tClass\tMethod");
    ListAllJavaFiles("../..");
    // FileInputStream f = new FileInputStream(FILE_PATH);
    // CompilationUnit cu = StaticJavaParser.parse(f);

    // VoidVisitor<?> methodNameVisitor = new MethodNamePrinter();
    // methodNameVisitor.visit(cu, null);

  }

  private static class MethodNamePrinter extends VoidVisitorAdapter<Void> {
    @Override
    public void visit(ClassOrInterfaceDeclaration cl, Void arg) {
      super.visit(cl, arg);
      for (MethodDeclaration method : cl.getMethods()) {
        Range r = method.getRange().get();
        int loc = Math.max(r.begin.line, r.end.line) - Math.min(r.begin.line, r.end.line) + 1;
        System.out.println(FILE_PATH + "\t" + cl.getName() + "\t" + method.getName() + "\t" + loc);
      }
    }
  }

  public static void ListAllJavaFiles(String RootPath){
    try(Stream<Path> walk = Files.walk(Paths.get(RootPath))){
      List<String> result = walk.map(x -> x.toString()).filter(f->f.endsWith(".java")).collect(Collectors.toList());
      for(String FileName : result){
        System.out.println(FileName);
        FileInputStream f = new FileInputStream(FileName);
        try{
          CompilationUnit cu = StaticJavaParser.parse(f);
          VoidVisitor<?> methodNamePrinter = new MethodNamePrinter();
          methodNamePrinter.visit(cu, null);  
        }
        catch(ParseProblemException e){
          e.printStackTrace();
        }
      }
      // result.forEach(System.out::println);
    } catch(IOException e){
      e.printStackTrace();
    }
  }
}


