import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@/auth';
import { prisma } from '@/lib/prisma';

export async function POST(req: NextRequest) {
    const session = await auth();
    if (!session || !session.user || !session.user.email) {
        return NextResponse.json({ message: 'Unauthorized' }, { status: 401 });
    }

    const { message } = await req.json();
    const userId = session.user.id; // Or email if ID is not available?
    // User ID is better. session.user.id is populated in auth.ts callback.

    // Use email as session_id for Python backend for now (simple 1-1 mapping)
    const sessionId = session.user.email;

    try {
        // 1. Save User Message to DB (Optional for now, but good for history)
        // We need a Chat ID. For now, let's create a "default" chat or just log messages?
        // Let's skip DB persistence for this precise step to get RAG working first, 
        // unless we want to show history.

        // 2. Call Python Backend
        const backendUrl = 'http://127.0.0.1:8000/chat';
        const res = await fetch(backendUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                session_id: sessionId,
                message: message
            }),
        });

        if (!res.ok) {
            console.error("Backend Error:", await res.text());
            return NextResponse.json({ message: 'Backend error' }, { status: 500 });
        }

        const data = await res.json();
        return NextResponse.json(data);

    } catch (error) {
        console.error(error);
        return NextResponse.json({ message: 'Internal Error' }, { status: 500 });
    }
}
