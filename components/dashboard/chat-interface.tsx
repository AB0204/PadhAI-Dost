'use client';

import { useState, useRef, useEffect } from 'react';
import { Button, Input } from '@/components/ui/auth-components';
import { Send, User as UserIcon, Bot, Paperclip } from 'lucide-react';

interface Message {
    role: 'user' | 'assistant';
    content: string;
}

export default function ChatInterface() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    async function handleSubmit(e: React.FormEvent) {
        e.preventDefault();
        if (!input.trim() || isLoading) return;

        const userMessage = input;
        setInput('');
        setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
        setIsLoading(true);

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userMessage }),
            });

            if (!response.ok) {
                throw new Error('Failed to send message');
            }

            const data = await response.json();
            setMessages(prev => [...prev, { role: 'assistant', content: data.answer }]);
        } catch (error) {
            console.error(error);
            setMessages(prev => [...prev, { role: 'assistant', content: 'Sorry, something went wrong. Please check if the backend is running.' }]);
        } finally {
            setIsLoading(false);
        }
    }

    return (
        <div className="flex flex-col h-[calc(100vh-120px)] w-full max-w-4xl mx-auto bg-white rounded-lg shadow-sm border">
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.length === 0 && (
                    <div className="flex flex-col items-center justify-center h-full text-gray-400">
                        <Bot className="w-12 h-12 mb-2" />
                        <p>Start chatting with your document!</p>
                    </div>
                )}
                {messages.map((m, index) => (
                    <div
                        key={index}
                        className={`flex items-start gap-3 ${m.role === 'user' ? 'flex-row-reverse' : ''
                            }`}
                    >
                        <div
                            className={`p-2 rounded-full ${m.role === 'user' ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 text-gray-600'
                                }`}
                        >
                            {m.role === 'user' ? <UserIcon size={20} /> : <Bot size={20} />}
                        </div>
                        <div
                            className={`p-3 rounded-lg max-w-[80%] text-sm ${m.role === 'user'
                                    ? 'bg-blue-600 text-white'
                                    : 'bg-gray-100 text-gray-800'
                                }`}
                        >
                            {m.content}
                        </div>
                    </div>
                ))}
                {isLoading && (
                    <div className="flex items-start gap-3">
                        <div className="p-2 rounded-full bg-gray-100 text-gray-600">
                            <Bot size={20} />
                        </div>
                        <div className="p-3 rounded-lg bg-gray-50 text-gray-500 text-sm">
                            Thinking...
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            <div className="p-4 border-t bg-gray-50/50">
                <form onSubmit={handleSubmit} className="flex gap-2">
                    <Input
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Ask a question..."
                        disabled={isLoading}
                        className="flex-1 bg-white"
                    />
                    <Button type="submit" disabled={isLoading || !input.trim()}>
                        <Send size={18} />
                    </Button>
                </form>
            </div>
        </div>
    );
}
