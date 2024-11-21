package transform;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import org.eclipse.jdt.core.JavaCore;
import org.eclipse.jdt.core.dom.AST;
import org.eclipse.jdt.core.dom.ASTParser;
import org.eclipse.jdt.core.dom.CompilationUnit;
import org.eclipse.jface.text.Document;
import org.apache.commons.cli.*;

import java.io.*;
import java.lang.reflect.Type;
import java.util.*;
import java.util.concurrent.*;

public class Main {

    public static void parseFilesInDir(String outputDir, String ruleId, List<CodeInstance> projects) {
        ExecutorService executorService = Executors.newFixedThreadPool(4);

        List<Future<String>> futures = new ArrayList<>();
        // Submit tasks for each object in the list
        for (CodeInstance project : projects) {
            System.out.println("Processing: " + project.getInstanceId());
            ObjectProcessor task = new ObjectProcessor(project, outputDir, ruleId);
            Future<String> future = executorService.submit(task);
            futures.add(future);
        }

        // Process the results
        for (Future<String> future : futures) {
            try {
                String result = future.get();
            } catch (InterruptedException | ExecutionException e) {
                // Handle exceptions
            }
        }

        // Shutdown the ExecutorService
        executorService.shutdown();
    }

    public static void main(String[] args) {

        Options options = new Options();
        System.out.println("Code Transform");
        Option outputDirOption = new Option("o", "outputDir", true, "output directory");
        outputDirOption.setRequired(true);
        options.addOption(outputDirOption);

        Option ruleIdOption = new Option("r", "ruleId", true, "rule ID");
        ruleIdOption.setRequired(true);
        options.addOption(ruleIdOption);

        Option infoDirOption = new Option("f", "infoDir", true, "info directory");
        infoDirOption.setRequired(true);
        options.addOption(infoDirOption);

        CommandLineParser parser = new DefaultParser();
        HelpFormatter formatter = new HelpFormatter();
        CommandLine cmd;

        try {
            cmd = parser.parse(options, args);
        } catch (ParseException e) {
            System.out.println(e.getMessage());
            formatter.printHelp("utility-name", options);

            System.exit(1);
            return;
        }

        String outputDir = cmd.getOptionValue("outputDir");
        String ruleId = cmd.getOptionValue("ruleId");
        String infoDir = cmd.getOptionValue("infoDir");
        
        File file = new File(outputDir);
        if (!file.exists()) {
            file.mkdirs();
        }
        
        try (Reader reader = new FileReader(infoDir)) {
            Gson gson = new Gson();
            Type listType = new TypeToken<List<CodeInstance>>() {}.getType();
            List<CodeInstance> projects = gson.fromJson(reader, listType);
            parseFilesInDir(outputDir, ruleId, projects);
        } catch (FileNotFoundException e) {
            throw new RuntimeException(e);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}

class ObjectProcessor implements Callable<String> {
    private final CodeInstance project;
    private final String outputDir;
    private final String ruleId;

    public ObjectProcessor(CodeInstance project, String outputDir, String ruleId) {
        this.project = project;
        this.outputDir = outputDir;
        this.ruleId = ruleId;
    }

    public CodeInstance getProject() {
        return project;
    }

    // TODO: Add support for multiple target lines
    public static void parse(String code, String outputDir, String ruleId, ArrayList<Integer> targetLines) {
        System.out.println("Parsing code...");
        // Initialize a parser with JLS13 AST (Java 13)
        ASTParser parser = ASTParser.newParser(AST.JLS13);

        // Resolve binding
        parser.setResolveBindings(true);

        // Set kind of parser at compilation unit level
        parser.setKind(ASTParser.K_COMPILATION_UNIT);

        // Allow binding recovery
        parser.setBindingsRecovery(true);

        // Get default compiler options and set them as parser options
        Map<String, String> options = JavaCore.getOptions();
        parser.setCompilerOptions(options);

        String unitName = "Unit.java"; // Just some random name
        parser.setUnitName(unitName);

        // This code for setting environment. But we do not need for now
        String[] sources = {""}; // Just the file itself
        String[] classpath = {""};
        parser.setEnvironment(classpath, sources, new String[] { "UTF-8" }, true);

        parser.setSource(code.toCharArray());
        CompilationUnit cu = (CompilationUnit) parser.createAST(null);

        // Create a document object of code
        Document document = new Document(code);
        cu.accept(RuleSelector.create(ruleId, cu, document, outputDir, targetLines));
    }

    @Override
    public String call() throws Exception {
        File targetFile = new File(project.getSourceFile());
        System.out.println("Processing: " + project.getInstanceId());

        String filePath = targetFile.getAbsolutePath();
        System.out.println("File path: " + filePath);
        // TODO: Add support for multiple target lines
        ArrayList<Integer> targetLines = new ArrayList<>();
        for (Integer line : project.getTargetLines()) {
            targetLines.add(line);
        }

        if (targetFile.isFile()) {
            try {
                // Read code from current file
                String codeOfCurrentFile = Utils.readFileToString(filePath);

                // Output file
                String outputFile = Utils.sublizeOutput(filePath, outputDir);

                // Parse current file
                parse(codeOfCurrentFile, outputFile, ruleId, targetLines);

            } catch (Exception e) {
                e.printStackTrace();
                System.out.println("Transformation failed: " + filePath);
            } catch (Error s) {
                s.printStackTrace();
                System.out.println("Transformation failed: " + s.toString());
            }
        }
        return "Processed: " + project.getInstanceId();
    }
}

class CodeInstance {
    private String instanceId;
    private String sourceFile;
    private List<Integer> targetLines;
    private int methodStartLine;
    private int methodEndLine;

    public String getInstanceId() {
        return instanceId;
    }

    public void setInstanceId(String instanceId) {
        this.instanceId = instanceId;
    }

    public String getSourceFile() {
        return sourceFile;
    }

    public void setSourceFile(String sourceFile) {
        this.sourceFile = sourceFile;
    }

    public List<Integer> getTargetLines() {
        return targetLines;
    }

    public void setTargetLines(List<Integer> targetLines) {
        this.targetLines = targetLines;
    }

    public int getMethodStartLine() {
        return methodStartLine;
    }

    public void setMethodStartLine(int methodStartLine) {
        this.methodStartLine = methodStartLine;
    }

    public int getMethodEndLine() {
        return methodEndLine;
    }

    public void setMethodEndLine(int methodEndLine) {
        this.methodEndLine = methodEndLine;
    }

    @Override
    public String toString() {
        return "{" +
                "instanceId: '" + this.instanceId + ", " +
                "sourceFile: '" + this.sourceFile + ", " +
                "lineNumber: '" + this.targetLines.get(0) + ", " +
                '}';
    }
}
