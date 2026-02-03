"use client";

import { useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { useQuery } from "@tanstack/react-query";
import { articlesApi } from "@/lib/api";
import { useAuthStore, useThemeStore } from "@/lib/store";
import {
  Loader2,
  ArrowLeft,
  BookOpen,
  ChevronRight,
  Moon,
  Sun,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { format } from "date-fns";

export default function LibraryPage() {
  const router = useRouter();
  const { isAuthenticated } = useAuthStore();
  const { theme, toggleTheme } = useThemeStore();

  useEffect(() => {
    if (!isAuthenticated) {
      router.push("/login");
    }
  }, [isAuthenticated, router]);

  const { data: savedArticles, isLoading } = useQuery({
    queryKey: ["savedArticles"],
    queryFn: async () => {
      const response = await articlesApi.getSaved();
      return response.data;
    },
    enabled: isAuthenticated,
  });

  if (!isAuthenticated) return null;

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b sticky top-0 bg-background z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <Link href="/dashboard">
              <Button variant="ghost" size="icon">
                <ArrowLeft className="h-5 w-5" />
              </Button>
            </Link>
            <h1 className="text-xl font-semibold">My Library</h1>
          </div>
          <Button variant="ghost" size="icon" onClick={toggleTheme}>
            {theme === "light" ? (
              <Moon className="h-5 w-5" />
            ) : (
              <Sun className="h-5 w-5" />
            )}
          </Button>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8 max-w-3xl">
        {isLoading ? (
          <div className="flex justify-center py-16">
            <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
          </div>
        ) : savedArticles?.length > 0 ? (
          <div className="space-y-4">
            {savedArticles.map((article: any) => (
              <Link key={article.id} href={`/article/${article.id}`}>
                <Card className="hover:border-primary transition-colors cursor-pointer">
                  <CardContent className="py-4">
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-1">
                          <span className="text-sm text-muted-foreground">
                            {article.topic_name}
                          </span>
                          <span className="text-muted-foreground">·</span>
                          <span className="text-sm text-muted-foreground">
                            Day {article.day_number}
                          </span>
                        </div>
                        <h3 className="font-semibold">{article.title}</h3>
                        <div className="flex items-center space-x-3 mt-2">
                          <span
                            className={cn(
                              "text-xs px-2 py-0.5 rounded-full",
                              article.difficulty === "easy"
                                ? "bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300"
                                : article.difficulty === "medium"
                                ? "bg-yellow-100 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-300"
                                : "bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300"
                            )}
                          >
                            {article.difficulty}
                          </span>
                          <span className="text-xs text-muted-foreground">
                            ~{article.avg_read_time} min
                          </span>
                          <span className="text-xs text-muted-foreground">
                            Saved{" "}
                            {format(new Date(article.saved_at), "MMM d, yyyy")}
                          </span>
                        </div>
                        {article.notes && (
                          <p className="text-sm text-muted-foreground mt-2 line-clamp-2">
                            {article.notes}
                          </p>
                        )}
                      </div>
                      <ChevronRight className="h-5 w-5 text-muted-foreground ml-4" />
                    </div>
                  </CardContent>
                </Card>
              </Link>
            ))}
          </div>
        ) : (
          <div className="text-center py-16">
            <BookOpen className="h-16 w-16 mx-auto text-muted-foreground mb-4" />
            <h2 className="text-xl font-semibold mb-2">Your library is empty</h2>
            <p className="text-muted-foreground mb-6">
              Save articles while learning to build your personal knowledge base
            </p>
            <Link href="/dashboard">
              <Button>Go to Dashboard</Button>
            </Link>
          </div>
        )}
      </main>
    </div>
  );
}
