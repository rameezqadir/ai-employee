#!/usr/bin/env node

/**
 * Email MCP Server
 * Provides Gmail tools to Claude Desktop
 */

const { Server } = require('@modelcontextprotocol/sdk/server/index.js');
const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio.js');
const { google } = require('googleapis');
const fs = require('fs');
const path = require('path');

const SCOPES = [
  'https://www.googleapis.com/auth/gmail.readonly',
  'https://www.googleapis.com/auth/gmail.send'
];

class EmailMCPServer {
  constructor() {
    this.server = new Server(
      {
        name: 'email-mcp-server',
        version: '0.1.0'
      },
      {
        capabilities: {
          tools: {}
        }
      }
    );

    this.gmailClient = null;
    this.setupToolHandlers();
    
    // Initialize Gmail client
    this.initializeGmail();
  }

  async initializeGmail() {
    try {
      const tokenPath = path.join(__dirname, '../../token.json');
      
      if (!fs.existsSync(tokenPath)) {
        console.error('token.json not found. Run gmail_setup.py first.');
        return;
      }

      const credentials = JSON.parse(fs.readFileSync(tokenPath, 'utf8'));
      const auth = new google.auth.OAuth2();
      auth.setCredentials(credentials);
      
      this.gmailClient = google.gmail({ version: 'v1', auth });
      console.error('Gmail client initialized');
    } catch (error) {
      console.error('Error initializing Gmail:', error);
    }
  }

  setupToolHandlers() {
    // List available tools
    this.server.setRequestHandler('tools/list', async () => ({
      tools: [
        {
          name: 'list_unread_emails',
          description: 'List unread emails from Gmail',
          inputSchema: {
            type: 'object',
            properties: {
              max_results: {
                type: 'number',
                description: 'Maximum number of emails to return (default: 10)',
                default: 10
              }
            }
          }
        },
        {
          name: 'send_email',
          description: 'Send an email via Gmail (requires approval)',
          inputSchema: {
            type: 'object',
            properties: {
              to: {
                type: 'string',
                description: 'Recipient email address'
              },
              subject: {
                type: 'string',
                description: 'Email subject'
              },
              body: {
                type: 'string',
                description: 'Email body content'
              }
            },
            required: ['to', 'subject', 'body']
          }
        },
        {
          name: 'mark_as_read',
          description: 'Mark an email as read',
          inputSchema: {
            type: 'object',
            properties: {
              message_id: {
                type: 'string',
                description: 'Gmail message ID'
              }
            },
            required: ['message_id']
          }
        }
      ]
    }));

    // Handle tool calls
    this.server.setRequestHandler('tools/call', async (request) => {
      const { name, arguments: args } = request.params;

      if (!this.gmailClient) {
        return {
          content: [{
            type: 'text',
            text: 'Error: Gmail not initialized. Run gmail_setup.py first.'
          }]
        };
      }

      try {
        switch (name) {
          case 'list_unread_emails':
            return await this.listUnreadEmails(args.max_results || 10);
          
          case 'send_email':
            return await this.sendEmail(args.to, args.subject, args.body);
          
          case 'mark_as_read':
            return await this.markAsRead(args.message_id);
          
          default:
            return {
              content: [{
                type: 'text',
                text: `Unknown tool: ${name}`
              }]
            };
        }
      } catch (error) {
        return {
          content: [{
            type: 'text',
            text: `Error: ${error.message}`
          }]
        };
      }
    });
  }

  async listUnreadEmails(maxResults) {
    const response = await this.gmailClient.users.messages.list({
      userId: 'me',
      q: 'is:unread',
      maxResults: maxResults
    });

    const messages = response.data.messages || [];
    
    if (messages.length === 0) {
      return {
        content: [{
          type: 'text',
          text: 'No unread emails found.'
        }]
      };
    }

    const emailDetails = [];
    
    for (const msg of messages) {
      const detail = await this.gmailClient.users.messages.get({
        userId: 'me',
        id: msg.id,
        format: 'metadata',
        metadataHeaders: ['From', 'Subject', 'Date']
      });

      const headers = detail.data.payload.headers;
      const from = headers.find(h => h.name === 'From')?.value || 'Unknown';
      const subject = headers.find(h => h.name === 'Subject')?.value || 'No Subject';
      const date = headers.find(h => h.name === 'Date')?.value || '';

      emailDetails.push(`From: ${from}\nSubject: ${subject}\nDate: ${date}\nID: ${msg.id}\n`);
    }

    return {
      content: [{
        type: 'text',
        text: `Found ${messages.length} unread email(s):\n\n${emailDetails.join('\n---\n')}`
      }]
    };
  }

  async sendEmail(to, subject, body) {
    const message = [
      `To: ${to}`,
      `Subject: ${subject}`,
      '',
      body
    ].join('\n');

    const encodedMessage = Buffer.from(message)
      .toString('base64')
      .replace(/\+/g, '-')
      .replace(/\//g, '_')
      .replace(/=+$/, '');

    await this.gmailClient.users.messages.send({
      userId: 'me',
      requestBody: {
        raw: encodedMessage
      }
    });

    return {
      content: [{
        type: 'text',
        text: `✅ Email sent successfully to ${to}`
      }]
    };
  }

  async markAsRead(messageId) {
    await this.gmailClient.users.messages.modify({
      userId: 'me',
      id: messageId,
      requestBody: {
        removeLabelIds: ['UNREAD']
      }
    });

    return {
      content: [{
        type: 'text',
        text: `✅ Email marked as read`
      }]
    };
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('Email MCP Server running on stdio');
  }
}

const server = new EmailMCPServer();
server.run().catch(console.error);
