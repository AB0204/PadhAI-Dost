'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { LayoutDashboard, MessageSquare, Files, Settings, LogOut, BookOpen } from 'lucide-react';
import { signOut } from 'next-auth/react';

const links = [
    { name: 'Chat', href: '/chat', icon: MessageSquare },
    { name: 'Documents', href: '/documents', icon: Files },
    { name: 'Progress', href: '/progress', icon: LayoutDashboard },
];

export default function SideNav() {
    const pathname = usePathname();

    return (
        <div className="flex h-full flex-col px-3 py-4 md:px-2">
            <Link
                className="mb-2 flex h-20 items-end justify-start rounded-md bg-black p-4 md:h-40"
                href="/"
            >
                <div className="w-32 text-white md:w-40">
                    <div className="flex items-center gap-2 font-bold text-xl">
                        <BookOpen className="h-8 w-8" />
                        <span>PadhAI Dost</span>
                    </div>
                    <div className="text-xs text-gray-400 mt-1">v2.0</div>
                </div>
            </Link>
            <div className="flex grow flex-row justify-between space-x-2 md:flex-col md:space-x-0 md:space-y-2">
                {links.map((link) => {
                    const LinkIcon = link.icon;
                    return (
                        <Link
                            key={link.name}
                            href={link.href}
                            className={`flex h-[48px] grow items-center justify-center gap-2 rounded-md bg-gray-50 p-3 text-sm font-medium hover:bg-sky-100 hover:text-blue-600 md:flex-none md:justify-start md:p-2 md:px-3
              ${pathname === link.href ? 'bg-sky-100 text-blue-600' : ''}
              `}
                        >
                            <LinkIcon className="w-6" />
                            <p className="hidden md:block">{link.name}</p>
                        </Link>
                    );
                })}
                <div className="hidden h-auto w-full grow rounded-md bg-gray-50 md:block"></div>
                <form
                    action={async () => {
                        // We can't use server action passed to onClick directly in client component nicely without wrapping
                        // But we can use next-auth/react signOut
                        await signOut();
                    }}
                >
                    <button className="flex h-[48px] w-full grow items-center justify-center gap-2 rounded-md bg-gray-50 p-3 text-sm font-medium hover:bg-sky-100 hover:text-blue-600 md:flex-none md:justify-start md:p-2 md:px-3">
                        <LogOut className="w-6" />
                        <div className="hidden md:block">Sign Out</div>
                    </button>
                </form>
            </div>
        </div>
    );
}
