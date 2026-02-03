"use client";

import { useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { useQuery } from "@tanstack/react-query";
import { userApi, topicsApi, roadmapApi } from "@/lib/api";
import { useAuthStore } from "@/lib/store";
import {
  Loader2,
  Flame,
  BookOpen,
  Trophy,
  ChevronRight,
  MessageCircle,
  Settings,
  LogOut,
  Moon,
  Sun,
} from "lucide-react";
import { useThemeStore } from "@/lib/store";
import { cn } from "@/lib/utils";

export default function DashboardPage() {
  const router = useRouter();
  const { user, isAuthenticated, logout } = useAuthStore();
  const { theme, toggleTheme } = useThemeStore();

  useEffect(() => {
    if (!isAuthenticated) {
      router.push("/login");
    }
  }, [isAuthenticated, router]);

  // Fetch user stats
  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ["userStats"],
    queryFn: async () => {
      const response = await userApi.getStats();
      return response.data;
    },
    enabled: isAuthenticated,
  });

  // Fetch user topics
  const { data: myTopics, isLoading: topicsLoading } = useQuery({
    queryKey: ["myTopics"],
    queryFn: async () => {
      const response = await topicsApi.getMyTopics();
      return response.data;
    },
    enabled: isAuthenticated,
  });

  // Fetch today's concept
  const { data: todayConcept } = useQuery({
    queryKey: ["todayConcept"],
    queryFn: async () => {
      const response = await roadmapApi.getToday();
      return response.data;
    },
    enabled: isAuthenticated,
  });

  const handleLogout = () => {
    logout();
    router.push("/");
  };

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b sticky top-0 bg-background z-50">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <Link href="/dashboard" className="text-2xl font-bold text-primary">
            DailyDev
          </Link>
          <div className="flex items-center space-x-4">
            <Button variant="ghost" size="icon" onClick={toggleTheme}>
              {theme === "light" ? (
                <Moon className="h-5 w-5" />
              ) : (
                <Sun className="h-5 w-5" />
              )}
            </Button>
            <Link href="/library">
              <Button variant="ghost" size="icon">
                <BookOpen className="h-5 w-5" />
              </Button>
            </Link>
            <Link href="/settings">
              <Button variant="ghost" size="icon">
                <Settings className="h-5 w-5" />
              </Button>
            </Link>
            <Button variant="ghost" size="icon" onClick={handleLogout}>
              <LogOut className="h-5 w-5" />
            </Button>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">
            Welcome back, {user?.name || "Learner"}!
          </h1>
          <p className="text-muted-foreground">
            Keep building your skills one day at a time.
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center space-x-2">
                <Flame className="h-5 w-5 text-orange-500" />
                <span className="text-2xl font-bold">
                  {statsLoading ? "-" : stats?.current_streak || 0}
                </span>
              </div>
              <p className="text-sm text-muted-foreground mt-1">Day Streak</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center space-x-2">
                <BookOpen className="h-5 w-5 text-primary" />
                <span className="text-2xl font-bold">
                  {statsLoading ? "-" : stats?.total_concepts_learned || 0}
                </span>
              </div>
              <p className="text-sm text-muted-foreground mt-1">
                Concepts Learned
              </p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center space-x-2">
                <Trophy className="h-5 w-5 text-yellow-500" />
                <span className="text-2xl font-bold">
                  {statsLoading ? "-" : stats?.longest_streak || 0}
                </span>
              </div>
              <p className="text-sm text-muted-foreground mt-1">Best Streak</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center space-x-2">
                <MessageCircle className="h-5 w-5 text-green-500" />
                <span className="text-2xl font-bold">
                  {user?.whatsapp_connected === "connected" ? "On" : "Off"}
                </span>
              </div>
              <p className="text-sm text-muted-foreground mt-1">WhatsApp</p>
            </CardContent>
          </Card>
        </div>

        {/* Today's Concept */}
        {todayConcept && !todayConcept.message && (
          <Card className="mb-8 border-primary">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="flex items-center gap-2">
                    <span className="text-xl">🎯</span>
                    Today&apos;s Concept
                  </CardTitle>
                  <CardDescription>
                    Day {todayConcept.day_number} - {todayConcept.topic_name}
                  </CardDescription>
                </div>
                <span
                  className={cn(
                    "px-2 py-1 text-xs rounded-full",
                    todayConcept.difficulty === "easy"
                      ? "bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300"
                      : todayConcept.difficulty === "medium"
                      ? "bg-yellow-100 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-300"
                      : "bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300"
                  )}
                >
                  {todayConcept.difficulty}
                </span>
              </div>
            </CardHeader>
            <CardContent>
              <h3 className="text-xl font-semibold mb-2">
                {todayConcept.concept_title}
              </h3>
              {todayConcept.hook_message && (
                <p className="text-muted-foreground mb-4 whitespace-pre-line">
                  {todayConcept.hook_message}
                </p>
              )}
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">
                  ~{todayConcept.estimated_read_time} min read
                </span>
                {todayConcept.has_article ? (
                  <Link href={`/article/${todayConcept.article_id}`}>
                    <Button>
                      Read Article <ChevronRight className="ml-2 h-4 w-4" />
                    </Button>
                  </Link>
                ) : (
                  <Link href={`/article/${todayConcept.id}?generate=true`}>
                    <Button>
                      Generate Article <ChevronRight className="ml-2 h-4 w-4" />
                    </Button>
                  </Link>
                )}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Topics Progress */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold">Your Topics</h2>
            <Link href="/onboarding">
              <Button variant="outline" size="sm">
                Add Topics
              </Button>
            </Link>
          </div>
          {topicsLoading ? (
            <div className="flex justify-center py-8">
              <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
            </div>
          ) : myTopics?.length > 0 ? (
            <div className="space-y-4">
              {myTopics.map((topic: any) => (
                <Card key={topic.topic_id}>
                  <CardContent className="pt-6">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center space-x-3">
                        <span className="text-2xl">{topic.topic_icon}</span>
                        <div>
                          <h3 className="font-semibold">{topic.topic_name}</h3>
                          <p className="text-sm text-muted-foreground">
                            {topic.progress.completed} / {topic.progress.total}{" "}
                            concepts
                          </p>
                        </div>
                      </div>
                      <Link href={`/roadmap/${topic.topic_id}`}>
                        <Button variant="ghost" size="sm">
                          View <ChevronRight className="ml-1 h-4 w-4" />
                        </Button>
                      </Link>
                    </div>
                    <Progress
                      value={topic.progress.percentage}
                      className="h-2"
                    />
                    <div className="flex justify-between mt-2 text-xs text-muted-foreground">
                      <span>{topic.progress.percentage}% complete</span>
                      <span className="flex items-center">
                        <Flame className="h-3 w-3 mr-1 text-orange-500" />
                        {topic.progress.streak} day streak
                      </span>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <Card>
              <CardContent className="py-8 text-center">
                <p className="text-muted-foreground mb-4">
                  You haven&apos;t selected any topics yet.
                </p>
                <Link href="/onboarding">
                  <Button>Select Topics</Button>
                </Link>
              </CardContent>
            </Card>
          )}
        </div>

        {/* WhatsApp Connection */}
        {user?.whatsapp_connected !== "connected" && (
          <Card className="bg-green-50 dark:bg-green-950 border-green-200 dark:border-green-800">
            <CardContent className="py-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <MessageCircle className="h-8 w-8 text-green-600" />
                  <div>
                    <h3 className="font-semibold">Connect WhatsApp</h3>
                    <p className="text-sm text-muted-foreground">
                      Get daily learning hooks delivered to your WhatsApp
                    </p>
                  </div>
                </div>
                <Link href="/settings">
                  <Button variant="outline">Connect</Button>
                </Link>
              </div>
            </CardContent>
          </Card>
        )}
      </main>
    </div>
  );
}
