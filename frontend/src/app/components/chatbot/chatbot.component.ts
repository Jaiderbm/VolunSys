import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { ApiService } from '../../services/api.service';

interface ChatMessage {
  text: string;
  html: SafeHtml;
  isUser: boolean;
  time: string;
}

@Component({
  selector: 'app-chatbot',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chatbot.component.html',
  styleUrl: './chatbot.component.css'
})
export class ChatbotComponent {
  isOpen = false;
  messages: ChatMessage[] = [];

  ngOnInit() {
    const welcomeText = '¡Hola! Soy VolunBot 🤖. ¿En qué puedo ayudarte hoy?';
    this.messages.push({ text: welcomeText, html: this.parseMarkdown(welcomeText), isUser: false, time: this.getCurrentTime() });
  }
  newMessage = '';
  isTyping = false;

  constructor(private apiService: ApiService, private sanitizer: DomSanitizer) {}

  // Simple markdown-to-HTML converter
  parseMarkdown(text: string): SafeHtml {
    let html = text
      // Escape HTML
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      // Bold **text**
      .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      // Italic *text*
      .replace(/\*(.+?)\*/g, '<em>$1</em>')
      // Convert numbered list lines: "1. item"
      .replace(/(?:^|\n)(\d+\.\s+)(.+)/g, '<li>$2</li>')
      // Convert bullet list lines: "- item" or "• item"
      .replace(/(?:^|\n)[-•]\s+(.+)/g, '<li>$1</li>')
      // Wrap consecutive <li> with <ul>
      .replace(/(<li>.*<\/li>)/gs, '<ul class="chat-list">$1</ul>')
      // Newlines to <br> (excluding those already in lists)
      .replace(/(?<!>)\n(?!<)/g, '<br>');
    return this.sanitizer.bypassSecurityTrustHtml(html);
  }

  toggleChat() {
    this.isOpen = !this.isOpen;
  }

  getCurrentTime(): string {
    const now = new Date();
    return now.getHours().toString().padStart(2, '0') + ':' + now.getMinutes().toString().padStart(2, '0');
  }

  async sendMessage() {
    if (!this.newMessage.trim()) return;

    // Add user message
    const userText = this.newMessage;
    this.messages.push({
      text: userText,
      html: this.parseMarkdown(userText),
      isUser: true,
      time: this.getCurrentTime()
    });

    this.newMessage = '';
    this.isTyping = true;

    try {
      const historyToSend = this.messages.map(msg => ({
          role: msg.isUser ? 'user' : 'assistant',
          content: msg.text
      }));

      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: historyToSend })
      });
      
      const data = await response.json();
      const replyText = data.response || 'Hubo un error al entender tu mensaje.';
      
      this.isTyping = false;
      this.messages.push({
        text: replyText,
        html: this.parseMarkdown(replyText),
        isUser: false,
        time: this.getCurrentTime()
      });
    } catch (error) {
      const errMsg = 'Lo siento, no me pude conectar con el servidor. Intenta de nuevo más tarde.';
      this.isTyping = false;
      this.messages.push({
        text: errMsg,
        html: this.parseMarkdown(errMsg),
        isUser: false,
        time: this.getCurrentTime()
      });
    }
  }
}
