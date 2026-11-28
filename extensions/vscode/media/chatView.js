// OpenClone Webview Chat Controller Script
(function () {
    const vscode = acquireVsCodeApi();

    // DOM Elements
    const connectionBadge = document.getElementById('connectionBadge');
    const clearChatBtn = document.getElementById('clearChatBtn');
    const reconnectBtn = document.getElementById('reconnectBtn');
    const modelSelect = document.getElementById('modelSelect');
    const agentSelect = document.getElementById('agentSelect');
    const contextBar = document.getElementById('contextBar');
    const contextText = document.getElementById('contextText');
    const detachContextBtn = document.getElementById('detachContextBtn');
    const chatFeed = document.getElementById('chatFeed');
    const promptInput = document.getElementById('promptInput');
    const sendBtn = document.getElementById('sendBtn');
    const branchLabel = document.getElementById('branchLabel');

    let includeContext = true;
    let isConnected = false;
    let currentContext = null;

    // Initialize Webview State
    vscode.postMessage({ type: 'init' });

    // Auto-resize textarea
    promptInput.addEventListener('input', () => {
        promptInput.style.height = 'auto';
        promptInput.style.height = Math.min(promptInput.scrollHeight, 120) + 'px';
    });

    // Handle Send
    function handleSend() {
        const text = promptInput.value.trim();
        if (!text) return;

        appendMessage('user', text);
        promptInput.value = '';
        promptInput.style.height = 'auto';
        sendBtn.disabled = true;

        showThinkingIndicator();

        vscode.postMessage({
            type: 'sendMessage',
            message: text,
            includeContext: includeContext
        });
    }

    sendBtn.addEventListener('click', handleSend);

    promptInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    });

    // Clear Chat
    clearChatBtn.addEventListener('click', () => {
        chatFeed.innerHTML = '';
        vscode.postMessage({ type: 'clearConversation' });
    });

    // Reconnect / Health Check
    reconnectBtn.addEventListener('click', () => {
        connectionBadge.textContent = 'Checking...';
        connectionBadge.className = 'status-badge';
        vscode.postMessage({ type: 'checkHealth' });
    });

    // Detach / Attach Context
    detachContextBtn.addEventListener('click', () => {
        includeContext = !includeContext;
        if (includeContext) {
            detachContextBtn.textContent = 'Detach';
            contextBar.style.opacity = '1';
        } else {
            detachContextBtn.textContent = 'Attach';
            contextBar.style.opacity = '0.5';
        }
    });

    // Model Selector Change
    modelSelect.addEventListener('change', () => {
        vscode.postMessage({
            type: 'selectModel',
            modelId: modelSelect.value
        });
    });

    // Agent Selector Change
    agentSelect.addEventListener('change', () => {
        vscode.postMessage({
            type: 'selectAgent',
            agentRole: agentSelect.value
        });
    });

    // Quick Actions
    document.querySelectorAll('.action-chip').forEach(btn => {
        btn.addEventListener('click', () => {
            const action = btn.getAttribute('data-action');
            vscode.postMessage({
                type: 'quickAction',
                action: action,
                context: currentContext
            });
        });
    });

    // Handle Incoming Messages from Extension Host
    window.addEventListener('message', (event) => {
        const msg = event.data;
        switch (msg.type) {
            case 'healthUpdate':
                isConnected = msg.healthy;
                connectionBadge.textContent = msg.healthy ? 'Connected' : 'Offline';
                connectionBadge.className = 'status-badge ' + (msg.healthy ? 'online' : 'offline');
                if (msg.gitBranch) {
                    branchLabel.textContent = msg.gitBranch;
                }
                break;

            case 'modelsList':
                populateModels(msg.models);
                break;

            case 'agentsList':
                populateAgents(msg.agents);
                break;

            case 'contextUpdate':
                updateContextBar(msg.context);
                break;

            case 'startStream':
                // Streaming start handled by showThinkingIndicator
                break;

            case 'chatResponse':
                removeThinkingIndicator();
                sendBtn.disabled = false;
                appendAssistantMessage(msg.reply, msg.agent, msg.model, msg.actions, msg.governance);
                break;

            case 'chatError':
                removeThinkingIndicator();
                sendBtn.disabled = false;
                appendErrorMessage(msg.error);
                break;

            case 'conversationCleared':
                chatFeed.innerHTML = `
                    <div class="message assistant intro">
                        <div class="msg-header">
                            <span class="agent-tag">SYSTEM</span>
                            <span class="time-tag">New Session</span>
                        </div>
                        <div class="msg-body">
                            <p>Conversation history reset. Ready for governed tasks.</p>
                        </div>
                    </div>`;
                break;
        }
    });

    function populateModels(models) {
        if (!models || !models.length) return;
        const current = modelSelect.value;
        modelSelect.innerHTML = '<option value="">Auto Route (MIE)</option>';
        models.forEach(m => {
            const opt = document.createElement('option');
            opt.value = m.model_id;
            opt.textContent = `${m.display_name} (${m.provider_id})`;
            if (m.model_id === current) opt.selected = true;
            modelSelect.appendChild(opt);
        });
    }

    function populateAgents(agents) {
        if (!agents || !agents.length) return;
        const current = agentSelect.value;
        agentSelect.innerHTML = '<option value="">OpenClone Assistant</option>';
        agents.forEach(a => {
            const opt = document.createElement('option');
            opt.value = a.role;
            opt.textContent = `${a.role} [${a.division}]`;
            if (a.role === current) opt.selected = true;
            agentSelect.appendChild(opt);
        });
    }

    function updateContextBar(ctx) {
        currentContext = ctx;
        if (ctx && ctx.hasActiveEditor && ctx.activeFile) {
            contextBar.classList.remove('hidden');
            let txt = ctx.activeFile;
            if (ctx.startLine) {
                txt += ` : L${ctx.startLine}-L${ctx.endLine}`;
            }
            contextText.textContent = txt;
            contextText.title = ctx.fullPath || txt;
        } else {
            contextBar.classList.add('hidden');
        }
    }

    function appendMessage(role, text) {
        const msgEl = document.createElement('div');
        msgEl.className = `message ${role}`;

        const headerEl = document.createElement('div');
        headerEl.className = 'msg-header';

        if (role === 'user') {
            headerEl.innerHTML = `<span class="user-tag">YOU</span>`;
        } else {
            headerEl.innerHTML = `<span class="agent-tag">ASSISTANT</span>`;
        }

        const bodyEl = document.createElement('div');
        bodyEl.className = 'msg-body';
        bodyEl.textContent = text;

        msgEl.appendChild(headerEl);
        msgEl.appendChild(bodyEl);
        chatFeed.appendChild(msgEl);
        scrollToBottom();
    }

    function appendAssistantMessage(reply, agentName, modelName, actions, governance) {
        const msgEl = document.createElement('div');
        msgEl.className = 'message assistant';

        const headerEl = document.createElement('div');
        headerEl.className = 'msg-header';
        const displayAgent = agentName || 'OpenClone';
        const displayModel = modelName ? ` • ${modelName}` : '';
        headerEl.innerHTML = `<span class="agent-tag">${escapeHtml(displayAgent)}</span><span class="time-tag">${escapeHtml(displayModel)}</span>`;

        const bodyEl = document.createElement('div');
        bodyEl.className = 'msg-body';
        bodyEl.innerHTML = renderMarkdown(reply);

        // Append Actions if any
        if (actions && actions.length) {
            const actionsDiv = document.createElement('div');
            actionsDiv.className = 'msg-actions';
            actions.forEach(act => {
                const btn = document.createElement('button');
                btn.className = 'inline-action-btn';
                btn.textContent = act.label;
                btn.addEventListener('click', () => {
                    vscode.postMessage({
                        type: 'quickAction',
                        action: act.command,
                        context: act.args
                    });
                });
                actionsDiv.appendChild(btn);
            });
            bodyEl.appendChild(actionsDiv);
        }

        // Append Governance Approval Card if any
        if (governance && governance.requires_approval) {
            const card = document.createElement('div');
            card.className = 'approval-card';
            card.innerHTML = `
                <div class="approval-title">Deterministic Governance Approval Required</div>
                <div class="approval-digest">Digest: ${escapeHtml(governance.digest || '')}</div>
                <div class="approval-actions">
                    <button class="btn-approve" data-digest="${escapeHtml(governance.digest || '')}">Approve Operation</button>
                    <button class="btn-reject" data-digest="${escapeHtml(governance.digest || '')}">Reject</button>
                </div>
            `;

            card.querySelector('.btn-approve').addEventListener('click', () => {
                vscode.postMessage({
                    type: 'respondApproval',
                    digest: governance.digest,
                    action: 'approve'
                });
                card.remove();
            });

            card.querySelector('.btn-reject').addEventListener('click', () => {
                vscode.postMessage({
                    type: 'respondApproval',
                    digest: governance.digest,
                    action: 'reject'
                });
                card.remove();
            });

            bodyEl.appendChild(card);
        }

        msgEl.appendChild(headerEl);
        msgEl.appendChild(bodyEl);
        chatFeed.appendChild(msgEl);

        // Bind copy buttons
        bodyEl.querySelectorAll('.copy-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const code = btn.nextElementSibling.innerText;
                navigator.clipboard.writeText(code);
                btn.textContent = 'Copied!';
                setTimeout(() => { btn.textContent = 'Copy'; }, 1500);
            });
        });

        scrollToBottom();
    }

    function appendErrorMessage(err) {
        const msgEl = document.createElement('div');
        msgEl.className = 'message assistant error';

        const bodyEl = document.createElement('div');
        bodyEl.className = 'msg-body';
        bodyEl.style.borderColor = '#e74c3c';
        bodyEl.style.color = '#ff9999';
        bodyEl.innerHTML = `<p><strong>Error:</strong> ${escapeHtml(err)}</p>`;

        msgEl.appendChild(bodyEl);
        chatFeed.appendChild(msgEl);
        scrollToBottom();
    }

    function showThinkingIndicator() {
        const thinkingEl = document.createElement('div');
        thinkingEl.id = 'thinkingIndicator';
        thinkingEl.className = 'message assistant thinking';
        thinkingEl.innerHTML = `
            <div class="msg-body" style="display: flex; align-items: center; gap: 8px;">
                <span class="spinner"></span>
                <span style="font-size: 11px; opacity: 0.8;">OpenClone reasoning...</span>
            </div>`;
        chatFeed.appendChild(thinkingEl);
        scrollToBottom();
    }

    function removeThinkingIndicator() {
        const el = document.getElementById('thinkingIndicator');
        if (el) el.remove();
    }

    function scrollToBottom() {
        chatFeed.scrollTop = chatFeed.scrollHeight;
    }

    function escapeHtml(str) {
        if (!str) return '';
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    function renderMarkdown(md) {
        if (!md) return '';
        let html = escapeHtml(md);

        // Code blocks with syntax copy button
        html = html.replace(/```([a-zA-Z0-9_\-]*)\n([\s\S]*?)```/g, (match, lang, code) => {
            return `<pre><button class="copy-btn">Copy</button><code class="language-${lang}">${code}</code></pre>`;
        });

        // Inline code
        html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

        // Bold
        html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

        // Headers
        html = html.replace(/^### (.*$)/gim, '<h3 style="font-size: 13px; font-weight: 700; margin: 8px 0 4px; color: var(--oc-gold);">$1</h3>');
        html = html.replace(/^## (.*$)/gim, '<h2 style="font-size: 14px; font-weight: 700; margin: 10px 0 6px; color: var(--oc-gold);">$1</h2>');

        // Lists
        html = html.replace(/^\- (.*$)/gim, '<li style="margin-left: 16px;">$1</li>');

        // Paragraphs
        html = html.replace(/\n\n/g, '</p><p>');
        html = '<p>' + html + '</p>';

        return html;
    }
})();
