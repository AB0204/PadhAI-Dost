import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@/auth';

export async function POST(req: NextRequest) {
    const session = await auth();
    if (!session || !session.user || !session.user.email) {
        return NextResponse.json({ message: 'Unauthorized' }, { status: 401 });
    }

    const formData = await req.formData();
    const file = formData.get('file');

    if (!file) {
        return NextResponse.json({ message: 'No file uploaded' }, { status: 400 });
    }

    const sessionId = session.user.email;

    try {
        // Forward to Python Backend
        const backendFormData = new FormData();
        backendFormData.append('file', file);

        // Add auth header if needed, for now just forward
        // session_id as query param
        const backendUrl = `http://127.0.0.1:8000/upload?session_id=${encodeURIComponent(sessionId)}`;

        // We need to fetch from node-js to python fastapi
        const res = await fetch(backendUrl, {
            method: 'POST',
            body: backendFormData as any, // TypeScript might complain about FormData in fetch body
        });

        if (!res.ok) {
            const text = await res.text();
            console.error("Backend Upload Error:", text);
            return NextResponse.json({ message: `Backend error: ${text}` }, { status: 500 });
        }

        const data = await res.json();
        return NextResponse.json(data);

    } catch (error) {
        console.error(error);
        return NextResponse.json({ message: 'Internal Error' }, { status: 500 });
    }
}
