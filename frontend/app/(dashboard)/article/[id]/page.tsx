"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams, useSearchParams, useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { useQuery, useMutation } from "@tanstack/react-query";
import { articlesApi } from "@/lib/api";
import { useAuthStore, useThemeStore } from "@/lib/store";
import ReactMarkdown from "react-markdown";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import {
  oneDark,
  oneLight,
} from "react-syntax-highlighter/dist/esm/styles/prism";
import {
  Loader2,
  ArrowLeft,
  Bookmark,
  BookmarkCheck,
  Copy,
  Check,
  ExternalLink,
  ChevronDown,
  ChevronUp,
  Moon,
  Sun,
} from "lucide-react";
import { cn } from "@/lib/utils";

export default function ArticlePage() {
  const params = useParams();
  const searchParams = useSearchParams();
  const router = useRouter();
  const { isAuthenticated } = useAuthStore();
  const { theme, toggleTheme } = useThemeStore();
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);
  const [expandedSections, setExpandedSections] = useState<string[]>([
    "eli5",
    "technical",
    "code",
    "real_world",
    "practice",
  ]);

  const articleId = params.id as string;
  const shouldGenerate = searchParams.get("generate") === "true";

  useEffect(() => {
    if (!isAuthenticated) {
      router.push("/login");
    }
  }, [isAuthenticated, router]);

  // Generate article if needed
  const generateMutation = useMutation({
    mutationFn: async () => {
      const response = await articlesApi.generate(articleId);
      return response.data;
    },
  });

  useEffect(() => {
    if (shouldGenerate && !generateMutation.isPending && !generateMutation.data) {
      generateMutation.mutate();
    }
  }, [shouldGenerate]);

  // Fetch article
  const {
    data: article,
    isLoading,
    refetch,
  } = useQuery({
    queryKey: ["article", generateMutation.data?.article_id || articleId],
    queryFn: async () => {
      const id = generateMutation.data?.article_id || articleId;
      const response = await articlesApi.getById(id);
      return response.data;
    },
    enabled: isAuthenticated && (!shouldGenerate || !!generateMutation.data),
  });

  // Save mutation
  const saveMutation = useMutation({
    mutationFn: async () => {
      if (article?.is_saved) {
        await articlesApi.unsave(article.id);
      } else {
        await articlesApi.save(article.id);
      }
    },
    onSuccess: () => refetch(),
  });

  const copyCode = (code: string, index: number) => {
    navigator.clipboard.writeText(code);
    setCopiedIndex(index);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  const toggleSection = (section: string) => {
    setExpandedSections((prev) =>
      prev.includes(section)
        ? prev.filter((s) => s !== section)
        : [...prev, section]
    );
  };

  if (!isAuthenticated) return null;

  if (generateMutation.isPending) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-background">
        <Loader2 className="h-12 w-12 animate-spin text-primary mb-4" />
        <p className="text-lg font-medium">Generating your article...</p>
        <p className="text-muted-foreground">This may take a few seconds</p>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <Loader2 className="h-12 w-12 animate-spin text-primary" />
      </div>
    );
  }

  if (!article) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-background">
        <p className="text-lg mb-4">Article not found</p>
        <Link href="/dashboard">
          <Button>Back to Dashboard</Button>
        </Link>
      </div>
    );
  }

  const Section = ({
    id,
    title,
    children,
  }: {
    id: string;
    title: string;
    children: React.ReactNode;
  }) => (
    <div className="border-b last:border-b-0">
      <button
        onClick={() => toggleSection(id)}
        className="w-full py-4 flex items-center justify-between text-left hover:bg-muted/50 transition-colors"
      >
        <h2 className="text-xl font-semibold">{title}</h2>
        {expandedSections.includes(id) ? (
          <ChevronUp className="h-5 w-5 text-muted-foreground" />
        ) : (
          <ChevronDown className="h-5 w-5 text-muted-foreground" />
        )}
      </button>
      {expandedSections.includes(id) && (
        <div className="pb-6 prose dark:prose-invert max-w-none">{children}</div>
      )}
    </div>
  );

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
            <div>
              <p className="text-sm text-muted-foreground">
                {article.topic_name} - Day {article.day_number}
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <Button variant="ghost" size="icon" onClick={toggleTheme}>
              {theme === "light" ? (
                <Moon className="h-5 w-5" />
              ) : (
                <Sun className="h-5 w-5" />
              )}
            </Button>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => saveMutation.mutate()}
              disabled={saveMutation.isPending}
            >
              {article.is_saved ? (
                <BookmarkCheck className="h-5 w-5 text-primary" />
              ) : (
                <Bookmark className="h-5 w-5" />
              )}
            </Button>
          </div>
        </div>
      </header>

      {/* Content */}
      <main className="container mx-auto px-4 py-8 max-w-3xl">
        {/* Title */}
        <div className="mb-8">
          <h1 className="text-3xl md:text-4xl font-bold mb-4">
            {article.title}
          </h1>
          <div className="flex items-center space-x-4 text-sm text-muted-foreground">
            <span
              className={cn(
                "px-2 py-1 rounded-full",
                article.difficulty === "easy"
                  ? "bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300"
                  : article.difficulty === "medium"
                  ? "bg-yellow-100 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-300"
                  : "bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300"
              )}
            >
              {article.difficulty}
            </span>
            <span>~{article.avg_read_time} min read</span>
            <span>{article.view_count} views</span>
          </div>
        </div>

        {/* Article Sections */}
        <div className="space-y-0">
          {/* ELI5 */}
          {article.eli5_content && (
            <Section id="eli5" title="🎈 Explain Like I'm 5">
              <ReactMarkdown>{article.eli5_content}</ReactMarkdown>
            </Section>
          )}

          {/* Technical Deep Dive */}
          {article.technical_content && (
            <Section id="technical" title="🔬 Technical Deep Dive">
              <ReactMarkdown>{article.technical_content}</ReactMarkdown>
            </Section>
          )}

          {/* Code Snippets */}
          {article.code_snippets && article.code_snippets.length > 0 && (
            <Section id="code" title="💻 Code Implementation">
              {article.code_snippets.map((snippet: any, index: number) => (
                <div key={index} className="mb-6">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium capitalize">
                      {snippet.language}
                    </span>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => copyCode(snippet.code, index)}
                    >
                      {copiedIndex === index ? (
                        <Check className="h-4 w-4 mr-1" />
                      ) : (
                        <Copy className="h-4 w-4 mr-1" />
                      )}
                      {copiedIndex === index ? "Copied!" : "Copy"}
                    </Button>
                  </div>
                  <SyntaxHighlighter
                    language={snippet.language.toLowerCase()}
                    style={theme === "dark" ? oneDark : oneLight}
                    customStyle={{
                      borderRadius: "0.5rem",
                      fontSize: "0.875rem",
                    }}
                  >
                    {snippet.code}
                  </SyntaxHighlighter>
                  {snippet.explanation && (
                    <p className="text-sm text-muted-foreground mt-2">
                      {snippet.explanation}
                    </p>
                  )}
                </div>
              ))}
            </Section>
          )}

          {/* Real World Examples */}
          {article.real_world_examples && (
            <Section id="real_world" title="🌍 Real-World Examples">
              <ReactMarkdown>{article.real_world_examples}</ReactMarkdown>
            </Section>
          )}

          {/* Practice Problems */}
          {article.practice_problems && article.practice_problems.length > 0 && (
            <Section id="practice" title="📝 Practice Problems">
              <div className="space-y-4">
                {article.practice_problems.map((problem: any, index: number) => (
                  <Card key={index}>
                    <CardContent className="py-4">
                      <div className="flex items-start justify-between">
                        <div>
                          <h4 className="font-medium">{problem.question}</h4>
                          <span
                            className={cn(
                              "text-xs px-2 py-0.5 rounded-full mt-2 inline-block",
                              problem.difficulty === "easy"
                                ? "bg-green-100 text-green-700"
                                : problem.difficulty === "medium"
                                ? "bg-yellow-100 text-yellow-700"
                                : "bg-red-100 text-red-700"
                            )}
                          >
                            {problem.difficulty}
                          </span>
                        </div>
                        {problem.link && (
                          <a
                            href={problem.link}
                            target="_blank"
                            rel="noopener noreferrer"
                          >
                            <Button variant="ghost" size="sm">
                              <ExternalLink className="h-4 w-4" />
                            </Button>
                          </a>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </Section>
          )}
        </div>

        {/* Footer */}
        <div className="mt-8 pt-8 border-t flex items-center justify-between">
          <Link href="/dashboard">
            <Button variant="outline">
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back to Dashboard
            </Button>
          </Link>
          <Button
            variant={article.is_saved ? "secondary" : "default"}
            onClick={() => saveMutation.mutate()}
            disabled={saveMutation.isPending}
          >
            {article.is_saved ? (
              <>
                <BookmarkCheck className="mr-2 h-4 w-4" />
                Saved
              </>
            ) : (
              <>
                <Bookmark className="mr-2 h-4 w-4" />
                Save to Library
              </>
            )}
          </Button>
        </div>
      </main>
    </div>
  );
}
