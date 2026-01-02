'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/auth-components';
import { Upload, FileText, CheckCircle, AlertCircle } from 'lucide-react';
import { useRouter } from 'next/navigation';

export default function DocumentUploader() {
    const [file, setFile] = useState<File | null>(null);
    const [isUploading, setIsUploading] = useState(false);
    const [status, setStatus] = useState<'idle' | 'success' | 'error'>('idle');
    const router = useRouter();

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
            setStatus('idle');
        }
    };

    const handleUpload = async () => {
        if (!file) return;

        setIsUploading(true);
        setStatus('idle');

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) throw new Error('Upload failed');

            setStatus('success');
            // Refresh router or notify parent
            router.refresh();
        } catch (error) {
            console.error(error);
            setStatus('error');
        } finally {
            setIsUploading(false);
        }
    };

    return (
        <div className="p-4 bg-white rounded-lg border shadow-sm mb-6">
            <div className="flex items-center gap-4">
                <div className="relative group">
                    <input
                        type="file"
                        onChange={handleFileChange}
                        accept=".pdf,.txt"
                        className="absolute inset-0 opacity-0 cursor-pointer w-full h-full z-10"
                    />
                    <Button type="button" className="pointer-events-none relative">
                        <Upload size={16} className="mr-2" />
                        Select Document
                    </Button>
                </div>

                {file && (
                    <div className="flex items-center gap-2 text-sm text-gray-600 flex-1">
                        <FileText size={16} />
                        <span className="truncate max-w-[150px]">{file.name}</span>
                    </div>
                )}

                {file && (
                    <Button
                        onClick={handleUpload}
                        disabled={isUploading}
                        className={status === 'success' ? 'bg-green-600 hover:bg-green-700' : ''}
                    >
                        {isUploading ? 'Uploading...' : status === 'success' ? 'Uploaded' : 'Start Processing'}
                    </Button>
                )}
            </div>

            {status === 'success' && (
                <div className="mt-2 text-xs text-green-600 flex items-center gap-1">
                    <CheckCircle size={12} /> Document processed and ready for chat!
                </div>
            )}
            {status === 'error' && (
                <div className="mt-2 text-xs text-red-600 flex items-center gap-1">
                    <AlertCircle size={12} /> Upload failed. Ensure the backend is running.
                </div>
            )}
        </div>
    );
}
