import { Button } from "@/components/ui/button";
import { ArrowRight, BookOpen, Brain, Trophy, Users, Github, Star } from "lucide-react";

export default function HomePage() {
    return (
        <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white dark:from-gray-900 dark:to-gray-800">
            {/* Hero Section */}
            <section className="container mx-auto px-4 py-20">
                <div className="text-center space-y-6 max-w-4xl mx-auto">
                    <h1 className="text-5xl md:text-7xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                        PadhAI-Dost 🎓
                    </h1>
                    <p className="text-xl md:text-2xl text-gray-600 dark:text-gray-300">
                        Your free AI-powered learning companion. <span className="font-semibold">Forever.</span>
                    </p>
                    <p className="text-lg text-gray-500 dark:text-gray-400 max-w-2xl mx-auto">
                        Unlike ChatGPT, Chegg, or Coursera - we&apos;re completely free.
                        Get personalized AI tutoring, smart practice problems, and track your progress.
                    </p>

                    <div className="flex flex-col sm:flex-row gap-4 justify-center pt-6">
                        <a
                            href="https://github.com/AB0204/PadhAI-Dost"
                            target="_blank"
                            rel="noopener noreferrer"
                        >
                            <Button size="lg" className="text-lg px-8">
                                <Github className="mr-2 h-5 w-5" />
                                View on GitHub
                            </Button>
                        </a>
                        <a
                            href="https://github.com/AB0204/PadhAI-Dost"
                            target="_blank"
                            rel="noopener noreferrer"
                        >
                            <Button size="lg" variant="outline" className="text-lg px-8">
                                <Star className="mr-2 h-5 w-5" />
                                Star the Repo
                            </Button>
                        </a>
                    </div>

                    <p className="text-sm text-gray-500 dark:text-gray-400 pt-4">
                        🚧 Authentication & full app coming soon! Follow the repo for updates.
                    </p>
                </div>
            </section>

            {/* Features Section */}
            <section className="container mx-auto px-4 py-16">
                <h2 className="text-3xl md:text-4xl font-bold text-center mb-12">
                    Everything You Need to Learn
                </h2>

                <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
                    <FeatureCard
                        icon={<Brain className="h-8 w-8 text-blue-600" />}
                        title="AI Tutoring"
                        description="24/7 personalized help from AI that adapts to your learning style"
                        status="Coming Soon"
                    />
                    <FeatureCard
                        icon={<BookOpen className="h-8 w-8 text-purple-600" />}
                        title="Smart Practice"
                        description="Auto-generated problems tailored to your current skill level"
                        status="Coming Soon"
                    />
                    <FeatureCard
                        icon={<Trophy className="h-8 w-8 text-yellow-600" />}
                        title="Gamification"
                        description="Earn XP, badges, and compete on leaderboards while learning"
                        status="Coming Soon"
                    />
                    <FeatureCard
                        icon={<Users className="h-8 w-8 text-green-600" />}
                        title="Study Groups"
                        description="Collaborate with peers and learn together"
                        status="Coming Soon"
                    />
                </div>
            </section>

            {/* Why Free Section */}
            <section className="container mx-auto px-4 py-16 bg-blue-50 dark:bg-gray-800 rounded-lg my-16">
                <div className="max-w-3xl mx-auto text-center space-y-4">
                    <h2 className="text-3xl md:text-4xl font-bold">Why Free?</h2>
                    <p className="text-lg text-gray-600 dark:text-gray-300">
                        Education should be accessible to everyone, regardless of financial background.
                        PadhAI-Dost is built by students who struggled with expensive tools, and we&apos;re
                        committed to keeping core features free forever.
                    </p>
                    <p className="text-base text-gray-500 dark:text-gray-400">
                        If you find it helpful, consider starring our repo, sharing with friends,
                        or contributing to make it even better!
                    </p>
                </div>
            </section>

            {/* Development Status */}
            <section className="container mx-auto px-4 py-16">
                <div className="max-w-3xl mx-auto bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8">
                    <h2 className="text-2xl md:text-3xl font-bold text-center mb-6">
                        🚀 Development Roadmap
                    </h2>
                    <div className="space-y-4">
                        <RoadmapItem status="done" text="Landing Page & Design System" />
                        <RoadmapItem status="progress" text="AI Backend Integration" />
                        <RoadmapItem status="planned" text="User Authentication" />
                        <RoadmapItem status="planned" text="Flashcard Generation" />
                        <RoadmapItem status="planned" text="Study Analytics" />
                        <RoadmapItem status="planned" text="Mobile App" />
                    </div>
                    <div className="text-center mt-8">
                        <a
                            href="https://github.com/AB0204/PadhAI-Dost/issues"
                            target="_blank"
                            rel="noopener noreferrer"
                        >
                            <Button size="lg" variant="outline">
                                Contribute on GitHub
                                <ArrowRight className="ml-2 h-5 w-5" />
                            </Button>
                        </a>
                    </div>
                </div>
            </section>

            {/* Footer */}
            <footer className="border-t bg-gray-50 dark:bg-gray-900 py-8">
                <div className="container mx-auto px-4 text-center text-gray-600 dark:text-gray-400">
                    <p>Built with ❤️ by students, for students</p>
                    <p className="text-sm mt-2">Education is a right, not a privilege. 🎓</p>
                    <div className="flex justify-center gap-4 mt-4">
                        <a
                            href="https://github.com/AB0204/PadhAI-Dost"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-600 hover:text-blue-700 dark:text-blue-400"
                        >
                            GitHub
                        </a>
                        <span>•</span>
                        <a
                            href="https://github.com/AB0204/PadhAI-Dost/blob/main/README.md"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-600 hover:text-blue-700 dark:text-blue-400"
                        >
                            Documentation
                        </a>
                        <span>•</span>
                        <a
                            href="https://github.com/AB0204/PadhAI-Dost/blob/main/CONTRIBUTING.md"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-600 hover:text-blue-700 dark:text-blue-400"
                        >
                            Contribute
                        </a>
                    </div>
                </div>
            </footer>
        </div>
    );
}

function FeatureCard({
    icon,
    title,
    description,
    status
}: {
    icon: React.ReactNode;
    title: string;
    description: string;
    status?: string;
}) {
    return (
        <div className="p-6 bg-white dark:bg-gray-800 rounded-lg shadow-lg hover:shadow-xl transition-shadow">
            <div className="mb-4">{icon}</div>
            <h3 className="text-xl font-semibold mb-2">{title}</h3>
            <p className="text-gray-600 dark:text-gray-400 mb-3">{description}</p>
            {status && (
                <span className="inline-block px-3 py-1 text-xs font-semibold rounded-full bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200">
                    {status}
                </span>
            )}
        </div>
    );
}

function RoadmapItem({ status, text }: { status: "done" | "progress" | "planned"; text: string }) {
    const icons = {
        done: "✅",
        progress: "🔄",
        planned: "📋"
    };

    return (
        <div className="flex items-center gap-3 text-lg">
            <span className="text-2xl">{icons[status]}</span>
            <span className={status === "done" ? "text-gray-500 line-through" : ""}>{text}</span>
        </div>
    );
}
