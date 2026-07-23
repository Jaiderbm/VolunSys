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
  newMessage = '';
  isTyping = false;

  // Quick suggestion chips shown on first interaction
  quickSuggestions: string[] = [
    '🏖️ ¿Qué programas de voluntariado hay disponibles?',
    '📊 ¿Cuántos voluntarios registrados hay?',
    '📝 ¿Cómo me inscribo a una jornada?',
    '🔐 ¿Qué roles existen en el sistema?',
    '🛠️ ¿Con qué tecnologías está construido VolunSys?'
  ];

  constructor(private apiService: ApiService, private sanitizer: DomSanitizer) {}

  ngOnInit() {
    const welcomeText = '¡Hola! 👋 Soy **VolunBot**, tu asistente inteligente de **VolunSys**.\n\nPuedo ayudarte con información sobre:\n- 🏖️ Limpieza de Playas\n- 🐾 Rescate Animal\n- 👴 Apoyo a Adultos Mayores\n\n¿En qué puedo ayudarte hoy?';
    this.messages.push({
      text: welcomeText,
      html: this.parseMarkdown(welcomeText),
      isUser: false,
      time: this.getCurrentTime()
    });
  }

  /**
   * Converts markdown-like text to safe HTML for rendering in bot messages.
   * Handles bold, italic, numbered lists, bullet lists, and line breaks.
   */
  parseMarkdown(text: string): SafeHtml {
    let html = text
      // Escape HTML entities
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

  /**
   * Clears the chat history and re-adds the welcome message.
   */
  clearChat() {
    this.messages = [];
    this.ngOnInit();
  }

  /**
   * Fills the input with a quick suggestion and sends it.
   */
  useSuggestion(suggestion: string) {
    this.newMessage = suggestion;
    this.sendMessage();
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

      const response = await fetch('http://127.0.0.1:8000/api/chat', {
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
      const errMsg = '⚠️ No pude conectarme con el servidor. Asegúrate de que el backend FastAPI esté corriendo en el puerto 8000.';
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
