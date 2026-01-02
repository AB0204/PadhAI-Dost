import { SignUpForm } from '@/components/ui/auth-forms';
import Link from 'next/link';
import { Metadata } from 'next';

export const metadata: Metadata = {
    title: 'Sign Up - PadhAI Dost',
};

export default function SignupPage() {
    return (
        <div className="flex min-h-screen flex-col items-center justify-center bg-gray-50 p-6">
            <div className="w-full max-w-sm bg-white p-8 rounded-lg shadow-md border space-y-6">
                <div className="text-center">
                    <h1 className="text-2xl font-bold tracking-tight">Create Account</h1>
                    <p className="text-sm text-gray-500">Get started with your AI Study Buddy</p>
                </div>

                <SignUpForm />

                <div className="text-center text-sm">
                    Already have an account?{' '}
                    <Link href="/login" className="underline hover:text-blue-600">
                        Log in
                    </Link>
                </div>
            </div>
        </div>
    );
}
