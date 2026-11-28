/**
 * OpenClone REST Runtime Client for VS Code Extension.
 * Communicates with the local OpenClone REST Gateway (default: http://127.0.0.1:8000/api/v1).
 */
const http = require('http');
const https = require('https');
const { URL } = require('url');

class OpenCloneRuntimeClient {
    constructor(baseUrl = 'http://127.0.0.1:8000') {
        this.baseUrl = baseUrl.replace(/\/+$/, '');
        this.isConnected = false;
        this.lastError = null;
    }

    setBaseUrl(url) {
        this.baseUrl = url.replace(/\/+$/, '');
    }

    _request(method, path, body = null, timeoutMs = 15000) {
        return new Promise((resolve, reject) => {
            try {
                const targetUrl = new URL(this.baseUrl + path);
                const isHttps = targetUrl.protocol === 'https:';
                const transport = isHttps ? https : http;

                const options = {
                    hostname: targetUrl.hostname,
                    port: targetUrl.port || (isHttps ? 443 : 80),
                    path: targetUrl.pathname + targetUrl.search,
                    method: method.toUpperCase(),
                    headers: {
                        'Accept': 'application/json',
                        'User-Agent': 'OpenClone-VSCode/2.0.0'
                    },
                    timeout: timeoutMs
                };

                let requestBody = null;
                if (body && (method === 'POST' || method === 'PUT')) {
                    requestBody = JSON.stringify(body);
                    options.headers['Content-Type'] = 'application/json';
                    options.headers['Content-Length'] = Buffer.byteLength(requestBody);
                }

                const req = transport.request(options, (res) => {
                    let responseData = '';
                    res.setEncoding('utf8');

                    res.on('data', (chunk) => {
                        responseData += chunk;
                    });

                    res.on('end', () => {
                        try {
                            const parsed = JSON.parse(responseData || '{}');
                            if (res.statusCode >= 200 && res.statusCode < 300) {
                                this.isConnected = true;
                                this.lastError = null;
                                resolve(parsed);
                            } else {
                                resolve({
                                    error: parsed.error || `HTTP ${res.statusCode}`,
                                    statusCode: res.statusCode,
                                    data: parsed
                                });
                            }
                        } catch (e) {
                            resolve({
                                error: `Failed to parse response JSON: ${e.message}`,
                                raw: responseData,
                                statusCode: res.statusCode
                            });
                        }
                    });
                });

                req.on('timeout', () => {
                    req.destroy();
                    this.isConnected = false;
                    this.lastError = 'Connection timed out';
                    reject(new Error(`Request to ${path} timed out after ${timeoutMs}ms`));
                });

                req.on('error', (err) => {
                    this.isConnected = false;
                    this.lastError = err.message;
                    reject(err);
                });

                if (requestBody) {
                    req.write(requestBody);
                }
                req.end();
            } catch (err) {
                this.isConnected = false;
                this.lastError = err.message;
                reject(err);
            }
        });
    }

    async checkHealth() {
        try {
            const data = await this._request('GET', '/api/v1/health', null, 3000);
            this.isConnected = data.status === 'healthy';
            return data;
        } catch (e) {
            this.isConnected = false;
            return { status: 'offline', error: e.message };
        }
    }

    async getWorkspaceContext() {
        return this._request('GET', '/api/v1/projects');
    }

    async getModels() {
        return this._request('GET', '/api/v1/models');
    }

    async getProviders() {
        return this._request('GET', '/api/v1/providers');
    }

    async getAgents() {
        return this._request('GET', '/api/v1/agents');
    }

    async sendChat(message, model = null, agent = null, context = null) {
        return this._request('POST', '/api/v1/chat', {
            message,
            model,
            agent,
            context
        }, 30000);
    }

    async getConversationHistory() {
        return this._request('GET', '/api/v1/conversation/history');
    }

    async clearConversation() {
        return this._request('POST', '/api/v1/conversation/clear', {});
    }

    async respondApproval(digest, action, notes = '') {
        return this._request('POST', '/api/v1/approvals', {
            digest,
            action,
            notes
        });
    }

    async executePlan(requirement) {
        return this._request('POST', '/api/v1/plans', { prompt: requirement });
    }

    async executeTask(instruction) {
        return this._request('POST', '/api/v1/execution', { prompt: instruction });
    }
}

module.exports = { OpenCloneRuntimeClient };
