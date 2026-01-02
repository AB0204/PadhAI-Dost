import { LoginForm } from '@/components/ui/auth-forms';
import Link from 'next/link';
import { Metadata } from 'next';

export const metadata: Metadata = {
    title: 'Login - PadhAI Dost',
};

export default function LoginPage() {
    return (
        <div className="flex min-h-screen flex-col items-center justify-center bg-gray-50 p-6">
            <div className="w-full max-w-sm bg-white p-8 rounded-lg shadow-md border space-y-6">
                <div className="text-center">
                    <h1 className="text-2xl font-bold tracking-tight">Welcome Back</h1>
                    <p className="text-sm text-gray-500">Sign in to your account</p>
                </div>

                <LoginForm />

                <div className="text-center text-sm">
                    Don't have an account?{' '}
                    <Link href="/signup" className="underline hover:text-blue-600">
                        Sign up
                    </Link>
                </div>
            </div>
        </div>
    );
}
