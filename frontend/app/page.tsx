"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  ArrowRight,
  MessageCircle,
  BookOpen,
  Trophy,
  Zap,
  Code,
  Database,
  Cpu,
  Globe,
} from "lucide-react";

const topics = [
  { name: "DSA", icon: Code, description: "Master algorithms with real-world problems" },
  { name: "System Design", icon: Database, description: "Design scalable systems like Netflix" },
  { name: "LLD", icon: Cpu, description: "Low-level design and SOLID principles" },
  { name: "Applied AI", icon: Zap, description: "Build production AI systems" },
  { name: "Networks", icon: Globe, description: "Deep dive into networking" },
  { name: "And More...", icon: BookOpen, description: "OS, DBMS, Backend, Distributed Systems" },
];

const features = [
  {
    icon: MessageCircle,
    title: "WhatsApp Delivery",
    description: "Daily hook messages right where you already are",
  },
  {
    icon: BookOpen,
    title: "Real-World Context",
    description: "Learn how Netflix, Google, and Amazon solve problems",
  },
  {
    icon: Trophy,
    title: "Gamified Progress",
    description: "Streaks, badges, and visual progress tracking",
  },
  {
    icon: Zap,
    title: "Personalized Learning",
    description: "AI analyzes your resume to create custom roadmaps",
  },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <span className="text-2xl font-bold text-primary">DailyDev</span>
          </div>
          <div className="flex items-center space-x-4">
            <Link href="/login">
              <Button variant="ghost">Login</Button>
            </Link>
            <Link href="/signup">
              <Button>Get Started Free</Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto text-center max-w-4xl">
          <h1 className="text-4xl md:text-6xl font-bold mb-6">
            Interview Prep,{" "}
            <span className="text-primary">One Day at a Time</span>
          </h1>
          <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
            Transform interview preparation into a daily habit through bite-sized,
            real-world problem-driven learning delivered via WhatsApp.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/signup">
              <Button size="lg" className="w-full sm:w-auto">
                Start Learning Free <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </Link>
            <Link href="#features">
              <Button size="lg" variant="outline" className="w-full sm:w-auto">
                See How It Works
              </Button>
            </Link>
          </div>
          <p className="text-sm text-muted-foreground mt-4">
            100% Free. No credit card required.
          </p>
        </div>
      </section>

      {/* How it Works */}
      <section className="py-16 px-4 bg-muted/50">
        <div className="container mx-auto max-w-5xl">
          <h2 className="text-3xl font-bold text-center mb-12">
            How DailyDev Works
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-primary">1</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Morning Hook</h3>
              <p className="text-muted-foreground">
                Wake up to a real-world engineering problem from companies like
                Netflix or Uber on WhatsApp.
              </p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-primary">2</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Reply "YES"</h3>
              <p className="text-muted-foreground">
                Curious? Just reply YES to get a detailed article with ELI5
                explanation, code, and practice problems.
              </p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-primary">3</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Build Streaks</h3>
              <p className="text-muted-foreground">
                Learn consistently, track your progress, and watch your
                interview readiness grow day by day.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Example Message */}
      <section className="py-16 px-4">
        <div className="container mx-auto max-w-3xl">
          <h2 className="text-3xl font-bold text-center mb-8">
            Your Daily Hook Message
          </h2>
          <Card className="bg-green-50 dark:bg-green-950 border-green-200 dark:border-green-800">
            <CardContent className="p-6">
              <div className="flex items-start space-x-3">
                <div className="w-10 h-10 bg-green-500 rounded-full flex items-center justify-center flex-shrink-0">
                  <MessageCircle className="h-5 w-5 text-white" />
                </div>
                <div className="bg-white dark:bg-gray-900 rounded-lg p-4 shadow-sm max-w-md">
                  <p className="text-sm">
                    <span className="text-lg">🚀</span> <strong>Real-World Problem:</strong>
                    <br /><br />
                    Netflix streams 4K video to millions simultaneously without
                    buffering. When you click "play", how does a single server
                    in LA instantly deliver content to users in Tokyo, Mumbai,
                    and São Paulo?
                    <br /><br />
                    This is the <strong>CDN + Consistent Hashing</strong> problem.
                    <br /><br />
                    Want to learn how top companies solve this?
                    <br />
                    Reply <strong>'YES'</strong> 🎯
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="py-16 px-4 bg-muted/50">
        <div className="container mx-auto max-w-5xl">
          <h2 className="text-3xl font-bold text-center mb-12">
            Why Engineers Love DailyDev
          </h2>
          <div className="grid md:grid-cols-2 gap-6">
            {features.map((feature, index) => (
              <Card key={index}>
                <CardHeader>
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center">
                      <feature.icon className="h-5 w-5 text-primary" />
                    </div>
                    <CardTitle className="text-lg">{feature.title}</CardTitle>
                  </div>
                </CardHeader>
                <CardContent>
                  <CardDescription>{feature.description}</CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Topics */}
      <section className="py-16 px-4">
        <div className="container mx-auto max-w-5xl">
          <h2 className="text-3xl font-bold text-center mb-4">
            Topics You Can Master
          </h2>
          <p className="text-center text-muted-foreground mb-12 max-w-2xl mx-auto">
            Choose your focus areas and get a personalized 30, 60, or 90-day
            roadmap tailored to your current skills.
          </p>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {topics.map((topic, index) => (
              <Card key={index} className="hover:border-primary transition-colors cursor-pointer">
                <CardContent className="p-4 text-center">
                  <topic.icon className="h-8 w-8 mx-auto mb-2 text-primary" />
                  <h3 className="font-semibold">{topic.name}</h3>
                  <p className="text-xs text-muted-foreground mt-1">
                    {topic.description}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 px-4 bg-primary text-primary-foreground">
        <div className="container mx-auto text-center max-w-3xl">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Ready to Transform Your Interview Prep?
          </h2>
          <p className="text-lg opacity-90 mb-8">
            Join thousands of engineers building their skills one day at a time.
            Completely free, forever.
          </p>
          <Link href="/signup">
            <Button size="lg" variant="secondary">
              Start Your Journey <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 px-4 border-t">
        <div className="container mx-auto text-center text-muted-foreground">
          <p>Built with passion for the developer community.</p>
          <p className="text-sm mt-2">
            DailyDev - Free Daily Interview Prep Platform
          </p>
        </div>
      </footer>
    </div>
  );
}
