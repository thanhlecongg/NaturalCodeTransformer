package transform.rules;

import org.eclipse.jdt.core.dom.*;
import org.eclipse.jdt.core.dom.rewrite.ASTRewrite;
import org.eclipse.jdt.core.dom.rewrite.ListRewrite;
import org.eclipse.jface.text.Document;
import org.eclipse.text.edits.TextEdit;
import transform.Utils;
import java.util.ArrayList;

public class Do2While extends ASTVisitor {
    CompilationUnit cu;
    Document document;
    String outputDirPath;
    ArrayList<Integer> targetLines;
    ArrayList<DoStatement> dosBin = new ArrayList<>();

    public Do2While(CompilationUnit cu_, Document document_, String outputDirPath_, ArrayList targetLines) {
        this.cu = cu_;
        this.document = document_;
        this.outputDirPath = outputDirPath_;
        this.targetLines = targetLines;
    }

    public boolean visit(DoStatement node) {
        if (Utils.checkTargetLines(targetLines, cu, node)) {
            dosBin.add(node);
        }
        return true;
    }

    @SuppressWarnings("unchecked")
    public void endVisit(CompilationUnit node) {
        if (dosBin.size() != 0) {
            AST ast = cu.getAST();
            ASTRewrite rewriter = ASTRewrite.create(ast);

            for (DoStatement doStmt : dosBin) {
                // Create a new while statement
                WhileStatement whileStmt = ast.newWhileStatement();
                whileStmt.setExpression((Expression) ASTNode.copySubtree(ast, doStmt.getExpression()));
                Block whileBody = ast.newBlock();

                // Create a new block for the statements before the while loop
                Block newBody = ast.newBlock();

                if (doStmt.getBody() instanceof Block) {
                    // Add the statements of the do-while body to the new body
                    newBody.statements().addAll(ASTNode.copySubtrees(ast, ((Block) doStmt.getBody()).statements()));
                    // Add the statements of the do-while body to the while body
                    whileBody.statements().addAll(ASTNode.copySubtrees(ast, ((Block) doStmt.getBody()).statements()));
                } else {
                    // Add the single statement of the do-while body to the new body
                    newBody.statements().add(ASTNode.copySubtree(ast, doStmt.getBody()));
                    // Add the single statement of the do-while body to the while body
                    whileBody.statements().add(ASTNode.copySubtree(ast, doStmt.getBody()));
                }

                whileStmt.setBody(whileBody);

                // Replace the do-while statement with the new body followed by the while statement
                ListRewrite listRewrite = rewriter.getListRewrite(doStmt.getParent(), Block.STATEMENTS_PROPERTY);
                listRewrite.insertBefore(newBody, doStmt, null);
                listRewrite.replace(doStmt, whileStmt, null);
            }

            TextEdit edits = rewriter.rewriteAST(document, null);
            Utils.applyRewrite(edits, document, outputDirPath);
        }
    }
}