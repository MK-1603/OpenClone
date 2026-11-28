/**
 * Editor & Workspace Context Extractor for VS Code Extension.
 * Extracts active file, selection, syntax language, and relative path.
 */
const vscode = require('vscode');
const path = require('path');

class ContextManager {
    static getActiveEditorContext() {
        const editor = vscode.window.activeTextEditor;
        if (!editor || !editor.document) {
            return {
                hasActiveEditor: false,
                activeFile: null,
                fileName: null,
                language: null,
                selection: null,
                lineCount: 0,
                startLine: null,
                endLine: null
            };
        }

        const document = editor.document;
        const selection = editor.selection;
        let selectedText = '';

        if (!selection.isEmpty) {
            selectedText = document.getText(selection);
        }

        // Relative path calculation
        let relativePath = document.fileName;
        const workspaceFolder = vscode.workspace.getWorkspaceFolder(document.uri);
        if (workspaceFolder) {
            relativePath = path.relative(workspaceFolder.uri.fsPath, document.fileName);
        }

        return {
            hasActiveEditor: true,
            activeFile: relativePath,
            fullPath: document.fileName,
            fileName: path.basename(document.fileName),
            language: document.languageId,
            selection: selectedText || null,
            lineCount: document.lineCount,
            startLine: selection.isEmpty ? null : selection.start.line + 1,
            endLine: selection.isEmpty ? null : selection.end.line + 1,
            isDirty: document.isDirty
        };
    }

    static getSelectionOrFullText() {
        const editor = vscode.window.activeTextEditor;
        if (!editor || !editor.document) {
            return null;
        }
        const selection = editor.selection;
        if (!selection.isEmpty) {
            return editor.document.getText(selection);
        }
        return editor.document.getText();
    }
}

module.exports = { ContextManager };
