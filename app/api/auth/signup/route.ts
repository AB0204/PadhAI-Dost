import { prisma } from '@/lib/prisma';
import bcrypt from 'bcrypt';
import { NextResponse } from 'next/server';
import { z } from 'zod';

const signUpSchema = z.object({
    email: z.string().email(),
    password: z.string().min(6),
    name: z.string().min(2).optional(),
});

export async function POST(request: Request) {
    try {
        const body = await request.json();
        const { email, password, name } = signUpSchema.parse(body);

        const existingUser = await prisma.user.findUnique({
            where: { email },
        });

        if (existingUser) {
            return NextResponse.json(
                { message: 'User already exists' },
                { status: 400 }
            );
        }

        const hashedPassword = await bcrypt.hash(password, 10);

        const user = await prisma.user.create({
            data: {
                email,
                password: hashedPassword, // Store hashed password
                name,
            },
        });

        // Remove password from response
        const { password: _, ...userWithoutPassword } = user;

        return NextResponse.json(
            { message: 'User created successfully', user: userWithoutPassword },
            { status: 201 }
        );
    } catch (error) {
        console.error('Signup Error:', error);
        if (error instanceof z.ZodError) {
            return NextResponse.json({ message: error.flatten() }, { status: 400 });
        }
        return NextResponse.json(
            { message: 'Internal server error' },
            { status: 500 }
        );
    }
}
