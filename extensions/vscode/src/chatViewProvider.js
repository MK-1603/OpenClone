/**
 * OpenClone Webview Chat View Provider.
 * Implements vscode.WebviewViewProvider for the Activity Bar native sidebar panel.
 */
const vscode = require('vscode');
const path = require('path');
const fs = require('fs');
const { ContextManager } = require('./contextManager');

class OpenCloneChatViewProvider {
    constructor(extensionUri, runtimeClient) {
        this._extensionUri = extensionUri;
        this._runtimeClient = runtimeClient;
        this._view = null;
        this._selectedModel = null;
        this._selectedAgent = null;
        this._isGenerating = false;
    }

    resolveWebviewView(webviewView, context, _token) {
        this._view = webviewView;

        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [
                this._extensionUri,
                vscode.Uri.joinPath(this._extensionUri, 'media')
            ]
        };

        webviewView.webview.html = this._getHtmlForWebview(webviewView.webview);

        // Handle incoming messages from the Webview script
        webviewView.webview.onDidReceiveMessage(async (data) => {
            switch (data.type) {
                case 'init':
                    await this._handleInit();
                    break;
                case 'sendMessage':
                    await this._handleSendMessage(data.message, data.includeContext);
                    break;
                case 'selectModel':
                    this._selectedModel = data.modelId;
                    break;
                case 'selectAgent':
                    this._selectedAgent = data.agentRole;
                    break;
                case 'quickAction':
                    await this._handleQuickAction(data.action, data.context);
                    break;
                case 'respondApproval':
                    await this._handleApprovalResponse(data.digest, data.action);
                    break;
                case 'clearConversation':
                    await this._handleClearConversation();
                    break;
                case 'checkHealth':
                    await this._updateHealthStatus();
                    break;
                case 'openFile':
                    if (data.filePath) {
                        const doc = await vscode.workspace.openTextDocument(data.filePath);
                        await vscode.window.showTextDocument(doc);
                    }
                    break;
            }
        });

        // Trigger initial status check
        setTimeout(() => this._handleInit(), 500);
    }

    async _handleInit() {
        if (!this._view) return;

        // 1. Health check
        const health = await this._runtimeClient.checkHealth();
        this._view.webview.postMessage({
            type: 'healthUpdate',
            healthy: health.status === 'healthy',
            workspace: health.workspace || '',
            gitBranch: health.git_branch || 'main'
        });

        // 2. Load models
        try {
            const modelsData = await this._runtimeClient.getModels();
            if (modelsData && modelsData.models) {
                this._view.webview.postMessage({
                    type: 'modelsList',
                    models: modelsData.models
                });
            }
        } catch (e) {
            console.error('Failed to load models:', e);
        }

        // 3. Load agents
        try {
            const agentsData = await this._runtimeClient.getAgents();
            if (agentsData && agentsData.agents) {
                this._view.webview.postMessage({
                    type: 'agentsList',
                    agents: agentsData.agents
                });
            }
        } catch (e) {
            console.error('Failed to load agents:', e);
        }

        // 4. Update editor context badge
        this.updateContextIndicator();
    }

    updateContextIndicator() {
        if (!this._view) return;
        const ctx = ContextManager.getActiveEditorContext();
        this._view.webview.postMessage({
            type: 'contextUpdate',
            context: ctx
        });
    }

    async _handleSendMessage(messageText, includeContext = true) {
        if (!this._view || !messageText.trim()) return;

        let editorContext = {};
        if (includeContext) {
            editorContext = ContextManager.getActiveEditorContext();
        }

        this._isGenerating = true;
        this._view.webview.postMessage({
            type: 'startStream',
            userMessage: messageText
        });

        try {
            const resp = await this._runtimeClient.sendChat(
                messageText,
                this._selectedModel,
                this._selectedAgent,
                editorContext
            );

            if (resp.error) {
                this._view.webview.postMessage({
                    type: 'chatError',
                    error: resp.error
                });
            } else {
                this._view.webview.postMessage({
                    type: 'chatResponse',
                    reply: resp.reply,
                    model: resp.model,
                    agent: resp.agent,
                    actions: resp.actions || [],
                    governance: resp.governance || null
                });
            }
        } catch (err) {
            this._view.webview.postMessage({
                type: 'chatError',
                error: `Communication error with OpenClone Gateway: ${err.message}. Ensure gateway is running on http://127.0.0.1:8000.`
            });
        } finally {
            this._isGenerating = false;
        }
    }

    async _handleQuickAction(actionType, contextData) {
        const editorContext = ContextManager.getActiveEditorContext();
        let prompt = '';

        switch (actionType) {
            case 'explain':
                prompt = editorContext.selection
                    ? `Explain this selected code in detail:\n\`\`\`${editorContext.language}\n${editorContext.selection}\n\`\`\``
                    : `Explain the purpose, structure, and architecture of file \`${editorContext.activeFile}\`.`;
                break;
            case 'debug':
                prompt = editorContext.selection
                    ? `Identify potential bugs, edge cases, and runtime pitfalls in this code snippet:\n\`\`\`${editorContext.language}\n${editorContext.selection}\n\`\`\``
                    : `Inspect \`${editorContext.activeFile}\` for logical flaws or bugs.`;
                break;
            case 'refactor':
                prompt = `Refactor this code to improve clarity, performance, and adhere to OpenClone engineering standards:\n\`\`\`${editorContext.language}\n${editorContext.selection || 'Current file'}\n\`\`\``;
                break;
            case 'generateTests':
                prompt = `Generate comprehensive unit test suites with pytest or jest for:\n\`\`\`${editorContext.language}\n${editorContext.selection || editorContext.activeFile}\n\`\`\``;
                break;
            case 'review':
                prompt = `Perform an EGM security and architecture review on file \`${editorContext.activeFile}\`.`;
                break;
            case 'architect':
                prompt = `Generate a governed architecture specification and component dependency graph for this workspace.`;
                break;
            default:
                prompt = actionType;
        }

        await this._handleSendMessage(prompt, true);
    }

    async _handleApprovalResponse(digest, action) {
        try {
            const res = await this._runtimeClient.respondApproval(digest, action);
            vscode.window.showInformationMessage(`OpenClone Governance: ${res.message || 'Approval recorded'}`);
            if (this._view) {
                this._view.webview.postMessage({
                    type: 'approvalRecorded',
                    digest,
                    action
                });
            }
        } catch (e) {
            vscode.window.showErrorMessage(`Failed to record approval: ${e.message}`);
        }
    }

    async _handleClearConversation() {
        await this._runtimeClient.clearConversation();
        if (this._view) {
            this._view.webview.postMessage({ type: 'conversationCleared' });
        }
    }

    async _updateHealthStatus() {
        const health = await this._runtimeClient.checkHealth();
        if (this._view) {
            this._view.webview.postMessage({
                type: 'healthUpdate',
                healthy: health.status === 'healthy',
                workspace: health.workspace || '',
                gitBranch: health.git_branch || 'main'
            });
        }
    }

    postMessageToWebview(message) {
        if (this._view) {
            this._view.webview.postMessage(message);
        }
    }

    _getHtmlForWebview(webview) {
        const scriptUri = webview.asWebviewUri(vscode.Uri.joinPath(this._extensionUri, 'media', 'chatView.js'));
        const styleUri = webview.asWebviewUri(vscode.Uri.joinPath(this._extensionUri, 'media', 'chatView.css'));
        const nonce = getNonce();

        return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src ${webview.cspSource} https: data:; style-src ${webview.cspSource} 'unsafe-inline'; script-src 'nonce-${nonce}';">
    <link href="${styleUri}" rel="stylesheet" />
    <title>OpenClone Assistant</title>
</head>
<body>
    <div id="app" class="chat-container">
        <!-- Header Bar -->
        <header class="chat-header">
            <div class="header-left">
                <span class="brand-title">OPENCLONE</span>
                <span id="connectionBadge" class="status-badge offline" title="Gateway Status">Connecting...</span>
            </div>
            <div class="header-right">
                <button id="clearChatBtn" class="icon-btn" title="Clear Conversation">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
                </button>
                <button id="reconnectBtn" class="icon-btn" title="Refresh Connection">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg>
                </button>
            </div>
        </header>

        <!-- Selector Bar -->
        <div class="selector-bar">
            <div class="selector-group">
                <label for="modelSelect">MODEL</label>
                <select id="modelSelect">
                    <option value="">Auto Route (MIE)</option>
                </select>
            </div>
            <div class="selector-group">
                <label for="agentSelect">AGENT</label>
                <select id="agentSelect">
                    <option value="">OpenClone Assistant</option>
                </select>
            </div>
        </div>

        <!-- Active Context Indicator -->
        <div id="contextBar" class="context-bar hidden">
            <span class="context-icon">📎</span>
            <span id="contextText" class="context-text">No file active</span>
            <button id="detachContextBtn" class="btn-text-sm" title="Exclude Editor Context">Detach</button>
        </div>

        <!-- Quick Actions Ribbon -->
        <div class="quick-actions">
            <button class="action-chip" data-action="explain">Explain</button>
            <button class="action-chip" data-action="debug">Debug</button>
            <button class="action-chip" data-action="refactor">Refactor</button>
            <button class="action-chip" data-action="generateTests">Tests</button>
            <button class="action-chip" data-action="review">Review</button>
        </div>

        <!-- Message History Feed -->
        <main id="chatFeed" class="chat-feed">
            <div class="message assistant intro">
                <div class="msg-header">
                    <span class="agent-tag">SYSTEM</span>
                    <span class="time-tag">OpenClone 2.0</span>
                </div>
                <div class="msg-body">
                    <p><strong>Universal AI Engineering Assistant</strong></p>
                    <p>Connected to governed workspace intelligence, 72 agent workforce contracts, and deterministic execution runtime.</p>
                    <p class="hint">Ask questions about your codebase, select code in the editor, or use quick action chips above.</p>
                </div>
            </div>
        </main>

        <!-- Input Bar -->
        <footer class="chat-input-area">
            <div class="input-wrapper">
                <textarea id="promptInput" rows="1" placeholder="Ask OpenClone or type /help..." autofocus></textarea>
                <div class="input-actions">
                    <button id="sendBtn" class="send-btn" title="Send Message (Enter)">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
                    </button>
                </div>
            </div>
            <div class="input-footer">
                <span class="governance-label">Deterministic Governance Active</span>
                <span id="branchLabel" class="branch-label">main</span>
            </div>
        </footer>
    </div>

    <script nonce="${nonce}" src="${scriptUri}"></script>
</body>
</html>`;
    }
}

function getNonce() {
    let text = '';
    const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    for (let i = 0; i < 32; i++) {
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    }
    return text;
}

module.exports = { OpenCloneChatViewProvider };
